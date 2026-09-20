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


try:
    import tree as tree_renderer
    from tree import Node
    import computational_methods as cm
except ImportError:  # pragma: no cover - exercised only where svgwrite is absent
    tree_renderer = Node = cm = None

needs_tree = pytest.mark.skipif(tree_renderer is None, reason="svgwrite is not installed")


@needs_tree
class TestTreeLayout:
    def test_a_parent_sits_over_the_children_it_has(self):
        root = Node("top", children=[Node("a"), Node("b"), Node("c")])
        tree_renderer._measure(root)
        placed: list = []
        tree_renderer._place(root, 0.0, 0, placed)
        first, last = root.children[0], root.children[-1]
        assert root.centre == pytest.approx((first.centre + last.centre) / 2)

    def test_a_deeper_level_sits_below_a_shallower_one(self):
        root = Node("top", children=[Node("a", children=[Node("deep")])])
        tree_renderer._measure(root)
        placed: list = []
        tree_renderer._place(root, 0.0, 0, placed)
        tops = {node.label: node.top for node in placed}
        assert tops["top"] < tops["a"] < tops["deep"]

    def test_siblings_do_not_overlap(self):
        root = Node("top", children=[
            Node("wide label here"), Node("b"), Node("another wide one"),
        ])
        tree_renderer._measure(root)
        placed: list = []
        tree_renderer._place(root, 0.0, 0, placed)
        spans = sorted(
            (c.centre - c.box_width / 2, c.centre + c.box_width / 2)
            for c in root.children
        )
        for (_, left_end), (right_start, _) in zip(spans, spans[1:]):
            assert right_start >= left_end


@needs_tree
class TestTheRepeatedQuestion:
    """The marked amount has to be the one a reader can count in front of
    them, which is not the one the whole recursion repeats most."""

    def test_counts_are_taken_over_the_drawn_depth_not_the_whole_recursion(self):
        drawn = cm._repeat_counts(6, [1, 3, 4], cm.MAKE_CHANGE_DEPTH)
        whole = cm._repeat_counts(6, [1, 3, 4], 99)
        busiest_drawn = max(
            (a for a in drawn if a not in (0, 6)), key=lambda a: (drawn[a], a))
        busiest_whole = max(
            (a for a in whole if a not in (0, 6)), key=lambda a: (whole[a], a))
        assert busiest_drawn == 2
        assert busiest_whole == 1, "the two differ, which is why depth matters"

    def test_the_marked_amount_appears_more_than_once_in_the_drawing(self):
        counts = cm._repeat_counts(6, [1, 3, 4], cm.MAKE_CHANGE_DEPTH)
        repeated = max(
            (a for a in counts if a not in (0, 6)), key=lambda a: (counts[a], a))
        drawn = cm._call_tree(6, [1, 3, 4], repeated, cm.MAKE_CHANGE_DEPTH)
        marked: list = []

        def walk(node):
            if node.marked:
                marked.append(node.label)
            for child in node.children:
                walk(child)

        walk(drawn)
        assert len(marked) >= 2, "a mark that appears once argues nothing"
        assert set(marked) == {str(repeated)}
