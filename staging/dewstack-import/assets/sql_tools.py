"""dewstack's SQL cell runtime.

A trimmed relative of dewlab's `tutorial_tools.py` (`_run_sql_cell()`):
a dewstack SQL cell never runs arbitrary Python, only SQL, so this needs
none of that file's cell-execution, traceback, or widget machinery —
just enough to turn SQL text into an HTML table. No pandas here: a
plain sqlite3 cursor's columns and rows are enough for a table, and a
page whose only fenced blocks are SQL cells and checks loads only
`sqlite3` alongside core Pyodide (build.py works out which packages a
page needs from what is actually on it; see `render_body()`) — this
file staying pandas-free is what keeps that true. `get_connection()`
is the one door out: `python_tools.py`'s `read_sql()` calls it to pull
one of these tables into a DataFrame, on a page that also uses a
Python cell.

Loaded once per page (assets/sql-cell.js's boot()); every `.dl-sql-cell`
on that page keeps its own named connection here, so two cells sharing a
`db` name see the same tables and rows, and two different names never do.

The `check_*` functions below are the tentacular-plushies quiz's
self-check: each looks at a named connection's tables and returns one
line saying whether a task's requirements are met. They are a check, not
a grade — instant, run only when a reader clicks a button, and nothing
here records who ran one or what it found.
"""

from __future__ import annotations

import html
import sqlite3

_connections: dict[str, sqlite3.Connection] = {}


def _connection(db_name: str) -> sqlite3.Connection:
    if db_name not in _connections:
        _connections[db_name] = sqlite3.connect(":memory:")
    return _connections[db_name]


def get_connection(db_name: str) -> sqlite3.Connection:
    """The public form of `_connection()`, for `python_tools.py`'s
    `read_sql()` — a Python cell reaching into a SQL cell's own table,
    creating the connection fresh if that table has not been built yet."""
    return _connection(db_name)


def query_rows(db_name: str, sql: str, params: list | None = None) -> list[dict]:
    """Runs one SELECT against the named connection and returns its rows
    as a list of dicts, column name to value — the bridge a full-stack
    page's own JavaScript calls directly as `dlQuery()`
    (`assets/sql-cell.js`), the "Pyodide exposes a Python function to
    the page" `CONSOLIDATION_PLAN.md` section 12 describes.

    `params` fills in any `?` placeholders in `sql` — the way a value
    that came from a visitor (typed into a search box, say) belongs in a
    query. Pasting that value directly into the SQL text instead is how
    a stray quote breaks a query, or worse, changes what it does; a
    placeholder holds its place as one value, never as SQL of its own,
    however it is spelled.

    A bad query raises `sqlite3.Error` the same as `run_sql()`'s own
    statements do; unlike `run_sql()`, nothing here renders it as HTML —
    the reader's own JavaScript decides what a failed query looks like
    on the page.
    """
    conn = _connection(db_name)
    cursor = conn.execute(sql, params or [])
    columns = [description[0] for description in cursor.description or []]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def reset(db_name: str) -> None:
    """Closes and drops a named connection, so the next run starts fresh.

    Used by a cell's Reset button: a table created by an earlier run
    would otherwise still exist, and a `CREATE TABLE` a reader runs again
    would fail as a result.
    """
    conn = _connections.pop(db_name, None)
    if conn is not None:
        conn.close()


def _strip_comments(script: str) -> str:
    """Drops a `--` line comment from each line first, so a cell holding
    only an instructional comment — a placeholder before a reader's own
    code, or exercise text copied in above it — runs as nothing rather
    than as literal text sqlite3 cannot execute."""
    return "\n".join(line.split("--", 1)[0] for line in script.splitlines())


def run_sql(db_name: str, script: str, max_rows: int = 50) -> str:
    """Runs a SQL script against the named connection and returns HTML.

    Drops `--` comments, then splits on a bare `;`, the same as dewlab's
    `_run_sql_cell()` and for the same reason: a script, not one
    statement, is the normal shape of a SQL cell (`CREATE TABLE` here,
    `INSERT` there, `SELECT` at the end). Every statement but the last
    just runs; the last statement's
    result is what renders, as a table if it returned rows, otherwise as
    a count of rows affected. Every statement commits, so a `CREATE
    TABLE`/`INSERT` a reader runs is still there on the next run.

    A `sqlite3.Error` (a typo, a missing table) renders as a plain
    message rather than a Python traceback: nothing here runs the
    reader's own Python, so a traceback pointing at this file's own code
    would only confuse.
    """
    conn = _connection(db_name)
    statements = [s.strip() for s in _strip_comments(script).split(";") if s.strip()]
    if not statements:
        return '<p class="dl-sql-note">Nothing to run.</p>'

    try:
        for statement in statements[:-1]:
            conn.execute(statement)
        cursor = conn.execute(statements[-1])
        columns = [description[0] for description in cursor.description or []]
        if columns:
            rows = cursor.fetchmany(max_rows)
            more = cursor.fetchone() is not None
            result = _table_html(columns, rows, max_rows, more)
        else:
            noun = "row" if cursor.rowcount == 1 else "rows"
            result = f'<p class="dl-sql-note">{cursor.rowcount} {noun} affected.</p>'
        conn.commit()
        return result
    except sqlite3.Error as exc:
        return f'<p class="dl-sql-error">{html.escape(str(exc))}</p>'


