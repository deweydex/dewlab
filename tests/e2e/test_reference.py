"""The reference panel, in a real browser — planning/REFERENCE_PANEL.md.

A dedicated, tiny site build rather than the shared rendering-tour fixture
the rest of tests/e2e/ uses: this needs its own glossary files and series
order. It also needs no self-hosted Pyodide and none of the wait that comes
with one — every fixture tutorial here is prose-only, and
tutorial-runtime.js's own boot() skips loading Pyodide entirely when a page
has no cells (CONTENT_AND_FILE_ARCHITECTURE.md) — so unlike most of this
directory, this file runs without `python3 dev/fetch_pyodide.py` first.

    python3 -m pytest tests/e2e/test_reference.py -q
"""

from __future__ import annotations

import functools
import http.server
import socketserver
import sys
import threading
from pathlib import Path

import pytest
import yaml

DEWLAB = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(DEWLAB))

import build as b  # noqa: E402

MODULE = "reference-fixtures"

FRONTMATTER = """---
title: "{title}"
slug: {slug}
module: reference-fixtures
module_title: "Reference Fixtures"
year: "2026-2027"
series: sample-series
version: 2026.08.23.1
---

# {title}

Some prose. Nothing here is a cell, on purpose — this file's own fixtures
never boot Pyodide.
"""


def _tutorial(root: Path, slug: str, title: str = "A Title") -> None:
    path = root / "tutorials" / MODULE / f"{slug}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(FRONTMATTER.format(title=title, slug=slug))


def _glossary(root: Path, slug: str, entries: list[dict]) -> None:
    path = root / "tutorials" / MODULE / f"{slug}.glossary.yaml"
    path.write_text(yaml.dump({"entries": entries}))


NOTE_FRONTMATTER = """---
title: "{title}"
slug: {slug}
module: reference-fixtures
module_title: "Reference Fixtures"
year: "2026-2027"
series: sample-series
version: 2026.08.23.1
---

# {title}

<aside class="dl-note" id="{note_id}">

{note_body}

</aside>

Some prose after the note.
"""


def _tutorial_with_note(root: Path, slug: str, note_id: str, note_body: str,
                         title: str = "A Title") -> None:
    path = root / "tutorials" / MODULE / f"{slug}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(NOTE_FRONTMATTER.format(
        title=title, slug=slug, note_id=note_id, note_body=note_body))


DATASET_FRONTMATTER = """---
title: "{title}"
slug: {slug}
module: reference-fixtures
module_title: "Reference Fixtures"
year: "2026-2027"
series: sample-series
version: 2026.08.23.1
datasets:
  - {dataset_name}
---

# {title}

Some prose. Nothing here is a cell, on purpose.
"""


def _tutorial_with_dataset(root: Path, slug: str, dataset_name: str,
                            title: str = "A Title") -> None:
    path = root / "tutorials" / MODULE / f"{slug}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(DATASET_FRONTMATTER.format(
        title=title, slug=slug, dataset_name=dataset_name))


def _dataset_files(data_dir: Path, name: str, source: str = "Some source",
                    license: str = "CC0", description: str = "A dataset.") -> None:
    data_dir.mkdir(parents=True, exist_ok=True)
    (data_dir / f"{name}.csv").write_text("a,b\n1,2\n")
    (data_dir / f"{name}.yaml").write_text(
        f'source: "{source}"\nlicense: "{license}"\ndescription: "{description}"\n'
    )


def _set_order(root: Path, slugs: list[str]) -> None:
    path = root / "tutorials" / MODULE / "sample-series.order.yaml"
    path.write_text("series: Sample Series\norder:\n" + "".join(f"  - {s}\n" for s in slugs))


