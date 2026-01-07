#!/usr/bin/env python3
"""Test scrapers and save results to CSV"""
import sys
import os
import csv
from datetime import datetime
sys.path.insert(0, os.path.dirname(__file__))

def test_and_save(city_name, ScraperClass):
    try:
        print(f"Testing {city_name}...", end=" ", flush=True)
        scraper = ScraperClass()
        permits = scraper.scrape_permits(max_permits=10, days_back=7)
        
        if permits and len(permits) > 0:
            # Save to CSV
            filename = f"test_{city_name.lower().replace(' ', '_')}.csv"
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=permits[0].keys())
                writer.writeheader()
                writer.writerows(permits)
            print(f"✓ {len(permits)} permits -> {filename}")
            return len(permits)
        else:
            print(f"✗ No permits")
            return 0
    except Exception as e:
        print(f"✗ ERROR: {str(e)[:50]}")
        return -1

def main():
    print("Testing All Scrapers (10 permits max per city)\n")
    
    from scrapers.nashville import NashvillePermitScraper
    from scrapers.austin import AustinPermitScraper
    from scrapers.houston import HoustonPermitScraper
    from scrapers.sanantonio import SanAntonioPermitScraper
    from scrapers.charlotte import CharlottePermitScraper
    from scrapers.chattanooga import ChattanoogaPermitScraper
    from scrapers.phoenix import PhoenixPermitScraper
    from scrapers.atlanta import AtlantaPermitScraper
    from scrapers.philadelphia import PhiladelphiaPermitScraper
    from scrapers.dallas import DallasPermitScraper
    from scrapers.indianapolis import IndianapolisPermitScraper
    from scrapers.raleigh import RaleighPermitScraper
    from scrapers.sandiego import SanDiegoPermitScraper
    from scrapers.seattle import SeattlePermitScraper
    from scrapers.cleveland import ClevelandPermitScraper

    scrapers = [
        ('Nashville', NashvillePermitScraper),
        ('Austin', AustinPermitScraper),
        ('Houston', HoustonPermitScraper),
        ('San Antonio', SanAntonioPermitScraper),
        ('Charlotte', CharlottePermitScraper),
        ('Chattanooga', ChattanoogaPermitScraper),
        ('Phoenix', PhoenixPermitScraper),
        ('Atlanta', AtlantaPermitScraper),
        ('Philadelphia', PhiladelphiaPermitScraper),
        ('Dallas', DallasPermitScraper),
        ('Indianapolis', IndianapolisPermitScraper),
        ('Raleigh', RaleighPermitScraper),
        ('San Diego', SanDiegoPermitScraper),
        ('Seattle', SeattlePermitScraper),
        ('Cleveland', ClevelandPermitScraper),
    ]

    results = {}
    for city_name, ScraperClass in scrapers:
        results[city_name] = test_and_save(city_name, ScraperClass)

    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    
    working = [(c, n) for c, n in results.items() if n > 0]
    failing = [c for c, n in results.items() if n < 0]
    empty = [c for c, n in results.items() if n == 0]
    
    print(f"\nWorking ({len(working)}):")
    for city, count in working:
        print(f"  {city}: {count} permits")
    
    if empty:
        print(f"\nEmpty ({len(empty)}): {', '.join(empty)}")
    if failing:
        print(f"\nFailing ({len(failing)}): {', '.join(failing)}")

if __name__ == '__main__':
    main()
