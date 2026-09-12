"""dewlab's tutorial-facing runtime.

This is the module a student's cell code sees. It does two jobs:

  * it runs a cell and renders whatever the cell produced — printed text, the
    value of the last expression, DataFrames, matplotlib figures, tracebacks —
    into that cell's own output area, in the order the code produced it;

  * it provides the small bridge a cell uses to put something on the page and
    read something back: `text_input`, `dropdown`, `button`, `show`,
    `show_table`, and `check` — plus `load_csv` and `run_query` for pulling
    in data, the latter usable wherever sqlite3 is loaded (dewmini today).

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
import json
import io
import linecache
import math
import os
import sys
import traceback
import warnings

os.environ.setdefault("MPLBACKEND", "AGG")

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
    "load_text",
    "run_query",
]


try:  # pragma: no cover - exercised in the browser, stubbed in unit tests
    import js as _js
    from pyodide.ffi import create_proxy as _create_proxy

    IN_BROWSER = True
except ImportError:
    _js = None
    _create_proxy = None
    IN_BROWSER = False


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
    an oversight — see `text_input`/`dropdown`/`button`'s own guard below."""

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


class _CellContext:
    def __init__(self, cell_id: str, sink, label: str | None = None):
        self.cell_id = cell_id
        self.sink = sink
        self.widget_seq = 0
        self.figures_rendered: set[int] = set()
        self.filename = cell_filename(cell_id, label)
        # (emission count, value) of the most recent check(), so a cell ending
        # in a check does not print a bare True/False under its own verdict.
        self.last_check: tuple[int, bool] | None = None
        self.checks: list[tuple[str | None, bool]] = []
        self.last_error: tuple[str, str] | None = None


_current: _CellContext | None = None

_page_globals: dict = {}

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


_CELL_FILENAME_PREFIX = "<cell "


def cell_filename(cell_id: str, label: str | None = None) -> str:
    """The pseudo-filename a cell's code is compiled under.

    Per cell rather than one shared name, for two reasons: a traceback then
    says which cell it came from, and each cell's source can be registered in
    `linecache` under its own key without a stale entry from another cell
    surfacing the wrong line. `label`, when given, replaces `cell_id`
    entirely, in `linecache`'s own key as well as what a reader sees —
    unlike an id, a label is not guaranteed unique (a reader can name two
    dewmini cells the same thing), so two same-named cells do share one
    `linecache` entry. That's harmless for either cell's own run: this
    module always re-registers a cell's source immediately before running
    it and formats its traceback immediately after, before any other cell
    gets a turn, so the entry a run's own traceback reads back is always
    its own. It would only surface a wrong line for a traceback formatted
    well after the fact, from a stored exception object — nothing in this
    module does that today.
    """
    return f"{_CELL_FILENAME_PREFIX}{label or cell_id}>"


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


_ERROR_HINTS = (
    (
        ("unknown url type", "urlopen error", "URLError", "RemoteDisconnected"),
        "Reading a web address directly needs one line of setup here. Python "
        "is running inside a browser tab, so it has no network connection of "
        "its own — it has to borrow the browser's, and pandas doesn't know to "
        "do that until it is told:\n\n"
        "    import pyodide_http\n"
        "    pyodide_http.patch_all()\n\n"
        "Run that once, and pandas reads a URL normally from then on.\n\n"
        "The shorter route, needing no setup at all:\n\n"
        "    df = await load_csv(\"https://example.org/data.csv\")\n\n"
        "Either way, the site you are reading from has to allow other pages "
        "to read it. Many do; some don't, and the error will say so.",
    ),
    (
        ("No module named 'requests'", "No module named 'httpx'",
         "No module named 'urllib3'", "No module named 'aiohttp'"),
        "That library exists here but isn't loaded yet — this Python starts "
        "with a small set of packages and fetches the rest on request:\n\n"
        "    import micropip\n"
        "    await micropip.install(\"requests\")\n\n"
        "It also needs to borrow the browser's own network connection, since "
        "a page has no other:\n\n"
        "    import pyodide_http\n"
        "    pyodide_http.patch_all()\n\n"
        "After that, `requests.get(...)` works as it does anywhere else. For "
        "a CSV, `await load_csv(url)` needs none of this.",
    ),
)


