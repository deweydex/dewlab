"""Choices an educator makes that the build carries out and says so.

A page that builds with a note is a page a teacher can ship; a page that
stops the build is a page they cannot. The rule (DECISIONS_LOG 7.300) is that
a choice an educator makes about their own page, how many hints, whether a
block has a question in it, which setting a typo leaves unreadable, never
stops a build. Only what a reader would find broken does: a page that cannot
be parsed, a cell that cannot run, a link to nothing, saved work lost, a
cell id or tutorial id used twice.

Each case here is a page that used to stop the build. It must now build, the
build must say what it did, and where the case changes what the reader gets,
the page must show it. `check.py` agrees with the build about every one
(test_check.py).
"""

from __future__ import annotations

import json

import pytest

from helpers import *  # noqa: F401,F403
from helpers import b

CELL = "```python exec\nid: add-up\ndef total_of(values):\n    ...\n```\n"
SOLUTION = "```solution\ndef total_of(values):\n    return sum(values)\n```\n"
INPUTS = "```inputs\ntotal_of([1, 2, 3])\n```\n"
CHOICE = "```predict\nWhich?\n\n- a\n- b\n```\n"

# (markdown, what the build says, something the page then holds or None)
CASES = {
    # hints
    "a hint after an unreadable term": (
        CELL + "```hint\nafter: soon\nX.\n```\n", "has a term I cannot read",
        'data-after="errors:5"'),
    "a hint after a signal the runtime does not track": (
        CELL + "```hint\nafter: 5 bananas\nX.\n```\n", "does not track",
        'data-after="errors:5"'),
    "a hint after a retired signal": (
        CELL + "```hint\nafter: 3 failed checks\nX.\n```\n", "does not track",
        'data-after="errors:5"'),
    "a hint with no text": (
        CELL + "```hint\nafter: 5 errors\n```\n", "has no text in it, so it is left out",
        None),
    # solutions, inputs, typed lines
    "a solution with only notes": (
        CELL + "```solution\n---\nOnly notes.\n```\n", "has no code in it, so it is left out",
        None),
    "an inputs block with no cases": (
        CELL + SOLUTION + "```inputs\n# only a comment\n```\n", "list no cases, so the block is left out",
        None),
    "a guess setting that is not yes or no": (
        CELL + SOLUTION + INPUTS.replace("```inputs\n", "```inputs\nguess: maybe\n"),
        "is not yes or no, so the reader is not asked to guess", None),
    "an empty typed block": (
        CELL + "```typed\n\n```\n", "has no lines in it, so it is left out", None),
    "two typed blocks for one cell": (
        CELL + "```typed\none\n```\n```typed\ntwo\n```\n",
        "two typed blocks, so their lines are read one after the other", None),
    # questions, worlds
    "a fill-in question with a brace that never closes": (
        "```question\nid: q\ntype: fill-in-the-blank\n\nA {real} gap and an {open one.\n```\n",
        "has a { with no matching }", 'data-expected="real"'),
    "a question with no text": (
        "```question\nid: q\ntype: multiple-choice\nanswer: 1\n```\n",
        "has no text in it, so it is left out", None),
    # notes on a page
    "two notes with the same id": (
        '<aside class="dl-note" id="dup">\n\nOne.\n\n</aside>\n\n'
        '<aside class="dl-note" id="dup">\n\nTwo.\n\n</aside>\n',
        "two notes share the id 'dup', so the second is dup-2", None),
    # predictions
    "a prediction of an unknown type": (
        CELL + "```predict\ntype: essay\n\nWhy?\n```\n", "so it is read as `text`", None),
    "a choice prediction with no options": (
        CELL + "```predict\ntype: choice\n\nWhich?\n```\n",
        "asks for a typed guess instead", None),
    "a prediction tolerance that is not a number": (
        CELL + "```predict\ntype: number\ntolerance: lots\n\nHow many?\n```\n",
        "which is not a number, so a guess has to match exactly", None),
    "a prediction with a negative tolerance": (
        CELL + "```predict\ntype: number\ntolerance: -2\n\nHow many?\n```\n",
        "negative tolerance", None),
    "a prediction that asks no question": (
        CELL + "```predict\n- a\n- b\n```\n", "asks no question", None),
    "two predictions for one cell": (
        CELL + CHOICE + CHOICE, "a cell takes one guess, so the second is left out", None),
}


@pytest.mark.parametrize("case", sorted(CASES))
def test_it_builds_and_says_what_it_did(repo, capsys, case):
    markdown, said, shown = CASES[case]
    write(repo, markdown)
    b.build()
    assert said in capsys.readouterr().err
    if shown:
        assert shown in built(repo)


def test_a_dropped_hint_does_not_take_a_number_from_the_hints_after_it(repo):
    # Saved hint progress is keyed by position, so an empty hint that is left
    # out must not leave a gap or push the next one along.
    write(repo, CELL + "```hint\nafter: 1 error\n```\n```hint\nafter: 2 errors\nSecond.\n```\n")
    b.build()
    page = built(repo)
    assert 'id="dl-staged-add-up-0"' in page and 'id="dl-staged-add-up-1"' not in page


