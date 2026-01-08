import csv
import requests
from datetime import datetime
from io import StringIO
from .utils import retry_with_backoff, setup_logger, ScraperHealthCheck, save_partial_results

class ChattanoogaHamiltonPermitScraper:
    def __init__(self):
        self.permits = []
        self.seen_permit_ids = set()
        self.logger = setup_logger('chattanooga_hamilton')
        self.health_check = ScraperHealthCheck('chattanooga_hamilton')

    @retry_with_backoff(max_retries=3, initial_delay=2, exceptions=(requests.RequestException,))
    def scrape_permits(self, max_permits=5000):
        """Chattanooga-Hamilton County - REAL DATA from ChattaData Socrata API"""
        permits = []
        try:
            self.logger.info("🕷️  Searching Chattanooga-Hamilton County (ChattaData API)...")
            print("🕷️  Searching Chattanooga-Hamilton County (ChattaData API)...")

            # ChattaData Open Data Portal: https://www.chattadata.org/
            # Dataset: All Permit Data (764y-vxm2)
            url = "https://www.chattadata.org/resource/764y-vxm2.json"
            params = {
                '$limit': '100',
                '$order': 'applieddate DESC',
                '$where': "permittype='Residential' OR permitclass LIKE '%Residential%'"
            }

            response = requests.get(url, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()

            for record in data:
                # Extract project cost
                value = 0
                if record.get('estprojectcost'):
                    try:
                        value = int(float(record['estprojectcost']))
                    except:
                        pass

                # Build full address
                address = record.get('originaladdress1', 'Unknown')
                city = record.get('originalcity', 'Chattanooga')
                state = record.get('originalstate', 'TN')
                zipcode = record.get('originalzip', '')
                full_address = f"{address}, {city}, {state} {zipcode}".strip()

                permit = {
                    'metro': 'Chattanooga',
                    'county': 'Hamilton',
                    'state': 'TN',
                    'permit_number': record.get('permitnum', 'Unknown'),
                    'address': full_address,
                    'permit_type': record.get('permitclass', 'Building Permit'),
                    'estimated_value': value if value > 0 else None,
                    'work_description': record.get('description', 'No description')[:200],
                    'issue_date': record.get('applieddate', '').split('T')[0] if record.get('applieddate') else None,
                    'scraped_at': datetime.now().isoformat(),
                    'data_source': '🌐 LIVE DATA (chattadata.org)'
                }
                permits.append(permit)

            self.logger.info(f"   ✅ Found {len(permits)} REAL Chattanooga-Hamilton permits")
            print(f"   ✅ Found {len(permits)} REAL Chattanooga-Hamilton permits")
        except Exception as e:
            self.logger.error(f"   ❌ Chattanooga error: {e}")
            print(f"   ❌ Chattanooga error: {e}")

        # Save partial results
        save_partial_results(permits, 'chattanooga_hamilton')
        return permits