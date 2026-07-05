import os
import django
import re
from datetime import datetime, timedelta
import ast

from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from home.models import Airport, Airline, Flight
from home.timezone_utils import ensure_aware_datetime

def parse_values(sql_file_path):
    with open(sql_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract the INSERT INTO statement
    match = re.search(r'INSERT INTO `[^`]+` VALUES\s*(.*);', content, re.DOTALL | re.IGNORECASE)
    if not match:
        return []
    
    values_str = match.group(1)
    
    # We can split by "),(" but it's safer to use regex to find all (...)
    # Replace NULL with None
    values_str = values_str.replace('NULL', 'None')
    
    # Extract all tuples
    tuples_strs = re.findall(r'\((.*?)\)', values_str)
    
    records = []
    for t_str in tuples_strs:
        # Evaluate as a python tuple
        # Need to handle empty string or syntax errors
        try:
            record = ast.literal_eval(f"({t_str})")
            records.append(record)
        except Exception as e:
            print(f"Error parsing: {t_str} - {e}")
            
    return records

def load_data():
    print("Loading Airports...")
    airports = parse_values('../data/flight_home_airport.sql')
    for a in airports:
        Airport.objects.update_or_create(
            id=a[0],
            defaults={
                'code': a[1],
                'name': a[2],
                'city': a[3],
                'country': a[4],
                'image': a[5] if a[5] else ''
            }
        )
        
    print("Loading Airlines...")
    airlines = parse_values('../data/flight_home_airline.sql')
    for a in airlines:
        Airline.objects.update_or_create(
            id=a[0],
            defaults={
                'name': a[1],
                'code': a[2],
                'logo': a[3] if a[3] else ''
            }
        )
        
    print("Loading Flights...")
    flights = parse_values('../data/flight_home_flight.sql')
    today = timezone.now().date()
    
    for f in flights:
        try:
            dep_time_str = f[2].split('.')[0] # Remove fractional seconds
            arr_time_str = f[3].split('.')[0]
            
            dep_time = ensure_aware_datetime(datetime.strptime(dep_time_str, '%Y-%m-%d %H:%M:%S'))
            arr_time = ensure_aware_datetime(datetime.strptime(arr_time_str, '%Y-%m-%d %H:%M:%S'))
            
            # Shift dates to be in the future (relative to today)
            # Find how many days passed since 2025-04-10 (the earliest date in the dump)
            # Or just replace the date with a day relative to today + a few days
            # Let's map original day 10 -> today + 1, day 11 -> today + 2, etc.
            original_day = dep_time.day
            day_offset = original_day - 10 # 0 for day 10
            if day_offset < 0:
                day_offset = 0 # fallback
                
            new_dep_date = today + timedelta(days=day_offset + 1)
            
            new_dep_time = ensure_aware_datetime(datetime.combine(new_dep_date, dep_time.time()))
            
            # Calculate duration
            duration = arr_time - dep_time
            new_arr_time = new_dep_time + duration
            
            # The columns in SQL are:
            # 0: id
            # 1: flight_number
            # 2: departure_time
            # 3: arrival_time
            # 4: economy_seats
            # 5: business_seats
            # 6: first_class_seats
            # 7: economy_price
            # 8: business_price
            # 9: first_class_price
            # 10: airline_id
            # 11: arrival_airport_id  OR departure_airport_id
            # 12: departure_airport_id OR arrival_airport_id
            
            # Looking at flight 11: AA101, airline_id=1. 11, 12 values: 2, 1. JFK(1) to LHR(2) makes sense. So 12 is departure_airport_id, 11 is arrival_airport_id.
            
            airline_id = f[10]
            arrival_airport_id = f[11]
            departure_airport_id = f[12]
            
            Flight.objects.update_or_create(
                id=f[0],
                defaults={
                    'flight_number': f[1],
                    'departure_time': new_dep_time,
                    'arrival_time': new_arr_time,
                    'economy_seats': f[4],
                    'business_seats': f[5],
                    'first_class_seats': f[6],
                    'economy_price': f[7],
                    'business_price': f[8],
                    'first_class_price': f[9],
                    'airline_id': airline_id,
                    'arrival_airport_id': arrival_airport_id,
                    'departure_airport_id': departure_airport_id
                }
            )
        except Exception as e:
            print(f"Error loading flight {f[0]}: {e}")
            
    print("Done loading and updating times.")

if __name__ == '__main__':
    load_data()
