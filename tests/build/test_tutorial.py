"""A tutorial's own file: frontmatter, cells, maths, folds, notes, assets, datasets, hints."""

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

class TestTheHappyPath:
    """One plain tutorial, with a stylesheet in assets/: it builds to one
    page at site/tutorials/<id>.html with every shell token filled and its
    asset bases one level up; its frontmatter reaches the page's metadata;
    its prose becomes HTML; the assets folder is copied but the shell
    template is not; and its manifest carries nothing it did not declare —
    no cells, no packages, no datasets, no notes, no maths."""

    def test_a_plain_tutorial_builds_to_one_page_under_site_tutorials_carrying_nothing_it_did_not_declare(self, repo):
        (repo / "assets" / "tutorial-style.css").write_text("/* style */")
        write(repo, "# Heading\n\nA paragraph.\n", version="2026.08.24.1")
        written = b.build()
        page = built(repo)
        assert repo / "site" / "tutorials" / "sample.html" in written
        # Every shell token is filled.
        assert "{{" not in built(repo)
        # The page sits in site/tutorials/, so the shared folders are one level up.
        assert manifest(built(repo))["assetBase"] == "../assets/"
        assert manifest(built(repo))["dataBase"] == "../data/"
        # Frontmatter reaches the page metadata.
        assert '<meta name="tutorial-version" content="2026.08.24.1">' in page
        assert '<meta name="tutorial-slug" content="sample">' in page
        # Prose becomes HTML.
        assert "<h1" in built(repo)
        assert "<p>A paragraph.</p>" in built(repo)
        # Assets are copied but the template is not.
        assert (repo / "site" / "assets" / "tutorial-style.css").is_file()
        assert not (repo / "site" / "assets" / "shell.html").exists()
        # A tutorial with no cells carries an empty manifest.
        assert manifest(built(repo))["cells"] == []
        # No packages field leaves the runtime default alone.
        assert "packages" not in manifest(built(repo))
        # A tutorial with no datasets has no datasets key.
        assert "datasets" not in manifest(built(repo))
        # A tutorial with no notes has no notes key.
        assert "notes" not in manifest(built(repo))
        # A page without maths carries no flag.
        assert "math" not in manifest(built(repo))


class TestCells:
    """A python exec fence. One plain cell (its markup, its manifest entry,
    and the keys a python-only page does not carry); one page of cells
    with hints, names, a name-shaped first line and a script-closing
    string; two cells in order; and the header lines a cell must have."""

    def test_one_python_exec_fence_becomes_a_cell_whose_code_travels_in_the_manifest(self, repo):
        write(repo, CELL)
        b.build()
        page = built(repo)
        assert 'class="dl-cell" data-cell-id="only-cell"' in page
        assert 'class="dl-editor"' in page and 'class="dl-output"' in page
        # The code travels in the manifest, not the markup.
        cells = manifest(page)["cells"]
        assert cells == [{"id": "only-cell", "hint": None, "code": 'print("hello")'}]
        # The footbar sits between the editor and the output.
        assert page.index('<div class="dl-editor">') < page.index('class="dl-cell-footbar"')
        assert page.index('class="dl-cell-footbar"') < page.index('<div class="dl-output">')
        # A plain python cell carries no type key (a sql cell does).
        assert "type" not in manifest(built(repo))["cells"][0]
        # A tutorial with no sql cells does not need sqlite.
        assert "needsSqlite" not in manifest(built(repo))
        # A tutorial with no site editors carries no siteEditors key.
        assert "siteEditors" not in manifest(built(repo))

    def test_hints_and_names_reach_the_page_and_the_manifest_escaped_and_unswallowed(self, repo):
        write(repo, '```python exec\nid: h\nhint: Mind the <angles> & things\n1\n```\n\n'
                    '```python exec\nid: c\nhint: Try this.\n1\n```\n\n'
                    '```python exec\nid: n\nname: filter-evening\n1\n```\n\n'
                    '```python exec\nid: m\nname: str = "Ada"\nprint(name)\n```\n\n'
                    '```python exec\nid: x\nprint("</script><script>alert(1)")\n```\n')
        b.build()
        page = built(repo)
        cells = {cell["id"]: cell for cell in manifest(page)["cells"]}
        # A hint is carried and escaped.
        assert "Mind the &lt;angles&gt; &amp; things" in page
        assert cells["h"]["hint"] == "Mind the <angles> & things"
        # A hint starts closed and is a real toggle, not a hover popover.
        assert '<div class="dl-hint-text" id="dl-hint-c" hidden>Try this.</div>' in page
        assert 'aria-controls="dl-hint-c"' in page
        assert 'aria-expanded="false"' in page
        assert 'role="tooltip"' not in page
        # A name is carried to the pill and the manifest.
        assert '<span class="dl-cell-name">filter-evening</span>' in page
        assert cells["n"]["name"] == "filter-evening"
        # A name-shaped first line of code is not swallowed as a header.
        cell = cells["m"]
        assert cell.get("name") is None
        assert cell["code"] == 'name: str = "Ada"\nprint(name)'
        # Angle brackets in code cannot close the script element.
        assert "</script><script>alert(1)" not in page
        assert cells["x"]["code"] == 'print("</script><script>alert(1)")'

    def test_cells_keep_document_order(self, repo):
        write(repo, "```python exec\nid: one\n1\n```\n\ntext\n\n```python exec\nid: two\n2\n```\n")
        b.build()
        assert [c["id"] for c in manifest(built(repo))["cells"]] == ["one", "two"]

    def test_a_cell_without_an_id_fails_the_build(self, repo):
        write(repo, "```python exec\nprint(1)\n```\n")
        with pytest.raises(b.BuildError, match="no `id:` line"):
            b.build()

    def test_two_cells_sharing_an_id_fail_the_build(self, repo):
        write(repo, "```python exec\nid: same\n1\n```\n\n```python exec\nid: same\n2\n```\n")
        with pytest.raises(b.BuildError, match="share the id"):
            b.build()


