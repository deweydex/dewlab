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
    def test_a_tutorial_builds_to_its_module_folder(self, repo):
        write(repo, "Some prose.\n")
        written = b.build()
        assert repo / "site" / "tutorials" / "sample.html" in written

    def test_every_shell_token_is_filled(self, repo):
        write(repo, "Some prose.\n")
        b.build()
        assert "{{" not in built(repo)

    def test_frontmatter_reaches_the_page_metadata(self, repo):
        write(repo, "Some prose.\n", version="2026.08.24.1")
        b.build()
        page = built(repo)
        assert '<meta name="tutorial-version" content="2026.08.24.1">' in page
        assert '<meta name="tutorial-slug" content="sample">' in page

    def test_prose_becomes_html(self, repo):
        write(repo, "# Heading\n\nA paragraph.\n")
        b.build()
        assert "<h1" in built(repo)
        assert "<p>A paragraph.</p>" in built(repo)

    def test_asset_paths_climb_out_of_the_module_folder(self, repo):
        write(repo, "Some prose.\n")
        b.build()
        assert manifest(built(repo))["assetBase"] == "../assets/"
        assert manifest(built(repo))["dataBase"] == "../data/"

    def test_assets_are_copied_but_the_template_is_not(self, repo):
        (repo / "assets" / "tutorial-style.css").write_text("/* style */")
        write(repo, "Some prose.\n")
        b.build()
        assert (repo / "site" / "assets" / "tutorial-style.css").is_file()
        assert not (repo / "site" / "assets" / "shell.html").exists()


