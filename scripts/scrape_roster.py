import requests
from bs4 import BeautifulSoup
import csv
import sys

URL = 'https://hurstathletics.com/sports/mens-ice-hockey/roster'
OUT = 'roster.csv'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
}
try:
    resp = requests.get(URL, timeout=30, headers=headers)
    resp.raise_for_status()
except Exception as e:
    print('Failed to fetch roster page:', e, file=sys.stderr)
    sys.exit(1)

soup = BeautifulSoup(resp.text, 'lxml')
players = []

# Extract player URLs from JSON-LD if available
import json
from urllib.parse import urljoin

player_urls = []
for script in soup.find_all('script', type='application/ld+json'):
    try:
        data = json.loads(script.string or '')
    except Exception:
        continue
    # data may be a dict containing 'item' list or a list of Person objects
    if isinstance(data, dict) and 'item' in data and isinstance(data['item'], list):
        for it in data['item']:
            url = it.get('url') if isinstance(it, dict) else None
            if url:
                player_urls.append(url)
    elif isinstance(data, list):
        for it in data:
            if isinstance(it, dict) and it.get('@type') == 'Person' and it.get('url'):
                player_urls.append(it.get('url'))

# Fall back: find links to roster.aspx
if not player_urls:
    for a in soup.find_all('a', href=True):
        if 'roster.aspx?rp_id=' in a['href']:
            player_urls.append(a['href'])

player_urls = list(dict.fromkeys(player_urls))

for rel in player_urls:
    url = urljoin(URL, rel)
    try:
        r = requests.get(url, timeout=20, headers=headers)
        r.raise_for_status()
    except Exception as e:
        print('Failed to fetch', url, e)
        continue
    ps = BeautifulSoup(r.text, 'lxml')

    # player block
    div = ps.find('div', class_='sidearm-roster-player-header-details')
    if not div:
        # try alternative wrapper
        div = ps.find('div', class_='sidearm-roster-player-header-info-wrapper') or ps

    # Number
    num_tag = div.find('span', class_='sidearm-roster-player-jersey-number')
    number = num_tag.get_text(strip=True) if num_tag else ''

    # Name
    name_tag = div.find('span', class_='sidearm-roster-player-name')
    first = ''
    last = ''
    if name_tag:
        spans = name_tag.find_all('span')
        if len(spans) >= 2:
            first = spans[0].get_text(strip=True)
            last = spans[1].get_text(strip=True)
        elif len(spans) == 1:
            first = spans[0].get_text(strip=True)

    # Fields
    fields = {}
    for dt in div.find_all('dt'):
        dd = dt.find_next_sibling('dd')
        if dd:
            key = dt.get_text(strip=True).rstrip(':')
            val = dd.get_text(strip=True)
            fields[key] = val

    position = fields.get('Position', '')
    height = fields.get('Height', '')
    weight = fields.get('Weight', '')
    hometown = fields.get('Hometown', '')
    clazz = fields.get('Class', '')
    highschool = fields.get('High School', '') or fields.get('Highschool', '')

    players.append({
        'Position': position,
        'Weight': weight,
        'Height': height,
        'Hometown': hometown,
        'Class': clazz,
        'High School': highschool,
        'Number': number,
        'First Name': first,
        'Last Name': last,
    })

# Write CSV
headers = ['Position','Weight','Height','Hometown','Class','High School','Number','First Name','Last Name']
with open(OUT, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=headers)
    writer.writeheader()
    for p in players:
        writer.writerow(p)

print(f'Wrote {len(players)} players to {OUT}')
