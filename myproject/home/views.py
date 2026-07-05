from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Contact, Airport, Airline, Flight, Booking, Passenger, Payment, BookingSegment, Ticket
import random
from django.contrib.auth.models import User
from datetime import datetime, date
from decimal import Decimal
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

from datetime import timedelta
from django.db.models import Q

def find_routes(source_id, destination_id, travel_date, travel_class, passengers, max_stops=1):
    """
    Recursive helper to find routes (direct and connecting).
    Returns list of paths: [{'segments': [f1, f2], 'total_price': X, 'total_duration': Y, 'layovers': [L1]}]
    """
    paths = []
    
    # 1. Direct Flights
    direct_flights = Flight.objects.filter(
        departure_airport_id=source_id,
        arrival_airport_id=destination_id,
        departure_time__date=travel_date
    )
    # Seat filter
    if travel_class == 'ECONOMY': direct_flights = direct_flights.filter(economy_seats__gte=passengers)
    elif travel_class == 'BUSINESS': direct_flights = direct_flights.filter(business_seats__gte=passengers)
    else: direct_flights = direct_flights.filter(first_class_seats__gte=passengers)

    for f in direct_flights:
        paths.append({
            'segments': [f],
            'total_price': f.get_price_for_class(travel_class),
            'total_duration': f.duration,
            'is_direct': True,
            'total_stops': f.stops,
            'layovers': []
        })

    # 2. 1-Stop Connecting Flights (Source -> X -> Dest)
    if max_stops >= 1:
        # Flights from Source on travel_date
        first_legs = Flight.objects.filter(
            departure_airport_id=source_id,
            departure_time__date=travel_date
        ).exclude(arrival_airport_id=destination_id)
        
        if travel_class == 'ECONOMY': first_legs = first_legs.filter(economy_seats__gte=passengers)
        elif travel_class == 'BUSINESS': first_legs = first_legs.filter(business_seats__gte=passengers)
        else: first_legs = first_legs.filter(first_class_seats__gte=passengers)

        for f1 in first_legs:
            # Find second legs from f1.arrival_airport to destination
            # Second leg must be after f1.arrival_time + 1 hour layover
            min_dep_time = f1.arrival_time + timedelta(hours=1)
            max_dep_time = f1.arrival_time + timedelta(hours=24) # Max 24h layover
            
            second_legs = Flight.objects.filter(
                departure_airport_id=f1.arrival_airport_id,
                arrival_airport_id=destination_id,
                departure_time__gte=min_dep_time,
                departure_time__lte=max_dep_time
            )
            
            if travel_class == 'ECONOMY': second_legs = second_legs.filter(economy_seats__gte=passengers)
            elif travel_class == 'BUSINESS': second_legs = second_legs.filter(business_seats__gte=passengers)
            else: second_legs = second_legs.filter(first_class_seats__gte=passengers)

            for f2 in second_legs:
                layover = f2.departure_time - f1.arrival_time
                total_dur = f2.arrival_time - f1.departure_time
                total_price = f1.get_price_for_class(travel_class) + f2.get_price_for_class(travel_class)
                
                paths.append({
                    'segments': [f1, f2],
                    'total_price': total_price,
                    'total_duration': total_dur,
                    'is_direct': False,
                    'total_stops': f1.stops + f2.stops + 1,
                    'layovers': [layover]
                })

    return paths

