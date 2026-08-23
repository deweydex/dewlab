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
import zipfile

import yaml
from pathlib import Path

import pytest

DEWLAB = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DEWLAB))

import build as b  # noqa: E402

SHELL = (DEWLAB / "assets" / "shell.html").read_text()

FRONTMATTER = """---
title: "A Title"
slug: {slug}
module: computational-methods
year: "2026-2027"
series: python-fundamentals
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


def set_order(repo: Path, module: str, series: str, slugs: list[str]) -> Path:
    """Write a series' order file. Ordering lives here now, not in frontmatter."""
    path = repo / "tutorials" / module / f"{series}.order.yaml"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("order:\n" + "".join(f"  - {slug}\n" for slug in slugs))
    return path


def write(repo: Path, body: str, slug: str = "sample",
          version: str = "2026.08.23.1") -> Path:
    path = repo / "tutorials" / "computational-methods" / f"{slug}.md"
    path.write_text(FRONTMATTER.format(slug=slug, version=version) + body)
    # Keep the series' order file listing whatever has been written so far.
    existing = sorted(
        p.stem for p in path.parent.glob("*.md")
    )
    set_order(repo, "computational-methods", "python-fundamentals", existing)
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

    def test_two_files_claiming_one_slug_and_one_version_fail_the_build(self, repo):
        """Two files sharing a slug are two *versions* of one tutorial now, so
        the collision that matters is the version: two releases cannot share a
        date and a number, because nothing could then say which is which."""
        write(repo, "One.\n", slug="same")
        path = repo / "tutorials" / "computational-methods" / "second.md"
        path.write_text(FRONTMATTER.format(slug="same", version="2026.08.23.1") + "Two.\n")
        set_order(repo, "computational-methods", "python-fundamentals", ["same"])
        with pytest.raises(b.BuildError, match="cannot share a date"):
            b.build()

    def test_two_modules_may_each_have_the_same_slug(self, repo):
        """The built path carries the module, so there is no ambiguity — and
        forcing them apart would mean naming tutorials around a constraint that
        does not exist."""
        write(repo, "One.\n", slug="first-steps")
        other = repo / "tutorials" / "other-module" / "first-steps.md"
        other.parent.mkdir(parents=True)
        other.write_text(
            '---\ntitle: "First Steps"\nslug: first-steps\nmodule: other-module\n'
            'year: "2026-2027"\nseries: intro\nversion: 2026.08.23.1\n---\n\nProse.\n'
        )
        set_order(repo, "other-module", "intro", ["first-steps"])
        b.build()
        assert (repo / "site" / "tutorials" / "other-module" / "first-steps.html").is_file()
        assert (repo / "site" / "tutorials" / "computational-methods"
                / "first-steps.html").is_file()

    def test_a_link_prefers_a_slug_in_its_own_module(self, repo):
        write(repo, "See [it](tutorial:twin).\n", slug="here")
        write(repo, "Mine.\n", slug="twin")
        other = repo / "tutorials" / "other-module" / "twin.md"
        other.parent.mkdir(parents=True)
        other.write_text(
            '---\ntitle: "Twin"\nslug: twin\nmodule: other-module\n'
            'year: "2026-2027"\nseries: intro\nversion: 2026.08.23.1\n---\n\nProse.\n'
        )
        set_order(repo, "other-module", "intro", ["twin"])
        b.build()
        assert 'href="twin.html"' in built(repo, "here")

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
        path.write_text(path.read_text().replace("version: 2026.08.23.1\n", ""))
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
    def series(self, repo, count: int = 3, series: str = "s", module: str = "computational-methods",
               order: list[str] | None = None):
        for n in range(1, count + 1):
            path = repo / "tutorials" / module / f"t{n}.md"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(
                f'---\ntitle: "Tutorial {n}"\nslug: t{n}\nmodule: {module}\n'
                f'year: "2026-2027"\nseries: {series}\nversion: 2026.08.23.1\n---\n\nProse.\n'
            )
        set_order(repo, module, series,
                  order or [f"t{n}" for n in range(1, count + 1)])

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

    def test_the_order_file_decides_the_sequence_not_the_filename(self, repo):
        """Reordering is moving a line, and nothing else changes."""
        self.series(repo, order=["t3", "t2", "t1"])
        b.build()
        assert '<a class="dl-nav-next" href="t2.html">' in self.page(repo, "t3")
        assert "dl-nav-next" not in self.page(repo, "t1")

    def test_two_series_do_not_link_into_each_other(self, repo):
        self.series(repo, count=2, series="one")
        path = repo / "tutorials" / "computational-methods" / "other.md"
        path.write_text(
            '---\ntitle: "Other"\nslug: other\nmodule: computational-methods\n'
            'year: "2026-2027"\nseries: two\nversion: 2026.08.23.1\n---\n\nProse.\n'
        )
        set_order(repo, "computational-methods", "two", ["other"])
        b.build()
        assert "dl-nav-prev" not in self.page(repo, "other")
        assert "dl-nav-next" not in self.page(repo, "other")

    def test_a_series_with_no_order_file_stops_the_build(self, repo):
        """Nothing knows the reading order, and guessing one would be worse."""
        self.series(repo, count=2)
        (repo / "tutorials" / "computational-methods" / "s.order.yaml").unlink()
        with pytest.raises(b.BuildError, match="decides the reading order"):
            b.build()

    def test_a_tutorial_the_order_file_forgets_stops_the_build(self, repo):
        self.series(repo, count=3, order=["t1", "t2"])
        with pytest.raises(b.BuildError, match="not listed"):
            b.build()

    def test_a_slug_with_no_tutorial_behind_it_stops_the_build(self, repo):
        """The more dangerous direction: the file looks complete and the series
        is quietly short."""
        self.series(repo, count=2, order=["t1", "t2", "t3"])
        with pytest.raises(b.BuildError, match="no tutorial in this series"):
            b.build()

    def test_a_slug_listed_twice_stops_the_build(self, repo):
        self.series(repo, count=2, order=["t1", "t2", "t1"])
        with pytest.raises(b.BuildError, match="more than once"):
            b.build()

    def test_order_left_in_the_frontmatter_stops_the_build(self, repo):
        """Half-migrated is worse than either state: the field would be ignored
        in silence, and it is exactly the field somebody would edit."""
        self.series(repo, count=1)
        path = repo / "tutorials" / "computational-methods" / "t1.md"
        path.write_text(path.read_text().replace("version: 2026.08.23.1", "order: 1\nversion: 2026.08.23.1"))
        with pytest.raises(b.BuildError, match="no longer belongs in frontmatter"):
            b.build()


