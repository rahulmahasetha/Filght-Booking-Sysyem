from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Contact, Airport, Airline, Flight, Booking, Passenger, Payment
from django.contrib.auth.models import User
from datetime import datetime, date
import random

# Home and static pages views
def index(request):
    featured_airports = Airport.objects.all()[:4]
    featured_airlines = Airline.objects.all()[:3]
    return render(request, 'index.html', {
        'featured_airports': featured_airports,
        'featured_airlines': featured_airlines,
    })

def about(request):
    return render(request, 'about.html')

def service(request):
    return render(request, 'services.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        pincode = request.POST.get('pincode')
        message = request.POST.get('message')
        contact = Contact(
            name=name, 
            email=email, 
            phone=phone, 
            pincode=pincode, 
            message=message,
            date=datetime.now()
        )
        contact.save()
        messages.success(request, "Your message has been sent successfully!")
        return redirect('contact')
    
    return render(request, 'contact.html')

# Flight booking views
def flight_search(request):
    if request.method == 'POST':
        departure = request.POST.get('departure')
        arrival = request.POST.get('arrival')
        date_str = request.POST.get('date')
        passengers = int(request.POST.get('passengers', 1))
        travel_class = request.POST.get('class', 'ECONOMY')
        
        try:
            # Convert string date to datetime object
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
            flights = Flight.objects.filter(
                departure_airport_id=departure,
                arrival_airport_id=arrival,
                departure_time__date=date_obj
            )
            
            # Filter by available seats
            if travel_class == 'ECONOMY':
                flights = flights.filter(economy_seats__gte=passengers)
            elif travel_class == 'BUSINESS':
                flights = flights.filter(business_seats__gte=passengers)
            elif travel_class == 'FIRST':
                flights = flights.filter(first_class_seats__gte=passengers)
            
            return render(request, 'search_results.html', {
                'flights': flights.order_by('departure_time'),
                'passengers': passengers,
                'travel_class': travel_class,
                'search_data': request.POST
            })
            
        except ValueError:
            messages.error(request, "Invalid date format")
            return redirect('flight_search')
    
    airports = Airport.objects.all()
    return render(request, 'search.html', {'airports': airports})

@login_required
def book_flight(request, flight_id):
    flight = get_object_or_404(Flight, pk=flight_id)
    
    if request.method == 'POST':
        passengers = int(request.POST.get('total_passengers', 1))
        travel_class = request.POST.get('travel_class')
        
        # Validate passenger data first
        passenger_details = []
        for i in range(1, passengers + 1):
            first_name = request.POST.get(f'passenger_{i}_first_name', '').strip()
            last_name = request.POST.get(f'passenger_{i}_last_name', '').strip()
            dob_str = request.POST.get(f'passenger_{i}_dob', '')
            id_type = request.POST.get(f'passenger_{i}_id_type', '')
            id_number = request.POST.get(f'passenger_{i}_id_number', '').strip()
            passport_number = request.POST.get(f'passenger_{i}_passport_number', '').strip()
            
            if not all([first_name, last_name, dob_str, id_type, id_number]):
                messages.error(request, "Please provide complete details for all passengers")
                return redirect(request.path)
            
            try:
                dob = datetime.strptime(dob_str, '%Y-%m-%d').date()
            except ValueError:
                messages.error(request, "Invalid date format for passenger date of birth")
                return redirect(request.path)
                
            passenger_details.append({
                'first_name': first_name,
                'last_name': last_name,
                'date_of_birth': dob,
                'id_type': id_type,
                'id_number': id_number,
                'passport_number': passport_number
            })
        
        
        # Calculate price
        if travel_class == 'ECONOMY':
            price = flight.economy_price
            available_seats = flight.economy_seats
        elif travel_class == 'BUSINESS':
            price = flight.business_price
            available_seats = flight.business_seats
        elif travel_class == 'FIRST':
            price = flight.first_class_price
            available_seats = flight.first_class_seats
        
        # Check seat availability
        if available_seats < passengers:
            messages.error(request, "Not enough seats available")
            return redirect('flight_search')
        
        total_price = price * passengers
        
        # Create booking
        booking = Booking(
            user=request.user,
            flight=flight,
            nums_passengers=passengers,
            travel_class=travel_class,
            total_price=total_price
        )
        booking.save()
        
        # Create passengers
        for detail in passenger_details:
            Passenger.objects.create(
                booking=booking,
                first_name=detail['first_name'],
                last_name=detail['last_name'],
                date_of_birth=detail['date_of_birth'],
                id_type=detail['id_type'],
                id_number=detail['id_number'],
                passport_number=detail['passport_number']
            )
        # Update available seats
        if travel_class == 'ECONOMY':
            flight.economy_seats -= passengers
        elif travel_class == 'BUSINESS':
            flight.business_seats -= passengers
        elif travel_class == 'FIRST':
            flight.first_class_seats -= passengers
        flight.save()
        
        return redirect('payment', booking_id=booking.id)
    
    # GET request handling
    passengers = int(request.GET.get('passengers', 1))
    travel_class = request.GET.get('class', 'ECONOMY')
    
    if travel_class == 'ECONOMY':
        price = flight.economy_price
    elif travel_class == 'BUSINESS':
        price = flight.business_price
    elif travel_class == 'FIRST':
        price = flight.first_class_price
    
    total_price = price * passengers
    
    return render(request, 'book.html', {
        'flight': flight,
        'passengers': range(1, passengers + 1),
        'travel_class': travel_class,
        'price': price,
        'total_price': total_price,
    })

@login_required
def payment(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id, user=request.user)
    passengers = booking.passengers.all()
    # Debug output to verify prices
    #print(f"Booking Total Price: {booking.total_price}")
    #print(f"Calculated Price: {booking.per_passenger_price * booking.nums_passengers}")
    if passengers.count() != booking.nums_passengers:
        messages.warning(request, "Passenger count mismatch detected")
    
    price_breakdown = {
        'per_passenger': booking.per_passenger_price,
        'total': booking.total_price,
        'passenger_count': booking.nums_passengers
    }
    if request.method == 'POST':
        if Payment.objects.filter(booking=booking).exists():
            messages.info(request, "Payment already completed")
            return redirect('booking_detail', reference=booking.reference)

        payment = Payment.objects.create(
            booking=booking,
            amount=booking.total_price,  # Use the stored total price
            transaction_id=f"TX{random.randint(100000000, 999999999)}",
            status='COMPLETED'
        )
        
        messages.success(request, "Payment successful!")
        return redirect('booking_detail', reference=booking.reference)
    
    return render(request, 'payment.html', {
        'booking': booking,
        'passengers': passengers,
        'price_breakdown': price_breakdown,

        'stripe_public_key': settings.STRIPE_PUBLIC_KEY
    })
@login_required
def booking_detail(request, reference):
    booking = get_object_or_404(Booking, reference=reference, user=request.user)
    passengers = Passenger.objects.filter(booking=booking)
    payment = Payment.objects.filter(booking=booking).first()
    
    print(f"Booking Reference: {booking.reference}")
    print(f"Passengers Count: {passengers.count()}")
    print(f"Booking Passenger Count: {booking.nums_passengers}")
    print(f"Total Price: {booking.total_price}")
    
    price_breakdown = {
        'per_passenger': booking.per_passenger_price,
        'total': booking.total_price,
        'passenger_count': booking.nums_passengers
    }
    
    if not payment:
        messages.error(request, "Payment information not found")
        return redirect('my_bookings')
    
    return render(request, 'booking_detail.html', {
    'booking': booking,
    'passengers': passengers,
    'payment': payment,
    'price_breakdown': price_breakdown
})

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-booking_date')
    return render(request, 'my_bookings.html', {'bookings': bookings})

@login_required
def cancel_booking(request, reference):
    booking = get_object_or_404(Booking, reference=reference, user=request.user)
    
    if booking.status != 'CONFIRMED':
        messages.error(request, "Only confirmed bookings can be cancelled")
        return redirect('my_bookings')
    
    if request.method == 'POST':
        # Return seats to flight
        passenger_count = booking.passengers.count()
        if booking.travel_class == 'ECONOMY':
            booking.flight.economy_seats += passenger_count
        elif booking.travel_class == 'BUSINESS':
            booking.flight.business_seats += passenger_count
        elif booking.travel_class == 'FIRST':
            booking.flight.first_class_seats += passenger_count
        booking.flight.save()
        
        # Update booking status
        booking.status = 'CANCELLED'
        booking.save()
        
        messages.success(request, "Booking cancelled successfully")
        return redirect('my_bookings')
    
    return render(request, 'cancel_confirm.html', {'booking': booking})

# Authentication views
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                next_url = request.GET.get('next', 'home')
                return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        messages.info(request, "You have been logged out.")
    return redirect('home')

def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('home')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
    else:
        form = UserCreationForm()
    
    return render(request, 'register.html', {'form': form})

from django.http import JsonResponse
from .models import UserProfile

@login_required
def profile_view(request):
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)
    bookings = Booking.objects.filter(user=user).select_related('flight__airline', 'flight__departure_airport', 'flight__arrival_airport').order_by('-booking_date')
    
    # Dashboard Stats
    total_flights = bookings.count()
    upcoming_trips = bookings.filter(status='CONFIRMED', flight__departure_time__gt=datetime.now()).count()
    cancelled_trips = bookings.filter(status='CANCELLED').count()
    total_spent = sum([b.total_price for b in bookings if b.status == 'CONFIRMED'])
    
    return render(request, 'profile.html', {
        'user': user,
        'profile': profile,
        'recent_bookings': bookings[:5],
        'stats': {
            'total_flights': total_flights,
            'upcoming_trips': upcoming_trips,
            'cancelled_trips': cancelled_trips,
            'total_spent': total_spent,
        }
    })

