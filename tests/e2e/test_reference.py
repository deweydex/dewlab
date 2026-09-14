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

from conftest import _open_panel
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
def site_url(site):
    server, thread, url = _serve(site / "site")
    try:
        yield url
    finally:
        server.shutdown()
        thread.join(timeout=5)


CONCEPT = {"term": "x", "kind": "concept", "definition": "The first thing."}
FUNCTION = {"term": "f()", "kind": "function", "definition": "Does a thing.", "example": "f(1)"}


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
            self, site, browser, site_url):
        """Math Basics and Python Basics are the same on every page, so the
        toggle shows even when this page and its series have nothing of
        their own yet."""
        _tutorial(site, "one", "One")
        _set_order(site, ["one"])
        b.build()
        context = browser.new_context()
        page = context.new_page()
        page.goto(f"{site_url}/tutorials/{MODULE}/one.html")
        assert _toggle_shows(page, "#dl-reference-toggle")
        _open_panel(page, "#dl-reference-toggle")
        assert page.is_visible("#dl-reference-nothing-yet")
        page.click("#dl-reference-tab-basics")
        assert page.locator("#dl-basics-groups dt").count() > 0
        page.click("#dl-reference-tab-python")
        assert page.locator("#dl-python-groups dt").count() > 0
        context.close()

    def test_a_tutorial_with_something_accumulated_shows_the_toggle(self, site, browser, site_url):
        _tutorial(site, "one", "One")
        _glossary(site, "one", [CONCEPT])
        _set_order(site, ["one"])
        b.build()
        context = browser.new_context()
        page = context.new_page()
        page.goto(f"{site_url}/tutorials/{MODULE}/one.html")
        assert _toggle_shows(page, "#dl-reference-toggle")
        context.close()


class TestIdentityCornerControlsAreDirect:
    """Series used to live behind a "Panels" disclosure shared with
    Reference; once Reference got its own corner-tab button, the group
    that disclosure gated could only ever hold Series alone, so the extra
    click it asked for stopped earning its keep — Series is now a plain
    button in the identity block, exactly like Reference and Appearance
    are direct everywhere."""

    def test_series_is_a_plain_visible_button_not_a_disclosure(
            self, site, browser, site_url):
        _tutorial(site, "one", "One")
        _tutorial(site, "two", "Two")
        _set_order(site, ["one", "two"])
        b.build()
        context = browser.new_context(viewport={"width": 1200, "height": 800})
        page = context.new_page()
        page.goto(f"{site_url}/tutorials/{MODULE}/one.html")

        assert page.locator("#dl-panels").count() == 0
        assert page.is_visible("#dl-seriesnav-toggle")
        page.click("#dl-seriesnav-toggle")
        assert page.is_visible("#dl-seriesnav")
        context.close()

    @pytest.mark.parametrize("path", ["index.html", f"{MODULE}.html"])
    def test_appearance_is_direct_on_home_and_module_pages(
            self, site, browser, site_url, path):
        """Appearance (and the rest of what used to be Settings) lives in
        its own corner dock now, never behind a disclosure — so this is
        direct everywhere, not only on pages with no series."""
        _tutorial(site, "one", "One")
        _set_order(site, ["one"])
        b.build()
        context = browser.new_context()
        page = context.new_page()
        page.goto(f"{site_url}/{path}")

        assert page.is_visible("#dl-appearance-toggle")
        page.click("#dl-appearance-toggle")
        assert page.is_visible("#dl-appearance")
        context.close()

