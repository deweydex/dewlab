"""Blocks attached to a cell (#312): a ```solution fence and an ```inputs
fence, and a cell of the reader's own tests. Each belongs to the exec cell
above it, or to the one its `for:` line names. The build renders a solution
as a closed fold and the inputs as a comparison table, puts what the
comparison needs in the manifest, and runs every solution before a reader
can open it."""

from __future__ import annotations

import pytest

from helpers import *  # noqa: F401,F403
from helpers import b

CELL = """```python exec
id: add-up
def total_of(values):
    ...
```
"""

SOLUTION = """```solution
def total_of(values):
    return sum(values)
---
Python's own `sum()` is an **accumulator**.
```
"""

INPUTS = """```inputs
total_of([1, 2, 3])
total_of([])     # an empty list
```
"""


def cell_spec(page: str, ident: str) -> dict:
    return next(c for c in manifest(page)["cells"] if c["id"] == ident)


class TestRendering:
    def test_a_solution_is_a_closed_fold_with_its_code_and_notes(self, repo):
        write(repo, CELL + SOLUTION)
        b.build()
        page = built(repo)
        assert '<details class="dl-solution" data-cell="add-up">' in page
        assert "<summary>One way to do it</summary>" in page
        assert "return sum(values)" in page.split("dewlab-manifest")[0]
        assert "<strong>accumulator</strong>" in page

    def test_a_title_line_names_the_fold(self, repo):
        write(repo, CELL + SOLUTION.replace("```solution\n",
                                            "```solution\ntitle: a shorter way\n"))
        b.build()
        assert "<summary>a shorter way</summary>" in built(repo)

    def test_inputs_become_a_table_with_a_row_per_case_and_its_label(self, repo):
        write(repo, CELL + SOLUTION + INPUTS)
        b.build()
        page = built(repo)
        assert '<div class="dl-compare" data-cell="add-up">' in page
        assert page.count('<tr data-case="') == 2
        assert "<code>total_of([])</code>" in page
        assert '<span class="dl-compare-label">an empty list</span>' in page
        assert '<th scope="col">A solution</th>' in page
        assert ">Compare with a solution</button>" in page

    def test_without_a_solution_there_is_only_the_readers_column(self, repo):
        write(repo, CELL + INPUTS)
        b.build()
        page = built(repo)
        assert "A solution</th>" not in page
        assert ">Try these on your code</button>" in page

    def test_guess_yes_adds_a_box_per_case(self, repo):
        write(repo, CELL + INPUTS.replace("```inputs\n", "```inputs\nguess: yes\n"))
        b.build()
        page = built(repo)
        assert '<th scope="col">Your guess</th>' in page
        assert page.count('<td class="dl-compare-guess"><input type="text"') == 2

    def test_no_word_in_the_markup_judges(self, repo):
        write(repo, CELL + SOLUTION + INPUTS)
        b.build()
        table = built(repo).split('<div class="dl-compare"')[1].split("</div></div>")[0]
        for word in ("correct", "wrong", "not yet", "pass", "fail"):
            assert word not in table.lower()


class TestManifest:
    def test_the_comparison_travels_with_the_cell(self, repo):
        write(repo, CELL + SOLUTION + INPUTS)
        b.build()
        spec = cell_spec(built(repo), "add-up")
        assert spec["solution"] == "def total_of(values):\n    return sum(values)"
        assert spec["inputs"] == [
            {"expr": "total_of([1, 2, 3])", "label": None},
            {"expr": "total_of([])", "label": "an empty list"},
        ]
        assert "guess" not in spec

    def test_the_comparison_uses_the_first_of_two_solutions(self, repo):
        second = SOLUTION.replace("return sum(values)", "return 0 + sum(values)")
        write(repo, CELL + SOLUTION + second + INPUTS)
        b.build()
        page = built(repo)
        assert cell_spec(page, "add-up")["solution"].endswith("return sum(values)")
        assert page.count('class="dl-solution"') == 2

    def test_a_cell_of_tests_is_named_on_the_cell_it_tests(self, repo):
        tests = "```python exec\nid: my-tests\ntests: add-up\nassert total_of([1]) == 1\n```\n"
        write(repo, CELL + SOLUTION + INPUTS + tests)
        b.build()
        assert cell_spec(built(repo), "add-up")["tests"] == "my-tests"

    def test_for_attaches_a_block_to_another_cell(self, repo):
        other = "```python exec\nid: another\nx = 1\n```\n"
        write(repo, CELL + other + SOLUTION.replace("```solution\n", "```solution\nfor: add-up\n"))
        b.build()
        page = built(repo)
        assert "solution" in cell_spec(page, "add-up")
        assert "solution" not in cell_spec(page, "another")


