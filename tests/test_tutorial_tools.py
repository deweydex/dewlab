"""Covers the parts of tutorial_tools that are pure logic, using a recording
stub in place of the DOM; anything that genuinely needs Pyodide (running a
cell, `load_csv`, widget event handlers) is covered by the e2e test instead."""

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
    # pytest reinstates its own sys.stdout after fixture setup runs, so the
    # `cell` fixture can't leave this redirect in place; tests needing it
    # (the same two lines `_begin` runs) re-establish it here instead.
    saved = sys.stdout, sys.stderr
    sys.stdout = tt._StreamWriter("dl-stdout")
    sys.stderr = tt._StreamWriter("dl-error")
    try:
        yield
    finally:
        sys.stdout, sys.stderr = saved


@pytest.fixture()
def cell():
    sink = tt._RecordingSink()
    tt._begin("test-cell", sink)
    try:
        yield sink
    finally:
        tt._end(None)
        tt.reset_page_state()


class TestStreamedOutput:
    def test_print_lands_in_the_output_area_and_escapes_markup(self, cell):
        with streaming():
            print("hello")
        cell.close_stream()
        assert "dl-stdout" in cell.html
        assert "hello" in cell.html

        with streaming():
            print("<b>not bold</b>")
        cell.close_stream()
        assert "<b>not bold</b>" not in cell.html
        assert "&lt;b&gt;" in cell.html

    def test_consecutive_prints_share_one_block(self, cell):
        with streaming():
            print("one")
            print("two")
        cell.close_stream()
        assert cell.html.count("dl-stdout") == 1

    def test_a_widget_between_prints_breaks_the_block(self, cell):
        with streaming():
            print("before")
            tt.show("between")
            print("after")
        cell.close_stream()
        assert cell.html.count("dl-stdout") == 2


class TestRenderValue:
    def test_none_renders_nothing(self, cell):
        tt._render_value(None)
        assert cell.html == ""

    def test_values_render_as_escaped_repr(self, cell):
        tt._render_value(1024)
        assert "1024" in cell.html
        assert "dl-repr" in cell.html

        tt._render_value("<img src=x onerror=alert(1)>")
        assert "onerror=alert(1)>" not in cell.html
        assert "&lt;img" in cell.html

    def test_show_renders_each_value(self, cell):
        tt.show(1, "two", [3])
        assert cell.html.count("dl-repr") == 3

    def test_show_label_appears_first(self, cell):
        tt.show(1, label="A number")
        assert cell.html.index("A number") < cell.html.index("dl-repr")


class TestAnimations:
    def test_an_animation_renders_as_a_moving_png_and_its_figure_only_once(self, cell):
        matplotlib = pytest.importorskip("matplotlib")
        matplotlib.use("Agg")
        import base64
        import io
        import matplotlib.pyplot as plt
        from matplotlib.animation import FuncAnimation
        from PIL import Image

        figure, axes = plt.subplots(figsize=(1, 1))
        (dot,) = axes.plot([0], [0], "o")
        animation = FuncAnimation(
            figure, lambda step: dot.set_data([step], [step]), frames=3, interval=100
        )
        tt._render_value(animation)
        assert cell.html.count("data:image/png") == 1
        assert "Animation produced by this cell" in cell.html

        encoded = cell.html.split("base64,")[1].split('"')[0]
        image = Image.open(io.BytesIO(base64.b64decode(encoded)))
        assert image.is_animated and image.n_frames == 3

        # The figure the frames were drawn on is not rendered again as a
        # still when the cell's leftover figures are flushed.
        tt._flush_figures()
        assert cell.html.count("data:image/png") == 1


class TestSuppressedReprs:
    def test_a_bool_renders(self, cell):
        tt._render_value(False)
        assert "dl-repr" in cell.html


class TestOutsideACell:
    def test_output_functions_refuse_to_run_outside_a_cell(self):
        tt._current = None
        with pytest.raises(RuntimeError, match="running cell"):
            tt.show(1)
        with pytest.raises(RuntimeError, match="running cell"):
            tt.show_table([1])


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

    def test_dataframes_read_as_the_same_elementwise_not_ambiguously(self, frame):
        assert tt._same(frame, frame.copy())
        other = frame.copy()
        other.loc[0, "value"] = 99
        assert not tt._same(frame, other)
        assert not tt._same(frame, [1, 2, 3])