class TestCells:
    def test_an_exec_fence_becomes_a_cell(self, repo):
        write(repo, CELL)
        b.build()
        page = built(repo)
        assert 'class="dl-cell" data-cell-id="only-cell"' in page
        assert 'class="dl-editor"' in page and 'class="dl-output"' in page

    def test_the_code_travels_in_the_manifest_not_the_markup(self, repo):
        write(repo, CELL)
        b.build()
        page = built(repo)
        cells = manifest(page)["cells"]
        assert cells == [{"id": "only-cell", "hint": None, "code": 'print("hello")'}]

    def test_a_hint_is_carried_and_escaped(self, repo):
        write(repo, '```python exec\nid: c\nhint: Mind the <angles> & things\n1\n```\n')
        b.build()
        page = built(repo)
        assert "Mind the &lt;angles&gt; &amp; things" in page
        assert manifest(page)["cells"][0]["hint"] == "Mind the <angles> & things"

    def test_a_hint_starts_closed_and_is_a_real_toggle_not_a_hover_popover(self, repo):
        write(repo, '```python exec\nid: c\nhint: Try this.\n1\n```\n')
        b.build()
        page = built(repo)
        assert '<div class="dl-hint-text" id="dl-hint-c" hidden>Try this.</div>' in page
        assert 'aria-controls="dl-hint-c"' in page
        assert 'aria-expanded="false"' in page
        assert 'role="tooltip"' not in page

    def test_a_name_is_carried_to_the_pill_and_the_manifest(self, repo):
        write(repo, '```python exec\nid: c\nname: filter-evening\n1\n```\n')
        b.build()
        page = built(repo)
        assert '<span class="dl-cell-name">filter-evening</span>' in page
        assert manifest(page)["cells"][0]["name"] == "filter-evening"

    def test_a_name_shaped_first_line_of_code_is_not_swallowed_as_a_header(self, repo):
        write(repo, '```python exec\nid: c\nname: str = "Ada"\nprint(name)\n```\n')
        b.build()
        page = built(repo)
        cell = manifest(page)["cells"][0]
        assert cell.get("name") is None
        assert cell["code"] == 'name: str = "Ada"\nprint(name)'

    def test_the_footbar_sits_between_the_editor_and_output(self, repo):
        write(repo, CELL)
        b.build()
        page = built(repo)
        assert page.index('<div class="dl-editor">') < page.index('class="dl-cell-footbar"')
        assert page.index('class="dl-cell-footbar"') < page.index('<div class="dl-output">')

    def test_an_untagged_fence_stays_ordinary_code(self, repo):
        write(repo, "```python\nnot_a_cell = 1\n```\n")
        b.build()
        page = built(repo)
        assert "dl-cell" not in page
        assert "<code" in page

    def test_cells_keep_document_order(self, repo):
        write(repo, "```python exec\nid: one\n1\n```\n\ntext\n\n```python exec\nid: two\n2\n```\n")
        b.build()
        assert [c["id"] for c in manifest(built(repo))["cells"]] == ["one", "two"]

    def test_angle_brackets_in_code_cannot_close_the_script_element(self, repo):
        write(repo, '```python exec\nid: c\nprint("</script><script>alert(1)")\n```\n')
        b.build()
        page = built(repo)
        assert "</script><script>alert(1)" not in page
        assert manifest(page)["cells"][0]["code"] == 'print("</script><script>alert(1)")'

    def test_a_cell_without_an_id_fails_the_build(self, repo):
        write(repo, "```python exec\nprint(1)\n```\n")
        with pytest.raises(b.BuildError, match="no `id:` line"):
            b.build()

    def test_two_cells_sharing_an_id_fail_the_build(self, repo):
        write(repo, "```python exec\nid: same\n1\n```\n\n```python exec\nid: same\n2\n```\n")
        with pytest.raises(b.BuildError, match="share the id"):
            b.build()

    def test_a_tutorial_with_no_cells_carries_an_empty_manifest(self, repo):
        write(repo, "Prose only, no code at all.\n")
        b.build()
        assert manifest(built(repo))["cells"] == []


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
    only the fence's language word and the pill it produces differ."""

    def test_a_sql_exec_fence_becomes_a_cell(self, repo):
        write(repo, SQL_CELL)
        b.build()
        page = built(repo)
        assert 'class="dl-cell" data-cell-id="only-sql-cell"' in page
        assert 'class="dl-editor"' in page and 'class="dl-output"' in page

    def test_the_pill_reads_sql_not_python(self, repo):
        write(repo, SQL_CELL)
        b.build()
        page = built(repo)
        assert '<span class="dl-cell-pill-type" data-type="sql">SQL</span>' in page

    def test_a_python_cell_on_the_same_page_still_reads_python(self, repo):
        write(repo, SQL_CELL + "\n" + CELL)
        b.build()
        page = built(repo)
        assert '<span class="dl-cell-pill-type" data-type="sql">SQL</span>' in page
        assert '<span class="dl-cell-pill-type" data-type="python">Python</span>' in page

    def test_the_sql_travels_in_the_manifest_as_a_typed_cell(self, repo):
        write(repo, SQL_CELL)
        b.build()
        cells = manifest(built(repo))["cells"]
        assert cells == [{"id": "only-sql-cell", "hint": None, "code": "SELECT 1;", "type": "sql"}]

    def test_a_plain_python_cell_carries_no_type_key(self, repo):
        write(repo, CELL)
        b.build()
        assert "type" not in manifest(built(repo))["cells"][0]

    def test_a_sql_cell_gets_hint_and_expect_like_any_other(self, repo):
        write(repo, '```sql exec\nid: c\nhint: Try SELECT *.\nSELECT 1;\n```\n')
        b.build()
        page = built(repo)
        assert manifest(page)["cells"][0]["hint"] == "Try SELECT *."
        assert 'aria-controls="dl-hint-c"' in page

    def test_a_tutorial_with_a_sql_cell_needs_sqlite(self, repo):
        write(repo, SQL_CELL)
        b.build()
        assert manifest(built(repo))["needsSqlite"] is True

    def test_a_tutorial_with_no_sql_cells_does_not_need_sqlite(self, repo):
        write(repo, CELL)
        b.build()
        assert "needsSqlite" not in manifest(built(repo))

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
    only a fence's first word."""

    def test_a_solo_site_pane_becomes_an_editor(self, repo):
        write(repo, SITE_HTML)
        b.build()
        page = built(repo)
        assert 'class="dl-site-editor" data-site-name="hero"' in page
        assert 'data-lang="html"' in page
        assert 'class="dl-editor"' in page

    def test_consecutive_panes_of_the_same_site_share_one_editor(self, repo):
        write(repo, SITE_HTML + SITE_CSS + SITE_JS)
        b.build()
        page = built(repo)
        assert page.count('data-site-name="hero"') == 1
        assert page.count('class="dl-site-pane"') == 3

    def test_panes_are_optional_html_and_css_only(self, repo):
        write(repo, SITE_HTML + SITE_CSS)
        b.build()
        page = built(repo)
        assert 'data-lang="html"' in page and 'data-lang="css"' in page
        assert 'data-lang="js"' not in page

    def test_a_js_pane_gets_a_run_button_and_a_console(self, repo):
        write(repo, SITE_HTML + SITE_JS)
        b.build()
        page = built(repo)
        assert "dl-btn-site-run" in page
        assert "dl-site-console-output" in page

    def test_an_html_and_css_only_editor_gets_no_run_button_or_console(self, repo):
        write(repo, SITE_HTML + SITE_CSS)
        b.build()
        page = built(repo)
        assert "dl-btn-site-run" not in page
        assert "dl-site-console-output" not in page

    def test_the_starter_code_travels_in_the_manifest_not_the_dom(self, repo):
        write(repo, SITE_HTML)
        b.build()
        page = built(repo)
        assert "<button>Hi</button>" not in page
        editors = manifest(page)["siteEditors"]
        assert editors == [{"name": "hero", "panes": {"html": {"id": "hero-html", "code": "<button>Hi</button>"}}}]

    def test_a_tutorial_with_no_site_editors_carries_no_manifest_key(self, repo):
        write(repo, CELL)
        b.build()
        assert "siteEditors" not in manifest(built(repo))

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

    def test_two_different_sites_on_one_page_both_render(self, repo):
        write(repo, SITE_HTML + SITE_CSS + "```html site\nid: aside-html\nsite: aside\n<p>hi</p>\n```\n")
        b.build()
        page = built(repo)
        assert 'data-site-name="hero"' in page
        assert 'data-site-name="aside"' in page
        assert [e["name"] for e in manifest(page)["siteEditors"]] == ["hero", "aside"]

    def test_a_cell_between_two_site_editors_does_not_confuse_them(self, repo):
        write(repo, SITE_HTML + SITE_CSS + CELL + "```html site\nid: aside-html\nsite: aside\n<p>hi</p>\n```\n")
        b.build()
        page = built(repo)
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
    def test_an_image_without_alt_fails_the_build(self, repo):
        write(repo, 'A diagram:\n\n<img src="d.png">\n')
        asset(repo, "sample", "d.png")
        with pytest.raises(b.BuildError, match="no alt attribute"):
            b.build()

    def test_an_explicitly_empty_alt_is_allowed_as_decorative(self, repo):
        write(repo, 'A flourish:\n\n<img src="d.png" alt="">\n')
        asset(repo, "sample", "d.png")
        b.build()
        assert 'src="sample/d.png"' in built(repo)

    def test_markdown_image_syntax_carries_its_alt_through(self, repo):
        write(repo, "![A labelled diagram](d.png)\n")
        asset(repo, "sample", "d.png")
        b.build()
        assert 'alt="A labelled diagram"' in built(repo)