SQL_CELL = """```sql exec
id: only-sql-cell
SELECT 1;
```
"""


SITE_HTML = """```html site
id: hero-html
site: hero
<button>Hi</button>
```
"""


SITE_CSS = """```css site
id: hero-css
site: hero
button { color: red; }
```
"""


SITE_JS = """```js site
id: hero-js
site: hero
console.log("hi");
```
"""


class TestSqlCells:
    """A sql exec cell shares python exec's header grammar and manifest shape;
    only the fence's language word and the pill it produces differ. One sql
    cell alone; a sql cell with a hint and a python cell on one page; the
    two types in order; a fence in an unknown language. (What a python-only
    page does not carry — no type key, no needsSqlite — is checked in
    TestCells.)"""

    def test_one_sql_exec_fence_becomes_a_typed_cell_that_needs_sqlite(self, repo):
        write(repo, SQL_CELL)
        b.build()
        page = built(repo)
        assert 'class="dl-cell" data-cell-id="only-sql-cell"' in page
        assert 'class="dl-editor"' in page and 'class="dl-output"' in page
        # The pill reads SQL, not Python.
        assert '<span class="dl-cell-pill-type" data-type="sql">SQL</span>' in page
        # The sql travels in the manifest as a typed cell.
        cells = manifest(built(repo))["cells"]
        assert cells == [{"id": "only-sql-cell", "hint": None, "code": "SELECT 1;", "type": "sql"}]
        assert manifest(built(repo))["needsSqlite"] is True

    def test_a_sql_cell_with_a_hint_and_a_python_cell_each_keep_their_own_pill(self, repo):
        write(repo, '```sql exec\nid: c\nhint: Try SELECT *.\nSELECT 1;\n```\n\n' + CELL)
        b.build()
        page = built(repo)
        # A python cell on the same page still reads Python.
        assert '<span class="dl-cell-pill-type" data-type="sql">SQL</span>' in page
        assert '<span class="dl-cell-pill-type" data-type="python">Python</span>' in page
        # A sql cell gets hint and expect like any other.
        assert manifest(page)["cells"][0]["hint"] == "Try SELECT *."
        assert 'aria-controls="dl-hint-c"' in page

    def test_an_unknown_fence_language_fails_the_build(self, repo):
        write(repo, "```rust exec\nid: c\nfn main() {}\n```\n")
        with pytest.raises(b.BuildError, match="not one of"):
            b.build()

    def test_cells_of_different_types_keep_document_order(self, repo):
        write(repo, "```sql exec\nid: one\nSELECT 1;\n```\n\ntext\n\n```python exec\nid: two\n2\n```\n")
        b.build()
        assert [c["id"] for c in manifest(built(repo))["cells"]] == ["one", "two"]


