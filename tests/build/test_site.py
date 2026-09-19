"""The site's own pages and chrome: front page, about, features, settings,
footer, published tools. One test per scenario: a plain tutorial built once
carries every check on the site's chrome and its own pages, and the other
classes hold the scenarios that need a different page or a second build."""

from __future__ import annotations

import json
import re
import sys
import urllib.parse
import zipfile
from pathlib import Path

import pytest
import yaml

from helpers import *  # noqa: F401,F403
from helpers import DEWLAB, FRONTMATTER, CELL, COURSE, SERIES, b

CONTENTS_RUNG = r'<details class="dl-crumb-level dl-crumb-level-4">.*?</details>'


def contents_rung(repo) -> str:
    """The page's own sections, as the innermost rung of the where-you-are
    tree — contents_items_html()'s output, or "" when the page has none."""
    page = built(repo)
    match = re.search(CONTENTS_RUNG, page, re.DOTALL)
    return match.group(0) if match else ""


def sections(count: int, sub: str = "") -> str:
    return "\n".join(f"## Section {n}\n\n{sub}Prose.\n" for n in range(1, count + 1))


class TestBuildingNothing:
    """No tutorials at all: the build returns nothing, fails nothing, and
    writes none of the site's own pages."""

    def test_an_empty_tutorials_folder_builds_nothing_and_does_not_fail(self, repo):
        assert b.build() == []
        assert not (repo / "site" / "index.html").exists()
        assert not (repo / "site" / "features.html").exists()
        assert not (repo / "site" / "all-tutorials.html").exists()