class TestTheContentsPage:
    def test_it_is_written_at_the_site_root(self, repo):
        write(repo, "Prose.\n")
        b.build()
        assert (repo / "site" / "index.html").is_file()

    def test_it_lists_every_tutorial_in_order(self, repo):
        for n in (1, 2):
            path = repo / "tutorials" / "computational-methods" / f"t{n}.md"
            path.write_text(
                f'---\ntitle: "Tutorial {n}"\nslug: t{n}\nmodule: computational-methods\n'
                f'year: "2026-2027"\nseries: s\nversion: 2026.08.23.1\n---\n\nProse.\n'
            )
        set_order(repo, "computational-methods", "s", ["t2", "t1"])
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

    def module_headings(self, repo) -> list[str]:
        """The module headings in page order.

        By the heading rather than by substring: the slug also appears in every
        href below it, so a plain `index()` finds the link, not the heading."""
        page = (repo / "site" / "index.html").read_text()
        return re.findall(r"<h2>(.*?)</h2>", page)

    def test_modules_appear_in_the_order_the_module_file_gives(self, repo):
        """Alphabetical by folder name is not an order anybody chose — it is the
        same invisible accident the series order files were introduced to end."""
        write(repo, "Prose.\n")
        other = repo / "tutorials" / "zz-later-module"
        other.mkdir(parents=True)
        (other / "t1.md").write_text(
            '---\ntitle: "Elsewhere"\nslug: t1\nmodule: zz-later-module\n'
            'module_title: "Later Module"\nyear: "2026-2027"\nseries: s\nversion: 2026.08.23.1\n---\n\nProse.\n'
        )
        set_order(repo, "zz-later-module", "s", ["t1"])
        (repo / "tutorials" / "modules.yaml").write_text(
            "order:\n  - computational-methods\n  - zz-later-module\n")
        b.build()
        assert self.module_headings(repo) == ["computational-methods", "Later Module"]

        (repo / "tutorials" / "modules.yaml").write_text(
            "order:\n  - zz-later-module\n  - computational-methods\n")
        b.build()
        assert self.module_headings(repo) == ["Later Module", "computational-methods"]

    def test_an_unlisted_module_lands_last_rather_than_breaking_the_page(self, repo):
        """Lenient where the series files are strict: a tutorial missing from
        its order file vanishes, so that must stop the build. A module missing
        from here is still on the page, and that is not worth refusing over."""
        write(repo, "Prose.\n")
        other = repo / "tutorials" / "zz-later-module"
        other.mkdir(parents=True)
        (other / "t1.md").write_text(
            '---\ntitle: "Elsewhere"\nslug: t1\nmodule: zz-later-module\n'
            'module_title: "Later Module"\nyear: "2026-2027"\nseries: s\nversion: 2026.08.23.1\n---\n\nProse.\n'
        )
        set_order(repo, "zz-later-module", "s", ["t1"])
        (repo / "tutorials" / "modules.yaml").write_text(
            "order:\n  - zz-later-module\n")
        b.build()
        assert self.module_headings(repo) == ["Later Module", "computational-methods"]

    def test_no_module_file_falls_back_to_alphabetical(self, repo):
        write(repo, "Prose.\n")
        b.build()
        assert "computational-methods" in (repo / "site" / "index.html").read_text()

    def test_a_series_is_headed_by_its_name_not_its_filename(self, repo):
        """A module with two series shows a heading per series, and until one
        had two nobody saw that the heading was the slug."""
        write(repo, "Prose.\n")
        second = repo / "tutorials" / "computational-methods" / "looking-back.md"
        second.write_text(
            '---\ntitle: "Looking Back"\nslug: looking-back\n'
            "module: computational-methods\n"
            'year: "2026-2027"\nseries: reflections-and-review\nversion: 2026.08.23.1\n---\n\nProse.\n'
        )
        order = set_order(repo, "computational-methods", "reflections-and-review",
                          ["looking-back"])
        order.write_text('series: Reflections and review\n' + order.read_text())
        # `write` re-lists every markdown file it finds, so put the first series
        # back to just its own.
        set_order(repo, "computational-methods", "python-fundamentals", ["sample"])
        b.build()
        index = (repo / "site" / "index.html").read_text()
        assert "<h3>Reflections and review</h3>" in index
        assert "<h3>reflections-and-review</h3>" not in index

    def test_a_series_without_a_name_falls_back_to_its_filename(self, repo):
        """Optional, because a heading nobody sees is not worth a build error."""
        write(repo, "Prose.\n")
        second = repo / "tutorials" / "computational-methods" / "looking-back.md"
        second.write_text(
            '---\ntitle: "Looking Back"\nslug: looking-back\n'
            "module: computational-methods\n"
            'year: "2026-2027"\nseries: later\nversion: 2026.08.23.1\n---\n\nProse.\n'
        )
        set_order(repo, "computational-methods", "later", ["looking-back"])
        set_order(repo, "computational-methods", "python-fundamentals", ["sample"])
        b.build()
        assert "<h3>later</h3>" in (repo / "site" / "index.html").read_text()

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
        assert (repo_with_assets / "site" / "download" / "computational-methods" / "sample.html").is_file()

    def test_it_is_not_written_unless_asked(self, repo_with_assets):
        write(repo_with_assets, "Some prose.\n")
        b.build()
        assert not (repo_with_assets / "site" / "download").exists()

    def test_the_page_links_to_it(self, repo_with_assets):
        write(repo_with_assets, "Some prose.\n")
        b.build(standalone=True)
        page = built(repo_with_assets)
        assert 'href="../../download/computational-methods/sample.html"' in page

    def standalone(self, repo) -> str:
        return (repo / "site" / "download" / "computational-methods" / "sample.html").read_text()

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
                f'year: "2026-2027"\nseries: s\nversion: 2026.08.23.1\n---\n\nProse.\n'
            )
        set_order(repo_with_assets, "computational-methods", "s", ["t1", "t2"])
        b.build(standalone=True)
        page = (repo_with_assets / "site" / "download" / "computational-methods" / "t1.html").read_text()
        assert "<nav" not in page

    def test_the_version_list_does_not_travel_with_it(self, repo_with_assets):
        """Only the default gets a downloadable copy, so the other releases are
        not on the reader's disk. A picker offering to move to files that are
        not there would be worse than no picker."""
        for version in ("2026.06.02.1", "2026.09.15.1"):
            folder = repo_with_assets / "tutorials" / "computational-methods" / "sample"
            folder.mkdir(parents=True, exist_ok=True)
            (folder / f"v{version}.md").write_text(
                '---\ntitle: "The Tutorial"\nslug: sample\n'
                "module: computational-methods\n"
                f'year: "2026-2027"\nseries: python-fundamentals\nversion: {version}\n'
                "status: live\n---\n\nProse.\n"
            )
        set_order(repo_with_assets, "computational-methods", "python-fundamentals",
                  ["sample"])
        b.build(standalone=True)
        hosted = (repo_with_assets / "site" / "tutorials" / "computational-methods"
                  / "sample.html").read_text()
        assert len(manifest(hosted)["versions"]) == 2
        assert "versions" not in manifest(self.standalone(repo_with_assets))

    def test_it_warns_when_a_tutorial_loads_data_it_cannot_carry(self, repo_with_assets, capsys):
        write(repo_with_assets, '```python exec\nid: c\ndf = await load_csv("x.csv")\n```\n')
        b.build(standalone=True)
        assert "cannot reach" in capsys.readouterr().err


class TestTheSeriesArchive:
    def two_tutorials(self, repo):
        for n in (1, 2):
            path = repo / "tutorials" / "computational-methods" / f"t{n}.md"
            path.write_text(
                f'---\ntitle: "T{n}"\nslug: t{n}\nmodule: computational-methods\n'
                f'year: "2026-2027"\nseries: Core skills\nversion: 2026.08.23.1\n---\n\nProse.\n'
            )
        set_order(repo, "computational-methods", "Core skills", ["t1", "t2"])

    def archive(self, repo) -> Path:
        return repo / "site" / "download" / "computational-methods-core-skills.zip"

    def test_a_series_is_gathered_into_one_archive(self, repo_with_assets):
        self.two_tutorials(repo_with_assets)
        b.build(standalone=True)
        assert self.archive(repo_with_assets).is_file()

    def test_it_holds_every_downloadable_copy_in_the_series(self, repo_with_assets):
        self.two_tutorials(repo_with_assets)
        b.build(standalone=True)
        with zipfile.ZipFile(self.archive(repo_with_assets)) as archive:
            assert sorted(archive.namelist()) == [
                "computational-methods-core-skills/t1.html",
                "computational-methods-core-skills/t2.html",
            ]

    def test_what_it_holds_still_runs(self, repo_with_assets):
        self.two_tutorials(repo_with_assets)
        b.build(standalone=True)
        with zipfile.ZipFile(self.archive(repo_with_assets)) as archive:
            page = archive.read("computational-methods-core-skills/t1.html").decode()
        assert "pyodide.js" in page
        assert "--dl-navy" in page

    def test_the_contents_page_offers_it(self, repo_with_assets):
        self.two_tutorials(repo_with_assets)
        b.build(standalone=True)
        index = (repo_with_assets / "site" / "index.html").read_text()
        assert 'href="download/computational-methods-core-skills.zip"' in index
        assert "Download all 2" in index

    def test_a_series_of_one_is_offered_in_the_singular(self, repo_with_assets):
        """"Download all 1 as single files" is not a sentence, and a series of
        one stopped being hypothetical when reflections moved to their own."""
        path = repo_with_assets / "tutorials" / "computational-methods" / "t1.md"
        path.write_text(
            '---\ntitle: "One"\nslug: t1\nmodule: computational-methods\n'
            'year: "2026-2027"\nseries: core-skills\nversion: 2026.08.23.1\n---\n\nProse.\n'
        )
        set_order(repo_with_assets, "computational-methods", "core-skills", ["t1"])
        b.build(standalone=True)
        index = (repo_with_assets / "site" / "index.html").read_text()
        assert "Download this one as a single file" in index
        assert "Download all 1" not in index

    def test_a_build_without_the_copies_offers_nothing_to_download(self, repo):
        self.two_tutorials(repo)
        b.build()
        index = (repo / "site" / "index.html").read_text()
        assert ".zip" not in index
        assert not (repo / "site" / "download").exists()

    def test_a_series_name_written_for_people_becomes_a_filename(self):
        assert b.series_slug("MIT-PDP", "Maths & Programming") == "mit-pdp-maths-programming"

    def test_a_size_is_reported_in_units_a_person_reads(self, tmp_path):
        small = tmp_path / "small"
        small.write_bytes(b"x" * 4000)
        big = tmp_path / "big"
        big.write_bytes(b"x" * 2_500_000)
        assert b.readable_size(small) == "4 KB"
        assert b.readable_size(big) == "2 MB"


