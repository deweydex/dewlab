#!/usr/bin/env python3
"""Phase 0 scaffolding: render the shell template by hand.

build.py does not exist yet — it is Phase 1 — but Phase 0 has to prove that the
shell template, the shared assets and the execution path actually work
together. This script fills the shell's tokens with a fixed set of cells chosen
to exercise every branch of the output renderer, and writes the result to
dev/harness/.

It is a test fixture, not a preview tool. When build.py lands it replaces this
entirely; the cell markup below is the contract build.py has to emit.

    python3 dev/make_harness.py
    python3 -m http.server -d dev/harness 8000
"""

from __future__ import annotations

import html
import json
import shutil
import textwrap
from pathlib import Path

DEWLAB = Path(__file__).resolve().parent.parent
OUT = DEWLAB / "dev" / "harness"

# (id, hint, code). Between them these cover every path in _render_value,
# _flush_figures, _format_exception and the widget bridge.
CELLS: list[tuple[str, str | None, str]] = [
    (
        "plain-python",
        None,
        textwrap.dedent(
            """
            # Printed text and the value of the last expression both show up.
            for n in range(3):
                print("counting:", n)

            2 ** 10
            """
        ).strip(),
    ),
    (
        "numpy-basics",
        "Arrays behave like a whole column at once, not one number at a time.",
        textwrap.dedent(
            """
            import numpy as np

            readings = np.array([12.5, 13.0, 11.75, 14.25])
            print("mean:", readings.mean())
            readings * 2
            """
        ).strip(),
    ),
    (
        "pandas-table",
        None,
        textwrap.dedent(
            """
            import pandas as pd

            df = pd.DataFrame({
                "country": ["Ireland", "Spain", "Japan", "Kenya"],
                "life_expectancy": [82.4, 83.2, 84.8, 66.7],
            })
            df[df["life_expectancy"] > 75]
            """
        ).strip(),
    ),
    (
        "matplotlib-figure",
        None,
        textwrap.dedent(
            """
            import matplotlib.pyplot as plt
            import numpy as np

            x = np.linspace(0, 2 * np.pi, 200)
            plt.plot(x, np.sin(x))
            plt.title("One period of sin(x)")
            """
        ).strip(),
    ),
    (
        "error-traceback",
        None,
        textwrap.dedent(
            """
            # A mistake should point at the student's own line,
            # not at dewlab's plumbing.
            total = 0
            for value in [1, 2, "three"]:
                total += value
            """
        ).strip(),
    ),
    (
        "tools-show-check",
        "check() is feedback, not a mark. Nothing is recorded.",
        textwrap.dedent(
            """
            show("show() renders anything, mid-cell.")
            show_table(df, max_rows=3, caption="First three rows")

            check(sum([1, 2, 3]), 6, label="Does the total come out right?")
            check(0.1 + 0.2, 0.3)          # floats compare within a tolerance
            check(2 + 2, 5)                # and a wrong answer says so
            """
        ).strip(),
    ),
    (
        "tools-widgets",
        None,
        textwrap.dedent(
            """
            name = text_input("Your name", value="")
            units = dropdown("Units", ["metric", "imperial"])

            def greet():
                print(f"Hello {name.value or 'there'} — using {units.value} units.")

            button("Say hello", on_click=greet)
            """
        ).strip(),
    ),
]

PROSE = {
    "plain-python": (
        "<h2>Running code</h2>"
        "<p>Every cell below is live. Edit it, press <strong>Run</strong> (or "
        "Ctrl-Enter), and the output appears directly underneath — the same "
        "prose, cell, output rhythm every dewlab tutorial follows.</p>"
    ),
    "numpy-basics": "<h2>numpy</h2><p>Whole arrays at once.</p>",
    "pandas-table": "<h2>pandas</h2><p>A DataFrame renders as a table.</p>",
    "matplotlib-figure": "<h2>matplotlib</h2><p>A figure renders as an image.</p>",
    "error-traceback": "<h2>When it goes wrong</h2><p>Errors are part of the lesson.</p>",
    "tools-show-check": "<h2>Checking your own answer</h2>",
    "tools-widgets": "<h2>Widgets</h2><p>Type something, then press the button.</p>",
}


def render_cell(cell_id: str, hint: str | None) -> str:
    """The markup contract build.py has to emit for an `exec` fence."""
    safe_id = html.escape(cell_id, quote=True)
    hint_markup = ""
    if hint:
        hint_markup = (
            '<span class="dl-hint">'
            f'<button type="button" class="dl-hint-icon" aria-label="Hint for {safe_id}">?</button>'
            f'<span class="dl-hint-text" role="tooltip">{html.escape(hint)}</span>'
            "</span>"
        )
    return (
        f'<div class="dl-cell" data-cell-id="{safe_id}">'
        '<div class="dl-cell-bar">'
        f'<span class="dl-cell-id">{safe_id}</span>'
        '<span class="dl-cell-spacer"></span>'
        f"{hint_markup}"
        '<button type="button" class="dl-btn dl-btn-reset">reset</button>'
        '<button type="button" class="dl-btn dl-btn-run" disabled>…</button>'
        "</div>"
        '<div class="dl-editor"></div>'
        '<div class="dl-output"></div>'
        "</div>"
    )


def main() -> None:
    shell = (DEWLAB / "assets" / "shell.html").read_text()

    body = "\n".join(
        PROSE.get(cell_id, "") + render_cell(cell_id, hint) for cell_id, hint, _ in CELLS
    )

    manifest = {
        "slug": "phase0-harness",
        "version": 1,
        "assetBase": "assets/",
        "dataBase": "data/",
        "cells": [{"id": cid, "hint": hint, "code": code} for cid, hint, code in CELLS],
    }

    page = shell
    for token, value in {
        "{{TITLE}}": "Phase 0 harness",
        "{{VERSION}}": "1",
        "{{SLUG}}": "phase0-harness",
        "{{MODULE}}": "computational-methods",
        "{{YEAR}}": "2026-2027",
        "{{SERIES}}": "phase0",
        "{{ASSET_BASE}}": "assets/",
        "{{ROOT_BASE}}": "",
        "{{NAV_PREV_NEXT}}": "",
        "{{BODY}}": body,
        # `<` escaped so no value can close the surrounding <script> element.
        "{{MANIFEST_JSON}}": json.dumps(manifest).replace("<", "\\u003c"),
    }.items():
        page = page.replace(token, value)

    if "{{" in page:
        leftover = sorted({p.split("}}")[0] + "}}" for p in page.split("{{")[1:]})
        raise SystemExit(f"shell template has tokens this script does not fill: {leftover}")

    OUT.mkdir(parents=True, exist_ok=True)
    shutil.rmtree(OUT / "assets", ignore_errors=True)
    shutil.copytree(DEWLAB / "assets", OUT / "assets")
    (OUT / "index.html").write_text(page)
    print(f"wrote {OUT / 'index.html'} ({len(CELLS)} cells)")


if __name__ == "__main__":
    main()
