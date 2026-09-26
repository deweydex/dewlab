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
import math
import re
import sqlite3
import sys
from pathlib import Path

import svgwrite

sys.path.insert(0, str(Path(__file__).resolve().parent))

import erd  # noqa: E402
from palette import (  # noqa: E402
    FILL_AMBER, FILL_BLUE, FILL_GREEN, INK, MONO, MUTED, PANEL, RULE, SANS,
)

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


# The pictures on the first three pages of "A table of your own" are not
# ERDs. They are pictures of a table's rows: which ones a statement picks,
# which values it changes, which rows it takes away. Every value in them
# comes from running the page's own cell here, for the same reason the
# ERDs read the page's own `CREATE TABLE`: a picture that shows a row the
# box does not build is worse than no picture.

ROW_H = 24             # one row of a drawn table
HEAD_H = 28            # the band with the column names in it
CELL_PAD = 9           # inside a cell, left and right
DATA_PT = 11.5
NOTE_PT = 12
STEP_PT = 13
CHAR_W = 0.62          # a monospace character, as a fraction of its size
ARROW_HEAD = 7


def _cell_rows(slug: str, cell_id: str, query: str, *, before: str = "") -> tuple[list[str], list[tuple]]:
    """Run a tutorial cell's own SQL, then `query`, and give back what came out.

    `before` runs first, on a fresh database, for a picture of what a
    statement does to a table the page has already built.
    """
    page = (TUTORIALS / slug / f"{slug}.md").read_text()
    if f"id: {cell_id}" not in page:
        raise SystemExit(f"{slug}: no cell called {cell_id!r} any more")
    script = page.split(f"id: {cell_id}", 1)[1].split("```", 1)[0]
    connection = _database(script + ";\n" + before)
    cursor = connection.execute(query)
    return [column[0] for column in cursor.description], cursor.fetchall()


def _show(value) -> str:
    return f"{value:.1f}" if isinstance(value, float) else str(value)


def _widths(headers: list[str], rows: list[tuple], size: float = DATA_PT) -> list[float]:
    return [
        max(len(text) for text in [header, *(_show(row[index]) for row in rows)])
        * size * CHAR_W + 2 * CELL_PAD
        for index, header in enumerate(headers)
    ]


def _drawing(width: float, height: float) -> svgwrite.Drawing:
    drawing = svgwrite.Drawing(
        size=(f"{width:.0f}px", f"{height:.0f}px"),
        viewBox=f"0 0 {width:.0f} {height:.0f}", debug=False)
    drawing.attribs["fill"] = INK
    drawing.attribs["font-family"] = SANS
    return drawing


def _text(drawing, group, text: str, x: float, y: float, *, size: float = NOTE_PT,
          anchor: str = "start", colour: str = INK, mono: bool = False,
          bold: bool = False, italic: bool = False) -> None:
    group.add(drawing.text(
        text, insert=(x, y), text_anchor=anchor, font_size=f"{size}px",
        font_family=MONO if mono else SANS, fill=colour,
        font_weight="bold" if bold else "normal",
        font_style="italic" if italic else "normal"))


def _arrow(drawing, group, start, end) -> None:
    (x1, y1), (x2, y2) = start, end
    angle = math.atan2(y2 - y1, x2 - x1)
    stop = (x2 - (ARROW_HEAD - 1) * math.cos(angle), y2 - (ARROW_HEAD - 1) * math.sin(angle))
    group.add(drawing.line(start=start, end=stop, stroke=INK, stroke_width=1.5))
    back = [(x2 - ARROW_HEAD * math.cos(angle + turn), y2 - ARROW_HEAD * math.sin(angle + turn))
            for turn in (0.42, -0.42)]
    group.add(drawing.polygon([(x2, y2), *back], fill=INK, stroke="none"))