class TestTheSettingsPanel:
    def test_the_download_sits_in_the_panel_and_not_in_the_navigation(self, repo):
        write(repo, "Some prose.\n")
        b.build()
        page = built(repo)
        nav = re.search(r'<nav class="dl-nav dl-nav-top">.*?</nav>', page, re.DOTALL).group(0)
        assert "dl-download" not in nav
        section = re.search(
            r'<section class="dl-settings-section" id="dl-settings-download">.*?</section>',
            page, re.DOTALL,
        ).group(0)
        assert 'href="../../download/computational-methods/sample.html"' in section

    def test_the_contents_page_has_no_tutorial_to_download(self, repo):
        write(repo, "Some prose.\n")
        b.build()
        index = (repo / "site" / "index.html").read_text()
        assert (
            '<section class="dl-settings-section" id="dl-settings-download"></section>'
            in index
        )

    def test_one_control_opens_it(self, repo):
        write(repo, "Some prose.\n")
        b.build()
        page = built(repo)
        assert 'id="dl-settings-toggle"' in page
        assert 'aria-controls="dl-settings"' in page
        # The two separate toggles it replaced.
        assert "dl-texture-toggle" not in page
        assert "dl-progress-toggle" not in page

    def test_a_downloadable_copy_does_not_offer_its_own_download(self, repo_with_assets):
        write(repo_with_assets, "Some prose.\n")
        b.build(standalone=True)
        page = (repo_with_assets / "site" / "download" / "computational-methods" / "sample.html").read_text()
        assert (
            '<section class="dl-settings-section" id="dl-settings-download"></section>'
            in page
        )
        assert "download/computational-methods/sample.html" not in page

    def test_a_downloadable_copy_keeps_the_rest_of_the_panel(self, repo_with_assets):
        write(repo_with_assets, "```python exec\nid: c\n1 + 1\n```\n")
        b.build(standalone=True)
        page = (repo_with_assets / "site" / "download" / "computational-methods" / "sample.html").read_text()
        assert 'id="dl-settings-toggle"' in page
        assert 'id="dl-settings-work"' in page
        assert 'id="dl-settings-texture"' in page


class TestTheContentsOfAPage:
    def toc(self, repo) -> str:
        page = built(repo)
        match = re.search(r'<details class="dl-toc">.*?</details>', page, re.DOTALL)
        return match.group(0) if match else ""

    def sections(self, count: int, sub: str = "") -> str:
        return "\n".join(f"## Section {n}\n\n{sub}Prose.\n" for n in range(1, count + 1))

    def test_a_page_with_sections_gets_a_contents_list(self, repo):
        write(repo, self.sections(3))
        b.build()
        toc = self.toc(repo)
        assert 'href="#section-1"' in toc
        assert 'href="#section-3"' in toc
        assert "3 sections" in toc

    def test_it_starts_closed(self, repo):
        write(repo, self.sections(3))
        b.build()
        assert "<details class=\"dl-toc\">" in built(repo)
        assert "<details open" not in built(repo)

    def test_one_section_does_not_get_a_contents_list(self, repo):
        """A contents list for a single heading is furniture."""
        write(repo, self.sections(1))
        b.build()
        assert self.toc(repo) == ""

    def test_prose_with_no_sections_does_not_either(self, repo):
        write(repo, "Just prose, no headings at all.\n")
        b.build()
        assert self.toc(repo) == ""

    def test_sub_headings_nest_under_their_section(self, repo):
        write(repo, "## First\n\nProse.\n\n### Detail\n\nProse.\n\n## Second\n\nProse.\n")
        b.build()
        toc = self.toc(repo)
        assert re.search(r'href="#first".*?<ul>.*?href="#detail".*?</ul>', toc, re.DOTALL)

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

    def test_the_contents_page_has_no_contents_list_of_its_own(self, repo):
        write(repo, self.sections(3))
        b.build()
        assert "dl-toc" not in (repo / "site" / "index.html").read_text()

    def test_a_downloadable_copy_keeps_it(self, repo_with_assets):
        """Its links are inside the file, so they work from a student's disk."""
        write(repo_with_assets, self.sections(3))
        b.build(standalone=True)
        page = (repo_with_assets / "site" / "download" / "computational-methods" / "sample.html").read_text()
        assert 'href="#section-1"' in page


class TestTheStickyChrome:
    def test_the_masthead_and_navigation_are_one_group(self, repo):
        write(repo, "Some prose.\n")
        b.build()
        page = built(repo)
        chrome = re.search(r'<div class="dl-chrome".*?</div>', page, re.DOTALL).group(0)
        assert "dl-masthead" in chrome
        assert "dl-nav-top" in chrome

    def test_a_downloadable_copy_keeps_the_chrome_without_the_navigation(
        self, repo_with_assets
    ):
        write(repo_with_assets, "Some prose.\n")
        b.build(standalone=True)
        page = (repo_with_assets / "site" / "download" / "computational-methods" / "sample.html").read_text()
        assert "dl-chrome" in page
        assert "dl-nav" not in page.split("<style>")[0] + page.split("</style>")[-1]


