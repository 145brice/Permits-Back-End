#!/usr/bin/env python3
"""
Create HTML reports from CSV permit data (can be printed to PDF)
"""
import pandas as pd
import os
from datetime import datetime

def create_html_from_csv(csv_path, output_path):
    """Create an HTML report from CSV data"""
    try:
        # Read CSV
        df = pd.read_csv(csv_path)

        # Create HTML content
        city_name = os.path.basename(csv_path).split('_')[1].replace('.csv', '').title()

        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>{city_name} Construction Permits Report</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }}
        .header {{
            background-color: #2c3e50;
            color: white;
            padding: 20px;
            text-align: center;
            border-radius: 5px;
            margin-bottom: 20px;
        }}
        .stats {{
            background-color: #3498db;
            color: white;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
            text-align: center;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            background-color: white;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            border-radius: 5px;
            overflow: hidden;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        th {{
            background-color: #34495e;
            color: white;
            font-weight: bold;
        }}
        tr:nth-child(even) {{
            background-color: #f8f9fa;
        }}
        tr:hover {{
            background-color: #e8f4fd;
        }}
        .footer {{
            text-align: center;
            margin-top: 20px;
            color: #7f8c8d;
            font-size: 12px;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>{city_name} Construction Permits Report</h1>
        <p>Last 7 Days Data</p>
    </div>

    <div class="stats">
        <h2>Report Summary</h2>
        <p><strong>Total Permits:</strong> {len(df)}</p>
        <p><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p><strong>Data Source:</strong> City Permit Database</p>
    </div>

    <table>
        <thead>
            <tr>
"""

        # Add table headers
        for col in df.columns:
            html_content += f"                <th>{col.replace('_', ' ').title()}</th>\n"
        html_content += "            </tr>\n        </thead>\n        <tbody>\n"

        # Add table rows
        for _, row in df.iterrows():
            html_content += "            <tr>\n"
            for value in row:
                html_content += f"                <td>{value}</td>\n"
            html_content += "            </tr>\n"

        html_content += """        </tbody>
    </table>

    <div class="footer">
        <p>This report was automatically generated from permit database records.</p>
        <p>For questions or concerns, please contact the development team.</p>
    </div>
</body>
</html>"""

        # Save HTML file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"✅ Created HTML report: {output_path}")
        return True

    except Exception as e:
        print(f"❌ Failed to create HTML for {csv_path}: {e}")
        return False

def main():
    print("📄 Creating HTML reports from CSV permit data...")

    # Base directory for leads
    leads_dir = os.path.join(os.path.dirname(__file__), '..', 'leads')

    # Cities to process
    cities = ['nashville', 'austin', 'sanantonio']

    for city in cities:
        csv_dir = os.path.join(leads_dir, city, '2026-01-09')
        csv_file = f'2026-01-09_{city}.csv'
        csv_path = os.path.join(csv_dir, csv_file)

        if os.path.exists(csv_path):
            html_file = f'2026-01-09_{city}_permits.html'
            html_path = os.path.join(csv_dir, html_file)

            print(f"\n📊 Processing {city}...")
            create_html_from_csv(csv_path, html_path)
        else:
            print(f"❌ CSV file not found: {csv_path}")

if __name__ == "__main__":
    main()