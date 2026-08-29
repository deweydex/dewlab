"""dewlab's tutorial-facing runtime.

This is the module a student's cell code sees. It does two jobs:

  * it runs a cell and renders whatever the cell produced — printed text, the
    value of the last expression, DataFrames, matplotlib figures, tracebacks —
    into that cell's own output area, in the order the code produced it;

  * it provides the small bridge a cell uses to put something on the page and
    read something back: `text_input`, `dropdown`, `button`, `show`,
    `show_table`, and `check` — plus `load_csv` and `run_query` for pulling
    in data, the latter usable wherever sqlite3 is loaded (Mini IDE today;
    planning/MINI_IDE_REDESIGN.md Phase 4).

Built from the specification in planning/DECISIONS.md, which names those six
functions and pins down one signature, `check(actual, expected)`. Everything
else about how they behave was designed rather than looked up, and every such
choice is written down in DECISIONS_LOG.md rather than left implicit here.

Nothing about this is assessment-shaped: no scoring, no submission, no record
kept anywhere. `check` tells a student whether they got it, and that is all.

The module imports and works under plain CPython, with the DOM replaced by a
recording stub. That is what lets the rendering rules be unit-tested without a
browser; it is not a supported way to run tutorials.
"""

from __future__ import annotations

import asyncio
import base64
import html
import io
import linecache
import math
import os
import sys
import traceback
import warnings

# Force matplotlib's non-interactive backend before it is ever imported. dewlab
# captures figures itself, as PNGs written into the cell's output area, rather
# than letting a canvas backend draw wherever it likes on the page.
os.environ.setdefault("MPLBACKEND", "AGG")

# That backend has no window to open, so matplotlib warns when a student calls
# plt.show(). The figure appears anyway — dewlab renders it — which makes the
# warning purely alarming: a scarlet block under a plot that worked. dewlab
# replaces show() with its own (see _patch_pyplot_show); this covers the gap in
# a cell that imports pyplot and calls show() before that replacement lands.
warnings.filterwarnings(
    "ignore", message="FigureCanvasAgg is non-interactive", category=UserWarning
)

__all__ = [
    "text_input",
    "dropdown",
    "button",
    "image_input",
    "show",
    "show_table",
    "check",
    "load_csv",
    "run_query",
]

# --------------------------------------------------------------------------
# Environment
# --------------------------------------------------------------------------

try:  # pragma: no cover - exercised in the browser, stubbed in unit tests
    import js as _js
    from pyodide.ffi import create_proxy as _create_proxy

    IN_BROWSER = True
except ImportError:
    _js = None
    _create_proxy = None
    IN_BROWSER = False


# --------------------------------------------------------------------------
# Output sinks
#
# A sink is "where this cell's output goes". The browser sink appends real
# elements to the cell's output div; the recording sink keeps the markup in a
# list so tests can assert on it. Everything above this line generates markup
# and does not care which one it is talking to.
# --------------------------------------------------------------------------


"""These three sink classes are a small example of "duck typing": they
share no common base class, but each one defines the same four methods
(`stream`, `close_stream`, `append_html`, `clear`) with the same meaning.
Anything that calls `cell.sink.stream(...)` doesn't need to check which
kind of sink it has — as long as it quacks like a sink (has those
methods), it works. That's what lets the exact same rendering code
further down this file (`_render_value`, `show`, `check`, and so on) work
identically whether the cell is running in a browser tab, inside a Web
Worker, or in a plain Python test with no browser at all."""


class _RecordingSink:
    """Collects emitted markup instead of touching a DOM. Used by the tests."""

    def __init__(self):
        self.emitted: list[str] = []
        self.count = 0
        self._stream_class: str | None = None
        self._stream_text: str = ""

    # -- streaming text (stdout/stderr) ------------------------------------

    def stream(self, css_class: str, text: str) -> None:
        if self._stream_class != css_class:
            self.close_stream()
            self._stream_class = css_class
            self.count += 1
        self._stream_text += text

    def close_stream(self) -> None:
        if self._stream_class is not None:
            self.emitted.append(
                f'<pre class="{self._stream_class}">{html.escape(self._stream_text)}</pre>'
            )
            self._stream_class = None
            self._stream_text = ""

    # -- discrete blocks ---------------------------------------------------

    def append_html(self, markup: str):
        self.close_stream()
        self.emitted.append(markup)
        self.count += 1
        return None

    def clear(self) -> None:
        self.emitted.clear()
        self._stream_class = None
        self._stream_text = ""

    @property
    def html(self) -> str:
        """Everything emitted so far, including any still-open stream block."""
        pending = (
            [f'<pre class="{self._stream_class}">{html.escape(self._stream_text)}</pre>']
            if self._stream_class is not None
            else []
        )
        return "".join(self.emitted + pending)