def _hint_for(message: str) -> str | None:
    """A plain-English note to sit under a traceback, or None for the many
    errors that are genuinely about the student's own code and where a hint
    would just be noise."""
    for needles, hint in _ERROR_HINTS:
        if any(needle in message for needle in needles):
            return hint
    return None


def render_error(message: str) -> None:
    """Show an error block in the current cell. Also called from the runtime.

    A recognised failure gets a second block underneath explaining it — see
    `_ERROR_HINTS`. Under the traceback rather than instead of it: the real
    error is still what happened, and a student who goes looking for the
    exact message (in these notes, in a search) should find it.
    """
    cell = _require_cell()
    cell.sink.append_html(f'<pre class="dl-error">{html.escape(message)}</pre>')
    hint = _hint_for(message)
    if hint:
        cell.sink.append_html(f'<pre class="dl-error-hint">{html.escape(hint)}</pre>')


def _begin(cell_id: str, sink, code: str = "", label: str | None = None) -> None:
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
    _current = _CellContext(cell_id, sink, label)
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


async def run_cell(
    cell_id: str, output_target, code: str, expect: str | None = None, label: str | None = None,
) -> bool:
    """Run one cell's code and render everything it produced.

    Returns True if the code completed without raising. `expect`, when
    given, is evaluated after the run for the report `run_cell_report()`
    returns — it never affects the run itself. `label`, when given, is
    what a traceback's file line calls this cell instead of its own id —
    a tutorial's author-given `name:`, or dewmini's "Cell 3" for a cell
    nobody has named, rather than either's own internal id showing up in
    front of a reader (planning/CELL_IDENTITY.md). The whole lifecycle
    lives here, in Python, rather than being split across the JS runtime, so
    output ordering and traceback formatting have exactly one implementation.

    `output_target` is either a real `.dl-output` element (the main-thread
    path the standalone export still uses, kept on the pre-Worker runtime)
    or the `emit` callable
    `assets/pyodide-worker.js` passes for a page running Pyodide in a Worker.
    A callable can never be mistaken for an element, so which sink to build
    is exactly that check.
    """
    from pyodide.code import eval_code_async  # pragma: no cover - browser only

    global _last_report
    sink = _MessageSink(output_target) if callable(output_target) else _DomSink(output_target)
    _begin(cell_id, sink, code, label)
    ok = True
    value = None
    try:
        value = await eval_code_async(
            code, globals=_page_globals, filename=_current.filename
        )
    except KeyboardInterrupt:
        ok = False
        _current.last_error = ("KeyboardInterrupt", "Stopped.")
        _current.sink.close_stream()
        render_error("Stopped.")
    except BaseException as exc:  # noqa: BLE001 - a student's error is normal traffic
        ok = False
        _current.last_error = _describe_error(exc)
        _current.sink.close_stream()
        render_error(_format_exception(exc))
    finally:
        _last_report = _report(ok, _current, expect)
        _end(value if ok else None)
    return ok


# The report of the most recent run_cell(), kept for run_cell_report() —
# see there for why the two are separate functions.
_last_report: dict = {}


def _describe_error(exc: BaseException) -> tuple[str, str]:
    """An exception as (type name, first line of its message): what a staged
    hint's "identical errors" count compares from one run to the next. The
    first line only, because a SyntaxError's message runs on for several
    lines that repeat the offending code, and two runs of the same mistake
    should read as the same mistake."""
    message = str(exc).strip().split("\n", 1)[0]
    return type(exc).__name__, message


def holds(expression: str) -> bool:
    """Whether an author's `expect:` line is true of the page namespace right
    now (planning/CELL_HINTS.md §3). Anything that goes wrong evaluating it —
    a name not yet defined, a comparison that raises — is "not yet", not an
    error to show: the expression is the author's and the reader has never
    seen it."""
    try:
        return bool(eval(expression, _page_globals))  # noqa: S307 - the author's own expression
    except BaseException:  # noqa: BLE001
        return False


