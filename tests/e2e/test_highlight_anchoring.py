"""planning/HIGHLIGHTS_AND_NOTES.md §3: the anchoring lookup that will let a
highlight survive a tutorial's prose being edited later, tested here on its
own before anything in the page calls it (rollout sketch, step 2).

PARA-ONE deliberately repeats "the pivot" so the disambiguation path (an
exact match on the surrounding text, not just the quote itself) actually
gets exercised rather than assumed."""

from __future__ import annotations

import functools
import http.server
import socketserver
import sys
import threading
from pathlib import Path

import pytest

DEWLAB = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(DEWLAB))

import build as b  # noqa: E402

MODULE = "anchor-fixtures"
SLUG = "one"

FRONTMATTER = """---
title: "Anchor Fixture"
slug: one
module: anchor-fixtures
module_title: "Anchor Fixtures"
year: "2026-2027"
series: sample-series
version: 2026.08.23.1
---

# Anchor Fixture

PARA-ZERO plain filler text to open the page.

PARA-ONE mentions the pivot only works here, and later PARA-ONE mentions the pivot again in the same paragraph.

PARA-TWO is a short filler paragraph.

PARA-THREE is the target passage the reader wants to keep marked forever in this test.

PARA-FOUR filler.

PARA-FIVE filler.

PARA-SIX filler.

PARA-SEVEN filler.

PARA-EIGHT filler.

PARA-NINE filler.

```python exec
id: plain-cell
1 + 1
```
"""

# Blocks as build.py renders them: index 0 is the title H1, then one
# paragraph per index in source order (there is only one heading, so
# render_toc() adds no contents list to compete for indices).
TARGET_BLOCK = 4  # "PARA-THREE is the target passage..."
REPEATED_BLOCK = 2  # "PARA-ONE mentions the pivot..." (twice)


@pytest.fixture()
def site(tmp_path, monkeypatch):
    (tmp_path / "tutorials" / MODULE).mkdir(parents=True)
    (tmp_path / "tutorials" / MODULE / f"{SLUG}.md").write_text(FRONTMATTER)
    (tmp_path / "tutorials" / MODULE / "sample-series.order.yaml").write_text(
        "series: Sample Series\norder:\n  - one\n"
    )
    monkeypatch.setattr(b, "ROOT", tmp_path)
    monkeypatch.setattr(b, "TUTORIALS", tmp_path / "tutorials")
    monkeypatch.setattr(b, "OUT", tmp_path / "site")
    monkeypatch.setattr(b, "SETUP", DEWLAB / "setup")
    monkeypatch.setattr(b, "DATA", DEWLAB / "data")
    monkeypatch.setattr(b, "ASSETS", DEWLAB / "assets")
    monkeypatch.setattr(b, "SHELL", DEWLAB / "assets" / "shell.html")
    b.build()
    return tmp_path


def _serve(out_dir: Path):
    handler = functools.partial(_QuietHandler, directory=str(out_dir))
    server = socketserver.TCPServer(("127.0.0.1", 0), handler)
    port = server.server_address[1]
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server, thread, f"http://127.0.0.1:{port}"


class _QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


@pytest.fixture()
def site_url(site):
    server, thread, url = _serve(site / "site")
    try:
        yield url
    finally:
        server.shutdown()
        thread.join(timeout=5)


@pytest.fixture()
def page(browser, site_url):
    context = browser.new_context()
    dl_page = context.new_page()
    dl_page.goto(f"{site_url}/tutorials/{MODULE}/{SLUG}.html")
    dl_page.wait_for_function("() => !!globalThis.dewlab")
    yield dl_page
    context.close()


def _quote_within(page, block_index: int, quote: str, occurrence: int = 0) -> dict:
    """The {block_index, quote, prefix, suffix} anchor describeQuote() would
    have produced for the `occurrence`-th appearance of `quote` in that
    block's own text — found here with indexOf() rather than hardcoding an
    offset the fixture text would silently drift out of sync with."""
    return page.evaluate(
        """([blockIndex, quote, occurrence]) => {
            const block = dewlab.proseBlocks()[blockIndex];
            const text = block.textContent;
            let start = -1;
            for (let i = 0, from = 0; i <= occurrence; i++) {
                start = text.indexOf(quote, from);
                from = start + 1;
            }
            const described = dewlab.describeQuote(block, start, start + quote.length);
            return { block_index: blockIndex, ...described };
        }""",
        [block_index, quote, occurrence],
    )


class TestProseBlocks:
    def test_lists_the_fixtures_paragraphs_in_reading_order(self, page):
        texts = page.evaluate("dewlab.proseBlocks().map((el) => el.textContent.trim())")
        assert texts[0] == "Anchor Fixture"
        assert texts[1].startswith("PARA-ZERO")
        assert texts[TARGET_BLOCK].startswith("PARA-THREE")
        # The H1, ten paragraphs, then three more blocks that only appear
        # once a page has a cell: the (hidden) report-a-problem paragraph
        # (planning/feedback.yaml `enabled: true`) and the "Try something
        # of your own" heading/paragraph PRACTICE.md adds below the last
        # cell. Both are real, readable prose -- correctly not excluded,
        # since neither lives inside `.dl-editor`/`.dl-output`.
        assert len(texts) == 14

    def test_excludes_a_cells_own_output(self, page):
        # A cell's output is only ever filled in by running Python, which
        # this test doesn't need Pyodide for -- injecting the same shape of
        # markup show_table() would produce is enough to prove the
        # exclusion, without paying for a real boot.
        page.evaluate(
            """() => {
                document.querySelector('[data-cell-id="plain-cell"] .dl-output')
                    .innerHTML = "<p>THE-STOWAWAY should never be treated as prose.</p>";
            }"""
        )
        texts = page.evaluate("dewlab.proseBlocks().map((el) => el.textContent)")
        assert not any("THE-STOWAWAY" in text for text in texts)


