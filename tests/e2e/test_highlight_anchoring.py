"""The anchoring lookup that will let a highlight survive a tutorial's
prose being edited later, tested here on its own before anything in
the page calls it (rollout sketch, step 2).

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
from layout import write_course, write_tutorial  # noqa: E402

COURSE = "anchor-fixtures"
SLUG = "one"

FRONTMATTER = """---
title: "Anchor Fixture"
year: "2026-2027"
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
    (tmp_path / "tutorials").mkdir(parents=True)
    write_tutorial(tmp_path, SLUG, FRONTMATTER)
    write_course(tmp_path, COURSE, "Sample Series", ["one"])
    monkeypatch.setattr(b, "ROOT", tmp_path)
    monkeypatch.setattr(b, "TUTORIALS", tmp_path / "tutorials")
    monkeypatch.setattr(b, "COURSES", tmp_path / "courses")
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
    dl_page.goto(f"{site_url}/tutorials/{SLUG}.html")
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
        # The H1, ten paragraphs, then four more blocks that only appear
        # once a page has a cell: the (hidden) report-a-problem paragraph
        # (planning/feedback.yaml `enabled: true`) and its GitHub
        # sign-in note, and the "Try something of your own"
        # heading/paragraph a reader's own practice cell adds below the
        # last cell. All are
        # real, readable prose -- correctly not excluded, since none
        # lives inside `.dl-editor`/`.dl-output`.
        assert len(texts) == 15

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
    @pytest.mark.parametrize(
        "block_index, quote, occurrence",
        [
            pytest.param(
                TARGET_BLOCK,
                "the target passage the reader wants to keep marked forever",
                0,
                id="unique_quote",
            ),
            # "the pivot" itself appears twice in REPEATED_BLOCK -- these two
            # are the actual ambiguous case findQuoteInBlockText() has to
            # resolve by context, unlike the unique-quote case above where
            # the quote text happened to be unique even though the paragraph
            # mentions "the pivot" twice.
            pytest.param(REPEATED_BLOCK, "the pivot", 0, id="first_of_two_identical"),
            pytest.param(REPEATED_BLOCK, "the pivot", 1, id="second_of_two_identical"),
        ],
    )
    def test_locates_the_anchor_at_the_right_occurrence(
        self, page, block_index, quote, occurrence
    ):
        anchor = _quote_within(page, block_index, quote, occurrence)
        found = page.evaluate(
            "(anchor) => { const r = dewlab.locateHighlightAnchor(anchor); "
            "return r && r.index; }",
            anchor,
        )
        # Recomputed the same way _quote_within() found the occurrence-th
        # match in the first place, rather than hardcoding an offset.
        expected = page.evaluate(
            """([blockIndex, quote, occurrence]) => {
                const text = dewlab.proseBlocks()[blockIndex].textContent;
                let start = -1;
                for (let i = 0, from = 0; i <= occurrence; i++) {
                    start = text.indexOf(quote, from);
                    from = start + 1;
                }
                return start;
            }""",
            [block_index, quote, occurrence],
        )
        assert found == expected

    def test_search_window_follows_a_moved_paragraph_until_the_move_is_too_big(self, page):
        anchor = _quote_within(
            page, TARGET_BLOCK, "the target passage the reader wants to keep marked forever"
        )

        def _insert_before_target(count, start_at):
            page.evaluate(
                """([count, startAt]) => {
                    const target = dewlab.proseBlocks().find(
                        (el) => el.textContent.startsWith("PARA-THREE")
                    );
                    for (let i = 0; i < count; i++) {
                        const p = document.createElement("p");
                        p.textContent = "INSERTED-" + (startAt + i) + " filler paragraph.";
                        target.parentNode.insertBefore(p, target);
                    }
                }""",
                [count, start_at],
            )

        # Two inserted paragraphs shift PARA-THREE from index 4 to 6 -- still
        # inside the +/-5 search window the stale block_index=4 anchor
        # carries.
        _insert_before_target(2, start_at=0)
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

        # Four more paragraphs (six total) push PARA-THREE to index 10 --
        # one past the +/-5 window the stale anchor's block_index=4 covers
        # (up to 9).
        _insert_before_target(4, start_at=2)
        assert page.evaluate("dewlab.proseBlocks()[10].textContent.trim()").startswith(
            "PARA-THREE"
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