class TestOnePlainTutorial:
    """One tutorial of plain prose (no cells, no sections) in the default
    course, a second course beside it, a hand-written pages/about.md, and
    the real assets — built once. Everything the site promises on that
    build is checked here: the front page and the features page, the about
    page, the settings panel, the corner docks that replaced the top bar,
    the footer's report doors, and the version every asset URL carries."""

    def test_the_site_s_pages_and_chrome_are_all_there(self, repo_with_assets):
        repo = repo_with_assets
        (repo / "pages" / "about.md").write_text(
            "---\ntitle: A Different Title\n---\n\n"
            "# About this project\n\nSomething only this test wrote.\n\n"
            "See the [topic tree](tree.html) for more.\n"
        )
        write(repo, "Some prose.\n")
        course(repo, "web-authoring", {}, title="Web Authoring", card="Pages, styled.",
               code="5N1355 · QQI Level 5", status="live")
        b.build()
        index = (repo / "site" / "index.html").read_text()
        page = built(repo)

        # ---- The front page (index.html) is written at the site root.
        assert (repo / "site" / "index.html").is_file()
        # It needs no Python runtime.
        assert manifest(index)["cells"] == []
        # It ends with the short attribution. Whitespace-normalized:
        # pages/home.md's own line wrapping is real markdown source, not a
        # single-line string, and the markdown converter keeps a paragraph's
        # own internal line breaks rather than collapsing them.
        match = re.search(r'<div class="dl-attribution">\s*(<p>.*?</p>)\s*</div>', index, re.DOTALL)
        assert match, "no dl-attribution paragraph found"
        assert " ".join(match.group(1).split()) == (
            "<p>This site is being actively developed by "
            '<strong><a href="https://github.com/deweydex">Joshua Aaron</a></strong> '
            "(Dublin College Dundrum), with contributions from "
            '<strong><a href="https://github.com/mcgarry">Sean McGarry</a></strong> '
            "(Dublin College Blackrock). To find out more, read "
            '<a href="about.html">About this project</a> or visit '
            '<a href="https://github.com/deweydex/dewlab">the project on GitHub</a>.</p>'
        )
        # Its search box has no hint line, but every other one does: the
        # sentence above the front page's box already says what a search
        # matches; the all-tutorials page has no such sentence.
        front = index[index.index('id="dl-search"'):index.index("dl-search-results")]
        assert "dl-search-hint" not in front and "aria-describedby" not in front
        listing = (repo / "site" / "all-tutorials.html").read_text()
        assert 'id="dl-search-hint"' in listing and 'aria-describedby="dl-search-hint"' in listing
        # The tile for the features page sits under the opening.
        hero = index[index.index('<div class="dl-hero">'):index.index('<div class="dl-audience">')]
        assert 'href="features.html"' in hero
        assert index.index("What do you want to learn?") < index.index('href="computational-methods.html"')
        # The course cards come from the course files: there is nothing
        # hand-written left to disagree with a course page.
        cards = index[index.index("What do you want to learn?"):]
        assert cards.index('href="computational-methods.html"') < cards.index('href="web-authoring.html"')
        assert "<h3>Web Authoring" in cards and "Pages, styled." in cards
        assert "5N1355 · QQI Level 5" in cards
        assert 'data-status="live">Live</span>' in cards
        assert 'href="all-tutorials.html"' in index
        assert 'href="features.html"' in index
        assert "dewstack" not in index

        # ---- The features page is written at the site root.
        features = repo / "site" / "features.html"
        assert features.is_file()
        features_page = features.read_text()
        assert "What dewlab can do" in features_page
        assert "Use dewmini without a tutorial" in features_page
        assert 'href="compose/dewmini.html"' in features_page
        assert manifest(features_page)["cells"] == []

        # ---- The about page is written at the site root, from
        # pages/about.md rather than a hardcoded string in build.py — see
        # read_page(): its content, its title (from the frontmatter) and a
        # markdown link all come through.
        assert (repo / "site" / "about.html").is_file()
        about = (repo / "site" / "about.html").read_text()
        assert "Something only this test wrote." in about
        assert "<title>A Different Title" in about
        assert '<a href="tree.html">topic tree</a>' in about

        # ---- The settings panel: the download sits in the panel and not
        # in the navigation.
        nav = re.search(r'<nav class="dl-nav dl-nav-bottom">.*?</nav>', page, re.DOTALL).group(0)
        assert "dl-download" not in nav
        section = re.search(
            r'<section class="dl-settings-section" id="dl-settings-download">.*?</section>',
            page, re.DOTALL,
        ).group(0)
        assert 'href="../download/sample.html"' in section
        # The front page has no tutorial to download.
        assert (
            '<section class="dl-settings-section" id="dl-settings-download"></section>'
            in index
        )
        # Give Feedback, Appearance and Imports & Exports live behind one
        # corner-dock toggle, Settings, opening #dl-settings — an internal
        # tablist inside it switches between the three, the way Reference's
        # own tabs already do for its three sections. Not the two separate
        # texture/progress toggles this panel originally replaced, and not
        # a toggle of its own for each of the three.
        assert 'id="dl-settings-toggle"' in page
        assert 'aria-controls="dl-settings"' in page
        assert 'id="dl-settings-tab-appearance"' in page
        assert 'id="dl-settings-tab-feedback"' in page
        assert 'id="dl-settings-tab-importsexports"' in page
        assert "dl-texture-toggle" not in page
        assert "dl-progress-toggle" not in page
        assert 'id="dl-appearance-toggle"' not in page
        assert 'id="dl-report-toggle"' not in page
        assert 'id="dl-importsexports-toggle"' not in page

        # ---- Nothing sits above the page. What the top bar held — all
        # tutorials, previous and next, search, contents — is all in the
        # top-left dock's tree or its search bar now, so the bar itself is
        # gone and the page starts at its own heading. Previous and next
        # survive at the foot of the page.
        assert 'id="dl-chrome"' not in page
        assert "dl-nav-top" not in page
        assert "dl-masthead" not in page
        assert '<nav class="dl-nav dl-nav-bottom">' in page
        # The identity lives in the top-left corner dock.
        start = page.index('<div class="dl-corner-dock dl-corner-dock-tl"')
        depth = 0
        end = start
        for tag in re.finditer(r"<div\b|</div>", page[start:]):
            depth += 1 if tag.group(0) == "<div" else -1
            if depth == 0:
                end = start + tag.end()
                break
        corner = page[start:end]
        assert "dl-wordmark" in corner
        assert "dl-crumbtrail" in corner
        assert "dl-nav-search" in corner
        assert 'id="dl-reference-toggle"' in corner
        assert "dl-seriesnav" not in page
        assert "dl-documentation" not in page
        # The right dock is one stack of three tabs with icons: Notes,
        # Python and Settings — Give Feedback, Appearance and Imports &
        # Exports no longer each get their own.
        start = page.index('<div class="dl-corner-dock dl-corner-dock-tr"')
        end = page.index("<!-- Phone-only", start)
        dock = page[start:end]
        ids = re.findall(r'id="(dl-[a-z]+-toggle)"', dock)
        assert ids == ["dl-yourwork-toggle", "dl-python-toggle", "dl-settings-toggle"]
        assert dock.count('class="dl-tab-icon"') == 3
        assert "dl-corner-dock-bl" not in page
        assert "dl-corner-dock-br" not in page
        # The search line under the wordmark is the input itself.
        # nav_search_html() — a magnifier and "Search for a topic" between
        # the wordmark and the tree, and the line is the search widget's own
        # input with those words as its placeholder: nothing to open first,
        # no second bar (7.169). It has to be the input itself: a summary
        # styled to look like a field read as a search bar that did nothing
        # when typed into (7.166).
        start = page.index('<div class="dl-corner-dock dl-corner-dock-tl"')
        end = page.index('<div class="dl-corner-dock dl-corner-dock-tr"', start)
        left = page[start:end]
        line = left.index('<div class="dl-nav-search">')
        assert left.index("dl-wordmark") < line < left.index('<nav class="dl-crumbtrail"')
        field = re.search(r'<input type="search" id="dl-nav-search-input" class="dl-search-input"[^>]*>', left)
        assert field and 'placeholder="Search for a topic"' in field.group(0)
        assert "<details" not in left[line:left.index('<nav class="dl-crumbtrail"')]
        assert "<summary" not in left[line:left.index('<nav class="dl-crumbtrail"')]

        # ---- Prose with no sections gets no contents rung.
        assert contents_rung(repo) == ""

        # ---- The footer's report doors are on by default: feedback_enabled()
        # is true without a config file, and the doors are on the tutorial
        # page and on the front page.
        assert b.feedback_enabled() is True
        assert '<details class="dl-report-doors">' in page
        assert "Something wrong on this page? Tell us." in page
        assert "I have a question" in page
        assert "It gives an error" in page
        assert "The page is wrong, or I could not follow it" in page
        assert "github.com/deweydex/dewlab/discussions/new" in page
        assert "github.com/deweydex/dewlab/issues/new?" in page
        assert "template=report.yml" in page
        assert "page=sample" in page
        assert "version=2026.08.23.1" in page
        assert "kind=It+gives+an+error" in page
        assert "kind=The+page+is+wrong" in page
        assert "Something wrong on this page? Tell us." in index
        assert "discussions/new" in index

        # ---- Asset versions (cache-busting: without a version in the URL a
        # browser keeps an old stylesheet forever, and the bug looks like
        # page breakage rather than caching; checked against the real
        # assets, since a version of a file that is not there proves
        # nothing). The stylesheet and the runtime both carry a version,
        # and so does the maths stylesheet.
        markup = page + index
        assert re.search(r"tutorial-style\.css\?v=[0-9a-f]{8}", markup)
        assert re.search(r"tutorial-runtime\.js\?v=[0-9a-f]{8}", markup)
        assert re.search(r"katex\.min\.css\?v=[0-9a-f]{8}", markup)
        # Two repositories in one process do not share a version: the cache
        # is keyed by path. Keyed by name, a second build in the same
        # process would be handed the first one's hash.
        mine = b.asset_version("tutorial-style.css")
        assert mine != "missing"
        assert len(b._ASSET_VERSIONS) >= 1
        assert all(k.startswith("/") for k in b._ASSET_VERSIONS)


