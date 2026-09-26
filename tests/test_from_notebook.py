"""Every notebook here is built in the test itself: the real teaching
notebooks live in another repository, so a test needing them would stop
running the moment this one is cloned on its own."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "dev"))

import from_notebook as fn  # noqa: E402


def notebook(*cells: tuple[str, str]) -> dict:
    # Keep trailing newlines on source lines (nbformat's own shape) — drop
    # them and the fixture parses into one run-on line, a fixture bug that
    # reads like a converter bug.
    return {
        "cells": [
            {
                "cell_type": kind,
                "source": source.splitlines(keepends=True),
                "outputs": [],
                "metadata": {},
            }
            for kind, source in cells
        ],
        "metadata": {},
        "nbformat": 4,
        "nbformat_minor": 5,
    }


def write(tmp_path: Path, name: str, data: dict) -> Path:
    path = tmp_path / name
    path.write_text(json.dumps(data))
    return path


def convert(path: Path, **kwargs):
    options = {"year": "2026-2027"}
    options.update(kwargs)
    return fn.convert(path, **options)


class TestFrontmatter:
    @pytest.mark.parametrize(
        "filename, cell_source, expected_title, title_in_frontmatter",
        [
            pytest.param(
                "Tutorial_01_First_Steps.ipynb",
                "# Tutorial 1: First Steps\n\nProse.",
                "Tutorial 1: First Steps",
                True,
                id="title_from_first_heading",
            ),
            pytest.param(
                "Loose_Notes.ipynb",
                "No heading here.",
                "Loose Notes",
                False,
                id="filename_stands_in_for_missing_heading",
            ),
        ],
    )
    def test_the_title(self, tmp_path, filename, cell_source, expected_title, title_in_frontmatter):
        path = write(tmp_path, filename, notebook(("markdown", cell_source)))
        text, result = convert(path)
        assert result.title == expected_title
        if title_in_frontmatter:
            assert f'title: "{expected_title}"' in text

    def test_the_slug_comes_from_the_filename(self, tmp_path):
        path = write(tmp_path, "Tutorial_09_Counting_Carefully.ipynb",
                     notebook(("markdown", "# Counting")))
        _, result = convert(path)
        assert result.slug == "tutorial-09-counting-carefully"

    @pytest.mark.parametrize(
        "filename, cell_source, kwargs, expected_order",
        [
            pytest.param(
                "Tutorial_09_Counting.ipynb", "# C", {}, 9,
                id="order_from_number_in_filename",
            ),
            pytest.param(
                "Interlude.ipynb", "# I", {"default_order": 18}, 18,
                id="order_falls_back_without_a_number",
            ),
        ],
    )
    def test_order(self, tmp_path, filename, cell_source, kwargs, expected_order):
        path = write(tmp_path, filename, notebook(("markdown", cell_source)))
        _, result = convert(path, **kwargs)
        assert result.order == expected_order

    def test_the_supplied_fields_are_written_through(self, tmp_path):
        path = write(tmp_path, "T.ipynb", notebook(("markdown", "# T")))
        text, _ = convert(path, year="2027-2028")
        assert 'year: "2027-2028"' in text
        # Where the tutorial sits is not the file's to say.
        assert "module:" not in text and "series:" not in text and "slug:" not in text
        assert f"version: {fn.today_release()}" in text

    def test_a_quote_in_the_title_does_not_break_the_frontmatter(self, tmp_path):
        path = write(tmp_path, "T.ipynb", notebook(("markdown", '# The "Big" Idea')))
        text, _ = convert(path)
        title_line = next(l for l in text.split("\n") if l.startswith("title:"))
        assert title_line == 'title: "The \'Big\' Idea"'
        assert "# The \"Big\" Idea" in text


class TestCells:
    @pytest.mark.parametrize(
        "cells, expected_substrings, expected_count",
        [
            pytest.param(
                [("markdown", "# Adding"), ("code", "1 + 1")],
                ["```python exec\nid: adding-1\n1 + 1\n```"],
                1,
                id="base_exec_fence",
            ),
            pytest.param(
                [("markdown", "# Loops"), ("code", "a = 1"), ("code", "b = 2")],
                ["id: loops-1", "id: loops-2"],
                2,
                id="ids_numbered_within_a_section",
            ),
            pytest.param(
                [("markdown", "# Loops"), ("code", "a = 1"),
                 ("markdown", "## Lists"), ("code", "b = 2")],
                ["id: loops-1", "id: lists-1"],
                2,
                id="new_heading_starts_a_new_id_family",
            ),
        ],
    )
    def test_cell_ids(self, tmp_path, cells, expected_substrings, expected_count):
        path = write(tmp_path, "T.ipynb", notebook(*cells))
        text, result = convert(path)
        for substring in expected_substrings:
            assert substring in text
        assert result.cells == expected_count

    def test_markdown_is_carried_through_unchanged(self, tmp_path):
        prose = "Some *emphasis*, a $\\frac{1}{2}$, and a [link](https://example.org)."
        path = write(tmp_path, "T.ipynb", notebook(("markdown", prose)))
        text, _ = convert(path)
        assert prose in text

    def test_saved_outputs_are_dropped(self, tmp_path):
        data = notebook(("code", "1 + 1"))
        data["cells"][0]["outputs"] = [
            {"output_type": "execute_result", "data": {"text/plain": ["2"]}}
        ]
        path = write(tmp_path, "T.ipynb", data)
        text, _ = convert(path)
        assert "execute_result" not in text
        assert "text/plain" not in text

    def test_empty_cells_are_skipped(self, tmp_path):
        path = write(tmp_path, "T.ipynb",
                     notebook(("code", "   \n\n"), ("markdown", "# Real")))
        _, result = convert(path)
        assert result.cells == 0

    def test_a_raw_cell_is_skipped_and_noted(self, tmp_path):
        path = write(tmp_path, "T.ipynb", notebook(("raw", "\\newpage")))
        _, result = convert(path)
        assert any("raw cell" in note for note in result.notes)


class TestNotebookOnlyLines:
    @pytest.mark.parametrize(
        "heading, code, dropped, kept, note_substring",
        [
            pytest.param(
                "# Plots", "%matplotlib inline\nimport numpy",
                "%matplotlib", "import numpy", "%matplotlib inline",
                id="magics_are_dropped",
            ),
            pytest.param(
                "# Setup", "!pip install pandas\nimport pandas",
                "!pip install", "import pandas", None,
                id="shell_escapes_are_dropped",
            ),
            pytest.param(
                "# Maths", "remainder = 7 % 3",
                None, "remainder = 7 % 3", None,
                id="percent_inside_code_is_left_alone",
            ),
        ],
    )
    def test_magic_re_lines(self, tmp_path, heading, code, dropped, kept, note_substring):
        path = write(tmp_path, "T.ipynb", notebook(("markdown", heading), ("code", code)))
        text, result = convert(path)
        if dropped is not None:
            assert dropped not in text
        assert kept in text
        if note_substring is not None:
            assert any(note_substring in note for note in result.notes)

    def test_a_cell_of_nothing_but_magics_is_dropped_entirely(self, tmp_path):
        path = write(tmp_path, "T.ipynb", notebook(
            ("markdown", "# Setup"), ("code", "%matplotlib inline")))
        _, result = convert(path)
        assert result.cells == 0
        assert any("only magics" in note for note in result.notes)

    def test_an_embedded_attachment_is_flagged_rather_than_silently_broken(self, tmp_path):
        path = write(tmp_path, "T.ipynb",
                     notebook(("markdown", "![plot](attachment:plot.png)")))
        _, result = convert(path)
        assert any("attachment" in note for note in result.notes)


class TestRefusals:
    def test_a_fence_inside_a_code_cell_is_refused(self, tmp_path):
        path = write(tmp_path, "T.ipynb", notebook(
            ("markdown", "# X"), ("code", "print('''\n```\n''')")))
        with pytest.raises(fn.ConversionError, match="fence"):
            convert(path)

    def test_a_file_that_is_not_json_is_refused(self, tmp_path):
        path = tmp_path / "broken.ipynb"
        path.write_text("this is not json")
        with pytest.raises(fn.ConversionError, match="not valid notebook JSON"):
            convert(path)

    def test_a_json_file_that_is_not_a_notebook_is_refused(self, tmp_path):
        path = tmp_path / "other.ipynb"
        path.write_text(json.dumps({"hello": "world"}))
        with pytest.raises(fn.ConversionError, match="no cells"):
            convert(path)


class TestTheOutputActuallyBuilds:
    def test_a_converted_notebook_is_a_tutorial_build_py_accepts(self, tmp_path, monkeypatch):
        """The point of the whole script: what comes out has to build."""
        import build as b

        source = write(tmp_path, "Tutorial_03_Making_Decisions.ipynb", notebook(
            ("markdown", "# Making Decisions\n\nSome prose with $x^2$ in it."),
            ("code", "%matplotlib inline\nvalue = 4\nvalue > 3"),
            ("markdown", "## A second section"),
            ("code", "print('done')"),
        ))
        text, result = fn.convert(source, year="2026-2027")

        repo = tmp_path / "repo"
        (repo / "tutorials" / result.slug).mkdir(parents=True)
        (repo / "tutorials" / result.slug / f"{result.slug}.md").write_text(text)
        # Where a tutorial sits is a course file's business, so a converted
        # notebook has to be listed before the build will place it.
        (repo / "courses").mkdir()
        (repo / "courses" / "fixtures.yaml").write_text(
            f"title: Fixtures\ncontents:\n  - title: S\n    tutorials: [{result.slug}]\n"
        )
        (repo / "assets").mkdir()
        (repo / "assets" / "shell.html").write_text(
            (Path(__file__).resolve().parent.parent / "assets" / "shell.html").read_text()
        )
        for name, value in {
            "ROOT": repo, "TUTORIALS": repo / "tutorials", "COURSES": repo / "courses",
            "SETUP": repo / "setup",
            "DATA": repo / "data", "ASSETS": repo / "assets",
            "SHELL": repo / "assets" / "shell.html", "OUT": repo / "site",
        }.items():
            monkeypatch.setattr(b, name, value)

        written = b.build()
        # The tutorial, minus the pages (and the search index, not a page at
        # all) the build always writes alongside it.
        alongside = {"index.html", "features.html", "all-tutorials.html",
                     "all-notes.html", "tree.html", "about.html", "editor.html",
                     "studying.html", "reading-helpers.html",
                     "fixtures.html", "search-index.json", "routes.json",
                     "reference-index.json"}
        pages = [path for path in written if path.name not in alongside]
        assert len(pages) == 1, [path.name for path in pages]
        page = pages[0].read_text()
        assert "{{" not in page
        assert 'data-cell-id="making-decisions-1"' in page
        assert 'data-cell-id="a-second-section-1"' in page
        assert '<span class="dl-math">x^2</span>' in page


class TestTheReport:
    """`--out` may point outside the repo; `relative_to` alone crashed on such
    a path after the files were already written, the worst order to fail in."""

    @pytest.mark.parametrize("is_inside", [True, False], ids=["inside_the_repo", "outside_it"])
    def test_shown(self, tmp_path, is_inside):
        if is_inside:
            path = fn.ROOT / "tutorials" / "somewhere" / "a-tutorial.md"
            expected = "tutorials/somewhere/a-tutorial.md"
        else:
            path = tmp_path / "a-tutorial.md"
            expected = str(path)
        assert fn.shown(path) == expected