class TestTutorialAssets:
    """A tutorial is a folder; an asset it uses sits there and is referenced
    by its plain name (planning/ROADMAP.md Phase 1)."""

    def test_an_asset_is_copied_beside_the_tutorial(self, repo):
        write(repo, '<img src="d.png" alt="A diagram">\n')
        asset(repo, "sample", "d.png", b"PNG-BYTES")
        b.build()
        copied = repo / "site" / "tutorials" / "sample" / "d.png"
        assert copied.read_bytes() == b"PNG-BYTES"

    def test_the_current_release_reaches_into_the_tutorials_folder(self, repo):
        # Served one level above its own folder, so a plain name needs the
        # folder added to still resolve.
        write(repo, '<img src="d.png" alt="A diagram">\n')
        asset(repo, "sample", "d.png")
        b.build()
        assert 'src="sample/d.png"' in built(repo)

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

    def test_an_external_image_is_left_alone(self, repo):
        write(repo, '<img src="https://example.org/d.png" alt="A diagram">\n')
        b.build()
        assert 'src="https://example.org/d.png"' in built(repo)

    def test_the_glossary_is_not_treated_as_an_asset(self, repo):
        write(repo, "Prose.\n")
        glossary(repo, "sample", [{"term": "x", "kind": "concept", "definition": "y"}])
        b.build()
        assert not (repo / "site" / "tutorials" / "sample" / "sample.glossary.yaml").exists()

    def test_a_downloadable_sibling_file_is_linked_and_copied(self, repo):
        # A downloadable starting point, linked with href= rather than shown
        # with src=; resolves the same one-level-above-itself way a picture does.
        write(repo, '<a href="demo.html">demo.html</a>\n')
        asset(repo, "sample", "demo.html", b"<p>a starter</p>")
        b.build()
        assert 'href="sample/demo.html"' in built(repo)
        copied = repo / "site" / "tutorials" / "sample" / "demo.html"
        assert copied.read_bytes() == b"<p>a starter</p>"

    def test_an_href_naming_a_file_that_is_not_there_is_left_alone(self, repo):
        # Unlike src=, a missing href doesn't fail the build: a page links to
        # plenty of non-local things, and this must not mistake an
        # already-resolved tutorial: link for a missing file.
        write(repo, '<a href="not-a-real-file.html">a link</a>\n')
        b.build()
        assert 'href="not-a-real-file.html"' in built(repo)

    def test_an_external_href_is_left_alone(self, repo):
        write(repo, '<a href="https://example.org/demo.html">demo</a>\n')
        b.build()
        assert 'href="https://example.org/demo.html"' in built(repo)

    def test_a_src_or_href_shown_as_text_in_a_code_span_is_not_resolved(self, repo):
        # Code-span text escapes angle brackets but leaves the quoted src/href
        # alone, so this must be told apart from a real attribute or a
        # quick-reference table breaks the build over its own example.
        write(repo, 'Shown as text: `<img src="not-a-real-file.png">` and '
                    '`<a href="not-a-real-file.html">`.\n')
        b.build()
        page = built(repo)
        assert 'src="not-a-real-file.png"' in page
        assert 'href="not-a-real-file.html"' in page