def _report(ok: bool, cell: "_CellContext", expect: str | None) -> dict:
    """What one run amounted to, for the page's attempt counters: whether it
    raised and which error, whether its checks passed and which one did not,
    and whether `expect:` holds. All plain values, so it can cross the
    Worker's postMessage boundary as JSON."""
    check = None
    if cell.checks:
        failed = [label for label, passed in cell.checks if not passed]
        check = {"passed": not failed, "label": failed[0] if failed else cell.checks[-1][0]}
    error = None
    if cell.last_error:
        error = {"type": cell.last_error[0], "message": cell.last_error[1]}
    return {
        "ok": ok,
        "error": error,
        "check": check,
        "reached": holds(expect) if expect else None,
    }


async def run_cell_report(
    cell_id: str, output_target, code: str, expect: str | None = None, label: str | None = None,
) -> str:
    """run_cell(), plus a JSON report of what the run amounted to — see
    `_report()`. The tutorial page calls this one; `run_cell()` itself
    keeps returning a plain boolean because dewmini and the shared engine
    (compose/dewmini.js, assets/pyodide-engine.js) read it that way. A
    string rather than a dict so the same value crosses both the main-thread
    call and the Worker's postMessage unchanged."""
    global _last_report
    _last_report = {}
    await run_cell(cell_id, output_target, code, expect, label)
    return json.dumps(_last_report)


def reset_page_state() -> None:
    """Clear the shared namespace and every remembered widget value."""
    _page_globals.clear()
    _widget_values.clear()


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
    cell.checks.append((label, passed))
    return passed


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
    into. Nothing published uses `text_input`,
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


async def load_csv(name: str, **read_csv_kwargs):
    """Fetch a CSV and return a DataFrame.

    `name` is either a file in the shared `/data/` folder, or a full URL to
    a CSV somewhere else on the web:

        df = await load_csv("life-expectancy.csv")
        df = await load_csv("https://example.org/some-data.csv")

    Datasets in the shared folder live once and are fetched at runtime —
    never embedded or copied per tutorial. They come from the same origin
    as the page, so that fetch is straightforward.

    A URL is not, and the failure needs explaining rather than reporting.
    A browser will only let a page read a file from another website if that
    website says it may (the CORS rule); when it refuses, the fetch fails
    with nothing useful attached, and a student reasonably concludes their
    own code is wrong. So a remote failure raises a message that says what
    actually happened and what to do instead — downloading the file and
    adding it through dewmini's Files section always works, because a file
    already on the machine has no other website's permission to ask for.
    """
    import pandas as pd  # noqa: PLC0415 - deliberately lazy
    from pyodide.http import pyfetch  # pragma: no cover - browser only

    remote = name.startswith("http://") or name.startswith("https://")
    url = name if remote else _data_base + name

    try:
        response = await pyfetch(url)
    except Exception as exc:  # pragma: no cover - browser-only failure path
        if not remote:
            raise
        raise ConnectionError(
            f"Couldn't fetch {name}.\n\n"
            "That file is on another website, and a browser only allows this "
            "page to read it if that site permits it — many do not. Nothing "
            "is wrong with your code.\n\n"
            "What does always work: download the file yourself, then add it "
            "through Files in the Workbench panel, and load it by name "
            "instead."
        ) from exc

    if response.status != 200:
        if remote:
            raise ConnectionError(
                f"{name} returned HTTP {response.status}.\n\n"
                "The address may have changed, or that site may not be "
                "handing this file out any more. Downloading it yourself and "
                "adding it through Files in the Workbench panel always works."
            )
        raise FileNotFoundError(
            f"{name} is not in the shared data folder (HTTP {response.status})"
        )
    return pd.read_csv(io.BytesIO(await response.bytes()), **read_csv_kwargs)


