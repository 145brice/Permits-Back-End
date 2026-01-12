# Contractor Leads Backend

Backend API for the Contractor Leads SaaS platform. Handles permit data scraping, Supabase database storage, user management, and admin dashboard.

## ⚠️ IMPORTANT: API Keys & Credentials

### All API Keys (SAVE THESE!)

| Service | Key | Created | Notes |
|---------|-----|---------|-------|
| **MapTiler** | `jEn4MW4VhPVe82B3bazQ` | 2026-01-07 | Map tiles for frontend |
| **Stripe** | Set in Render env vars | - | Payment processing |
| **SendGrid** | Set in Render env vars | - | Email delivery |
| **Supabase** | See below | 2026-01-11 | Database for permits & users |

### Supabase Database
- **Project URL**: `https://zppsfwxycmujqetsnbtj.supabase.co`
- **Anon Key**: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpwcHNmd3h5Y211anFldHNuYnRqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjgxNzMzNzAsImV4cCI6MjA4Mzc0OTM3MH0.WMHBIe9vACzzBx4Y2t4sNonEWgm0IvYPMyy3tV-eujo`
- **Service Role Key**: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpwcHNmd3h5Y211anFldHNuYnRqIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2ODE3MzM3MCwiZXhwIjoyMDgzNzQ5MzcwfQ.R9ptEOkGAc3xVBf9fgAa3Tse3LWzDGT0VdrcZ4WsaGk`
- **Dashboard**: https://supabase.com/dashboard/project/zppsfwxycmujqetsnbtj

### Render Environment Variables
```bash
SUPABASE_URL=https://zppsfwxycmujqetsnbtj.supabase.co
SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
SENDGRID_API_KEY=SG....
OWNER_EMAIL=145brice@gmail.com
FROM_EMAIL=leads@yourdomain.com
ADMIN_SECRET=admin123
```

### Paid/Admin Emails (hardcoded bypass)
- 145brice@gmail.com
- test@example.com
- admin@permits.com

## Architecture

### Database: Supabase (PostgreSQL)
- **permits** table: All scraped permit data with geocoded coordinates
- **geocode_cache** table: Address → lat/lng mappings to reduce API calls
- **subscribers** table: User subscriptions and Stripe customer data
- See `supabase_setup.sql` for schema

### Data Flow
1. **Scraper runs** → Fetches permits from city APIs
2. **Saves to CSV** → Local backup in `leads/` folder
3. **Uploads to Supabase** → Batch upsert to `permits` table (100 at a time)
4. **Frontend reads** → API serves from Supabase for real-time data

### Firebase (Optional/Legacy)
Firebase integration exists but Supabase is primary database. Firebase can be removed entirely.

## Features

- **Automated Scraping**: Daily scraping from 33+ US cities
- **Supabase Integration**: All permits automatically uploaded to cloud database
- **Manual Scraper Control**: Admin dashboard with run/stop buttons
- **Emergency Kill Switch**: Stop scrapers mid-run if needed
- **Real-time Logs**: View scraper progress in admin dashboard
- **Geocoding Cache**: Efficient address to coordinate mapping
- **User Management**: Stripe + Supabase for subscriptions
- **Email Distribution**: Daily leads via SendGrid

## Supported Cities (33 Total)

### Priority Cities (Always Run First)
- **Austin, TX** ✅ Active
- **Nashville, TN** ✅ Active
- **Houston, TX** ✅ Active (Fixed 2026-01-12)
- **San Antonio, TX** ✅ Active

### All Supported Cities
Austin, Nashville, Houston, San Antonio, Charlotte, Phoenix, Chattanooga, Atlanta, Seattle, San Diego, Chicago, Indianapolis, Columbus, Boston, Philadelphia, Richmond, Milwaukee, Omaha, Knoxville, Birmingham, Snohomish, Maricopa, Mecklenburg, Clark County, Cleveland, Fort Collins, Santa Barbara, Virginia Beach, Tulsa, Colorado Springs, Raleigh, Oklahoma City, Albuquerque

## Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Up Supabase
Run the SQL in `supabase_setup.sql` in your Supabase SQL Editor:
```sql
-- Creates: permits, geocode_cache, subscribers tables
-- Sets up RLS policies for public access
```

