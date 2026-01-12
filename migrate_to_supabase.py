"""
Migrate existing CSV permit data to Supabase
Run this once to upload all permits from CSV files to Supabase
"""

import os
import csv
from supabase import create_client, Client
from datetime import datetime

# Supabase credentials
SUPABASE_URL = "https://zppsfwxycmujqetsnbtj.supabase.co"
SUPABASE_SERVICE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpwcHNmd3h5Y211anFldHNuYnRqIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2ODE3MzM3MCwiZXhwIjoyMDgzNzQ5MzcwfQ.R9ptEOkGAc3xVBf9fgAa3Tse3LWzDGT0VdrcZ4WsaGk"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

def migrate_csv_to_supabase():
    """Read all CSV files and insert permits into Supabase"""
    leads_dir = 'leads'
    total_inserted = 0
    total_skipped = 0
    
    if not os.path.exists(leads_dir):
        print(f"Leads directory not found: {leads_dir}")
        return
    
    # Iterate through each city folder
    for city in os.listdir(leads_dir):
        city_dir = os.path.join(leads_dir, city)
        if not os.path.isdir(city_dir):
            continue
            
        print(f"\nProcessing city: {city}")
        
        # Iterate through each date folder
        for date_folder in os.listdir(city_dir):
            date_path = os.path.join(city_dir, date_folder)
            if not os.path.isdir(date_path):
                continue
            
            # Find CSV files
            csv_files = [f for f in os.listdir(date_path) if f.endswith('.csv')]
            
            for csv_file in csv_files:
                csv_path = os.path.join(date_path, csv_file)
                print(f"  Reading: {csv_path}")
                
                try:
                    with open(csv_path, 'r', encoding='utf-8') as f:
                        reader = csv.DictReader(f)
                        batch = []
                        
                        for row in reader:
                            # Parse the permit data
                            permit = {
                                'permit_number': row.get('permit_number', ''),
                                'address': row.get('address', 'Unknown Address'),
                                'city': city.title(),
                                'zip_code': row.get('zip_code', ''),
                                'permit_type': row.get('permit_type', row.get('work_type', '')),
                                'description': row.get('description', ''),
                                'issue_date': parse_date(row.get('issue_date', row.get('date', date_folder))),
                                'estimated_cost': parse_cost(row.get('estimated_cost', row.get('permit_value', ''))),
                                'status': row.get('status', ''),
                                'owner_name': row.get('owner_name', ''),
                                'contractor': row.get('contractor', ''),
                                'contractor_phone': row.get('contractor_phone', ''),
                                'source': csv_file
                            }
                            
                            # Skip if no permit number (can't dedupe)
                            if not permit['permit_number']:
                                permit['permit_number'] = f"{city}_{permit['address'][:20]}_{date_folder}"
                            
                            batch.append(permit)
                            
                            # Insert in batches of 100
                            if len(batch) >= 100:
                                inserted, skipped = insert_batch(batch)
                                total_inserted += inserted
                                total_skipped += skipped
                                batch = []
                        
                        # Insert remaining
                        if batch:
                            inserted, skipped = insert_batch(batch)
                            total_inserted += inserted
                            total_skipped += skipped
                            
                except Exception as e:
                    print(f"    Error reading {csv_path}: {e}")
    
    print(f"\n{'='*50}")
    print(f"Migration complete!")
    print(f"Total inserted: {total_inserted}")
    print(f"Total skipped (duplicates): {total_skipped}")

def parse_date(date_str):
    """Parse various date formats"""
    if not date_str:
        return None
    try:
        # Try ISO format first
        if 'T' in date_str:
            return date_str.split('T')[0]
        # Try YYYY-MM-DD
        if len(date_str) == 10 and date_str[4] == '-':
            return date_str
        return date_str[:10] if len(date_str) >= 10 else None
    except:
        return None

def parse_cost(cost_str):
    """Parse cost string to decimal"""
    if not cost_str:
        return None
    try:
        # Remove $ and commas
        cleaned = str(cost_str).replace('$', '').replace(',', '').strip()
        return float(cleaned) if cleaned else None
    except:
        return None

def insert_batch(batch):
    """Insert a batch of permits, handling duplicates"""
    import time
    inserted = 0
    skipped = 0
    
    for i, permit in enumerate(batch):
        try:
            # Use upsert to handle duplicates
            result = supabase.table('permits').upsert(
                permit,
                on_conflict='permit_number,city'
            ).execute()
            inserted += 1
            # Small delay to avoid rate limiting
            if i % 10 == 0:
                time.sleep(0.1)
        except Exception as e:
            if 'duplicate' in str(e).lower():
                skipped += 1
            else:
                print(f"    Error inserting: {e}")
                skipped += 1
                time.sleep(0.5)  # Longer delay on error
    
    return inserted, skipped

if __name__ == '__main__':
    print("Starting migration from CSV to Supabase...")
    migrate_csv_to_supabase()
