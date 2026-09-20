#!/usr/bin/env python3
"""Every diagram Database Methods uses, and where each one is written.

    python3 dev/graphics/database_methods.py          # report what would change
    python3 dev/graphics/database_methods.py --write  # write it

Each diagram is a function returning an SVG string, so fixing a picture
means fixing a function and running this again — never opening a file and
nudging a box. The schema a diagram is drawn from is a real sqlite database
built here, not a description of one typed twice: if the picture and the
tutorial's own `CREATE TABLE` ever disagree, that is a mistake this makes
visible rather than one it hides.
"""

from __future__ import annotations

import argparse
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import erd  # noqa: E402

TUTORIALS = Path(__file__).resolve().parent.parent.parent / "tutorials"


def _database(statements: str) -> sqlite3.Connection:
    connection = sqlite3.connect(":memory:")
    connection.executescript(statements)
    return connection


def products_and_sales() -> str:
    """The pair *Designing a Table Before You Build It* reasons about.

    A price lives in `products` once. A sale points at it. The diagram is
    there so a reader can see which way round that goes — one product row
    reached by many sales rows, and not the reverse — which is the thing the
    prose has to say twice to make stick.
    """
    return erd.render(erd.schema_from(_database("""
        CREATE TABLE products (
            id INTEGER PRIMARY KEY,
            name TEXT,
            price REAL
        );
        CREATE TABLE sales (
            id INTEGER PRIMARY KEY,
            product_id INTEGER,
            sold_on TEXT,
            quantity INTEGER,
            FOREIGN KEY (product_id) REFERENCES products(id)
        );
    """)))


DIAGRAMS = {
    "designing-a-table-before-you-build-it/products-sales-erd.svg": products_and_sales,
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true",
                        help="write the files rather than reporting on them")
    written = parser.parse_args().write

    changed = 0
    for relative, draw in sorted(DIAGRAMS.items()):
        target = TUTORIALS / relative
        fresh = draw()
        current = target.read_text() if target.exists() else None
        if current == fresh:
            print(f"  unchanged  {relative}")
            continue
        changed += 1
        if written:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(fresh)
            print(f"  written    {relative}")
        else:
            print(f"  would write {relative}")
    if changed and not written:
        print(f"\n{changed} diagram(s) differ. Re-run with --write.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
