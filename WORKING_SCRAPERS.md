# Working Scrapers Documentation

## Currently Active Scrapers (Enabled in Daily Run)

### ✅ Austin, TX - Travis County
- **Scraper Class**: `AustinPermitScraper`
- **File**: `scrapers/austin.py`
- **Data Source**: Socrata Open Data API (`https://data.austintexas.gov/resource/3syk-w9eu.json`)
- **Status**: ✅ ACTIVE - Fetches real permit data
- **Frontend Status**: ✅ Available for download
- **Last Verified**: January 8, 2026

### ✅ Nashville, TN - Davidson County
- **Scraper Class**: `NashvilleDavidsonPermitScraper`
- **File**: `scrapers/nashville_davidson.py`
- **Data Source**: ArcGIS MapServer API (`https://maps.nashville.gov/arcgis/rest/services/Codes/BuildingPermits/MapServer/0/query`)
- **Status**: ✅ ACTIVE - Fetches real permit data from official city API
- **Frontend Status**: ✅ Available for download
- **Last Verified**: January 8, 2026

## Recently Created Scrapers (Not Yet Enabled)

### 🟡 San Antonio, TX - Bexar County
- **Scraper Class**: `SanAntonioBexarPermitScraper`
- **File**: `scrapers/san_antonio_bexar.py`
- **Data Source**: OpenGov CSV Download (`https://data.sanantonio.gov/dataset/.../download/accelasubmitpermitsextract.csv`)
- **Status**: 🟡 CREATED - Code complete, not tested in production
- **Frontend Status**: ❌ Not enabled (San Antonio exists but uses different scraper)
- **Notes**: Parses CSV data, limits to 200 permits per run

### 🟡 Austin, TX - Travis County (Alternative)
- **Scraper Class**: `AustinTravisPermitScraper`
- **File**: `scrapers/austin_travis.py`
- **Data Source**: Socrata Open Data API (same as main Austin scraper)
- **Status**: 🟡 CREATED - Alternative implementation
- **Frontend Status**: ❌ Not enabled (replaced by main Austin scraper)
- **Notes**: Simplified version of the main Austin scraper

## Non-Working Scrapers

### ❌ Chattanooga, TN - Hamilton County
- **Scraper Class**: `ChattanoogaHamiltonPermitScraper`
- **File**: `scrapers/chattanooga_hamilton.py`
- **Data Source**: ChattaData Socrata API (`https://www.chattadata.org/resource/764y-vxm2.json`)
- **Status**: ❌ BROKEN - API access issues
- **Frontend Status**: ❌ Disabled
- **Notes**: User reported scraper doesn't work

## Legacy/Development Scrapers

The following scrapers exist but are either:
- Sample data generators (not real APIs)
- Under development
- Using deprecated methods
- Not integrated into the main system

### Sample Data Scrapers (Not Real APIs)
- `NashvillePermitScraper` (scrapers/nashville.py) - Generates sample data
- `SanAntonioPermitScraper` (scrapers/sanantonio.py) - Generates sample data
- `ChattanoogaPermitScraper` (scrapers/chattanooga.py) - Generates sample data
- And many others in scrapers/ directory

### Development/Experimental Scrapers
- Various Selenium-based scrapers
- HTML table parsers
- Accela-based scrapers
- GIS/ArcGIS scrapers

## Testing Working Scrapers

To test a scraper manually:

```bash
cd "Permits Back End/Permits-Back-End"
python -c "from scrapers import AustinPermitScraper; scraper = AustinPermitScraper(); permits = scraper.run(); print(f'Found {len(permits)} permits')"
```

## Adding New Working Scrapers

1. Create scraper class in `scrapers/` directory
2. Add to `scrapers/__init__.py`
3. Import in `app.py`
4. Add to `run_daily_scrapers()` list
5. Enable in frontend dashboard if ready
6. Test thoroughly before enabling for users

## Data Quality Notes

- **Austin**: High-quality data from official city portal, includes valuation data
- **Nashville**: Real-time data from city GIS system, comprehensive permit details
- All working scrapers include retry logic, error handling, and health monitoring
- CSV files saved to `leads/{city}/{date}/{date}_{city}.csv` format

---

*Last Updated: January 8, 2026*
*Active Cities: 2 (Austin, Nashville)*
*Working Scrapers: 2*</content>
<parameter name="filePath">c:\Users\user\OneDrive\Desktop\Permits Back End\Permits-Back-End\WORKING_SCRAPERS.md