def _table(drawing, group, x: float, y: float, headers: list[str], rows: list[tuple], *,
           widths: list[float] | None = None, fills: dict | None = None,
           struck: set[int] = frozenset(), faded: set[int] = frozenset(),
           shown: dict | None = None, empty_note: str | None = None) -> tuple[float, float]:
    """One table: a band of column names, then a row per record.

    `fills` maps (row, column) to a fill, with `None` for a whole row or a
    whole column, header included for a column. `struck` rows get a line
    through them, the way a row a statement takes away is drawn. `shown`
    replaces a value's text without changing the row it came from. Returns
    the table's width and height.
    """
    fills = fills or {}
    shown = shown or {}
    widths = widths or _widths(headers, rows)
    width = sum(widths)
    body = max(len(rows), 1) * ROW_H
    height = HEAD_H + body

    def fill_of(row, column):
        for key in ((row, column), (row, None), (None, column)):
            if key in fills:
                return fills[key]
        return None

    left = x
    for column, (header, column_width) in enumerate(zip(headers, widths)):
        group.add(drawing.rect(insert=(left, y), size=(column_width, HEAD_H),
                               fill=fill_of("head", column) or PANEL, stroke="none"))
        _text(drawing, group, header, left + CELL_PAD, y + HEAD_H / 2 + 4,
              size=DATA_PT, mono=True, bold=True)
        top = y + HEAD_H
        for row, values in enumerate(rows):
            fill = fill_of(row, column)
            if fill:
                group.add(drawing.rect(insert=(left, top), size=(column_width, ROW_H),
                                       fill=fill, stroke="none"))
            text = shown.get((row, column), _show(values[column]))
            _text(drawing, group, text, left + CELL_PAD, top + ROW_H / 2 + 4, size=DATA_PT,
                  mono=True, colour=MUTED if row in faded else INK)
            top += ROW_H
        left += column_width

    if not rows and empty_note:
        _text(drawing, group, empty_note, x + width / 2, y + HEAD_H + ROW_H / 2 + 4,
              size=DATA_PT, anchor="middle", colour=MUTED, italic=True)
    for index in range(1, len(rows)):
        line_y = y + HEAD_H + index * ROW_H
        group.add(drawing.line(start=(x, line_y), end=(x + width, line_y),
                               stroke=RULE, stroke_width=0.8))
    left = x
    for column_width in widths[:-1]:
        left += column_width
        group.add(drawing.line(start=(left, y), end=(left, y + height),
                               stroke=RULE, stroke_width=0.8))
    group.add(drawing.line(start=(x, y + HEAD_H), end=(x + width, y + HEAD_H),
                           stroke=INK, stroke_width=1.3))
    for row in struck:
        line_y = y + HEAD_H + row * ROW_H + ROW_H / 2
        group.add(drawing.line(start=(x + 4, line_y), end=(x + width - 4, line_y),
                               stroke=INK, stroke_width=1.6))
    group.add(drawing.rect(insert=(x, y), size=(width, height), fill="none",
                           stroke=INK, stroke_width=1.3, rx=4))
    return width, height


DINOSAURS = ("a-table-is-a-list-of-rows", "create-dinosaurs-table")


def parts_of_a_table() -> str:
    """A shopping list as a table, with its four parts named.

    The page opens with this before any SQL, so a reader has a picture to
    hang *row*, *column*, *cell* and *record* on. Each part is named by a
    label with a line to it, not only by its tint, so the picture still
    reads without colour. The list is invented and says nothing about SQL.
    """
    headers = ["item", "quantity", "aisle"]
    rows = [("Milk", 2, 1), ("Bread", 1, 3), ("Eggs", 12, 1), ("Apples", 6, 5)]
    widths = [96, 96, 76]
    row_pick, column_pick, cell_pick = 2, 1, (3, 2)
    fills = {(row_pick, None): FILL_GREEN, (None, column_pick): FILL_BLUE,
             ("head", column_pick): FILL_BLUE, cell_pick: FILL_AMBER}

    x, y = 24, 34
    drawing = _drawing(620, 256)
    root = drawing.g()
    _text(drawing, root, "a shopping list", x, y - 12, colour=MUTED, italic=True)
    width, height = _table(drawing, root, x, y, headers, rows, widths=widths, fills=fills)
    right = x + width
    label_x = right + 56

    def label(target_y: float, lines: list[str], from_x: float = right) -> None:
        root.add(drawing.line(start=(from_x + 4, target_y), end=(label_x - 8, target_y),
                              stroke=INK, stroke_width=1))
        root.add(drawing.circle(center=(from_x + 4, target_y), r=2.6, fill=INK))
        for index, line in enumerate(lines):
            _text(drawing, root, line, label_x, target_y + 4 + index * 16,
                  bold=index == 0, colour=INK if index == 0 else MUTED)

    label(y + HEAD_H / 2, ["header", "the name of each column"])
    label(y + HEAD_H + row_pick * ROW_H + ROW_H / 2 - 18,
          ["row, or record", "one thing on the list, left to right"])
    root.add(drawing.line(start=(right + 4, y + HEAD_H + row_pick * ROW_H + ROW_H / 2 - 18),
                          end=(right + 4, y + HEAD_H + row_pick * ROW_H + ROW_H / 2),
                          stroke=INK, stroke_width=1))
    label(y + HEAD_H + cell_pick[0] * ROW_H + ROW_H / 2 + 22,
          ["cell", "one value: one box of the grid"])
    root.add(drawing.line(start=(right + 4, y + HEAD_H + cell_pick[0] * ROW_H + ROW_H / 2),
                          end=(right + 4, y + HEAD_H + cell_pick[0] * ROW_H + ROW_H / 2 + 22),
                          stroke=INK, stroke_width=1))

    column_x = x + sum(widths[:column_pick]) + widths[column_pick] / 2
    bottom = y + height
    root.add(drawing.line(start=(column_x, bottom + 4), end=(column_x, bottom + 26),
                          stroke=INK, stroke_width=1))
    root.add(drawing.circle(center=(column_x, bottom + 4), r=2.6, fill=INK))
    _text(drawing, root, "column, or attribute", column_x, bottom + 42, anchor="middle", bold=True)
    _text(drawing, root, "one kind of value, top to bottom,", column_x, bottom + 58,
          anchor="middle", colour=MUTED)
    _text(drawing, root, "the same for every row", column_x, bottom + 74,
          anchor="middle", colour=MUTED)
    drawing.add(root)
    return drawing.tostring()