class _DomSink:
    """Appends output into one cell's `.dl-output` element."""

    def __init__(self, element):
        self._el = element
        self.count = 0
        self._stream_el = None
        self._stream_class = None

    def stream(self, css_class: str, text: str) -> None:
        if self._stream_class != css_class or self._stream_el is None:
            self.close_stream()
            el = _js.document.createElement("pre")
            el.className = css_class
            self._el.appendChild(el)
            self._stream_el = el
            self._stream_class = css_class
            self.count += 1
        # textContent, never innerHTML: printed output is data, not markup.
        self._stream_el.textContent = self._stream_el.textContent + text

    def close_stream(self) -> None:
        self._stream_el = None
        self._stream_class = None

    def append_html(self, markup: str):
        self.close_stream()
        template = _js.document.createElement("template")
        template.innerHTML = markup
        # Capture the root before appendChild empties the fragment; widgets
        # need it to find their own input element again.
        root = template.content.firstElementChild
        self._el.appendChild(template.content)
        self.count += 1
        return root

    def clear(self) -> None:
        self.close_stream()
        self._el.replaceChildren()


class _MessageSink:
    """The Worker-side counterpart to `_DomSink`: nothing here has a `document`
    to touch — a Worker has none — so instead of appending real elements, each
    call posts one event to the main thread, which does the actual DOM write
    (`assets/pyodide-worker.js`'s `run-cell` handler, `applyOutputEvent()` in
    tutorial-runtime.js). `emit` is a plain JS function called with four
    positional, always-primitive arguments — `(kind, css_class, text,
    markup)`, unused ones `None` — rather than a dict, so nothing here ever
    crosses the postMessage boundary as a PyProxy needing `.toJs()`.

    `append_html()` always returns `None`: there is no live element for a
    widget to find itself again through. That is a real, deliberate gap, not
    an oversight — see `text_input`/`dropdown`/`button`'s own guard below and
    DECISIONS_LOG.md 7.77."""

    def __init__(self, emit):
        self._emit = emit
        self.count = 0
        self._stream_class: str | None = None

    def stream(self, css_class: str, text: str) -> None:
        if self._stream_class != css_class:
            self.count += 1
        self._stream_class = css_class
        self._emit("stream", css_class, text, None)

    def close_stream(self) -> None:
        self._stream_class = None

    def append_html(self, markup: str):
        self.close_stream()
        self.count += 1
        self._emit("append", None, None, markup)
        return None

    def clear(self) -> None:
        self.close_stream()
        self._emit("clear", None, None, None)


# --------------------------------------------------------------------------
# Cell state
# --------------------------------------------------------------------------


class _CellContext:
    def __init__(self, cell_id: str, sink):
        self.cell_id = cell_id
        self.sink = sink
        self.widget_seq = 0
        self.figures_rendered: set[int] = set()
        self.filename = cell_filename(cell_id)
        # (emission count, value) of the most recent check(), so a cell ending
        # in a check does not print a bare True/False under its own verdict.
        self.last_check: tuple[int, bool] | None = None


_current: _CellContext | None = None

# Every cell on a page shares one namespace, in document order — the notebook
# model. This does not persist across pages: each tutorial page is its own
# Pyodide instance, so a setup cell re-executes on every page load.
_page_globals: dict = {}

# What a student typed into a widget, keyed by (cell_id, widget_id). Re-running
# a cell rebuilds its widgets from scratch, so without this every re-run would
# silently discard the reader's input.
_widget_values: dict[tuple[str, str], object] = {}

# Where this page's shared CSV data lives, relative to the page. Set by the
# runtime from the build-time manifest.
_data_base = "../data/"


def configure(data_base: str) -> None:
    """Point `load_csv` at this page's `/data/` folder."""
    global _data_base
    _data_base = data_base or "../data/"


def _require_cell() -> _CellContext:
    if _current is None:
        raise RuntimeError(
            "tutorial_tools output functions can only be called from inside a "
            "running cell."
        )
    return _current


class _StreamWriter(io.TextIOBase):
    """Routes `print` into the running cell's output area as it happens.

    `print(...)` doesn't know anything about cells or web pages — it just
    writes text to whatever object is currently `sys.stdout` (Python's
    built-in idea of "the output stream"). Normally that's the terminal;
    here, `_begin()` further down swaps `sys.stdout` out for one of these
    objects instead, for the duration of one cell's run. `io.TextIOBase`
    is Python's own base class for "a thing text can be written to" — by
    subclassing it and overriding `write()`, this becomes a valid
    stand-in for stdout as far as `print` is concerned, even though
    what it actually does with the text (append it into a cell's output
    area) has nothing to do with files or terminals.
    """

    def __init__(self, css_class: str):
        self._css_class = css_class

    def write(self, text: str) -> int:  # type: ignore[override]
        if text and _current is not None:
            _current.sink.stream(self._css_class, text)
        return len(text)

    def writable(self) -> bool:  # type: ignore[override]
        return True


# --------------------------------------------------------------------------
# Value rendering
# --------------------------------------------------------------------------


def _pandas():
    """pandas, but only if the cell already imported it. Never forces it.

    `sys.modules` is Python's own cache of every module that has been
    imported anywhere so far in this program. Checking it with `.get(...)`
    (which returns `None` instead of raising if the key isn't there) is
    how this asks "has pandas been imported yet?" without importing it
    itself — importing pandas here "just to check" would make it load on
    every single cell run, whether or not the student's own code ever
    uses it, which would slow things down for no reason.
    """
    return sys.modules.get("pandas")


def _numpy():
    """Same idea as `_pandas` above, for numpy."""
    return sys.modules.get("numpy")


