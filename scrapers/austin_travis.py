import csv
import requests
from datetime import datetime
from io import StringIO
from .utils import retry_with_backoff, setup_logger, ScraperHealthCheck, save_partial_results

class AustinTravisPermitScraper:
    def __init__(self):
        self.permits = []
        self.seen_permit_ids = set()
        self.logger = setup_logger('austin_travis')
        self.health_check = ScraperHealthCheck('austin_travis')

    @retry_with_backoff(max_retries=3, initial_delay=2, exceptions=(requests.RequestException,))
    def scrape_permits(self, max_permits=5000):
        """Austin-Travis County - REAL DATA from Socrata API"""
        permits = []
        try:
            self.logger.info("🕷️  Searching Austin-Travis County (Socrata API)...")
            print("🕷️  Searching Austin-Travis County (Socrata API)...")

            # Austin Open Data Portal: https://data.austintexas.gov/
            # Dataset: Issued Construction Permits (3syk-w9eu)
            url = "https://data.austintexas.gov/resource/3syk-w9eu.json"
            params = {
                '$limit': '100',
                '$order': 'applieddate DESC',
                '$where': "permit_class_mapped='Residential'"
            }

            response = requests.get(url, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()

            for record in data:
                # Extract construction value if available
                value = 0
                if record.get('total_job_valuation'):
                    try:
                        value = int(float(record['total_job_valuation']))
                    except:
                        pass

                permit = {
                    'metro': 'Austin',
                    'county': 'Travis',
                    'state': 'TX',
                    'permit_number': record.get('permit_number', 'Unknown'),
                    'address': record.get('permit_location', 'Unknown'),
                    'permit_type': record.get('permit_type_desc', 'Building Permit'),
                    'estimated_value': value if value > 0 else None,
                    'work_description': record.get('description', 'No description'),
                    'issue_date': record.get('applieddate', '').split('T')[0] if record.get('applieddate') else None,
                    'scraped_at': datetime.now().isoformat(),
                    'data_source': '🌐 LIVE DATA (data.austintexas.gov)'
                }
                permits.append(permit)

            self.logger.info(f"   ✅ Found {len(permits)} REAL Austin-Travis permits")
            print(f"   ✅ Found {len(permits)} REAL Austin-Travis permits")
        except Exception as e:
            self.logger.error(f"   ❌ Austin error: {e}")
            print(f"   ❌ Austin error: {e}")

        # Save partial results
        save_partial_results(permits, 'austin_travis')
        return permits