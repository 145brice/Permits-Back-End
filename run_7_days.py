#!/usr/bin/env python3
"""
Run all scrapers for last 7 days
"""
import sys
import os

# Add scrapers to path
sys.path.insert(0, os.path.dirname(__file__))

def run_scraper_for_7_days(city_name, ScraperClass):
    """Run a single scraper for last 7 days"""
    print(f"\n{'='*60}")
    print(f"Running {city_name} scraper for last 7 days...")
    print(f"{'='*60}")

    try:
        scraper = ScraperClass()
        print(f"✅ {city_name} scraper initialized")

        # Run scrape for last 7 days
        print(f"\n🚀 Running scrape for last 7 days...")
        permits = scraper.run()

        if permits:
            print(f"✅ {city_name} scraper completed! Retrieved {len(permits)} permits")
            return True
        else:
            print(f"⚠️  {city_name} scraper returned 0 permits")
            return False

    except Exception as e:
        print(f"❌ {city_name} scraper failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("🚀 Running All Scrapers for Last 7 Days\n")

    from scrapers.nashville import NashvillePermitScraper
    from scrapers.austin import AustinPermitScraper
    from scrapers.sanantonio import SanAntonioPermitScraper

    # Run the 3 main scrapers
    scrapers = [
        ('nashville', NashvillePermitScraper),
        ('austin', AustinPermitScraper),
        ('sanantonio', SanAntonioPermitScraper),
    ]

    results = {}
    for city_name, ScraperClass in scrapers:
        results[city_name] = run_scraper_for_7_days(city_name, ScraperClass)

    print(f"\n{'='*60}")
    print("SCRAPER RUN SUMMARY")
    print(f"{'='*60}")
    for city, success in results.items():
        status = "✅ SUCCESS" if success else "❌ FAILED"
        print(f"{city.upper()}: {status}")

if __name__ == "__main__":
    main()