import requests

cities = ['austin', 'nashville', 'sanantonio', 'houston', 'charlotte', 'chattanooga', 'phoenix']
API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpwcHNmd3h5Y211anFldHNuYnRqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjgxNzMzNzAsImV4cCI6MjA4Mzc0OTM3MH0.WMHBIe9vACzzBx4Y2t4sNonEWgm0IvYPMyy3tV-eujo'

print("Supabase Permits by City:")
print("=" * 35)

total = 0
for city in cities:
    url = f"https://zppsfwxycmujqetsnbtj.supabase.co/rest/v1/permits?city=eq.{city}&select=id"
    r = requests.get(url, headers={'apikey': API_KEY, 'Prefer': 'count=exact'})
    count = int(r.headers.get('content-range', '0-0/0').split('/')[1])
    total += count
    print(f"  {city:15}: {count:,}")

print("=" * 35)
print(f"  {'TOTAL':15}: {total:,}")
