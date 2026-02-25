#!/usr/bin/env python3
"""Scrape the Individual Overall Skaters table and write CSV to stdout.

This script uses requests + BeautifulSoup for robust parsing.
"""
import csv
import sys
import requests
from bs4 import BeautifulSoup

URL = 'https://hurstathletics.com/sports/mens-ice-hockey/stats/2025-26'


def dedupe_name(s: str) -> str:
    parts = s.split()
    n = len(parts)
    if n >= 2 and n % 2 == 0 and parts[: n // 2] == parts[n // 2 :]:
        return " ".join(parts[: n // 2])
    return s


def scrape_rows():
    resp = requests.get(URL, timeout=15)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    section = soup.find("section", id="individual-overall-skaters")
    if not section:
        raise SystemExit("Skaters section not found")

    table = section.find("table")
    if not table:
        raise SystemExit("Skaters table not found")

    rows = []
    for tr in table.find_all("tr"):
        # skip header rows
        if tr.find_all("th"):
            continue
        tds = tr.find_all("td")
        if not tds:
            continue

        cells = []
        for td in tds:
            text = td.get_text(" ", strip=True)
            cells.append(text)

        # Normalize player name (2nd column) to remove duplicated variants
        if len(cells) >= 2:
            cells[1] = dedupe_name(cells[1])

        # Drop potential trailing Bio column if present (we expect 22 columns)
        if len(cells) > 22:
            cells = cells[:22]

        if len(cells) == 22:
            rows.append(cells)

    return rows


def main():
    header = [
        "#",
        "Player",
        "GP",
        "G",
        "A",
        "PTS",
        "SH",
        "SH%",
        "+/-",
        "PPG",
        "SHG",
        "FG",
        "GWG",
        "GTG",
        "OTG",
        "HTG",
        "UAG",
        "PN-PIM",
        "MIN",
        "MAJ",
        "OTH",
        "BLK",
    ]

    rows = scrape_rows()

    writer = csv.writer(sys.stdout)
    writer.writerow(header)
    for r in rows:
        writer.writerow(r)


if __name__ == "__main__":
    main()