def _is_dataframe(value) -> bool:
    pd = _pandas()
    return pd is not None and isinstance(value, (pd.DataFrame, pd.Series))


def _is_artist(value) -> bool:
    """A matplotlib drawing object — a Line2D, a Text, a container of them.

    `plt.plot(...)` returns a list of Line2D and `plt.title(...)` returns a
    Text. A notebook prints those reprs above the figure; for someone meeting
    matplotlib for the first time it is pure noise, and dewlab drops it. The
    figure itself still renders.
    """
    artist = sys.modules.get("matplotlib.artist")
    if artist is None:
        return False
    if isinstance(value, artist.Artist):
        return True
    return (
        isinstance(value, (list, tuple))
        and len(value) > 0
        and all(isinstance(item, artist.Artist) for item in value)
    )


def _is_figure(value) -> bool:
    mpl = sys.modules.get("matplotlib.figure")
    return mpl is not None and isinstance(value, mpl.Figure)


# Axis chrome is drawn in one neutral grey rather than the current theme's
# foreground. A theme-matched ink would look better right up until the reader
# switches theme, at which point every already-rendered figure would be wrong —
# the PNG is baked, and keeping every figure open for the life of the page just
# to repaint it is not worth it. This grey holds about 4.15:1 against both the
# light and the dark page background, so it is readable either way and never
# becomes wrong.
_FIGURE_INK = "#7a7a7a"


def _recolour_for_theme(figure, ink: str) -> None:
    """Repaint a figure's chrome — titles, labels, ticks, spines — in `ink`.

    Only the chrome. The plotted data keeps whatever colours the student's code
    chose, which is the part they are learning to control.
    """
    for axes in figure.get_axes():
        axes.title.set_color(ink)
        axes.xaxis.label.set_color(ink)
        axes.yaxis.label.set_color(ink)
        axes.tick_params(colors=ink, which="both")
        for spine in axes.spines.values():
            spine.set_color(ink)
        legend = axes.get_legend()
        if legend is not None:
            for text in legend.get_texts():
                text.set_color(ink)
    for text in figure.texts:
        text.set_color(ink)


def _figure_html(figure) -> str:
    # Transparent, so the page background shows through and a figure never sits
    # in a white box on a dark page.
    _recolour_for_theme(figure, _FIGURE_INK)

    buffer = io.BytesIO()
    figure.savefig(
        buffer, format="png", dpi=110, bbox_inches="tight", transparent=True
    )
    encoded = base64.b64encode(buffer.getvalue()).decode("ascii")
    return (
        '<div class="dl-figure">'
        f'<img alt="Figure produced by this cell" src="data:image/png;base64,{encoded}">'
        "</div>"
    )


def _table_html(frame, max_rows: int = 20, caption: str | None = None) -> str:
    """A DataFrame or Series as a scrollable HTML table.

    Long frames are truncated rather than dumping thousands of rows into the
    page; the note under the table says so, so a reader is never misled about
    how much data they are looking at.
    """
    pd = _pandas()
    if pd is None:  # pragma: no cover - unreachable once pandas is loaded
        return f'<pre class="dl-repr">{html.escape(repr(frame))}</pre>'

    total = len(frame)
    truncated = max_rows is not None and total > max_rows
    shown = frame.head(max_rows) if truncated else frame

    if isinstance(shown, pd.Series):
        shown = shown.to_frame()

    # pandas escapes cell contents by default; keep it that way.
    table = shown.to_html(border=0, classes=None, escape=True, na_rep="")

    parts = ['<div class="dl-table-wrap">']
    if caption:
        parts.append(f'<div class="dl-table-caption">{html.escape(str(caption))}</div>')
    parts.append(table)
    if truncated:
        parts.append(
            f'<div class="dl-table-note">Showing the first {max_rows} of {total} rows.</div>'
        )
    parts.append("</div>")
    return "".join(parts)


def _render_value(value) -> None:
    """Render one value into the current cell's output area.

    The rules, in order: `None` renders nothing (so a cell ending in an
    assignment or a `print` stays quiet); DataFrames and Series render as
    tables; matplotlib figures render as PNGs; everything else falls back to
    `repr`, which is what a reader coming from a notebook expects.
    """
    if value is None:
        return

    cell = _require_cell()

    # A cell ending in `check(...)` shows the verdict, not a bare True or False
    # repeated underneath it.
    if (
        isinstance(value, bool)
        and cell.last_check is not None
        and cell.last_check == (cell.sink.count, value)
    ):
        return

    if _is_dataframe(value):
        cell.sink.append_html(_table_html(value))
        return

    if _is_figure(value):
        cell.figures_rendered.add(id(value))
        cell.sink.append_html(_figure_html(value))
        return

    if _is_artist(value):
        return

    cell.sink.append_html(f'<pre class="dl-repr">{html.escape(repr(value))}</pre>')


