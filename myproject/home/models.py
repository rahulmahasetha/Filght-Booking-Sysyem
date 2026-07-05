from django.db import models
from decimal import Decimal
from datetime import timedelta
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
import random

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    bio = models.TextField(blank=True)
    gender = models.CharField(max_length=10, blank=True)
    dob = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    pincode = models.CharField(max_length=100)
    message = models.TextField()
    date = models.DateTimeField(null=True, blank=True)

class Airport(models.Model):
    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    image = models.ImageField(upload_to='airports/', null=True, blank=True)
    
    def __str__(self):
        return f"{self.city} ({self.code})"

class Airline(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=2, unique=True)
    logo = models.ImageField(upload_to='airlines/', null=True, blank=True)
    
    def __str__(self):
        return self.name

# NEW: FlightRoute for template management in Admin
class FlightRoute(models.Model):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Route: {self.name}"

class RouteStop(models.Model):
    route = models.ForeignKey(FlightRoute, on_delete=models.CASCADE, related_name='stops')
    airport = models.ForeignKey(Airport, on_delete=models.CASCADE)
    sequence = models.PositiveIntegerField(default=1)
    arrival_time = models.DateTimeField(null=True, blank=True)
    departure_time = models.DateTimeField(null=True, blank=True)
    departure_airline = models.ForeignKey(Airline, on_delete=models.SET_NULL, null=True, blank=True)
    flight_number = models.CharField(max_length=10, blank=True)
    
    class Meta:
        ordering = ['sequence']

    def __str__(self):
        return f"{self.route} - {self.airport.code} (Stop {self.sequence})"

class Flight(models.Model):
    flight_number = models.CharField(max_length=10)
    airline = models.ForeignKey(Airline, on_delete=models.CASCADE)
    departure_airport = models.ForeignKey(Airport, related_name='departures', on_delete=models.CASCADE)
    arrival_airport = models.ForeignKey(Airport, related_name='arrivals', on_delete=models.CASCADE)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    economy_seats = models.PositiveIntegerField()
    business_seats = models.PositiveIntegerField()
    first_class_seats = models.PositiveIntegerField()
    economy_price = models.DecimalField(max_digits=10, decimal_places=2)
    business_price = models.DecimalField(max_digits=10, decimal_places=2)
    first_class_price = models.DecimalField(max_digits=10, decimal_places=2)
    stops = models.PositiveIntegerField(default=0)
    cabin_allowance = models.CharField('Cabin', max_length=80, default='7 kg cabin bag')
    check_in_allowance = models.CharField('Check In', max_length=80, default='15 kg check-in bag')
    
    @property
    def duration(self):
        delta = self.arrival_time - self.departure_time
        total_seconds = delta.total_seconds()
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)
        return timedelta(hours=hours, minutes=minutes)
    
    @property
    def current_economy_price(self):
        return self._calculate_dynamic_price(self.economy_price, self.economy_seats)
        
    @property
    def current_business_price(self):
        return self._calculate_dynamic_price(self.business_price, self.business_seats)
        
    @property
    def current_first_class_price(self):
        return self._calculate_dynamic_price(self.first_class_price, self.first_class_seats)

    def _calculate_dynamic_price(self, base_price, available_seats):
        if not base_price:
            return Decimal('0.00')
        price_multiplier = Decimal('1.00')
        if available_seats <= 10:
            price_multiplier += Decimal('0.20')
        elif available_seats > 100:
            price_multiplier -= Decimal('0.10')
        from django.utils import timezone
        time_left = self.departure_time - timezone.now()
        if time_left.days <= 2 and time_left.days >= 0:
            price_multiplier += Decimal('0.15')
        return round(base_price * price_multiplier, 2)

    def duration_display(self):
        delta = self.duration
        hours = delta.seconds // 3600
        minutes = (delta.seconds % 3600) // 60
        return f"{hours}h {minutes}m"

    def get_price_for_class(self, travel_class):
        if travel_class == 'ECONOMY': return self.current_economy_price
        elif travel_class == 'BUSINESS': return self.current_business_price
        elif travel_class == 'FIRST': return self.current_first_class_price
        return Decimal('0.00')

    def __str__(self):
        return f"{self.airline.code}{self.flight_number}"

