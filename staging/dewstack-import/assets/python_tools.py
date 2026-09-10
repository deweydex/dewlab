"""dewstack's Python/pandas cell runtime.

A trimmed relative of dewlab's `tutorial_tools.py`: dewstack's cells have
no widgets, no `check()` (that is `sql_tools.py`'s separate `check_*`
mechanism), and no notebook-wide state to manage beyond one namespace per
cell name — so this needs only the parts of dewlab's file that turn a
script into rendered output: capturing the last expression's value,
rendering a DataFrame as a table and a matplotlib figure as a PNG, and
catching whatever the script prints or raises. The rendering functions
below (`_figure_html()`, `_table_html()`, `_recolour_for_theme()`) are
ported near verbatim from dewlab's, including its reasoning for each.

Loaded once per page, alongside `sql_tools.py`, only when the page has a
`py cell=` block (build.py's `render_body()` decides this at build time
the same way it decides a page's Pyodide package list). `read_sql()` is
the bridge between the two: it calls `sql_tools.get_connection()` to
pull a SQL cell's own table into a DataFrame, so a page can open a real
dataset in SQL and chart it in the next cell down without an import.
"""

from __future__ import annotations

import base64
import html
import io
import os
import sys

# Force matplotlib's non-interactive backend before it is ever imported,
# for the same reason dewlab's tutorial_tools.py does: there is no window
# for it to open in a browser tab, and importing pyplot first would pick
# a backend that then fails.
os.environ.setdefault("MPLBACKEND", "AGG")

_namespaces: dict[str, dict] = {}


def _namespace(name: str) -> dict:
    if name not in _namespaces:
        _namespaces[name] = {"read_sql": read_sql, "load_csv": load_csv, "download_csv": download_csv}
    return _namespaces[name]


def reset(name: str) -> None:
    """Drops a cell's namespace, so its next run starts with no
    variables and no imports left over from before."""
    _namespaces.pop(name, None)


def read_sql(db_name: str, query: str):
    """A SQL cell's table, or a query against it, as a DataFrame.

    `db_name` is the same name a `` ```sql cell=name `` block on this
    page uses; the connection it built (or an empty one, if this is
    called first) comes from `sql_tools.get_connection()`."""
    import pandas as pd
    import sql_tools

    return pd.read_sql_query(query, sql_tools.get_connection(db_name))


async def load_csv(url: str, **read_csv_kwargs):
    """Fetches a CSV from `url` and returns it as a DataFrame.

    Ported from dewlab's `tutorial_tools.load_csv()`, trimmed to the one
    case dewstack needs: dewstack has no shared `/data/` folder the way
    a dewlab tutorial does, so `url` is always a full address, never a
    filename.

    Plain `pandas.read_csv(url)` fails here with a message that explains
    nothing — `urlopen error unknown url type: https` — because this
    Python runs inside a browser tab with no network connection of its
    own; it has to borrow the browser's, through `pyodide.http.pyfetch`
    rather than the stdlib `urllib` pandas reaches for by default. A
    genuine refusal (the site declining to let another page read it, the
    CORS rule every browser enforces) is rarer than that first failure,
    but gets its own message too, since nothing in a reader's own code
    would explain it either.
    """
    import pandas as pd
    from pyodide.http import pyfetch  # pragma: no cover - browser only

    try:
        response = await pyfetch(url)
    except Exception as exc:  # pragma: no cover - browser-only failure path
        raise ConnectionError(
            f"Couldn't fetch {url}.\n\n"
            "That address is on another website, and a browser only lets "
            "this page read it if that site allows it — most public data "
            "sites do, but not all of them. Nothing is wrong with your "
            "code; try the address in a new tab to check it still exists."
        ) from exc

    if response.status != 200:
        raise ConnectionError(
            f"{url} returned HTTP {response.status}.\n\n"
            "The address may have changed, or that site may not be "
            "handing this file out any more."
        )
    return pd.read_csv(io.BytesIO(await response.bytes()), **read_csv_kwargs)


def download_csv(dataframe, filename: str) -> None:
    """Saves `dataframe` as `filename` on the reader's own computer.

    A query's result leaving the browser needs a real click-and-save,
    the same as a SQL cell's own Download button — there is no folder
    here to write a file into, only the reader's own Downloads. Calling
    this from a cell's own code is what stands in for clicking a
    button: a query built entirely inside the page, exported the moment
    a reader chooses to keep it, the same way `sql-cell.js`'s
    `downloadCell()` saves a cell's text.
    """
    import js  # pragma: no cover - browser only

    csv_text = dataframe.to_csv(index=False)
    blob = js.Blob.new([csv_text])
    url = js.URL.createObjectURL(blob)
    link = js.document.createElement("a")
    link.href = url
    link.download = filename
    js.document.body.appendChild(link)
    link.click()
    link.remove()
    js.URL.revokeObjectURL(url)


def _pandas():
    return sys.modules.get("pandas")


def _is_dataframe(value) -> bool:
    pd = _pandas()
    return pd is not None and isinstance(value, (pd.DataFrame, pd.Series))


def _is_figure(value) -> bool:
    mpl = sys.modules.get("matplotlib.figure")
    return mpl is not None and isinstance(value, mpl.Figure)


# Ported from dewlab's tutorial_tools.py: one neutral grey for a figure's
# chrome, legible against both the light and dark page background (about
# 4.15:1 against each), so a figure drawn before a reader switches theme
# never becomes wrong — the PNG is baked, and it is not worth keeping
# every figure open for the life of the page just to repaint it.
_FIGURE_INK = "#7a7a7a"