class TestOpeningAndClosing:
    def open_page(self, site, browser, site_url, slug="two"):
        _tutorial(site, "one", "One")
        _tutorial(site, "two", "Two")
        _glossary(site, "one", [CONCEPT])
        _glossary(site, "two", [FUNCTION])
        _set_order(site, ["one", "two"])
        b.build()
        context = browser.new_context()
        page = context.new_page()
        page.goto(f"{site_url}/tutorials/{MODULE}/{slug}.html")
        return context, page

    def test_the_panel_is_closed_by_default(self, site, browser, site_url):
        context, page = self.open_page(site, browser, site_url)
        assert page.is_hidden("#dl-reference")
        context.close()

    def test_clicking_the_toggle_opens_it(self, site, browser, site_url):
        context, page = self.open_page(site, browser, site_url)
        _open_panel(page, "#dl-reference-toggle")
        assert page.is_visible("#dl-reference")
        context.close()

    def test_escape_closes_it(self, site, browser, site_url):
        context, page = self.open_page(site, browser, site_url)
        _open_panel(page, "#dl-reference-toggle")
        page.keyboard.press("Escape")
        assert page.is_hidden("#dl-reference")
        context.close()

    def test_the_close_button_closes_it(self, site, browser, site_url):
        context, page = self.open_page(site, browser, site_url)
        _open_panel(page, "#dl-reference-toggle")
        page.click("#dl-reference-close")
        assert page.is_hidden("#dl-reference")
        context.close()

    def test_clicking_outside_closes_it(self, site, browser, site_url):
        context, page = self.open_page(site, browser, site_url)
        _open_panel(page, "#dl-reference-toggle")
        page.click("main#dl-body")
        assert page.is_hidden("#dl-reference")
        context.close()

    def test_opening_the_reference_does_not_close_appearance(self, site, browser, site_url):
        context, page = self.open_page(site, browser, site_url)
        _open_panel(page, "#dl-appearance-toggle")
        assert page.is_visible("#dl-appearance")
        _open_panel(page, "#dl-reference-toggle")
        assert page.is_visible("#dl-reference")
        assert page.is_visible("#dl-appearance")
        context.close()

    def test_opening_appearance_does_not_close_the_reference(self, site, browser, site_url):
        context, page = self.open_page(site, browser, site_url)
        _open_panel(page, "#dl-reference-toggle")
        assert page.is_visible("#dl-reference")
        _open_panel(page, "#dl-appearance-toggle")
        assert page.is_visible("#dl-appearance")
        assert page.is_visible("#dl-reference")
        context.close()


class TestContent:
    def test_a_tutorial_shows_its_own_and_earlier_entries(self, site, browser, site_url):
        _tutorial(site, "one", "One")
        _tutorial(site, "two", "Two")
        _glossary(site, "one", [CONCEPT])
        _glossary(site, "two", [FUNCTION])
        _set_order(site, ["one", "two"])
        b.build()
        context = browser.new_context()
        page = context.new_page()
        page.goto(f"{site_url}/tutorials/{MODULE}/two.html")
        _open_panel(page, "#dl-reference-toggle")
        text = page.inner_text("#dl-reference-groups")
        assert "x" in text and "The first thing." in text
        assert "f()" in text and "Does a thing." in text
        assert "f(1)" in text
        context.close()

    def test_a_tutorial_never_shows_a_later_ones_entries(self, site, browser, site_url):
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
        page.goto(f"{site_url}/tutorials/{MODULE}/one.html")
        _open_panel(page, "#dl-reference-toggle")
        text = page.inner_text("#dl-reference-groups")
        assert "x" in text
        assert "f()" not in text
        context.close()

    def test_entries_are_grouped_by_kind(self, site, browser, site_url):
        _tutorial(site, "one", "One")
        _glossary(site, "one", [CONCEPT, FUNCTION])
        _set_order(site, ["one"])
        b.build()
        context = browser.new_context()
        page = context.new_page()
        page.goto(f"{site_url}/tutorials/{MODULE}/one.html")
        _open_panel(page, "#dl-reference-toggle")
        headings = page.eval_on_selector_all(
            "#dl-reference-groups h3", "els => els.map(e => e.textContent)")
        assert headings == ["Concepts", "Functions"]
        context.close()