class TestFrontmatter:
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

    def test_a_packages_list_widens_the_manifest(self, repo):
        path = write(repo, "Prose.\n")
        path.write_text(path.read_text().replace("version: 2026.08.23.1", "version: 2026.08.23.1\npackages: [sympy]"))
        b.build()
        assert manifest(built(repo))["packages"] == ["sympy"]

    def test_no_packages_field_leaves_the_runtime_default_alone(self, repo):
        write(repo, "Prose.\n")
        b.build()
        assert "packages" not in manifest(built(repo))

    def test_a_title_with_markup_is_escaped_into_the_page(self, repo):
        path = write(repo, "Prose.\n")
        path.write_text(path.read_text().replace('title: "A Title"', 'title: "A <b>Title</b>"'))
        b.build()
        assert "<title>A &lt;b&gt;Title&lt;/b&gt; — dewlab</title>" in built(repo)


class TestMaths:
    def test_inline_maths_is_marked_and_survives_markdown(self, repo):
        write(repo, "The term $a_i + b_j$ matters.\n")
        b.build()
        page = built(repo)
        assert '<span class="dl-math">a_i + b_j</span>' in page
        assert "<em>" not in page  # the underscores would otherwise become emphasis

    def test_display_maths_gets_its_own_class(self, repo):
        write(repo, "$$x^2$$\n")
        b.build()
        assert '<span class="dl-math dl-math-display">x^2</span>' in built(repo)

    def test_the_source_tex_stays_in_the_page_as_a_fallback(self, repo):
        write(repo, r"Here: $\frac{1}{3}$." + "\n")
        b.build()
        assert r"\frac{1}{3}" in built(repo)

    def test_currency_is_not_mistaken_for_maths(self, repo):
        write(repo, "It cost $5 or $6 depending on the day.\n")
        b.build()
        page = built(repo)
        assert "dl-math" not in page
        assert "$5 or $6" in page

    def test_an_escaped_dollar_stays_literal(self, repo):
        write(repo, r"A round \$99 exactly." + "\n")
        b.build()
        page = built(repo)
        assert "$99" in page
        assert "dl-math" not in page

    def test_maths_inside_a_fence_is_left_alone(self, repo):
        write(repo, "```python\ncost = '$5 and $6'\n```\n")
        b.build()
        assert "dl-math" not in built(repo)

    def test_the_manifest_flags_a_page_with_maths(self, repo):
        write(repo, "Some $x$ here.\n")
        b.build()
        assert manifest(built(repo))["math"] is True

    def test_a_page_without_maths_carries_no_flag(self, repo):
        write(repo, "No maths at all.\n")
        b.build()
        assert "math" not in manifest(built(repo))

    def test_tex_is_escaped_into_the_markup(self, repo):
        write(repo, "$a < b$\n")
        b.build()
        page = built(repo)
        assert "a &lt; b" in page