def three_statements() -> str:
    """What each of the first page's three statements leaves behind.

    Two tables, because two of the statements change something and one
    only reads: `CREATE TABLE` leaves an empty table with its columns named,
    `INSERT INTO` fills it, and `SELECT` shows it. `dinosaur_id` is tinted
    in the second, since no `INSERT` line gives one and the page asks the
    reader to guess what it will hold before running the box.
    """
    headers, rows = _cell_rows(*DINOSAURS, "SELECT * FROM dinosaur_tbl")
    widths = _widths(headers, rows)
    width = sum(widths)
    x = 20
    drawing_width = x * 2 + width
    drawing = _drawing(drawing_width, 410)
    root = drawing.g()

    y = 24
    _text(drawing, root, "1.  CREATE TABLE makes the table: its name and its columns, no rows yet.",
          x, y, size=STEP_PT, bold=True)
    _, height = _table(drawing, root, x, y + 12, headers, [], widths=widths,
                       empty_note="no rows yet")
    y += 12 + height + 26
    _arrow(drawing, root, (x + width / 2, y - 22), (x + width / 2, y - 4))
    y += 18
    _text(drawing, root, "2.  INSERT INTO adds six rows. The database gives each row its dinosaur_id.",
          x, y, size=STEP_PT, bold=True)
    _, height = _table(drawing, root, x, y + 12, headers, rows, widths=widths,
                       fills={(None, 0): FILL_AMBER, ("head", 0): FILL_AMBER})
    y += 12 + height + 26
    _arrow(drawing, root, (x + width / 2, y - 22), (x + width / 2, y - 4))
    y += 18
    _text(drawing, root, "3.  SELECT * FROM dinosaur_tbl reads every row back.",
          x, y, size=STEP_PT, bold=True)
    _text(drawing, root, "It shows them under the box, and changes nothing: the table stays as",
          x + 22, y + 20, colour=MUTED)
    _text(drawing, root, "step 2 left it.", x + 22, y + 36, colour=MUTED)
    drawing.add(root)
    return drawing.tostring()