class TestPageCardsAndSections:
    """```card fences and [[name]] generated-block markers — the two
    pieces pages/home.md needed that pages/about.md never has. See
    parse_card()/render_card()/place_page_cards() and
    extract_generated_blocks()/place_generated_blocks() in build.py.
    Three home pages, each built once: one with a plain card and a wide
    one beside a generated block and a wrapped section (and a feature
    list on the features page), one with a status card and cards kept
    apart by prose, and one with two adjacent cards — the exact grid and
    card counts keep those three apart. Then the ways a card or a marker
    fails the build."""

    def home(self, repo, body: str) -> None:
        (repo / "pages" / "home.md").write_text(f"---\ntitle: dewlab\n---\n\n{body}")

    def features(self, repo, body: str) -> None:
        (repo / "pages" / "features.md").write_text(f"---\ntitle: What dewlab can do\n---\n\n{body}")

    def test_cards_markers_and_wrapped_sections_render_on_the_site_s_own_pages(self, repo):
        self.home(repo, (
            "[[search-box]]\n\n"
            "```card\n"
            "url: features.html\n"
            "### What dewlab can do\n"
            "The tools built into every page.\n"
            "```\n\n"
            "```card\n"
            "url: features.html\n"
            "wide: true\n"
            "### What dewlab can do\n"
            "```\n\n"
            '<div class="dl-audience">\n\n'
            "## A Section\n\n"
            "Some **bold** text and a [link](features.html).\n\n"
            "</div>\n"
        ))
        self.features(repo, (
            '<ul class="dl-feature-list">\n\n'
            "- **First.** One thing.\n"
            "- **Second.** Another thing.\n\n"
            "</ul>\n"
        ))
        write(repo, "Prose.\n")
        b.build()
        page = (repo / "site" / "index.html").read_text()
        # A card fence renders as a module card.
        assert (
            '<a class="dl-module-card" href="features.html">'
            "<h3>What dewlab can do</h3>"
            "<p>The tools built into every page.</p></a>"
        ) in page
        # A wide card gets the wide class, and no meta or badge.
        assert '<a class="dl-module-card dl-module-card-wide" href="features.html">' in page
        assert "dl-module-card-badge" not in page
        assert "dl-module-card-meta" not in page
        # The search box marker is replaced.
        assert 'id="dl-search-input"' in page
        assert "[[search-box]]" not in page
        # A dl-audience section's markdown converts properly. Regression
        # test: Python-Markdown treats a raw <div> block as opaque HTML
        # through to its closing tag, so a heading or paragraph written
        # inside one would otherwise reach the page as literal, unconverted
        # markdown — see convert_page_wrapper_bodies().
        assert "<h2" in page and ">A Section</h2>" in page
        assert "<strong>bold</strong>" in page
        assert '<a href="features.html">link</a>' in page
        assert "## A Section" not in page
        # A dl-feature-list's markdown converts to real list items. The
        # same raw-HTML-block problem, met on a <ul> rather than a <div>:
        # a markdown bullet list converts to its own <ul>...</ul>, which
        # would double up inside a wrapper that already supplies the real
        # one — convert_page_wrapper_bodies() strips the redundant inner
        # tag for a `ul` wrapper specifically.
        page = (repo / "site" / "features.html").read_text()
        assert (
            '<ul class="dl-feature-list">\n'
            "<li><strong>First.</strong> One thing.</li>\n"
            "<li><strong>Second.</strong> Another thing.</li>\n"
            "</ul>"
        ) in page
        assert "- **First.**" not in page

    def test_a_status_card_and_cards_separated_by_other_content_get_separate_grids(self, repo):
        self.home(repo, (
            "```card\n"
            "url: computational-methods.html\n"
            "status: beta\n"
            "meta: 5N0554 · QQI Level 5\n"
            "### Computational Methods\n"
            "```\n\n"
            "```card\n"
            "url: a.html\n"
            "### A\n"
            "```\n\n"
            "Some prose in between.\n\n"
            "```card\n"
            "url: b.html\n"
            "### B\n"
            "```\n"
        ))
        write(repo, "Prose.\n")
        b.build()
        page = (repo / "site" / "index.html").read_text()
        # Status and meta render as badge and meta span.
        assert '<span class="dl-module-card-badge" data-status="beta">Beta</span>' in page
        assert '<span class="dl-module-card-meta">5N0554 · QQI Level 5</span>' in page
        assert page.count('<div class="dl-module-grid">') == 2

    def test_adjacent_cards_share_one_module_grid(self, repo):
        self.home(repo, (
            "```card\n"
            "url: a.html\n"
            "### A\n"
            "```\n\n"
            "```card\n"
            "url: b.html\n"
            "### B\n"
            "```\n"
        ))
        write(repo, "Prose.\n")
        b.build()
        page = (repo / "site" / "index.html").read_text()
        assert page.count('<div class="dl-module-grid">') == 1
        assert page.count("dl-module-card\" href") == 2

    def test_a_card_with_no_url_fails_the_build(self, repo):
        self.home(repo, "```card\n### A\n```\n")
        write(repo, "Prose.\n")
        with pytest.raises(b.BuildError, match="url"):
            b.build()

    def test_a_card_with_no_heading_fails_the_build(self, repo):
        self.home(repo, "```card\nurl: a.html\nJust prose, no heading.\n```\n")
        write(repo, "Prose.\n")
        with pytest.raises(b.BuildError, match="heading"):
            b.build()

    def test_an_unknown_generated_block_fails_the_build(self, repo):
        self.home(repo, "[[not-a-real-block]]\n")
        write(repo, "Prose.\n")
        with pytest.raises(b.BuildError, match="not-a-real-block"):
            b.build()

    def test_maths_works_in_a_cards_own_body_a_wrapped_section_and_the_pages_own_prose(self, repo):
        # convert_prose_with_math() is the same self-contained
        # extract-then-place dance the tutorial body's own maths already
        # gets, applied to three surfaces that each convert their own
        # markdown separately: a card's body (parse_card), a wrapped
        # section (convert_page_wrapper_bodies), and the page's own
        # top-level prose (read_page).
        self.home(repo, (
            r"The page opens with $a^2 + b^2 = c^2$." + "\n\n"
            "```card\n"
            "url: features.html\n"
            "### A card\n"
            "Its area is $\\pi r^2$.\n"
            "```\n\n"
            '<div class="dl-audience">\n\n'
            "A section with $x^2$ in it.\n\n"
            "</div>\n"
        ))
        write(repo, "Prose.\n")
        b.build()
        page = (repo / "site" / "index.html").read_text()
        assert '<span class="dl-math">a^2 + b^2 = c^2</span>' in page
        assert '<span class="dl-math">\\pi r^2</span>' in page
        assert '<span class="dl-math">x^2</span>' in page
        # The manifest turns the KaTeX bundle fetch on for this page —
        # renderMaths() (tutorial-runtime.js) checks manifest.math before
        # it ever looks for a .dl-math span.
        assert manifest(page)["math"] is True

    def test_a_page_with_no_maths_at_all_carries_no_math_flag(self, repo):
        self.home(repo, "Just prose, no maths anywhere.\n")
        write(repo, "Prose.\n")
        b.build()
        page = (repo / "site" / "index.html").read_text()
        assert "dl-math" not in page
        assert "math" not in manifest(page)


