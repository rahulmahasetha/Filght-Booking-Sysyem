import os
import django
from datetime import timedelta
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

# Override settings to use SQLite to avoid mysqlclient requirement
from django.conf import settings
if not settings.configured:
    settings.configure(
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },
        INSTALLED_APPS=[
            'home.apps.HomeConfig',
            'django.contrib.auth',
            'django.contrib.contenttypes',
        ]
    )

import django
django.setup()

from django.utils import timezone
from home.models import Flight, Airline, Airport

def test_dynamic_pricing():
    # We can create a dummy flight without saving it to the DB just to test the @property
    now = timezone.now()
    
    airline = Airline(name="Test Airline", code="TA")
    dep_airport = Airport(code="DEP", name="Departure", city="DepCity", country="DepCountry")
    arr_airport = Airport(code="ARR", name="Arrival", city="ArrCity", country="ArrCountry")
    
    # Normal Flight: > 10 and <= 100 seats, departure > 48 hours
    flight = Flight(
        flight_number="123",
        airline=airline,
        departure_airport=dep_airport,
        arrival_airport=arr_airport,
        departure_time=now + timedelta(days=5),
        arrival_time=now + timedelta(days=5, hours=2),
        economy_seats=50,
        business_seats=50,
        first_class_seats=50,
        economy_price=Decimal('100.00'),
        business_price=Decimal('100.00'),
        first_class_price=Decimal('100.00')
    )
    print(f"Base price: $100.00")
    print(f"Normal (50 seats, 5 days away): ${flight.current_economy_price}")
    
    # > 100 seats (-10%)
    flight.economy_seats = 150
    print(f"High capacity (150 seats, 5 days away): ${flight.current_economy_price}")
    
    # <= 10 seats (+20%)
    flight.economy_seats = 5
    print(f"Low capacity (5 seats, 5 days away): ${flight.current_economy_price}")
    
    # Within 48 hours (+15%)
    flight.economy_seats = 50
    flight.departure_time = now + timedelta(hours=24)
    print(f"Last minute (50 seats, 24 hours away): ${flight.current_economy_price}")
    
    # <= 10 seats AND within 48 hours (+20% + 15% = +35%)
    flight.economy_seats = 5
    flight.departure_time = now + timedelta(hours=24)
    print(f"Last minute & low capacity (5 seats, 24 hours away): ${flight.current_economy_price}")

if __name__ == '__main__':
    test_dynamic_pricing()