def _patch_pyplot_show() -> None:
    """Make `plt.show()` mean what someone learning matplotlib expects.

    Every tutorial and every textbook ends a plot with `plt.show()`, so students
    write it whether or not dewlab needs it. Under the non-interactive backend
    matplotlib's own show() draws nothing and warns about a canvas — noise at
    best, and at worst a red block under a plot that rendered perfectly well.

    dewlab's replacement renders the open figures at the point of the call, so a
    cell that draws, prints something, then draws again reads in the order it
    was written. Installed lazily because pyplot may not be imported yet, and
    idempotent because it is called on every cell.
    """
    plt = sys.modules.get("matplotlib.pyplot")
    if plt is None or getattr(plt.show, "_dewlab", False):
        return

    def show(*args, **kwargs):
        """Render the figures drawn so far. Accepts and ignores matplotlib's
        own arguments (`block=`) so existing code keeps working."""
        _flush_figures()

    show._dewlab = True
    plt.show = show


def _flush_figures() -> None:
    """Render any figure the cell created but never returned.

    `plt.plot(...)` followed by nothing is the common case in a tutorial, and a
    reader reasonably expects the plot to appear. Figures are closed afterwards
    so the next cell starts clean.
    """
    plt = sys.modules.get("matplotlib.pyplot")
    if plt is None:
        return
    _patch_pyplot_show()

    cell = _require_cell()
    for number in plt.get_fignums():
        figure = plt.figure(number)
        if id(figure) not in cell.figures_rendered:
            cell.sink.append_html(_figure_html(figure))
    plt.close("all")


# --------------------------------------------------------------------------
# Errors
# --------------------------------------------------------------------------

_CELL_FILENAME_PREFIX = "<cell "


def cell_filename(cell_id: str) -> str:
    """The pseudo-filename a cell's code is compiled under.

    Per cell rather than one shared name, for two reasons: a traceback then
    says which cell it came from, and each cell's source can be registered in
    `linecache` under its own key without a stale entry from another cell
    surfacing the wrong line.
    """
    return f"{_CELL_FILENAME_PREFIX}{cell_id}>"


def _is_user_frame(filename: str) -> bool:
    return filename.startswith(_CELL_FILENAME_PREFIX)


def _register_source(filename: str, code: str) -> None:
    """Let `traceback` show the student the line that actually failed.

    A cell's code never touches disk, so `linecache` has nothing to read and a
    traceback would name a line number without ever showing the line. Seeding
    the cache is the standard fix, and to a learner the line matters a great
    deal more than the number does.
    """
    linecache.cache[filename] = (len(code), None, code.splitlines(keepends=True), filename)


def _format_exception(exc: BaseException) -> str:
    """A traceback trimmed to the student's own code.

    The frames from `eval_code_async` and from this module are noise to someone
    learning Python; a NameError should point at the line they wrote, not at
    dewlab's plumbing.

    A syntax error has no frames of the student's at all, because it is raised
    while the code is being compiled rather than while it runs — so trimming
    leaves nothing. This used to fall back to the full traceback, which opened
    every syntax error with two frames of `tutorial_tools.py` before the line
    the student had actually mistyped. That is the wrong thing to show anybody,
    and it is very much the wrong thing to show a reader of *When It Goes
    Wrong*, whose subject is reading these messages.

    But a syntax error carries its own location — filename, line, and the caret
    — and Python prints those from the exception rather than from the stack. So
    where the exception knows where it happened, the stack goes entirely and
    what is left is exactly the part that helps.
    """
    summary = traceback.TracebackException.from_exception(exc)

    for item in [summary] + list(_chained(summary)):
        user_frames = [f for f in item.stack if _is_user_frame(f.filename)]
        if user_frames:
            item.stack = traceback.StackSummary.from_list(user_frames)
        elif getattr(item, "lineno", None) is not None:
            # A syntax error: it says where it is, so the frames that led here
            # are all ours and none of them help.
            item.stack = traceback.StackSummary.from_list([])

    return "".join(summary.format())


def _chained(summary):
    """Walks the chain of "this error happened while handling that other
    error" back to its start.

    In Python, raising an exception while already handling one (a `raise`
    inside an `except` block, or even just a second error happening inside
    that block) doesn't lose the original — Python remembers it on the new
    exception's `__context__` attribute (or `__cause__`, if it was an
    explicit `raise new_error from original_error`). `_format_exception`
    above uses this to trim *every* traceback in the chain down to the
    student's own code, not just the outermost one. `seen` guards against
    looping forever in the (rare, but possible) case where two exceptions
    somehow end up referencing each other.
    """
    seen = []
    current = summary
    while True:
        nxt = current.__cause__ or current.__context__
        if nxt is None or nxt in seen:
            return seen
        seen.append(nxt)
        current = nxt


def render_error(message: str) -> None:
    """Show an error block in the current cell. Also called from the runtime."""
    cell = _require_cell()
    cell.sink.append_html(f'<pre class="dl-error">{html.escape(message)}</pre>')


# --------------------------------------------------------------------------
# Cell lifecycle
# --------------------------------------------------------------------------


def _begin(cell_id: str, sink, code: str = "") -> None:
    """Everything that has to happen right before a cell's code runs:
    clear its old output, make it the "current" cell (so the module-level
    functions below like `show()` know which cell they belong to), teach
    `linecache` about its source for tracebacks, and — this is the
    important part — replace `sys.stdout`/`sys.stderr` with the
    `_StreamWriter`s from above, so any `print()` the student's code does
    lands in this cell's output area instead of vanishing into nowhere
    (there's no terminal for it to go to in a browser).
    """
    global _current
    sink.clear()
    _current = _CellContext(cell_id, sink)
    _register_source(_current.filename, code)
    _patch_pyplot_show()
    sys.stdout = _StreamWriter("dl-stdout")
    sys.stderr = _StreamWriter("dl-error")