class TestSiteEditors:
    """Site identity lives in an id:/site: header, not a `site=name` info
    string, because the Crepe-based authoring editor's round trip keeps
    only a fence's first word. Scenarios: an html pane alone; html and css;
    html, css and js; two sites on one page with a cell between them; and
    the headers and orderings that fail the build. (A page with no site
    editors at all is checked in TestCells.)"""

    def test_a_solo_html_pane_becomes_an_editor_whose_starter_code_travels_in_the_manifest(self, repo):
        write(repo, SITE_HTML)
        b.build()
        page = built(repo)
        assert 'class="dl-site-editor" data-site-name="hero"' in page
        assert 'data-lang="html"' in page
        assert 'class="dl-editor"' in page
        # The starter code travels in the manifest, not the DOM.
        assert "<button>Hi</button>" not in page
        editors = manifest(page)["siteEditors"]
        assert editors == [{"name": "hero", "panes": {"html": {"id": "hero-html", "code": "<button>Hi</button>"}}}]

    def test_three_consecutive_panes_share_one_editor_with_a_run_button_and_a_console(self, repo):
        write(repo, SITE_HTML + SITE_CSS + SITE_JS)
        b.build()
        page = built(repo)
        assert page.count('data-site-name="hero"') == 1
        assert page.count('class="dl-site-pane"') == 3
        # A js pane gets a run button and a console.
        assert "dl-btn-site-run" in page
        assert "dl-site-console-output" in page

    def test_an_html_and_css_only_editor_has_no_js_pane_run_button_or_console(self, repo):
        write(repo, SITE_HTML + SITE_CSS)
        b.build()
        page = built(repo)
        # Panes are optional: html and css only.
        assert 'data-lang="html"' in page and 'data-lang="css"' in page
        assert 'data-lang="js"' not in page
        assert "dl-btn-site-run" not in page
        assert "dl-site-console-output" not in page

    def test_an_unknown_pane_language_fails_the_build(self, repo):
        write(repo, "```php site\nid: c\nsite: hero\n<?php ?>\n```\n")
        with pytest.raises(b.BuildError, match="not one of"):
            b.build()

    def test_a_pane_with_no_id_fails_the_build(self, repo):
        write(repo, "```html site\nsite: hero\n<p>hi</p>\n```\n")
        with pytest.raises(b.BuildError, match="no `id:` line"):
            b.build()

    def test_a_pane_with_no_site_name_fails_the_build(self, repo):
        write(repo, "```html site\nid: c\n<p>hi</p>\n```\n")
        with pytest.raises(b.BuildError, match="no `site:` line"):
            b.build()

    def test_two_panes_of_the_same_language_in_one_editor_fails_the_build(self, repo):
        write(repo, SITE_HTML + "```html site\nid: hero-html-2\nsite: hero\n<p>again</p>\n```\n")
        with pytest.raises(b.BuildError, match="two html panes"):
            b.build()

    def test_non_consecutive_panes_of_the_same_site_fail_the_build(self, repo):
        write(repo, SITE_HTML + "\ntext in between\n\n" + SITE_CSS)
        with pytest.raises(b.BuildError, match="not consecutive"):
            b.build()

    def test_a_site_pane_id_cannot_collide_with_a_cell_id(self, repo):
        write(repo, "```html site\nid: dup\nsite: hero\n<p>hi</p>\n```\n\n"
                    "```python exec\nid: dup\nprint(1)\n```\n")
        with pytest.raises(b.BuildError, match="share the id"):
            b.build()

    def test_two_different_sites_with_a_cell_between_them_both_render_unconfused(self, repo):
        write(repo, SITE_HTML + SITE_CSS + CELL + "```html site\nid: aside-html\nsite: aside\n<p>hi</p>\n```\n")
        b.build()
        page = built(repo)
        # Two different sites on one page both render.
        assert 'data-site-name="hero"' in page
        assert 'data-site-name="aside"' in page
        # The cell between them does not confuse them.
        assert [e["name"] for e in manifest(page)["siteEditors"]] == ["hero", "aside"]
        assert manifest(page)["cells"][0]["id"] == "only-cell"


class TestIncludes:
    def test_an_include_is_expanded_into_the_cell(self, repo):
        (repo / "setup" / "shared.py").write_text("shared = 1\n")
        write(repo, "```python exec\nid: c\n{{include: setup/shared.py}}\nshared\n```\n")
        b.build()
        assert manifest(built(repo))["cells"][0]["code"] == "shared = 1\nshared"

    def test_a_missing_include_fails_the_build(self, repo):
        write(repo, "```python exec\nid: c\n{{include: setup/absent.py}}\n```\n")
        with pytest.raises(b.BuildError, match="does not exist"):
            b.build()

    def test_an_include_cannot_escape_the_repository(self, repo):
        write(repo, "```python exec\nid: c\n{{include: ../../etc/passwd}}\n```\n")
        with pytest.raises(b.BuildError, match="escapes the repository|does not exist"):
            b.build()


class TestAltText:
    """An image without alt text fails the build. (An explicitly empty alt,
    and the alt markdown image syntax carries, are checked on the assets
    page in TestTutorialAssets.)"""

    def test_an_image_without_alt_fails_the_build(self, repo):
        write(repo, 'A diagram:\n\n<img src="d.png">\n')
        asset(repo, "sample", "d.png")
        with pytest.raises(b.BuildError, match="no alt attribute"):
            b.build()


