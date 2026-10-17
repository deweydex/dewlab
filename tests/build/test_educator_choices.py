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