def _recolour_for_theme(figure, ink: str) -> None:
    """Repaints a figure's chrome — titles, labels, ticks, spines — in
    `ink`. Only the chrome: the plotted data keeps whatever colours the
    reader's own code chose."""
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
    _recolour_for_theme(figure, _FIGURE_INK)
    buffer = io.BytesIO()
    figure.savefig(buffer, format="png", dpi=110, bbox_inches="tight", transparent=True)
    encoded = base64.b64encode(buffer.getvalue()).decode("ascii")
    return (
        '<div class="dl-figure">'
        f'<img alt="Figure produced by this cell" src="data:image/png;base64,{encoded}">'
        "</div>"
    )


def _table_html(frame, max_rows: int = 20) -> str:
    pd = _pandas()
    total = len(frame)
    truncated = total > max_rows
    shown = frame.head(max_rows) if truncated else frame
    if isinstance(shown, pd.Series):
        shown = shown.to_frame()
    table = shown.to_html(border=0, classes=None, escape=True, na_rep="")
    parts = ['<div class="dl-table-wrap">', table]
    if truncated:
        parts.append(f'<div class="dl-table-note">Showing the first {max_rows} of {total} rows.</div>')
    parts.append("</div>")
    return "".join(parts)


class _Sink:
    """Collects one cell run's output as HTML, ported from dewlab's own
    `_RecordingSink`: consecutive `print()` writes of the same kind
    (stdout, or a traceback on stderr) accumulate into one `<pre>`
    rather than a fresh one per write, so printed text reads as one
    block the way a terminal would show it. A DataFrame, a figure, or
    any other discrete result closes whatever stream was open first, so
    printed text always appears in the order the cell produced it."""

    def __init__(self) -> None:
        self._parts: list[str] = []
        self._stream_class: str | None = None
        self._stream_text = ""
        self.figures_rendered: set[int] = set()

    def stream(self, css_class: str, text: str) -> None:
        if self._stream_class != css_class:
            self.close_stream()
            self._stream_class = css_class
        self._stream_text += text

    def close_stream(self) -> None:
        if self._stream_class is not None:
            self._parts.append(f'<pre class="{self._stream_class}">{html.escape(self._stream_text)}</pre>')
            self._stream_class = None
            self._stream_text = ""

    def append_html(self, markup: str) -> None:
        self.close_stream()
        self._parts.append(markup)

    @property
    def html(self) -> str:
        self.close_stream()
        return "".join(self._parts)


def _render_value(value, sink: _Sink) -> None:
    """Renders one value into the cell's output, the same three rules
    dewlab's `_render_value()` uses: nothing for `None`, a table for a
    DataFrame or Series, a PNG for a figure, `repr` for everything
    else. A figure rendered this way is remembered, so `_flush_figures()`
    does not draw it a second time just because it is still open."""
    if value is None:
        return
    if _is_dataframe(value):
        sink.append_html(_table_html(value))
        return
    if _is_figure(value):
        sink.figures_rendered.add(id(value))
        sink.append_html(_figure_html(value))
        return
    sink.append_html(f'<pre class="dl-repr">{html.escape(repr(value))}</pre>')


def _flush_figures(sink: _Sink) -> None:
    """Renders any figure the cell drew but never returned or showed —
    the common case of `plt.plot(...)` with nothing after it — then
    closes every open figure so the next run starts clean."""
    plt = sys.modules.get("matplotlib.pyplot")
    if plt is None:
        return
    for number in plt.get_fignums():
        figure = plt.figure(number)
        if id(figure) not in sink.figures_rendered:
            sink.append_html(_figure_html(figure))
    plt.close("all")


def _patch_pyplot_show(sink: _Sink) -> None:
    """Makes `plt.show()` render the figures drawn so far, instead of
    matplotlib's own version, which draws nothing under this
    non-interactive backend and warns about a missing canvas. Installed
    fresh on every run, since pyplot may not be imported yet the first
    time a cell calls this."""
    plt = sys.modules.get("matplotlib.pyplot")
    if plt is None:
        return

    def show(*args, **kwargs):
        _flush_figures(sink)

    plt.show = show


class _StreamWriter:
    """Sends `print()` and any traceback text into the cell's own output,
    since there is no terminal in a browser tab for it to go to."""

    def __init__(self, sink: _Sink, css_class: str) -> None:
        self._sink = sink
        self._css_class = css_class

    def write(self, text: str) -> None:
        if text:
            self._sink.stream(self._css_class, text)

    def flush(self) -> None:
        pass


async def run_python(name: str, code: str) -> str:
    """Runs one cell's Python against its named namespace and returns
    the HTML it produced: printed text, the last expression's value (a
    DataFrame as a table, a figure as a PNG, anything else as `repr`),
    and any figure drawn but not otherwise shown. A cell's own error
    renders as its message, not a traceback pointing at this file."""
    from pyodide.code import eval_code_async

    ns = _namespace(name)
    sink = _Sink()
    _patch_pyplot_show(sink)

    old_stdout, old_stderr = sys.stdout, sys.stderr
    sys.stdout = _StreamWriter(sink, "dl-stdout")
    sys.stderr = _StreamWriter(sink, "dl-error")
    try:
        value = await eval_code_async(code, globals=ns)
        _render_value(value, sink)
        _flush_figures(sink)
    except BaseException as exc:  # noqa: BLE001 - a reader's error is normal traffic
        sink.append_html(f'<pre class="dl-error">{html.escape(f"{type(exc).__name__}: {exc}")}</pre>')
    finally:
        sys.stdout, sys.stderr = old_stdout, old_stderr

    return sink.html or '<p class="dl-sql-note">Nothing to show.</p>'
