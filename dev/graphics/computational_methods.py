#!/usr/bin/env python3
"""Every diagram Computational Methods uses, and where each one is written.

    python3 dev/graphics/computational_methods.py --write

Same rule as the database module's generator: a diagram is drawn from what
the tutorial actually does, not from a description of it typed a second
time. The recursion tree below is walked by the tutorial's own algorithm
with the tutorial's own tokens, so the repeated question it marks is the
one a reader's own cell would ask.
"""

from __future__ import annotations

import argparse
import ast
import collections
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import states  # noqa: E402
import tree as tree_renderer  # noqa: E402
from tree import Node  # noqa: E402

TUTORIALS = Path(__file__).resolve().parent.parent.parent / "tutorials"

MAKE_CHANGE_TOKENS = [1, 3, 4]
MAKE_CHANGE_TARGET = 6
MAKE_CHANGE_DEPTH = 2


def _repeat_counts(amount: int, tokens: list[int], depth: int) -> collections.Counter:
    """How often each amount is asked about within the depth being drawn.

    Counted over the drawn part rather than the whole recursion on purpose:
    the argument is one a reader makes by looking and counting, so the
    amount marked has to be the one that visibly recurs in front of them.
    Over the full tree a different amount wins, and marking that one would
    put a claim in the picture the picture does not support.
    """
    counts: collections.Counter = collections.Counter()

    def walk(remaining: int, level: int) -> None:
        counts[remaining] += 1
        if level < depth:
            for token in tokens:
                if token <= remaining:
                    walk(remaining - token, level + 1)

    walk(amount, 0)
    return counts


def _call_tree(amount: int, tokens: list[int], repeated: int, depth: int) -> Node:
    """The tree the brute-force version walks, cut off where it stops being
    readable. Every node asking the repeated amount is marked, because
    counting them is the argument."""

    def build(remaining: int, level: int, took: int | None) -> Node:
        node = Node(
            str(remaining),
            # Just the token: the node below already shows what is left, so
              # "take 3" spends width restating the arithmetic beside it.
              edge=f"\u2212{took}" if took is not None else "",
            marked=remaining == repeated,
        )
        if level < depth:
            node.children = [
                build(remaining - token, level + 1, token)
                for token in tokens
                if token <= remaining
            ]
        elif any(token <= remaining for token in tokens):
            node.note = "…"
        return node

    return build(amount, 0, None)


def the_same_question_twice() -> str:
    """*Three Ways to Make Change*'s argument for remembering an answer.

    Reaching the target by different first moves arrives at the same
    smaller amount, and brute force works it out again every time. The
    marked boxes are that amount; there are more of them further down than
    the drawing shows, which is the point.
    """
    counts = _repeat_counts(MAKE_CHANGE_TARGET, MAKE_CHANGE_TOKENS,
                            MAKE_CHANGE_DEPTH)
    # The amount asked most often, ignoring 0 (reaching the target exactly,
    # which is an ending rather than a question worth caching).
    repeated = max(
        (amount for amount in counts if amount not in (0, MAKE_CHANGE_TARGET)),
        key=lambda amount: (counts[amount], amount),
    )
    return tree_renderer.render(
        _call_tree(MAKE_CHANGE_TARGET, MAKE_CHANGE_TOKENS, repeated, MAKE_CHANGE_DEPTH))


def a_folder_of_folders() -> str:
    """The `photos` dictionary *Finding Everything Inside a Folder* builds.

    The tutorial describes three levels one node at a time, because a nested
    dictionary literal does not read as a shape. The same picture then
    serves twice more: the recursive walk descends it, and the iterative
    walk pushes and pops on it.
    """
    return tree_renderer.render(Node("photos", note="2 files", children=[
        Node("2025", note="1 file"),
        Node("2026", note="no files", children=[
            Node("trip", note="2 files"),
        ]),
    ]), note_style="code")


def _matrix_from_cell(slug: str, cell_id: str, name: str) -> list[list[float]]:
    """Read a matrix literal out of the tutorial's own cell.

    Same rule as everywhere else here: if the page changes its numbers, the
    picture changes with them, and if it stops defining them this fails at
    generation time rather than drawing yesterday's weather.
    """
    page = (TUTORIALS / slug / f"{slug}.md").read_text()
    if f"id: {cell_id}" not in page:
        raise SystemExit(f"{slug}: no cell called {cell_id!r} any more")
    block = page.split(f"id: {cell_id}", 1)[1].split("```", 1)[0]
    for line in block.splitlines():
        if line.strip().startswith(f"{name} ="):
            return ast.literal_eval(line.split("=", 1)[1].strip())
    raise SystemExit(f"{slug}/{cell_id}: no {name} defined")


def a_weather_machine() -> str:
    """The transition matrix in *Where Chains Lead*, drawn as what it is.

    Two states, four arrows, and the two self-loops included, because each
    row of the matrix is the arrows leaving one state and a row summing to
    one is only visible if every arrow out of that state is there.
    """
    matrix = _matrix_from_cell("where-chains-lead", "a-weather-machine-1", "P")
    return states.render(["sunny", "rainy"], matrix,
                         fmt=lambda p: f"{round(p * 100)}%")


DIAGRAMS = {
    "where-chains-lead/weather-states.svg": a_weather_machine,
    "three-ways-to-make-change/repeated-question.svg": the_same_question_twice,
    "finding-everything-inside-a-folder/photos-tree.svg": a_folder_of_folders,
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    written = parser.parse_args().write
    changed = 0
    for relative, draw in sorted(DIAGRAMS.items()):
        target = TUTORIALS / relative
        fresh = draw()
        if target.exists() and target.read_text() == fresh:
            print(f"  unchanged  {relative}")
            continue
        changed += 1
        if written:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(fresh)
            print(f"  written    {relative}")
        else:
            print(f"  would write {relative}")
    if changed and not written:
        print(f"\n{changed} diagram(s) differ. Re-run with --write.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
