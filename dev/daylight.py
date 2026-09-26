"""Make data/daylight.csv: sunrise, sunset and hours of daylight for four
places through one year, from NASA/JPL's Horizons system.

    python3 dev/daylight.py            # writes data/daylight.csv for 2026

Horizons answers one place at a time, as text, not as a CSV, so this
dataset has no recipe and no live source (data/daylight.yaml says so);
this script is how its snapshot was made, and how to make it again.

Each sunrise is paired with the sunset after it, and the row is dated by
the sunrise, in UTC. Pairing that way keeps a Reykjavík summer night,
when the sun sets after midnight UTC, on the day it belongs to.
"""

from __future__ import annotations

import csv
import datetime
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
YEAR = 2026

# Name, then east longitude and latitude in degrees, as Horizons takes them.
PLACES = [
    ("Reykjavik", -21.9426, 64.1466),
    ("Dublin", -6.2603, 53.3498),
    ("Accra", -0.1870, 5.6037),
    ("Cape Town", 18.4241, -33.9249),
]

EVENT = re.compile(r"^\s*(\d{4}-[A-Z][a-z]{2}-\d{2} \d{2}:\d{2})\s+\S?([rs])\s")


def horizons(lon: float, lat: float) -> str:
    """Horizons' rise, transit and set table for the Sun from one place, for
    the whole year, against the true visual horizon: the sun's upper edge,
    with the air's bending of its light, as sunrise is usually defined."""
    query = {
        "format": "text", "COMMAND": "'10'", "EPHEM_TYPE": "'OBSERVER'",
        "CENTER": "'coord@399'", "COORD_TYPE": "'GEODETIC'",
        "SITE_COORD": f"'{lon},{lat},0'",
        "START_TIME": f"'{YEAR}-01-01'", "STOP_TIME": f"'{YEAR + 1}-01-02'",
        "STEP_SIZE": "'1m'", "R_T_S_ONLY": "'TVH'", "QUANTITIES": "'4'",
    }
    url = "https://ssd.jpl.nasa.gov/api/horizons.api?" + urllib.parse.urlencode(query)
    with urllib.request.urlopen(url, timeout=300) as response:
        return response.read().decode("utf-8")


def rows_for(name: str, text: str) -> list[list]:
    body = text.split("$$SOE", 1)[1].split("$$EOE", 1)[0]
    events = []
    for line in body.splitlines():
        match = EVENT.match(line)
        if match:
            when = datetime.datetime.strptime(match.group(1), "%Y-%b-%d %H:%M")
            events.append((when, match.group(2)))
    rows = []
    for i, (when, kind) in enumerate(events):
        if kind != "r" or when.year != YEAR:
            continue
        sunset = next((t for t, k in events[i + 1:] if k == "s"), None)
        if sunset is None:
            continue
        hours = (sunset - when).total_seconds() / 3600
        rows.append([name, when.date().isoformat(), when.strftime("%H:%M"),
                     sunset.strftime("%H:%M"), round(hours, 2)])
    return rows


def main() -> int:
    rows = []
    for name, lon, lat in PLACES:
        found = rows_for(name, horizons(lon, lat))
        print(f"{name}: {len(found)} days", file=sys.stderr)
        rows.extend(found)
    with open(ROOT / "data" / "daylight.csv", "w", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["place", "date", "sunrise_utc", "sunset_utc", "daylight_hours"])
        writer.writerows(rows)
    return 0


if __name__ == "__main__":
    sys.exit(main())