def columns_and_rows() -> str:
    """`SELECT` picks columns, `WHERE` picks rows, and the answer is where they cross.

    The whole table, with the two named columns tinted one way, the rows the
    condition keeps tinted another, and the cells in both tinted a third.
    Under it, the result the box shows, so the reader can match each of its
    cells to one in the table. The tints are backed up by labels: a mark
    above each picked column, and one beside each kept row.
    """
    headers, rows = _cell_rows(
        "asking-questions-of-a-table", "create-dinosaurs-table", "SELECT * FROM dinosaur_tbl")
    picked = [headers.index("name"), headers.index("length_meters")]
    kept = [index for index, row in enumerate(rows) if row[headers.index("diet")] == "Carnivore"]
    result_headers, result = _cell_rows(
        "asking-questions-of-a-table", "create-dinosaurs-table",
        "SELECT name, length_meters FROM dinosaur_tbl WHERE diet = 'Carnivore'")

    fills = {}
    for column in picked:
        fills[(None, column)] = FILL_BLUE
        fills[("head", column)] = FILL_BLUE
    for row in kept:
        fills[(row, None)] = FILL_GREEN
        for column in picked:
            fills[(row, column)] = FILL_AMBER

    widths = _widths(headers, rows)
    width = sum(widths)
    gutter = 116
    x, y = gutter, 56
    drawing = _drawing(x + width + 20, 400)
    root = drawing.g()

    for column in picked:
        centre = x + sum(widths[:column]) + widths[column] / 2
        _text(drawing, root, "SELECT", centre, y - 26, size=11, anchor="middle", bold=True)
        _arrow(drawing, root, (centre, y - 20), (centre, y - 3))
    _, height = _table(drawing, root, x, y, headers, rows, widths=widths, fills=fills)
    for row in kept:
        middle = y + HEAD_H + row * ROW_H + ROW_H / 2
        _text(drawing, root, "WHERE keeps", x - 26, middle + 4, size=11, anchor="end", bold=True)
        _arrow(drawing, root, (x - 22, middle), (x - 3, middle))

    y += height + 22
    _text(drawing, root, "SELECT name, length_meters FROM dinosaur_tbl WHERE diet = 'Carnivore';",
          x, y + 4, size=11, mono=True)
    _arrow(drawing, root, (x + 60, y + 12), (x + 60, y + 38))
    y += 48
    result_widths = [widths[column] for column in picked]
    _, height = _table(drawing, root, x, y, result_headers, result, widths=result_widths,
                       fills={(None, 0): FILL_AMBER, (None, 1): FILL_AMBER})
    note_x = x + sum(result_widths) + 24
    _text(drawing, root, "What the box shows: only the", note_x, y + 30, colour=MUTED)
    _text(drawing, root, "cells that are in a picked column", note_x, y + 46, colour=MUTED)
    _text(drawing, root, "and in a kept row.", note_x, y + 62, colour=MUTED)
    drawing.add(root)
    return drawing.tostring()


def where_then_order() -> str:
    """The last query on the page, one clause at a time.

    `WHERE` first, drawn as the six rows with the one it drops struck
    through, then `ORDER BY` putting the five that are left in order. The
    two 9.0s sit together at the bottom, which the page's closing challenge
    asks about.
    """
    slug, cell = "asking-questions-of-a-table", "create-dinosaurs-table"
    headers, rows = _cell_rows(slug, cell, "SELECT name, length_meters FROM dinosaur_tbl")
    dropped = {index for index, row in enumerate(rows) if not row[1] > 5}
    sorted_headers, ordered = _cell_rows(
        slug, cell,
        "SELECT name, length_meters FROM dinosaur_tbl WHERE length_meters > 5 "
        "ORDER BY length_meters DESC")
    widths = _widths(headers, rows)
    width = sum(widths)
    gap = 70
    x, y = 20, 52
    drawing = _drawing(x * 2 + width * 2 + gap, 256)
    root = drawing.g()

    _text(drawing, root, "WHERE length_meters > 5", x, y - 26, size=STEP_PT, bold=True, mono=True)
    _text(drawing, root, "keeps five rows, and drops one", x, y - 9, colour=MUTED)
    _table(drawing, root, x, y, headers, rows, widths=widths, struck=dropped, faded=dropped)

    right = x + width + gap
    _arrow(drawing, root, (x + width + 10, y + HEAD_H + 3 * ROW_H), (right - 10, y + HEAD_H + 3 * ROW_H))
    _text(drawing, root, "ORDER BY length_meters DESC", right, y - 26, size=STEP_PT, bold=True, mono=True)
    _text(drawing, root, "then puts those five in order, longest first", right, y - 9, colour=MUTED)
    _table(drawing, root, right, y, sorted_headers, ordered, widths=widths)
    drawing.add(root)
    return drawing.tostring()


