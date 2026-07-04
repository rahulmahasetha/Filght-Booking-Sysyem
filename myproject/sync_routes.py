import os
import django
from datetime import datetime

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from home.models import Flight, FlightRoute, RouteStop, Airline, Airport

def sync_routes_to_flights():
    routes = FlightRoute.objects.filter(is_active=True)
    for route in routes:
        stops = list(route.stops.all().order_by('sequence'))
        if len(stops) < 2:
            continue
            
        for i in range(len(stops) - 1):
            s1 = stops[i]
            s2 = stops[i+1]
            
            # Determine airline and flight number for this leg
            airline = s1.departure_airline
            flight_num = s1.flight_number
            
            # Update or create the Flight leg
            # Find a flight that matches this route's sequence if possible, 
            # or just look for a flight between these airports at this time
            flight, created = Flight.objects.get_or_create(
                departure_airport=s1.airport,
                arrival_airport=s2.airport,
                departure_time=s1.departure_time,
                defaults={
                    'arrival_time': s2.arrival_time,
                    'airline': airline,
                    'flight_number': flight_num,
                    'economy_seats': 150,
                    'business_seats': 20,
                    'first_class_seats': 10,
                    'economy_price': 5000,
                    'business_price': 10000,
                    'first_class_price': 15000,
                }
            )
            
            if not created:
                flight.airline = airline
                flight.flight_number = flight_num
                flight.arrival_time = s2.arrival_time
                flight.save()
            
            print(f"Synced Leg: {s1.airport.code} -> {s2.airport.code} ({airline.name} {flight_num})")

if __name__ == "__main__":
    sync_routes_to_flights()