class TestIllustrativeCode:
    def test_an_untagged_fence_is_marked_for_highlighting(self, repo):
        write(repo, "```python\ntotal = 1\n```\n")
        b.build()
        assert '<pre class="dl-static" data-lang="python"><code>total = 1</code></pre>' in built(repo)

    def test_a_fence_with_no_language_still_renders(self, repo):
        write(repo, "```\nplain text\n```\n")
        b.build()
        page = built(repo)
        assert '<pre class="dl-static"><code>plain text</code></pre>' in page

    def test_illustrative_code_is_escaped(self, repo):
        write(repo, "```python\nprint('<b>hi</b>')\n```\n")
        b.build()
        page = built(repo)
        assert "&lt;b&gt;hi&lt;/b&gt;" in page
        assert "<b>hi</b>" not in page

    def test_it_carries_no_run_button(self, repo):
        write(repo, "```python\ntotal = 1\n```\n")
        b.build()
        assert "dl-btn-run" not in built(repo)

    def test_markdown_cannot_reinterpret_what_is_inside_it(self, repo):
        write(repo, "```python\nname_with_underscores = 1\n```\n")
        b.build()
        page = built(repo)
        assert "name_with_underscores" in page
        assert "<em>" not in page


class TestListsWrittenTightAgainstProse:
    """Markdown written elsewhere often puts a list straight under a paragraph."""

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

    def test_the_paragraph_above_it_is_left_intact(self, repo):
        write(repo, "The pattern appears everywhere:\n- Looking up a contact\n")
        b.build()
        assert "<p>The pattern appears everywhere:</p>" in built(repo)

    def test_a_list_that_already_had_its_blank_line_is_untouched(self, repo):
        write(repo, "Consider:\n\n- One\n- Two\n")
        b.build()
        assert built(repo).count("<li>") == 2

    def test_a_list_under_a_heading_is_untouched(self, repo):
        write(repo, "## A heading\n- One\n- Two\n")
        b.build()
        page = built(repo)
        assert "<ul>" in page and "<h2" in page

    def test_items_within_a_list_are_not_split_apart(self, repo):
        write(repo, "Consider:\n- One\n- Two\n- Three\n")
        b.build()
        page = built(repo)
        assert page.count("<ul>") == 1
        assert page.count("<li>") == 3

    def test_a_dash_inside_a_fence_is_left_alone(self, repo):
        write(repo, "```python\ntotal = 1\n- not a list\n```\n")
        b.build()
        assert "<li>" not in built(repo)

    def test_a_hyphenated_sentence_is_not_mistaken_for_a_list(self, repo):
        write(repo, "A sentence.\n-5 degrees is cold.\n")
        b.build()
        assert "<li>" not in built(repo)


