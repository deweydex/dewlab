"""Fast unit tests for the parts of tutorial_tools that are pure logic.

tutorial_tools imports and runs under plain CPython, with a recording stub in
place of the DOM, which is what makes this possible without a browser. Anything
that genuinely needs Pyodide — running a cell, `load_csv`, widget event
handlers — is covered by the e2e test instead.

    python3 -m pytest dewlab/tests -q
"""

from __future__ import annotations

import sys
from contextlib import contextmanager
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "assets"))

import tutorial_tools as tt  # noqa: E402


@contextmanager
def streaming():
    """Redirect stdout/stderr into the running cell, inside the test body.

    pytest reinstates its own `sys.stdout` at the start of each test phase,
    which happens *after* fixture setup — so a fixture cannot leave the
    redirect in place for a test that exercises `print`. Tests that need it
    re-establish it here, which is the same two lines `_begin` runs.
    """
    saved = sys.stdout, sys.stderr
    sys.stdout = tt._StreamWriter("dl-stdout")
    sys.stderr = tt._StreamWriter("dl-error")
    try:
        yield
    finally:
        sys.stdout, sys.stderr = saved


@pytest.fixture()
def cell():
    """Put the module into the state a running cell would leave it in."""
    sink = tt._RecordingSink()
    tt._begin("test-cell", sink)
    try:
        yield sink
    finally:
        tt._end(None)
        tt.reset_page_state()


# ---------------------------------------------------------------- check()


class TestCompare:
    """`check`'s comparison rules, which are where its behaviour actually is."""

    @pytest.mark.parametrize(
        ("actual", "expected"),
        [
            (6, 6),
            ("hello", "hello"),
            ([1, 2, 3], [1, 2, 3]),
            ((1, 2), (1, 2)),
            ({"a": 1}, {"a": 1}),
            (0.1 + 0.2, 0.3),  # the classic float trap: must pass
            (1 / 3, 0.3333333333333333),
        ],
    )
    def test_equal_values_pass(self, actual, expected):
        passed, detail = tt._compare(actual, expected, None)
        assert passed, detail

    @pytest.mark.parametrize(
        ("actual", "expected"),
        [
            (4, 5),
            ("hello", "Hello"),
            ([1, 2, 3], [1, 2, 4]),
            ([1, 2], [1, 2, 3]),
            (0.5, 0.6),
        ],
    )
    def test_different_values_fail(self, actual, expected):
        passed, detail = tt._compare(actual, expected, None)
        assert not passed
        assert detail, "a failure must say something about why"

    def test_true_is_not_one(self):
        """`True == 1` in Python, but it is not the answer a student meant."""
        assert not tt._compare(True, 1, None)[0]
        assert not tt._compare(1, True, None)[0]
        assert tt._compare(True, True, None)[0]

    def test_explicit_tolerance(self):
        assert tt._compare(9.81, 9.8, 0.05)[0]
        assert not tt._compare(9.81, 9.8, 0.001)[0]

    def test_list_failure_names_the_position(self):
        passed, detail = tt._compare([1, 2, 3], [1, 5, 3], None)
        assert not passed
        assert "item 1" in detail

    def test_length_mismatch_is_reported_as_length(self):
        passed, detail = tt._compare([1, 2], [1, 2, 3], None)
        assert not passed
        assert "2 items" in detail and "3" in detail

    def test_uncomparable_types_fail_rather_than_raise(self):
        class Awkward:
            def __eq__(self, other):
                raise TypeError("no")

        passed, _ = tt._compare(Awkward(), 1, None)
        assert not passed

    def test_long_values_are_truncated_in_the_message(self):
        _, detail = tt._compare("x" * 500, "y", None)
        assert "..." in detail
        assert len(detail) < 300


class TestCheckRendering:
    def test_pass_renders_a_pass_indicator(self, cell):
        assert tt.check(6, 6) is True
        assert "dl-check-pass" in cell.html
        assert "✓" in cell.html

    def test_fail_renders_a_fail_indicator_with_a_reason(self, cell):
        assert tt.check(4, 5) is False
        assert "dl-check-fail" in cell.html
        assert "expected 5" in cell.html

    def test_custom_label_is_used(self, cell):
        tt.check(1, 1, label="Is the total right?")
        assert "Is the total right?" in cell.html

    def test_label_is_escaped(self, cell):
        tt.check(1, 2, label="<script>bad()</script>")
        assert "<script>bad()</script>" not in cell.html
        assert "&lt;script&gt;" in cell.html


