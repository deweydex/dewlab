"""Tests for the later-use lister: it must read only what the author wrote,
or "cell" from every cell's own label would be listed on every page."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "dev"))

import term_uses  # noqa: E402


PAGE = """<main class="dl-page" id="dl-body">
<p>Each loop adds one <em>float</em> to the total.</p>
<div class="dl-cell" data-cell-id="a-1"><div class="dl-cell-head"><span class="dl-cell-pill">
<span class="dl-cell-pill-num">Cell 1</span></span></div>
<pre><code>total = 0.5</code></pre>
<p class="dl-panel-note">GitHub will ask you to sign in.</p></div>
<div class="dl-predict"><p class="dl-predict-prompt">What will the loop print?</p>
<div class="dl-predict-unsure" hidden><p>The first hint under the cell is open now.</p></div></div>
<p>A <span class="dl-math">x^2</span> term, and a <a href="x.html">matrix link</a>.</p>
<br><p>After a break, the list continues.</p>
</main>"""


def test_prose_keeps_the_authors_words():
    words = term_uses.prose(PAGE)
    assert "Each loop adds one" in words
    assert "What will the loop print?" in words
    assert "the list continues" in words


def test_prose_skips_what_the_page_adds_round_them():
    words = term_uses.prose(PAGE)
    for chrome in ("Cell 1", "sign in", "hint under the cell", "total = 0.5"):
        assert chrome not in words
    for skipped in ("float", "x^2", "matrix link"):
        assert skipped not in words


def _page(tmp_path, body, glossary):
    import json
    manifest = json.dumps({"glossary": glossary})
    path = tmp_path / "page.html"
    path.write_text(
        f'<main class="dl-page" id="dl-body">{body}</main>'
        f'<script type="application/json" id="dewlab-manifest">{manifest}</script>'
    )
    return path


EARLIER = {"title": "Earlier", "href": "earlier.html"}


def test_a_longer_term_wins_and_a_capital_is_matched_as_written(tmp_path):
    page = _page(
        tmp_path,
        "<p>We met selection sort, and there is none left over.</p>",
        [
            {"term": "selection", "kind": "concept", "definition": "if/else", "origin": EARLIER},
            {"term": "selection sort", "kind": "concept", "definition": "a sort"},
            {"term": "None", "kind": "concept", "definition": "no value", "origin": EARLIER},
        ],
    )
    assert term_uses.candidates(page) == []


def test_check_reads_a_marked_term(tmp_path):
    page = _page(
        tmp_path,
        '<p>A <em class="term">matrix</em> and an <em class="term">elephant</em>.</p>',
        [{"term": "matrix", "kind": "concept", "definition": "a grid", "origin": EARLIER}],
    )
    assert term_uses.unmatched_marks(page) == ["elephant (names no concept)"]


def test_a_frequent_term_is_marked_only_near_its_start(monkeypatch):
    monkeypatch.setattr(term_uses, "course_orders", lambda: {
        "One": ["intro", "next", "later"],
        "Two": ["later", "other"],
    })
    monkeypatch.setattr(term_uses, "windows", lambda: {
        "One": {"cell": ({"intro", "intro-practice", "next"}, 1.0)},
        "Two": {},
    })
    assert not term_uses.after_its_start("next", "cells")
    assert term_uses.after_its_start("intro-practice", "cell") is False
    assert term_uses.after_its_start("next-practice", "cell")
    # Past the start in One, but Two lists "later" too and marks "cell"
    # everywhere, so the mark stays.
    assert not term_uses.after_its_start("later", "cell")
    # A term no course windows is never past its start.
    assert not term_uses.after_its_start("later", "matrix")
    # Only courses that list the page count.
    assert not term_uses.after_its_start("other", "cell")