class TestTheKnowledgeMap:
    def series(self, repo, count=4, covers=True):
        strands = ["programming", "programming", "algorithms", "algebra"]
        codes = ["PDP-LO4", "PDP-LO6", "MIT-6.3", "MIT-1.6"]
        (repo / "planning" / "curriculum").mkdir(parents=True, exist_ok=True)
        (repo / "planning" / "curriculum" / "outcomes.yaml").write_text(
            "outcomes:\n" + "".join(
                f"  - code: {c}\n    title: t\n    strand: {s}\n"
                for c, s in zip(codes, strands)
            )
        )
        for n in range(1, count + 1):
            block = ""
            if covers:
                block = f"covers:\n  a-section:\n    covers: [{codes[(n - 1) % 4]}]\n"
            (repo / "tutorials" / "computational-methods" / f"t{n}.md").write_text(
                f'---\ntitle: "Tutorial {n}"\nslug: t{n}\nmodule: computational-methods\n'
                f'year: "2026-2027"\nseries: s\nversion: 2026.08.23.1\n{block}'
                f"---\n\n# Tutorial {n}\n\n## A section\n\nProse.\n"
            )
        set_order(repo, "computational-methods", "s",
                  [f"t{n}" for n in range(1, count + 1)])

    def svg(self, repo) -> str:
        """The tutorial map lives on the tree page, under the topic tree."""
        page = repo / "site" / "tree.html"
        match = re.search(r'<svg class="dl-map".*?</svg>',
                          page.read_text() if page.is_file() else "", re.DOTALL)
        return match.group(0) if match else ""

    def test_a_series_gets_a_map(self, repo):
        self.series(repo)
        b.build()
        svg = self.svg(repo)
        assert svg.count('class="dl-map-node"') == 4
        assert svg.count('class="dl-map-next"') == 3

    def test_a_series_too_short_to_have_a_shape_gets_none(self, repo):
        self.series(repo, count=2)
        b.build()
        assert self.svg(repo) == ""

    def test_every_node_links_to_a_page_that_exists(self, repo):
        self.series(repo)
        b.build()
        for href in re.findall(r'<a class="dl-map-node" href="([^"]+)"', self.svg(repo)):
            assert (repo / "site" / href).is_file(), href

    def test_lanes_come_from_the_curriculum_data(self, repo):
        self.series(repo)
        b.build()
        svg = self.svg(repo)
        assert ">programming</text>" in svg
        assert ">algorithms</text>" in svg

    def test_it_still_builds_without_the_curriculum_data(self, repo):
        """The site has to build from the tutorials alone. Without the outcome
        data there is no topic tree — but the tutorial map does not need it."""
        self.series(repo, covers=False)
        (repo / "planning" / "curriculum" / "outcomes.yaml").unlink()
        b.build()
        assert (repo / "site" / "index.html").is_file()

    def test_naming_an_earlier_tutorial_draws_an_arrow_back_to_it(self, repo):
        self.series(repo)
        path = repo / "tutorials" / "computational-methods" / "t4.md"
        path.write_text(path.read_text() + "\nWe used this in Tutorial 1.\n")
        b.build()
        assert 'class="dl-map-back"' in self.svg(repo)

    def test_the_tutorial_just_before_does_not_get_a_second_arrow(self, repo):
        """The reading-order arrow already says that one."""
        self.series(repo)
        path = repo / "tutorials" / "computational-methods" / "t4.md"
        path.write_text(path.read_text() + "\nAs in Tutorial 3.\n")
        b.build()
        assert 'class="dl-map-back"' not in self.svg(repo)

    def test_a_long_title_is_shortened_rather_than_overflowing(self):
        assert b.shorten("Short") == "Short"
        # Cut at the limit, then back to the last whole word.
        assert b.shorten("A very considerably longer tutorial title") == (
            "A very considerably…"
        )
        assert len(b.shorten("A" * 60)) <= 23

    def test_a_tutorial_is_placed_by_what_it_mostly_covers(self):
        strands = {"A": "algebra", "B": "algebra", "C": "sets"}
        assert b.strand_of(["A", "B", "C"], strands) == "algebra"
        assert b.strand_of([], strands) == "other"


class TestAssetVersions:
    """A page that has been visited before must not be served an old stylesheet.

    Without a version in the URL, a browser keeps the copy it downloaded the
    first time however many times the site is published — and the result does
    not look like a caching problem, it looks like the page is broken, only for
    people who have been here before.

    Against the real assets, because a version of a file that is not there
    proves nothing.
    """

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


class TestVersionsOfATutorial:
    """A version is a release, not a save: the version students could first see
    it, and one they can go back to. `planning/VERSIONS.md`."""

    def release(self, repo, slug: str, version: str, status: str = "live",
                body: str = "Prose.\n") -> Path:
        """One release of a tutorial, in the folder its versions share."""
        folder = repo / "tutorials" / "computational-methods" / slug
        folder.mkdir(parents=True, exist_ok=True)
        path = folder / f"v{version}.md"
        path.write_text(
            f'---\ntitle: "The Tutorial"\nslug: {slug}\n'
            "module: computational-methods\n"
            f'year: "2026-2027"\nseries: python-fundamentals\nversion: {version}\n'
            f"status: {status}\n---\n\n{body}"
        )
        # Only a live release is on the route. A draft is not on the site at
        # all, and a beta is reachable without being part of the course — so
        # listing either would be the contradiction the order file refuses.
        if status == "live":
            listed = repo / "tutorials" / "computational-methods" / "python-fundamentals.order.yaml"
            already = [l.strip("- ").strip() for l in listed.read_text().splitlines()
                       if l.strip().startswith("- ")] if listed.is_file() else []
            if slug not in already:
                set_order(repo, "computational-methods", "python-fundamentals",
                          already + [slug])
        return path

    def out(self, repo, *parts) -> Path:
        return repo.joinpath("site", "tutorials", "computational-methods", *parts)

    def test_the_newest_live_version_answers_the_tutorial_url(self, repo):
        """Every link written before versions existed keeps working and keeps
        meaning "the current one"."""
        self.release(repo, "thing", "2026.06.02.1", body="Old.\n")
        self.release(repo, "thing", "2026.09.15.1", body="New.\n")
        b.build()
        assert "New." in self.out(repo, "thing.html").read_text()

    def test_an_older_version_is_still_built_and_still_reachable(self, repo):
        self.release(repo, "thing", "2026.06.02.1", body="Old.\n")
        self.release(repo, "thing", "2026.09.15.1", body="New.\n")
        b.build()
        older = self.out(repo, "thing", "v2026.06.02.1.html")
        assert older.is_file()
        assert "Old." in older.read_text()

    def test_an_older_version_says_so_and_points_at_the_newer_one(self, repo):
        self.release(repo, "thing", "2026.06.02.1", body="Old.\n")
        self.release(repo, "thing", "2026.09.15.1", body="New.\n")
        b.build()
        page = self.out(repo, "thing", "v2026.06.02.1.html").read_text()
        assert "2 June 2026 version" in page
        assert "15 September 2026" in page
        assert "../thing.html" in page

    def test_dates_sort_by_date_and_not_as_text(self, repo):
        """2026.09.02.1 comes before 2026.09.15.1. Compared as strings it would
        come after, because "2" sorts after "1"."""
        self.release(repo, "thing", "2026.09.02.1", body="Earlier.\n")
        self.release(repo, "thing", "2026.09.15.1", body="Later.\n")
        b.build()
        assert "Later." in self.out(repo, "thing.html").read_text()

    def test_two_releases_on_one_day_are_told_apart_by_the_last_number(self, repo):
        self.release(repo, "thing", "2026.09.15.1", body="Morning.\n")
        self.release(repo, "thing", "2026.09.15.2", body="Afternoon.\n")
        b.build()
        assert "Afternoon." in self.out(repo, "thing.html").read_text()

    def test_a_draft_is_not_built_at_all(self, repo):
        """The site is static and public: anything built has a URL, and a URL is
        public. So the only honest draft is one with no page."""
        write(repo, "Prose.\n")
        self.release(repo, "thing", "2026.09.15.1", status="draft", body="Secret.\n")
        b.build()
        assert not self.out(repo, "thing.html").exists()
        assert not self.out(repo, "thing").exists()

    def test_a_beta_is_built_but_is_never_the_default(self, repo):
        """Freeze the live release, mark the working copy beta, and students
        keep getting the live one until the beta is promoted."""
        self.release(repo, "thing", "2026.06.02.1", body="Live.\n")
        self.release(repo, "thing", "2026.09.15.1", status="beta", body="Trying.\n")
        b.build()
        assert "Live." in self.out(repo, "thing.html").read_text()
        beta = self.out(repo, "thing", "v2026.09.15.1.html")
        assert "Trying." in beta.read_text()
        assert "not the tutorial your course uses" in beta.read_text()

    def test_a_beta_is_not_in_the_reading_order(self, repo):
        self.release(repo, "thing", "2026.06.02.1", body="Live.\n")
        self.release(repo, "thing", "2026.09.15.1", status="beta", body="Trying.\n")
        write(repo, "Another.\n", slug="other")
        set_order(repo, "computational-methods", "python-fundamentals",
                  ["thing", "other"])
        b.build()
        page = self.out(repo, "thing.html").read_text()
        # The route, rather than the whole page: the beta *is* in the version
        # list, tagged as a draft, which is the point of having a list. What it
        # must never be is the next thing a reader is walked into.
        route = "".join(re.findall(r"<nav class=\"dl-nav.*?</nav>", page, re.DOTALL))
        assert "other.html" in route          # next, in the series
        assert "v2026.09.15.1" not in route   # the beta is nowhere in the route
        assert "v2026.09.15.1" not in re.sub(
            r'<script type="application/json".*?</script>', "", page, flags=re.DOTALL)

    def test_only_the_default_teaches_an_outcome(self, repo):
        """A superseded release claims the same coverage as the one that
        replaced it. Counting both would make one outcome look taught twice."""
        covers = "covers:\n  a-section:\n    covers: [MIT-1.4]\n"
        for version in ("2026.06.02.1", "2026.09.15.1"):
            path = self.release(repo, "thing", version, body="## A section\n\nProse.\n")
            path.write_text(path.read_text().replace(
                f"status: live\n", f"status: live\n{covers}"))
        b.build()
        data = json.loads(re.search(
            r'<script type="application/json" id="dewlab-tree">(.*?)</script>',
            (repo / "site" / "tree.html").read_text(), re.DOTALL).group(1))
        node = next(n for n in data["nodes"] if n["code"] == "MIT-1.4")
        assert node["state"] == "taught"
        assert "/thing.html#" in node["where"]["href"]

    def test_an_older_release_points_search_at_the_current_one(self, repo):
        """Two releases of one tutorial are near-identical pages. Without a
        canonical link they compete with each other in search results, and the
        one that wins is whichever the crawler happened to like."""
        self.release(repo, "thing", "2026.06.02.1")
        self.release(repo, "thing", "2026.09.15.1")
        b.build()
        older = self.out(repo, "thing", "v2026.06.02.1.html").read_text()
        assert '<link rel="canonical" href="../thing.html">' in older

    def test_the_current_one_does_not_point_at_itself(self, repo):
        self.release(repo, "thing", "2026.06.02.1")
        self.release(repo, "thing", "2026.09.15.1")
        b.build()
        assert "canonical" not in self.out(repo, "thing.html").read_text()

    def test_a_version_that_is_not_a_release_date_stops_the_build(self, repo):
        path = write(repo, "Prose.\n")
        path.write_text(path.read_text().replace(
            "version: 2026.08.23.1", "version: 3"))
        with pytest.raises(b.BuildError, match="release date"):
            b.build()