# Flight booking views
def flight_search(request):
    if request.method == 'POST':
        departure = request.POST.get('departure')
        arrival = request.POST.get('arrival')
        date_str = request.POST.get('date')
        passengers = int(request.POST.get('passengers', 1))
        travel_class = request.POST.get('class', 'ECONOMY')
        fare_type = request.POST.get('fare_type', 'NORMAL').upper()
        if fare_type not in ['NORMAL', 'STUDENT']:
            fare_type = 'NORMAL'
        
        # Filters
        max_layover = request.POST.get('max_layover') # in hours
        preferred_airline = request.POST.get('airline')
        
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
            all_paths = find_routes(departure, arrival, date_obj, travel_class, passengers)

            if fare_type == 'STUDENT':
                for path in all_paths:
                    base_price = path['total_price']
                    path['original_price'] = base_price
                    path['discount_amount'] = round(base_price * Decimal('0.10'), 2)
                    path['total_price'] = base_price - path['discount_amount']
            else:
                for path in all_paths:
                    path['original_price'] = path['total_price']
                    path['discount_amount'] = Decimal('0.00')
            
            # Apply additional filters
            if max_layover:
                max_l_td = timedelta(hours=int(max_layover))
                all_paths = [p for p in all_paths if not p['layovers'] or all(l <= max_l_td for l in p['layovers'])]
            
            if preferred_airline:
                all_paths = [p for p in all_paths if all(s.airline_id == int(preferred_airline) for s in p['segments'])]

            # Sort by price then duration
            all_paths.sort(key=lambda x: (x['total_price'], x['total_duration']))

            return render(request, 'search_results.html', {
                'paths': all_paths,
                'passengers': passengers,
                'travel_class': travel_class,
                'fare_type': fare_type,
                'search_data': request.POST,
                'airlines': Airline.objects.all()
            })
            
        except ValueError:
            messages.error(request, "Invalid date format")
            return redirect('flight_search')
    
    airports = Airport.objects.all()
    return render(request, 'search.html', {'airports': airports})

