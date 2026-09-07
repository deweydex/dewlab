# `assets/tutorial_tools.py`, explained

This is the Python file every dewlab cell actually runs against — not
just dewmini's cells, but every tutorial page's too. When a student's
cell calls `show(...)`, `check(...)`, or `text_input(...)`, this is where
those functions live. It also does something a student never calls
directly: it's what actually *runs* a cell's code and turns whatever
happened — printed text, a returned value, an error — into what appears
on the page.

If you're new to reading a file this size, the module's own top
docstring is the best two-paragraph summary; this document is about how
the pieces underneath it fit together.

---

## The big idea: three "sinks," one set of rendering rules

dewlab runs cells in three different situations: in a real browser tab,
inside a Web Worker (a background thread with no direct access to the
page), and — for testing — in plain Python with no browser at all. All
three need output to end up somewhere, but "somewhere" is a completely
different kind of object in each case.

Rather than writing the output-handling logic three times, this file
writes it **once** and hides the difference behind three small classes —
`_DomSink`, `_MessageSink`, and `_RecordingSink` — that all offer the
same four methods: `stream()`, `close_stream()`, `append_html()`, and
`clear()`. Every rendering function in this file (`_render_value`,
`show`, `check`, the widgets) calls `cell.sink.append_html(...)` or
similar without ever checking which kind of sink it has. This pattern —
several unrelated classes sharing the same method names so calling code
doesn't need to know which one it has — is called "duck typing" in
Python, and it's the single idea that makes the rest of this file make
sense.

---

## Reading order

1. **The module docstring** — what this file is for, in the author's own
   words, plus where its design comes from (`planning/DECISIONS.md`,
   `DECISIONS_LOG.md`).
2. **Environment** — `IN_BROWSER`, the try/except that decides whether
   `js` and `pyodide.ffi` are actually available, since this file also
   has to work under plain CPython for the test suite.
3. **Output sinks** — the three classes described above.
4. **Cell state** — `_CellContext` (everything true about one cell while
   it's running), the module-level `_current` cell, `_page_globals` (the
   one namespace every cell on a page shares), and `_StreamWriter` (how
   `print()` gets redirected into a cell's output).
5. **Value rendering** — `_render_value` and everything it depends on:
   detecting a DataFrame, a matplotlib figure, or a plotting "artist," and
   turning each into the right kind of HTML.
6. **Errors** — `cell_filename`, `_register_source`, `_format_exception`,
   `_chained`: how a traceback gets trimmed down to just the student's
   own code.
7. **Cell lifecycle** — `_begin`, `_end`, and `run_cell`, which ties
   everything above together into "run this code and render what it
   did."
8. **Public output functions** — `show`, `show_table`.
9. **`check()`** — `_compare` (the actual comparison logic) and
   `_check_html` (turning the result into markup).
10. **Widgets** — `text_input`, `dropdown`, `button`, `image_input`, and
    the shared machinery behind them (`_widget_id`, `_Widget`,
    `_mount_widget`, `_require_dom_sink`).
11. **Shared data** — `load_csv`, `load_text`, and `run_query`; `load_text`
    sits right after `load_csv` and fetches the same way (the shared
    `/data/` folder, or a full URL), returning the file's contents as a
    plain string instead of a parsed DataFrame. Right after `run_query`
    sits `_run_sql_cell` (not in `__all__` — internal plumbing, not
    something a reader calls by name), `run_query`'s multi-statement
    counterpart: dewmini's own SQL cell type (DECISIONS_LOG.md 7.118,
    `planning/CELL_IDENTITY.md` §8) generates a call to this rather than
    handing a reader's raw SQL to Pyodide directly. Splits a script on a
    bare `;`, runs every statement but the last, and renders only the
    last one's own result — a table if it returned rows, otherwise how
    many rows it touched.

---

## Two patterns worth understanding on their own

**Swapping out `sys.stdout`.** `print()` doesn't know anything about
cells — it just writes to whatever object Python currently considers
"standard output." `_begin()` takes advantage of that: right before a
cell runs, it replaces `sys.stdout` (and `sys.stderr`) with a
`_StreamWriter`, a small object that looks enough like a file to satisfy
`print()`, but actually appends the text into that cell's own output
area. `_end()` always puts the real `sys.stdout` back afterward — this
matters, because if it didn't, the *next* thing that tried to print
(another cell, or dewlab's own code) would end up writing into a cell
that had already finished.

**Binding a closure's variables early.** Several widget functions build a
JavaScript event handler as a small Python function defined right there,
e.g. `_mount_widget`'s `on_change`. Giving it default-argument values
like `_cell=cell_id` (instead of using `cell_id` directly inside the
function body) is a deliberate trick: it locks in the *current* value of
`cell_id` at the moment the function is created. Without it, if several
widgets get created in a row, every one of their event handlers would
share the same `cell_id` variable — and by the time the student actually
clicks something, that variable might have moved on to a different
widget entirely. `_mount_widget`'s own comment walks through this in
more detail; it's worth reading once, since the same shape shows up in
`button()` and `image_input()` too.

---

## Where to look for something specific

- **"Why did my print statement show up in red?"** — `_StreamWriter` is
  created with a CSS class (`"dl-stdout"` or `"dl-error"`); `_begin()`
  wires `sys.stderr` to the error one, so anything a library itself
  writes to stderr (not just exceptions) renders with error styling.
- **"How does dewlab decide a traceback is 'done'?"** — `_format_exception`
  and `_chained`. Only frames whose filename starts with `"<cell "` (see
  `cell_filename`) are kept; dewlab's own frames are always dropped.
- **"Why does `check()` need its own comparison function instead of
  `==`?"** — `_compare`, and its own docstring: floats need a tolerance,
  numpy arrays and DataFrames raise on a bare `==`, and `True == 1` in
  Python would let a boolean answer through disguised as a numeric one.
- **"What does the page learn about a run beyond its output?"** —
  `run_cell_report()` and `_report()`: the same run as `run_cell()`, plus a
  JSON report of whether it raised (`_describe_error()`: type and first
  line), whether its `check()` calls passed and which did not, and whether
  the cell's `expect:` expression `holds()` in the page namespace. The
  tutorial page counts attempts for staged hints from this
  (planning/CELL_HINTS.md); `run_cell()` keeps its boolean for dewmini.
- **"Why is `image_input()`'s value `None` at first?"** — reading a
  picked file's bytes is asynchronous; see the comment on `on_change`
  inside `image_input()` for how `asyncio.ensure_future` fits in.
- **"What happens if a widget is used in a Worker-run tutorial page?"**
  — `_require_dom_sink` raises a clear error instead of silently doing
  nothing; see its own comment and `DECISIONS_LOG.md` 7.77 for why
  widgets need a real page to attach to.