def test_two_typed_blocks_are_one_list_in_the_order_written(repo):
    write(repo, CELL + SOLUTION + INPUTS + "```typed\none\n```\n```typed\ntwo\n```\n")
    b.build()
    cell = b.load(next((repo / "tutorials").rglob("sample.md"))).cells[0]
    assert cell.typed == ["one", "two"]


def test_worlds_given_as_a_list_of_keys_are_worlds_without_a_line_each(repo, capsys):
    variants = "".join(
        f'<div class="dl-world" data-world="{world}">\n\nTask.\n\n'
        f"```python exec\nid: task--{world}\nx = 1\n```\n</div>\n\n"
        for world in ("planets", "sea-floor"))
    path = write(repo, "# A page\n\n" + variants)
    add_frontmatter(path, "worlds: [planets, sea-floor]\n")
    b.build()
    assert "is a list of keys" in capsys.readouterr().err
    page = built(repo)
    assert '<span class="dl-world-name">Sea floor</span>' in page
    assert 'value="planets"' in page


class TestADatasetThatDoesNotSayWhereItCameFrom:
    """Where numbers came from is the educator's to say. A blank field is
    listed in a note and the Reference tab says it was not recorded; only a
    missing snapshot date makes the dataset unusable as a source, and then it
    is treated like a data file with no yaml at all."""

    def declare(self, repo, text):
        path = write(repo, "Prose.\n", slug="one")
        add_frontmatter(path, "datasets:\n  - sparse\n")
        (repo / "data" / "sparse.csv").write_text("a,b\n1,2\n")
        (repo / "data" / "sparse.yaml").write_text(text)

    def test_blank_fields_are_listed_and_said_to_be_unrecorded(self, repo, capsys):
        self.declare(repo, 'source: "Somewhere"\nsnapshot: 2026-09-26\n')
        b.build()
        assert "does not give its url, license, trimmed, description" in capsys.readouterr().err
        page = built(repo, "one")
        assert "No description recorded" in page and "licence not recorded" in page
        assert "Somewhere" in page and "26 September 2026" in page

    def test_no_snapshot_date_is_a_note_and_the_dataset_is_left_out_of_the_reference(self, repo, capsys):
        self.declare(repo, 'source: "Somewhere"\n')
        b.build()
        assert "has no snapshot: date like 2026-09-26" in capsys.readouterr().err
        # Not in the page's reference, and the data index carries it with no date.
        assert "datasets" not in manifest(built(repo, "one"))
        assert json.loads((repo / "site" / "data" / "index.json").read_text())["sparse.csv"] == {}


class TestACourseIndexAndCourseFileTheEducatorLeftRough:
    """courses/ is the educator's, and its small slips change a tile or an
    order, never whether the site builds."""

    def index(self, repo, text):
        (repo / "courses" / "index.yaml").write_text(text)

    def test_cards_that_is_not_a_list_leaves_the_tiles_in_order(self, repo, capsys):
        write(repo, "Prose.\n")
        self.index(repo, "cards: computational-methods\n")
        b.build()
        assert "needs `cards:` as a list" in capsys.readouterr().err
        assert [course.id for course in b.course_card_order()] == list(b.courses())

    def test_order_that_is_not_a_list_leaves_the_courses_alphabetical(self, repo, capsys):
        write(repo, "Prose.\n")
        self.index(repo, "order: computational-methods\n")
        b.build()
        assert "needs `order:` as a list" in capsys.readouterr().err

    def test_a_card_named_twice_is_one_tile(self, repo):
        write(repo, "Prose.\n")
        self.index(repo, "cards:\n  - computational-methods\n  - computational-methods\n")
        b.build()
        assert [course.id for course in b.course_card_order()].count("computational-methods") == 1

    def test_a_course_with_no_title_is_called_by_its_file_name(self, repo, capsys):
        write(repo, "Prose.\n")
        (repo / "courses" / "untitled.yaml").write_text("contents: []\n")
        b.build()
        assert "has no `title:` line, so the course is called 'untitled'" in capsys.readouterr().err
        assert "untitled" in (repo / "site" / "index.html").read_text()

    def test_a_course_status_this_build_does_not_know_has_no_badge(self, repo, capsys):
        write(repo, "Prose.\n")
        (repo / "courses" / "odd.yaml").write_text("title: Odd\nstatus: lvie\ncontents: []\n")
        b.build()
        assert "status 'lvie' is not one of" in capsys.readouterr().err
        assert b.courses()["odd"].status == "live"


def test_a_tutorial_with_no_year_builds_without_one(repo):
    # Year is a label for the educator's own use; nothing a reader meets
    # depends on it.
    path = write(repo, "Prose.\n")
    path.write_text(path.read_text().replace('year: "2026-2027"\n', ""))
    b.build()
    assert 'name="tutorial-year" content=""' in built(repo)
