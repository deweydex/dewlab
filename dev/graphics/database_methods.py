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
import re
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


def _schema_from_cell(slug: str, cell_id: str) -> sqlite3.Connection:
    """Build the schema out of a tutorial's own `CREATE TABLE` statements.

    Reading the page rather than restating it is what stops a diagram
    quietly describing a schema the tutorial no longer builds. If the cell
    is renamed or its statements change shape, this raises here at
    generation time rather than shipping a picture that has gone wrong.
    """
    page = (TUTORIALS / slug / f"{slug}.md").read_text()
    if f"id: {cell_id}" not in page:
        raise SystemExit(f"{slug}: no cell called {cell_id!r} any more")
    block = page.split(f"id: {cell_id}", 1)[1].split("```", 1)[0]
    statements = [m.group(0) for m in re.finditer(r"CREATE TABLE.*?\);", block, re.S)]
    if not statements:
        raise SystemExit(f"{slug}/{cell_id}: no CREATE TABLE statements found")
    return _database("\n".join(statements))


def _schema_from_section(slug: str, heading: str) -> sqlite3.Connection:
    """Build the schema out of the `CREATE TABLE` statements under a heading.

    For a worked solution, which is plain SQL in a fold rather than a cell
    with an id. Same reason as `_schema_from_cell()`: read the page, so the
    picture cannot describe a schema the page does not show.
    """
    page = (TUTORIALS / slug / f"{slug}.md").read_text()
    if heading not in page:
        raise SystemExit(f"{slug}: no section called {heading!r} any more")
    block = page.split(heading, 1)[1]
    statements = [m.group(0) for m in re.finditer(r"CREATE TABLE.*?\);", block, re.S)]
    if not statements:
        raise SystemExit(f"{slug}/{heading}: no CREATE TABLE statements found")
    return _database("\n".join(statements))


def products_and_sales() -> str:
    """The pair *Designing tables: columns, types and one-to-many links* reasons about.

    A price lives in `product_tbl` once. A sale points at it. The diagram is
    there so a reader can see which way round that goes — one product row
    reached by many sale rows, and not the reverse — which is the thing the
    prose has to say twice to make stick.

    The page has no cell building these two, so the schema is written here,
    in the course's convention: `_tbl` names, a key named after its table,
    and the foreign key directly under the key. The line runs from
    `product_id` to `product_id`, which is the point the prose makes.
    """
    return erd.render(erd.schema_from(_database("""
        CREATE TABLE product_tbl (
            product_id INTEGER PRIMARY KEY,
            product_name TEXT,
            price REAL
        );
        CREATE TABLE sale_tbl (
            sale_id INTEGER PRIMARY KEY,
            product_id INTEGER,
            sold_on TEXT,
            quantity INTEGER,
            FOREIGN KEY (product_id) REFERENCES product_tbl(product_id)
        );
    """)))


def college_timetable() -> str:
    """The five tables *A college timetable: five tables and finding clashes* builds.

    Four tables describing things, and a fifth describing an event that ties
    several of them together — the shape the section names in prose and
    which takes a paragraph to assemble from sentences. Drawn from the
    page's own `CREATE TABLE` statements, so it says what the page builds.
    """
    return erd.render(erd.schema_from(
        _schema_from_cell("a-college-timetable", "create-timetable-tables")))


def plushies_solution() -> str:
    """The shape the plushies quiz's worked solution builds.

    It sits inside the answer fold, beside the SQL it describes: before it,
    the picture would hand over the design the tasks ask the reader to
    arrive at themselves.
    """
    return erd.render(erd.schema_from(
        _schema_from_section("the-tentacular-plushies-quiz", "## One way to do it")))


def library_solution() -> str:
    """The library quiz's five tables, with `book_author_tbl` between two of them.

    A junction table is the thing this quiz is actually about, and it is the
    one relationship a reader cannot check by reading a single `CREATE
    TABLE`: crow's feet at both ends of the middle box are what say
    many-to-many.
    """
    return erd.render(erd.schema_from(
        _schema_from_section("the-library-loans-quiz", "## One way to do it")))


DIAGRAMS = {
    "designing-a-table-before-you-build-it/products-sales-erd.svg": products_and_sales,
    "a-college-timetable/timetable-erd.svg": college_timetable,
    "the-tentacular-plushies-quiz/plushies-erd.svg": plushies_solution,
    "the-library-loans-quiz/library-erd.svg": library_solution,
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
