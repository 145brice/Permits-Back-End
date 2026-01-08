import csv
import requests
from datetime import datetime
from io import StringIO
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
        save_partial_results(permits, 'san_antonio_bexar')
        return permits