def _before_and_after(slug: str, statement_with: str, statement_without: str, query: str, *,
                      titles: tuple[tuple[str, str], tuple[str, str]], mark) -> str:
    """Two copies of a table after one statement: with a `WHERE`, and without.

    `mark(before_rows, after_rows)` says, for one side, which rows to strike
    and which cells to tint, so an `UPDATE` and a `DELETE` can share the
    drawing and differ only in what they do to a row.
    """
    cell = "create-dinosaurs-table"
    headers, before = _cell_rows(slug, cell, query)
    sides = [_cell_rows(slug, cell, query, before=statement)[1]
             for statement in (statement_with, statement_without)]
    marks = [mark(before, after) for after in sides]
    # A changed value is drawn as "old → new", which is wider than either.
    widths = _widths(headers, before)
    for _, _, shown, _ in marks:
        for (_, column), text in shown.items():
            widths[column] = max(widths[column], len(text) * DATA_PT * CHAR_W + 2 * CELL_PAD)
    width = sum(widths)
    gap = 56
    x, y = 20, 70
    drawing = _drawing(x * 2 + width * 2 + gap, y + HEAD_H + len(before) * ROW_H + 62)
    root = drawing.g()
    for index, ((title, note), (struck, fills, shown, summary)) in enumerate(zip(titles, marks)):
        left = x + index * (width + gap)
        _text(drawing, root, note, left, y - 42, size=STEP_PT, bold=True)
        _text(drawing, root, title, left, y - 22, size=11, mono=True, colour=MUTED)
        _table(drawing, root, left, y, headers, before, widths=widths,
               struck=struck, faded=struck, fills=fills, shown=shown)
        for line, text in enumerate(summary.split("\n")):
            _text(drawing, root, text, left, y + HEAD_H + len(before) * ROW_H + 24 + line * 16,
                  bold=line == 0, colour=INK if line == 0 else MUTED)
    drawing.add(root)
    return drawing.tostring()


def update_with_and_without_where() -> str:
    """One `UPDATE`, once with its `WHERE` and once without.

    The same six rows twice, each drawn after the statement has run: on
    the left one cell changed, on the right every cell in the column. Each
    changed cell is tinted and shows its new value, so the right-hand side
    is a column of 2.5s that says what leaving the `WHERE` out costs.
    """
    def mark(before, after):
        changed = [row for row, (old, new) in enumerate(zip(before, after)) if old != new]
        fills = {(row, 1): FILL_AMBER for row in changed}
        shown = {(row, 1): f"{_show(before[row][1])} → {_show(after[row][1])}" for row in changed}
        count = len(changed)
        return set(), fills, shown, f"{count} row{'s' if count != 1 else ''} changed"

    return _before_and_after(
        "changing-what-is-in-it",
        "UPDATE dinosaur_tbl SET length_meters = 2.5 WHERE name = 'Velociraptor'",
        "UPDATE dinosaur_tbl SET length_meters = 2.5",
        "SELECT name, length_meters FROM dinosaur_tbl ORDER BY dinosaur_id",
        titles=(("... WHERE name = 'Velociraptor';", "With WHERE"),
                ("... SET length_meters = 2.5;", "Without WHERE")),
        mark=mark)


def delete_with_and_without_where() -> str:
    """One `DELETE`, once with its `WHERE` and once without.

    Rows a statement removed are struck through rather than left out, so
    the reader sees which ones went. `dinosaur_id` is drawn too: after the
    first `DELETE` the ids left are 1, 2, 3, 4 and 6, and nothing fills the
    gap, which is worth seeing once.
    """
    def mark(before, after):
        gone = {row for row, values in enumerate(before) if values not in after}
        left = len(before) - len(gone)
        if left == 0:
            summary = "no rows left\nthe table and its columns stay"
        else:
            summary = f"{left} row{'s' if left != 1 else ''} left"
        return gone, {}, {}, summary

    return _before_and_after(
        "changing-what-is-in-it",
        "DELETE FROM dinosaur_tbl WHERE name = 'Stegosaurus'",
        "DELETE FROM dinosaur_tbl",
        "SELECT dinosaur_id, name FROM dinosaur_tbl ORDER BY dinosaur_id",
        titles=(("... WHERE name = 'Stegosaurus';", "With WHERE"),
                ("DELETE FROM dinosaur_tbl;", "Without WHERE")),
        mark=mark)


DIAGRAMS = {
    "a-table-is-a-list-of-rows/parts-of-a-table.svg": parts_of_a_table,
    "a-table-is-a-list-of-rows/three-statements.svg": three_statements,
    "asking-questions-of-a-table/columns-and-rows.svg": columns_and_rows,
    "asking-questions-of-a-table/where-then-order.svg": where_then_order,
    "changing-what-is-in-it/update-with-and-without-where.svg": update_with_and_without_where,
    "changing-what-is-in-it/delete-with-and-without-where.svg": delete_with_and_without_where,
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