def _table_columns(conn: sqlite3.Connection, table: str) -> set[str] | None:
    """The column names of `table`, or `None` if it does not exist yet.
    `table` is always one of this file's own hardcoded names, never text
    a reader typed, so building it into a query here is safe."""
    try:
        cursor = conn.execute(f"SELECT * FROM {table} LIMIT 0")
    except sqlite3.Error:
        return None
    return {description[0] for description in cursor.description}


def _check_html(ok: bool, message: str) -> str:
    """One line of self-check feedback: instant, and never sent
    anywhere. A check like this tells a reader whether a task's
    requirements are met; it is not a grade, and nothing here records
    who ran it or what the result was."""
    css_class = "dl-check-pass" if ok else "dl-check-fail"
    icon = "✓" if ok else "✗"
    return f'<p class="{css_class}">{icon} {html.escape(message)}</p>'


def check_products_table(db_name: str) -> str:
    """Task 1: does `products` exist, with the columns the task asks
    for?"""
    columns = _table_columns(_connection(db_name), "products")
    if columns is None:
        return _check_html(False, "There is no products table yet.")
    required = {"id", "product_name", "category", "price", "stock_quantity"}
    missing = required - columns
    if missing:
        return _check_html(False, f"products is missing: {', '.join(sorted(missing))}.")
    return _check_html(True, "products exists, with all the required columns.")


def check_transactions_table(db_name: str) -> str:
    """Task 2: does `transactions` exist, with the columns the task
    asks for? (The foreign key itself isn't checked: sqlite3 only
    enforces one if it was asked to, and this task is about the column
    being there, ready to hold a product's id.)"""
    columns = _table_columns(_connection(db_name), "transactions")
    if columns is None:
        return _check_html(False, "There is no transactions table yet.")
    required = {"id", "product_id", "customer_name", "quantity"}
    missing = required - columns
    if missing:
        return _check_html(False, f"transactions is missing: {', '.join(sorted(missing))}.")
    return _check_html(True, "transactions exists, with all the required columns.")


def check_products_rows(db_name: str) -> str:
    """Task 3: at least four products, across at least three
    categories."""
    conn = _connection(db_name)
    if _table_columns(conn, "products") is None:
        return _check_html(False, "products needs to exist before this check means anything.")
    rows = conn.execute("SELECT category FROM products").fetchall()
    categories = {row[0] for row in rows}
    if len(rows) < 4:
        return _check_html(False, f"products has {len(rows)} row(s); the task asks for at least four.")
    if len(categories) < 3:
        return _check_html(False, f"products uses {len(categories)} category or categories; the task asks for at least three.")
    return _check_html(True, f"products has {len(rows)} rows across {len(categories)} categories.")


def check_transactions_rows(db_name: str) -> str:
    """Task 4: at least three transactions."""
    conn = _connection(db_name)
    if _table_columns(conn, "transactions") is None:
        return _check_html(False, "transactions needs to exist before this check means anything.")
    count = conn.execute("SELECT COUNT(*) FROM transactions").fetchone()[0]
    if count < 3:
        return _check_html(False, f"transactions has {count} row(s); the task asks for at least three.")
    return _check_html(True, f"transactions has {count} rows.")


def check_quiz_queries(db_name: str) -> str:
    """Task 5: the three required queries would each have something to
    return. Not a check of the queries themselves — there's no one
    right way to write a SELECT — but of whether the data underneath
    them can produce a real answer."""
    conn = _connection(db_name)
    if _table_columns(conn, "products") is None or _table_columns(conn, "transactions") is None:
        return _check_html(False, "Both tables are needed before this check means anything.")
    over_30 = conn.execute("SELECT COUNT(*) FROM products WHERE price > 30").fetchone()[0]
    under_15 = conn.execute("SELECT COUNT(*) FROM products WHERE stock_quantity < 15").fetchone()[0]
    problems = []
    if over_30 == 0:
        problems.append("no product has a price over 30, so the first query would return nothing")
    if under_15 == 0:
        problems.append("no product has a stock_quantity under 15, so the second query would return nothing")
    if problems:
        return _check_html(False, "; ".join(problems).capitalize() + ".")
    return _check_html(True, "Both conditions have at least one matching product.")


def _table_html(columns: list[str], rows: list[tuple], max_rows: int, more: bool) -> str:
    head = "".join(f"<th>{html.escape(str(c))}</th>" for c in columns)
    body = "".join(
        "<tr>" + "".join(f"<td>{html.escape('' if v is None else str(v))}</td>" for v in row) + "</tr>"
        for row in rows
    )
    parts = [
        '<div class="dl-sql-result">',
        f"<table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>",
        "</div>",
    ]
    if more:
        parts.append(f'<p class="dl-sql-note">Showing the first {max_rows} rows.</p>')
    return "".join(parts)