class TestTutorialAssets:
    """A tutorial is a folder; an asset it uses sits there and is referenced
    by its plain name (planning/ROADMAP.md Phase 1). One page that uses a
    picture, a downloadable file, external and missing links, and shows
    markup as text; a tutorial with a frozen release; and a picture that
    is not there."""

    def test_a_page_of_pictures_and_links_resolves_its_own_files_and_leaves_the_rest_alone(self, repo):
        write(repo, 'A flourish:\n\n<img src="d.png" alt="">\n\n'
                    "![A labelled diagram](d.png)\n\n"
                    '<img src="https://example.org/d.png" alt="A diagram">\n\n'
                    '<a href="demo.html">demo.html</a>\n\n'
                    '<a href="not-a-real-file.html">a link</a>\n\n'
                    '<a href="https://example.org/demo.html">demo</a>\n\n'
                    'Shown as text: `<img src="not-a-real-file.png">` and '
                    '`<a href="not-a-real-file.html">`.\n')
        asset(repo, "sample", "d.png", b"PNG-BYTES")
        asset(repo, "sample", "demo.html", b"<p>a starter</p>")
        glossary(repo, "sample", [{"term": "x", "kind": "concept", "definition": "y"}])
        b.build()
        page = built(repo)
        # An asset is copied beside the tutorial.
        copied = repo / "site" / "tutorials" / "sample" / "d.png"
        assert copied.read_bytes() == b"PNG-BYTES"
        # The current release reaches into its own folder: the page is
        # site/tutorials/<id>.html, one level above the folder its assets
        # are copied to, so a plain name needs the folder added to still
        # resolve.
        # (d.png is the one with the explicitly empty alt, allowed as
        # decorative, so this line also proves that image survived.)
        assert 'src="sample/d.png"' in built(repo)
        # Markdown image syntax carries its alt through.
        assert 'alt="A labelled diagram"' in built(repo)
        # An external image is left alone.
        assert 'src="https://example.org/d.png"' in built(repo)
        # The glossary is not treated as an asset.
        assert not (repo / "site" / "tutorials" / "sample" / "sample.glossary.yaml").exists()
        # A downloadable sibling file is linked with href= rather than shown
        # with src=; it resolves the same one-level-above-itself way a
        # picture does, and is copied.
        assert 'href="sample/demo.html"' in built(repo)
        copied = repo / "site" / "tutorials" / "sample" / "demo.html"
        assert copied.read_bytes() == b"<p>a starter</p>"
        # Unlike src=, an href naming a file that is not there doesn't fail
        # the build: a page links to plenty of non-local things, and this
        # must not mistake an already-resolved tutorial: link for a missing
        # file.
        assert 'href="not-a-real-file.html"' in built(repo)
        # An external href is left alone.
        assert 'href="https://example.org/demo.html"' in built(repo)
        # A src or href shown as text in a code span is not resolved:
        # code-span text escapes angle brackets but leaves the quoted
        # src/href alone, so this must be told apart from a real attribute
        # or a quick-reference table breaks the build over its own example.
        assert 'src="not-a-real-file.png"' in page
        assert 'href="not-a-real-file.html"' in page

    def test_a_frozen_release_is_already_inside_it(self, repo):
        # A frozen release's page sits inside its own folder, so the plain
        # name is already right and must be left alone.
        write(repo, '<img src="d.png" alt="A diagram">\n', version="2026.09.01.1")
        old = tutorial_path(repo, "sample").parent / "v2026.08.23.1.md"
        old.write_text(FRONTMATTER.format(version="2026.08.23.1")
                       + '<img src="d.png" alt="A diagram">\n')
        asset(repo, "sample", "d.png")
        b.build()
        frozen = (repo / "site" / "tutorials" / "sample" / "v2026.08.23.1.html").read_text()
        assert 'src="d.png"' in frozen

    def test_an_image_naming_a_file_that_is_not_there_fails_the_build(self, repo):
        # Same stance as a dead tutorial: link — fail loud rather than ship a
        # page that only looks finished.
        write(repo, '<img src="missing.png" alt="A diagram">\n')
        with pytest.raises(b.BuildError, match="not a file in this tutorial's folder"):
            b.build()


class TestFrontmatter:
    """A frontmatter with a packages list and a title holding markup; and
    the frontmatter faults that fail the build. (A frontmatter with no
    packages field is checked in TestTheHappyPath.)"""

    def test_a_missing_field_fails_the_build(self, repo):
        path = write(repo, "Prose.\n")
        path.write_text(path.read_text().replace("version: 2026.08.23.1\n", ""))
        with pytest.raises(b.BuildError, match="missing version"):
            b.build()

    def test_a_file_without_frontmatter_fails_the_build(self, repo):
        (tutorial_path(repo, "bare")).write_text("Just prose.\n")
        with pytest.raises(b.BuildError, match="no YAML frontmatter"):
            b.build()

    def test_unclosed_frontmatter_fails_the_build(self, repo):
        (tutorial_path(repo, "bad")).write_text("---\ntitle: x\n")
        with pytest.raises(b.BuildError, match="never closed"):
            b.build()

    def test_a_packages_list_widens_the_manifest_and_a_title_with_markup_is_escaped(self, repo):
        path = write(repo, "Prose.\n")
        path.write_text(path.read_text().replace("version: 2026.08.23.1", "version: 2026.08.23.1\npackages: [sympy]"))
        path.write_text(path.read_text().replace('title: "A Title"', 'title: "A <b>Title</b>"'))
        b.build()
        assert manifest(built(repo))["packages"] == ["sympy"]
        assert "<title>A &lt;b&gt;Title&lt;/b&gt; — dewlab</title>" in built(repo)


