import os
import django
from datetime import datetime, timedelta
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from home.models import Flight

def extend_flights():
    print("Generating flights for the next 9 months (270 days)...")
    unique_routes = Flight.objects.values('flight_number', 'departure_airport', 'arrival_airport').distinct()
    
    today = timezone.now().date()
    total_days = 270
    
    flights_to_create = []
    
    for route in unique_routes:
        prototype = Flight.objects.filter(
            flight_number=route['flight_number'],
            departure_airport=route['departure_airport'],
            arrival_airport=route['arrival_airport']
        ).first()
        
        if not prototype:
            continue
            
        prototype_dep_time = prototype.departure_time.time()
        duration = prototype.duration
        
        for day_offset in range(total_days):
            target_date = today + timedelta(days=day_offset)
            
            target_dep = timezone.make_aware(
                datetime.combine(target_date, prototype_dep_time),
                timezone.get_default_timezone(),
            )
            target_arr = target_dep + duration
            
            exists = Flight.objects.filter(
                flight_number=prototype.flight_number,
                departure_airport=prototype.departure_airport,
                departure_time=target_dep
            ).exists()
            
            if not exists:
                new_flight = Flight(
                    flight_number=prototype.flight_number,
                    airline=prototype.airline,
                    departure_airport=prototype.departure_airport,
                    arrival_airport=prototype.arrival_airport,
                    departure_time=target_dep,
                    arrival_time=target_arr,
                    economy_seats=prototype.economy_seats,
                    business_seats=prototype.business_seats,
                    first_class_seats=prototype.first_class_seats,
                    economy_price=prototype.economy_price,
                    business_price=prototype.business_price,
                    first_class_price=prototype.first_class_price,
                    stops=prototype.stops,
                    cabin_allowance=prototype.cabin_allowance,
                    check_in_allowance=prototype.check_in_allowance
                )
                flights_to_create.append(new_flight)
                
    if flights_to_create:
        print(f"Creating {len(flights_to_create)} new flights...")
        Flight.objects.bulk_create(flights_to_create, batch_size=500)
        print("Done creating flights.")
    else:
        print("No new flights to create. Data already up to date.")

if __name__ == '__main__':
    extend_flights()