class TestTheAboutPage:
    """about.html: hand-written content, from pages/about.md rather than a
    hardcoded string in build.py — see read_page(). The page that builds
    is checked in TestOnePlainTutorial; these are the two ways it fails."""

    def test_a_missing_pages_about_md_fails_the_build(self, repo):
        (repo / "pages" / "about.md").unlink()
        write(repo, "Prose.\n")
        with pytest.raises(b.BuildError, match="pages/about.md"):
            b.build()

    def test_frontmatter_with_no_title_fails_the_build(self, repo):
        (repo / "pages" / "about.md").write_text("---\nnot_title: x\n---\n\nBody.\n")
        write(repo, "Prose.\n")
        with pytest.raises(b.BuildError, match="title"):
            b.build()


class TestTheContentsOfAPage:
    """contents_items_html() — the page's own sections, as the innermost
    rung of the where-you-are tree rather than a list in the page. Three
    pages: three sections, one section, and sections with sub-headings
    (one nested, one repeated, one distinct). A page with no sections is
    in TestOnePlainTutorial; a downloadable copy in TestTheDownloadableCopy."""

    def test_three_sections_give_the_page_its_own_closed_rung_and_the_front_page_none(self, repo):
        """The page's own name is the caret: it opens straight onto the
        sections, no "Contents" rung in between, and starts closed — a
        reader arriving at a tutorial should meet the tutorial, not a list
        of its parts. The front page (index.html) has no such rung."""
        write(repo, sections(3))
        b.build()
        toc = contents_rung(repo)
        assert 'href="#section-1"' in toc
        assert 'href="#section-3"' in toc
        assert "3 sections" in toc
        page = built(repo)
        assert '<details class="dl-crumb-level dl-crumb-level-4">' in page
        assert '<details class="dl-crumb-level dl-crumb-level-4" open' not in page
        assert "dl-crumb-level-5" not in page
        assert "<summary>Contents" not in page
        assert "dl-crumb-level-4" not in (repo / "site" / "index.html").read_text()

    def test_one_section_does_not_get_a_contents_rung(self, repo):
        """A contents list for a single heading is furniture — the
        tutorial's own rung is then a plain line, no caret with nothing
        behind it."""
        write(repo, sections(1))
        b.build()
        assert contents_rung(repo) == ""
        assert 'class="dl-crumb-current dl-crumb-level-4"' in built(repo)

    def test_sub_headings_nest_and_a_repeated_one_is_left_out_while_a_distinct_one_is_kept(self, repo):
        """Five entries reading "Your turn" are a list nobody can choose from."""
        write(
            repo,
            "## First\n\nProse.\n\n### Detail\n\nProse.\n\n### Your turn\n\nProse.\n\n"
            "## Second\n\nProse.\n\n### Your turn\n\nProse.\n\n### Something distinct\n\nProse.\n",
        )
        b.build()
        toc = contents_rung(repo)
        # Sub-headings nest under their section.
        assert re.search(r'href="#first".*?<div role="list">.*?href="#detail".*?</div>', toc, re.DOTALL)
        # A sub-heading that repeats is left out.
        assert "Your turn" not in toc
        assert 'href="#first"' in toc
        assert 'href="#second"' in toc
        # A sub-heading that appears once is kept.
        assert "Something distinct" in contents_rung(repo)


