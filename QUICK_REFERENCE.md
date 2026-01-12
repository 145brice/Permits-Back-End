# Quick Reference - Contractor Leads System

## 🚀 Quick Start

### Run Scrapers Manually
1. Go to admin dashboard (deployed on Vercel/Netlify)
2. Click **"Run Scrapers Now"**
3. Watch logs update every 2 seconds
4. Click **"Stop Scrapers"** if you need to stop early

### Check Supabase Data
1. Go to: https://supabase.com/dashboard/project/zppsfwxycmujqetsnbtj
2. Click **Table Editor** → **permits**
3. You should see new data with today's date

### View Backend Logs (Render)
1. Go to: https://dashboard.render.com
2. Select your **Permits-Back-End** service
3. Click **Logs** tab
4. Look for "☁️ Uploaded X permits to Supabase"

## 📁 Repository Structure

| Repo | Purpose | URL |
|------|---------|-----|
| **Permits-Back-End** | Main backend with scrapers | `c:\Users\user\OneDrive\Desktop\Permits Back End\Permits-Back-End` |
| **Permits-Front-End** | User-facing frontend | `c:\Users\user\OneDrive\Desktop\Fresh Repo Permits Clone\Permits-Front-End` |
| **Permits-Admin** | Admin dashboard | `c:\Users\user\OneDrive\Desktop\Fresh Repo Permits Clone\Permits-Admin` |

## 🔑 Key Credentials

### Supabase
- **URL**: `https://zppsfwxycmujqetsnbtj.supabase.co`
- **Service Key**: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpwcHNmd3h5Y211anFldHNuYnRqIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2ODE3MzM3MCwiZXhwIjoyMDgzNzQ5MzcwfQ.R9ptEOkGAc3xVBf9fgAa3Tse3LWzDGT0VdrcZ4WsaGk`

### Render Backend
- **URL**: `https://permits-back-end.onrender.com`
- **Branch**: `main`
- **Auto-deploy**: Enabled

### Admin Access
- **Email**: `145brice@gmail.com` (hardcoded bypass)

## 🏙️ Active Cities

**Priority (Run First):**
1. Austin, TX
2. Nashville, TN
3. Houston, TX ← **FIXED 2026-01-12**
4. San Antonio, TX

**Total**: 33 cities supported

## 🔧 Common Tasks

### Add a New City Scraper
1. Create `scrapers/newcity.py` based on `austin.py` template
2. Add to `scrapers/__init__.py` imports
3. Add to scraper list in `app.py` (line ~1060)
4. Add to `config.json` for state validation
5. Test: `python scrapers/newcity.py`
6. Commit and push

### Backfill Existing CSV Data to Supabase
```bash
cd "c:\Users\user\OneDrive\Desktop\Permits Back End\Permits-Back-End"
python simple_migrate.py
```

### Check Supabase Connection
```bash
python check_supabase.py
```

### Count Total Permits
```bash
python count_permits.py
```

## ⚠️ Important Notes

### Firebase = LEGACY
- Firebase code exists in `app.py` but is **NOT USED**
- Supabase is the primary database
- Firebase can be removed entirely

### Data Flow
```
Scraper API → CSV File → Supabase Database → Frontend
                ↓
          Local Backup
```

### Scraper Behavior
- **Manual Run**: No delay, 4 cities, check kill switch
- **Scheduled Run**: 0-30min delay, 33 cities, fallback data

### Admin Dashboard
- Logs update every **2 seconds** while scrapers run
- Stop button stays visible **indefinitely** (no timeout)
- Kill switch stops after **current city finishes**

## 🐛 Troubleshooting

### No Data in Supabase?
```bash
# Check logs
https://dashboard.render.com → Logs

# Look for errors
grep -i "supabase" logs/*.log

# Test connection
python check_supabase.py
```

### Scrapers Failing?
```bash
# Test individual scraper
python scrapers/austin.py

# Check city API
curl https://data.austintexas.gov/resource/3syk-w9eu.json?$limit=1
```

### Admin Not Updating?
1. Clear browser cache
2. Check Network tab for API errors
3. Verify backend URL in admin code
4. Check CORS settings in backend

## 📝 Recent Changes (2026-01-12)

1. ✅ **Houston scraper created** - Uses ArcGIS REST API
2. ✅ **Manual runs fixed** - No more random delay
3. ✅ **Kill switch added** - Emergency stop button works
4. ✅ **Supabase auto-upload** - All scraped data goes to cloud DB
5. ✅ **Admin dashboard enhanced** - Real-time progress tracking
6. ✅ **Old backend removed** - Only one source of truth now

## 🎯 Next Steps

- [ ] Remove Firebase code entirely (optional cleanup)
- [ ] Add geocoding to scrapers (lat/lng)
- [ ] Set up automated daily cron job
- [ ] Add email notifications when scrapers fail
- [ ] Create data export functionality for users
