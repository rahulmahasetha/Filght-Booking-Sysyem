import os
import django
from datetime import datetime, timedelta
from decimal import Decimal
from django.utils import timezone

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from home.models import Airport, Airline, Flight, FlightRoute, RouteStop
from home.timezone_utils import ensure_aware_datetime

def setup_patna_stop():
    # 1. Ensure Patna Airport exists
    patna, _ = Airport.objects.get_or_create(
        code='PAT',
        defaults={
            'name': 'Jay Prakash Narayan International Airport',
            'city': 'Patna',
            'country': 'India'
        }
    )
    print(f"Airport ensured: {patna}")

    # 2. Get the Airline
    na, _ = Airline.objects.get_or_create(
        code='NA',
        defaults={'name': 'Nepal Airlines'}
    )

    # 3. Handle the Flight NA1154
    # We will create/update the segments to include the stop at PAT
    
    vga = Airport.objects.get(code='VGA')
    ktm = Airport.objects.get(code='KTM')
    
    # Timings from user request
    departure_vga = ensure_aware_datetime(datetime(2026, 5, 15, 18, 13, 50))
    arrival_ktm = ensure_aware_datetime(datetime(2026, 5, 18, 23, 0, 4))
    
    # Intermediate timings for PAT
    arrival_pat = departure_vga + timedelta(hours=2)
    departure_pat = arrival_pat + timedelta(hours=1) # 1 hour layover
    
    # Delete existing flight to re-create with segments if needed, 
    # but let's just create new segments
    Flight.objects.filter(flight_number='1154', airline=na).delete()
    
    # Leg 1: VGA -> PAT
    f1 = Flight.objects.create(
        flight_number='1154',
        airline=na,
        departure_airport=vga,
        arrival_airport=patna,
        departure_time=departure_vga,
        arrival_time=arrival_pat,
        economy_seats=150,
        business_seats=20,
        first_class_seats=10,
        economy_price=Decimal('4500.00'),
        business_price=Decimal('8500.00'),
        first_class_price=Decimal('12000.00'),
        stops=1
    )
    
    # Leg 2: PAT -> KTM
    f2 = Flight.objects.create(
        flight_number='1154',
        airline=na,
        departure_airport=patna,
        arrival_airport=ktm,
        departure_time=departure_pat,
        arrival_time=arrival_ktm,
        economy_seats=150,
        business_seats=20,
        first_class_seats=10,
        economy_price=Decimal('5500.00'),
        business_price=Decimal('9500.00'),
        first_class_price=Decimal('15000.00'),
        stops=0
    )
    
    print(f"Created segments for NA1154 via PAT")

    # 4. Optional: Create a FlightRoute for Admin management
    route, _ = FlightRoute.objects.get_or_create(
        airline=na,
        flight_number='1154'
    )
    route.stops.all().delete()
    RouteStop.objects.create(route=route, airport=vga, sequence=1, departure_time=departure_vga)
    RouteStop.objects.create(route=route, airport=patna, sequence=2, arrival_time=arrival_pat, departure_time=departure_pat)
    RouteStop.objects.create(route=route, airport=ktm, sequence=3, arrival_time=arrival_ktm)
    
    print(f"FlightRoute configured for NA1154")

if __name__ == "__main__":
    setup_patna_stop()
