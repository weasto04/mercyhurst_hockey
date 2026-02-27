"""Utilities to build Bio instances from the roster CSV."""
from __future__ import annotations
import csv
from typing import List


def load_bios_from_roster(path: str = "roster.csv") -> List:
    """Read `path` and return a list of `models.Bio` instances.

    The function imports `Bio` lazily so callers can import this module
    without immediately requiring a DB engine or side-effects.
    """
    from models import Bio

    bios: List[Bio] = []
    with open(path, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            # normalize and convert fields
            first_name = (row.get("First Name") or "").strip()
            last_name = (row.get("Last Name") or "").strip()

            def to_int(val: str):
                try:
                    return int(val)
                except Exception:
                    return None

            number = to_int((row.get("Number") or "").strip())
            weight = to_int((row.get("Weight") or "").strip())

            bio = Bio(
                first_name=first_name,
                last_name=last_name,
                number=number,
                position=(row.get("Position") or None),
                height=(row.get("Height") or None),
                weight=weight,
                academic_class=(row.get("Class") or None),
                hometown=(row.get("Hometown") or None),
                high_school=(row.get("High School") or None),
            )
            bios.append(bio)

    return bios