class TestLocateHighlightAnchor:
    def test_finds_an_untouched_highlight_in_its_own_block(self, page):
        anchor = _quote_within(
            page, TARGET_BLOCK, "the target passage the reader wants to keep marked forever"
        )
        found = page.evaluate(
            "(anchor) => { const r = dewlab.locateHighlightAnchor(anchor); "
            "return r && { text: r.block.textContent.trim(), index: r.index }; }",
            anchor,
        )
        expected_index = page.evaluate(
            "(a) => dewlab.proseBlocks()[a.block_index].textContent.indexOf(a.quote)", anchor
        )
        assert found is not None
        assert found["text"].startswith("PARA-THREE")
        assert found["index"] == expected_index

    def test_disambiguates_the_first_of_two_identical_phrases(self, page):
        # "the pivot" itself appears twice in REPEATED_BLOCK -- this is the
        # actual ambiguous case findQuoteInBlockText() has to resolve by
        # context, unlike the two tests above where the quote text happened
        # to be unique even though the paragraph mentions "the pivot" twice.
        anchor = _quote_within(page, REPEATED_BLOCK, "the pivot", occurrence=0)
        found = page.evaluate(
            "(anchor) => { const r = dewlab.locateHighlightAnchor(anchor); "
            "return r && r.index; }",
            anchor,
        )
        expected = page.evaluate(
            "(a) => dewlab.proseBlocks()[a.block_index].textContent.indexOf(a.quote)",
            anchor,
        )
        assert found == expected

    def test_disambiguates_the_second_of_two_identical_phrases(self, page):
        anchor = _quote_within(page, REPEATED_BLOCK, "the pivot", occurrence=1)
        found = page.evaluate(
            "(anchor) => { const r = dewlab.locateHighlightAnchor(anchor); "
            "return r && r.index; }",
            anchor,
        )
        expected_second = page.evaluate(
            "(a) => dewlab.proseBlocks()[a.block_index].textContent.lastIndexOf(a.quote)",
            anchor,
        )
        expected_first = page.evaluate(
            "(a) => dewlab.proseBlocks()[a.block_index].textContent.indexOf(a.quote)", anchor
        )
        assert found == expected_second
        assert found != expected_first

    def test_follows_a_highlight_after_a_paragraph_is_inserted_above_it(self, page):
        anchor = _quote_within(
            page, TARGET_BLOCK, "the target passage the reader wants to keep marked forever"
        )
        # Shifts PARA-THREE from index 4 to 6 -- still inside the +/-5
        # search window the stale block_index=4 anchor carries.
        page.evaluate(
            """() => {
                const target = dewlab.proseBlocks()[%d];
                for (let i = 0; i < 2; i++) {
                    const p = document.createElement("p");
                    p.textContent = "INSERTED-" + i + " filler paragraph.";
                    target.parentNode.insertBefore(p, target);
                }
            }""" % TARGET_BLOCK
        )
        assert page.evaluate("dewlab.proseBlocks()[6].textContent.trim()").startswith(
            "PARA-THREE"
        )
        found = page.evaluate(
            "(anchor) => { const r = dewlab.locateHighlightAnchor(anchor); "
            "return r && r.block.textContent.trim(); }",
            anchor,
        )
        assert found is not None
        assert found.startswith("PARA-THREE")

    def test_gives_up_once_the_move_is_bigger_than_the_search_window(self, page):
        anchor = _quote_within(
            page, TARGET_BLOCK, "the target passage the reader wants to keep marked forever"
        )
        # Six new paragraphs push PARA-THREE from index 4 to 10 -- one past
        # the +/-5 window the stale anchor's block_index=4 covers (up to 9).
        page.evaluate(
            """() => {
                const target = dewlab.proseBlocks()[%d];
                for (let i = 0; i < 6; i++) {
                    const p = document.createElement("p");
                    p.textContent = "INSERTED-" + i + " filler paragraph.";
                    target.parentNode.insertBefore(p, target);
                }
            }""" % TARGET_BLOCK
        )
        found = page.evaluate("(anchor) => dewlab.locateHighlightAnchor(anchor)", anchor)
        assert found is None

    def test_gives_up_when_the_quote_itself_is_gone(self, page):
        anchor = _quote_within(
            page, TARGET_BLOCK, "the target passage the reader wants to keep marked forever"
        )
        page.evaluate(
            "() => { dewlab.proseBlocks()[%d].textContent = 'Completely rewritten.'; }"
            % TARGET_BLOCK
        )
        found = page.evaluate("(anchor) => dewlab.locateHighlightAnchor(anchor)", anchor)
        assert found is None
