"""The ER diagram generator's layout rules.

`svgwrite` is not a build dependency — nothing in `dev/graphics/` runs during
a build, and CI never installs it — so these skip where it is absent rather
than forcing it into `requirements-build.txt` for a picture.
"""

from __future__ import annotations

import sqlite3
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "dev" / "graphics"))

try:
    import erd
except ImportError:  # pragma: no cover - exercised only where svgwrite is absent
    erd = None

needs_svgwrite = pytest.mark.skipif(erd is None, reason="svgwrite is not installed")

TIMETABLE = """
CREATE TABLE programmes (id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE teachers  (id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE rooms     (id INTEGER PRIMARY KEY, name TEXT, capacity INTEGER);
CREATE TABLE modules   (id INTEGER PRIMARY KEY, name TEXT, programme_id INTEGER,
    FOREIGN KEY (programme_id) REFERENCES programmes(id));
CREATE TABLE sessions  (id INTEGER PRIMARY KEY, module_id INTEGER, teacher_id INTEGER,
    room_id INTEGER, session_date TEXT,
    FOREIGN KEY (module_id) REFERENCES modules(id),
    FOREIGN KEY (teacher_id) REFERENCES teachers(id),
    FOREIGN KEY (room_id) REFERENCES rooms(id));
"""


def database(statements: str) -> sqlite3.Connection:
    connection = sqlite3.connect(":memory:")
    connection.executescript(statements)
    return connection


@needs_svgwrite
class TestReadingASchema:
    def test_a_declared_foreign_key_is_reported(self):
        schema = erd.schema_from(database(TIMETABLE))
        modules = {c["name"]: c for c in schema["modules"]["columns"]}
        assert modules["programme_id"]["references"] == ("programmes", "id")
        assert modules["id"]["primary"] is True

    def test_a_column_that_only_looks_like_a_key_draws_no_arrow(self):
        """`PRAGMA foreign_key_list` reports what was declared, not what was
        named suggestively — which is the honest picture of the schema."""
        schema = erd.schema_from(database(
            "CREATE TABLE a (id INTEGER PRIMARY KEY);"
            "CREATE TABLE b (id INTEGER PRIMARY KEY, a_id INTEGER);"
        ))
        assert schema["b"]["columns"][1]["references"] is None


@needs_svgwrite
class TestLayout:
    def test_a_table_sits_to_the_right_of_what_it_points_at(self):
        depth = erd._depth(erd.schema_from(database(TIMETABLE)))
        assert depth["programmes"] == 0
        assert depth["modules"] == 1
        assert depth["sessions"] == 2

    def test_a_cycle_does_not_loop_forever(self):
        """Two tables naming each other have no left-to-right order. It has
        to settle on something rather than run until the process is killed."""
        depth = erd._depth({
            "a": {"columns": [{"name": "b_id", "references": ("b", "id"),
                               "primary": False, "type": "integer"}]},
            "b": {"columns": [{"name": "a_id", "references": ("a", "id"),
                               "primary": False, "type": "integer"}]},
        })
        assert set(depth) == {"a", "b"}


@needs_svgwrite
class TestTheDrawing:
    def test_colours_are_theme_tokens_rather_than_literals(self):
        """A literal here would need `dev/normalise_svg.py` to map it back,
        and would be wrong in at least one of the four display modes until
        it did."""
        import re

        svg = erd.render(erd.schema_from(database(TIMETABLE)))
        literals = {
            value for value in re.findall(r'(?:fill|stroke)="([^"]+)"', svg)
            if value not in ("none",)
            and not value.startswith("var(--dl-")
            and value != "currentColor"
        }
        assert not literals, f"literal colours in the output: {sorted(literals)}"

    def test_an_edge_reaching_past_a_column_does_not_cross_it(self):
        """`rooms` points at `sessions` two columns away. The straight line
        would run through whatever sits between, so it drops below every box
        instead — which shows up as a turn beneath the tallest of them."""
        schema = erd.schema_from(database(TIMETABLE))
        placed = erd._layout(schema)
        boxes_bottom = placed["height"]
        svg = erd.render(schema)
        ys = [
            float(pair.split(",")[1])
            for points in __import__("re").findall(r'points="([^"]+)"', svg)
            for pair in points.split()
        ]
        assert max(ys) > boxes_bottom, "no edge was routed below the boxes"
