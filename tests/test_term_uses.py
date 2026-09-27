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