class TestTheVersionListInTheManifest:
    """What the page needs to offer a reader another release, and to say what
    moving there will do to their work before they do it.

    Saved answers are matched back on cell id, so which of them survive a move
    is knowable rather than a matter of hope — but only if the page knows which
    cells each release has. `planning/VERSIONS.md`."""

    release = TestVersionsOfATutorial.release
    out = TestVersionsOfATutorial.out

    CELLS = (
        "## A section\n\n```python exec\nid: one\nprint(1)\n```\n\n"
        "```python exec\nid: two\nprint(2)\n```\n"
    )

    def test_one_release_carries_no_list(self, repo):
        """A picker with a single entry is furniture, and every tutorial would
        pay for it in bytes and in clutter."""
        write(repo, "Prose.\n")
        b.build()
        assert "versions" not in manifest(built(repo))

    def test_every_release_is_listed_newest_first(self, repo):
        self.release(repo, "thing", "2026.06.02.1")
        self.release(repo, "thing", "2026.09.15.1")
        b.build()
        listed = manifest(self.out(repo, "thing.html").read_text())["versions"]
        assert [v["version"] for v in listed] == ["2026.09.15.1", "2026.06.02.1"]

    def test_each_entry_carries_the_date_a_reader_would_read(self, repo):
        """"15 September 2026", not "2026.09.15.1" and not "version 2". The
        dotted form is for the file and the URL; a person gets a date."""
        self.release(repo, "thing", "2026.06.02.1")
        self.release(repo, "thing", "2026.09.15.1")
        b.build()
        listed = manifest(self.out(repo, "thing.html").read_text())["versions"]
        assert [v["date"] for v in listed] == ["15 September 2026", "2 June 2026"]

    def test_the_default_is_marked_and_the_others_are_not(self, repo):
        self.release(repo, "thing", "2026.06.02.1")
        self.release(repo, "thing", "2026.09.15.1")
        b.build()
        listed = manifest(self.out(repo, "thing.html").read_text())["versions"]
        assert [v["isDefault"] for v in listed] == [True, False]

    def test_a_beta_is_listed_as_a_beta(self, repo):
        """It is reachable, so it belongs in the list. It is not the course, so
        the list has to say which one it is."""
        self.release(repo, "thing", "2026.06.02.1")
        self.release(repo, "thing", "2026.09.15.1", status="beta")
        b.build()
        listed = manifest(self.out(repo, "thing.html").read_text())["versions"]
        assert {v["version"]: v["status"] for v in listed} == {
            "2026.06.02.1": "live", "2026.09.15.1": "beta",
        }

    def test_each_url_is_relative_to_the_page_that_carries_it(self, repo):
        """The default sits one folder up from its own older releases, so the
        same list is written twice with different paths in it."""
        self.release(repo, "thing", "2026.06.02.1")
        self.release(repo, "thing", "2026.09.15.1")
        b.build()

        from_default = manifest(self.out(repo, "thing.html").read_text())["versions"]
        assert {v["version"]: v["url"] for v in from_default} == {
            "2026.09.15.1": "thing.html",
            "2026.06.02.1": "thing/v2026.06.02.1.html",
        }

        older = self.out(repo, "thing", "v2026.06.02.1.html").read_text()
        from_older = manifest(older)["versions"]
        assert {v["version"]: v["url"] for v in from_older} == {
            "2026.09.15.1": "../thing.html",
            "2026.06.02.1": "v2026.06.02.1.html",
        }

    def test_each_entry_carries_that_release_s_cell_ids(self, repo):
        """The whole point of the list. Without these the page can only warn a
        reader that their work "may not line up"; with them it can count."""
        self.release(repo, "thing", "2026.06.02.1", body=self.CELLS)
        self.release(repo, "thing", "2026.09.15.1",
                     body=self.CELLS.replace("id: two", "id: three"))
        b.build()
        listed = manifest(self.out(repo, "thing.html").read_text())["versions"]
        assert {v["version"]: v["cells"] for v in listed} == {
            "2026.09.15.1": ["one", "three"],
            "2026.06.02.1": ["one", "two"],
        }


class TestTheManifestIdentifiesThePage:
    def test_it_carries_the_module_as_well_as_the_slug(self, repo):
        """Saved work is keyed on the pair. A slug is only unique within its
        module — both modules have a `first-steps` — so the slug alone put both
        tutorials' answers in one record, each overwriting the other."""
        write(repo, "Prose.\n")
        b.build()
        page = (repo / "site" / "tutorials" / "computational-methods"
                / "sample.html").read_text()
        assert manifest(page)["module"] == "computational-methods"
        assert manifest(page)["slug"] == "sample"


