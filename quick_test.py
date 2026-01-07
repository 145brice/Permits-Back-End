#!/usr/bin/env python3
"""Quick test all scrapers - clean output"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

def test_scraper(city_name, ScraperClass):
    try:
        scraper = ScraperClass()
        permits = scraper.scrape_permits(max_permits=100, days_back=7)
        return len(permits) if permits else 0
    except Exception as e:
        print(f"ERROR {city_name}: {e}")
        return -1

def main():
    print("Testing All Scrapers...\n")
    
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
        print(f"Testing {city_name}...", end=" ")
        count = test_scraper(city_name, ScraperClass)
        results[city_name] = count
        if count > 0:
            print(f"OK ({count} permits)")
        elif count == 0:
            print(f"WARN (0 permits)")
        else:
            print(f"FAIL")

    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    
    working = [c for c, n in results.items() if n > 0]
    failing = [c for c, n in results.items() if n < 0]
    empty = [c for c, n in results.items() if n == 0]
    
    print(f"\nWorking ({len(working)}): {', '.join(working) if working else 'None'}")
    print(f"Empty ({len(empty)}): {', '.join(empty) if empty else 'None'}")
    print(f"Failing ({len(failing)}): {', '.join(failing) if failing else 'None'}")

if __name__ == '__main__':
    main()