class TestNotes:
    """planning/SIDEBAR_CONTENT.md §3/§4: unlike the glossary, a note is
    never cumulative across a series — it belongs to the tutorial that wrote it."""

    def test_a_note_appears_in_the_manifest(self, repo):
        write(repo, '<aside class="dl-note" id="why-it-works">\n\n'
                    "Because reasons.\n\n</aside>\n\nMore prose.\n", slug="one")
        b.build()
        assert manifest(built(repo, "one"))["notes"] == [
            {"id": "why-it-works", "html": "<p>Because reasons.</p>"},
        ]

    def test_a_notes_content_is_markdown_not_raw_text(self, repo):
        # Converted on its own, separately from the surrounding raw HTML
        # block, unlike a fold's own contents (planning/SIDEBAR_CONTENT.md §1).
        write(repo, '<aside class="dl-note" id="pic">\n\n'
                    '![a chart](chart.png)\n\n</aside>\n', slug="one")
        b.build()
        assert manifest(built(repo, "one"))["notes"] == [
            {"id": "pic", "html": '<p><img alt="a chart" src="chart.png" /></p>'},
        ]

    def test_an_image_in_a_note_still_needs_alt_text(self, repo):
        write(repo, '<aside class="dl-note" id="pic">\n\n'
                    '<img src="chart.png">\n\n</aside>\n', slug="one")
        with pytest.raises(b.BuildError, match="no alt attribute"):
            b.build()

    def test_a_note_is_removed_from_the_page_body(self, repo):
        write(repo, '<aside class="dl-note" id="why-it-works">\n\n'
                    "Because reasons.\n\n</aside>\n\nMore prose.\n", slug="one")
        b.build()
        page = built(repo, "one")
        assert "dl-note" not in page.split("dewlab-manifest")[0]
        assert "More prose." in page

    def test_a_tutorial_with_no_notes_has_no_notes_key(self, repo):
        write(repo, "Prose only.\n", slug="one")
        b.build()
        assert "notes" not in manifest(built(repo, "one"))

    def test_two_notes_sharing_an_id_fail_the_build(self, repo):
        write(repo,
              '<aside class="dl-note" id="dup">\n\nOne.\n\n</aside>\n\n'
              '<aside class="dl-note" id="dup">\n\nTwo.\n\n</aside>\n', slug="one")
        with pytest.raises(b.BuildError, match="share the id"):
            b.build()

    def test_a_note_is_not_inherited_by_a_later_tutorial(self, repo):
        write(repo, '<aside class="dl-note" id="early">\n\nEarly note.\n\n</aside>\n',
              slug="one")
        write(repo, "Two.\n", slug="two")
        set_order(repo, "computational-methods", "python-fundamentals", ["one", "two"])
        b.build()
        assert "notes" not in manifest(built(repo, "two"))


class TestDatasets:
    def test_a_declared_dataset_appears_in_the_manifest(self, repo):
        path = write(repo, "Prose.\n", slug="one")
        add_frontmatter(path, "datasets:\n  - life-expectancy\n")
        dataset(repo, "life-expectancy", source="World Bank", license="CC-BY-4.0",
                description="Life expectancy by country and year.")
        b.build()
        assert manifest(built(repo, "one"))["datasets"] == [{
            "name": "life-expectancy",
            "source": "World Bank",
            "license": "CC-BY-4.0",
            "description": "Life expectancy by country and year.",
        }]

    def test_a_declared_dataset_can_be_a_text_file(self, repo):
        path = write(repo, "Prose.\n", slug="one")
        add_frontmatter(path, "datasets:\n  - a-book\n")
        dataset(repo, "a-book", with_csv=False, with_txt=True,
                source="Some author", license="Public domain",
                description="A plain-text dataset, loaded with load_text().")
        b.build()
        assert manifest(built(repo, "one"))["datasets"] == [{
            "name": "a-book",
            "source": "Some author",
            "license": "Public domain",
            "description": "A plain-text dataset, loaded with load_text().",
        }]

    def test_a_tutorial_with_no_datasets_has_no_datasets_key(self, repo):
        write(repo, "Prose.\n", slug="one")
        b.build()
        assert "datasets" not in manifest(built(repo, "one"))

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

    def test_a_dataset_is_not_inherited_by_a_later_tutorial(self, repo):
        path = write(repo, "One.\n", slug="one")
        add_frontmatter(path, "datasets:\n  - a-dataset\n")
        dataset(repo, "a-dataset")
        write(repo, "Two.\n", slug="two")
        set_order(repo, "computational-methods", "python-fundamentals", ["one", "two"])
        b.build()
        assert "datasets" not in manifest(built(repo, "two"))