@pytest.fixture()
def site(tmp_path, monkeypatch):
    """A real build, real assets, isolated content — ROOT/TUTORIALS/OUT move
    to tmp_path; ASSETS/SHELL/SETUP/DATA stay pointed at the real repository,
    read-only, so the page that loads is running the actual runtime and CSS
    rather than a stand-in for them."""
    (tmp_path / "tutorials" / MODULE).mkdir(parents=True)
    monkeypatch.setattr(b, "ROOT", tmp_path)
    monkeypatch.setattr(b, "TUTORIALS", tmp_path / "tutorials")
    monkeypatch.setattr(b, "OUT", tmp_path / "site")
    monkeypatch.setattr(b, "SETUP", DEWLAB / "setup")
    monkeypatch.setattr(b, "DATA", DEWLAB / "data")
    monkeypatch.setattr(b, "ASSETS", DEWLAB / "assets")
    monkeypatch.setattr(b, "SHELL", DEWLAB / "assets" / "shell.html")
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
def base_url(site):
    server, thread, url = _serve(site / "site")
    try:
        yield url
    finally:
        server.shutdown()
        thread.join(timeout=5)


CONCEPT = {"term": "x", "kind": "concept", "definition": "The first thing."}
FUNCTION = {"term": "f()", "kind": "function", "definition": "Does a thing.", "example": "f(1)"}


class TestVisibility:
    def test_no_glossary_anywhere_in_the_series_hides_the_toggle(self, site, browser, base_url):
        _tutorial(site, "one", "One")
        _set_order(site, ["one"])
        b.build()
        context = browser.new_context()
        page = context.new_page()
        page.goto(f"{base_url}/tutorials/{MODULE}/one.html")
        assert page.is_hidden("#dl-reference-toggle")
        context.close()

    def test_a_tutorial_with_something_accumulated_shows_the_toggle(self, site, browser, base_url):
        _tutorial(site, "one", "One")
        _glossary(site, "one", [CONCEPT])
        _set_order(site, ["one"])
        b.build()
        context = browser.new_context()
        page = context.new_page()
        page.goto(f"{base_url}/tutorials/{MODULE}/one.html")
        assert page.is_visible("#dl-reference-toggle")
        context.close()


class TestOpeningAndClosing:
    def open_page(self, site, browser, base_url, slug="two"):
        _tutorial(site, "one", "One")
        _tutorial(site, "two", "Two")
        _glossary(site, "one", [CONCEPT])
        _glossary(site, "two", [FUNCTION])
        _set_order(site, ["one", "two"])
        b.build()
        context = browser.new_context()
        page = context.new_page()
        page.goto(f"{base_url}/tutorials/{MODULE}/{slug}.html")
        return context, page

    def test_the_panel_is_closed_by_default(self, site, browser, base_url):
        context, page = self.open_page(site, browser, base_url)
        assert page.is_hidden("#dl-reference")
        context.close()

    def test_clicking_the_toggle_opens_it(self, site, browser, base_url):
        context, page = self.open_page(site, browser, base_url)
        page.click("#dl-reference-toggle")
        assert page.is_visible("#dl-reference")
        context.close()

    def test_escape_closes_it(self, site, browser, base_url):
        context, page = self.open_page(site, browser, base_url)
        page.click("#dl-reference-toggle")
        page.keyboard.press("Escape")
        assert page.is_hidden("#dl-reference")
        context.close()

    def test_the_close_button_closes_it(self, site, browser, base_url):
        context, page = self.open_page(site, browser, base_url)
        page.click("#dl-reference-toggle")
        page.click("#dl-reference-close")
        assert page.is_hidden("#dl-reference")
        context.close()

    def test_clicking_outside_closes_it(self, site, browser, base_url):
        context, page = self.open_page(site, browser, base_url)
        page.click("#dl-reference-toggle")
        page.click("main#dl-body")
        assert page.is_hidden("#dl-reference")
        context.close()

    def test_opening_the_reference_does_not_close_settings(self, site, browser, base_url):
        # Settings is right-anchored; the reference panel is left-anchored
        # (tutorial-style.css) — genuinely different corners, so a reader
        # can have both open together (see DECISIONS_LOG.md on this).
        context, page = self.open_page(site, browser, base_url)
        page.click("#dl-settings-toggle")
        assert page.is_visible("#dl-settings")
        page.click("#dl-reference-toggle")
        assert page.is_visible("#dl-reference")
        assert page.is_visible("#dl-settings")
        context.close()

    def test_opening_settings_does_not_close_the_reference(self, site, browser, base_url):
        context, page = self.open_page(site, browser, base_url)
        page.click("#dl-reference-toggle")
        assert page.is_visible("#dl-reference")
        page.click("#dl-settings-toggle")
        assert page.is_visible("#dl-settings")
        assert page.is_visible("#dl-reference")
        context.close()