class TestTheDownloadableCopy:
    """A tutorial with a cell and three sections, built with its
    downloadable copy (standalone=True) from the real assets: what the
    copy keeps of the settings panel, the docks and the contents rung,
    what it drops of the cross-file navigation, and what the site's own
    copy of the page tells the runtime to fetch. Then the export's one
    failure path."""

    def test_the_copy_keeps_the_panel_the_docks_and_its_own_contents_and_nothing_that_links_out(
        self, repo_with_assets
    ):
        write(repo_with_assets, "```python exec\nid: c\n1 + 1\n```\n\n" + sections(3))
        b.build(standalone=True)
        page = (repo_with_assets / "site" / "download" / "sample.html").read_text()
        # A downloadable copy does not offer its own download.
        assert (
            '<section class="dl-settings-section" id="dl-settings-download"></section>'
            in page
        )
        assert "download/sample.html" not in page
        # It keeps the rest of the panel.
        assert 'id="dl-settings-toggle"' in page
        assert 'id="dl-settings-work"' in page
        assert 'id="dl-settings-texture"' in page
        # It keeps the contents rung and nothing else of the tree: its
        # links are inside the file, so they work from a student's disk —
        # unlike the rest of the tree, which links to other files.
        markup = outside_style_and_script(page)
        assert 'href="#section-1"' in markup
        assert "dl-crumb-level-4" in markup
        assert "dl-crumb-level-3" not in markup
        # It keeps the docks without the navigation.
        assert "dl-corner-dock" in page
        # The inlined stylesheet and runtime both name .dl-nav in their own
        # text (the runtime redraws previous/next for a chosen course), so
        # only the markup outside both is checked.
        assert "dl-nav" not in outside_style_and_script(page)
        # What the runtime fetches for itself is versioned: it is not in
        # the markup, so the page cannot bust it — the manifest can.
        versions = manifest(built(repo_with_assets))["assetVersions"]
        assert re.fullmatch(r"[0-9a-f]{8}", versions["tutorial_tools.py"])

    def test_a_replacement_that_finds_nothing_stops_the_build(self):
        """A silent no-op here is a downloadable copy with no stylesheet."""
        with pytest.raises(b.BuildError, match="drifted apart"):
            b.replace_once("<p>a page</p>", "<not-here>", "x", "the thing")


