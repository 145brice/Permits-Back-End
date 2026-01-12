import requests

r = requests.get(
    'https://zppsfwxycmujqetsnbtj.supabase.co/rest/v1/permits?select=city',
    headers={
        'apikey': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpwcHNmd3h5Y211anFldHNuYnRqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjgxNzMzNzAsImV4cCI6MjA4Mzc0OTM3MH0.WMHBIe9vACzzBx4Y2t4sNonEWgm0IvYPMyy3tV-eujo',
        'Prefer': 'count=exact'
    },
    timeout=10
)
print(f'Total records: {r.headers.get("content-range", "unknown")}')

# Count by city
from collections import Counter
data = r.json()
cities = Counter([p['city'] for p in data])
print("\nBy city:")
for city, count in cities.most_common():
    print(f"  {city}: {count}")