class TestNotes:
    """Pedagogical notes surfacing in the reference panel —
    planning/SIDEBAR_CONTENT.md §3/§4."""

    def test_a_note_alone_shows_the_toggle(self, site, browser, site_url):
        _tutorial_with_note(site, "one", "why-it-works", "Because reasons.")
        _set_order(site, ["one"])
        b.build()
        context = browser.new_context()
        page = context.new_page()
        page.goto(f"{site_url}/tutorials/{MODULE}/one.html")
        assert _toggle_shows(page, "#dl-reference-toggle")
        context.close()

    def test_opening_the_panel_shows_the_notes_heading_and_content(self, site, browser, site_url):
        _tutorial_with_note(site, "one", "why-it-works", "Because reasons.")
        _set_order(site, ["one"])
        b.build()
        context = browser.new_context()
        page = context.new_page()
        page.goto(f"{site_url}/tutorials/{MODULE}/one.html")
        _open_panel(page, "#dl-reference-toggle")
        headings = page.eval_on_selector_all(
            "#dl-reference-groups h3", "els => els.map(e => e.textContent)")
        assert "Notes" in headings
        assert "Because reasons." in page.inner_text("#dl-reference-groups")
        context.close()

    def test_the_note_is_not_in_the_page_body(self, site, browser, site_url):
        """It surfaces in the panel instead of staying inline
        (planning/SIDEBAR_CONTENT.md §4's settled answer)."""
        _tutorial_with_note(site, "one", "why-it-works", "Because reasons.")
        _set_order(site, ["one"])
        b.build()
        context = browser.new_context()
        page = context.new_page()
        page.goto(f"{site_url}/tutorials/{MODULE}/one.html")
        assert "Because reasons." not in page.inner_text("main#dl-body")
        context.close()

    def test_a_note_and_a_glossary_both_appear_with_their_own_headings(self, site, browser, site_url):
        _tutorial_with_note(site, "one", "why-it-works", "Because reasons.")
        _glossary(site, "one", [CONCEPT])
        _set_order(site, ["one"])
        b.build()
        context = browser.new_context()
        page = context.new_page()
        page.goto(f"{site_url}/tutorials/{MODULE}/one.html")
        _open_panel(page, "#dl-reference-toggle")
        headings = page.eval_on_selector_all(
            "#dl-reference-groups h3", "els => els.map(e => e.textContent)")
        assert headings == ["Concepts", "Notes"]
        context.close()


class TestDatasets:
    """Dataset attribution surfacing in the reference panel —
    planning/SIDEBAR_CONTENT.md §2/§4."""

    def test_a_dataset_alone_shows_the_toggle(self, site, browser, site_url, monkeypatch):
        monkeypatch.setattr(b, "DATA", site / "data")
        _dataset_files(site / "data", "life-expectancy", source="World Bank",
                        license="CC-BY-4.0", description="Life expectancy by country.")
        _tutorial_with_dataset(site, "one", "life-expectancy")
        _set_order(site, ["one"])
        b.build()
        context = browser.new_context()
        page = context.new_page()
        page.goto(f"{site_url}/tutorials/{MODULE}/one.html")
        assert _toggle_shows(page, "#dl-reference-toggle")
        context.close()

    def test_opening_the_panel_shows_the_datasets_heading_and_attribution(
        self, site, browser, site_url, monkeypatch
    ):
        monkeypatch.setattr(b, "DATA", site / "data")
        _dataset_files(site / "data", "life-expectancy", source="World Bank",
                        license="CC-BY-4.0", description="Life expectancy by country.")
        _tutorial_with_dataset(site, "one", "life-expectancy")
        _set_order(site, ["one"])
        b.build()
        context = browser.new_context()
        page = context.new_page()
        page.goto(f"{site_url}/tutorials/{MODULE}/one.html")
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


