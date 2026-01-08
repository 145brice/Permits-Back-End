import csv
import requests
from datetime import datetime
from io import StringIO
import os
from .utils import retry_with_backoff, setup_logger, ScraperHealthCheck, save_partial_results

class SanAntonioBexarPermitScraper:
    def __init__(self):
        self.permits = []
        self.seen_permit_ids = set()
        self.logger = setup_logger('san_antonio_bexar')
        self.health_check = ScraperHealthCheck('san_antonio_bexar')

    @retry_with_backoff(max_retries=3, initial_delay=2, exceptions=(requests.RequestException,))
    def scrape_permits(self, max_permits=5000):
        """San Antonio-Bexar County - REAL DATA from OpenGov CSV"""
        permits = []
        try:
            self.logger.info("🕷️  Scraping San Antonio-Bexar County (OpenGov CSV)...")
            print("🕷️  Scraping San Antonio-Bexar County (OpenGov CSV)...")

            # San Antonio OpenGov CSV - Direct download
            csv_url = 'https://data.sanantonio.gov/dataset/05012dcb-ba1b-4ade-b5f3-7403bc7f52eb/resource/fbb7202e-c6c1-475b-849e-c5c2cfb65833/download/accelasubmitpermitsextract.csv'

            response = requests.get(csv_url, timeout=30)
            response.raise_for_status()

            # Parse CSV
            csv_data = StringIO(response.text)
            reader = csv.DictReader(csv_data)

            count = 0
            for row in reader:
                # Filter for building permits only (not garage sales, signs, etc.)
                permit_type = row.get('PERMIT TYPE', '')
                if not any(keyword in permit_type.lower() for keyword in ['building', 'commercial', 'residential', 'mep', 'trade', 'repair']):
                    continue

                # Map CSV columns to our format
                permit = {
                    'metro': 'San Antonio',
                    'county': 'Bexar',
                    'state': 'TX',
                    'permit_number': row.get('PERMIT #', ''),
                    'address': row.get('ADDRESS', ''),
                    'permit_type': permit_type,
                    'estimated_value': int(float(row.get('DECLARED VALUATION', 0) or 0)),
                    'work_description': row.get('WORK TYPE', ''),
                    'owner_name': row.get('PRIMARY CONTACT', ''),
                    'project_name': row.get('PROJECT NAME', ''),
                    'issue_date': row.get('DATE ISSUED', ''),
                    'applied_date': row.get('DATE SUBMITTED', ''),
                    'area_sf': row.get('AREA (SF)', ''),
                    'scraped_at': datetime.now().isoformat(),
                    'data_source': '✅ LIVE - San Antonio OpenGov CSV'
                }
                permits.append(permit)
                count += 1

                # Limit to 200 permits per scrape
                if count >= 200:
                    break

            self.logger.info(f"   ✅ Scraped {len(permits)} REAL San Antonio-Bexar building permits")
            print(f"   ✅ Scraped {len(permits)} REAL San Antonio-Bexar building permits")
        except Exception as e:
            self.logger.error(f"   ❌ San Antonio error: {e}")
            print(f"   ❌ San Antonio error: {e}")

        # Save partial results
        save_partial_results(permits, f'../leads/sanantonio/{datetime.now().strftime("%Y-%m-%d")}/{datetime.now().strftime("%Y-%m-%d")}_sanantonio_partial.csv', 'san_antonio_bexar')
        return permits

    def save_to_csv(self, filename=None):
        """Save permits to CSV file"""
        if not self.permits:
            return
        if filename is None:
            today = datetime.now().strftime('%Y-%m-%d')
            filename = f'../leads/sanantonio/{today}/{today}_sanantonio.csv'
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        import csv
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=list(self.permits[0].keys()))
            writer.writeheader()
            writer.writerows(self.permits)
        print(f"✅ Saved {len(self.permits)} permits to {filename}")

    def run(self):
        """Main execution with error handling and auto-recovery"""
        try:
            self.permits = self.scrape_permits()
            if self.permits:
                self.save_to_csv()
                self.logger.info(f"✅ Scraped {len(self.permits)} permits for san_antonio_bexar")
                print(f"✅ Scraped {len(self.permits)} permits for san_antonio_bexar")
                return self.permits
            else:
                self.logger.warning("❌ No permits scraped for san_antonio_bexar")
                print(f"❌ No permits scraped for san_antonio_bexar - will retry next run")
                return []
        except Exception as e:
            self.logger.error(f"Fatal error in scraper: {e}", exc_info=True)
            self.health_check.record_failure(str(e))
            print(f"❌ Fatal error in san_antonio_bexar scraper: {e}")
            return []