class TestWhatTheRuntimeReads:
    """Two JSON files the page scripts fetch: the search index, and the
    routes file the runtime draws a course's chrome from. One scenario: a
    tutorial with a practice page, listed in two courses."""

    def test_the_search_index_and_routes_json_carry_every_course_and_page(self, repo):
        write(repo, "Prose.\n")
        practice(repo, "sample")
        course(repo, "zz-other", {"Also": ["sample"]}, title="Other Course")
        b.build()
        # Search entries carry the course (a practice page gets no entry).
        [entry] = json.loads((repo / "site" / "assets" / "search-index.json").read_text())
        assert entry["id"] == "sample"
        assert entry["url"] == "tutorials/sample.html"
        assert entry["module"] == "computational-methods"
        assert entry["moduleTitle"] == "Computational Methods"
        assert entry["series"] == "Python fundamentals"
        assert entry["courses"] == ["computational-methods", "zz-other"]
        # routes.json lists every course with its pages.
        routes = json.loads((repo / "site" / "assets" / "routes.json").read_text())["courses"]
        assert [c["id"] for c in routes] == ["computational-methods", "zz-other"]
        first = routes[0]
        assert first["title"] == "Computational Methods" and first["url"] == "computational-methods.html"
        [series] = first["series"]
        assert series["key"] == "python-fundamentals" and series["title"] == "Python fundamentals"
        [entry] = series["tutorials"]
        assert entry == {
            "id": "sample", "title": "A Title", "url": "tutorials/sample.html",
            "practice": {"id": "sample-practice", "title": "A Title", "url": "tutorials/sample-practice.html"},
        }
        assert routes[1]["series"][0]["title"] == "Also"