# --------------------------------------------------------------- output


class TestStreamedOutput:
    def test_print_lands_in_the_output_area(self, cell):
        with streaming():
            print("hello")
        cell.close_stream()
        assert "dl-stdout" in cell.html
        assert "hello" in cell.html

    def test_consecutive_prints_share_one_block(self, cell):
        with streaming():
            print("one")
            print("two")
        cell.close_stream()
        assert cell.html.count("dl-stdout") == 1

    def test_a_widget_between_prints_breaks_the_block(self, cell):
        with streaming():
            print("before")
            tt.check(1, 1)
            print("after")
        cell.close_stream()
        assert cell.html.count("dl-stdout") == 2

    def test_printed_markup_is_escaped_not_rendered(self, cell):
        with streaming():
            print("<b>not bold</b>")
        cell.close_stream()
        assert "<b>not bold</b>" not in cell.html
        assert "&lt;b&gt;" in cell.html


class TestRenderValue:
    def test_none_renders_nothing(self, cell):
        tt._render_value(None)
        assert cell.html == ""

    def test_other_values_render_as_repr(self, cell):
        tt._render_value(1024)
        assert "1024" in cell.html
        assert "dl-repr" in cell.html

    def test_repr_is_escaped(self, cell):
        tt._render_value("<img src=x onerror=alert(1)>")
        assert "onerror=alert(1)>" not in cell.html
        assert "&lt;img" in cell.html

    def test_show_renders_each_value(self, cell):
        tt.show(1, "two", [3])
        assert cell.html.count("dl-repr") == 3

    def test_show_label_appears_first(self, cell):
        tt.show(1, label="A number")
        assert cell.html.index("A number") < cell.html.index("dl-repr")


class TestSuppressedReprs:
    """Two things a notebook prints that a beginner reads as noise."""

    def test_a_cell_ending_in_check_does_not_repeat_the_bool(self, cell):
        result = tt.check(2, 2)
        tt._render_value(result)
        assert "dl-check-pass" in cell.html
        assert "dl-repr" not in cell.html

    def test_a_bool_that_is_not_the_last_check_still_renders(self, cell):
        tt.check(2, 2)
        tt.show("something else")
        tt._render_value(True)
        assert "dl-repr" in cell.html

    def test_an_unrelated_bool_renders(self, cell):
        tt._render_value(False)
        assert "dl-repr" in cell.html


class TestOutsideACell:
    def test_output_functions_refuse_to_run_outside_a_cell(self):
        tt._current = None
        with pytest.raises(RuntimeError, match="running cell"):
            tt.show(1)
        with pytest.raises(RuntimeError, match="running cell"):
            tt.check(1, 1)


# --------------------------------------------------------------- tables

pd = pytest.importorskip("pandas")


@pytest.fixture()
def frame():
    return pd.DataFrame({"country": ["IE", "ES", "JP"], "value": [1, 2, 3]})


class TestTables:
    def test_dataframe_renders_as_a_table(self, cell, frame):
        tt._render_value(frame)
        assert "dl-table-wrap" in cell.html
        assert "<table" in cell.html
        assert "country" in cell.html

    def test_series_renders_as_a_table(self, cell, frame):
        tt._render_value(frame["value"])
        assert "<table" in cell.html

    def test_long_frames_are_truncated_and_say_so(self, cell):
        big = pd.DataFrame({"n": range(100)})
        tt.show_table(big, max_rows=5)
        assert "first 5 of 100 rows" in cell.html

    def test_short_frames_carry_no_truncation_note(self, cell, frame):
        tt.show_table(frame, max_rows=20)
        assert "dl-table-note" not in cell.html

    def test_caption_is_rendered_and_escaped(self, cell, frame):
        tt.show_table(frame, caption="<b>Cap</b>")
        assert "&lt;b&gt;Cap" in cell.html

    def test_cell_contents_are_escaped(self, cell):
        nasty = pd.DataFrame({"x": ["<script>alert(1)</script>"]})
        tt.show_table(nasty)
        assert "<script>alert(1)</script>" not in cell.html

    def test_dataframes_compare_elementwise_not_ambiguously(self, frame):
        assert tt._compare(frame, frame.copy(), None)[0]
        other = frame.copy()
        other.loc[0, "value"] = 99
        assert not tt._compare(frame, other, None)[0]

    def test_dataframe_against_a_non_frame_reports_the_type(self, frame):
        passed, detail = tt._compare(frame, [1, 2, 3], None)
        assert not passed
        assert "DataFrame" in detail


