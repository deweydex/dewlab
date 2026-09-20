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


try:
    import states as state_renderer
except ImportError:  # pragma: no cover - exercised only where svgwrite is absent
    state_renderer = None

needs_states = pytest.mark.skipif(state_renderer is None, reason="svgwrite is not installed")


@needs_states
class TestStateDiagram:
    WEATHER = [[0.7, 0.3], [0.4, 0.6]]

    def test_every_entry_of_the_matrix_gets_an_arrow(self):
        """Including the two on the diagonal. Dropping a self-loop would make
        a row look as though it did not sum to one."""
        svg = state_renderer.render(["sunny", "rainy"], self.WEATHER,
                                    fmt=lambda p: f"{round(p * 100)}%")
        for row in self.WEATHER:
            for probability in row:
                assert f">{round(probability * 100)}%<" in svg

    def test_a_zero_chance_draws_no_arrow(self):
        svg = state_renderer.render(["a", "b"], [[1.0, 0.0], [0.0, 1.0]],
                                    fmt=lambda p: f"{p:g}")
        assert svg.count(">0<") == 0

    def test_the_matrix_is_read_from_the_tutorial_not_restated(self):
        matrix = cm._matrix_from_cell("where-chains-lead", "a-weather-machine-1", "P")
        assert matrix == self.WEATHER
        for row in matrix:
            assert sum(row) == pytest.approx(1.0), "a row that does not sum to 1"

    def test_more_than_two_states_says_so_rather_than_drawing_badly(self):
        with pytest.raises(ValueError, match="two states"):
            state_renderer.render(["a", "b", "c"], [[1, 0, 0], [0, 1, 0], [0, 0, 1]])


try:
    import maths as maths_diagrams
except ImportError:  # pragma: no cover - exercised only where svgwrite is absent
    maths_diagrams = None

needs_maths = pytest.mark.skipif(maths_diagrams is None, reason="svgwrite is not installed")


@needs_maths
class TestTheTwoAcesTree:
    def test_it_draws_the_numbers_the_page_multiplies(self):
        svg = maths_diagrams.drawing_two_aces()
        assert ">4/52<" in svg and ">3/51<" in svg

    def test_both_second_draws_are_out_of_the_same_smaller_deck(self):
        """One card is gone whichever one it was — that shared 51 is half of
        what makes the two draws dependent."""
        svg = maths_diagrams.drawing_two_aces()
        assert ">3/51<" in svg and ">4/51<" in svg, "the numerators must differ"

    def test_sibling_branches_summing_wrong_stops_generation(self, monkeypatch):
        """A tree whose branches do not sum to 1 is arithmetic a reader would
        be right to distrust, so it fails here rather than shipping."""
        monkeypatch.setattr(maths_diagrams, "ACES", 5)
        monkeypatch.setattr(maths_diagrams, "CARDS", 0)
        with pytest.raises(ZeroDivisionError):
            maths_diagrams.drawing_two_aces()


try:
    import grids as grid_renderer
except ImportError:  # pragma: no cover - exercised only where svgwrite is absent
    grid_renderer = None

needs_grids = pytest.mark.skipif(grid_renderer is None, reason="svgwrite is not installed")


@needs_grids
class TestRowTimesColumn:
    A = [[1, 2], [3, 4]]
    B = [[5, 0], [1, -1]]
    AB = [[7, -2], [19, -4]]

    def test_the_working_matches_the_entry_it_explains(self):
        svg = grid_renderer.row_times_column(self.A, self.B, self.AB, row=0, column=0)
        assert "1×5 + 2×1 = 7" in svg

    def test_it_draws_the_matrices_the_tutorial_defines(self):
        left, right = cm._matrices_from_cell(
            "multiplying-grids", "multiplying-two-grids-3", ("A", "B"))
        assert left == self.A and right == self.B
        columns = list(zip(*right))
        product = [[sum(a * b for a, b in zip(r, c)) for c in columns] for r in left]
        assert product == self.AB, "the tutorial's own numbers changed"

    def test_a_different_entry_picks_a_different_row_and_column(self):
        svg = grid_renderer.row_times_column(self.A, self.B, self.AB, row=1, column=1)
        assert "3×0 + 4×-1 = -4" in svg


try:
    import steps as step_renderer
except ImportError:  # pragma: no cover - exercised only where svgwrite is absent
    step_renderer = None

needs_steps = pytest.mark.skipif(step_renderer is None, reason="svgwrite is not installed")


@needs_steps
class TestTheRangeCollapsing:
    ITEMS = [3, 7, 11, 15, 19, 23, 27, 31, 35, 40, 42, 55, 68, 72, 89]

    def test_the_chosen_target_actually_halves(self):
        """31 sits on the midpoint and is found on the first pass — a fine
        test case and a picture with no halving in it. 3 takes four."""
        def passes(target):
            low, high, count = 0, len(self.ITEMS) - 1, 0
            while low <= high:
                mid = (low + high) // 2
                count += 1
                if self.ITEMS[mid] == target:
                    return count
                if target < self.ITEMS[mid]:
                    high = mid - 1
                else:
                    low = mid + 1
            return count

        assert passes(31) == 1
        assert passes(3) == 4

    def test_marks_landing_on_one_cell_are_drawn_once(self):
        """By the last pass low, mid and high are the same index. Three
        labels at one position overlap into something unreadable."""
        svg = step_renderer.binary_search_steps(self.ITEMS, 3)
        assert ">low mid high<" in svg
        assert svg.count(">low<") == 3, "one per pass that has them apart"

    def test_the_list_comes_from_the_tutorial(self):
        items, target = cm._search_case()
        assert items == self.ITEMS
        assert items == sorted(items), "binary search needs it sorted"
        assert target in items


@needs_steps
class TestTheMergeWalk:
    A = [1, 3, 4, 5]
    B = [1, 2, 5, 7, 8]

    def test_the_sets_come_from_the_tutorial(self):
        left, right = maths_diagrams._sets_from_cell()
        assert left == self.A and right == self.B
        for values in (left, right):
            assert values == sorted(set(values)), "make_set sorts and dedupes"

    def test_every_comparison_case_appears(self):
        """Equal, less-than and greater-than each happen on this pair, so
        the picture shows all three rules the prose states rather than
        illustrating one and asserting the others.

        Unescaped first: `<` and `>` are `&lt;` and `&gt;` in the file, as
        they have to be.
        """
        import html as html_module

        svg = html_module.unescape(step_renderer.merge_walk(self.A, self.B))
        assert "1 = 1" in svg
        assert "3 > 2" in svg
        assert "3 < 5" in svg

    def test_the_union_it_reports_is_the_union(self):
        svg = step_renderer.merge_walk(self.A, self.B)
        expected = "  ".join(str(v) for v in sorted(set(self.A) | set(self.B)))
        assert f"union  {expected}" in svg

    def test_leftovers_are_named_from_the_list_that_still_has_them(self):
        svg = step_renderer.merge_walk(self.A, self.B)
        assert "left in b: 7  8" in svg
