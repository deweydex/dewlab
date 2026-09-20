#!/usr/bin/env python3
"""Diagrams for the maths series of the integrated course.

    python3 dev/graphics/maths.py --write

Same rule as the other generators: every number in a picture is computed
here rather than typed, so a figure cannot quietly disagree with the
arithmetic the page teaches.
"""

from __future__ import annotations

import argparse
import ast
import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import nested  # noqa: E402
import steps  # noqa: E402
import tree as tree_renderer  # noqa: E402
from tree import Node  # noqa: E402

TUTORIALS = Path(__file__).resolve().parent.parent.parent / "tutorials"

ACES, CARDS = 4, 52


def drawing_two_aces() -> str:
    """The tree behind *What Are the Chances?*'s two-aces example.

    The formula on the page, 4/52 times 3/51, is correct and says nothing
    about where 51 came from or why the second numerator is 3 rather than
    4. Both fall out of the picture: the deck is smaller on the second draw
    whatever happened, and how many aces are left depends on which branch
    you took. That difference between the two second-level branches is
    exactly what "not independent" means.
    """
    remaining = CARDS - 1
    first_ace = Fraction(ACES, CARDS)
    first_other = Fraction(CARDS - ACES, CARDS)
    ace_then_ace = Fraction(ACES - 1, remaining)
    ace_then_other = Fraction(remaining - (ACES - 1), remaining)
    other_then_ace = Fraction(ACES, remaining)
    other_then_other = Fraction(remaining - ACES, remaining)

    for siblings in ((first_ace, first_other),
                     (ace_then_ace, ace_then_other),
                     (other_then_ace, other_then_other)):
        if sum(siblings) != 1:
            raise SystemExit(f"branches {siblings} do not sum to 1")

    def label(numerator_over: Fraction) -> str:
        return f"{numerator_over.numerator}/{numerator_over.denominator}"

    def raw(top: int, bottom: int) -> str:
        return f"{top}/{bottom}"

    return tree_renderer.render(Node(f"{CARDS} cards", children=[
        Node("ace", note=f"{ACES - 1} aces left", edge=raw(ACES, CARDS), children=[
            Node("ace", note="both aces", edge=raw(ACES - 1, remaining), marked=True),
            Node("other", edge=raw(remaining - (ACES - 1), remaining)),
        ]),
        Node("other", note=f"{ACES} aces left", edge=raw(CARDS - ACES, CARDS), children=[
            Node("ace", edge=raw(ACES, remaining)),
            Node("other", edge=raw(remaining - ACES, remaining)),
        ]),
    ]))


def the_number_domains() -> str:
    """The nesting *Numbers and Their Families* writes as a chain of symbols.

    Each example sits in the band for the smallest family it belongs to, so
    the question the section sets — which families does this number belong
    to — is answered by finding the number and reading outwards. That is
    what the containment chain says, and it is faster to point at.
    """
    return nested.render(nested.Ring(
        "ℝ  reals", "√2   π   −1.5",
        inside=nested.Ring(
            "ℚ  rationals", "2/3   0.25",
            inside=nested.Ring(
                "ℤ  integers", "−5   −1",
                inside=nested.Ring("ℕ  naturals", "0   1   2   3")))))


def _sets_from_cell() -> tuple[list[int], list[int]]:
    """The two sets *Sets as Sorted Lists* walks, from its own cell."""
    page = (TUTORIALS / "sets-as-sorted-lists" / "sets-as-sorted-lists.md").read_text()
    cell = "set-operations-the-merge-pattern-1"
    if f"id: {cell}" not in page:
        raise SystemExit(f"sets-as-sorted-lists: no cell called {cell!r} any more")
    block = page.split(f"id: {cell}", 1)[1].split("```", 1)[0]
    found = {}
    for line in block.splitlines():
        stripped = line.strip()
        for name in ("a", "b"):
            if stripped.startswith(f"{name} = make_set("):
                inner = stripped[stripped.index("(") + 1:stripped.rindex(")")]
                found[name] = sorted(set(ast.literal_eval(inner)))
    if set(found) != {"a", "b"}:
        raise SystemExit(f"sets-as-sorted-lists/{cell}: no a and b defined")
    return found["a"], found["b"]


def walking_two_sorted_lists() -> str:
    """The merge pattern in *Sets as Sorted Lists*, one comparison per step.

    The prose states the rule as three cases and then a fourth about what
    is left over. Three of the reader's own functions are that same walk
    with a different line about what to keep, so it is worth seeing the
    walk itself once, with both pointers visible and the consequence of
    each comparison spelled out.
    """
    left, right = _sets_from_cell()
    return steps.merge_walk(left, right)


DIAGRAMS = {
    "sets-as-sorted-lists/merge-walk.svg": walking_two_sorted_lists,
    "numbers-and-their-families/number-domains.svg": the_number_domains,
    "what-are-the-chances/two-aces-tree.svg": drawing_two_aces,
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