def _end(value) -> None:
    """The matching cleanup for `_begin()`, always run once a cell finishes
    (successfully or not — see `run_cell`'s `finally` below). Renders
    whatever value the cell's last line produced, flushes any matplotlib
    figures that were drawn but never shown, and — critically — puts
    `sys.stdout`/`sys.stderr` back the way they were (`sys.__stdout__` is
    Python's own untouched original, saved before anything could replace
    it) so a later cell, or anything else in the interpreter, doesn't
    keep writing into a cell that has already finished running.
    """
    global _current
    try:
        _render_value(value)
        _flush_figures()
        _current.sink.close_stream()
    finally:
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
        _current = None


async def run_cell(cell_id: str, output_target, code: str) -> bool:
    """Run one cell's code and render everything it produced.

    Returns True if the code completed without raising. The whole lifecycle
    lives here, in Python, rather than being split across the JS runtime, so
    output ordering and traceback formatting have exactly one implementation.

    `output_target` is either a real `.dl-output` element (the main-thread
    path the standalone export still uses — DECISIONS_LOG.md 7.77 keeps that
    export on the pre-Worker runtime) or the `emit` callable
    `assets/pyodide-worker.js` passes for a page running Pyodide in a Worker.
    A callable can never be mistaken for an element, so which sink to build
    is exactly that check.
    """
    from pyodide.code import eval_code_async  # pragma: no cover - browser only

    sink = _MessageSink(output_target) if callable(output_target) else _DomSink(output_target)
    _begin(cell_id, sink, code)
    ok = True
    value = None
    try:
        value = await eval_code_async(
            code, globals=_page_globals, filename=_current.filename
        )
    except KeyboardInterrupt:
        # A reader's own Stop click (planning/CELL_CONTROLS.md), not a bug in
        # their code — a full traceback would say so anyway, but "Stopped."
        # is the honest, unintimidating version of the same fact.
        ok = False
        _current.sink.close_stream()
        render_error("Stopped.")
    except BaseException as exc:  # noqa: BLE001 - a student's error is normal traffic
        ok = False
        _current.sink.close_stream()
        render_error(_format_exception(exc))
    finally:
        _end(value if ok else None)
    return ok


def reset_page_state() -> None:
    """Clear the shared namespace and every remembered widget value."""
    _page_globals.clear()
    _widget_values.clear()


# --------------------------------------------------------------------------
# Public output functions
# --------------------------------------------------------------------------


def show(*values, label: str | None = None) -> None:
    """Render values into this cell's output area.

    The explicit form of what a cell's last expression does automatically —
    useful mid-cell, or for showing several things from one cell.
    """
    cell = _require_cell()
    if label:
        cell.sink.append_html(
            f'<div class="dl-table-caption">{html.escape(str(label))}</div>'
        )
    for value in values:
        _render_value(value)


def show_table(frame, max_rows: int = 20, caption: str | None = None) -> None:
    """Render a DataFrame or Series as a table, truncated to `max_rows`."""
    cell = _require_cell()
    cell.sink.append_html(_table_html(frame, max_rows=max_rows, caption=caption))


# --------------------------------------------------------------------------
# check()
# --------------------------------------------------------------------------


def _compare(actual, expected, tolerance: float | None) -> tuple[bool, str]:
    """Compare two answers the way a person would mean it.

    Pure, and the reason `check` is worth unit-testing: floats compare within a
    tolerance rather than exactly, numpy arrays and pandas objects compare
    elementwise instead of raising "truth value is ambiguous", and everything
    else falls back to `==`.

    Returns (passed, detail) where detail is a short human-readable reason,
    empty when it passed.
    """
    np = _numpy()
    pd = _pandas()

    def describe(value) -> str:
        text = repr(value)
        return text if len(text) <= 120 else text[:117] + "..."

    mismatch = f"got {describe(actual)}, expected {describe(expected)}"

    # pandas first: a DataFrame is also array-like, and .equals is the right
    # comparison for one.
    if pd is not None and isinstance(actual, (pd.DataFrame, pd.Series)):
        if not isinstance(expected, type(actual)):
            return False, f"got a {type(actual).__name__}, expected a {type(expected).__name__}"
        if tolerance is not None and np is not None:
            try:
                same = actual.shape == expected.shape and bool(
                    np.allclose(actual.to_numpy(), expected.to_numpy(), atol=tolerance, rtol=0)
                )
            except (TypeError, ValueError):
                same = bool(actual.equals(expected))
        else:
            same = bool(actual.equals(expected))
        return same, "" if same else "the values differ"

    if np is not None and isinstance(actual, np.ndarray):
        expected_array = np.asarray(expected)
        if actual.shape != expected_array.shape:
            return False, f"got shape {actual.shape}, expected shape {expected_array.shape}"
        if np.issubdtype(actual.dtype, np.floating) or tolerance is not None:
            same = bool(np.allclose(actual, expected_array, atol=tolerance or 1e-9, rtol=1e-9))
        else:
            same = bool(np.array_equal(actual, expected_array))
        return same, "" if same else "the values differ"

    # bool before int: True == 1 is true in Python, and it is not the answer a
    # student meant to give.
    if isinstance(actual, bool) or isinstance(expected, bool):
        same = actual is expected
        return same, "" if same else mismatch

    if isinstance(actual, (int, float)) and isinstance(expected, (int, float)):
        if tolerance is not None:
            same = abs(actual - expected) <= tolerance
        elif isinstance(actual, float) or isinstance(expected, float):
            same = math.isclose(actual, expected, rel_tol=1e-9, abs_tol=1e-12)
        else:
            same = actual == expected
        return same, "" if same else mismatch

    if isinstance(actual, (list, tuple)) and isinstance(expected, (list, tuple)):
        if len(actual) != len(expected):
            return False, f"got {len(actual)} items, expected {len(expected)}"
        for index, (a, e) in enumerate(zip(actual, expected)):
            same, _ = _compare(a, e, tolerance)
            if not same:
                return False, f"item {index} differs: got {describe(a)}, expected {describe(e)}"
        return True, ""

    try:
        same = bool(actual == expected)
    except (TypeError, ValueError):
        same = False
    return same, "" if same else mismatch