@login_required
def update_profile(request):
    if request.method == 'POST':
        user = request.user
        profile, created = UserProfile.objects.get_or_create(user=user)
        
        # Update User fields
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.save()
        
        # Update Profile fields
        profile.phone = request.POST.get('phone', profile.phone)
        profile.address = request.POST.get('address', profile.address)
        profile.bio = request.POST.get('bio', profile.bio)
        profile.gender = request.POST.get('gender', profile.gender)
        
        dob = request.POST.get('dob')
        if dob:
            try:
                profile.dob = datetime.strptime(dob, '%Y-%m-%d').date()
            except ValueError:
                pass
                
        # Handle Image Upload
        if 'profile_picture' in request.FILES:
            profile.profile_picture = request.FILES['profile_picture']
            
        profile.save()
        
        profile_pic_url = profile.profile_picture.url if profile.profile_picture else ''
        
        return JsonResponse({
            'success': True,
            'message': 'Profile updated successfully',
            'data': {
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'phone': profile.phone,
                'address': profile.address,
                'bio': profile.bio,
                'gender': profile.gender,
                'dob': profile.dob.strftime('%Y-%m-%d') if profile.dob else '',
                'profile_picture': profile_pic_url
            }
        })
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum, Count, F
from django.utils import timezone

@staff_member_required
def admin_dashboard_api(request):
    """API endpoint to feed live data to the custom admin dashboard."""
    # Basic Counters
    total_flights = Flight.objects.count()
    active_flights = Flight.objects.filter(departure_time__gte=timezone.now()).count()
    total_bookings = Booking.objects.count()
    total_users = User.objects.count()
    total_cancellations = Booking.objects.filter(status='CANCELLED').count()
    
    # Revenue calculations
    total_revenue = Booking.objects.filter(status='CONFIRMED').aggregate(Sum('total_price'))['total_price__sum'] or 0
    pending_payments = Payment.objects.filter(status='PENDING').count()
    
    # Top Performing Flight
    top_flight = Flight.objects.annotate(
        num_bookings=Count('booking'),
        total_revenue=Sum('booking__total_price')
    ).order_by('-num_bookings').first()
    
    top_flight_data = None
    if top_flight:
        total_capacity = top_flight.economy_seats + top_flight.business_seats + top_flight.first_class_seats
        # Calculate occupancy (booked passengers / total capacity)
        booked_passengers = Booking.objects.filter(flight=top_flight, status='CONFIRMED').aggregate(Sum('nums_passengers'))['nums_passengers__sum'] or 0
        occupancy = int((booked_passengers / total_capacity * 100)) if total_capacity > 0 else 0
        
        top_flight_data = {
            'code': f"{top_flight.airline.code}{top_flight.flight_number}",
            'route': f"{top_flight.departure_airport.city} → {top_flight.arrival_airport.city}",
            'bookings': top_flight.num_bookings,
            'revenue': float(top_flight.total_revenue or 0),
            'occupancy': occupancy
        }
        
    # Low Seat Flights (Sum of all seats <= 20)
    # Using annotation to sum available seats
    low_seat_flights_query = Flight.objects.annotate(
        total_available=F('economy_seats') + F('business_seats') + F('first_class_seats')
    ).filter(total_available__lte=20, departure_time__gte=timezone.now()).order_by('total_available')[:5]
    
    low_seat_flights = []
    for flight in low_seat_flights_query:
        low_seat_flights.append({
            'code': f"{flight.airline.code}{flight.flight_number}",
            'route': f"{flight.departure_airport.city} → {flight.arrival_airport.city}",
            'seats': flight.total_available,
            'id': flight.id
        })
        
    # Chart Data (Mock trend for last 7 days for simplicity, but could be real)
    today = timezone.now().date()
    dates = [(today - timedelta(days=i)) for i in range(6, -1, -1)]
    revenue_chart_data = []
    bookings_chart_data = []
    
    for d in dates:
        day_bookings = Booking.objects.filter(booking_date__date=d, status='CONFIRMED')
        revenue_chart_data.append(float(day_bookings.aggregate(Sum('total_price'))['total_price__sum'] or 0))
        bookings_chart_data.append(day_bookings.count())

    return JsonResponse({
        'stats': {
            'total_flights': total_flights,
            'active_flights': active_flights,
            'total_bookings': total_bookings,
            'total_users': total_users,
            'total_revenue': float(total_revenue),
            'pending_payments': pending_payments,
            'total_cancellations': total_cancellations,
        },
        'top_flight': top_flight_data,
        'low_seat_flights': low_seat_flights,
        'charts': {
            'labels': [d.strftime('%b %d') for d in dates],
            'revenue': revenue_chart_data,
            'bookings': bookings_chart_data
        }
    })

