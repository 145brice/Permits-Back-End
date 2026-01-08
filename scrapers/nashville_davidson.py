import csv
import requests
from datetime import datetime
from io import StringIO
from .utils import retry_with_backoff, setup_logger, ScraperHealthCheck, save_partial_results

class NashvilleDavidsonPermitScraper:
    def __init__(self):
        self.permits = []
        self.seen_permit_ids = set()
        self.logger = setup_logger('nashville_davidson')
        self.health_check = ScraperHealthCheck('nashville_davidson')

    @retry_with_backoff(max_retries=3, initial_delay=2, exceptions=(requests.RequestException,))
    def scrape_permits(self, max_permits=5000):
        """Nashville-Davidson County - REAL DATA from ArcGIS"""
        permits = []
        try:
            self.logger.info("🕷️  Scraping Nashville-Davidson County (LIVE DATA - ArcGIS)...")
            print("🕷️  Scraping Nashville-Davidson County (LIVE DATA - ArcGIS)...")

            url = "https://maps.nashville.gov/arcgis/rest/services/Codes/BuildingPermits/MapServer/0/query"
            params = {
                'where': '1=1',
                'outFields': '*',
                'returnGeometry': 'false',
                'resultRecordCount': '100',
                'orderByFields': 'DATE_ACCEPTED DESC',
                'f': 'json'
            }

            response = requests.get(url, params=params, timeout=15)
            if response.status_code == 200:
                data = response.json()

                if 'features' in data:
                    for feature in data['features']:
                        attrs = feature.get('attributes', {})
                        const_val = attrs.get('CONSTVAL', 0) or 0

                        date_accepted = attrs.get('DATE_ACCEPTED')
                        if date_accepted:
                            date_str = datetime.fromtimestamp(date_accepted / 1000).strftime('%Y-%m-%d')
                        else:
                            date_str = 'N/A'

                        permit = {
                            'metro': 'Nashville',
                            'county': 'Davidson',
                            'state': 'TN',
                            'permit_number': attrs.get('CASE_NUMBER', 'N/A'),
                            'address': attrs.get('LOCATION', 'N/A'),
                            'permit_type': attrs.get('CASE_TYPE_DESC', 'Building Permit'),
                            'sub_type': attrs.get('SUB_TYPE_DESC', ''),
                            'estimated_value': float(const_val),
                            'work_description': (attrs.get('SCOPE', 'Construction project') or 'Construction project')[:200],
                            'issue_date': date_str,
                            'status': attrs.get('STATUS_CODE', 'N/A'),
                            'building_sqft': attrs.get('BLDG_SQ_FT', 0) or 0,
                            'scraped_at': datetime.now().isoformat(),
                            'data_source': '🌐 LIVE - Nashville ArcGIS API'
                        }
                        permits.append(permit)

                    self.logger.info(f"   ✅ Found {len(permits)} REAL Nashville-Davidson permits")
                    print(f"   ✅ Found {len(permits)} REAL Nashville-Davidson permits")
            else:
                self.logger.error(f"   ❌ Nashville API error: {response.status_code}")
                print(f"   ❌ Nashville API error: {response.status_code}")
        except Exception as e:
            self.logger.error(f"   ❌ Nashville error: {e}")
            print(f"   ❌ Nashville error: {e}")

        # Save partial results
        save_partial_results(permits, 'nashville_davidson')
        return permits