async def load_text(name: str) -> str:
    """Fetch a plain-text file and return its contents as a string.

    `name` is either a file in the shared `/data/` folder, or a full URL to
    a text file somewhere else on the web:

        book = await load_text("pride-and-prejudice.txt")
        page = await load_text("https://example.org/some-page.txt")

    Same shared-folder-or-remote-URL split as `load_csv`, and the same
    reason a remote failure gets an honest message instead of a bare
    traceback — see `load_csv`, just above, for the full explanation.
    """
    from pyodide.http import pyfetch  # pragma: no cover - browser only

    remote = name.startswith("http://") or name.startswith("https://")
    url = name if remote else _data_base + name

    try:
        response = await pyfetch(url)
    except Exception as exc:  # pragma: no cover - browser-only failure path
        if not remote:
            raise
        raise ConnectionError(
            f"Couldn't fetch {name}.\n\n"
            "That file is on another website, and a browser only allows this "
            "page to read it if that site permits it — many do not. Nothing "
            "is wrong with your code.\n\n"
            "What does always work: download the file yourself, then add it "
            "through Files in the Workbench panel, and load it by name "
            "instead."
        ) from exc

    if response.status != 200:
        if remote:
            raise ConnectionError(
                f"{name} returned HTTP {response.status}.\n\n"
                "The address may have changed, or that site may not be "
                "handing this file out any more. Downloading it yourself and "
                "adding it through Files in the Workbench panel always works."
            )
        raise FileNotFoundError(
            f"{name} is not in the shared data folder (HTTP {response.status})"
        )
    return await response.string()


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


def _run_sql_cell(conn, script: str, max_rows: int = 20):
    """dewmini's own SQL cell type (planning/CELL_IDENTITY.md §8) —
    internal plumbing a generated cell call reaches, not something a
    reader is expected to call by name themselves; `run_query()` above
    is the public, one-statement version of the same idea.

    Splits `script` into statements on a bare `;` and runs each in
    turn against `conn` — a script, not a single query, is the normal
    shape of a SQL *cell* (`CREATE TABLE` here, `INSERT` there,
    `SELECT` at the end), where `run_query()` only ever runs one
    statement. Only the *last* statement's own result renders: if it
    returned rows (a `SELECT`), as a table; otherwise, how many rows it
    touched, the way a database console reports a `CREATE`/`INSERT`/
    `UPDATE`/`DELETE`. Every statement commits at the end, same
    friendlier default `run_query()` already made.

    The split is a bare `;`, not a real SQL parser — a semicolon inside
    a string literal would split somewhere it shouldn't. Good enough
    for what a teaching notebook's SQL cell is for; reach for
    `run_query()` directly, one statement at a time, for anything that
    needs to be exact about it.
    """
    import pandas as pd  # noqa: PLC0415

    cell = _require_cell()
    statements = [s.strip() for s in script.split(";") if s.strip()]
    if not statements:
        return None

    for statement in statements[:-1]:
        conn.execute(statement)

    cursor = conn.execute(statements[-1])
    columns = [description[0] for description in cursor.description or []]
    frame = None
    if columns:
        frame = pd.DataFrame(cursor.fetchall(), columns=columns)
        cell.sink.append_html(_table_html(frame, max_rows=max_rows))
    elif cursor.rowcount >= 0:
        noun = "row" if cursor.rowcount == 1 else "rows"
        cell.sink.append_html(f'<pre class="dl-repr">{cursor.rowcount} {noun} affected.</pre>')
    conn.commit()
    return frame


def _query_rows(sql: str, params: list | None = None) -> list[dict]:
    """The Python half of a full-stack cell's own bridge
    (planning/DEWSTACK_MERGE.md §3, §7 phase 4) — internal plumbing an
    app cell's generated JavaScript calls, not something a reader is
    expected to call by name themselves, the same relationship
    `_run_sql_cell()` has to a SQL cell.

    Runs one `SELECT` against the page's own shared `db` connection —
    the same one every `sql exec` cell reads and writes — and returns
    its rows as a list of dicts, column name to value: a plain,
    JSON-safe shape that crosses the worker's postMessage boundary the
    same way `describe_globals()`'s own result does, with no Pyodide
    proxy machinery on the far side. `params` fills in any `?`
    placeholders in `sql`, so a value that came from a reader — typed
    into a search box, say — is bound as one value rather than pasted
    into the query's own text, where a stray quote could change what
    the query does.

    Unlike `_run_sql_cell()`, this needs no `_require_cell()`: an app
    cell's JavaScript calls it directly, outside the normal cell-run
    lifecycle, so there is no cell sink for it to render into and
    nothing here tries to — a bad query's own `sqlite3.Error` is left
    to propagate, for the calling JavaScript to catch and show.
    """
    conn = _page_globals.get("db")
    if conn is None:
        raise RuntimeError(
            "No database connection yet — this page has nothing for a query to run against."
        )
    cursor = conn.execute(sql, params or [])
    columns = [description[0] for description in cursor.description or []]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


