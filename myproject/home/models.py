from django.db import models
from decimal import Decimal
from datetime import timedelta
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
import random
# Create your models here.

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
    
    '''def duration(self):
        return self.arrival_time - self.departure_time'''
    @property
    def duration(self):
        """Calculate flight duration in hours and minutes"""
        delta = self.arrival_time - self.departure_time
        # Convert to total seconds and then to hours/minutes
        total_seconds = delta.total_seconds()
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)
        return timedelta(hours=hours, minutes=minutes)
    
    def duration_display(self):
        """Formatted duration string"""
        delta = self.duration
        hours = delta.seconds // 3600
        minutes = (delta.seconds % 3600) // 60
        return f"{hours}h {minutes}m"
    def __str__(self):
        return f"{self.airline.code}{self.flight_number}"



class Booking(models.Model):
    STATUS_CHOICES = [
        ('CONFIRMED', 'Confirmed'),
        ('CANCELLED', 'Cancelled'),
        ('PENDING', 'Pending'),
    ]
    
    CLASS_CHOICES = [
        ('ECONOMY', 'Economy'),
        ('BUSINESS', 'Business'),
        ('FIRST', 'First Class'),
    ]
    
    reference = models.CharField(max_length=8, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    flight = models.ForeignKey('Flight', on_delete=models.CASCADE)
    nums_passengers = models.PositiveIntegerField(default=1)
    travel_class = models.CharField(max_length=10, choices=CLASS_CHOICES)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='CONFIRMED')

    def calculate_total_price(self):
        """Calculate total price based on class and passenger count"""
        if self.nums_passengers is None or self.nums_passengers <= 0:
            self.total_price = Decimal('0.00')
            return

        price_per_passenger = self.per_passenger_price
        self.total_price = price_per_passenger * self.nums_passengers

    def save(self, *args, **kwargs):
        if not self.reference:
            self.reference = f"BK{random.randint(100000, 999999)}"
        self.calculate_total_price()
        super().save(*args, **kwargs)

    @property
    def per_passenger_price(self):
        """Price per passenger based on travel class"""
        if not self.flight:
            return Decimal('0.00')
        
        if self.travel_class == 'ECONOMY':
            return self.flight.economy_price or Decimal('0.00')
        elif self.travel_class == 'BUSINESS':
            return self.flight.business_price or Decimal('0.00')
        elif self.travel_class == 'FIRST':
            return self.flight.first_class_price or Decimal('0.00')
        return Decimal('0.00')

    
class Passenger(models.Model):
    ID_TYPE_CHOICES = [
        ('PASSPORT', 'Passport'),
        ('NATIONAL_ID', 'National ID'),
        ('DRIVING_LICENSE', 'Driving License'),
    ]
    
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='passengers',null=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    id_type = models.CharField(max_length=20, choices=ID_TYPE_CHOICES)
    id_number = models.CharField(max_length=50)
    passport_number = models.CharField(max_length=20, blank=True, null=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Payment(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2,blank = True)
    payment_date = models.DateTimeField(auto_now_add=True)
    transaction_id = models.CharField(max_length=50, blank=True)
    status = models.CharField(max_length=20, default='COMPLETED')
    
    def __str__(self):
        return f"Payment for {self.booking}"