class TestPanelClearsTheCornerDocks:
    """The top-left dock (wordmark, breadcrumb tree, search, the Series
    toggle) and the bottom-left dock (Documentation's own tab) both stay
    above a left-side panel in z-index so their toggle stays reachable
    while the panel is open — see trackCornerDockHeights() in
    tutorial-runtime.js. Without the panel carving out room for both, its
    own header (or its content once scrolled to the bottom) renders right
    underneath them."""

    def test_the_reference_panel_starts_below_the_top_left_dock(self, site, browser, site_url):
        _tutorial(site, "one", "One")
        _glossary(site, "one", [CONCEPT])
        _set_order(site, ["one"])
        b.build()
        context = browser.new_context(viewport={"width": 1400, "height": 900})
        page = context.new_page()
        page.goto(f"{site_url}/tutorials/{MODULE}/one.html")
        _open_panel(page, "#dl-reference-toggle")
        dock_bottom = page.eval_on_selector(
            ".dl-corner-dock-tl", "el => el.getBoundingClientRect().bottom")
        panel_top = page.eval_on_selector(
            "#dl-reference", "el => el.getBoundingClientRect().top")
        assert panel_top >= dock_bottom - 1
        context.close()

    def test_the_reference_panel_ends_above_the_bottom_left_dock(self, site, browser, site_url):
        _tutorial(site, "one", "One")
        _glossary(site, "one", [CONCEPT])
        _set_order(site, ["one"])
        b.build()
        context = browser.new_context(viewport={"width": 1400, "height": 900})
        page = context.new_page()
        page.goto(f"{site_url}/tutorials/{MODULE}/one.html")
        _open_panel(page, "#dl-reference-toggle")
        dock_top = page.eval_on_selector(
            ".dl-corner-dock-bl", "el => el.getBoundingClientRect().top")
        panel_bottom = page.eval_on_selector(
            "#dl-reference", "el => el.getBoundingClientRect().bottom")
        assert panel_bottom <= dock_top + 1
        context.close()

    def test_the_notes_panel_starts_below_the_top_right_strip(self, site, browser, site_url):
        _tutorial(site, "one", "One")
        _set_order(site, ["one"])
        b.build()
        context = browser.new_context(viewport={"width": 1400, "height": 900})
        page = context.new_page()
        page.goto(f"{site_url}/tutorials/{MODULE}/one.html")
        _open_panel(page, "#dl-yourwork-toggle")
        dock_bottom = page.eval_on_selector(
            ".dl-corner-dock-tr", "el => el.getBoundingClientRect().bottom")
        panel_top = page.eval_on_selector(
            "#dl-yourwork", "el => el.getBoundingClientRect().top")
        assert panel_top >= dock_bottom - 1
        context.close()

    def test_the_appearance_panel_ends_above_the_bottom_right_strip(self, site, browser, site_url):
        _tutorial(site, "one", "One")
        _set_order(site, ["one"])
        b.build()
        context = browser.new_context(viewport={"width": 1400, "height": 900})
        page = context.new_page()
        page.goto(f"{site_url}/tutorials/{MODULE}/one.html")
        _open_panel(page, "#dl-appearance-toggle")
        dock_top = page.eval_on_selector(
            ".dl-corner-dock-br", "el => el.getBoundingClientRect().top")
        panel_bottom = page.eval_on_selector(
            "#dl-appearance", "el => el.getBoundingClientRect().bottom")
        assert panel_bottom <= dock_top + 1
        context.close()


class TestMobile:
    """REFERENCE_PANEL.md §6: on a phone the panel becomes a bottom sheet,
    mirroring .dl-settings' own mobile treatment, rather than staying hidden."""

    def test_the_toggle_is_visible_on_a_phone_sized_viewport(self, site, browser, site_url):
        _tutorial(site, "one", "One")
        _glossary(site, "one", [CONCEPT])
        _set_order(site, ["one"])
        b.build()
        context = browser.new_context(viewport={"width": 375, "height": 700})
        page = context.new_page()
        page.goto(f"{site_url}/tutorials/{MODULE}/one.html")
        assert _toggle_shows(page, "#dl-reference-toggle")
        context.close()

    def test_opening_it_shows_a_sheet_anchored_to_the_bottom_edge(self, site, browser, site_url):
        """The raw toggle is CSS-hidden on a phone-sized viewport now — a
        thumb reaches Reference through the mobile launcher instead
        (initMobileLauncher(), tutorial-runtime.js), which forwards a real
        click to this same button. Opened that way here, matching what a
        phone actually does, rather than clicking the (invisible) toggle
        directly."""
        _tutorial(site, "one", "One")
        _glossary(site, "one", [CONCEPT])
        _set_order(site, ["one"])
        b.build()
        context = browser.new_context(viewport={"width": 375, "height": 700})
        page = context.new_page()
        page.goto(f"{site_url}/tutorials/{MODULE}/one.html")
        page.click("#dl-mobile-fab")
        page.click("#dl-mobile-item-reference")
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