def _check_html(passed: bool, label: str | None, detail: str) -> str:
    css = "dl-check-pass" if passed else "dl-check-fail"
    mark = "✓" if passed else "✗"
    heading = label or ("That's right." if passed else "Not quite yet.")
    parts = [
        f'<div class="dl-check {css}">',
        f'<span class="dl-check-mark">{mark}</span>',
        f"<span>{html.escape(str(heading))}",
    ]
    if detail and not passed:
        parts.append(f' <span class="dl-check-detail">({html.escape(detail)})</span>')
    parts.append("</span></div>")
    return "".join(parts)


def check(actual, expected, tolerance: float | None = None, label: str | None = None) -> bool:
    """Compare a student's answer with the expected one and say how it went.

    Formative feedback only. Nothing is scored, nothing is recorded, and the
    result has no connection to any institutional grade. Returns the boolean
    too, so a cell can branch on it.
    """
    cell = _require_cell()
    passed, detail = _compare(actual, expected, tolerance)
    cell.sink.append_html(_check_html(passed, label, detail))
    cell.last_check = (cell.sink.count, passed)
    return passed


# --------------------------------------------------------------------------
# Widgets
# --------------------------------------------------------------------------


def _widget_id(explicit: str | None, label: str) -> str:
    """A stable id for a widget within its cell.

    Explicit beats derived; derived beats positional. The point is that the
    same widget keeps the same id across re-runs, so the value a student typed
    survives clicking Run again.
    """
    cell = _require_cell()
    cell.widget_seq += 1
    if explicit:
        return str(explicit)
    slug = "".join(c.lower() if c.isalnum() else "-" for c in str(label)).strip("-")
    slug = "-".join(part for part in slug.split("-") if part)
    return f"{slug or 'widget'}-{cell.widget_seq}"


class _Widget:
    """A handle onto a control rendered in the cell's output area.

    `.value` reads the live DOM every time rather than caching, so a cell that
    reads it after the reader has typed sees what is actually on screen.
    """

    def __init__(self, cell_id: str, widget_id: str, element, kind: str):
        self._cell_id = cell_id
        self._widget_id = widget_id
        self._element = element
        self._kind = kind

    @property
    def id(self) -> str:
        return self._widget_id

    @property
    def value(self):
        # An `image_input` keeps its picked value out of band in
        # `_widget_values` (see `image_input` below) rather than in the file
        # input's own `.value`, which is only ever the filename string.
        if self._kind == "image_input" or self._element is None:
            return _widget_values.get((self._cell_id, self._widget_id))
        control = self._element.querySelector("input, select")
        if control is None:
            return None
        return control.value

    def __repr__(self) -> str:
        return f"<{self._kind} {self._widget_id!r} value={self.value!r}>"


def _remember(cell_id: str, widget_id: str, value) -> None:
    _widget_values[(cell_id, widget_id)] = value


def _require_dom_sink(kind: str) -> _CellContext:
    """Widgets need a live element to attach a listener to — one
    `_MessageSink` (a Worker-run page) cannot hand back, since there is no
    DOM on that side of the postMessage boundary to hand back a reference
    into (DECISIONS_LOG.md 7.77). Nothing published uses `text_input`,
    `dropdown`, `button` or `image_input` today, so this is a real gap with
    no live tutorial behind it — and a clear error a reader can see beats
    the silent one this would otherwise be: markup that renders but does
    nothing when clicked or typed into."""
    cell = _require_cell()
    if isinstance(cell.sink, _MessageSink):
        raise RuntimeError(
            f"{kind}() needs a page running Pyodide on the main thread — this "
            "tutorial page runs it in a background Worker, and Worker code has "
            "no direct access to the page to attach the widget to."
        )
    return cell