class TestContent:
    def test_a_tutorial_shows_its_own_and_earlier_entries(self, site, browser, base_url):
        _tutorial(site, "one", "One")
        _tutorial(site, "two", "Two")
        _glossary(site, "one", [CONCEPT])
        _glossary(site, "two", [FUNCTION])
        _set_order(site, ["one", "two"])
        b.build()
        context = browser.new_context()
        page = context.new_page()
        page.goto(f"{base_url}/tutorials/{MODULE}/two.html")
        page.click("#dl-reference-toggle")
        text = page.inner_text("#dl-reference-groups")
        assert "x" in text and "The first thing." in text
        assert "f()" in text and "Does a thing." in text
        assert "f(1)" in text
        context.close()

    def test_a_tutorial_never_shows_a_later_ones_entries(self, site, browser, base_url):
        """The one guarantee that matters more than any other in this
        feature (planning/REFERENCE_PANEL.md §1)."""
        _tutorial(site, "one", "One")
        _tutorial(site, "two", "Two")
        _glossary(site, "one", [CONCEPT])
        _glossary(site, "two", [FUNCTION])
        _set_order(site, ["one", "two"])
        b.build()
        context = browser.new_context()
        page = context.new_page()
        page.goto(f"{base_url}/tutorials/{MODULE}/one.html")
        page.click("#dl-reference-toggle")
        text = page.inner_text("#dl-reference-groups")
        assert "x" in text
        assert "f()" not in text
        context.close()

    def test_entries_are_grouped_by_kind(self, site, browser, base_url):
        _tutorial(site, "one", "One")
        _glossary(site, "one", [CONCEPT, FUNCTION])
        _set_order(site, ["one"])
        b.build()
        context = browser.new_context()
        page = context.new_page()
        page.goto(f"{base_url}/tutorials/{MODULE}/one.html")
        page.click("#dl-reference-toggle")
        headings = page.eval_on_selector_all(
            "#dl-reference-groups h3", "els => els.map(e => e.textContent)")
        assert headings == ["Concepts", "Functions"]
        context.close()


class TestNotes:
    """Pedagogical notes surfacing in the reference panel —
    planning/SIDEBAR_CONTENT.md §3/§4."""

    def test_a_note_alone_shows_the_toggle(self, site, browser, base_url):
        """No glossary at all — a note by itself is enough reason to show
        the panel."""
        _tutorial_with_note(site, "one", "why-it-works", "Because reasons.")
        _set_order(site, ["one"])
        b.build()
        context = browser.new_context()
        page = context.new_page()
        page.goto(f"{base_url}/tutorials/{MODULE}/one.html")
        assert page.is_visible("#dl-reference-toggle")
        context.close()

    def test_opening_the_panel_shows_the_notes_heading_and_content(self, site, browser, base_url):
        _tutorial_with_note(site, "one", "why-it-works", "Because reasons.")
        _set_order(site, ["one"])
        b.build()
        context = browser.new_context()
        page = context.new_page()
        page.goto(f"{base_url}/tutorials/{MODULE}/one.html")
        page.click("#dl-reference-toggle")
        headings = page.eval_on_selector_all(
            "#dl-reference-groups h3", "els => els.map(e => e.textContent)")
        assert "Notes" in headings
        assert "Because reasons." in page.inner_text("#dl-reference-groups")
        context.close()

    def test_the_note_is_not_in_the_page_body(self, site, browser, base_url):
        """It surfaces in the panel instead of staying inline
        (planning/SIDEBAR_CONTENT.md §4's settled answer)."""
        _tutorial_with_note(site, "one", "why-it-works", "Because reasons.")
        _set_order(site, ["one"])
        b.build()
        context = browser.new_context()
        page = context.new_page()
        page.goto(f"{base_url}/tutorials/{MODULE}/one.html")
        assert "Because reasons." not in page.inner_text("main#dl-body")
        context.close()

    def test_a_note_and_a_glossary_both_appear_with_their_own_headings(self, site, browser, base_url):
        _tutorial_with_note(site, "one", "why-it-works", "Because reasons.")
        _glossary(site, "one", [CONCEPT])
        _set_order(site, ["one"])
        b.build()
        context = browser.new_context()
        page = context.new_page()
        page.goto(f"{base_url}/tutorials/{MODULE}/one.html")
        page.click("#dl-reference-toggle")
        headings = page.eval_on_selector_all(
            "#dl-reference-groups h3", "els => els.map(e => e.textContent)")
        assert headings == ["Concepts", "Notes"]
        context.close()