### 3. Environment Variables
Create `.env` file or set in Render:
```bash
SUPABASE_URL=https://zppsfwxycmujqetsnbtj.supabase.co
SUPABASE_SERVICE_KEY=your_service_key
STRIPE_SECRET_KEY=your_stripe_key
SENDGRID_API_KEY=your_sendgrid_key
OWNER_EMAIL=your@email.com
```

### 4. Run Server
```bash
# Development
python app.py

# Production (Render)
gunicorn app:app
```

The server will start on port 5000 (or PORT env var).

## API Endpoints

### Public
- `GET /last-week?cities=austin,houston` - Get permits from last 7 days
- `POST /webhook` - Stripe webhook handler
- `GET /health` - Health check

### Admin (Protected)
- `POST /api/run-scrapers` - Trigger manual scraper run (no delay)
- `POST /api/stop-scrapers` - Emergency kill switch
- `GET /api/get-logs` - View recent scraper logs
- `GET /api/get-leads-structure` - View saved CSV structure

### Scraper Behavior
**Manual Runs** (via admin dashboard):
- Start immediately (no delay)
- Run 4 priority cities: Austin, Nashville, Houston, San Antonio
- Check kill switch before each city
- Upload to Supabase after each city completes

**Scheduled Runs** (daily cron):
- Random 0-30 minute delay to avoid rate limits
- Run all 33 cities
- Fallback to previous day's data if scraper fails
- Upload all results to Supabase

## Admin Dashboard

Admin portal at: https://github.com/145brice/Permits-Admin

Features:
- **Run Scrapers Now** button - starts scrapers immediately
- **Stop Scrapers** button - emergency kill switch (appears while running)
- **Live Logs** - updates every 2 seconds during scraper runs
- **City Status Cards** - shows permit count per city (last 7 days)
- **Leads Structure** - view saved CSV files by city and date

## Deployment (Render)

1. **Connect GitHub**: Link this repo to Render
2. **Set Branch**: `main`
3. **Build Command**: `pip install -r requirements.txt`
4. **Start Command**: `gunicorn app:app`
5. **Environment Variables**: Add all keys from above
6. **Auto-deploy**: Enabled (redeploys on push)

Backend URL: `https://permits-back-end.onrender.com`

## Troubleshooting

### No Data in Supabase?
1. Check Render logs for Supabase connection errors
2. Verify `SUPABASE_SERVICE_KEY` is set (not anon key)
3. Check Supabase dashboard → Tables → permits for data
4. Run `simple_migrate.py` to backfill existing CSV data

### Scrapers Not Running?
1. Check admin dashboard logs for errors
2. Verify city APIs are accessible
3. Check `logs/` folder for detailed scraper logs
4. Try running individual scraper: `python scrapers/austin.py`

### Kill Switch Not Working?
1. Kill switch stops after current city finishes (not instant)
2. Check logs for "🛑 KILL SWITCH ACTIVATED" message
3. Scrapers must check flag between cities

## Migration Scripts

- `simple_migrate.py` - Migrate existing CSV data to Supabase
- `migrate_to_supabase.py` - Advanced migration with geocoding
- `count_permits.py` - Check total permits in Supabase
- `check_supabase.py` - Test Supabase connection

## Files & Folders

```
Permits-Back-End/
├── app.py                      # Main Flask application
├── scrapers/                   # City scraper modules
│   ├── austin.py
│   ├── houston.py
│   ├── nashville.py
│   ├── sanantonio.py
│   └── ... (30+ more cities)
├── leads/                      # CSV backups
│   ├── austin/
│   ├── houston/
│   └── ...
├── logs/                       # Scraper logs
├── supabase_setup.sql         # Database schema
├── simple_migrate.py          # Migration tool
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## Recent Updates (2026-01-12)

- ✅ Added Houston scraper (ArcGIS REST API)
- ✅ Created Nashville & San Antonio scrapers
- ✅ Fixed manual scraper runs (removed 0-30min delay)
- ✅ Added emergency kill switch functionality
- ✅ **Integrated automatic Supabase upload after scraping**
- ✅ Scrapers now save to both CSV and Supabase
- ✅ Enhanced admin dashboard with real-time progress
- ✅ Removed old backend repo without Supabase

## License

Proprietary - All Rights Reserved
