"""Unit tests for build.py — the markdown-to-HTML converter (Phase 1).

build.py resolves everything against module-level paths derived from its own
location, so the fixture below repoints those at a temporary directory and
writes tutorials into it. That keeps the tests independent of whatever real
content happens to be sitting in tutorials/.

    python3 -m pytest tests/test_build.py -q
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import build as b  # noqa: E402

SHELL = (Path(__file__).resolve().parent.parent / "assets" / "shell.html").read_text()

FRONTMATTER = """---
title: "A Title"
slug: {slug}
module: computational-methods
year: "2026-2027"
series: python-fundamentals
order: 1
version: {version}
---

"""


@pytest.fixture()
def repo(tmp_path, monkeypatch):
    """A throwaway repository laid out the way build.py expects."""
    for name in ("tutorials/computational-methods", "setup", "data", "assets"):
        (tmp_path / name).mkdir(parents=True)
    (tmp_path / "assets" / "shell.html").write_text(SHELL)

    monkeypatch.setattr(b, "ROOT", tmp_path)
    monkeypatch.setattr(b, "TUTORIALS", tmp_path / "tutorials")
    monkeypatch.setattr(b, "SETUP", tmp_path / "setup")
    monkeypatch.setattr(b, "DATA", tmp_path / "data")
    monkeypatch.setattr(b, "ASSETS", tmp_path / "assets")
    monkeypatch.setattr(b, "SHELL", tmp_path / "assets" / "shell.html")
    monkeypatch.setattr(b, "OUT", tmp_path / "site")
    return tmp_path


def write(repo: Path, body: str, slug: str = "sample", version: int = 1) -> Path:
    path = repo / "tutorials" / "computational-methods" / f"{slug}.md"
    path.write_text(FRONTMATTER.format(slug=slug, version=version) + body)
    return path


def built(repo: Path, slug: str = "sample") -> str:
    return (repo / "site" / "tutorials" / "computational-methods" / f"{slug}.html").read_text()


def manifest(page: str) -> dict:
    raw = re.search(r'id="dewlab-manifest">(.*?)</script>', page, re.S).group(1)
    return json.loads(raw)


CELL = """```python exec
id: only-cell
print("hello")
```
"""


class TestTheHappyPath:
    def test_a_tutorial_builds_to_its_module_folder(self, repo):
        write(repo, "Some prose.\n")
        written = b.build()
        assert repo / "site" / "tutorials" / "computational-methods" / "sample.html" in written

    def test_every_shell_token_is_filled(self, repo):
        write(repo, "Some prose.\n")
        b.build()
        assert "{{" not in built(repo)

    def test_frontmatter_reaches_the_page_metadata(self, repo):
        write(repo, "Some prose.\n", version=4)
        b.build()
        page = built(repo)
        assert '<meta name="tutorial-version" content="4">' in page
        assert '<meta name="tutorial-slug" content="sample">' in page

    def test_prose_becomes_html(self, repo):
        write(repo, "# Heading\n\nA paragraph.\n")
        b.build()
        assert "<h1" in built(repo)
        assert "<p>A paragraph.</p>" in built(repo)

    def test_asset_paths_climb_out_of_the_module_folder(self, repo):
        write(repo, "Some prose.\n")
        b.build()
        assert manifest(built(repo))["assetBase"] == "../../assets/"
        assert manifest(built(repo))["dataBase"] == "../../data/"

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
        write(repo, "```python exec\nid: c\n{{include: ../../../etc/passwd}}\n```\n")
        with pytest.raises(b.BuildError, match="escapes the repository|does not exist"):
            b.build()


class TestCrossLinks:
    def test_a_link_resolves_to_a_relative_href(self, repo):
        write(repo, "See [other](tutorial:other).\n", slug="sample")
        write(repo, "Other.\n", slug="other")
        b.build()
        assert 'href="other.html"' in built(repo, "sample")

    def test_an_anchor_is_kept(self, repo):
        write(repo, "See [other](tutorial:other#a-heading).\n", slug="sample")
        write(repo, "## A heading\n", slug="other")
        b.build()
        assert 'href="other.html#a-heading"' in built(repo, "sample")

    def test_a_cell_id_counts_as_an_anchor(self, repo):
        write(repo, "See [other](tutorial:other#only-cell).\n", slug="sample")
        write(repo, CELL, slug="other")
        b.build()
        assert 'href="other.html#only-cell"' in built(repo, "sample")

    def test_an_unknown_slug_fails_the_build(self, repo):
        write(repo, "See [nowhere](tutorial:nowhere).\n")
        with pytest.raises(b.BuildError, match="unknown tutorial"):
            b.build()

    def test_an_unknown_anchor_fails_the_build(self, repo):
        write(repo, "See [other](tutorial:other#absent).\n", slug="sample")
        write(repo, "Other.\n", slug="other")
        with pytest.raises(b.BuildError, match="no anchor"):
            b.build()

    def test_two_tutorials_sharing_a_slug_fail_the_build(self, repo):
        write(repo, "One.\n", slug="same")
        path = repo / "tutorials" / "computational-methods" / "second.md"
        path.write_text(FRONTMATTER.format(slug="same", version=1) + "Two.\n")
        with pytest.raises(b.BuildError, match="already used by"):
            b.build()

    def test_an_ordinary_link_is_left_alone(self, repo):
        write(repo, "See [the docs](https://example.org/page).\n")
        b.build()
        assert 'href="https://example.org/page"' in built(repo)


class TestAltText:
    def test_an_image_without_alt_fails_the_build(self, repo):
        write(repo, 'A diagram:\n\n<img src="d.png">\n')
        with pytest.raises(b.BuildError, match="no alt attribute"):
            b.build()

    def test_an_explicitly_empty_alt_is_allowed_as_decorative(self, repo):
        write(repo, 'A flourish:\n\n<img src="d.png" alt="">\n')
        b.build()
        assert 'src="d.png"' in built(repo)

    def test_markdown_image_syntax_carries_its_alt_through(self, repo):
        write(repo, "![A labelled diagram](d.png)\n")
        b.build()
        assert 'alt="A labelled diagram"' in built(repo)


class TestFrontmatter:
    def test_a_missing_field_fails_the_build(self, repo):
        path = write(repo, "Prose.\n")
        path.write_text(path.read_text().replace("version: 1\n", ""))
        with pytest.raises(b.BuildError, match="missing version"):
            b.build()

    def test_a_file_without_frontmatter_fails_the_build(self, repo):
        (repo / "tutorials" / "computational-methods" / "bare.md").write_text("Just prose.\n")
        with pytest.raises(b.BuildError, match="no YAML frontmatter"):
            b.build()

    def test_unclosed_frontmatter_fails_the_build(self, repo):
        (repo / "tutorials" / "computational-methods" / "bad.md").write_text("---\ntitle: x\n")
        with pytest.raises(b.BuildError, match="never closed"):
            b.build()

    def test_a_packages_list_widens_the_manifest(self, repo):
        path = write(repo, "Prose.\n")
        path.write_text(path.read_text().replace("version: 1", "version: 1\npackages: [sympy]"))
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


class TestBuildingNothing:
    def test_an_empty_tutorials_folder_builds_nothing_and_does_not_fail(self, repo):
        assert b.build() == []


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


class TestNavigation:
    def series(self, repo, count: int = 3, series: str = "s", module: str = "computational-methods"):
        for n in range(1, count + 1):
            path = repo / "tutorials" / module / f"t{n}.md"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(
                f'---\ntitle: "Tutorial {n}"\nslug: t{n}\nmodule: {module}\n'
                f'year: "2026-2027"\nseries: {series}\norder: {n}\nversion: 1\n---\n\nProse.\n'
            )

    def page(self, repo, slug, module="computational-methods"):
        return (repo / "site" / "tutorials" / module / f"{slug}.html").read_text()

    def test_a_middle_tutorial_links_both_ways(self, repo):
        self.series(repo)
        b.build()
        page = self.page(repo, "t2")
        assert '<a class="dl-nav-prev" href="t1.html">Tutorial 1</a>' in page
        assert '<a class="dl-nav-next" href="t3.html">Tutorial 3</a>' in page

    def test_the_first_has_no_previous_and_the_last_no_next(self, repo):
        self.series(repo)
        b.build()
        assert "dl-nav-prev" not in self.page(repo, "t1")
        assert "dl-nav-next" in self.page(repo, "t1")
        assert "dl-nav-next" not in self.page(repo, "t3")
        assert "dl-nav-prev" in self.page(repo, "t3")

    def test_every_page_offers_the_way_back_to_the_contents(self, repo):
        self.series(repo)
        b.build()
        for slug in ("t1", "t2", "t3"):
            assert '<a class="dl-nav-up" href="../../index.html">' in self.page(repo, slug)

    def test_order_decides_the_sequence_not_the_filename(self, repo):
        self.series(repo)
        # reverse the orders: t1 becomes last, t3 first
        for n, order in ((1, 3), (3, 1)):
            path = repo / "tutorials" / "computational-methods" / f"t{n}.md"
            path.write_text(path.read_text().replace(f"order: {n}", f"order: {order}"))
        b.build()
        assert '<a class="dl-nav-next" href="t2.html">' in self.page(repo, "t3")
        assert "dl-nav-next" not in self.page(repo, "t1")

    def test_two_series_do_not_link_into_each_other(self, repo):
        self.series(repo, count=2, series="one")
        path = repo / "tutorials" / "computational-methods" / "other.md"
        path.write_text(
            '---\ntitle: "Other"\nslug: other\nmodule: computational-methods\n'
            'year: "2026-2027"\nseries: two\norder: 1\nversion: 1\n---\n\nProse.\n'
        )
        b.build()
        assert "dl-nav-prev" not in self.page(repo, "other")
        assert "dl-nav-next" not in self.page(repo, "other")

    def test_two_tutorials_in_the_same_position_still_build(self, repo, capsys):
        """Ambiguous ordering is worth saying, not worth stopping for."""
        self.series(repo, count=2)
        path = repo / "tutorials" / "computational-methods" / "t2.md"
        path.write_text(path.read_text().replace("order: 2", "order: 1"))
        b.build()
        assert "both order 1" in capsys.readouterr().err
        assert '<a class="dl-nav-next" href="t2.html">' in self.page(repo, "t1")

    def test_a_non_numeric_order_fails_the_build(self, repo):
        self.series(repo, count=1)
        path = repo / "tutorials" / "computational-methods" / "t1.md"
        path.write_text(path.read_text().replace("order: 1", "order: first"))
        with pytest.raises(b.BuildError, match="whole number"):
            b.build()


class TestTheContentsPage:
    def test_it_is_written_at_the_site_root(self, repo):
        write(repo, "Prose.\n")
        b.build()
        assert (repo / "site" / "index.html").is_file()

    def test_it_lists_every_tutorial_in_order(self, repo):
        for n, order in ((1, 2), (2, 1)):
            path = repo / "tutorials" / "computational-methods" / f"t{n}.md"
            path.write_text(
                f'---\ntitle: "Tutorial {n}"\nslug: t{n}\nmodule: computational-methods\n'
                f'year: "2026-2027"\nseries: s\norder: {order}\nversion: 1\n---\n\nProse.\n'
            )
        b.build()
        index = (repo / "site" / "index.html").read_text()
        assert index.index("Tutorial 2") < index.index("Tutorial 1")

    def test_the_links_reach_the_pages_they_name(self, repo):
        write(repo, "Prose.\n")
        b.build()
        index = (repo / "site" / "index.html").read_text()
        assert 'href="tutorials/computational-methods/sample.html"' in index
        assert (repo / "site" / "tutorials" / "computational-methods" / "sample.html").is_file()

    def test_it_needs_no_python_runtime(self, repo):
        write(repo, "Prose.\n")
        b.build()
        assert manifest((repo / "site" / "index.html").read_text())["cells"] == []

    def test_a_module_title_is_shown_where_one_is_given(self, repo):
        path = write(repo, "Prose.\n")
        path.write_text(path.read_text().replace(
            "module: computational-methods",
            'module: computational-methods\nmodule_title: "Computational Methods"'))
        b.build()
        assert "<h2>Computational Methods</h2>" in (repo / "site" / "index.html").read_text()

    def test_without_one_the_folder_name_is_shown(self, repo):
        write(repo, "Prose.\n")
        b.build()
        assert "<h2>computational-methods</h2>" in (repo / "site" / "index.html").read_text()

    def test_no_tutorials_means_no_index(self, repo):
        assert b.build() == []
        assert not (repo / "site" / "index.html").exists()


@pytest.fixture()
def repo_with_assets(repo):
    """A repository carrying the real assets, which the standalone export needs.

    Separate from `repo` because copying the vendor bundles costs a moment, and
    only these tests care. It is the same reason build() does not write the
    downloadable copies unless asked.
    """
    import shutil

    real = Path(__file__).resolve().parent.parent / "assets"
    shutil.rmtree(repo / "assets")
    shutil.copytree(real, repo / "assets")
    return repo


class TestTheDownloadableCopy:
    def test_it_is_written_beside_the_site(self, repo_with_assets):
        write(repo_with_assets, "Some prose.\n")
        b.build(standalone=True)
        assert (repo_with_assets / "site" / "download" / "sample.html").is_file()

    def test_it_is_not_written_unless_asked(self, repo_with_assets):
        write(repo_with_assets, "Some prose.\n")
        b.build()
        assert not (repo_with_assets / "site" / "download").exists()

    def test_the_page_links_to_it(self, repo_with_assets):
        write(repo_with_assets, "Some prose.\n")
        b.build(standalone=True)
        page = built(repo_with_assets)
        assert 'class="dl-download" href="../../download/sample.html" download' in page

    def standalone(self, repo) -> str:
        return (repo / "site" / "download" / "sample.html").read_text()

    def test_nothing_is_left_pointing_outside_the_file(self, repo_with_assets):
        write(repo_with_assets, "```python exec\nid: c\n1 + 1\n```\n")
        b.build(standalone=True)
        page = self.standalone(repo_with_assets)
        assert '<link rel="stylesheet"' not in page
        assert '<script type="module"' not in page

    def test_the_stylesheet_travels_inside_it(self, repo_with_assets):
        write(repo_with_assets, "Some prose.\n")
        b.build(standalone=True)
        assert "--dl-navy" in self.standalone(repo_with_assets)

    def test_the_runtime_travels_inside_it_as_a_classic_script(self, repo_with_assets):
        write(repo_with_assets, "Some prose.\n")
        b.build(standalone=True)
        page = self.standalone(repo_with_assets)
        assert "pyodide.js" in page  # the classic loader, not the module
        assert len(page) > 300_000  # the bundle really is in there

    def test_the_python_tools_travel_inside_it(self, repo_with_assets):
        write(repo_with_assets, "```python exec\nid: c\n1 + 1\n```\n")
        b.build(standalone=True)
        page = self.standalone(repo_with_assets)
        assert "toolsSource" in page
        assert "def check(" in page

    def test_it_marks_itself_as_standalone(self, repo_with_assets):
        write(repo_with_assets, "Some prose.\n")
        b.build(standalone=True)
        assert manifest(self.standalone(repo_with_assets))["standalone"] is True

    def test_maths_fonts_travel_with_a_maths_tutorial(self, repo_with_assets):
        write(repo_with_assets, "An equation: $x^2$.\n")
        b.build(standalone=True)
        assert "data:font/woff2;base64," in self.standalone(repo_with_assets)

    def test_a_tutorial_without_maths_does_not_carry_them(self, repo_with_assets):
        write(repo_with_assets, "No maths at all.\n")
        b.build(standalone=True)
        assert "data:font/woff2;base64," not in self.standalone(repo_with_assets)

    def test_navigation_is_dropped_rather_than_left_broken(self, repo_with_assets):
        for n in (1, 2):
            path = repo_with_assets / "tutorials" / "computational-methods" / f"t{n}.md"
            path.write_text(
                f'---\ntitle: "T{n}"\nslug: t{n}\nmodule: computational-methods\n'
                f'year: "2026-2027"\nseries: s\norder: {n}\nversion: 1\n---\n\nProse.\n'
            )
        b.build(standalone=True)
        page = (repo_with_assets / "site" / "download" / "t1.html").read_text()
        assert "<nav" not in page

    def test_it_warns_when_a_tutorial_loads_data_it_cannot_carry(self, repo_with_assets, capsys):
        write(repo_with_assets, '```python exec\nid: c\ndf = await load_csv("x.csv")\n```\n')
        b.build(standalone=True)
        assert "cannot reach" in capsys.readouterr().err