class TestMobileLauncher:
    """A thumb has room for one button, not six — every corner-tab toggle
    collapses into one launcher on a phone (initMobileLauncher(),
    tutorial-runtime.js), forwarding a real click to the actual toggle
    rather than duplicating its open/close logic a second time."""

    def open_page(self, site, browser, site_url):
        _tutorial(site, "one", "One")
        _glossary(site, "one", [CONCEPT])
        _set_order(site, ["one"])
        b.build()
        context = browser.new_context(viewport={"width": 375, "height": 700})
        page = context.new_page()
        page.goto(f"{site_url}/tutorials/{MODULE}/one.html")
        return context, page

    def test_the_fab_is_hidden_on_desktop(self, site, browser, site_url):
        _tutorial(site, "one", "One")
        _set_order(site, ["one"])
        b.build()
        context = browser.new_context(viewport={"width": 1200, "height": 800})
        page = context.new_page()
        page.goto(f"{site_url}/tutorials/{MODULE}/one.html")
        assert page.eval_on_selector(
            "#dl-mobile-fab", "el => getComputedStyle(el).display") == "none"
        context.close()

    def test_clicking_the_fab_opens_the_menu(self, site, browser, site_url):
        context, page = self.open_page(site, browser, site_url)
        assert page.is_hidden("#dl-mobile-menu")
        page.click("#dl-mobile-fab")
        assert page.is_visible("#dl-mobile-menu")
        context.close()

    def test_forwarding_opens_the_real_panel_and_closes_the_menu(self, site, browser, site_url):
        context, page = self.open_page(site, browser, site_url)
        page.click("#dl-mobile-fab")
        page.click("#dl-mobile-item-reference")
        assert page.is_visible("#dl-reference")
        assert page.is_hidden("#dl-mobile-menu")
        context.close()

    def test_the_forwarded_click_does_not_reopen_and_reclose_itself(
            self, site, browser, site_url):
        """A regression test for a real bug: the forwarded click's own
        original event kept bubbling to the same document-level
        outside-click listener that had just reacted to it opening the
        panel, reading the (still-bubbling) original click as "outside"
        and closing the panel right back — all within the one click.
        Fixed with stopPropagation() on the menu item's own handler."""
        context, page = self.open_page(site, browser, site_url)
        page.click("#dl-mobile-fab")
        page.click("#dl-mobile-item-reference")
        assert page.is_visible("#dl-reference")
        context.close()

    def test_series_is_reachable_from_the_launcher(self, site, browser, site_url):
        """Series left the identity row on phones (it had shrunk to an
        icon-only square floating over the page) for the launcher. The
        launcher mirrors the toggle's own hidden state once at load, so
        this also pins the init order: initSeriesNav() has to have
        unhidden the toggle before initMobileLauncher() looks."""
        _tutorial(site, "one", "One")
        _tutorial(site, "two", "Two")
        _set_order(site, ["one", "two"])
        b.build()
        context = browser.new_context(viewport={"width": 375, "height": 700})
        page = context.new_page()
        page.goto(f"{site_url}/tutorials/{MODULE}/one.html")
        page.click("#dl-mobile-fab")
        assert page.is_visible("#dl-mobile-item-seriesnav")
        page.click("#dl-mobile-item-seriesnav")
        assert page.is_visible("#dl-seriesnav")
        context.close()

    def test_the_identity_row_sits_in_flow_above_the_page_not_over_it(
            self, site, browser, site_url):
        """Fixed at the top-left, the wordmark and search sat over the
        first lines of every page on a phone — there is no spare column
        to reserve for them there. In flow, the page starts below them."""
        _tutorial(site, "one", "One")
        _set_order(site, ["one"])
        b.build()
        context = browser.new_context(viewport={"width": 375, "height": 700})
        page = context.new_page()
        page.goto(f"{site_url}/tutorials/{MODULE}/one.html")
        row_bottom = page.eval_on_selector(
            ".dl-corner-dock-tl", "el => el.getBoundingClientRect().bottom")
        body_top = page.eval_on_selector(
            "main#dl-body", "el => el.getBoundingClientRect().top")
        assert page.eval_on_selector(
            ".dl-corner-dock-tl", "el => getComputedStyle(el).position") == "static"
        assert body_top >= row_bottom
        context.close()

    def test_a_button_with_nothing_to_forward_to_is_absent_from_the_menu(
            self, site, browser, site_url):
        """One tutorial with no glossary at all has nothing for
        Documentation to show — the same content-presence rule the
        desktop toggle already follows, mirrored here."""
        _tutorial(site, "one", "One")
        _set_order(site, ["one"])
        b.build()
        context = browser.new_context(viewport={"width": 375, "height": 700})
        page = context.new_page()
        page.goto(f"{site_url}/tutorials/{MODULE}/one.html")
        page.click("#dl-mobile-fab")
        assert page.is_hidden("#dl-mobile-item-documentation")
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

    def open_page(self, site, browser, site_url):
        path = site / "tutorials" / MODULE / "lookup.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(LOOKUP_PROSE)
        _glossary(site, "lookup", [LOOKUP_TERM])
        _set_order(site, ["lookup"])
        b.build()
        context = browser.new_context()
        page = context.new_page()
        page.goto(f"{site_url}/tutorials/{MODULE}/lookup.html")
        page.wait_for_selector("#dl-body")
        return context, page

    def test_nothing_is_offered_until_something_is_selected(self, site, browser, site_url):
        context, page = self.open_page(site, browser, site_url)
        assert page.is_hidden(".dl-lookup")
        context.close()

    def test_selecting_a_term_offers_to_look_it_up(self, site, browser, site_url):
        context, page = self.open_page(site, browser, site_url)
        assert page.evaluate(SELECT, "gradient")
        page.wait_for_selector(".dl-lookup:not([hidden])")
        assert "gradient" in page.inner_text(".dl-lookup")
        context.close()

    def test_selecting_a_word_the_reference_does_not_know_offers_nothing(
            self, site, browser, site_url):
        """A reader selecting a sentence to copy must not be interrupted."""
        context, page = self.open_page(site, browser, site_url)
        assert page.evaluate(SELECT, "serendipity")
        page.wait_for_timeout(200)
        assert page.is_hidden(".dl-lookup")
        context.close()

    def test_using_it_opens_the_panel_filtered_to_that_term(self, site, browser, site_url):
        context, page = self.open_page(site, browser, site_url)
        page.evaluate(SELECT, "gradient")
        page.wait_for_selector(".dl-lookup:not([hidden])")
        page.click(".dl-lookup")
        page.wait_for_selector("#dl-reference:not([hidden])")
        shown = page.eval_on_selector_all(
            "#dl-reference-groups dt:not([hidden])", "els => els.map(e => e.textContent)")
        assert shown == ["gradient"]
        context.close()

    def test_the_offer_goes_away_once_it_has_been_used(self, site, browser, site_url):
        """Otherwise it sits over the reading offering the same lookup again."""
        context, page = self.open_page(site, browser, site_url)
        page.evaluate(SELECT, "gradient")
        page.wait_for_selector(".dl-lookup:not([hidden])")
        page.click(".dl-lookup")
        page.wait_for_selector("#dl-reference:not([hidden])")
        assert page.is_hidden(".dl-lookup")
        context.close()
