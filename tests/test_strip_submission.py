"""dev/strip_submission.py: what it drops, what it keeps, and what it says.

Notebooks are built in the tests themselves, as in test_from_notebook.py. The
PDF step needs XeLaTeX and pandoc, which CI does not install, so it is skipped
where they are missing; everything before it is tested without them."""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

import pytest

nbformat = pytest.importorskip("nbformat")
pytest.importorskip("yaml")

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "dev"))

import strip_submission as ss  # noqa: E402

md, code = nbformat.v4.new_markdown_cell, nbformat.v4.new_code_cell

TEMPLATE_CELLS = [
    ("markdown", "# Brief\n\n| a | b |\n|---|---|\n| 1 | 2 |"),
    ("markdown", "## Part 1: `f`\n\nWrite `def f():`"),
    ("markdown", "### 1.1 Plan\n\n*Write your plan here.*"),
    ("code", ""),
    ("code", "# PROVIDED. Do not change this cell.\nDATA = [1, 2, 3]\n"),
]


def make(cells) -> "nbformat.NotebookNode":
    return nbformat.v4.new_notebook(cells=[
        md(src) if kind == "markdown" else code(src) for kind, src in cells])


@pytest.fixture
def template():
    return make(TEMPLATE_CELLS)


def run(template, cells, rubric=None):
    return ss.strip(template, make(cells), rubric, "sub.ipynb")


def sources(nb):
    return [c.source for c in nb.cells]


class TestWhatGoes:
    def test_an_untouched_template_cell_is_dropped(self, template):
        nb, report = run(template, TEMPLATE_CELLS)
        assert report.dropped == 4 and report.kept == 0

    def test_whitespace_and_line_endings_do_not_make_a_cell_the_students(self, template):
        nb, report = run(template, [("code", "# PROVIDED. Do not change this cell.  \r\nDATA = [1, 2, 3]\r\n\r\n")])
        assert report.dropped == 1 and not report.flags

    def test_a_cell_of_the_wrong_type_is_not_a_match(self, template):
        nb, report = run(template, [("code", "## Part 1: `f`\n\nWrite `def f():`")])
        assert report.kept == 1

    def test_blank_cells_are_nobodys_work(self, template):
        nb, report = run(template, [("code", "   \n"), ("markdown", "")])
        assert nb.cells == [] and report.kept == 0

    def test_without_a_rubric_headings_up_to_level_two_stay(self, template):
        nb, _ = run(template, TEMPLATE_CELLS)
        assert sources(nb) == ["# Brief", "## Part 1: `f`"]


class TestWhatStays:
    def test_the_students_cells_are_kept_whole_and_in_order(self, template):
        mine = [("markdown", "## Part 1: `f`\n\nWrite `def f():`"),
                ("code", "def f():\n    return 1"), ("markdown", "my note")]
        nb, report = run(template, mine)
        assert sources(nb)[1:] == ["def f():\n    return 1", "my note"]
        assert report.kept == 2

    def test_outputs_are_kept(self, template):
        cell = code("print(1)")
        cell.outputs = [nbformat.v4.new_output("stream", name="stdout", text="1\n")]
        sub = nbformat.v4.new_notebook(cells=[cell])
        nb, _ = ss.strip(template, sub, None, "s.ipynb")
        assert nb.cells[0].outputs[0].text == "1\n"


class TestWhatItSaysAboutEdits:
    def test_an_edited_do_not_change_cell_is_kept_and_flagged(self, template):
        nb, report = run(template, [("code", "# PROVIDED. Do not change this cell.\nDATA = [1, 2, 4]")])
        assert report.kept == 1
        assert any("do-not-change" in f for f in report.flags)

    def test_a_template_cell_the_student_wrote_into_is_kept_and_flagged(self, template):
        nb, report = run(template, [("markdown", "### 1.1 Plan\n\n*Write your plan here.*\nFOR each x IN y")])
        assert report.kept == 1
        assert any("edited from a template cell" in f for f in report.flags)

    def test_an_unrelated_cell_is_not_flagged(self, template):
        _, report = run(template, [("code", "def f():\n    return 1")])
        assert not report.flags

    def test_characters_the_pdf_font_lacks_are_flagged(self, template):
        _, report = run(template, [("markdown", "日本語 🙂")])
        assert any("may not show" in f for f in report.flags)


