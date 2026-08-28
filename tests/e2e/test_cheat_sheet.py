"""The cheat sheet panel, in a real browser — planning/CHEAT_SHEETS.md.

A dedicated, tiny site build rather than the shared rendering-tour fixture
the rest of tests/e2e/ uses: this needs its own glossary files and series
order. It also needs no self-hosted Pyodide and none of the wait that comes
with one — every fixture tutorial here is prose-only, and
tutorial-runtime.js's own boot() skips loading Pyodide entirely when a page
has no cells (CONTENT_AND_FILE_ARCHITECTURE.md) — so unlike most of this
directory, this file runs without `python3 dev/fetch_pyodide.py` first.

    python3 -m pytest tests/e2e/test_cheat_sheet.py -q
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

MODULE = "cheatsheet-fixtures"

FRONTMATTER = """---
title: "{title}"
slug: {slug}
module: cheatsheet-fixtures
module_title: "Cheat Sheet Fixtures"
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
module: cheatsheet-fixtures
module_title: "Cheat Sheet Fixtures"
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
module: cheatsheet-fixtures
module_title: "Cheat Sheet Fixtures"
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
        assert page.is_hidden("#dl-cheatsheet-toggle")
        context.close()

    def test_a_tutorial_with_something_accumulated_shows_the_toggle(self, site, browser, base_url):
        _tutorial(site, "one", "One")
        _glossary(site, "one", [CONCEPT])
        _set_order(site, ["one"])
        b.build()
        context = browser.new_context()
        page = context.new_page()
        page.goto(f"{base_url}/tutorials/{MODULE}/one.html")
        assert page.is_visible("#dl-cheatsheet-toggle")
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
        assert page.is_hidden("#dl-cheatsheet")
        context.close()

    def test_clicking_the_toggle_opens_it(self, site, browser, base_url):
        context, page = self.open_page(site, browser, base_url)
        page.click("#dl-cheatsheet-toggle")
        assert page.is_visible("#dl-cheatsheet")
        context.close()

    def test_escape_closes_it(self, site, browser, base_url):
        context, page = self.open_page(site, browser, base_url)
        page.click("#dl-cheatsheet-toggle")
        page.keyboard.press("Escape")
        assert page.is_hidden("#dl-cheatsheet")
        context.close()

    def test_the_close_button_closes_it(self, site, browser, base_url):
        context, page = self.open_page(site, browser, base_url)
        page.click("#dl-cheatsheet-toggle")
        page.click("#dl-cheatsheet-close")
        assert page.is_hidden("#dl-cheatsheet")
        context.close()

    def test_clicking_outside_closes_it(self, site, browser, base_url):
        context, page = self.open_page(site, browser, base_url)
        page.click("#dl-cheatsheet-toggle")
        page.click("main#dl-body")
        assert page.is_hidden("#dl-cheatsheet")
        context.close()

    def test_opening_the_cheat_sheet_closes_settings(self, site, browser, base_url):
        context, page = self.open_page(site, browser, base_url)
        page.click("#dl-settings-toggle")
        assert page.is_visible("#dl-settings")
        page.click("#dl-cheatsheet-toggle")
        assert page.is_visible("#dl-cheatsheet")
        assert page.is_hidden("#dl-settings")
        context.close()

    def test_opening_settings_closes_the_cheat_sheet(self, site, browser, base_url):
        context, page = self.open_page(site, browser, base_url)
        page.click("#dl-cheatsheet-toggle")
        assert page.is_visible("#dl-cheatsheet")
        page.click("#dl-settings-toggle")
        assert page.is_visible("#dl-settings")
        assert page.is_hidden("#dl-cheatsheet")
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
        page.click("#dl-cheatsheet-toggle")
        text = page.inner_text("#dl-cheatsheet-groups")
        assert "x" in text and "The first thing." in text
        assert "f()" in text and "Does a thing." in text
        assert "f(1)" in text
        context.close()

    def test_a_tutorial_never_shows_a_later_ones_entries(self, site, browser, base_url):
        """The one guarantee that matters more than any other in this
        feature (planning/CHEAT_SHEETS.md §1)."""
        _tutorial(site, "one", "One")
        _tutorial(site, "two", "Two")
        _glossary(site, "one", [CONCEPT])
        _glossary(site, "two", [FUNCTION])
        _set_order(site, ["one", "two"])
        b.build()
        context = browser.new_context()
        page = context.new_page()
        page.goto(f"{base_url}/tutorials/{MODULE}/one.html")
        page.click("#dl-cheatsheet-toggle")
        text = page.inner_text("#dl-cheatsheet-groups")
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
        page.click("#dl-cheatsheet-toggle")
        headings = page.eval_on_selector_all(
            "#dl-cheatsheet-groups h3", "els => els.map(e => e.textContent)")
        assert headings == ["Concepts", "Functions"]
        context.close()


class TestNotes:
    """Pedagogical notes surfacing in the cheat sheet panel —
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
        assert page.is_visible("#dl-cheatsheet-toggle")
        context.close()

    def test_opening_the_panel_shows_the_notes_heading_and_content(self, site, browser, base_url):
        _tutorial_with_note(site, "one", "why-it-works", "Because reasons.")
        _set_order(site, ["one"])
        b.build()
        context = browser.new_context()
        page = context.new_page()
        page.goto(f"{base_url}/tutorials/{MODULE}/one.html")
        page.click("#dl-cheatsheet-toggle")
        headings = page.eval_on_selector_all(
            "#dl-cheatsheet-groups h3", "els => els.map(e => e.textContent)")
        assert "Notes" in headings
        assert "Because reasons." in page.inner_text("#dl-cheatsheet-groups")
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
        page.click("#dl-cheatsheet-toggle")
        headings = page.eval_on_selector_all(
            "#dl-cheatsheet-groups h3", "els => els.map(e => e.textContent)")
        assert headings == ["Concepts", "Notes"]
        context.close()


class TestDatasets:
    """Dataset attribution surfacing in the cheat sheet panel —
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
        assert page.is_visible("#dl-cheatsheet-toggle")
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
        page.click("#dl-cheatsheet-toggle")
        headings = page.eval_on_selector_all(
            "#dl-cheatsheet-groups h3", "els => els.map(e => e.textContent)")
        assert "Datasets used here" in headings
        text = page.inner_text("#dl-cheatsheet-groups")
        assert "life-expectancy" in text
        assert "World Bank" in text
        assert "CC-BY-4.0" in text
        assert "Life expectancy by country." in text
        context.close()


class TestMobile:
    """Planning/CHEAT_SHEETS.md's §6 mobile note, settled in
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
        assert page.is_visible("#dl-cheatsheet-toggle")
        context.close()

    def test_opening_it_shows_a_sheet_anchored_to_the_bottom_edge(self, site, browser, base_url):
        _tutorial(site, "one", "One")
        _glossary(site, "one", [CONCEPT])
        _set_order(site, ["one"])
        b.build()
        context = browser.new_context(viewport={"width": 375, "height": 700})
        page = context.new_page()
        page.goto(f"{base_url}/tutorials/{MODULE}/one.html")
        page.click("#dl-cheatsheet-toggle")
        assert page.is_visible("#dl-cheatsheet")
        style = page.eval_on_selector(
            "#dl-cheatsheet",
            "el => { const s = getComputedStyle(el); "
            "return { position: s.position, bottom: s.bottom, left: s.left, right: s.right }; }",
        )
        assert style["position"] == "fixed"
        assert style["bottom"] == "0px"
        assert style["left"] == "0px"
        assert style["right"] == "0px"
        context.close()