class TestAssetVersions:
    """Cache-busting across builds. That every asset URL carries a version
    is checked in TestOnePlainTutorial; this is what happens to the
    version when the site is built again — unchanged assets keep it,
    an edited asset changes it."""

    def test_the_same_assets_give_the_same_version_and_an_edit_changes_it(self, repo_with_assets):
        """Otherwise every publish invalidates every cache for no reason."""
        write(repo_with_assets, "Some prose.\n")
        b.build()
        first = re.search(r"tutorial-style\.css\?v=([0-9a-f]{8})", built(repo_with_assets))
        b._ASSET_VERSIONS.clear()
        b.build()
        again = re.search(r"tutorial-style\.css\?v=([0-9a-f]{8})", built(repo_with_assets))
        assert first.group(1) == again.group(1)

        # Editing an asset changes its version.
        style = repo_with_assets / "assets" / "tutorial-style.css"
        style.write_text(style.read_text() + "\n.something-new { color: red; }\n")
        b._ASSET_VERSIONS.clear()
        b.build()
        after = re.search(r"tutorial-style\.css\?v=([0-9a-f]{8})", built(repo_with_assets))
        assert first.group(1) != after.group(1)


def test_the_marking_workbench_the_topic_pair_game_and_the_topic_editor_are_published(repo, monkeypatch):
    # Nothing on the site links to /dewmark/, so a broken copy step would go
    # unnoticed until somebody typed the address.
    workbench = repo / "dewmark" / "workbench"
    workbench.mkdir(parents=True)
    (workbench / "index.html").write_text("<h1>dewmark marking workbench</h1>")
    monkeypatch.setattr(b, "DEWMARK_WORKBENCH", workbench)
    # The pair game's README is written for somebody reading the
    # repository, not a visitor.
    game = repo / "topic_tree_game"
    game.mkdir(parents=True)
    (game / "index.html").write_text("<h1>topic pairs</h1>")
    (game / "help.html").write_text("<h1>how to play</h1>")
    (game / "README.md").write_text("how the loop works")
    monkeypatch.setattr(b, "TOPIC_GAME", game)
    # The topic editor is published beside the game, on the same terms:
    # one page, nothing linking to it.
    editor = repo / "topic_editor"
    editor.mkdir(parents=True)
    (editor / "index.html").write_text("<h1>topic editor</h1>")
    (editor / "help.html").write_text("<h1>how it works</h1>")
    (editor / "README.md").write_text("for a reader of the repository")
    monkeypatch.setattr(b, "TOPIC_EDITOR", editor)

    b.build()

    published = b.OUT / "dewmark" / "index.html"
    assert published.is_file()
    assert published.read_text() == (workbench / "index.html").read_text()
    # The topic pair game is published without its README.
    assert (b.OUT / "topic_tree_game" / "index.html").is_file()
    assert (b.OUT / "topic_tree_game" / "help.html").is_file()
    assert not (b.OUT / "topic_tree_game" / "README.md").exists()
    # The topic editor likewise.
    assert (b.OUT / "topic_editor" / "index.html").read_text() == "<h1>topic editor</h1>"
    assert (b.OUT / "topic_editor" / "help.html").is_file()
    assert not (b.OUT / "topic_editor" / "README.md").exists()