np = pytest.importorskip("numpy")


class TestArrays:
    def test_equal_arrays_pass(self):
        assert tt._compare(np.array([1, 2, 3]), np.array([1, 2, 3]), None)[0]

    def test_float_arrays_compare_within_tolerance(self):
        assert tt._compare(np.array([0.1 + 0.2]), np.array([0.3]), None)[0]

    def test_different_arrays_fail(self):
        assert not tt._compare(np.array([1, 2, 3]), np.array([1, 2, 4]), None)[0]

    def test_shape_mismatch_reports_shape(self):
        passed, detail = tt._compare(np.zeros((2, 2)), np.zeros((3, 3)), None)
        assert not passed
        assert "shape" in detail


# -------------------------------------------------------------- widgets


class TestWidgetIds:
    """Ids have to be stable across re-runs, or a re-run loses what was typed."""

    def test_label_derives_a_readable_id(self, cell):
        assert tt._widget_id(None, "Your name") == "your-name-1"

    def test_explicit_id_wins(self, cell):
        assert tt._widget_id("answer", "Your name") == "answer"

    def test_ids_are_unique_within_a_cell(self, cell):
        assert tt._widget_id(None, "Pick") != tt._widget_id(None, "Pick")

    def test_unlabelled_widgets_still_get_an_id(self, cell):
        assert tt._widget_id(None, "!!!") == "widget-1"


class TestWidgetMarkup:
    def test_text_input_renders_a_labelled_input(self, cell):
        tt.text_input("Your name")
        assert 'type="text"' in cell.html
        assert "Your name" in cell.html

    def test_text_input_restores_a_remembered_value(self, cell):
        tt._widget_values[("test-cell", "answer")] = "42"
        tt.text_input("Answer", id="answer")
        assert 'value="42"' in cell.html

    def test_dropdown_selects_the_first_option_by_default(self, cell):
        tt.dropdown("Units", ["metric", "imperial"])
        assert cell.html.count("<option") == 2
        assert '<option value="metric" selected>' in cell.html

    def test_dropdown_honours_an_explicit_value(self, cell):
        tt.dropdown("Units", ["metric", "imperial"], value="imperial")
        assert '<option value="imperial" selected>' in cell.html

    def test_widget_labels_and_options_are_escaped(self, cell):
        tt.dropdown('<b>x</b>', ['"><script>'])
        assert "<script>" not in cell.html
        assert "&lt;b&gt;" in cell.html

    def test_button_renders_a_button(self, cell):
        tt.button("Say hello")
        assert "Say hello" in cell.html
        assert "<button" in cell.html


# ------------------------------------------------------------ tracebacks


class TestTracebackTrimming:
    SOURCE = "def f():\n    return 1 + 'x'\nf()\n"

    def _raise_from_user_code(self, filename):
        tt._register_source(filename, self.SOURCE)
        exec(compile(self.SOURCE, filename, "exec"), {})  # noqa: S102 - the point

    def test_traceback_keeps_only_the_students_frames(self):
        filename = tt.cell_filename("demo")
        try:
            self._raise_from_user_code(filename)
        except TypeError as exc:
            text = tt._format_exception(exc)
        assert "TypeError" in text
        assert "test_tutorial_tools.py" not in text
        assert filename in text

    def test_traceback_shows_the_line_that_failed_not_just_its_number(self):
        """A line number with no line beside it is close to useless to a learner."""
        filename = tt.cell_filename("demo")
        try:
            self._raise_from_user_code(filename)
        except TypeError as exc:
            text = tt._format_exception(exc)
        assert "return 1 + 'x'" in text

    def test_each_cell_gets_its_own_filename(self):
        """Shared filenames would let one cell's linecache entry shadow another's."""
        assert tt.cell_filename("a") != tt.cell_filename("b")
        assert "a" in tt.cell_filename("a")

    def test_a_traceback_with_no_user_frames_is_still_shown(self):
        try:
            raise ValueError("straight from the test")
        except ValueError as exc:
            text = tt._format_exception(exc)
        assert "ValueError: straight from the test" in text