class TestMaths:
    """One page of maths — inline, display, TeX with backslashes and angle
    brackets — and one page of dollars that are not maths. (A page with no
    maths at all is checked in TestTheHappyPath.)"""

    def test_inline_and_display_maths_are_marked_flagged_and_escaped_with_the_tex_kept(self, repo):
        write(repo, "The term $a_i + b_j$ matters.\n\n"
                    "$$x^2$$\n\n"
                    r"Here: $\frac{1}{3}$." + "\n\n"
                    "Some $x$ here.\n\n"
                    "$a < b$\n")
        b.build()
        page = built(repo)
        # Inline maths is marked and survives markdown.
        assert '<span class="dl-math">a_i + b_j</span>' in page
        assert "<em>" not in page  # the underscores would otherwise become emphasis
        # Display maths gets its own class.
        assert '<span class="dl-math dl-math-display">x^2</span>' in built(repo)
        # The source TeX stays in the page as a fallback.
        assert r"\frac{1}{3}" in built(repo)
        # The manifest flags a page with maths.
        assert manifest(built(repo))["math"] is True
        # TeX is escaped into the markup.
        assert "a &lt; b" in page

    def test_currency_an_escaped_dollar_and_a_dollar_in_a_fence_are_not_maths(self, repo):
        write(repo, "It cost $5 or $6 depending on the day.\n\n"
                    r"A round \$99 exactly." + "\n\n"
                    "```python\ncost = '$5 and $6'\n```\n")
        b.build()
        page = built(repo)
        assert "dl-math" not in page
        # Currency is not mistaken for maths.
        assert "$5 or $6" in page
        # An escaped dollar stays literal.
        assert "$99" in page
        # Maths inside a fence is left alone.
        assert "dl-math" not in built(repo)


class TestIllustrativeCode:
    """One page of untagged fences: one marked for highlighting, one with no
    language, one holding markup, one holding underscores, one that would
    be a cell if tagged, and one holding a dash that is not a list."""

    def test_untagged_fences_are_static_highlighted_escaped_and_never_cells_or_lists(self, repo):
        write(repo, "```python\ntotal = 1\n```\n\n"
                    "```\nplain text\n```\n\n"
                    "```python\nprint('<b>hi</b>')\n```\n\n"
                    "```python\nname_with_underscores = 1\n```\n\n"
                    "```python\nnot_a_cell = 1\n```\n\n"
                    "```python\ntotal = 1\n- not a list\n```\n")
        b.build()
        page = built(repo)
        # An untagged fence is marked for highlighting.
        assert '<pre class="dl-static" data-lang="python"><code>total = 1</code></pre>' in built(repo)
        # A fence with no language still renders.
        assert '<pre class="dl-static"><code>plain text</code></pre>' in page
        # Illustrative code is escaped.
        assert "&lt;b&gt;hi&lt;/b&gt;" in page
        assert "<b>hi</b>" not in page
        # It carries no run button.
        assert "dl-btn-run" not in built(repo)
        # Markdown cannot reinterpret what is inside it.
        assert "name_with_underscores" in page
        assert "<em>" not in page
        # An untagged fence stays ordinary code, not a cell.
        assert "dl-cell" not in page
        assert "<code" in page
        # A dash inside a fence is left alone.
        assert "<li>" not in built(repo)


class TestListsWrittenTightAgainstProse:
    """Markdown written elsewhere often puts a list straight under a
    paragraph. Each list page counts its items, so a page holds one list:
    a bullet list, a numbered list, one with its blank line, one of three
    items; then a page with a list under a heading beside one under a
    paragraph, and a page whose leading hyphen is not a list at all."""

    def test_a_bullet_list_under_a_paragraph_still_becomes_a_list(self, repo):
        write(repo, "When you look at it, consider:\n- Is it symmetric?\n- Is there one peak?\n")
        b.build()
        page = built(repo)
        assert "<ul>" in page
        assert page.count("<li>") == 2

    def test_a_numbered_list_under_a_paragraph_still_becomes_a_list(self, repo):
        write(repo, "Then do this:\n1. Print the first value\n2. Print the last value\n")
        b.build()
        page = built(repo)
        assert "<ol>" in page
        assert page.count("<li>") == 2

    def test_the_paragraph_above_a_list_and_a_heading_above_another_are_left_intact(self, repo):
        write(repo, "The pattern appears everywhere:\n- Looking up a contact\n\n"
                    "## A heading\n- One\n- Two\n")
        b.build()
        page = built(repo)
        # The paragraph above it is left intact.
        assert "<p>The pattern appears everywhere:</p>" in built(repo)
        # A list under a heading is untouched.
        assert "<ul>" in page and "<h2" in page

    def test_a_list_that_already_had_its_blank_line_is_untouched(self, repo):
        write(repo, "Consider:\n\n- One\n- Two\n")
        b.build()
        assert built(repo).count("<li>") == 2

    def test_items_within_a_list_are_not_split_apart(self, repo):
        write(repo, "Consider:\n- One\n- Two\n- Three\n")
        b.build()
        page = built(repo)
        assert page.count("<ul>") == 1
        assert page.count("<li>") == 3

    def test_a_hyphenated_sentence_is_not_mistaken_for_a_list(self, repo):
        write(repo, "A sentence.\n-5 degrees is cold.\n")
        b.build()
        assert "<li>" not in built(repo)