@login_required
def book_flight(request, flight_id):
    # Support multi-segment paths
    path_str = request.GET.get('path', request.POST.get('path', str(flight_id)))
    path_ids = path_str.split(',')
    flights = [get_object_or_404(Flight, pk=int(fid)) for fid in path_ids]
    
    if request.method == 'POST':
        total_pax = int(request.POST.get('total_passengers', 1))
        travel_class = request.POST.get('travel_class', 'ECONOMY')
        fare_type = request.POST.get('fare_type', 'NORMAL').upper()
        if fare_type not in ['NORMAL', 'STUDENT']:
            fare_type = 'NORMAL'
        
        # Combined base price for all segments
        combined_base_price = sum(f.get_price_for_class(travel_class) for f in flights)
            
        calculated_total_price = Decimal('0.00')
        passenger_details = []
        
        for i in range(1, total_pax + 1):
            pax_type = request.POST.get(f'passenger_{i}_type')
            first_name = request.POST.get(f'passenger_{i}_first_name')
            last_name = request.POST.get(f'passenger_{i}_last_name')
            gender = request.POST.get(f'passenger_{i}_gender')
            age_val = request.POST.get(f'passenger_{i}_age', '0')
            age = int(age_val) if age_val.isdigit() else 0
            dob = request.POST.get(f'passenger_{i}_dob')
            id_type = request.POST.get(f'passenger_{i}_id_type')
            id_number = request.POST.get(f'passenger_{i}_id_number')
            is_pregnant = request.POST.get(f'passenger_{i}_is_pregnant') == 'on'
            special_assistance = request.POST.get(f'passenger_{i}_special_assistance') == 'on'
            assistance_details = request.POST.get(f'passenger_{i}_special_assistance_details', '')
            
            # Pricing logic: Child <= 5 is free
            pax_price = combined_base_price
            if pax_type == 'CHILD' and age <= 5:
                pax_price = Decimal('0.00')
            
            calculated_total_price += pax_price
            
            passenger_details.append({
                'first_name': first_name,
                'last_name': last_name,
                'gender': gender,
                'age': age,
                'is_child': (pax_type == 'CHILD'),
                'date_of_birth': dob,
                'id_type': id_type,
                'id_number': id_number,
                'is_pregnant': is_pregnant,
                'special_assistance': special_assistance,
                'special_assistance_details': assistance_details
            })
            
        discount_amount = Decimal('0.00')
        if fare_type == 'STUDENT' and calculated_total_price > 0:
            discount_amount = round(calculated_total_price * Decimal('0.10'), 2)
            calculated_total_price -= discount_amount

        booking = Booking.objects.create(
            user=request.user,
            flight=flights[0], # Reference to first leg
            nums_passengers=total_pax,
            travel_class=travel_class,
            fare_type=fare_type,
            discount_amount=discount_amount,
            total_price=calculated_total_price
        )
        
        # Create Booking Segments
        booking_segments = []
        for idx, f in enumerate(flights):
            layover = None
            if idx > 0:
                layover = f.departure_time - flights[idx-1].arrival_time
            seg = BookingSegment.objects.create(
                booking=booking,
                flight=f,
                sequence=idx+1,
                layover_duration=layover
            )
            booking_segments.append(seg)

        for detail in passenger_details:
            pax = Passenger.objects.create(
                booking=booking,
                **detail
            )
            
            # Ticket Generation Logic
            # Group segments by airline name and number
            ticket_groups = []
            if booking_segments:
                current_group = [booking_segments[0]]
                for s_idx in range(1, len(booking_segments)):
                    prev = booking_segments[s_idx-1].flight
                    curr = booking_segments[s_idx].flight
                    if prev.airline.name == curr.airline.name and prev.flight_number == curr.flight_number:
                        current_group.append(booking_segments[s_idx])
                    else:
                        ticket_groups.append(current_group)
                        current_group = [booking_segments[s_idx]]
                ticket_groups.append(current_group)
            
            for group in ticket_groups:
                # Generate unique ticket number
                tkt_num = f"{group[0].flight.airline.code}{random.randint(1000000, 9999999)}"
                tkt = Ticket.objects.create(
                    passenger=pax,
                    ticket_number=tkt_num,
                    airline_name=group[0].flight.airline.name,
                    flight_number=group[0].flight.flight_number
                )
                tkt.segments.set(group)
            
        # Update available seats for ALL segments
        for f in flights:
            if travel_class == 'ECONOMY': f.economy_seats -= total_pax
            elif travel_class == 'BUSINESS': f.business_seats -= total_pax
            elif travel_class == 'FIRST': f.first_class_seats -= total_pax
            f.save()
        
        return redirect('payment', booking_id=booking.id)
    
    # GET request
    passengers = int(request.GET.get('passengers', 1))
    travel_class = request.GET.get('class', 'ECONOMY')
    fare_type = request.GET.get('fare_type', 'NORMAL').upper()
    if fare_type not in ['NORMAL', 'STUDENT']:
        fare_type = 'NORMAL'
    
    combined_price = sum(f.get_price_for_class(travel_class) for f in flights)
    original_total_price = combined_price * passengers
    discount_amount = Decimal('0.00')
    total_price = original_total_price
    if fare_type == 'STUDENT' and original_total_price > 0:
        discount_amount = round(original_total_price * Decimal('0.10'), 2)
        total_price = original_total_price - discount_amount
    
    return render(request, 'book.html', {
        'flight': flights[0],
        'flights': flights, # Pass all segments
        'path': path_str,
        'passengers': range(1, passengers + 1),
        'travel_class': travel_class,
        'fare_type': fare_type,
        'price': combined_price,
        'original_total_price': original_total_price,
        'discount_amount': discount_amount,
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
        'base_fare': booking.base_fare,
        'gst_amount': booking.gst_amount,
        'total': booking.final_total,
        'passenger_count': booking.nums_passengers
    }
    final_price = booking.final_total
    discount = 0
    coupon_applied = None

    if request.method == 'POST':
        if 'apply_coupon' in request.POST:
            coupon_code = request.POST.get('coupon_code', '').strip().upper()
            if coupon_code == 'UDAAAN':
                # Check if this is the user's first booking (no other completed payments)
                previous_payments = Payment.objects.filter(booking__user=request.user, status='COMPLETED').exists()
                if not previous_payments:
                    discount = booking.final_total
                    final_price = 0
                    coupon_applied = 'UDAAAN'
                    messages.success(request, "Coupon applied! 100% discount for your first booking.")
                else:
                    messages.error(request, "The coupon UDAAAN is only valid for your first booking.")
            else:
                messages.error(request, "Invalid coupon code.")
            
            return render(request, 'payment.html', {
                'booking': booking,
                'passengers': passengers,
                'price_breakdown': price_breakdown,
                'final_price': final_price,
                'discount': discount,
                'coupon_applied': coupon_applied,
                'stripe_public_key': settings.STRIPE_PUBLIC_KEY
            })

        if 'complete_payment' in request.POST:
            if Payment.objects.filter(booking=booking).exists():
                messages.info(request, "Payment already completed")
                return redirect('booking_detail', reference=booking.reference)

            # Re-verify coupon if it was passed during final payment submission
            coupon_code = request.POST.get('coupon_code', '').strip().upper()
            payment_amount = booking.final_total
            
            if coupon_code == 'UDAAAN':
                previous_payments = Payment.objects.filter(booking__user=request.user, status='COMPLETED').exists()
                if not previous_payments:
                    payment_amount = 0

            payment_method_input = request.POST.get('payment_method', 'credit_card')
            payment_method_display = 'PayPal' if payment_method_input == 'paypal' else 'Credit Card'

            payment = Payment.objects.create(
                booking=booking,
                amount=payment_amount,
                transaction_id=f"TX{random.randint(100000000, 999999999)}",
                payment_method=payment_method_display,
                status='COMPLETED'
            )
            
            # If 100% discount, update booking price to 0 too for consistency?
            # Actually, keeping total_price as base and amount as paid is fine.
            
            messages.success(request, "Payment successful!")
            return redirect('booking_detail', reference=booking.reference)
    
    return render(request, 'payment.html', {
        'booking': booking,
        'passengers': passengers,
        'price_breakdown': price_breakdown,
        'final_price': final_price,
        'discount': discount,
        'coupon_applied': coupon_applied,
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
    print(f"Total Price: {booking.final_total}")
    
    price_breakdown = {
        'per_passenger': booking.per_passenger_price,
        'base_fare': booking.base_fare,
        'gst_amount': booking.gst_amount,
        'total': booking.final_total,
        'passenger_count': booking.nums_passengers
    }
    
    
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
            user = form.save(commit=False)
            user.first_name = request.POST.get('first_name', '')
            user.last_name = request.POST.get('last_name', '')
            user.save()
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
    travel_class = request.GET.get('class', 'ECONOMY').upper()
    fare_type = request.GET.get('fare_type', 'NORMAL').upper()
    if fare_type not in ['NORMAL', 'STUDENT']:
        fare_type = 'NORMAL'
    passengers = int(request.GET.get('passengers', 1))
    
    if not departure_id or not arrival_id:
        return JsonResponse({'error': 'Missing parameters'}, status=400)
        
    from django.utils import timezone
    from django.db.models import Min
    
    # Filter flights from today onwards
    flights = Flight.objects.filter(
        departure_airport_id=departure_id, 
        arrival_airport_id=arrival_id, 
        departure_time__gte=timezone.now()
    ).select_related('airline', 'departure_airport', 'arrival_airport').order_by('departure_time')
    
    availability = {}
    
    for flight in flights:
        # Check seats for requested class
        if travel_class == 'ECONOMY':
            seats = flight.economy_seats
            price = float(flight.economy_price)
        elif travel_class == 'BUSINESS':
            seats = flight.business_seats
            price = float(flight.business_price)
        else: # FIRST
            seats = flight.first_class_seats
            price = float(flight.first_class_price)

        original_price = price
        discount_amount = 0
        if fare_type == 'STUDENT':
            discount_amount = round(price * 0.10, 2)
            price = round(price - discount_amount, 2)
            
        if seats < passengers:
            continue
            
        date_str = flight.departure_time.strftime('%Y-%m-%d')
        
        if date_str not in availability:
            availability[date_str] = {
                'min_price': price,
                'flights': []
            }
        
        availability[date_str]['min_price'] = min(availability[date_str]['min_price'], price)
        availability[date_str]['flights'].append({
            'id': flight.id,
            'airline': flight.airline.name,
            'airline_code': flight.airline.code,
            'airline_logo': flight.airline.logo.url if flight.airline.logo else '',
            'flight_number': flight.flight_number,
            'departure_time': flight.departure_time.strftime('%H:%M'),
            'arrival_time': flight.arrival_time.strftime('%H:%M'),
            'duration': flight.duration_display(),
            'original_price': original_price,
            'discount_amount': discount_amount,
            'price': price,
            'seats': seats
        })
        
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