def _mount_widget(markup: str, cell_id: str, widget_id: str, kind: str) -> _Widget:
    """Puts a widget's HTML on the page and wires it up to remember what
    the student types into it.

    The `on_change(_event, _cell=cell_id, _wid=widget_id, _control=control)`
    line looks unusual, and it's worth understanding why it's written that
    way rather than just using `cell_id`, `widget_id`, and `control`
    directly inside the function. If several widgets get created (say, in
    a loop, or just several `text_input()` calls in the same cell),
    ordinary variables like `cell_id` would be *shared* by every one of
    those inner functions — by the time a student actually clicks or
    types, `cell_id` might have already changed to a later widget's value.
    Giving each argument a default value captures the *current* value of
    `cell_id`/`widget_id`/`control` at the moment `on_change` is defined,
    once per widget, so each widget's own change handler always uses its
    own values no matter what happens afterward. This is a common Python
    idiom for exactly this problem, sometimes called "binding early."

    `_create_proxy` matters too: this is Python code, but
    `addEventListener` is a JavaScript API — Pyodide's `create_proxy`
    wraps a Python function so JavaScript can call it back like a normal
    JS callback. Skipped (via the `is not None` check) when this file is
    running outside a browser at all, e.g. under the plain-Python tests.
    """
    cell = _require_cell()
    root = cell.sink.append_html(markup)
    widget = _Widget(cell_id, widget_id, root, kind)

    if root is not None and _create_proxy is not None:
        control = root.querySelector("input, select")
        if control is not None:
            def on_change(_event, _cell=cell_id, _wid=widget_id, _control=control):
                _remember(_cell, _wid, _control.value)

            control.addEventListener("input", _create_proxy(on_change))
    return widget


def text_input(label: str = "", value: str = "", id: str | None = None) -> _Widget:  # noqa: A002
    """A single-line text box. Read what the reader typed with `.value`."""
    cell = _require_dom_sink("text_input")
    widget_id = _widget_id(id, label or "text")
    current = _widget_values.get((cell.cell_id, widget_id), value)
    dom_id = f"dl-w-{html.escape(cell.cell_id)}-{html.escape(widget_id)}"
    markup = (
        '<div class="dl-widget">'
        + (f'<label for="{dom_id}">{html.escape(str(label))}</label>' if label else "")
        + f'<input type="text" id="{dom_id}" value="{html.escape(str(current), quote=True)}">'
        + "</div>"
    )
    return _mount_widget(markup, cell.cell_id, widget_id, "text_input")


def dropdown(label: str = "", options=(), value=None, id: str | None = None) -> _Widget:  # noqa: A002
    """A select box over `options`. Read the chosen option with `.value`."""
    cell = _require_dom_sink("dropdown")
    widget_id = _widget_id(id, label or "choice")
    options = list(options)
    current = _widget_values.get((cell.cell_id, widget_id), value)
    if current is None and options:
        current = options[0]

    dom_id = f"dl-w-{html.escape(cell.cell_id)}-{html.escape(widget_id)}"
    choices = "".join(
        f'<option value="{html.escape(str(option), quote=True)}"'
        + (" selected" if str(option) == str(current) else "")
        + f">{html.escape(str(option))}</option>"
        for option in options
    )
    markup = (
        '<div class="dl-widget">'
        + (f'<label for="{dom_id}">{html.escape(str(label))}</label>' if label else "")
        + f'<select id="{dom_id}">{choices}</select>'
        + "</div>"
    )
    return _mount_widget(markup, cell.cell_id, widget_id, "dropdown")


def button(label: str = "Go", on_click=None, id: str | None = None) -> _Widget:  # noqa: A002
    """A button that calls `on_click` when pressed.

    The callback runs with this cell's output area still current, so anything
    it prints or `show`s appends beneath the button rather than vanishing.
    """
    cell = _require_dom_sink("button")
    widget_id = _widget_id(id, label or "button")
    dom_id = f"dl-w-{html.escape(cell.cell_id)}-{html.escape(widget_id)}"
    markup = (
        '<div class="dl-widget">'
        f'<button type="button" class="dl-btn" id="{dom_id}">{html.escape(str(label))}</button>'
        "</div>"
    )

    sink = cell.sink
    root = sink.append_html(markup)
    widget = _Widget(cell.cell_id, widget_id, root, "button")

    if root is not None and on_click is not None and _create_proxy is not None:
        cell_id = cell.cell_id

        def handle(_event):
            """Runs `on_click()` when the button is clicked — which can
            happen long after the cell itself finished running, so this
            can't just reuse `_begin()`/`_end()` (those assume a cell is
            actively running via `run_cell`). Instead it does a smaller,
            self-contained version of the same setup/teardown: remember
            whatever cell was "current" before this click (`previous`,
            which is normally `None`, since no cell is running while the
            student is just clicking a button), temporarily make *this*
            button's cell current and route stdout/stderr into it so
            `print()` inside `on_click` works, run the callback, then put
            everything back exactly as it was — including restoring
            `previous` rather than always resetting to `None`, in case
            this button's own callback somehow triggers another cell
            while it runs.
            """
            global _current
            previous = _current
            _current = _CellContext(cell_id, sink)
            saved_stdout, saved_stderr = sys.stdout, sys.stderr
            sys.stdout = _StreamWriter("dl-stdout")
            sys.stderr = _StreamWriter("dl-error")
            try:
                _render_value(on_click())
                _flush_figures()
            except BaseException as exc:  # noqa: BLE001
                sink.close_stream()
                render_error(_format_exception(exc))
            finally:
                sink.close_stream()
                sys.stdout, sys.stderr = saved_stdout, saved_stderr
                _current = previous

        root.querySelector("button").addEventListener("click", _create_proxy(handle))

    return widget