class TestNotesAndDatasets:
    """planning/SIDEBAR_CONTENT.md §3/§4: unlike the glossary, a note is
    never cumulative across a series — it belongs to the tutorial that wrote
    it, and so does a declared dataset. Two tutorials in one series, the
    first declaring a note and a dataset; the same with a note holding
    markdown and a dataset that is a text file; and the faults that fail
    the build. (A tutorial with neither is checked in TestTheHappyPath.)"""

    def test_a_note_and_a_dataset_reach_the_manifest_of_their_own_tutorial_and_not_the_next(self, repo):
        path = write(repo, '<aside class="dl-note" id="why-it-works">\n\n'
                           "Because reasons.\n\n</aside>\n\nMore prose.\n", slug="one")
        add_frontmatter(path, "datasets:\n  - life-expectancy\n")
        dataset(repo, "life-expectancy", source="World Bank", license="CC-BY-4.0",
                description="Life expectancy by country and year.")
        write(repo, "Two.\n", slug="two")
        set_order(repo, "computational-methods", "python-fundamentals", ["one", "two"])
        b.build()
        # A note appears in the manifest.
        assert manifest(built(repo, "one"))["notes"] == [
            {"id": "why-it-works", "html": "<p>Because reasons.</p>"},
        ]
        # And it is removed from the page body.
        page = built(repo, "one")
        assert "dl-note" not in page.split("dewlab-manifest")[0]
        assert "More prose." in page
        # A declared dataset appears in the manifest.
        assert manifest(built(repo, "one"))["datasets"] == [{
            "name": "life-expectancy",
            "source": "World Bank",
            "license": "CC-BY-4.0",
            "description": "Life expectancy by country and year.",
        }]
        # A note is not inherited by a later tutorial.
        assert "notes" not in manifest(built(repo, "two"))
        # Nor is a dataset.
        assert "datasets" not in manifest(built(repo, "two"))

    def test_a_note_holds_markdown_and_a_dataset_can_be_a_text_file(self, repo):
        # An aside is a raw HTML block, which Python-Markdown would
        # otherwise pass through opaque; mark_markdown_wrappers() marks it
        # so md_in_html parses inside (planning/SIDEBAR_CONTENT.md §1).
        path = write(repo, '<aside class="dl-note" id="pic">\n\n'
                           '![a chart](chart.png)\n\n</aside>\n', slug="one")
        add_frontmatter(path, "datasets:\n  - a-book\n")
        dataset(repo, "a-book", with_csv=False, with_txt=True,
                source="Some author", license="Public domain",
                description="A plain-text dataset, loaded with load_text().")
        b.build()
        assert manifest(built(repo, "one"))["notes"] == [
            {"id": "pic", "html": '<p><img alt="a chart" src="chart.png" /></p>'},
        ]
        assert manifest(built(repo, "one"))["datasets"] == [{
            "name": "a-book",
            "source": "Some author",
            "license": "Public domain",
            "description": "A plain-text dataset, loaded with load_text().",
        }]

    def test_maths_works_inside_a_note(self, repo):
        # This checks maths reaches a note, and that the tutorial's own
        # maths flag notices even though a note's own <span> never ends up
        # in body_html at all, only in the manifest — extract_notes() has
        # taken the aside out by the time that flag is computed.
        write(repo, '<aside class="dl-note" id="why-it-works">\n\n'
                    r"Because $E = mc^2$." + "\n\n</aside>\n", slug="one")
        b.build()
        assert manifest(built(repo, "one"))["notes"] == [
            {"id": "why-it-works", "html": '<p>Because <span class="dl-math">E = mc^2</span>.</p>'},
        ]
        assert manifest(built(repo, "one"))["math"] is True

    def test_an_image_in_a_note_still_needs_alt_text(self, repo):
        write(repo, '<aside class="dl-note" id="pic">\n\n'
                    '<img src="chart.png">\n\n</aside>\n', slug="one")
        with pytest.raises(b.BuildError, match="no alt attribute"):
            b.build()

    def test_two_notes_sharing_an_id_fail_the_build(self, repo):
        write(repo,
              '<aside class="dl-note" id="dup">\n\nOne.\n\n</aside>\n\n'
              '<aside class="dl-note" id="dup">\n\nTwo.\n\n</aside>\n', slug="one")
        with pytest.raises(b.BuildError, match="share the id"):
            b.build()

    def test_a_dataset_with_no_csv_file_fails_the_build(self, repo):
        path = write(repo, "Prose.\n", slug="one")
        add_frontmatter(path, "datasets:\n  - missing\n")
        dataset(repo, "missing", with_csv=False)
        with pytest.raises(b.BuildError, match="data/missing.csv"):
            b.build()

    def test_a_dataset_with_no_attribution_file_fails_the_build(self, repo):
        path = write(repo, "Prose.\n", slug="one")
        add_frontmatter(path, "datasets:\n  - missing\n")
        dataset(repo, "missing", with_attribution=False)
        with pytest.raises(b.BuildError, match="data/missing.yaml"):
            b.build()

    def test_an_attribution_file_missing_a_field_fails_the_build(self, repo):
        path = write(repo, "Prose.\n", slug="one")
        add_frontmatter(path, "datasets:\n  - incomplete\n")
        (repo / "data" / "incomplete.csv").write_text("a,b\n1,2\n")
        (repo / "data" / "incomplete.yaml").write_text('source: "Somewhere"\n')
        with pytest.raises(b.BuildError, match="license, description"):
            b.build()


