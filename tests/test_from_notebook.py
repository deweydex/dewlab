"""Unit tests for dev/from_notebook.py.

Every notebook here is built in the test itself. The converter has to be
testable without the real teaching notebooks — they live in another repository,
and a test that needs them is a test that stops running the moment someone
clones this one on its own.

    python3 -m pytest tests/test_from_notebook.py -q
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "dev"))

import from_notebook as fn  # noqa: E402


def notebook(*cells: tuple[str, str]) -> dict:
    """A notebook in the shape nbformat actually stores one.

    `source` is a list of lines that keep their trailing newlines — everything
    but possibly the last. Splitting them off instead produces a file that
    looks plausible and parses into one run-on line, which is a fixture bug
    that reads like a converter bug.
    """
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
    options = {"module": "a-module", "series": "a-series", "year": "2026-2027"}
    options.update(kwargs)
    return fn.convert(path, **options)


class TestFrontmatter:
    def test_the_title_comes_from_the_first_heading(self, tmp_path):
        path = write(tmp_path, "Tutorial_01_First_Steps.ipynb",
                     notebook(("markdown", "# Tutorial 1: First Steps\n\nProse.")))
        text, result = convert(path)
        assert result.title == "Tutorial 1: First Steps"
        assert 'title: "Tutorial 1: First Steps"' in text

    def test_the_filename_stands_in_when_there_is_no_heading(self, tmp_path):
        path = write(tmp_path, "Loose_Notes.ipynb", notebook(("markdown", "No heading here.")))
        _, result = convert(path)
        assert result.title == "Loose Notes"

    def test_the_slug_comes_from_the_filename(self, tmp_path):
        path = write(tmp_path, "Tutorial_09_Counting_Carefully.ipynb",
                     notebook(("markdown", "# Counting")))
        _, result = convert(path)
        assert result.slug == "tutorial-09-counting-carefully"

    def test_order_comes_from_the_number_in_the_filename(self, tmp_path):
        path = write(tmp_path, "Tutorial_09_Counting.ipynb", notebook(("markdown", "# C")))
        _, result = convert(path)
        assert result.order == 9

    def test_order_falls_back_when_the_filename_has_no_number(self, tmp_path):
        path = write(tmp_path, "Interlude.ipynb", notebook(("markdown", "# I")))
        _, result = convert(path, default_order=18)
        assert result.order == 18

    def test_the_supplied_fields_are_written_through(self, tmp_path):
        path = write(tmp_path, "T.ipynb", notebook(("markdown", "# T")))
        text, _ = convert(path, module="mit-pdp", series="maths", year="2027-2028")
        assert "module: mit-pdp" in text
        assert "series: maths" in text
        assert 'year: "2027-2028"' in text
        assert "version: 1" in text

    def test_a_quote_in_the_title_does_not_break_the_frontmatter(self, tmp_path):
        path = write(tmp_path, "T.ipynb", notebook(("markdown", '# The "Big" Idea')))
        text, _ = convert(path)
        title_line = next(l for l in text.split("\n") if l.startswith("title:"))
        assert title_line == 'title: "The \'Big\' Idea"'
        assert "# The \"Big\" Idea" in text  # the heading itself is untouched


class TestCells:
    def test_a_code_cell_becomes_an_exec_fence(self, tmp_path):
        path = write(tmp_path, "T.ipynb",
                     notebook(("markdown", "# Adding"), ("code", "1 + 1")))
        text, result = convert(path)
        assert "```python exec\nid: adding-1\n1 + 1\n```" in text
        assert result.cells == 1

    def test_ids_are_numbered_within_a_section(self, tmp_path):
        path = write(tmp_path, "T.ipynb", notebook(
            ("markdown", "# Loops"), ("code", "a = 1"), ("code", "b = 2")))
        text, _ = convert(path)
        assert "id: loops-1" in text and "id: loops-2" in text

    def test_a_new_heading_starts_a_new_id_family(self, tmp_path):
        path = write(tmp_path, "T.ipynb", notebook(
            ("markdown", "# Loops"), ("code", "a = 1"),
            ("markdown", "## Lists"), ("code", "b = 2")))
        text, _ = convert(path)
        assert "id: loops-1" in text and "id: lists-1" in text

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
    def test_magics_are_dropped(self, tmp_path):
        path = write(tmp_path, "T.ipynb", notebook(
            ("markdown", "# Plots"), ("code", "%matplotlib inline\nimport numpy")))
        text, result = convert(path)
        assert "%matplotlib" not in text
        assert "import numpy" in text
        assert any("%matplotlib inline" in note for note in result.notes)

    def test_shell_escapes_are_dropped(self, tmp_path):
        path = write(tmp_path, "T.ipynb", notebook(
            ("markdown", "# Setup"), ("code", "!pip install pandas\nimport pandas")))
        text, _ = convert(path)
        assert "!pip install" not in text
        assert "import pandas" in text

    def test_a_cell_of_nothing_but_magics_is_dropped_entirely(self, tmp_path):
        path = write(tmp_path, "T.ipynb", notebook(
            ("markdown", "# Setup"), ("code", "%matplotlib inline")))
        _, result = convert(path)
        assert result.cells == 0
        assert any("only magics" in note for note in result.notes)

    def test_a_percent_inside_code_is_left_alone(self, tmp_path):
        path = write(tmp_path, "T.ipynb", notebook(
            ("markdown", "# Maths"), ("code", "remainder = 7 % 3")))
        text, _ = convert(path)
        assert "remainder = 7 % 3" in text

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
        text, result = fn.convert(
            source, module="fixtures", series="s", year="2026-2027"
        )

        repo = tmp_path / "repo"
        (repo / "tutorials" / "fixtures").mkdir(parents=True)
        (repo / "tutorials" / "fixtures" / f"{result.slug}.md").write_text(text)
        (repo / "assets").mkdir()
        (repo / "assets" / "shell.html").write_text(
            (Path(__file__).resolve().parent.parent / "assets" / "shell.html").read_text()
        )
        for name, value in {
            "ROOT": repo, "TUTORIALS": repo / "tutorials", "SETUP": repo / "setup",
            "DATA": repo / "data", "ASSETS": repo / "assets",
            "SHELL": repo / "assets" / "shell.html", "OUT": repo / "site",
        }.items():
            monkeypatch.setattr(b, name, value)

        written = b.build()
        assert len(written) == 1
        page = written[0].read_text()
        assert "{{" not in page
        assert 'data-cell-id="making-decisions-1"' in page
        assert 'data-cell-id="a-second-section-1"' in page
        assert '<span class="dl-math">x^2</span>' in page