class TestArchivedTutorials:
    """Retiring a tutorial without deleting it.

    Deleting the file was the only way to retire one, and deleting it strands
    every student who saved work in it — the work sits in local storage keyed to
    a page that no longer exists. Archiving keeps the page."""

    def archive(self, repo, slug: str = "sample") -> Path:
        """Mark a tutorial archived and take it out of the reading order."""
        path = repo / "tutorials" / "computational-methods" / f"{slug}.md"
        path.write_text(path.read_text().replace(
            "version: 2026.08.23.1\n", "version: 2026.08.23.1\nstatus: archived\n"))
        remaining = sorted(
            p.stem for p in path.parent.glob("*.md")
            if "status: archived" not in p.read_text()
        )
        set_order(repo, "computational-methods", "python-fundamentals", remaining)
        return path

    def test_an_archived_tutorial_is_still_built(self, repo):
        write(repo, "Prose.\n")
        write(repo, "More prose.\n", slug="second")
        self.archive(repo)
        b.build()
        page = repo / "site" / "tutorials" / "computational-methods" / "sample.html"
        assert page.is_file()

    def test_it_says_it_is_no_longer_part_of_the_course(self, repo):
        write(repo, "# Sample\n\nThe body of it.\n")
        write(repo, "More prose.\n", slug="second")
        self.archive(repo)
        b.build()
        page = (repo / "site" / "tutorials" / "computational-methods"
                / "sample.html").read_text()
        assert "no longer part of the course" in page
        # And the notice comes before the tutorial, not after it.
        assert page.index("dl-archived") < page.index("The body of it.")

    def test_it_is_not_in_the_reading_order(self, repo):
        """No previous, no next: there is nowhere in the series it sits."""
        write(repo, "Prose.\n")
        write(repo, "More prose.\n", slug="second")
        self.archive(repo)
        b.build()
        page = (repo / "site" / "tutorials" / "computational-methods"
                / "sample.html").read_text()
        assert "dl-nav-prev" not in page
        assert "dl-nav-next" not in page
        assert "dl-nav-up" in page

    def test_the_live_tutorials_close_up_behind_it(self, repo):
        """The tutorial after an archived one moves up rather than leaving a
        gap, because the order file no longer lists the archived one."""
        for slug in ("one", "two", "three"):
            write(repo, "Prose.\n", slug=slug)
        self.archive(repo, "two")
        b.build()
        page = (repo / "site" / "tutorials" / "computational-methods"
                / "one.html").read_text()
        assert "three.html" in page
        assert "two.html" not in page

    def test_the_contents_page_lists_it_under_an_archive_heading(self, repo):
        write(repo, "Prose.\n")
        write(repo, "More prose.\n", slug="second")
        self.archive(repo)
        b.build()
        index = (repo / "site" / "index.html").read_text()
        assert "Archive" in index
        assert 'href="tutorials/computational-methods/sample.html"' in index
        # Below the live series, not among it.
        assert index.index("second.html") < index.index("sample.html")

    def test_listing_an_archived_tutorial_in_the_order_file_is_an_error(self, repo):
        """The contradictory case. Silently ignoring the line would leave the
        order file saying one thing and the site doing another."""
        write(repo, "Prose.\n")
        write(repo, "More prose.\n", slug="second")
        path = repo / "tutorials" / "computational-methods" / "sample.md"
        path.write_text(path.read_text().replace(
            "version: 2026.08.23.1\n", "version: 2026.08.23.1\nstatus: archived\n"))
        # `write` re-listed everything, including the one just archived.
        with pytest.raises(b.BuildError, match="archived"):
            b.build()

    def test_an_unknown_status_stops_the_build(self, repo):
        path = write(repo, "Prose.\n")
        path.write_text(path.read_text().replace(
            "version: 2026.08.23.1\n", "version: 2026.08.23.1\nstatus: retired\n"))
        with pytest.raises(b.BuildError, match="status"):
            b.build()

    def test_it_teaches_nothing_the_map_can_point_at(self, repo):
        """It taught what it taught, but a student picking a topic today cannot
        be sent there. Counting it would make the map claim an outcome is
        covered when nothing on the course covers it."""
        path = write(repo, "## A section\n\nProse.\n")
        path.write_text(path.read_text().replace(
            "version: 2026.08.23.1\n", "version: 2026.08.23.1\ncovers:\n  a-section:\n    covers: [MIT-1.4]\n"))
        write(repo, "More prose.\n", slug="second")
        b.build()
        taught = json.loads(re.search(
            r'<script type="application/json" id="dewlab-tree">(.*?)</script>',
            (repo / "site" / "tree.html").read_text(), re.DOTALL).group(1))
        assert next(n for n in taught["nodes"] if n["code"] == "MIT-1.4")["state"] == "taught"

        self.archive(repo)
        b.build()
        taught = json.loads(re.search(
            r'<script type="application/json" id="dewlab-tree">(.*?)</script>',
            (repo / "site" / "tree.html").read_text(), re.DOTALL).group(1))
        assert next(n for n in taught["nodes"] if n["code"] == "MIT-1.4")["state"] != "taught"


class TestTheTopicTree:
    """The tree page: every topic in both descriptors, positioned by what has
    to come first, with what each one is and where it is used."""

    def tree(self, repo) -> str:
        page = repo / "site" / "tree.html"
        return page.read_text() if page.is_file() else ""

    def data(self, repo) -> dict:
        match = re.search(
            r'<script type="application/json" id="dewlab-tree">(.*?)</script>',
            self.tree(repo), re.DOTALL,
        )
        return json.loads(match.group(1)) if match else {}

    def test_the_page_is_built(self, repo):
        write(repo, "Some prose.\n")
        b.build()
        assert "The topic tree" in self.tree(repo)

    def test_every_topic_in_the_glossary_becomes_a_node(self, repo):
        write(repo, "Some prose.\n")
        b.build()
        topics = yaml.safe_load(
            (Path(__file__).resolve().parent.parent
             / "planning" / "curriculum" / "topics.yaml").read_text()
        )["topics"]
        assert len(self.data(repo)["nodes"]) == len(topics)

    def test_a_topic_carries_what_it_is_and_where_it_is_used(self, repo):
        write(repo, "Some prose.\n")
        b.build()
        node = next(n for n in self.data(repo)["nodes"] if n["code"] == "MIT-1.4")
        assert "two digits" in node["plain"]
        assert node["uses"]
        assert node["strand"] == "number"

    def test_nothing_needs_something_below_it(self, repo):
        """The whole layout rests on this: top to bottom is dependency, so an
        arrow that pointed upwards would be a lie about the tree."""
        write(repo, "Some prose.\n")
        b.build()
        data = self.data(repo)
        tier = {n["code"]: n["tier"] for n in data["nodes"]}
        for node in data["nodes"]:
            for need in node["needs"]:
                assert tier[need] < node["tier"], f"{node['code']} needs {need}"

    def test_the_tree_is_drawn_vertically(self, repo):
        """Tier is an abstraction; y is what a student actually sees. The two
        agreeing is the difference between a vertical tree and a horizontal one
        with vertical labels."""
        write(repo, "Some prose.\n")
        b.build()
        data = self.data(repo)
        place = {n["code"]: n for n in data["nodes"]}
        for node in data["nodes"]:
            for need in node["needs"]:
                assert place[need]["y"] < node["y"], f"{node['code']} needs {need}"

    def test_each_tier_is_a_row_of_its_own(self, repo):
        """A tier is a stripe across the tree, and the stripes stack without
        overlapping. Two tiers sharing vertical space would say two different
        depths are the same depth."""
        write(repo, "Some prose.\n")
        b.build()
        bands = self.data(repo)["bands"]
        assert [band["tier"] for band in bands] == sorted(band["tier"] for band in bands)
        for earlier, later in zip(bands, bands[1:]):
            assert earlier["y"] + earlier["height"] <= later["y"]

    def test_the_tree_is_taller_than_it_is_wide(self, repo):
        """The reason for the vertical layout in the first place. Giving each
        subject its own column produced 5854px wide against 756px tall — a
        horizontal tree in disguise, and unusable on a phone."""
        write(repo, "Some prose.\n")
        b.build()
        data = self.data(repo)
        assert data["height"] > data["width"]

    def test_the_top_row_says_you_can_start_there(self, repo):
        """The stripe labels are the only place the map explains itself."""
        write(repo, "Some prose.\n")
        b.build()
        bands = {band["tier"]: band["label"] for band in self.data(repo)["bands"]}
        assert bands[0] == "start anywhere here"
        assert bands[1] == "one layer down"
        assert bands[2] == "two layers down"

    def test_a_taught_topic_links_to_the_section_that_teaches_it(self, repo):
        """The link comes from the tutorial's own `covers:`, so it cannot point
        somewhere the tutorial does not claim."""
        path = write(repo, "## A section\n\nProse.\n")
        path.write_text(path.read_text().replace(
            "version: 2026.08.23.1\n", "version: 2026.08.23.1\ncovers:\n  a-section:\n    covers: [MIT-1.4]\n"
        ))
        b.build()
        node = next(n for n in self.data(repo)["nodes"] if n["code"] == "MIT-1.4")
        assert node["state"] == "taught"
        assert node["where"]["href"] == (
            "tutorials/computational-methods/sample.html#a-section"
        )

    def test_a_topic_no_tutorial_claims_is_not_marked_taught(self, repo):
        write(repo, "Some prose.\n")
        b.build()
        assert all(n["state"] != "taught" for n in self.data(repo)["nodes"])

    def test_a_topic_nobody_teaches_is_marked_planned(self, repo):
        write(repo, "Some prose.\n")
        b.build()
        states = {n["code"]: n["state"] for n in self.data(repo)["nodes"]}
        assert states["MIT-3.6"] == "planned"

    def test_groundwork_is_not_reported_as_a_missing_tutorial(self, repo):
        """A `PRE-` topic is nobody's learning outcome, so no tutorial can claim
        it in `covers:`. Left alone it would sit on the map forever marked
        "planned", which reads as a gap in the course rather than as something
        picked up in passing."""
        write(repo, "Some prose.\n")
        b.build()
        node = next(n for n in self.data(repo)["nodes"] if n["code"] == "PRE-1")
        assert node["state"] == "groundwork"

    def test_a_topic_may_name_its_own_strand(self, repo):
        """Strands come from outcomes.yaml, so a topic that is deliberately not
        an outcome has none — and lands in "other", which is not a subject."""
        write(repo, "Some prose.\n")
        b.build()
        node = next(n for n in self.data(repo)["nodes"] if n["code"] == "PRE-1")
        assert node["strand"] == "geometry"

    def test_the_colour_key_lists_every_strand_on_the_tree_and_no_others(self, repo):
        """The colours are on every node and were explained nowhere except the
        panel you only see after choosing something."""
        write(repo, "Some prose.\n")
        b.build()
        page = self.tree(repo)
        listed = set(re.findall(r'<span class="dl-tree-hue" data-strand="([^"]+)"', page))
        assert listed == {n["strand"] for n in self.data(repo)["nodes"]}
        assert "What the colours mean" in page

    def test_a_topic_we_ruled_out_says_so(self, repo):
        """Read from the file rather than named here. This test used to assert
        on MIT-2.3 by name and broke the day Venn diagrams came back into
        scope — which is a decision changing, not the tree breaking."""
        write(repo, "Some prose.\n")
        b.build()
        scope = yaml.safe_load(
            (DEWLAB / "planning" / "curriculum" / "out-of-scope.yaml").read_text()
        )
        ruled_out = [entry["code"] for entry in scope["outcomes"] or []]
        if not ruled_out:
            pytest.skip("nothing is ruled out at the moment, so there is nothing "
                        "for the tree to say so about")
        states = {n["code"]: n["state"] for n in self.data(repo)["nodes"]}
        for code in ruled_out:
            assert states[code] == "excluded", f"{code} is out of scope and the tree does not say so"

    def test_the_tutorial_map_moved_here_from_the_contents_page(self, repo):
        for n in (1, 2, 3):
            (repo / "tutorials" / "computational-methods" / f"t{n}.md").write_text(
                f'---\ntitle: "T{n}"\nslug: t{n}\nmodule: computational-methods\n'
                f'year: "2026-2027"\nseries: python-fundamentals\n'
                f"version: 2026.08.23.1\n---\n\n# T{n}\n\nProse.\n"
            )
        set_order(repo, "computational-methods", "python-fundamentals",
                  ["t1", "t2", "t3"])
        b.build()
        assert "dl-map-node" not in (repo / "site" / "index.html").read_text()
        assert "How the tutorials relate" in self.tree(repo)
        assert self.tree(repo).count('class="dl-map-node"') == 3

    def test_the_contents_page_introduces_the_place_instead(self, repo):
        write(repo, "Some prose.\n")
        b.build()
        index = (repo / "site" / "index.html").read_text()
        assert "runs in this browser" in index
        assert 'href="tree.html"' in index


