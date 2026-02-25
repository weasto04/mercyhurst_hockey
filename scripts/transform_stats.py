#!/usr/bin/env python3
import csv

IN = 'stats.csv'

with open(IN, newline='') as f:
    reader = csv.reader(f)
    rows = list(reader)

if not rows:
    raise SystemExit('empty csv')

old_header = rows[0]
new_header = []
player_idx = None
for i, col in enumerate(old_header):
    if col.strip() == '#':
        new_header.append('Number')
    elif col.strip() == 'Player':
        new_header.extend(['First_Name', 'Last_Name'])
        player_idx = i
    elif col.strip() == 'SH%':
        new_header.append('SH_PCT')
    elif col.strip() == '+/-':
        new_header.append('Plus_Minus')
    else:
        new_header.append(col)

new_rows = [new_header]
for row in rows[1:]:
    new_row = []
    for i, col in enumerate(old_header):
        val = row[i] if i < len(row) else ''
        if col.strip() == 'Player':
            v = val.strip()
            if ',' in v:
                last, first = v.split(',', 1)
                first = first.strip()
                last = last.strip()
            else:
                parts = v.split()
                if len(parts) >= 2:
                    first = parts[-1]
                    last = ' '.join(parts[:-1])
                else:
                    first = v
                    last = ''
            new_row.extend([first, last])
        elif col.strip() == '#':
            new_row.append(val)
        elif col.strip() == 'SH%':
            new_row.append(val)
        elif col.strip() == '+/-':
            new_row.append(val)
        else:
            new_row.append(val)
    new_rows.append(new_row)

with open(IN, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(new_rows)

print(f'Wrote {len(new_rows)-1} data rows to {IN}')