class TestMistakes:
    @pytest.mark.parametrize("body, match", [
        (SOLUTION, "no exec cell above it"),
        (CELL + SOLUTION.replace("```solution\n", "```solution\nfor: nowhere\n"),
         "does not have: 'nowhere'"),
        (CELL + "```solution\ndef total_of(values)\n    return 1\n```\n", "not valid Python"),
        (CELL + "```solution\n---\nOnly notes.\n```\n", "no code in it"),
        (CELL + "```inputs\ntotal_of([1] +)\n```\n", "not a Python expression"),
        (CELL + "```inputs\n# only a comment\n```\n", "list no cases"),
        (CELL + INPUTS + INPUTS, "two inputs blocks"),
        (CELL + INPUTS.replace("```inputs\n", "```inputs\nguess: maybe\n"), "guess: maybe"),
        ("```sql exec\nid: q\nSELECT 1;\n```\n" + SOLUTION, "only a Python cell"),
        (CELL + "```python exec\nid: t\ntests: nowhere\n```\n", "no other cell"),
        (CELL + "```python exec\nid: t1\ntests: add-up\n```\n"
                "```python exec\nid: t2\ntests: add-up\n```\n", "one cell of tests"),
    ])
    def test_the_build_says_what_is_wrong(self, repo, body, match):
        write(repo, body)
        with pytest.raises(b.BuildError, match=match):
            b.build()


class TestTheBuildRunsEverySolution:
    """check_solutions(): the page's cells run first, in a separate Python,
    then tutorial_tools.compare() runs each solution with its inputs."""

    def test_a_solution_that_raises_fails_the_build(self, repo):
        write(repo, CELL + "```solution\nraise ValueError('the page is wrong')\n```\n")
        with pytest.raises(b.BuildError, match="raised ValueError: the page is wrong"):
            b.build()

    def test_a_solution_may_use_what_earlier_cells_made(self, repo):
        data = "```python exec\nid: data\nwidths = [4879, 12104]\n```\n"
        write(repo, data + CELL + "```solution\ntotal = sum(widths)\n```\n"
                    "```inputs\ntotal\n```\n")
        b.build()

    def test_an_earlier_cell_that_fails_on_purpose_is_fine(self, repo):
        broken = "```python exec\nid: broken\n1 / 0\n```\n"
        write(repo, broken + CELL + SOLUTION + INPUTS)
        b.build()

    def test_a_page_this_python_lacks_a_package_for_is_skipped(self, repo, capsys):
        # The publish job installs only requirements-build.txt, so a setup
        # cell that imports matplotlib stops before it defines anything, and
        # the solution below it meets names that were never made. That says
        # nothing about the solution, so the build notes it and moves on.
        setup = ("```python exec\nid: setup\nimport a_package_this_python_lacks\n"
                 "def helper(values):\n    return sum(values)\n```\n")
        write(repo, setup + CELL + "```solution\ndef total_of(values):\n"
                    "    return helper(values)\n```\n```inputs\ntotal_of([1, 2])\n```\n")
        b.build()
        assert "a_package_this_python_lacks" in capsys.readouterr().err

    def test_an_input_the_solution_cannot_name_fails_the_build(self, repo):
        write(repo, CELL + SOLUTION + "```inputs\ntotl_of([1])\n```\n")
        with pytest.raises(b.BuildError, match="totl_of"):
            b.build()

    def test_an_input_that_raises_on_purpose_is_an_outcome(self, repo):
        write(repo, CELL + SOLUTION + "```inputs\ntotal_of(None)   # not a list\n```\n")
        b.build()

    def test_an_endless_cell_before_the_solution_does_not_hang_the_build(self, repo, monkeypatch):
        monkeypatch.setattr(b, "SOLUTION_CELL_SECONDS", 1)
        endless = "```python exec\nid: endless\nwhile True:\n    pass\n```\n"
        write(repo, endless + CELL + SOLUTION + INPUTS)
        b.build()

    def test_a_page_without_solutions_runs_nothing(self, repo, monkeypatch):
        def refuse(*args, **kwargs):
            raise AssertionError("ran a page with no solutions")
        monkeypatch.setattr(b.subprocess, "run", refuse)
        write(repo, CELL + INPUTS)
        b.build()