class TestDownloadsDoNotCollide:
    """Slugs are unique within a module, not across the site — so a flat
    download folder would let two modules' `first-steps` overwrite each other.
    Silently, because the loser simply never appears.

    The publish workflow's guard caught this on main once. This catches it
    before that.
    """

    def two_modules(self, repo):
        write(repo, "One.\n", slug="first-steps")
        other = repo / "tutorials" / "other-module" / "first-steps.md"
        other.parent.mkdir(parents=True)
        other.write_text(
            '---\ntitle: "First Steps"\nslug: first-steps\nmodule: other-module\n'
            'year: "2026-2027"\nseries: intro\nversion: 2026.08.23.1\n---\n\nProse.\n'
        )
        set_order(repo, "other-module", "intro", ["first-steps"])

    def test_every_page_has_its_own_downloadable_copy(self, repo_with_assets):
        self.two_modules(repo_with_assets)
        b.build(standalone=True)
        pages = list((repo_with_assets / "site" / "tutorials").rglob("*.html"))
        copies = list((repo_with_assets / "site" / "download").rglob("*.html"))
        assert len(copies) == len(pages) == 2

    def test_a_copy_sits_under_the_module_its_page_does(self, repo_with_assets):
        self.two_modules(repo_with_assets)
        b.build(standalone=True)
        for module in ("computational-methods", "other-module"):
            assert (repo_with_assets / "site" / "download" / module
                    / "first-steps.html").is_file()

    def test_the_link_points_at_the_right_one(self, repo_with_assets):
        self.two_modules(repo_with_assets)
        b.build(standalone=True)
        page = (repo_with_assets / "site" / "tutorials" / "other-module"
                / "first-steps.html").read_text()
        assert 'href="../../download/other-module/first-steps.html"' in page

    def test_the_archive_gathers_the_right_module(self, repo_with_assets):
        self.two_modules(repo_with_assets)
        b.build(standalone=True)
        archive = (repo_with_assets / "site" / "download"
                   / "other-module-intro.zip")
        with zipfile.ZipFile(archive) as opened:
            assert opened.namelist() == ["other-module-intro/first-steps.html"]