class Booking(models.Model):
    STATUS_CHOICES = [('CONFIRMED', 'Confirmed'), ('CANCELLED', 'Cancelled'), ('PENDING', 'Pending')]
    CLASS_CHOICES = [('ECONOMY', 'Economy'), ('BUSINESS', 'Business'), ('FIRST', 'First Class')]
    FARE_TYPE_CHOICES = [('NORMAL', 'Normal'), ('STUDENT', 'Student')]
    
    reference = models.CharField(max_length=8, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    flight = models.ForeignKey('Flight', on_delete=models.CASCADE, null=True, blank=True)
    flights = models.ManyToManyField('Flight', through='BookingSegment', related_name='multi_segment_bookings')
    nums_passengers = models.PositiveIntegerField(default=1)
    travel_class = models.CharField(max_length=10, choices=CLASS_CHOICES)
    fare_type = models.CharField(max_length=10, choices=FARE_TYPE_CHOICES, default='NORMAL')
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='CONFIRMED')

    def save(self, *args, **kwargs):
        if not self.reference:
            self.reference = f"BK{random.randint(100000, 999999)}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Booking {self.reference}"

    @property
    def per_passenger_price(self):
        """Total price for one passenger across all segments"""
        segments = self.booking_segments.all()
        if segments.exists():
            return sum(seg.flight.get_price_for_class(self.travel_class) for seg in segments)
        if self.flight:
            return self.flight.get_price_for_class(self.travel_class)
        return Decimal('0.00')

    @property
    def base_fare(self):
        """Dynamic base fare excluding GST"""
        return round((self.per_passenger_price * Decimal(self.nums_passengers)) - self.discount_amount, 2)

    @property
    def gst_amount(self):
        """18% GST on base fare"""
        return round(self.base_fare * Decimal('0.18'), 2)

    @property
    def final_total(self):
        """Total amount including GST"""
        return self.base_fare + self.gst_amount

class Passenger(models.Model):
    ID_TYPE_CHOICES = [('PASSPORT', 'Passport'), ('NATIONAL_ID', 'National ID'), ('DRIVING_LICENSE', 'Driving License')]
    GENDER_CHOICES = [('MALE', 'Male'), ('FEMALE', 'Female'), ('OTHER', 'Other')]
    
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='passengers')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='MALE')
    date_of_birth = models.DateField()
    id_type = models.CharField(max_length=20, choices=ID_TYPE_CHOICES)
    id_number = models.CharField(max_length=50)
    passport_number = models.CharField(max_length=20, blank=True, null=True)
    is_child = models.BooleanField(default=False)
    age = models.PositiveIntegerField(null=True, blank=True)
    is_pregnant = models.BooleanField(default=False)
    special_assistance = models.BooleanField(default=False)
    special_assistance_details = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class BookingSegment(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='booking_segments')
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    sequence = models.PositiveIntegerField(default=1)
    layover_duration = models.DurationField(null=True, blank=True)
    
    class Meta:
        ordering = ['sequence']

    def __str__(self):
        return f"{self.booking.reference} - Leg {self.sequence}: {self.flight.flight_number}"

# NEW: Ticket model for granular ticket generation
class Ticket(models.Model):
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE, related_name='tickets')
    segments = models.ManyToManyField(BookingSegment, related_name='tickets')
    ticket_number = models.CharField(max_length=20, unique=True)
    airline_name = models.CharField(max_length=100)
    flight_number = models.CharField(max_length=10)
    issued_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"TKT-{self.ticket_number} ({self.airline_name})"

class Payment(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    payment_date = models.DateTimeField(auto_now_add=True)
    transaction_id = models.CharField(max_length=50, blank=True)
    payment_method = models.CharField(max_length=50, default='Credit Card')
    status = models.CharField(max_length=20, default='COMPLETED')
    
    def __str__(self):
        return f"Payment for {self.booking}"

# Signals to sync RouteStops to Flights
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=RouteStop)
def sync_flight_from_route_stop(sender, instance, **kwargs):
    route = instance.route
    stops = list(route.stops.all().order_by('sequence'))
    if len(stops) < 2:
        return
        
    for i in range(len(stops) - 1):
        s1 = stops[i]
        s2 = stops[i+1]
        
        if s1.departure_airline and s1.flight_number:
            Flight.objects.update_or_create(
                departure_airport=s1.airport,
                arrival_airport=s2.airport,
                departure_time=s1.departure_time,
                defaults={
                    'arrival_time': s2.arrival_time,
                    'airline': s1.departure_airline,
                    'flight_number': s1.flight_number,
                    'economy_seats': 150,
                    'business_seats': 20,
                    'first_class_seats': 10,
                    'economy_price': 5000,
                    'business_price': 10000,
                    'first_class_price': 15000,
                    'stops': 0
                }
            )