def test_no_workbench_game_or_editor_folder_is_not_an_error(repo, monkeypatch):
    monkeypatch.setattr(b, "DEWMARK_WORKBENCH", repo / "dewmark" / "workbench")
    monkeypatch.setattr(b, "TOPIC_GAME", repo / "topic_tree_game")
    monkeypatch.setattr(b, "TOPIC_EDITOR", repo / "topic_editor")

    b.build()

    assert not (b.OUT / "dewmark").exists()
    assert not (b.OUT / "topic_tree_game").exists()
    assert not (b.OUT / "topic_editor").exists()


class TestFeedbackFooter:
    """The footer's "three doors" report disclosure. On by default (checked
    in TestOnePlainTutorial); planning/feedback.yaml is the kill switch.
    Here: the switch turned off, and the URL and template helpers on
    their own."""

    def test_doors_gone_when_switched_off(self, repo, monkeypatch):
        (repo / "planning").mkdir(parents=True, exist_ok=True)
        (repo / "planning" / "feedback.yaml").write_text("enabled: false\n")
        write(repo, "# Sample\n\nSome text.")
        b.build()

        # feedback_enabled() reads the config file.
        assert b.feedback_enabled() is False
        page = built(repo)
        assert "Something wrong on this page?" not in page
        assert "dl-report-doors" not in page
        assert "issues/new" not in page
        assert "discussions/new" not in page

    def test_the_issue_url_carries_page_version_and_kind_and_the_kinds_match_the_template(self):
        url = b.report_issue_url("first-steps", "2026.09.01.2")
        assert url.startswith("https://github.com/deweydex/dewlab/issues/new?")
        assert "page=first-steps" in url
        assert "version=2026.09.01.2" in url
        assert "template=report.yml" in url
        assert "kind=" not in url
        # It carries the kind when given.
        url = b.report_issue_url("a/b", "1", kind="The page is wrong, or I could not follow it")
        assert "kind=The+page+is+wrong" in url
        # report_doors_html()'s kinds match the issue template.
        template = yaml.safe_load(
            (b.ROOT / ".github" / "ISSUE_TEMPLATE" / "report.yml").read_text()
        )
        options = next(
            f["attributes"]["options"] for f in template["body"] if f.get("id") == "kind"
        )
        html = b.report_doors_html("a/b", "1")
        assert f"kind={urllib.parse.quote_plus(options[0])}" in html
        assert f"kind={urllib.parse.quote_plus(options[1])}" in html
        assert options[2] not in html
