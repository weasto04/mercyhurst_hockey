"""Utilities to build Stats instances from a CSV file."""
from __future__ import annotations
import csv
from typing import List


def load_stats_from_csv(path: str = "stats.csv") -> List:
    """Read `path` and return a list of `models.Stats` instances.

    Imports `Stats` lazily to avoid side-effects at import time.
    """
    from models import Stats

    stats = []

    def to_int(val: str):
        try:
            return int(val)
        except Exception:
            return None

    def to_float(val: str):
        if not val:
            return None
        v = val.strip()
        if v == "":
            return None
        if v.startswith("."):
            v = "0" + v
        try:
            return float(v)
        except Exception:
            return None

    with open(path, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            number = to_int((row.get("Number") or "").strip())
            first_name = (row.get("First_Name") or "").strip()
            last_name = (row.get("Last_Name") or "").strip()

            s = Stats(
                number=number,
                first_name=first_name,
                last_name=last_name,
                GP=to_int((row.get("GP") or "").strip()),
                G=to_int((row.get("G") or "").strip()),
                A=to_int((row.get("A") or "").strip()),
                PTS=to_int((row.get("PTS") or "").strip()),
                SH=to_int((row.get("SH") or "").strip()),
                SH_PCT=to_float((row.get("SH_PCT") or row.get("SH%") or "").strip()),
                Plus_Minus=to_int((row.get("Plus_Minus") or row.get("+/-") or "").strip()),
                PPG=to_int((row.get("PPG") or "").strip()),
                SHG=to_int((row.get("SHG") or "").strip()),
                FG=to_int((row.get("FG") or "").strip()),
                GWG=to_int((row.get("GWG") or "").strip()),
                GTG=to_int((row.get("GTG") or "").strip()),
                OTG=to_int((row.get("OTG") or "").strip()),
                HTG=to_int((row.get("HTG") or "").strip()),
                UAG=to_int((row.get("UAG") or "").strip()),
                PN_PIM=(row.get("PN-PIM") or "").strip() or None,
                MIN=to_int((row.get("MIN") or "").strip()),
                MAJ=to_int((row.get("MAJ") or "").strip()),
                OTH=to_int((row.get("OTH") or "").strip()),
                BLK=to_int((row.get("BLK") or "").strip()),
            )
            stats.append(s)

    return stats