class TestDatasets:
    """Dataset attribution surfacing in the reference panel —
    planning/SIDEBAR_CONTENT.md §2/§4."""

    def test_a_dataset_alone_shows_the_toggle(self, site, browser, base_url, monkeypatch):
        monkeypatch.setattr(b, "DATA", site / "data")
        _dataset_files(site / "data", "life-expectancy", source="World Bank",
                        license="CC-BY-4.0", description="Life expectancy by country.")
        _tutorial_with_dataset(site, "one", "life-expectancy")
        _set_order(site, ["one"])
        b.build()
        context = browser.new_context()
        page = context.new_page()
        page.goto(f"{base_url}/tutorials/{MODULE}/one.html")
        assert page.is_visible("#dl-reference-toggle")
        context.close()

    def test_opening_the_panel_shows_the_datasets_heading_and_attribution(
        self, site, browser, base_url, monkeypatch
    ):
        monkeypatch.setattr(b, "DATA", site / "data")
        _dataset_files(site / "data", "life-expectancy", source="World Bank",
                        license="CC-BY-4.0", description="Life expectancy by country.")
        _tutorial_with_dataset(site, "one", "life-expectancy")
        _set_order(site, ["one"])
        b.build()
        context = browser.new_context()
        page = context.new_page()
        page.goto(f"{base_url}/tutorials/{MODULE}/one.html")
        page.click("#dl-reference-toggle")
        headings = page.eval_on_selector_all(
            "#dl-reference-groups h3", "els => els.map(e => e.textContent)")
        assert "Datasets used here" in headings
        text = page.inner_text("#dl-reference-groups")
        assert "life-expectancy" in text
        assert "World Bank" in text
        assert "CC-BY-4.0" in text
        assert "Life expectancy by country." in text
        context.close()


class TestMobile:
    """Planning/REFERENCE_PANEL.md's §6 mobile note, settled in
    QUESTIONS.md/DECISIONS_LOG.md: the panel becomes a bottom sheet on a
    phone, mirroring .dl-settings' own existing mobile treatment, rather
    than staying hidden."""

    def test_the_toggle_is_visible_on_a_phone_sized_viewport(self, site, browser, base_url):
        _tutorial(site, "one", "One")
        _glossary(site, "one", [CONCEPT])
        _set_order(site, ["one"])
        b.build()
        context = browser.new_context(viewport={"width": 375, "height": 700})
        page = context.new_page()
        page.goto(f"{base_url}/tutorials/{MODULE}/one.html")
        assert page.is_visible("#dl-reference-toggle")
        context.close()

    def test_opening_it_shows_a_sheet_anchored_to_the_bottom_edge(self, site, browser, base_url):
        _tutorial(site, "one", "One")
        _glossary(site, "one", [CONCEPT])
        _set_order(site, ["one"])
        b.build()
        context = browser.new_context(viewport={"width": 375, "height": 700})
        page = context.new_page()
        page.goto(f"{base_url}/tutorials/{MODULE}/one.html")
        page.click("#dl-reference-toggle")
        assert page.is_visible("#dl-reference")
        style = page.eval_on_selector(
            "#dl-reference",
            "el => { const s = getComputedStyle(el); "
            "return { position: s.position, bottom: s.bottom, left: s.left, right: s.right }; }",
        )
        assert style["position"] == "fixed"
        assert style["bottom"] == "0px"
        assert style["left"] == "0px"
        assert style["right"] == "0px"
        context.close()


# --------------------------------------------- highlight-to-look-up

LOOKUP_TERM = {"term": "gradient", "kind": "concept",
               "definition": "How steeply something changes."}

