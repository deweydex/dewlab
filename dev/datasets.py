"""Check the datasets in data/ against their sources, and refresh a snapshot.

    python3 dev/datasets.py                  # every dataset with a recipe
    python3 dev/datasets.py life-expectancy  # just one
    python3 dev/datasets.py --refresh life-expectancy

A dataset's `recipe:` in `data/<name>.yaml` says where its source is and how
the snapshot is cut from it. This script fetches the source, shapes it with
the same function a page uses on a live copy (tutorial_tools.shape_live()),
and says how far the snapshot has drifted: how many rows are only in the
source, and how many only in the snapshot. `--refresh` writes the shaped copy over the snapshot and
moves its `snapshot:` date to today.

For a dataset marked `live: true` it also checks the one thing a browser
needs that this script does not: that the source lets a page on another
website read it (an `Access-Control-Allow-Origin` header). Without that,
every reader gets the snapshot, and `live:` should say false.

A refresh changes the numbers every page using the dataset quotes. Before
committing one, run the pages (DECISIONS_LOG 7.250 has the audit this
repository did the first time).
"""

from __future__ import annotations

import argparse
import datetime
import io
import re
import sys
import urllib.request
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
sys.path.insert(0, str(ROOT / "assets"))

import tutorial_tools  # noqa: E402 - needs the path above


def fetch(url: str) -> tuple[bytes, str | None]:
    """The source's bytes, and the CORS header it sent a page from elsewhere."""
    request = urllib.request.Request(url, headers={
        "Origin": "https://example.org",
        "User-Agent": "dewlab dev/datasets.py",
    })
    with urllib.request.urlopen(request, timeout=120) as response:
        return response.read(), response.headers.get("Access-Control-Allow-Origin")


def compare(old: bytes, new: bytes) -> str:
    """How the snapshot and the shaped source differ, in one line.

    Rows are compared whole, as a count of each distinct row, since not
    every dataset has columns that pick out one row (two finds of the same
    genus in the same country, say). A row whose value was revised shows
    as one row only in the source and one only in the snapshot.
    """
    import collections

    import pandas as pd

    before = pd.read_csv(io.BytesIO(old), keep_default_na=False, na_values=[""])
    after = pd.read_csv(io.BytesIO(new), keep_default_na=False, na_values=[""])
    if list(before.columns) != list(after.columns):
        return f"columns differ: {list(before.columns)} against {list(after.columns)}"
    if old == new:
        return "the same as the snapshot"
    rows_before = collections.Counter(map(tuple, before.astype(str).values.tolist()))
    rows_after = collections.Counter(map(tuple, after.astype(str).values.tolist()))
    only_source = sum((rows_after - rows_before).values())
    only_snapshot = sum((rows_before - rows_after).values())
    if not only_source and not only_snapshot:
        return f"{len(after)} rows, the same values, written differently"
    return (f"{len(after)} rows against {len(before)}: {only_source} only in the "
            f"source, {only_snapshot} only in the snapshot")


def set_snapshot_date(path: Path, day: datetime.date) -> None:
    """Moves `snapshot:` in place, so the file's comments and order stay."""
    text = path.read_text()
    text, count = re.subn(r"^snapshot: .*$", f"snapshot: {day.isoformat()}", text,
                          count=1, flags=re.MULTILINE)
    if count != 1:
        raise SystemExit(f"{path} has no snapshot: line to move")
    path.write_text(text)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("names", nargs="*", help="datasets to check (default: all)")
    parser.add_argument("--refresh", action="store_true",
                        help="write the shaped source over the snapshot")
    args = parser.parse_args()

    names = args.names or sorted(p.stem for p in DATA.glob("*.yaml"))
    status = 0
    for name in names:
        meta = yaml.safe_load((DATA / f"{name}.yaml").read_text()) or {}
        recipe = meta.get("recipe")
        if not recipe:
            if args.names:
                print(f"{name}: no recipe:, so nothing to fetch it from")
            continue
        snapshot = DATA / f"{name}.csv"
        try:
            raw, cors = fetch(recipe["url"])
            shaped = tutorial_tools.shape_live(raw, recipe)
        except Exception as exc:  # noqa: BLE001 - report and continue
            print(f"{name}: could not fetch or shape its source: {exc}")
            status = 1
            continue
        if snapshot.exists() and snapshot.stat().st_size:
            print(f"{name}: {compare(snapshot.read_bytes(), shaped)}")
        else:
            print(f"{name}: no snapshot yet")
        if meta.get("live") and cors != "*":
            print(f"  live: true, but {recipe['url']} sends no "
                  "Access-Control-Allow-Origin: *, so a page cannot read it")
            status = 1
        if args.refresh:
            # A copy of a file pages load by its address is the file itself,
            # as the address serves it; shape_live() would only reformat it.
            snapshot.write_bytes(raw if meta.get("address") else shaped)
            set_snapshot_date(DATA / f"{name}.yaml", datetime.date.today())
            print(f"  wrote data/{name}.csv and moved its snapshot: to today")
    return status


if __name__ == "__main__":
    sys.exit(main())