def image_input(label: str = "Choose an image", id: str | None = None) -> _Widget:  # noqa: A002
    """A file picker limited to image files.

    `.value` is `None` until a reader picks one, then a Pillow `Image` once
    Pillow is loaded on this page, or the file's raw bytes if it is not —
    decoding is a convenience this offers when it can, not a requirement, so
    a page that never asked for Pillow still gets the file rather than an
    import error.
    """
    cell = _require_dom_sink("image_input")
    widget_id = _widget_id(id, label or "image")
    dom_id = f"dl-w-{html.escape(cell.cell_id)}-{html.escape(widget_id)}"
    markup = (
        '<div class="dl-widget">'
        + (f'<label for="{dom_id}">{html.escape(str(label))}</label>' if label else "")
        + f'<input type="file" accept="image/*" id="{dom_id}">'
        + "</div>"
    )
    sink = cell.sink
    root = sink.append_html(markup)
    widget = _Widget(cell.cell_id, widget_id, root, "image_input")

    if root is not None and _create_proxy is not None:
        control = root.querySelector("input")
        cell_id = cell.cell_id

        def on_change(_event, _cell=cell_id, _wid=widget_id, _control=control):
            """See `_mount_widget`'s comment above for why `_cell`/`_wid`/
            `_control` are captured as default-argument values rather than
            used directly.

            Reading the picked file's bytes (`arrayBuffer()`) is itself
            asynchronous — it has to wait for the browser to actually read
            the file off disk — but a DOM `change` event handler can't be
            declared `async` and awaited the normal way; JavaScript just
            fires the event and moves on. So the actual reading happens in
            a separate `async def read()` function, and
            `asyncio.ensure_future(read())` schedules it to run in the
            background without this outer function waiting for it. That's
            why `image_input()`'s `.value` starts out as `None` and only
            becomes the picked image sometime after the student picks a
            file — there's no way to make picking a file instant.
            """
            files = _control.files
            if files is None or files.length == 0:
                return
            picked = files.item(0)

            async def read():
                buf = await picked.arrayBuffer()
                data = buf.to_bytes()
                try:
                    from PIL import Image  # noqa: PLC0415 - deliberately lazy, optional

                    image = Image.open(io.BytesIO(data))
                    image.load()
                except ImportError:
                    image = data
                _remember(_cell, _wid, image)

            asyncio.ensure_future(read())

        control.addEventListener("change", _create_proxy(on_change))

    return widget


# --------------------------------------------------------------------------
# Shared data
# --------------------------------------------------------------------------


async def load_csv(name: str, **read_csv_kwargs):
    """Fetch a CSV from the shared `/data/` folder and return a DataFrame.

    Datasets live once and are fetched at runtime — never embedded or copied
    per tutorial. Everything is served from one origin, so this is a plain
    relative fetch with no CORS involved.

    Setup snippets use it with top-level await:

        df = await load_csv("life-expectancy.csv")
    """
    import pandas as pd  # noqa: PLC0415 - deliberately lazy
    from pyodide.http import pyfetch  # pragma: no cover - browser only

    response = await pyfetch(_data_base + name)
    if response.status != 200:
        raise FileNotFoundError(
            f"{name} is not in the shared data folder (HTTP {response.status})"
        )
    return pd.read_csv(io.BytesIO(await response.bytes()), **read_csv_kwargs)


def run_query(conn_or_path, sql: str, params=None, max_rows: int = 20, caption: str | None = None):
    """Run a SQL query and render the results as a table.

    `conn_or_path` is either an already-open `sqlite3.Connection`, or a path
    (or `":memory:"`) passed straight to `sqlite3.connect()` — a short-lived
    connection is opened and closed around this one query in that case, so a
    one-off query doesn't need its own connect/close boilerplate:

        run_query("students.db", "select * from grades where score > ?", (80,))

    Every query commits, including a `CREATE TABLE`/`INSERT`/`UPDATE` — the
    friendlier default for a student who doesn't yet know sqlite3 needs an
    explicit commit(); reach for sqlite3 directly for real transaction
    control. A statement with nothing to fetch (anything but a `SELECT`)
    still runs and commits, it just renders nothing. Either way, the result
    comes back as a DataFrame — table rendering here is the display, not the
    only way to use what came back.
    """
    import sqlite3  # noqa: PLC0415 - deliberately lazy, mirrors load_csv's pandas import
    import pandas as pd  # noqa: PLC0415

    cell = _require_cell()

    owns_connection = isinstance(conn_or_path, str)
    conn = sqlite3.connect(conn_or_path) if owns_connection else conn_or_path
    try:
        cursor = conn.execute(sql, params or ())
        columns = [description[0] for description in cursor.description or []]
        rows = cursor.fetchall()
        conn.commit()
    finally:
        if owns_connection:
            conn.close()

    frame = pd.DataFrame(rows, columns=columns)
    if columns:
        cell.sink.append_html(_table_html(frame, max_rows=max_rows, caption=caption))
    return frame