class TestPagesOfProblems:
    """A practice page belongs to a tutorial, or draws on several.

    Both shapes are the same mechanically — built, reachable, off the reading
    order, no coverage of their own. What differs is what they point at, and
    whether anything points back."""

    def practice(self, repo, slug: str, **frontmatter) -> Path:
        """Write a page of problems, and keep it out of the order file."""
        path = repo / "tutorials" / "computational-methods" / f"{slug}.md"
        extra = "".join(
            f"{key}: {value}\n" if not isinstance(value, list)
            else f"{key}:\n" + "".join(f"  - {v}\n" for v in value)
            for key, value in frontmatter.items()
        )
        path.write_text(
            FRONTMATTER.format(slug=slug, version="2026.08.23.1").replace(
                "version: 2026.08.23.1\n", f"version: 2026.08.23.1\n{extra}")
            + "**1.** A question.\n"
        )
        listed = sorted(
            p.stem for p in path.parent.glob("*.md")
            if "practice_for" not in p.read_text()
            and "practice_across" not in p.read_text()
        )
        set_order(repo, "computational-methods", "python-fundamentals", listed)
        return path

    def test_a_page_of_problems_is_off_the_reading_order(self, repo):
        write(repo, "One.\n", slug="one")
        write(repo, "Two.\n", slug="two")
        self.practice(repo, "one-practice", practice_for="one")
        b.build()
        page = built(repo, "one")
        assert "two.html" in page          # next is the next tutorial
        assert "dl-nav-next" in page
        assert "one-practice.html" in page  # linked, but not as next

    def test_the_tutorial_links_to_its_problems_and_back(self, repo):
        write(repo, "One.\n", slug="one")
        self.practice(repo, "one-practice", practice_for="one")
        b.build()
        assert "dl-practice-link" in built(repo, "one")
        assert "dl-practice-back" in built(repo, "one-practice")

    def test_two_pages_cannot_claim_the_same_tutorial(self, repo):
        write(repo, "One.\n", slug="one")
        self.practice(repo, "one-practice", practice_for="one")
        self.practice(repo, "more-practice", practice_for="one")
        with pytest.raises(b.BuildError, match="has one page of problems"):
            b.build()

    def test_a_page_of_problems_declaring_coverage_is_an_error(self, repo):
        write(repo, "One.\n", slug="one")
        path = self.practice(repo, "one-practice", practice_for="one")
        path.write_text(path.read_text().replace(
            "practice_for: one\n",
            "practice_for: one\ncovers:\n  a-question:\n    covers: [MIT-1.1]\n"))
        with pytest.raises(b.BuildError, match="declares `covers:`"):
            b.build()

    def test_a_mixed_set_draws_on_several_tutorials(self, repo):
        write(repo, "One.\n", slug="one")
        write(repo, "Two.\n", slug="two")
        self.practice(repo, "mixed", practice_across=["one", "two"])
        page = (repo / "site" / "tutorials" / "computational-methods"
                / "mixed.html")
        b.build()
        text = page.read_text()
        assert "dl-practice-back" in text
        assert "one.html" in text and "two.html" in text

    def test_a_mixed_set_is_off_the_reading_order(self, repo):
        """Two tutorials, and the mixed set is not between them.

        Asserted on the navigation rather than on the whole page: the tutorial
        does link to a mixed set that names it, from the practice box at the
        end. What it must not do is offer one as the next thing to read."""
        write(repo, "One.\n", slug="one")
        write(repo, "Two.\n", slug="two")
        self.practice(repo, "mixed", practice_across=["one", "two"])
        b.build()
        page = built(repo, "one")
        nav = re.findall(r"<nav class=\"dl-nav[^\"]*\">.*?</nav>", page, re.S)
        assert nav, "the tutorial has no navigation at all"
        assert any("two.html" in bar for bar in nav)
        assert not any("mixed.html" in bar for bar in nav)

    def test_a_mixed_set_is_not_offered_as_this_tutorial_own_practice(self, repo):
        """The two links are distinguishable.

        Tutorials did not link back to mixed sets at all until Josh asked for
        them to (DECISIONS_LOG 7.51). What still has to hold is that a reader
        can tell the difference: one page is answerable from this tutorial and
        the other is not."""
        write(repo, "One.\n", slug="one")
        write(repo, "Two.\n", slug="two")
        self.practice(repo, "mixed", practice_across=["one", "two"])
        b.build()
        page = built(repo, "one")
        assert "dl-practice-mixed" in page
        assert "Practice problems for this tutorial" not in page
        assert "once more of the course is behind you" in page

    def test_the_contents_page_lists_mixed_sets(self, repo):
        write(repo, "One.\n", slug="one")
        write(repo, "Two.\n", slug="two")
        self.practice(repo, "mixed", practice_across=["one", "two"])
        b.build()
        index = (repo / "site" / "index.html").read_text()
        assert "Mixed problems" in index
        assert "dl-mixed" in index
        assert "mixed.html" in index

    def test_a_mixed_set_naming_one_tutorial_is_an_error(self, repo):
        write(repo, "One.\n", slug="one")
        self.practice(repo, "mixed", practice_across=["one"])
        with pytest.raises(b.BuildError, match="practice_for is for"):
            b.build()

    def test_a_mixed_set_naming_a_slug_that_does_not_exist_is_an_error(self, repo):
        write(repo, "One.\n", slug="one")
        self.practice(repo, "mixed", practice_across=["one", "nowhere"])
        with pytest.raises(b.BuildError, match="no tutorial in"):
            b.build()

    def test_a_mixed_set_naming_a_page_of_problems_is_an_error(self, repo):
        write(repo, "One.\n", slug="one")
        write(repo, "Two.\n", slug="two")
        self.practice(repo, "one-practice", practice_for="one")
        self.practice(repo, "mixed", practice_across=["two", "one-practice"])
        with pytest.raises(b.BuildError, match="itself a page of problems"):
            b.build()

    def test_a_mixed_set_naming_itself_is_an_error(self, repo):
        write(repo, "One.\n", slug="one")
        self.practice(repo, "mixed", practice_across=["one", "mixed"])
        with pytest.raises(b.BuildError, match="which is itself"):
            b.build()

    def test_a_repeated_slug_is_an_error(self, repo):
        write(repo, "One.\n", slug="one")
        write(repo, "Two.\n", slug="two")
        self.practice(repo, "mixed", practice_across=["one", "two", "one"])
        with pytest.raises(b.BuildError, match="more than once"):
            b.build()

    def test_a_page_cannot_be_both_kinds_at_once(self, repo):
        write(repo, "One.\n", slug="one")
        write(repo, "Two.\n", slug="two")
        self.practice(repo, "mixed", practice_for="one",
                      practice_across=["one", "two"])
        with pytest.raises(b.BuildError, match="cannot do both"):
            b.build()


class TestFolds:
    """A `<details>` in a tutorial has to name a fold this project styles.

    Writing a bare `<details><summary>` is what a plain HTML document looks
    like, and an earlier draft of the style guide showed exactly that. Without
    the class it renders as a browser-default triangle sitting in the prose."""

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


class TestPracticeIsReachable:
    """A tutorial links to every page of problems that names it.

    Its own practice page first, then any mixed set that draws on it — described
    as being for later, since a mixed set assumes tutorials this reader may not
    have met yet."""

    def practice(self, repo, slug: str, **frontmatter) -> Path:
        return TestPagesOfProblems().practice(repo, slug, **frontmatter)

    def test_a_tutorial_links_to_a_mixed_set_that_names_it(self, repo):
        write(repo, "One.\n", slug="one")
        write(repo, "Two.\n", slug="two")
        self.practice(repo, "mixed", practice_across=["one", "two"])
        b.build()
        page = built(repo, "one")
        assert "dl-practice-mixed" in page
        assert "mixed.html" in page

    def test_it_names_the_other_tutorials_the_set_draws_on(self, repo):
        """So a reader can tell whether it is for them yet."""
        write(repo, "One.\n", slug="one")
        write(repo, "Two.\n", slug="two")
        self.practice(repo, "mixed", practice_across=["one", "two"])
        b.build()
        page = built(repo, "one")
        assert "It also draws on A Title" in page

    def test_a_tutorial_no_mixed_set_names_gets_no_such_link(self, repo):
        write(repo, "One.\n", slug="one")
        write(repo, "Two.\n", slug="two")
        write(repo, "Three.\n", slug="three")
        self.practice(repo, "mixed", practice_across=["one", "two"])
        b.build()
        assert "dl-practice-mixed" not in built(repo, "three")

    def test_both_kinds_of_link_appear_together(self, repo):
        write(repo, "One.\n", slug="one")
        write(repo, "Two.\n", slug="two")
        self.practice(repo, "one-practice", practice_for="one")
        self.practice(repo, "mixed", practice_across=["one", "two"])
        b.build()
        page = built(repo, "one")
        assert "one-practice.html" in page and "mixed.html" in page
        # Its own practice page comes first: it is the one for now.
        assert page.index("one-practice.html") < page.index("mixed.html")


class TestTwoReleasesOnOneDay:
    """The picker shows a date. Two releases on one day show the same date.

    Found by releasing four tutorials on the afternoon they were first written:
    a reader choosing between them saw two identical options."""

    def release(self, repo, slug: str, version: str, status: str = "live") -> Path:
        folder = repo / "tutorials" / "computational-methods" / slug
        folder.mkdir(parents=True, exist_ok=True)
        name = f"{slug}.md" if status == "live" and version.endswith(".9") else f"v{version}.md"
        path = folder / name
        path.write_text(
            FRONTMATTER.format(slug=slug, version=version).replace(
                f"version: {version}\n", f"version: {version}\nstatus: {status}\n")
            + "Prose.\n"
        )
        set_order(repo, "computational-methods", "python-fundamentals", [slug])
        return path

    def versions(self, repo, slug: str) -> list[dict]:
        page = (repo / "site" / "tutorials" / "computational-methods"
                / f"{slug}.html").read_text()
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
        """Three releases, two of them on one day."""
        self.release(repo, "sample", "2026.08.23.1")
        self.release(repo, "sample", "2026.08.23.2")
        self.release(repo, "sample", "2026.09.15.1")
        b.build()
        shown = [v["date"] for v in self.versions(repo, "sample")]
        assert shown == ["15 September 2026", "23 August 2026 (2)", "23 August 2026 (1)"]
