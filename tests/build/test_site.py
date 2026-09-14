"""The site's own pages and chrome: front page, about, features, settings, footer, published tools."""

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

class TestBuildingNothing:
    def test_an_empty_tutorials_folder_builds_nothing_and_does_not_fail(self, repo):
        assert b.build() == []


class TestTheFrontPage:
    """index.html: the landing page, static and tutorial-data-free — the
    module listing itself now lives on all-tutorials.html (TestAllTutorialsPage)."""

    def test_it_is_written_at_the_site_root(self, repo):
        write(repo, "Prose.\n")
        b.build()
        assert (repo / "site" / "index.html").is_file()

    def test_it_needs_no_python_runtime(self, repo):
        write(repo, "Prose.\n")
        b.build()
        assert manifest((repo / "site" / "index.html").read_text())["cells"] == []

    def test_it_ends_with_the_short_attribution(self, repo):
        # Whitespace-normalized: pages/home.md's own line wrapping is real
        # markdown source, not a single-line string, and the markdown
        # converter keeps a paragraph's own internal line breaks rather
        # than collapsing them.
        write(repo, "Prose.\n")
        b.build()
        index = (repo / "site" / "index.html").read_text()
        match = re.search(r'<div class="dl-attribution">\s*(<p>.*?</p>)\s*</div>', index, re.DOTALL)
        assert match, "no dl-attribution paragraph found"
        assert " ".join(match.group(1).split()) == (
            "<p>This site is being actively developed by "
            '<strong><a href="https://github.com/deweydex">Joshua Aaron</a></strong> '
            "(Dublin College Dundrum), with contributions from "
            '<strong><a href="https://github.com/mcgarry">Sean McGarry</a></strong> '
            "(Dublin College Blackrock).</p>"
        )

    def test_the_course_cards_come_from_the_course_files(self, repo):
        # There is nothing hand-written left to disagree with a course page.
        write(repo, "Prose.\n")
        course(repo, "web-authoring", {}, title="Web Authoring", card="Pages, styled.",
               code="5N1355 · QQI Level 5", status="live")
        b.build()
        index = (repo / "site" / "index.html").read_text()
        cards = index[index.index("Choose a course"):]
        assert cards.index('href="computational-methods.html"') < cards.index('href="web-authoring.html"')
        assert "<h3>Web Authoring" in cards and "Pages, styled." in cards
        assert "5N1355 · QQI Level 5" in cards
        assert 'data-status="live">Live</span>' in cards
        assert 'href="all-tutorials.html"' in index
        assert 'href="features.html"' in index
        assert "dewstack" not in index

    def test_the_features_page_is_written_at_the_site_root(self, repo):
        write(repo, "Prose.\n")
        b.build()
        features = repo / "site" / "features.html"
        assert features.is_file()
        page = features.read_text()
        assert "What dewlab can do" in page
        assert "Use dewmini without a tutorial" in page
        assert 'href="compose/dewmini.html"' in page
        assert manifest(page)["cells"] == []

    def test_no_tutorials_means_no_front_page(self, repo):
        assert b.build() == []
        assert not (repo / "site" / "index.html").exists()
        assert not (repo / "site" / "features.html").exists()
        assert not (repo / "site" / "all-tutorials.html").exists()