_SUMMARY_LIMIT = 80


def _shape_summary(value: object) -> str | None:
    """"3 rows x 2 columns" for a table, "4 values" for a column, "array(2, 2)"
    for an array — or None for anything that is not shaped like those.

    Recognised by the attributes a value actually has rather than by its
    type's module path. The first version of this keyed on
    `(__module__, __name__)` and hardcoded `pandas.core.frame`, which was
    true of the pandas of the day and false in pandas 3, where public
    classes report `__module__ == "pandas"` — so a DataFrame silently fell
    through to printing its whole self into a sidebar. Duck typing cannot
    break that way when a library rearranges its internals.

    Deliberately does not import pandas or numpy to ask: they may not be
    loaded, and describing a namespace should never be the thing that
    drags them in.
    """
    shape = getattr(value, "shape", None)
    if not isinstance(shape, tuple) or not all(isinstance(n, int) for n in shape):
        return None
    if hasattr(value, "columns") and len(shape) == 2:  # a DataFrame, or close enough
        return f"{shape[0]} rows x {shape[1]} columns"
    if hasattr(value, "index") and len(shape) == 1:  # a Series
        return f"{shape[0]} values"
    return f"array{shape}"


def _summarise(value: object) -> str:
    """One short, human-readable line describing a value — its shape for a
    table or an array, its length for a container, and otherwise a truncated
    repr. Every branch is wrapped, because this runs over whatever a student
    happened to define: a repr that raises is a bug in their object, not a
    reason for the whole panel to go blank."""
    try:
        shaped = _shape_summary(value)
    except Exception:
        shaped = None
    if shaped is not None:
        return shaped
    if isinstance(value, (str, bytes)):
        try:
            text = repr(value)
        except Exception:
            return f"{len(value)} characters"
        return text if len(text) <= _SUMMARY_LIMIT else f"{text[:_SUMMARY_LIMIT - 1]}…"
    if isinstance(value, (list, tuple, set, frozenset, dict)):
        size = len(value)
        noun = "key" if isinstance(value, dict) else "item"
        return f"{size} {noun}{'' if size == 1 else 's'}"
    try:
        text = repr(value)
    except Exception:
        return "(cannot be displayed)"
    return text if len(text) <= _SUMMARY_LIMIT else f"{text[:_SUMMARY_LIMIT - 1]}…"


def describe_globals() -> list[dict]:
    """What is currently defined in the shared namespace, as plain data.

    Powers dewmini's variable inspector: a student can see what their code
    actually made, which turns "I ran a cell and something happened" into
    something inspectable. Returns a list of `{name, type, summary, kind}`
    dictionaries — only strings, so the whole result crosses the worker's
    postMessage boundary without any of Pyodide's proxy machinery.

    `kind` separates the three things a namespace holds, so the panel can
    show a student's own data first and keep the furniture out of the way:

      * "data" — what a student's own code made, and what they came to see;
      * "callable" — functions and classes, theirs or ours;
      * "module" — anything imported.

    Names starting with "_" are left out entirely, the same convention
    autocomplete already follows: they are this module's own bookkeeping,
    not anything a reader put there.
    """
    import types  # noqa: PLC0415 - only needed here, and only in this function

    described = []
    for name, value in list(_page_globals.items()):
        if name.startswith("_"):
            continue
        if isinstance(value, types.ModuleType):
            kind = "module"
        elif callable(value):
            kind = "callable"
        else:
            kind = "data"
        described.append({
            "name": name,
            "type": type(value).__name__,
            "summary": _summarise(value),
            "kind": kind,
        })
    described.sort(key=lambda entry: entry["name"].lower())
    return described
