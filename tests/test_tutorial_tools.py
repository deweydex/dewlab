"""Fast unit tests for the parts of tutorial_tools that are pure logic.

tutorial_tools imports and runs under plain CPython, with a recording stub in
place of the DOM, which is what makes this possible without a browser. Anything
that genuinely needs Pyodide — running a cell, `load_csv`, widget event
handlers — is covered by the e2e test instead.

    python3 -m pytest tests -q
"""

from __future__ import annotations

import sqlite3
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

# Imported at module level rather than through pytest.importorskip, which would
# skip this whole file — all 61 tests reported as one skip, which reads as a
# pass. tutorial_tools imports pandas lazily, so everything that does not touch
# a DataFrame still runs on a machine without it.
try:
    import pandas as pd
except ImportError:  # pragma: no cover - exercised only where pandas is absent
    pd = None

needs_pandas = pytest.mark.skipif(pd is None, reason="pandas is not installed")


@pytest.fixture()
def frame():
    return pd.DataFrame({"country": ["IE", "ES", "JP"], "value": [1, 2, 3]})


@needs_pandas
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


@needs_pandas
class TestRunQuery:
    """run_query — sqlite3 is stdlib so this runs under plain CPython
    same as everything else here; no Pyodide-only behaviour to defer to
    the e2e test."""

    @pytest.fixture()
    def seeded_db(self, tmp_path):
        db_path = tmp_path / "students.db"
        conn = sqlite3.connect(db_path)
        conn.execute("create table grades (name text, score integer)")
        conn.executemany(
            "insert into grades values (?, ?)",
            [("Ana", 92), ("Bo", 78), ("Cy", 85)],
        )
        conn.commit()
        conn.close()
        return db_path

    def test_select_renders_a_table_and_returns_a_frame(self, cell, seeded_db):
        result = tt.run_query(str(seeded_db), "select * from grades order by name")
        assert list(result["name"]) == ["Ana", "Bo", "Cy"]
        assert "<table" in cell.html
        assert "Ana" in cell.html

    def test_params_are_bound_not_interpolated(self, cell, seeded_db):
        result = tt.run_query(
            str(seeded_db), "select name from grades where score > ?", (80,)
        )
        assert set(result["name"]) == {"Ana", "Cy"}

    def test_a_statement_with_nothing_to_fetch_still_commits_and_renders_nothing(
        self, cell, seeded_db
    ):
        tt.run_query(str(seeded_db), "insert into grades values ('Dee', 60)")
        assert cell.html == ""
        conn = sqlite3.connect(seeded_db)
        assert conn.execute("select count(*) from grades").fetchone()[0] == 4
        conn.close()

    def test_an_open_connection_is_reused_not_closed(self, cell, seeded_db):
        conn = sqlite3.connect(seeded_db)
        try:
            tt.run_query(conn, "select 1")
            # Still usable — run_query only closes a connection it opened itself.
            assert conn.execute("select 2").fetchone() == (2,)
        finally:
            conn.close()

    def test_a_bad_query_raises_rather_than_rendering_anything(self, cell, seeded_db):
        with pytest.raises(sqlite3.OperationalError):
            tt.run_query(str(seeded_db), "select * from a_table_that_does_not_exist")
        assert cell.html == ""


@needs_pandas
class TestRunSqlCell:
    """_run_sql_cell() — the dewmini SQL cell type's own internal
    plumbing (planning/CELL_IDENTITY.md §8, DECISIONS_LOG.md 7.118),
    as opposed to run_query()'s public, one-statement API above."""

    @pytest.fixture()
    def conn(self):
        connection = sqlite3.connect(":memory:")
        yield connection
        connection.close()

    def test_a_script_of_several_statements_only_renders_the_last(self, cell, conn):
        result = tt._run_sql_cell(
            conn,
            "create table t (a, b); insert into t values (1, 2); select * from t",
        )
        assert list(result["a"]) == [1]
        assert "<table" in cell.html
        assert cell.html.count("<table") == 1

    def test_a_script_ending_in_a_non_select_reports_rows_affected(self, cell, conn):
        result = tt._run_sql_cell(conn, "create table t (a); insert into t values (1), (2)")
        assert result is None
        assert "2 rows affected" in cell.html
        assert conn.execute("select count(*) from t").fetchone()[0] == 2

    def test_state_persists_across_separate_calls_same_connection(self, cell, conn):
        tt._run_sql_cell(conn, "create table t (a)")
        tt._run_sql_cell(conn, "insert into t values (1)")
        result = tt._run_sql_cell(conn, "select * from t")
        assert list(result["a"]) == [1]

    def test_blank_and_trailing_semicolons_are_ignored(self, cell, conn):
        result = tt._run_sql_cell(conn, "create table t (a); ; insert into t values (1); ;")
        assert result is None
        assert "1 row affected" in cell.html

    def test_an_empty_script_does_nothing(self, cell, conn):
        assert tt._run_sql_cell(conn, "   ;  ;  ") is None
        assert cell.html == ""

    def test_a_bad_statement_raises_rather_than_rendering_anything(self, cell, conn):
        with pytest.raises(sqlite3.OperationalError):
            tt._run_sql_cell(conn, "select * from a_table_that_does_not_exist")
        assert cell.html == ""


