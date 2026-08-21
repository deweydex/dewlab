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
        assert written == [repo / "site" / "tutorials" / "computational-methods" / "sample.html"]

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