class TestFolds:
    """A `<details>` must name a fold class; an earlier style-guide draft
    showed a bare one, which renders as a plain browser triangle with none
    of this project's styling."""

    def test_an_answer_fold_is_fine(self, repo):
        write(repo, '<details class="dl-answer"><summary>answer</summary>\n\n'
                    "Forty-two.\n\n</details>\n")
        b.build()
        assert "dl-answer" in built(repo)

    def test_a_hint_fold_is_fine(self, repo):
        write(repo, '<details class="dl-hint"><summary>stuck?</summary>\n\n'
                    "1. Try this.\n\n</details>\n")
        b.build()
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
    rather than the finished HTML, so its body converts like any other prose."""

    CELL = "```python exec\nid: stub\n# Your add(a, b)\n```\n\n"

    def test_defaults_to_the_cell_above_and_five_errors(self, repo):
        write(repo, self.CELL + "```hint\nWhat did the last line say?\n```\n")
        b.build()
        page = built(repo)
        assert 'class="dl-hint dl-hint-staged"' in page
        assert 'data-cell="stub"' in page
        assert 'data-after="errors:5"' in page
        assert " hidden>" in page
        assert "<summary>Let’s slow down a moment…</summary>" in page

    def test_the_body_is_markdown_and_maths(self, repo):
        write(repo, self.CELL + "```hint\ntitle: some steps\n1. Look at `a[0]`.\n2. Then $x_i$.\n```\n")
        b.build()
        page = built(repo)
        assert "<summary>some steps</summary>" in page
        assert "<ol>" in page and "<code>a[0]</code>" in page
        assert "dl-math" in page

    def test_both_trigger_grammars_canonicalise_the_same_way(self, repo):
        write(repo, self.CELL
              + "```hint\nafter: 3 identical errors and 2 minutes\nA.\n```\n\n"
              + "```hint\nafter: same-errors:3, minutes:2\nB.\n```\n\n"
              + "```hint\nafter: 2 unchanged runs, 8 runs & 1 failed check\nC.\n```\n")
        b.build()
        page = built(repo)
        assert page.count('data-after="same-errors:3 minutes:2"') == 2
        assert 'data-after="unchanged:2 runs:8 check-fails:1"' in page

    def test_empty_results_reads_both_grammars(self, repo):
        write(repo, self.CELL
              + "```hint\nafter: 2 empty results\nA.\n```\n\n"
              + "```hint\nafter: empty-result:3\nB.\n```\n")
        b.build()
        page = built(repo)
        assert 'data-after="empty-results:2"' in page
        assert 'data-after="empty-results:3"' in page

    def test_a_second_hint_on_the_same_cell_gets_its_own_id(self, repo):
        write(repo, self.CELL + "```hint\nA.\n```\n\n```hint\nafter: 12 errors\nB.\n```\n")
        b.build()
        page = built(repo)
        assert 'id="dl-staged-stub-0"' in page and 'id="dl-staged-stub-1"' in page

    def test_for_names_a_cell_anywhere_on_the_page(self, repo):
        write(repo, "```hint\nfor: later\nEarly hint.\n```\n\n"
                    "```python exec\nid: later\n1\n```\n")
        b.build()
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