class TestPageCardsAndSections:
    """```card fences and [[name]] generated-block markers — the two
    pieces pages/home.md needed that pages/about.md never has. See
    parse_card()/render_card()/place_page_cards() and
    extract_generated_blocks()/place_generated_blocks() in build.py."""

    def home(self, repo, body: str) -> None:
        (repo / "pages" / "home.md").write_text(f"---\ntitle: dewlab\n---\n\n{body}")

    def test_a_card_fence_renders_as_a_module_card(self, repo):
        self.home(repo, (
            "```card\n"
            "url: features.html\n"
            "### What dewlab can do\n"
            "The tools built into every page.\n"
            "```\n"
        ))
        write(repo, "Prose.\n")
        b.build()
        page = (repo / "site" / "index.html").read_text()
        assert (
            '<a class="dl-module-card" href="features.html">'
            "<h3>What dewlab can do</h3>"
            "<p>The tools built into every page.</p></a>"
        ) in page

    def test_a_wide_card_gets_the_wide_class_and_no_meta_or_badge(self, repo):
        self.home(repo, (
            "```card\n"
            "url: features.html\n"
            "wide: true\n"
            "### What dewlab can do\n"
            "```\n"
        ))
        write(repo, "Prose.\n")
        b.build()
        page = (repo / "site" / "index.html").read_text()
        assert '<a class="dl-module-card dl-module-card-wide" href="features.html">' in page
        assert "dl-module-card-badge" not in page
        assert "dl-module-card-meta" not in page

    def test_status_and_meta_render_as_badge_and_meta_span(self, repo):
        self.home(repo, (
            "```card\n"
            "url: computational-methods.html\n"
            "status: beta\n"
            "meta: 5N0554 · QQI Level 5\n"
            "### Computational Methods\n"
            "```\n"
        ))
        write(repo, "Prose.\n")
        b.build()
        page = (repo / "site" / "index.html").read_text()
        assert '<span class="dl-module-card-badge" data-status="beta">Beta</span>' in page
        assert '<span class="dl-module-card-meta">5N0554 · QQI Level 5</span>' in page

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

    def test_cards_separated_by_other_content_get_separate_grids(self, repo):
        self.home(repo, (
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
        assert page.count('<div class="dl-module-grid">') == 2

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

    def test_the_search_box_marker_is_replaced(self, repo):
        self.home(repo, "[[search-box]]\n")
        write(repo, "Prose.\n")
        b.build()
        page = (repo / "site" / "index.html").read_text()
        assert 'id="dl-search-input"' in page
        assert "[[search-box]]" not in page

    def test_an_unknown_generated_block_fails_the_build(self, repo):
        self.home(repo, "[[not-a-real-block]]\n")
        write(repo, "Prose.\n")
        with pytest.raises(b.BuildError, match="not-a-real-block"):
            b.build()

    def test_a_dl_audience_section_s_markdown_converts_properly(self, repo):
        # Regression test: Python-Markdown treats a raw <div> block as
        # opaque HTML through to its closing tag, so a heading or paragraph
        # written inside one would otherwise reach the page as literal,
        # unconverted markdown — see convert_page_wrapper_bodies().
        self.home(repo, (
            '<div class="dl-audience">\n\n'
            "## A Section\n\n"
            "Some **bold** text and a [link](features.html).\n\n"
            "</div>\n"
        ))
        write(repo, "Prose.\n")
        b.build()
        page = (repo / "site" / "index.html").read_text()
        assert "<h2" in page and ">A Section</h2>" in page
        assert "<strong>bold</strong>" in page
        assert '<a href="features.html">link</a>' in page
        assert "## A Section" not in page

    def features(self, repo, body: str) -> None:
        (repo / "pages" / "features.md").write_text(f"---\ntitle: What dewlab can do\n---\n\n{body}")

    def test_a_dl_feature_list_s_markdown_converts_to_real_list_items(self, repo):
        # The same raw-HTML-block problem, met on a <ul> rather than a
        # <div>: a markdown bullet list converts to its own <ul>...</ul>,
        # which would double up inside a wrapper that already supplies the
        # real one — convert_page_wrapper_bodies() strips the redundant
        # inner tag for a `ul` wrapper specifically.
        self.features(repo, (
            '<ul class="dl-feature-list">\n\n'
            "- **First.** One thing.\n"
            "- **Second.** Another thing.\n\n"
            "</ul>\n"
        ))
        write(repo, "Prose.\n")
        b.build()
        page = (repo / "site" / "features.html").read_text()
        assert (
            '<ul class="dl-feature-list">\n'
            "<li><strong>First.</strong> One thing.</li>\n"
            "<li><strong>Second.</strong> Another thing.</li>\n"
            "</ul>"
        ) in page
        assert "- **First.**" not in page


class TestTheAboutPage:
    """about.html: hand-written content, from pages/about.md rather than a
    hardcoded string in build.py — see read_page()."""

    def test_the_about_page_is_written_at_the_site_root(self, repo):
        write(repo, "Prose.\n")
        b.build()
        assert (repo / "site" / "about.html").is_file()

    def test_content_comes_from_pages_about_md(self, repo):
        (repo / "pages" / "about.md").write_text(
            "---\ntitle: About this project\n---\n\n"
            "# About this project\n\nSomething only this test wrote.\n"
        )
        write(repo, "Prose.\n")
        b.build()
        page = (repo / "site" / "about.html").read_text()
        assert "Something only this test wrote." in page

    def test_the_title_comes_from_the_pages_frontmatter(self, repo):
        (repo / "pages" / "about.md").write_text(
            "---\ntitle: A Different Title\n---\n\nBody.\n"
        )
        write(repo, "Prose.\n")
        b.build()
        page = (repo / "site" / "about.html").read_text()
        assert "<title>A Different Title" in page

    def test_a_markdown_link_renders_as_a_real_link(self, repo):
        (repo / "pages" / "about.md").write_text(
            "---\ntitle: About this project\n---\n\n"
            "See the [topic tree](tree.html) for more.\n"
        )
        write(repo, "Prose.\n")
        b.build()
        page = (repo / "site" / "about.html").read_text()
        assert '<a href="tree.html">topic tree</a>' in page

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


class TestTheSettingsPanel:
    def test_the_download_sits_in_the_panel_and_not_in_the_navigation(self, repo):
        write(repo, "Some prose.\n")
        b.build()
        page = built(repo)
        nav = re.search(r'<nav class="dl-nav dl-nav-bottom">.*?</nav>', page, re.DOTALL).group(0)
        assert "dl-download" not in nav
        section = re.search(
            r'<section class="dl-settings-section" id="dl-settings-download">.*?</section>',
            page, re.DOTALL,
        ).group(0)
        assert 'href="../download/sample.html"' in section

    def test_the_contents_page_has_no_tutorial_to_download(self, repo):
        write(repo, "Some prose.\n")
        b.build()
        index = (repo / "site" / "index.html").read_text()
        assert (
            '<section class="dl-settings-section" id="dl-settings-download"></section>'
            in index
        )

    def test_one_control_opens_it(self, repo):
        """Settings now lives behind two corner-dock toggles rather than
        one — Appearance and Imports & Exports, each opening the same
        #dl-appearance panel to a different pane — not the two separate
        texture/progress toggles this panel originally replaced."""
        write(repo, "Some prose.\n")
        b.build()
        page = built(repo)
        assert 'id="dl-appearance-toggle"' in page
        assert 'id="dl-importsexports-toggle"' in page
        assert 'aria-controls="dl-appearance"' in page
        assert "dl-texture-toggle" not in page
        assert "dl-progress-toggle" not in page
        assert "dl-settings-toggle" not in page

    def test_a_downloadable_copy_does_not_offer_its_own_download(self, repo_with_assets):
        write(repo_with_assets, "Some prose.\n")
        b.build(standalone=True)
        page = (repo_with_assets / "site" / "download" / "sample.html").read_text()
        assert (
            '<section class="dl-settings-section" id="dl-settings-download"></section>'
            in page
        )
        assert "download/sample.html" not in page

    def test_a_downloadable_copy_keeps_the_rest_of_the_panel(self, repo_with_assets):
        write(repo_with_assets, "```python exec\nid: c\n1 + 1\n```\n")
        b.build(standalone=True)
        page = (repo_with_assets / "site" / "download" / "sample.html").read_text()
        assert 'id="dl-appearance-toggle"' in page
        assert 'id="dl-settings-work"' in page
        assert 'id="dl-settings-texture"' in page



class TestTheContentsOfAPage:
    """contents_items_html() — the page's own sections, as the innermost
    rung of the where-you-are tree rather than a list in the page."""

    TOC = r'<details class="dl-crumb-level dl-crumb-level-4">.*?</details>'

    def toc(self, repo) -> str:
        page = built(repo)
        match = re.search(self.TOC, page, re.DOTALL)
        return match.group(0) if match else ""

    def sections(self, count: int, sub: str = "") -> str:
        return "\n".join(f"## Section {n}\n\n{sub}Prose.\n" for n in range(1, count + 1))

    def test_a_page_with_sections_gets_a_contents_rung(self, repo):
        write(repo, self.sections(3))
        b.build()
        toc = self.toc(repo)
        assert 'href="#section-1"' in toc
        assert 'href="#section-3"' in toc
        assert "3 sections" in toc

    def test_it_is_the_tutorials_own_rung_which_starts_closed(self, repo):
        """The page's own name is the caret: it opens straight onto the
        sections, no "Contents" rung in between, and starts closed — a
        reader arriving at a tutorial should meet the tutorial, not a list
        of its parts."""
        write(repo, self.sections(3))
        b.build()
        page = built(repo)
        assert '<details class="dl-crumb-level dl-crumb-level-4">' in page
        assert '<details class="dl-crumb-level dl-crumb-level-4" open' not in page
        assert "dl-crumb-level-5" not in page
        assert "<summary>Contents" not in page

    def test_one_section_does_not_get_a_contents_rung(self, repo):
        """A contents list for a single heading is furniture — the
        tutorial's own rung is then a plain line, no caret with nothing
        behind it."""
        write(repo, self.sections(1))
        b.build()
        assert self.toc(repo) == ""
        assert 'class="dl-crumb-current dl-crumb-level-4"' in built(repo)

    def test_prose_with_no_sections_does_not_either(self, repo):
        write(repo, "Just prose, no headings at all.\n")
        b.build()
        assert self.toc(repo) == ""

    def test_sub_headings_nest_under_their_section(self, repo):
        write(repo, "## First\n\nProse.\n\n### Detail\n\nProse.\n\n## Second\n\nProse.\n")
        b.build()
        toc = self.toc(repo)
        assert re.search(r'href="#first".*?<div role="list">.*?href="#detail".*?</div>', toc, re.DOTALL)

    def test_a_sub_heading_that_repeats_is_left_out(self, repo):
        """Five entries reading "Your turn" are a list nobody can choose from."""
        write(
            repo,
            "## First\n\nProse.\n\n### Your turn\n\nProse.\n\n"
            "## Second\n\nProse.\n\n### Your turn\n\nProse.\n",
        )
        b.build()
        toc = self.toc(repo)
        assert "Your turn" not in toc
        assert 'href="#first"' in toc
        assert 'href="#second"' in toc

    def test_a_sub_heading_that_appears_once_is_kept(self, repo):
        write(
            repo,
            "## First\n\nProse.\n\n### Your turn\n\nProse.\n\n"
            "## Second\n\nProse.\n\n### Something distinct\n\nProse.\n",
        )
        b.build()
        assert "Something distinct" in self.toc(repo)

    def test_the_contents_page_has_no_contents_rung_of_its_own(self, repo):
        write(repo, self.sections(3))
        b.build()
        assert "dl-crumb-level-4" not in (repo / "site" / "index.html").read_text()

    def test_a_downloadable_copy_keeps_it_and_nothing_else_of_the_tree(self, repo_with_assets):
        """Its links are inside the file, so they work from a student's
        disk — unlike the rest of the tree, which links to other files."""
        write(repo_with_assets, self.sections(3))
        b.build(standalone=True)
        page = (repo_with_assets / "site" / "download" / "sample.html").read_text()
        markup = outside_style_and_script(page)
        assert 'href="#section-1"' in markup
        assert "dl-crumb-level-4" in markup
        assert "dl-crumb-level-3" not in markup


class TestTheStickyChrome:
    def test_nothing_sits_above_the_page(self, repo):
        """What the top bar held — all tutorials, previous and next, search,
        contents — is all in the top-left dock's tree or its search bar
        now, so the bar itself is gone and the page starts at its own
        heading. Previous and next survive at the foot of the page."""
        write(repo, "Some prose.\n")
        b.build()
        page = built(repo)
        assert 'id="dl-chrome"' not in page
        assert "dl-nav-top" not in page
        assert "dl-masthead" not in page
        assert '<nav class="dl-nav dl-nav-bottom">' in page

    def test_the_identity_lives_in_the_top_left_corner_dock(self, repo):
        write(repo, "Some prose.\n")
        b.build()
        page = built(repo)
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

    def test_the_right_dock_is_one_stack_of_five_tabs_with_icons(self, repo):
        write(repo, "Some prose.\n")
        b.build()
        page = built(repo)
        start = page.index('<div class="dl-corner-dock dl-corner-dock-tr"')
        end = page.index("<!-- Phone-only", start)
        dock = page[start:end]
        ids = re.findall(r'id="(dl-[a-z]+-toggle)"', dock)
        assert ids == ["dl-yourwork-toggle", "dl-report-toggle", "dl-python-toggle", "dl-appearance-toggle", "dl-importsexports-toggle"]
        assert dock.count('class="dl-tab-icon"') == 5
        assert "dl-corner-dock-bl" not in page
        assert "dl-corner-dock-br" not in page

    def test_the_search_line_under_the_wordmark_is_the_input_itself(self, repo):
        """nav_search_html() — a magnifier and "Search for a topic" between
        the wordmark and the tree, and the line is the search widget's own
        input with those words as its placeholder: nothing to open first,
        no second bar (7.169). It has to be the input itself: a summary
        styled to look like a field read as a search bar that did nothing
        when typed into (7.166)."""
        write(repo, "Some prose.\n")
        b.build()
        page = built(repo)
        start = page.index('<div class="dl-corner-dock dl-corner-dock-tl"')
        end = page.index('<div class="dl-corner-dock dl-corner-dock-tr"', start)
        corner = page[start:end]
        line = corner.index('<div class="dl-nav-search">')
        assert corner.index("dl-wordmark") < line < corner.index('<nav class="dl-crumbtrail"')
        field = re.search(r'<input type="search" id="dl-nav-search-input" class="dl-search-input"[^>]*>', corner)
        assert field and 'placeholder="Search for a topic"' in field.group(0)
        assert "<details" not in corner[line:corner.index('<nav class="dl-crumbtrail"')]
        assert "<summary" not in corner[line:corner.index('<nav class="dl-crumbtrail"')]

    def test_a_downloadable_copy_keeps_the_docks_without_the_navigation(
        self, repo_with_assets
    ):
        write(repo_with_assets, "Some prose.\n")
        b.build(standalone=True)
        page = (repo_with_assets / "site" / "download" / "sample.html").read_text()
        assert "dl-corner-dock" in page
        assert "dl-nav" not in page.split("<style>")[0] + page.split("</style>")[-1]


class TestWhatTheRuntimeReads:
    """Two JSON files the page scripts fetch: the search index, and the
    routes file the runtime draws a course's chrome from."""

    def test_search_entries_carry_the_course(self, repo):
        write(repo, "Prose.\n")
        course(repo, "zz-other", {"Also": ["sample"]}, title="Other Course")
        b.build()
        [entry] = json.loads((repo / "site" / "assets" / "search-index.json").read_text())
        assert entry["id"] == "sample"
        assert entry["url"] == "tutorials/sample.html"
        assert entry["module"] == "computational-methods"
        assert entry["moduleTitle"] == "Computational Methods"
        assert entry["series"] == "Python fundamentals"
        assert entry["courses"] == ["computational-methods", "zz-other"]

    def test_routes_json_lists_every_course_with_its_pages(self, repo):
        write(repo, "Prose.\n")
        practice(repo, "sample")
        course(repo, "zz-other", {"Also": ["sample"]}, title="Other Course")
        b.build()
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
    """Cache-busting: without a version in the URL a browser keeps an old
    stylesheet forever, and the bug looks like page breakage rather than
    caching. Tested against the real assets, since a version of a file that
    is not there proves nothing."""

    def urls(self, repo) -> str:
        return built(repo) + (repo / "site" / "index.html").read_text()

    def test_the_stylesheet_and_the_runtime_both_carry_a_version(self, repo_with_assets):
        write(repo_with_assets, "Some prose.\n")
        b.build()
        page = self.urls(repo_with_assets)
        assert re.search(r"tutorial-style\.css\?v=[0-9a-f]{8}", page)
        assert re.search(r"tutorial-runtime\.js\?v=[0-9a-f]{8}", page)

    def test_the_maths_stylesheet_does_too(self, repo_with_assets):
        write(repo_with_assets, "Some prose.\n")
        b.build()
        assert re.search(r"katex\.min\.css\?v=[0-9a-f]{8}", self.urls(repo_with_assets))

    def test_what_the_runtime_fetches_for_itself_is_versioned(self, repo_with_assets):
        """It is not in the markup, so the page cannot bust it — the manifest can."""
        write(repo_with_assets, "```python exec\nid: c\n1 + 1\n```\n")
        b.build()
        versions = manifest(built(repo_with_assets))["assetVersions"]
        assert re.fullmatch(r"[0-9a-f]{8}", versions["tutorial_tools.py"])

    def test_editing_an_asset_changes_its_version(self, repo_with_assets):
        write(repo_with_assets, "Some prose.\n")
        b.build()
        before = re.search(r"tutorial-style\.css\?v=([0-9a-f]{8})", built(repo_with_assets))

        style = repo_with_assets / "assets" / "tutorial-style.css"
        style.write_text(style.read_text() + "\n.something-new { color: red; }\n")
        b._ASSET_VERSIONS.clear()
        b.build()
        after = re.search(r"tutorial-style\.css\?v=([0-9a-f]{8})", built(repo_with_assets))
        assert before.group(1) != after.group(1)

    def test_the_same_assets_give_the_same_version(self, repo_with_assets):
        """Otherwise every publish invalidates every cache for no reason."""
        write(repo_with_assets, "Some prose.\n")
        b.build()
        first = re.search(r"tutorial-style\.css\?v=([0-9a-f]{8})", built(repo_with_assets))
        b._ASSET_VERSIONS.clear()
        b.build()
        again = re.search(r"tutorial-style\.css\?v=([0-9a-f]{8})", built(repo_with_assets))
        assert first.group(1) == again.group(1)

    def test_two_repositories_in_one_process_do_not_share_a_version(self, repo_with_assets):
        """The cache is keyed by path. Keyed by name, the second build here
        would be handed the first one's hash."""
        write(repo_with_assets, "Some prose.\n")
        b.build()
        mine = b.asset_version("tutorial-style.css")
        assert mine != "missing"
        assert len(b._ASSET_VERSIONS) >= 1
        assert all(k.startswith("/") for k in b._ASSET_VERSIONS)


class TestTheExportFailsLoudly:
    def test_a_replacement_that_finds_nothing_stops_the_build(self):
        """A silent no-op here is a downloadable copy with no stylesheet."""
        with pytest.raises(b.BuildError, match="drifted apart"):
            b.replace_once("<p>a page</p>", "<not-here>", "x", "the thing")


def test_the_marking_workbench_is_published(repo, monkeypatch):
    # Nothing on the site links to /dewmark/, so a broken copy step would go
    # unnoticed until somebody typed the address.
    workbench = repo / "dewmark" / "workbench"
    workbench.mkdir(parents=True)
    (workbench / "index.html").write_text("<h1>dewmark marking workbench</h1>")
    monkeypatch.setattr(b, "DEWMARK_WORKBENCH", workbench)

    b.build()

    published = b.OUT / "dewmark" / "index.html"
    assert published.is_file()
    assert published.read_text() == (workbench / "index.html").read_text()


def test_the_topic_pair_game_is_published_without_its_readme(repo, monkeypatch):
    # Its README is written for somebody reading the repository, not a visitor.
    game = repo / "topic_tree_game"
    game.mkdir(parents=True)
    (game / "index.html").write_text("<h1>topic pairs</h1>")
    (game / "help.html").write_text("<h1>how to play</h1>")
    (game / "README.md").write_text("how the loop works")
    monkeypatch.setattr(b, "TOPIC_GAME", game)

    b.build()

    assert (b.OUT / "topic_tree_game" / "index.html").is_file()
    assert (b.OUT / "topic_tree_game" / "help.html").is_file()
    assert not (b.OUT / "topic_tree_game" / "README.md").exists()


def test_no_topic_game_folder_is_not_an_error(repo, monkeypatch):
    monkeypatch.setattr(b, "TOPIC_GAME", repo / "topic_tree_game")

    b.build()

    assert not (b.OUT / "topic_tree_game").exists()


def test_the_topic_editor_is_published_beside_the_game(repo, monkeypatch):
    # Same terms as the pair game: one page, nothing linking to it.
    editor = repo / "topic_editor"
    editor.mkdir(parents=True)
    (editor / "index.html").write_text("<h1>topic editor</h1>")
    (editor / "help.html").write_text("<h1>how it works</h1>")
    (editor / "README.md").write_text("for a reader of the repository")
    monkeypatch.setattr(b, "TOPIC_EDITOR", editor)

    b.build()

    assert (b.OUT / "topic_editor" / "index.html").read_text() == "<h1>topic editor</h1>"
    assert (b.OUT / "topic_editor" / "help.html").is_file()
    assert not (b.OUT / "topic_editor" / "README.md").exists()


def test_no_topic_editor_folder_is_not_an_error(repo, monkeypatch):
    monkeypatch.setattr(b, "TOPIC_EDITOR", repo / "topic_editor")

    b.build()

    assert not (b.OUT / "topic_editor").exists()


def test_no_workbench_folder_is_not_an_error(repo, monkeypatch):
    monkeypatch.setattr(b, "DEWMARK_WORKBENCH", repo / "dewmark" / "workbench")
    b.build()
    assert not (b.OUT / "dewmark").exists()


class TestFeedbackFooter:
    """The footer's "three doors" report disclosure.
    On by default; planning/feedback.yaml is the kill switch."""

    def test_doors_on_a_tutorial_page_by_default(self, repo, monkeypatch):
        write(repo, "# Sample\n\nSome text.")
        b.build()

        page = built(repo)
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

    def test_doors_gone_when_switched_off(self, repo, monkeypatch):
        (repo / "planning").mkdir(parents=True, exist_ok=True)
        (repo / "planning" / "feedback.yaml").write_text("enabled: false\n")
        write(repo, "# Sample\n\nSome text.")
        b.build()

        page = built(repo)
        assert "Something wrong on this page?" not in page
        assert "dl-report-doors" not in page
        assert "issues/new" not in page
        assert "discussions/new" not in page

    def test_doors_also_appear_on_the_contents_page(self, repo, monkeypatch):
        write(repo, "# Sample\n\nSome text.")
        b.build()

        index = (repo / "site" / "index.html").read_text()
        assert "Something wrong on this page? Tell us." in index
        assert "discussions/new" in index

    def test_report_issue_url_carries_page_and_version(self):
        url = b.report_issue_url("computational-methods/first-steps", "2026.09.01.2")
        assert url.startswith("https://github.com/deweydex/dewlab/issues/new?")
        assert "page=computational-methods%2Ffirst-steps" in url
        assert "version=2026.09.01.2" in url
        assert "template=report.yml" in url
        assert "kind=" not in url

    def test_report_issue_url_carries_kind_when_given(self):
        url = b.report_issue_url("a/b", "1", kind="The page is wrong, or I could not follow it")
        assert "kind=The+page+is+wrong" in url

    def test_report_doors_html_kinds_match_the_issue_template(self):
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

    def test_feedback_enabled_defaults_true_without_a_config_file(self, repo):
        assert b.feedback_enabled() is True

    def test_feedback_enabled_reads_the_config_file(self, repo):
        (repo / "planning").mkdir(parents=True, exist_ok=True)
        (repo / "planning" / "feedback.yaml").write_text("enabled: false\n")
        assert b.feedback_enabled() is False
