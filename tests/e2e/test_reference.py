"""Every fixture here is prose-only, so tutorial-runtime.js never boots
Pyodide for these pages — unlike most of tests/e2e/, this file runs without
`python3 dev/fetch_pyodide.py` first."""

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
    """Only ROOT/TUTORIALS/OUT move to tmp_path; ASSETS/SHELL/SETUP/DATA stay
    pointed at the real repo, so the page runs the actual runtime and CSS."""
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


def _open_panel(actor, selector: str) -> None:
    """Reference/Series/Settings' toggles now collapse behind one
    "Panels" control in the masthead (shell.html's
    <details class="dl-panels">) rather than always showing — expand it
    first if it isn't already, then click the actual target. Checked via
    #dl-panels' own `open` property rather than the target's own
    visibility, so this never mistakes "already open" for "not open" and
    toggles it shut again right before the click that was supposed to
    land. Left expanded once opened (no auto-collapse), so this is only
    needed once per page load, not before every toggle click."""
    if not actor.eval_on_selector("#dl-panels", "el => el.open"):
        actor.click("#dl-panels summary")
    actor.click(selector)


def _toggle_shows(actor, selector: str) -> bool:
    """Whether a masthead toggle has content to show, via its own
    `hidden` attribute (tutorial-runtime.js's own content-presence
    signal) rather than Playwright's is_visible()/is_hidden() — those now
    also depend on whether "Panels" happens to be expanded, which is a
    question about the masthead's own UI state, not this page's
    content."""
    return actor.get_attribute(selector, "hidden") is None


class TestVisibility:
    def test_no_glossary_anywhere_in_the_series_still_shows_the_basics_tabs(
            self, site, browser, base_url):
        """Math Basics and Python Basics are the same on every page, so the
        toggle shows even when this page and its series have nothing of
        their own yet."""
        _tutorial(site, "one", "One")
        _set_order(site, ["one"])
        b.build()
        context = browser.new_context()
        page = context.new_page()
        page.goto(f"{base_url}/tutorials/{MODULE}/one.html")
        assert _toggle_shows(page, "#dl-reference-toggle")
        _open_panel(page, "#dl-reference-toggle")
        assert page.is_visible("#dl-reference-nothing-yet")
        page.click("#dl-reference-tab-basics")
        assert page.locator("#dl-basics-groups dt").count() > 0
        page.click("#dl-reference-tab-python")
        assert page.locator("#dl-python-groups dt").count() > 0
        context.close()

    def test_a_tutorial_with_something_accumulated_shows_the_toggle(self, site, browser, base_url):
        _tutorial(site, "one", "One")
        _glossary(site, "one", [CONCEPT])
        _set_order(site, ["one"])
        b.build()
        context = browser.new_context()
        page = context.new_page()
        page.goto(f"{base_url}/tutorials/{MODULE}/one.html")
        assert _toggle_shows(page, "#dl-reference-toggle")
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
        _open_panel(page, "#dl-reference-toggle")
        assert page.is_visible("#dl-reference")
        context.close()

    def test_escape_closes_it(self, site, browser, base_url):
        context, page = self.open_page(site, browser, base_url)
        _open_panel(page, "#dl-reference-toggle")
        page.keyboard.press("Escape")
        assert page.is_hidden("#dl-reference")
        context.close()

    def test_the_close_button_closes_it(self, site, browser, base_url):
        context, page = self.open_page(site, browser, base_url)
        _open_panel(page, "#dl-reference-toggle")
        page.click("#dl-reference-close")
        assert page.is_hidden("#dl-reference")
        context.close()

    def test_clicking_outside_closes_it(self, site, browser, base_url):
        context, page = self.open_page(site, browser, base_url)
        _open_panel(page, "#dl-reference-toggle")
        page.click("main#dl-body")
        assert page.is_hidden("#dl-reference")
        context.close()

    def test_opening_the_reference_does_not_close_settings(self, site, browser, base_url):
        context, page = self.open_page(site, browser, base_url)
        _open_panel(page, "#dl-settings-toggle")
        assert page.is_visible("#dl-settings")
        _open_panel(page, "#dl-reference-toggle")
        assert page.is_visible("#dl-reference")
        assert page.is_visible("#dl-settings")
        context.close()

    def test_opening_settings_does_not_close_the_reference(self, site, browser, base_url):
        context, page = self.open_page(site, browser, base_url)
        _open_panel(page, "#dl-reference-toggle")
        assert page.is_visible("#dl-reference")
        _open_panel(page, "#dl-settings-toggle")
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
        _open_panel(page, "#dl-reference-toggle")
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
        _open_panel(page, "#dl-reference-toggle")
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
        _open_panel(page, "#dl-reference-toggle")
        headings = page.eval_on_selector_all(
            "#dl-reference-groups h3", "els => els.map(e => e.textContent)")
        assert headings == ["Concepts", "Functions"]
        context.close()


class TestNotes:
    """Pedagogical notes surfacing in the reference panel —
    planning/SIDEBAR_CONTENT.md §3/§4."""

    def test_a_note_alone_shows_the_toggle(self, site, browser, base_url):
        _tutorial_with_note(site, "one", "why-it-works", "Because reasons.")
        _set_order(site, ["one"])
        b.build()
        context = browser.new_context()
        page = context.new_page()
        page.goto(f"{base_url}/tutorials/{MODULE}/one.html")
        assert _toggle_shows(page, "#dl-reference-toggle")
        context.close()

    def test_opening_the_panel_shows_the_notes_heading_and_content(self, site, browser, base_url):
        _tutorial_with_note(site, "one", "why-it-works", "Because reasons.")
        _set_order(site, ["one"])
        b.build()
        context = browser.new_context()
        page = context.new_page()
        page.goto(f"{base_url}/tutorials/{MODULE}/one.html")
        _open_panel(page, "#dl-reference-toggle")
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
        _open_panel(page, "#dl-reference-toggle")
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
        assert _toggle_shows(page, "#dl-reference-toggle")
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
        _open_panel(page, "#dl-reference-toggle")
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
    """REFERENCE_PANEL.md §6: on a phone the panel becomes a bottom sheet,
    mirroring .dl-settings' own mobile treatment, rather than staying hidden."""

    def test_the_toggle_is_visible_on_a_phone_sized_viewport(self, site, browser, base_url):
        _tutorial(site, "one", "One")
        _glossary(site, "one", [CONCEPT])
        _set_order(site, ["one"])
        b.build()
        context = browser.new_context(viewport={"width": 375, "height": 700})
        page = context.new_page()
        page.goto(f"{base_url}/tutorials/{MODULE}/one.html")
        assert _toggle_shows(page, "#dl-reference-toggle")
        context.close()

    def test_opening_it_shows_a_sheet_anchored_to_the_bottom_edge(self, site, browser, base_url):
        _tutorial(site, "one", "One")
        _glossary(site, "one", [CONCEPT])
        _set_order(site, ["one"])
        b.build()
        context = browser.new_context(viewport={"width": 375, "height": 700})
        page = context.new_page()
        page.goto(f"{base_url}/tutorials/{MODULE}/one.html")
        _open_panel(page, "#dl-reference-toggle")
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
    """The property worth protecting is not that the button appears, but that
    it stays away for every selection that isn't a term — most of them."""

    def open_page(self, site, browser, base_url):
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
        """A reader selecting a sentence to copy must not be interrupted."""
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