LOOKUP_PROSE = """---
title: "Lookup"
slug: lookup
module: reference-fixtures
module_title: "Reference Fixtures"
year: "2026-2027"
series: sample-series
version: 2026.08.23.1
---

# Lookup

The gradient of a line is one thing, and serendipity is quite another.
"""

# Selecting text from a test script: walk the reading for the word, put a
# Range over it, and make that the document's selection — which is what a
# reader's own drag produces, and what fires the selectionchange this
# feature listens on.
SELECT = """(word) => {
  const walk = document.createTreeWalker(
    document.getElementById('dl-body'), NodeFilter.SHOW_TEXT);
  let node;
  while ((node = walk.nextNode())) {
    const at = node.textContent.indexOf(word);
    if (at >= 0 && !node.parentElement.closest('.dl-editor')) {
      const range = document.createRange();
      range.setStart(node, at);
      range.setEnd(node, at + word.length);
      const selection = getSelection();
      selection.removeAllRanges();
      selection.addRange(range);
      return true;
    }
  }
  return false;
}"""


class TestHighlightToLookUp:
    """Selecting a word the reference knows offers to look it up —
    planning/ROADMAP.md Phase 5, DECISIONS_LOG.md 7.91.

    The property worth protecting is not that the button appears; it is that
    it *stays away* for every selection that is not a term, which is most of
    them.
    """

    def open_page(self, site, browser, base_url):
        # Flat, matching _tutorial()/_glossary() above rather than the
        # folder-per-tutorial layout the real tutorials/ uses: the build reads
        # a glossary from beside its own markdown wherever that sits, so these
        # fixtures work either way, and staying consistent with the rest of
        # this file keeps one convention per file.
        path = site / "tutorials" / MODULE / "lookup.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(LOOKUP_PROSE)
        _glossary(site, "lookup", [LOOKUP_TERM])
        _set_order(site, ["lookup"])
        b.build()
        context = browser.new_context()
        page = context.new_page()
        page.goto(f"{base_url}/tutorials/{MODULE}/lookup.html")
        page.wait_for_selector("#dl-body")
        return context, page

    def test_nothing_is_offered_until_something_is_selected(self, site, browser, base_url):
        context, page = self.open_page(site, browser, base_url)
        assert page.is_hidden(".dl-lookup")
        context.close()

    def test_selecting_a_term_offers_to_look_it_up(self, site, browser, base_url):
        context, page = self.open_page(site, browser, base_url)
        assert page.evaluate(SELECT, "gradient")
        page.wait_for_selector(".dl-lookup:not([hidden])")
        assert "gradient" in page.inner_text(".dl-lookup")
        context.close()

    def test_selecting_a_word_the_reference_does_not_know_offers_nothing(
            self, site, browser, base_url):
        """The whole reason this is not annoying. A reader selecting a
        sentence to copy must not be interrupted."""
        context, page = self.open_page(site, browser, base_url)
        assert page.evaluate(SELECT, "serendipity")
        page.wait_for_timeout(200)
        assert page.is_hidden(".dl-lookup")
        context.close()

    def test_using_it_opens_the_panel_filtered_to_that_term(self, site, browser, base_url):
        context, page = self.open_page(site, browser, base_url)
        page.evaluate(SELECT, "gradient")
        page.wait_for_selector(".dl-lookup:not([hidden])")
        page.click(".dl-lookup")
        page.wait_for_selector("#dl-reference:not([hidden])")
        shown = page.eval_on_selector_all(
            "#dl-reference-groups dt:not([hidden])", "els => els.map(e => e.textContent)")
        assert shown == ["gradient"]
        context.close()

    def test_the_offer_goes_away_once_it_has_been_used(self, site, browser, base_url):
        """Otherwise it sits over the reading offering the same lookup again."""
        context, page = self.open_page(site, browser, base_url)
        page.evaluate(SELECT, "gradient")
        page.wait_for_selector(".dl-lookup:not([hidden])")
        page.click(".dl-lookup")
        page.wait_for_selector("#dl-reference:not([hidden])")
        assert page.is_hidden(".dl-lookup")
        context.close()