class TestFolds:
    """A `<details>` must name a fold class; an earlier style-guide draft
    showed a bare one, which renders as a plain browser triangle with none
    of this project's styling."""

    def test_an_answer_fold_and_a_hint_fold_are_fine(self, repo):
        write(repo, '<details class="dl-answer"><summary>answer</summary>\n\n'
                    "Forty-two.\n\n</details>\n\n"
                    '<details class="dl-hint"><summary>stuck?</summary>\n\n'
                    "1. Try this.\n\n</details>\n")
        b.build()
        assert "dl-answer" in built(repo)
        assert "dl-hint" in built(repo)

    def test_a_fold_with_no_class_stops_the_build(self, repo):
        write(repo, "<details><summary>Check solution</summary>\n\nHere.\n\n</details>\n")
        with pytest.raises(b.BuildError, match="names no style"):
            b.build()

    def test_a_fold_with_the_wrong_class_stops_the_build(self, repo):
        write(repo, '<details class="solution"><summary>answer</summary>\n\n'
                    "Here.\n\n</details>\n")
        with pytest.raises(b.BuildError, match="names no style"):
            b.build()

    def test_the_stylesheet_defines_both(self):
        """A fold whose class has no rule is as invisible as one with no class."""
        css = (DEWLAB / "assets" / "tutorial-style.css").read_text()
        for name in b.FOLD_CLASSES:
            assert f".{name} " in css or f".{name}{{" in css or f".{name}[" in css

    def test_maths_works_inside_a_hand_written_fold(self, repo):
        # mark_markdown_wrappers() marks a fold for md_in_html, so its
        # body parses as part of the page's one markdown pass —
        # Python-Markdown treats <details>...</details> as opaque raw HTML,
        # so without this the working in a practice-page answer would
        # reach the page as literal, unrendered text.
        write(repo, '<details class="dl-answer"><summary>answer</summary>\n\n'
                    r"$C(n, r) = \binom{n}{r}$" + "\n\n</details>\n")
        b.build()
        page = built(repo)
        assert '<span class="dl-math">C(n, r) = \\binom{n}{r}</span>' in page
        # The tutorial's own maths flag notices it, even though this
        # never went through the top-level extract_math() call the flag
        # used to be computed from.
        assert manifest(page)["math"] is True


class TestTwoReleasesOnOneDay:
    """Found by releasing four tutorials on the afternoon they were first
    written: a reader choosing between them saw two identical dates."""

    def release(self, repo, slug: str, version: str, status: str = "live") -> Path:
        folder = repo / "tutorials" / slug
        folder.mkdir(parents=True, exist_ok=True)
        name = f"{slug}.md" if status == "live" and version.endswith(".9") else f"v{version}.md"
        path = folder / name
        path.write_text(
            FRONTMATTER.format(version=version).replace(
                f"version: {version}\n", f"version: {version}\nstatus: {status}\n")
            + "Prose.\n"
        )
        set_order(repo, "computational-methods", "python-fundamentals", [slug])
        return path

    def versions(self, repo, slug: str) -> list[dict]:
        page = (repo / "site" / "tutorials" / f"{slug}.html").read_text()
        return manifest(page).get("versions", [])

    def test_two_releases_on_one_day_are_told_apart(self, repo):
        self.release(repo, "sample", "2026.08.23.1")
        self.release(repo, "sample", "2026.08.23.2")
        b.build()
        shown = [v["date"] for v in self.versions(repo, "sample")]
        assert len(shown) == 2
        assert len(set(shown)) == 2, f"both options read the same: {shown}"
        assert shown == ["23 August 2026 (2)", "23 August 2026 (1)"]

    def test_releases_on_different_days_keep_a_plain_date(self, repo):
        """The number is noise where the date already separates them."""
        self.release(repo, "sample", "2026.08.23.1")
        self.release(repo, "sample", "2026.09.15.1")
        b.build()
        shown = [v["date"] for v in self.versions(repo, "sample")]
        assert shown == ["15 September 2026", "23 August 2026"]

    def test_only_the_crowded_day_is_numbered(self, repo):
        self.release(repo, "sample", "2026.08.23.1")
        self.release(repo, "sample", "2026.08.23.2")
        self.release(repo, "sample", "2026.09.15.1")
        b.build()
        shown = [v["date"] for v in self.versions(repo, "sample")]
        assert shown == ["15 September 2026", "23 August 2026 (2)", "23 August 2026 (1)"]


