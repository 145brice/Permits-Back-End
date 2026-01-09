#!/usr/bin/env python3
"""
Test the last-week endpoint logic
"""
import os
import csv
from datetime import datetime

def test_last_week_endpoint():
    """Test the logic for the last-week endpoint"""
    # Simulate the endpoint logic
    requested_cities = ['nashville', 'austin', 'sanantonio']

    available_cities = {
        'nashville': 'nashville',
        'austin': 'austin',
        'sanantonio': 'sanantonio',
        'houston': 'houston',
        'charlotte': 'charlotte',
        'phoenix': 'phoenix',
        'chattanooga': 'chattanooga',
        'dallas': 'dallas'
    }

    result = {}
    base_date = datetime.now().strftime('%Y-%m-%d')

    for city in requested_cities:
        if city not in available_cities:
            result[city] = {'error': f'City {city} not available'}
            continue

        try:
            # Try to read the CSV file for today
            csv_path = os.path.join('..', 'leads', available_cities[city], base_date, f'{base_date}_{available_cities[city]}.csv')

            print(f"Looking for CSV at: {csv_path}")
            print(f"Absolute path: {os.path.abspath(csv_path)}")

            if not os.path.exists(csv_path):
                result[city] = {'error': f'No data available for {city}'}
                print(f"CSV not found for {city}")
                continue

            # Read CSV and convert to JSON
            permits = []
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # Clean and standardize the data
                    clean_permit = {
                        'permit_number': row.get('permit_number', ''),
                        'address': row.get('address', ''),
                        'type': row.get('type', ''),
                        'value': row.get('value', 0),
                        'issued_date': row.get('issued_date', ''),
                        'status': row.get('status', ''),
                        'city': city.title()
                    }
                    permits.append(clean_permit)

            result[city] = {
                'count': len(permits),
                'permits': permits[:5]  # Just show first 5 for testing
            }
            print(f"Successfully loaded {len(permits)} permits for {city}")

        except Exception as e:
            result[city] = {'error': f'Error reading data for {city}: {str(e)}'}
            print(f"Error for {city}: {e}")

    return result

if __name__ == "__main__":
    print("Testing last-week endpoint logic...")
    result = test_last_week_endpoint()
    print("\nResult:")
    for city, data in result.items():
        if 'error' in data:
            print(f"{city}: ERROR - {data['error']}")
        else:
            print(f"{city}: {data['count']} permits (showing first 5)")