try:
    import numpy as np
except ImportError:  # pragma: no cover - exercised only where numpy is absent
    np = None

needs_numpy = pytest.mark.skipif(np is None, reason="numpy is not installed")


@needs_numpy
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

    def _syntax_error(self, filename, source):
        tt._register_source(filename, source)
        try:
            compile(source, filename, "exec")
        except SyntaxError as exc:
            return tt._format_exception(exc)
        raise AssertionError("that source compiled, so there is nothing to format")

    def test_a_syntax_error_opens_with_the_students_own_line(self):
        """It is raised while the code is compiled, so none of the frames are
        the student's — they are all ours. Showing them put two lines of
        tutorial_tools.py above the line somebody had actually mistyped, in a
        tutorial whose subject is reading these messages."""
        filename = tt.cell_filename("demo")
        text = self._syntax_error(filename, "if hours > 10\n    print('long')\n")
        assert "tutorial_tools" not in text
        assert "Traceback (most recent call last)" not in text
        assert text.lstrip().startswith("File")

    def test_and_still_says_where_and_what(self):
        filename = tt.cell_filename("demo")
        text = self._syntax_error(filename, "if hours > 10\n    print('long')\n")
        assert filename in text
        assert "if hours > 10" in text
        assert "SyntaxError" in text

    def test_an_indentation_error_is_treated_the_same_way(self):
        filename = tt.cell_filename("demo")
        text = self._syntax_error(filename, "def check():\nprint('hello')\n")
        assert "tutorial_tools" not in text
        assert "IndentationError" in text

    def test_a_traceback_with_no_user_frames_is_still_shown(self):
        try:
            raise ValueError("straight from the test")
        except ValueError as exc:
            text = tt._format_exception(exc)
        assert "ValueError: straight from the test" in text


class TestPltShow:
    """`plt.show()` is in every textbook, so students write it. Under the
    non-interactive backend matplotlib's own show() draws nothing and warns.

    matplotlib is not installed for these tests — it does not need to be. The
    patch only ever looks for `matplotlib.pyplot` in `sys.modules`, so a stub
    module exercises the whole of it.
    """

    @contextmanager
    def fake_pyplot(self):
        import types

        module = types.ModuleType("matplotlib.pyplot")
        module.calls = []

        def show(*args, **kwargs):
            module.calls.append(("original", args, kwargs))

        module.show = show
        module.get_fignums = lambda: []
        module.close = lambda *a: module.calls.append(("close", a, {}))
        sys.modules["matplotlib.pyplot"] = module
        try:
            yield module
        finally:
            del sys.modules["matplotlib.pyplot"]

    def test_show_is_replaced_when_a_cell_starts(self, cell):
        with self.fake_pyplot() as plt:
            tt._begin("c", tt._RecordingSink())
            assert plt.show is not None
            assert getattr(plt.show, "_dewlab", False) is True

    def test_the_replacement_renders_instead_of_warning(self, cell):
        with self.fake_pyplot() as plt:
            tt._begin("c", tt._RecordingSink())
            plt.show()
            # The original would have recorded a call; ours flushes figures,
            # which on a stub with no open figures closes them and returns.
            assert ("original", (), {}) not in plt.calls
            assert ("close", ("all",), {}) in plt.calls

    def test_it_accepts_the_arguments_matplotlib_takes(self, cell):
        with self.fake_pyplot() as plt:
            tt._begin("c", tt._RecordingSink())
            plt.show(block=False)  # would be a TypeError if the signature were bare

    def test_patching_twice_keeps_the_first_replacement(self, cell):
        with self.fake_pyplot() as plt:
            tt._begin("c", tt._RecordingSink())
            first = plt.show
            tt._patch_pyplot_show()
            assert plt.show is first

    def test_nothing_happens_when_matplotlib_was_never_imported(self, cell):
        sys.modules.pop("matplotlib.pyplot", None)
        tt._patch_pyplot_show()  # must not raise