class TestRubric:
    @pytest.fixture
    def rubric(self):
        return ss.Rubric(parts=[{"heading": "Part 1: `f`", "marks": 6}])

    def test_a_kept_heading_carries_its_marks(self, template, rubric):
        nb, _ = run(template, TEMPLATE_CELLS, rubric)
        assert sources(nb) == ["## Part 1: `f` *(6 marks)*"]

    def test_headings_outside_the_rubric_are_left_out(self, template, rubric):
        nb, report = run(template, TEMPLATE_CELLS, rubric)
        assert report.headings == 1

    def test_a_heading_the_student_typed_over_is_still_annotated(self, template, rubric):
        nb, _ = run(template, [("markdown", "## Part 1: `f`\nMy words")], rubric)
        assert nb.cells[0].source.startswith("## Part 1: `f` *(6 marks)*")

    def test_a_rubric_heading_missing_from_the_result_is_reported(self, template):
        rubric = ss.Rubric(parts=[{"heading": "Part 9: nowhere", "marks": 1}])
        _, report = run(template, TEMPLATE_CELLS, rubric)
        assert any("Part 9" in f for f in report.flags)

    def test_a_heading_inside_a_fence_is_a_comment_not_a_heading(self):
        text = "```\n## not a heading\n```\n## real"
        assert list(ss.headings_of(text)) == [(2, "real")]

    def test_criteria_that_do_not_add_up_are_refused(self, tmp_path):
        path = tmp_path / "r.yaml"
        path.write_text("parts:\n  - heading: P\n    marks: 5\n    criteria:\n"
                        "      - {for: a, marks: 2}\n      - {for: b, marks: 2}\n")
        with pytest.raises(ss.StripError, match="add to 4, not 5"):
            ss.load_rubric(path)

    def test_the_marks_table_totals_and_leaves_unknown_marks_blank(self):
        full = ss.Rubric(parts=[{"heading": "A", "marks": 3}, {"heading": "B", "marks": 7}])
        assert "| **Total** |  | 10 |" in ss.marks_table(full)
        gap = ss.Rubric(parts=[{"heading": "A", "marks": 3}, {"heading": "B", "marks": None}])
        assert "| **Total** |  |  |" in ss.marks_table(gap)

    def test_the_skeleton_rubric_lists_parts_and_guesses_no_marks(self, template, tmp_path):
        path = tmp_path / "t.ipynb"
        nbformat.write(template, str(path))
        skeleton = ss.init_rubric(path)
        rubric_path = tmp_path / "r.yaml"
        rubric_path.write_text(skeleton)
        rubric = ss.load_rubric(rubric_path)
        assert [p["heading"] for p in rubric.parts] == ["Part 1: `f`"]
        assert rubric.parts[0]["marks"] is None


class TestPercentFiles:
    def test_a_py_file_round_trips_through_the_notebook_form(self, tmp_path):
        nb = make([("markdown", "# Title\n\ntext"), ("code", "x = 1\n\ny = 2")])
        path = tmp_path / "a.py"
        ss.write_percent_py(nb, path)
        back = ss.load(path)
        assert [(c.cell_type, c.source) for c in back.cells] == [
            ("markdown", "# Title\n\ntext"), ("code", "x = 1\n\ny = 2")]

    def test_a_py_submission_is_stripped_against_an_ipynb_template(self, template, tmp_path):
        path = tmp_path / "s.py"
        ss.write_percent_py(make(TEMPLATE_CELLS + [("code", "def f(): pass")]), path)
        nb, report = ss.strip(template, ss.load(path), None, "s.py")
        assert report.kept == 1 and nb.cells[-1].source == "def f(): pass"

    def test_an_unreadable_notebook_is_a_clear_error(self, tmp_path):
        path = tmp_path / "bad.ipynb"
        path.write_text("{not json")
        with pytest.raises(ss.StripError, match="bad.ipynb"):
            ss.load(path)


@pytest.mark.skipif(not (shutil.which("xelatex") and shutil.which("pandoc")),
                    reason="needs xelatex and pandoc")
def test_the_marking_pdf_is_built_and_typesets_maths_and_accents(template, tmp_path):
    rubric = ss.Rubric(title="T", parts=[{"heading": "Part 1: `f`", "marks": 6,
                                          "criteria": [{"for": "Code", "marks": 6}]}])
    nb, _ = run(template, TEMPLATE_CELLS + [("markdown", "share $v/n$ and café, cost \\$5")], rubric)
    pdf = tmp_path / "out.pdf"
    ss.write_pdf(nbformat.v4.new_notebook(cells=[ss.cover_cell("s.ipynb", rubric), *nb.cells]),
                 "s.ipynb", pdf)
    assert pdf.read_bytes().startswith(b"%PDF")