class TestCellReportPanel:
    """code/output are filled in by tutorial-runtime.js at open time, not
    build time — see updateCellReportLinks() there."""

    def test_report_icon_and_panel_on_a_cell_by_default(self, repo, monkeypatch):
        write(repo, "```python exec\nid: greet\nprint('hi')\n```\n", slug="sample")
        b.build()

        page = built(repo)
        assert '<button type="button" class="dl-report-icon"' in page
        assert 'aria-controls="dl-report-greet"' in page
        assert 'id="dl-report-greet" hidden' in page
        assert 'class="dl-report-doors dl-cell-report-doors"' in page
        assert "cell=greet" in page
        assert "I have a question" in page
        assert "It gives an error" in page

    def test_report_icon_gone_when_switched_off(self, repo, monkeypatch):
        (repo / "planning").mkdir(parents=True, exist_ok=True)
        (repo / "planning" / "feedback.yaml").write_text("enabled: false\n")
        write(repo, "```python exec\nid: greet\nprint('hi')\n```\n", slug="sample")
        b.build()

        page = built(repo)
        assert "dl-report-icon" not in page
        assert "dl-cell-report-doors" not in page

    def test_report_issue_url_carries_cell_when_given(self):
        url = b.report_issue_url("a/b", "1", cell="greet")
        assert "cell=greet" in url

    def test_report_doors_links_marks_only_the_issue_links(self):
        html = b.report_doors_links("a/b", "1", cell="greet")
        assert html.count('class="dl-report-issue-link"') == 2
        # The Discussions link is deliberately not one of them — nothing
        # in tutorial-runtime.js should try to inject code/output into it.
        discuss_start = html.index("discussions/new")
        issue_start = html.index("dl-report-issue-link")
        assert discuss_start < issue_start


class TestStagedHints:
    """planning/CELL_HINTS.md. The fold is written back into the markdown
    rather than the finished HTML, so its body converts like any other prose.
    One page of staged hints on one stub cell — the default trigger, a
    titled markdown body, every trigger grammar, a second hint, and one
    naming a cell further down — then a cell with expect:, and the hints
    that fail the build."""

    CELL = "```python exec\nid: stub\n# Your add(a, b)\n```\n\n"

    def test_a_page_of_staged_hints_on_one_cell_reads_every_trigger_grammar(self, repo):
        write(repo, self.CELL
              + "```hint\nWhat did the last line say?\n```\n\n"
              + "```hint\ntitle: some steps\n1. Look at `a[0]`.\n2. Then $x_i$.\n```\n\n"
              + "```hint\nafter: 3 identical errors and 2 minutes\nA.\n```\n\n"
              + "```hint\nafter: same-errors:3, minutes:2\nB.\n```\n\n"
              + "```hint\nafter: 2 unchanged runs, 8 runs & 1 failed check\nC.\n```\n\n"
              + "```hint\nafter: 2 empty results\nA.\n```\n\n"
              + "```hint\nafter: empty-result:3\nB.\n```\n\n"
              + "```hint\nA.\n```\n\n```hint\nafter: 12 errors\nB.\n```\n\n"
              + "```hint\nfor: later\nEarly hint.\n```\n\n"
              + "```python exec\nid: later\n1\n```\n")
        b.build()
        page = built(repo)
        # Defaults to the cell above and five errors.
        assert 'class="dl-hint dl-hint-staged"' in page
        assert 'data-cell="stub"' in page
        assert 'data-after="errors:5"' in page
        assert " hidden>" in page
        assert "<summary>Let’s slow down a moment…</summary>" in page
        # The body is markdown and maths.
        assert "<summary>some steps</summary>" in page
        assert "<ol>" in page and "<code>a[0]</code>" in page
        assert "dl-math" in page
        # Both trigger grammars canonicalise the same way.
        assert page.count('data-after="same-errors:3 minutes:2"') == 2
        assert 'data-after="unchanged:2 runs:8 check-fails:1"' in page
        # Empty results reads both grammars.
        assert 'data-after="empty-results:2"' in page
        assert 'data-after="empty-results:3"' in page
        # A second hint on the same cell gets its own id.
        assert 'id="dl-staged-stub-0"' in page and 'id="dl-staged-stub-1"' in page
        # for: names a cell anywhere on the page.
        assert 'data-cell="later"' in built(repo)

    def test_a_hint_with_no_cell_above_and_no_for_fails(self, repo):
        write(repo, "```hint\nLost.\n```\n")
        with pytest.raises(b.BuildError, match="no exec cell above it"):
            b.build()

    def test_a_hint_naming_a_missing_cell_fails(self, repo):
        write(repo, self.CELL + "```hint\nfor: nope\nX.\n```\n")
        with pytest.raises(b.BuildError, match="does not have: 'nope'"):
            b.build()

    def test_an_unreadable_trigger_fails(self, repo):
        write(repo, self.CELL + "```hint\nafter: soon\nX.\n```\n")
        with pytest.raises(b.BuildError, match="cannot read"):
            b.build()

    def test_an_unknown_signal_fails(self, repo):
        write(repo, self.CELL + "```hint\nafter: 5 bananas\nX.\n```\n")
        with pytest.raises(b.BuildError, match="does not track"):
            b.build()

    def test_an_empty_hint_fails(self, repo):
        write(repo, self.CELL + "```hint\nafter: 5 errors\n```\n")
        with pytest.raises(b.BuildError, match="no text"):
            b.build()

    def test_expect_travels_in_the_manifest_only_when_set(self, repo):
        write(repo, "```python exec\nid: a\nexpect: total == 6\ntotal = 0\n```\n\n"
                    "```python exec\nid: b\n1\n```\n")
        b.build()
        cells = manifest(built(repo))["cells"]
        assert cells[0]["expect"] == "total == 6"
        assert "expect" not in cells[1]