class TestDescribeGlobals:
    """describe_globals() — what dewmini's variable inspector reads.

    Worth unit-testing rather than leaving to the browser precisely because
    it *can* be: it takes a dict and returns plain data, so every branch is
    reachable under CPython, and the e2e test can then be about the panel
    rather than about the summaries.
    """

    @pytest.fixture(autouse=True)
    def clean_namespace(self):
        """Each test gets the shared namespace to itself."""
        tt._page_globals.clear()
        yield
        tt._page_globals.clear()

    def described(self):
        return {entry["name"]: entry for entry in tt.describe_globals()}

    def test_a_number_shows_its_value(self):
        tt._page_globals["answer"] = 42
        entry = self.described()["answer"]
        assert entry["type"] == "int"
        assert entry["summary"] == "42"
        assert entry["kind"] == "data"

    def test_containers_are_counted_rather_than_printed(self):
        """A thousand-item list should say "1000 items", not print itself."""
        tt._page_globals.update({
            "names": ["ada", "alan"],
            "empty": [],
            "one": [1],
            "lookup": {"a": 1, "b": 2},
        })
        described = self.described()
        assert described["names"]["summary"] == "2 items"
        assert described["empty"]["summary"] == "0 items"
        assert described["one"]["summary"] == "1 item"
        assert described["lookup"]["summary"] == "2 keys"

    def test_a_long_string_is_truncated(self):
        tt._page_globals["essay"] = "x" * 500
        summary = self.described()["essay"]["summary"]
        assert summary.endswith("…")
        assert len(summary) <= tt._SUMMARY_LIMIT

    def test_a_short_string_keeps_its_quotes(self):
        """Quoted, so a reader can tell the string "42" from the number 42."""
        tt._page_globals["greeting"] = "hello"
        assert self.described()["greeting"]["summary"] == "'hello'"

    def test_private_names_are_left_out(self):
        """The same convention autocomplete follows — these are bookkeeping,
        not anything a reader put there."""
        tt._page_globals.update({"_internal": 1, "visible": 2})
        assert "_internal" not in self.described()
        assert "visible" in self.described()

    def test_functions_and_modules_are_separated_from_data(self):
        """What the panel folds away, so a student's own variables stay at
        the top rather than being buried under the seeded names."""
        import math

        def helper():
            return None

        tt._page_globals.update({"math": math, "helper": helper, "mine": 1})
        described = self.described()
        assert described["math"]["kind"] == "module"
        assert described["helper"]["kind"] == "callable"
        assert described["mine"]["kind"] == "data"

    def test_a_class_counts_as_callable(self):
        tt._page_globals["Thing"] = type("Thing", (), {})
        assert self.described()["Thing"]["kind"] == "callable"

    def test_a_value_whose_repr_raises_does_not_break_the_panel(self):
        """A student's own broken __repr__ is a bug in their object, not a
        reason for every other variable to disappear."""
        class Hostile:
            def __repr__(self):
                raise RuntimeError("no")

        tt._page_globals.update({"hostile": Hostile(), "fine": 1})
        described = self.described()
        assert described["hostile"]["summary"] == "(cannot be displayed)"
        assert described["fine"]["summary"] == "1"

    def test_entries_come_back_sorted_by_name(self):
        tt._page_globals.update({"zebra": 1, "apple": 2, "Mango": 3})
        assert [e["name"] for e in tt.describe_globals()] == ["apple", "Mango", "zebra"]

    def test_everything_is_a_string(self):
        """The reason this returns plain data: it crosses a postMessage
        boundary, where a Pyodide proxy would not survive."""
        tt._page_globals.update({"n": 1, "text": "x", "items": [1, 2]})
        for entry in tt.describe_globals():
            assert set(entry) == {"name", "type", "summary", "kind"}
            assert all(isinstance(value, str) for value in entry.values())


@needs_pandas
class TestDescribeGlobalsWithPandas:
    """The shape summaries, which are the point of the inspector for anyone
    working with data: a DataFrame should say how big it is, not print
    itself into a sidebar."""

    @pytest.fixture(autouse=True)
    def clean_namespace(self):
        tt._page_globals.clear()
        yield
        tt._page_globals.clear()

    def test_a_dataframe_shows_its_shape(self):
        tt._page_globals["df"] = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
        entry = next(e for e in tt.describe_globals() if e["name"] == "df")
        assert entry["summary"] == "3 rows x 2 columns"

    def test_a_series_shows_its_length(self):
        tt._page_globals["column"] = pd.Series([1, 2, 3, 4])
        entry = next(e for e in tt.describe_globals() if e["name"] == "column")
        assert entry["summary"] == "4 values"

    def test_an_array_shows_its_dimensions(self):
        import numpy as np

        tt._page_globals["grid"] = np.zeros((2, 3))
        entry = next(e for e in tt.describe_globals() if e["name"] == "grid")
        assert entry["summary"] == "array(2, 3)"

    def test_shape_is_recognised_by_duck_typing_not_module_path(self):
        """The regression this guards: the first version keyed on
        `(__module__, __name__)` with `pandas.core.frame` hardcoded, which
        pandas 3 broke by reporting `__module__ == "pandas"` — a DataFrame
        then printed its whole self into the sidebar. Nothing here should
        depend on where a class says it lives."""
        class NotPandas:
            shape = (5, 2)
            columns = ["a", "b"]

        tt._page_globals["lookalike"] = NotPandas()
        entry = next(e for e in tt.describe_globals() if e["name"] == "lookalike")
        assert entry["summary"] == "5 rows x 2 columns"
