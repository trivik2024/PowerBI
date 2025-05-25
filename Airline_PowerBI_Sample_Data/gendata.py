import pandas as pd
import random
from faker import Faker
import numpy as np
import os

# Initialize Faker and seed
fake = Faker()
Faker.seed(0)
random.seed(0)
np.random.seed(0)

# Configuration
num_records = 80000
output_dir = "airline_sample_data"
os.makedirs(output_dir, exist_ok=True)

# Helper: Generate unique 3-letter airport codes
def generate_airport_codes(n):
    codes = set()
    while len(codes) < n:
        code = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=3))
        codes.add(code)
    return list(codes)

# 1. Aircraft (10 records)
aircraft_ids = [f"A{i:03d}" for i in range(10)]
aircraft_types = ["A320", "B737", "A350", "B777", "B787", "A321", "B747", "E190", "CRJ900", "ATR72"]
manufacturers = ["Airbus", "Boeing", "Embraer", "Bombardier", "ATR"]

aircraft = pd.DataFrame({
    "AircraftID": aircraft_ids,
    "Type": aircraft_types,
    "Manufacturer": [random.choice(manufacturers) for _ in range(10)],
    "Seats": [random.randint(120, 300) for _ in range(10)],
    "Age": [random.randint(1, 15) for _ in range(10)]
})

# 2. Airports (20 records)
airport_codes = generate_airport_codes(20)
airports = pd.DataFrame({
    "AirportCode": airport_codes,
    "AirportName": [fake.city() + " Intl" for _ in range(20)],
    "City": [fake.city() for _ in range(20)],
    "Country": [fake.country() for _ in range(20)]
})

# 3. Passengers (8000 records)
passenger_ids = [f"P{i:05d}" for i in range(num_records)]
passengers = pd.DataFrame({
    "PassengerID": passenger_ids,
    "Name": [fake.name() for _ in range(num_records)],
    "Nationality": [fake.country() for _ in range(num_records)],
    "FrequentFlyerStatus": [random.choice(["None", "Silver", "Gold", "Platinum"]) for _ in range(num_records)]
})

# 4. Flights (8000 records)
flight_ids = [f"F{i:05d}" for i in range(num_records)]
flights = pd.DataFrame({
    "FlightID": flight_ids,
    "FlightNumber": [f"AI{random.randint(100,999)}" for _ in range(num_records)],
    "Origin": [random.choice(airport_codes) for _ in range(num_records)],
    "Destination": [random.choice(airport_codes) for _ in range(num_records)],
    "AircraftID": [random.choice(aircraft_ids) for _ in range(num_records)],
    "ScheduledDeparture": pd.date_range(start="2020-01-01", periods=num_records, freq='H'),
    "ActualDeparture": pd.date_range(start="2020-01-01 00:10", periods=num_records, freq='H') + pd.to_timedelta(np.random.randint(0, 60, num_records), unit='m'),
    "ScheduledArrival": pd.date_range(start="2020-01-01 03:00", periods=num_records, freq='H'),
    "ActualArrival": pd.date_range(start="2020-01-01 03:10", periods=num_records, freq='H') + pd.to_timedelta(np.random.randint(0, 90, num_records), unit='m')
})

# 5. Bookings (8000 records)
bookings = pd.DataFrame({
    "BookingID": [f"B{i:05d}" for i in range(num_records)],
    "FlightID": [random.choice(flight_ids) for _ in range(num_records)],
    "PassengerID": passenger_ids,
    "TicketClass": [random.choice(["Economy", "Business", "First"]) for _ in range(num_records)],
    "BookingDate": pd.date_range(end="2020-04-30", periods=num_records, freq='T'),
    "Fare": [round(random.uniform(100, 2000), 2) for _ in range(num_records)]
})

# Save as CSV
flights.to_csv(f"{output_dir}/Flights.csv", index=False)
bookings.to_csv(f"{output_dir}/Bookings.csv", index=False)
passengers.to_csv(f"{output_dir}/Passengers.csv", index=False)
aircraft.to_csv(f"{output_dir}/Aircraft.csv", index=False)
airports.to_csv(f"{output_dir}/Airports.csv", index=False)

print(f"✅ Files successfully saved in the folder: {output_dir}")

