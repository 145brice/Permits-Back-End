"""
Simple migration script using direct HTTP requests
"""
import os
import csv
import json
import requests
import time

# Supabase credentials
SUPABASE_URL = "https://zppsfwxycmujqetsnbtj.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpwcHNmd3h5Y211anFldHNuYnRqIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2ODE3MzM3MCwiZXhwIjoyMDgzNzQ5MzcwfQ.R9ptEOkGAc3xVBf9fgAa3Tse3LWzDGT0VdrcZ4WsaGk"

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "resolution=merge-duplicates"
}

cities = ['austin', 'nashville', 'sanantonio', 'houston', 'charlotte', 'chattanooga', 'phoenix']

def migrate():
    total_inserted = 0
    
    for city in cities:
        city_dir = os.path.join('leads', city)
        if not os.path.exists(city_dir):
            print(f"Skipping {city} - folder not found")
            continue
            
        print(f"\nProcessing {city}...")
        
        # Get all date folders
        date_folders = sorted([d for d in os.listdir(city_dir) if os.path.isdir(os.path.join(city_dir, d))], reverse=True)
        
        for date_folder in date_folders:
            date_path = os.path.join(city_dir, date_folder)
            csv_files = [f for f in os.listdir(date_path) if f.endswith('.csv')]
            
            for csv_file in csv_files:
                csv_path = os.path.join(date_path, csv_file)
                print(f"  Reading {csv_path}...")
                
                permits = []
                try:
                    with open(csv_path, 'r', encoding='utf-8') as f:
                        reader = csv.DictReader(f)
                        for row in reader:
                            permit_number = row.get('permit_number', '') or f"{city}_{row.get('address', 'unknown')[:30]}"
                            
                            # Parse estimated cost
                            cost_str = row.get('permit_value', row.get('estimated_cost', ''))
                            try:
                                cost_val = float(cost_str.replace('$', '').replace(',', '')) if cost_str else None
                            except:
                                cost_val = None
                            
                            permit = {
                                "permit_number": permit_number,
                                "address": row.get('address', 'Unknown'),
                                "city": city,
                                "permit_type": row.get('permit_type', 'Permit'),
                                "description": row.get('description', ''),
                                "issue_date": row.get('issue_date', date_folder),
                                "estimated_cost": cost_val,
                                "lat": None,
                                "lng": None
                            }
                            permits.append(permit)
                except Exception as e:
                    print(f"    Error reading CSV: {e}")
                    continue
                
                if permits:
                    # Insert in batches of 50
                    for i in range(0, len(permits), 50):
                        batch = permits[i:i+50]
                        try:
                            response = requests.post(
                                f"{SUPABASE_URL}/rest/v1/permits",
                                headers=headers,
                                json=batch,
                                timeout=30
                            )
                            if response.status_code in [200, 201]:
                                total_inserted += len(batch)
                                print(f"    Inserted batch of {len(batch)}")
                            else:
                                print(f"    Error: {response.status_code} - {response.text[:100]}")
                        except Exception as e:
                            print(f"    Request error: {e}")
                        
                        time.sleep(0.5)
    
    print(f"\n\nMigration complete! Total inserted: {total_inserted}")

if __name__ == '__main__':
    migrate()