def flight_availability_api(request):
    departure_id = request.GET.get('departure')
    arrival_id = request.GET.get('arrival')
    if not departure_id or not arrival_id:
        return JsonResponse({'error': 'Missing parameters'}, status=400)
    from django.utils import timezone
    flights = Flight.objects.filter(departure_airport_id=departure_id, arrival_airport_id=arrival_id, departure_time__gte=timezone.now())
    availability = {}
    for flight in flights:
        date_str = flight.departure_time.strftime('%Y-%m-%d')
        total_seats = flight.economy_seats + flight.business_seats + flight.first_class_seats
        if total_seats >= 20:
            status = 'green'
        elif total_seats > 0:
            status = 'yellow'
        else:
            status = 'red'
        if date_str not in availability:
            availability[date_str] = status
        else:
            current = availability[date_str]
            if status == 'green' or (status == 'yellow' and current == 'red'):
                availability[date_str] = status
    return JsonResponse(availability)

def reset_password_direct(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        new_password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if not all([username, new_password, confirm_password]):
            messages.error(request, 'All fields are required.')
            return redirect('login')
            
        if new_password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('login')
            
        try:
            user = User.objects.get(username=username)
            user.set_password(new_password)
            user.save()
            messages.success(request, 'Password updated successfully. You can now login.')
        except User.DoesNotExist:
            messages.error(request, 'Username not found.')
            
        return redirect('login')
    return redirect('login')