@needs_pandas
class TestRunQuery:
    # sqlite3 is stdlib, so run_query has no Pyodide-only behaviour to defer
    # to the e2e test — it runs under plain CPython like everything else here.

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
    plumbing, as opposed to run_query()'s public, one-statement API
    above."""

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

    def test_the_result_table_leaves_out_pandas_row_numbers(self, cell, conn):
        # The ids here skip 5, as a table does after a DELETE: pandas' own
        # 0-4 beside them would read as a second id column.
        result = tt._run_sql_cell(
            conn,
            "create table t (t_id); insert into t values (1), (2), (3), (4), (6); "
            "select * from t",
        )
        sql_table = cell.html
        assert "<th></th>" not in sql_table
        assert "<th>0</th>" not in sql_table
        assert sql_table.count("<td>") == 5
        # The same frame shown from a Python cell keeps its index.
        tt._render_value(result)
        python_table = cell.html[len(sql_table):]
        assert "<th>0</th>" in python_table

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

    @pytest.mark.parametrize(
        "script, expected_empty",
        [
            pytest.param(
                "create table t (a); insert into t values (1); "
                "select * from t where a = 2",
                True,
                id="rows_selected_but_none_match",
            ),
            pytest.param(
                "create table t (a); insert into t values (1); select * from t",
                False,
                id="rows_match",
            ),
            pytest.param(
                "create table t (a); insert into t values (1)",
                None,
                id="non_select_last_statement",
            ),
        ],
    )
    def test_last_result_empty(self, cell, conn, script, expected_empty):
        tt._run_sql_cell(conn, script)
        assert tt._current.last_result_empty is expected_empty

    @pytest.mark.parametrize(
        "setup_sql, query, expected_match, forbidden_text",
        [
            pytest.param(
                "create table products (a)", "select * from prodcuts",
                "did you mean 'products'", None,
                id="table_typo",
            ),
            pytest.param(
                "create table products (price)", "select pricee from products",
                "did you mean 'price'", None,
                id="column_typo",
            ),
            pytest.param(
                "create table products (a)", "select * from zzz",
                None, "did you mean",
                id="no_close_match",
            ),
            pytest.param(
                "create table t (a)", "select a from t where count(*) > 1",
                "HAVING instead", None,
                id="aggregate_in_where",
            ),
            pytest.param(
                "create table t (a)", "select a from t group by a where a > 1",
                "have to come in this order", None,
                id="clause_order",
            ),
        ],
    )
    def test_raises_with_a_specific_hint(
        self, cell, conn, setup_sql, query, expected_match, forbidden_text
    ):
        conn.execute(setup_sql)
        if expected_match is not None:
            with pytest.raises(sqlite3.OperationalError, match=expected_match):
                tt._run_sql_cell(conn, query)
        else:
            with pytest.raises(sqlite3.OperationalError) as excinfo:
                tt._run_sql_cell(conn, query)
            assert forbidden_text not in str(excinfo.value)

    @pytest.mark.parametrize(
        "setup_statements, query, expected, forbidden",
        [
            pytest.param(
                ["create table t (a)"],
                "select * from t",
                ["t has no rows in it yet"],
                [],
                id="empty_table",
            ),
            pytest.param(
                ["create table t (a)", "insert into t values (1)"],
                "select * from t where a = 2",
                ["t has 1 row(s) in it"],
                ["Ignoring uppercase"],
                id="filtered_empty",
            ),
            pytest.param(
                ["create table t (category)", "insert into t values ('Octopus')"],
                "select * from t where category = 'octopus'",
                ["t has 1 row(s) in it",
                 "Ignoring uppercase and lowercase, 1 row would have matched"],
                [],
                id="case_mismatch_hint",
            ),
            pytest.param(
                ["create table t (a)", "insert into t values (1)"],
                "select * from t",
                [],
                ["row(s) in it", "Ignoring uppercase"],
                id="non_empty_no_notes",
            ),
        ],
    )
    def test_empty_result_notes(self, cell, conn, setup_statements, query, expected, forbidden):
        for statement in setup_statements:
            conn.execute(statement)
        tt._run_sql_cell(conn, query)
        for substring in expected:
            assert substring in cell.html
        for substring in forbidden:
            assert substring not in cell.html


class TestQueryRows:
    """_query_rows() — the Python half of a full-stack cell's bridge to the
    page's shared `db` connection. Unlike _run_sql_cell(), this is called
    from an app cell's own JavaScript outside the normal cell-run
    lifecycle, so every test here runs with no `cell` fixture — a running
    cell is exactly what it must not require."""

    @pytest.fixture(autouse=True)
    def _no_stale_db(self):
        tt._page_globals.pop("db", None)
        try:
            yield
        finally:
            conn = tt._page_globals.pop("db", None)
            if conn is not None:
                conn.close()

    def test_no_connection_yet_raises(self):
        with pytest.raises(RuntimeError, match="nothing for a query to run against"):
            tt._query_rows("select 1")

    def test_a_query_returns_rows_as_plain_dicts(self):
        conn = sqlite3.connect(":memory:")
        conn.execute("create table t (a, b)")
        conn.execute("insert into t values (1, 'x'), (2, 'y')")
        tt._page_globals["db"] = conn
        assert tt._query_rows("select * from t order by a") == [
            {"a": 1, "b": "x"},
            {"a": 2, "b": "y"},
        ]

    def test_params_bind_rather_than_interpolate(self):
        conn = sqlite3.connect(":memory:")
        conn.execute("create table t (name)")
        conn.execute("insert into t values ('Ada'), ('Grace')")
        tt._page_globals["db"] = conn
        assert tt._query_rows("select name from t where name = ?", ["Ada"]) == [{"name": "Ada"}]

    def test_no_active_cell_is_not_required(self):
        tt._current = None
        conn = sqlite3.connect(":memory:")
        tt._page_globals["db"] = conn
        assert tt._query_rows("select 1 as n") == [{"n": 1}]

    def test_a_bad_query_raises_the_sqlite_error(self):
        conn = sqlite3.connect(":memory:")
        tt._page_globals["db"] = conn
        with pytest.raises(sqlite3.OperationalError):
            tt._query_rows("select * from a_table_that_does_not_exist")


try:
    import numpy as np
except ImportError:  # pragma: no cover - exercised only where numpy is absent
    np = None

needs_numpy = pytest.mark.skipif(np is None, reason="numpy is not installed")


@needs_numpy
class TestArrays:
    @pytest.mark.parametrize(
        "kind, should_pass",
        [
            pytest.param("equal", True, id="equal_arrays_pass"),
            pytest.param("float_tolerance", True, id="float_arrays_compare_within_tolerance"),
            pytest.param("different", False, id="different_arrays_fail"),
        ],
    )
    def test_array_comparisons(self, kind, should_pass):
        if kind == "equal":
            actual, expected = np.array([1, 2, 3]), np.array([1, 2, 3])
        elif kind == "float_tolerance":
            actual, expected = np.array([0.1 + 0.2]), np.array([0.3])
        else:
            actual, expected = np.array([1, 2, 3]), np.array([1, 2, 4])
        assert tt._same(actual, expected) is should_pass

    def test_a_different_shape_is_different(self):
        assert not tt._same(np.zeros((2, 2)), np.zeros((3, 3)))


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


class TestTracebackTrimming:
    SOURCE = "def f():\n    return 1 + 'x'\nf()\n"

    def _raise_from_user_code(self, filename):
        tt._register_source(filename, self.SOURCE)
        exec(compile(self.SOURCE, filename, "exec"), {})  # noqa: S102 - the point

    def test_traceback_keeps_only_the_students_frames_and_shows_the_failing_line(self):
        filename = tt.cell_filename("demo")
        try:
            self._raise_from_user_code(filename)
        except TypeError as exc:
            text = tt._format_exception(exc)
        assert "TypeError" in text
        assert "test_tutorial_tools.py" not in text
        assert filename in text
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

    SYNTAX_SOURCE = "if hours > 10\n    print('long')\n"
    INDENTATION_SOURCE = "def check():\nprint('hello')\n"

    @pytest.mark.parametrize(
        "source, expected, forbidden, starts_with_file, checks_filename",
        [
            pytest.param(
                SYNTAX_SOURCE, [], ["tutorial_tools", "Traceback (most recent call last)"],
                True, False,
                id="syntax_error_opens_with_the_students_own_line",
                # A syntax error has no frames of the student's — it's raised
                # while compiling, before any of their code runs — so the
                # frames are all ours.
            ),
            pytest.param(
                SYNTAX_SOURCE, ["if hours > 10", "SyntaxError"], [],
                False, True,
                id="and_still_says_where_and_what",
            ),
            pytest.param(
                INDENTATION_SOURCE, ["IndentationError"], ["tutorial_tools"],
                False, False,
                id="an_indentation_error_is_treated_the_same_way",
            ),
        ],
    )
    def test_syntax_and_indentation_errors(
        self, source, expected, forbidden, starts_with_file, checks_filename
    ):
        filename = tt.cell_filename("demo")
        text = self._syntax_error(filename, source)
        if starts_with_file:
            assert text.lstrip().startswith("File")
        if checks_filename:
            assert filename in text
        for substring in expected:
            assert substring in text
        for substring in forbidden:
            assert substring not in text

    def test_a_traceback_with_no_user_frames_is_still_shown(self):
        try:
            raise ValueError("straight from the test")
        except ValueError as exc:
            text = tt._format_exception(exc)
        assert "ValueError: straight from the test" in text


class TestPltShow:
    # matplotlib is not installed for these tests — it doesn't need to be,
    # since the patch only ever looks for "matplotlib.pyplot" in sys.modules,
    # so a stub module exercises the whole of it.

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

    def test_show_is_replaced_and_the_replacement_renders_instead_of_warning(self, cell):
        with self.fake_pyplot() as plt:
            tt._begin("c", tt._RecordingSink())
            assert plt.show is not None
            assert getattr(plt.show, "_dewlab", False) is True

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
    # describe_globals() takes a dict and returns plain data, so every branch
    # is reachable under CPython — worth unit-testing here rather than
    # leaving the summaries themselves to the e2e test.

    @pytest.fixture(autouse=True)
    def clean_namespace(self):
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
        # Quoted, so a reader can tell the string "42" from the number 42.
        tt._page_globals["greeting"] = "hello"
        assert self.described()["greeting"]["summary"] == "'hello'"

    def test_private_names_are_left_out(self):
        # The same convention autocomplete follows: bookkeeping, not a reader's own.
        tt._page_globals.update({"_internal": 1, "visible": 2})
        assert "_internal" not in self.described()
        assert "visible" in self.described()

    def test_functions_modules_and_classes_are_separated_from_data(self):
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

        tt._page_globals["Thing"] = type("Thing", (), {})
        assert self.described()["Thing"]["kind"] == "callable"

    def test_builtin_flag_tracks_the_seeded_toolbox_by_name(self):
        """RESEED_GLOBALS_SOURCE (tutorial-runtime.js) does exactly this
        update at boot and after every restart — simulated here rather
        than imported, since that source string lives in JS."""
        tt._page_globals.update({name: getattr(tt, name) for name in tt.__all__})
        tt._page_globals["mine"] = 1
        described = self.described()
        assert all(described[name]["builtin"] for name in tt.__all__)
        assert described["mine"]["builtin"] is False

        # Shadowing a tool name is still the reader's own doing — it
        # should show up as theirs, not stay tagged as the toolbox.
        tt._page_globals["show"] = lambda: None
        assert self.described()["show"]["builtin"] is False

        # A fresh sqlite3.Connection every boot (SEED_SQL_DB_SOURCE) means
        # there's no fixed object to compare against the way __all__'s
        # names can be — it's still exactly as pre-seeded, just by name.
        tt._page_globals["db"] = object()
        assert self.described()["db"]["builtin"] is True

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

    def test_everything_is_a_string_or_a_plain_bool(self):
        """The reason most of this returns plain strings: it crosses a
        postMessage boundary, where a Pyodide proxy would not survive.
        `builtin` is the one exception — a plain bool crosses that
        boundary just as cleanly, with no proxy to destroy() either
        side."""
        tt._page_globals.update({"n": 1, "text": "x", "items": [1, 2]})
        for entry in tt.describe_globals():
            assert set(entry) == {"name", "type", "summary", "kind", "builtin"}
            assert isinstance(entry["builtin"], bool)
            assert all(
                isinstance(value, str) for key, value in entry.items() if key != "builtin"
            )


@needs_pandas
class TestDescribeGlobalsWithPandas:
    """A DataFrame should say how big it is in the inspector, not print
    itself into a sidebar."""

    @pytest.fixture(autouse=True)
    def clean_namespace(self):
        tt._page_globals.clear()
        yield
        tt._page_globals.clear()

    @pytest.mark.parametrize(
        "name, kind, expected_summary",
        [
            pytest.param("df", "dataframe", "3 rows x 2 columns", id="dataframe_shows_its_shape"),
            pytest.param("column", "series", "4 values", id="series_shows_its_length"),
            pytest.param("grid", "array", "array(2, 3)", id="array_shows_its_dimensions"),
        ],
    )
    def test_shape_summaries(self, name, kind, expected_summary):
        if kind == "dataframe":
            value = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
        elif kind == "series":
            value = pd.Series([1, 2, 3, 4])
        else:
            import numpy as np

            value = np.zeros((2, 3))
        tt._page_globals[name] = value
        entry = next(e for e in tt.describe_globals() if e["name"] == name)
        assert entry["summary"] == expected_summary

    def test_shape_is_recognised_by_duck_typing_not_module_path(self):
        # Regression guard: the first version hardcoded `pandas.core.frame`
        # against __module__, which pandas 3 broke by reporting __module__
        # == "pandas", so a DataFrame fell through and printed its whole self.
        class NotPandas:
            shape = (5, 2)
            columns = ["a", "b"]

        tt._page_globals["lookalike"] = NotPandas()
        entry = next(e for e in tt.describe_globals() if e["name"] == "lookalike")
        assert entry["summary"] == "5 rows x 2 columns"


class TestRunReport:
    """What `run_cell_report()` tells the page about one run — the plain
    values `tutorial-runtime.js` counts attempts from."""

    def test_a_clean_run_with_no_expect(self, cell):
        report = tt._report(True, tt._current, None)
        assert report == {"ok": True, "error": None, "empty": None, "reached": None}

    def test_an_error_is_its_type_and_first_line(self, cell):
        try:
            raise ValueError("first line\nsecond line")
        except ValueError as exc:
            tt._current.last_error = tt._describe_error(exc)
        report = tt._report(False, tt._current, None)
        assert report["ok"] is False
        assert report["error"] == {"type": "ValueError", "message": "first line"}

    def test_expect_is_evaluated_in_the_page_namespace(self, cell):
        tt._page_globals["total"] = 6
        assert tt.holds("total == 6") is True
        assert tt.holds("total == 7") is False
        assert tt._report(True, tt._current, "total == 6")["reached"] is True

    def test_a_sql_cells_empty_result_is_reported_and_holds_treats_errors_as_false(self, cell):
        tt._current.last_result_empty = True
        assert tt._report(True, tt._current, None)["empty"] is True
        # holds() must treat any runtime or syntax error as simply "not
        # true", never let it escape as a crash.
        assert tt.holds("undefined_name == 1") is False
        assert tt.holds("1 / 0") is False
        assert tt.holds("this is not python") is False

class TestWidgetsOnAWorkerPage:
    """The hosted site runs Python in a Worker, where nothing can watch a
    control. `text_input` and `dropdown` still work there: the page watches
    the control and posts the value back between runs."""

    @pytest.fixture()
    def worker_cell(self):
        posted = []
        sink = tt._MessageSink(lambda *args: posted.append(args))
        tt._begin("test-cell", sink)
        try:
            yield posted
        finally:
            tt._end(None)
            tt.reset_page_state()

    def test_text_input_renders_rather_than_raising(self, worker_cell):
        tt.text_input("Your name", id="name")
        markup = "".join(args[3] or "" for args in worker_cell)
        assert 'id="dl-w-test-cell-name"' in markup

    def test_dropdown_renders_rather_than_raising(self, worker_cell):
        tt.dropdown("Units", ["metric", "imperial"], id="units")
        markup = "".join(args[3] or "" for args in worker_cell)
        assert "<select" in markup and "metric" in markup

    def test_value_is_what_was_rendered_before_anyone_types(self, worker_cell):
        widget = tt.text_input("Answer", value="42", id="answer")
        assert widget.value == "42"

    def test_a_dropdown_defaults_to_its_first_option(self, worker_cell):
        widget = tt.dropdown("Units", ["metric", "imperial"], id="units")
        assert widget.value == "metric"

    def test_the_page_reporting_a_change_is_what_value_reads(self, worker_cell):
        widget = tt.text_input("Answer", value="42", id="answer")
        tt._set_widget_value("test-cell", "answer", "7")
        assert widget.value == "7"

    def test_button_and_image_input_still_say_why_they_cannot(self, worker_cell):
        with pytest.raises(RuntimeError, match="main thread"):
            tt.button("Go")
        with pytest.raises(RuntimeError, match="main thread"):
            tt.image_input()


class TestAppCellQueriesCommit:
    def test_a_write_from_an_app_cell_survives_a_rollback(self):
        conn = sqlite3.connect(":memory:")
        conn.execute("CREATE TABLE plushies (name TEXT)")
        conn.commit()
        tt._page_globals["db"] = conn
        try:
            assert tt._query_rows("INSERT INTO plushies (name) VALUES (?)", ["Mug"]) == []
            conn.rollback()
            assert tt._query_rows("SELECT name FROM plushies") == [{"name": "Mug"}]
        finally:
            tt._page_globals.pop("db", None)


class TestLoadToolkit:
    """`_load_toolkit()`: earlier pages' toolkit cells, each run in a
    namespace of its own and exported to the shared one before a page's
    first cell. The reader's version where there
    is one, the reference where there is not or where theirs raises, and
    nothing either prints reaches any cell."""

    @pytest.fixture(autouse=True)
    def seeded(self):
        tt._page_globals.update({name: getattr(tt, name) for name in tt.__all__})
        tt._page_globals["__name__"] = "__dewlab__"
        yield
        tt.reset_page_state()

    def load(self, *entries):
        import json
        return json.loads(tt._load_toolkit(json.dumps(list(entries))))

    def test_the_readers_version_runs_when_there_is_one(self):
        result = self.load(
            {"tutorial": "one", "cell": "c", "reference": "def double(n):\n    return n * 2",
             "mine": "def double(n):\n    return n + n + 0"})
        assert result["entries"][0]["used"] == "mine"
        assert result["names"] == ["double"]
        assert tt._page_globals["double"](4) == 8

    def test_a_version_that_raises_is_undone_and_the_reference_runs(self):
        result = self.load(
            {"tutorial": "one", "cell": "c", "reference": "def double(n):\n    return n * 2",
             "mine": "def double(n):\n    return 0\nleftover = 1\nraise ValueError('mine')"})
        entry = result["entries"][0]
        assert entry["used"] == "reference" and entry["fell_back"]
        assert tt._page_globals["double"](4) == 8
        assert "leftover" not in tt._page_globals

    def test_names_are_what_the_toolkit_made_in_order_and_not_what_it_imported(self, capsys):
        result = self.load(
            {"tutorial": "one", "cell": "a", "reference": "def to_binary(n):\n    return bin(n)[2:]",
             "mine": None},
            {"tutorial": "two", "cell": "b", "mine": None,
             "reference": "from math import sqrt\nprint('loading')\nclass Point:\n    pass\n"
                          "def split_evenly(total, parts):\n    return total / parts\nrate = 0.1"})
        assert result["names"] == ["to_binary", "Point", "split_evenly"]
        assert result["entries"][1]["names"] == ["Point", "split_evenly"]
        assert "loading" not in capsys.readouterr().out
        assert tt._current is None

    def test_an_entrys_imports_stay_inside_it(self):
        # Untangling a condition imports itertools.product; Doing it again
        # later defines a toolkit product() of its own. Each keeps its own.
        self.load(
            {"tutorial": "one", "cell": "a", "mine": None,
             "reference": "from itertools import product\n"
                          "def rows(count):\n    return len(list(product([0, 1], repeat=count)))"},
            {"tutorial": "two", "cell": "b", "mine": None,
             "reference": "def product(values):\n    result = 1\n"
                          "    for value in values:\n        result *= value\n    return result"})
        assert tt._page_globals["rows"](3) == 8
        assert tt._page_globals["product"]([2, 3]) == 6

    def test_a_page_that_reuses_a_name_does_not_break_the_toolkit(self):
        self.load({"tutorial": "one", "cell": "a", "mine": None,
                   "reference": "RATE = 10\ndef margin(total):\n    return total * RATE / 100"})
        assert tt._page_globals["RATE"] == 10
        tt._page_globals["RATE"] = "a page's own RATE"
        assert tt._page_globals["margin"](50) == 5

    def test_a_later_entry_sees_the_earlier_ones(self):
        self.load(
            {"tutorial": "one", "cell": "a", "mine": None,
             "reference": "def factorial(n):\n    return 1 if n < 2 else n * factorial(n - 1)"},
            {"tutorial": "one", "cell": "b", "mine": None,
             "reference": "def permutations(n, r):\n    return factorial(n) // factorial(n - r)"})
        assert tt._page_globals["permutations"](5, 2) == 20

    def test_a_reference_that_raises_is_reported(self):
        result = self.load({"tutorial": "one", "cell": "c", "reference": "1 / 0", "mine": None})
        assert result["entries"][0]["error"] == ["ZeroDivisionError", "division by zero"]

    REFERENCE = (
        "RATE = 10\n"
        "def split_evenly(total, parts):\n    return total / parts\n"
        "def margin(total):\n    return total * RATE / 100\n"
        "def hello():\n    return 'hi'\n"
    )

    @pytest.mark.parametrize("stub_body", [
        '"""Split a total evenly."""\n    ...',
        "pass",
        "raise NotImplementedError",
        '"""Not yet."""\n    raise NotImplementedError("write me")',
    ])
    def test_an_untouched_stub_takes_the_reference_function(self, stub_body):
        mine = f"def split_evenly(total, parts):\n    {stub_body}\n"
        result = self.load({"tutorial": "one", "cell": "c", "reference": self.REFERENCE,
                            "mine": mine})
        entry = result["entries"][0]
        assert entry["used"] == "mine" and not entry["fell_back"]
        assert tt._page_globals["split_evenly"](10, 4) == 2.5
        # margin and hello are not in the reader's code at all.
        assert entry["from_reference"] == [
            {"name": "split_evenly", "why": "unwritten"},
            {"name": "margin", "why": "unwritten"},
            {"name": "hello", "why": "unwritten"}]
        # A reference function calls the reference's own helpers.
        assert tt._page_globals["margin"](50) == 5

    def test_per_function_the_readers_written_ones_stay_theirs(self):
        mine = ("def split_evenly(total, parts):\n    return 'mine'\n"
                "def margin(total):\n    ...\n"
                "hello = lambda: 'mine too'\n")
        result = self.load({"tutorial": "one", "cell": "c", "reference": self.REFERENCE,
                            "mine": mine})
        assert tt._page_globals["split_evenly"](1, 1) == "mine"
        assert tt._page_globals["hello"]() == "mine too"
        assert tt._page_globals["margin"](50) == 5
        assert result["entries"][0]["from_reference"] == [{"name": "margin", "why": "unwritten"}]
        assert result["names"] == ["split_evenly", "margin", "hello"]

    def test_a_version_that_raises_names_every_reference_function(self):
        result = self.load({"tutorial": "one", "cell": "c", "reference": self.REFERENCE,
                            "mine": "def split_evenly(total, parts):\n    return 0\n1 / 0"})
        assert [(f["name"], f["why"]) for f in result["entries"][0]["from_reference"]] == [
            ("split_evenly", "raised"), ("margin", "raised"), ("hello", "raised")]

    def test_nothing_saved_counts_as_unwritten_and_the_reference_mode_says_nothing(self):
        unsaved = self.load({"tutorial": "one", "cell": "c", "reference": self.REFERENCE,
                             "mine": None, "unsaved": True})
        assert [f["why"] for f in unsaved["entries"][0]["from_reference"]] == ["unwritten"] * 3
        chosen = self.load({"tutorial": "one", "cell": "c", "reference": self.REFERENCE,
                            "mine": None})
        assert chosen["entries"][0]["from_reference"] == []


class TestCompareWithASolution:
    """tutorial_tools.compare() (#312): the reader's code and a solution,
    case by case, in copies of the page namespace. Never a verdict."""

    @pytest.fixture(autouse=True)
    def page(self):
        tt._page_globals.clear()
        exec(
            "def total_of(values):\n"
            "    total = 0\n"
            "    for value in values[:-1]:\n"
            "        total = total + value\n"
            "    return total\n"
            "widths = [4879, 12104]\n",
            tt._page_globals,
        )
        yield
        tt._page_globals.clear()

    def run(self, solution, cases, tests=None):
        import asyncio
        import json

        inputs = json.dumps([{"expr": expr, "label": None} for expr in cases])
        return json.loads(asyncio.run(tt.compare(solution, inputs, tests)))

    SOLUTION = "def total_of(values):\n    return sum(values)\n"

    def test_each_case_has_both_sides_and_says_whether_they_differ(self):
        rows = self.run(self.SOLUTION, ["total_of([1, 2, 3])", "total_of([])"])["rows"]
        assert rows[0]["yours"] == {"shown": "3"}
        assert rows[0]["solution"] == {"shown": "6"}
        assert rows[0]["differ"] is True
        assert rows[1]["differ"] is False

    def test_asking_changes_nothing_in_the_page(self):
        self.run(self.SOLUTION + "widths.append(1)\n", ["widths"])
        assert tt._page_globals["total_of"]([1, 2, 3]) == 3
        assert tt._page_globals["widths"] == [4879, 12104]

    def test_the_solution_sees_the_readers_data(self):
        rows = self.run("total = sum(widths)\n", ["total"])["rows"]
        assert rows[0]["solution"] == {"shown": "16983"}
        assert rows[0]["yours"]["error"].startswith("NameError")

    def test_an_error_is_an_outcome_on_either_side(self):
        rows = self.run(self.SOLUTION, ["total_of(None)", "1 / 0"])["rows"]
        assert rows[0]["yours"]["error"].startswith("TypeError")
        assert rows[1]["yours"] == rows[1]["solution"] == {"error": "ZeroDivisionError: division by zero"}
        assert rows[1]["differ"] is False

    def test_close_floats_read_as_the_same_and_true_is_not_one(self):
        assert tt._same(0.1 + 0.2, 0.3)
        assert not tt._same(True, 1)
        assert tt._same([1.0, (2, 3)], [1, (2, 3)])
        assert not tt._same([1, 2], (1, 2))

    def test_two_classes_with_the_same_state_read_as_the_same(self):
        class Account:
            def __init__(self, balance):
                self.balance = balance
        first = Account(5)

        class Account:  # noqa: F811 - a second definition, as a solution makes
            def __init__(self, balance):
                self.balance = balance
        assert tt._same(first, Account(5))
        assert not tt._same(first, Account(6))

    def test_a_solution_that_raises_is_reported_and_its_column_left_empty(self):
        result = self.run("raise ValueError('nope')\n", ["total_of([1])"])
        assert result["solutionError"] == "ValueError: nope"
        assert "solution" not in result["rows"][0]

    def test_with_no_solution_only_the_readers_side_is_filled(self):
        row = self.run(None, ["total_of([1, 2])"])["rows"][0]
        assert row == {"input": "total_of([1, 2])", "label": None, "yours": {"shown": "1"}}

    def test_the_readers_tests_run_on_both_sides_statement_by_statement(self):
        tests = "assert total_of([2, 2]) == 4\nx = total_of([7])\nx\n"
        rows = self.run(self.SOLUTION, [], tests)["tests"]
        assert [r["input"] for r in rows] == ["assert total_of([2, 2]) == 4", "x = total_of([7])", "x"]
        assert rows[0]["yours"] == {"error": "AssertionError"}
        assert rows[0]["solution"] == {"shown": "no error"}
        assert rows[2]["yours"] == {"shown": "0"}
        assert rows[2]["solution"] == {"shown": "7"}

    def test_printing_goes_nowhere_and_a_long_value_is_cut(self, capsys):
        rows = self.run("print('from the solution')\n", ["list(range(1000))"])["rows"]
        assert "from the solution" not in capsys.readouterr().out
        assert rows[0]["yours"]["shown"].endswith("(cut short)")


class TestDatasets:
    """A dataset in `data/` comes live when it has a source a page may read,
    and from its snapshot when it has not or the source does not answer
    (#324). The fetches are browser-only, so they are replaced here; what
    is tested is the order, the shaping, and the note under the cell."""

    INDEX = {
        "life.csv": {
            "snapshot": "2026-09-26",
            "live": {"source": "Our World in Data", "url": "https://example.org/life.csv",
                     "rename": {"entity": "country"}, "columns": ["country", "year"]},
        },
        "book.txt": {"snapshot": "2026-09-20"},
        "income.csv": {
            "snapshot": "2026-09-26", "address": True,
            "live": {"source": "Our World in Data", "url": "https://example.org/income.csv",
                     "columns": ["a"]},
        },
    }

    @pytest.fixture()
    def world(self, monkeypatch):
        """A page whose index is INDEX, whose snapshots are `saved`, and
        whose web is `online`: a URL there answers, and any other raises."""
        state = {"online": {}, "saved": {
            "life.csv": b"country,year\nIreland,1950\n",
            "book.txt": b"It was a dark night.\n",
            "income.csv": b"a\n1\n",
        }}

        async def fetch(url):
            if url not in state["online"]:
                raise ConnectionError(url)
            return state["online"][url]

        async def snapshot(name):
            return state["saved"][name]

        monkeypatch.setattr(tt, "_data_index", dict(self.INDEX))
        monkeypatch.setattr(tt, "_fetch_bytes", fetch)
        monkeypatch.setattr(tt, "_snapshot_bytes", snapshot)
        return state

    @staticmethod
    def run(coroutine):
        import asyncio
        return asyncio.run(coroutine)

    def test_a_live_source_is_shaped_into_the_snapshots_columns(self, world, cell):
        world["online"]["https://example.org/life.csv"] = (
            b"entity,code,year\nIreland,IRL,1950\nIreland,IRL,1951\n")
        frame = self.run(tt.load_csv("life.csv"))
        assert list(frame.columns) == ["country", "year"]
        assert len(frame) == 2
        assert "from Our World in Data just now" in cell.html
        assert "copy saved on 26 September 2026" in cell.html

    def test_a_source_that_does_not_answer_gives_the_snapshot_and_says_so(self, world, cell):
        frame = self.run(tt.load_csv("life.csv"))
        assert frame.to_dict("records") == [{"country": "Ireland", "year": 1950}]
        assert "The live copy from Our World in Data could not be used" in cell.html

    def test_a_live_copy_the_recipe_no_longer_fits_gives_the_snapshot(self, world, cell):
        world["online"]["https://example.org/life.csv"] = b"place,when\nIreland,1950\n"
        frame = self.run(tt.load_csv("life.csv"))
        assert list(frame.columns) == ["country", "year"]
        assert "could not be used just now" in cell.html

    def test_a_dataset_with_no_live_source_names_its_date(self, world, cell):
        assert self.run(tt.load_text("book.txt")) == "It was a dark night.\n"
        assert "Loaded the copy of book.txt saved on 20 September 2026." in cell.html

    def test_an_address_data_keeps_a_copy_of_falls_back_to_it(self, world, cell):
        frame = self.run(tt.load_csv("https://example.org/income.csv"))
        assert frame.to_dict("records") == [{"a": 1}]
        assert "Loaded the copy of income.csv saved on" in cell.html

    def test_any_other_address_still_explains_its_failure(self, world, monkeypatch):
        async def remote(name):
            raise ConnectionError(f"Couldn't fetch {name}.")
        monkeypatch.setattr(tt, "_fetch_remote", remote)
        with pytest.raises(ConnectionError, match="Couldn't fetch"):
            self.run(tt.load_csv("https://example.org/other.csv"))

    def test_outside_a_cell_the_data_still_loads_without_a_note(self, world):
        assert self.run(tt.load_text("book.txt")) == "It was a dark night.\n"

    def test_a_downloaded_page_reads_its_snapshots_from_the_manifest(self):
        import base64
        import gzip
        import json
        packed = base64.b64encode(gzip.compress(b"x\n1\n")).decode()
        tt.configure("../data/", json.dumps({"x.csv": {"snapshot": "2026-09-26"}}),
                     json.dumps({"x.csv": packed}))
        try:
            assert self.run(tt._snapshot_bytes("x.csv")) == b"x\n1\n"
            assert self.run(tt._dataset_index()) == {"x.csv": {"snapshot": "2026-09-26"}}
        finally:
            tt.configure("../data/")


class TestShapeLive:
    def test_every_step_in_its_order(self):
        raw = (b"-BEGIN HEADER-\nnotes\n-END HEADER-\n"
               b"YEAR, T2M ,CODE\n1949,1.234,A\n1950,-999,B\n1951,2.345,\n2030,3.0,C\n")
        recipe = {
            "skip_through": "-END HEADER-",
            "rename": {"YEAR": "year", "T2M": "temperature"},
            "missing": [-999],
            "drop_empty": ["CODE"],
            "at_least": {"year": 1950},
            "at_most": {"year": 2025},
            "columns": ["year", "temperature"],
            "round": {"temperature": 1},
        }
        # 1949 is too early, 1951 has no code, 2030 is too late: only 1950
        # is left, and its -999 is no value at all.
        assert tt.shape_live(raw, recipe) == b"year,temperature\n1950,\n"

    def test_namibia_is_not_a_missing_value(self):
        raw = b"name,cc\nMassospondylus,NA\nTyrannosaurus,US\nSomething,\n"
        assert tt.shape_live(raw, {"columns": ["name", "cc"]}) == (
            b"name,cc\nMassospondylus,NA\nTyrannosaurus,US\nSomething,\n")

    def test_a_marker_that_is_not_there_is_a_failure(self):
        with pytest.raises(ValueError, match="no line starts with"):
            tt.shape_live(b"a\n1\n", {"skip_through": "-END-", "columns": ["a"]})


class TestDataNote:
    def test_its_three_cases(self):
        import datetime
        entry = {"snapshot": "2026-09-26", "live": {"source": "Our World in Data"}}
        assert tt.data_note("life.csv", entry, used_live=True) == (
            "Loaded life.csv from Our World in Data just now. The numbers on this "
            "page come from the copy saved on 26 September 2026, so yours may be "
            "a little different.")
        assert tt.data_note("life.csv", entry, used_live=False,
                            today=datetime.date(2026, 10, 6)) == (
            "Loaded the copy of life.csv saved on 26 September 2026 (10 days ago). "
            "The live copy from Our World in Data could not be used just now, so "
            "this is the copy the page was written with.")
        assert tt.data_note("book.txt", {"snapshot": "2026-09-20"}, used_live=False) == (
            "Loaded the copy of book.txt saved on 20 September 2026.")
        assert tt.data_note("x.csv", {}, used_live=False) == "Loaded x.csv."
