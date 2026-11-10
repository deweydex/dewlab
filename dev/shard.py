#!/usr/bin/env python3
"""Split test files across machines, so each machine runs one share.

    python3 dev/shard.py 4 2 tests/e2e/test_*.py     # the second of four shares

Prints the files in share K (counting from 1) of N, one per line. Whole files
are kept together, because most browser test files build a site once and share
it between their tests; splitting a file would build it again on every machine.

The biggest file goes first, onto whichever share is lightest so far, and so
on down. File size stands in for how long a file takes, which is rough and
needs no list of timings to keep up to date: a new file is placed by its size
with no one editing anything. Two machines given the same files and the same N
always give the same shares.
"""

from __future__ import annotations

import os
import sys


def shares(files: list[str], count: int) -> list[list[str]]:
    """`files` dealt into `count` shares, the heaviest first onto the lightest."""
    weight = {f: os.path.getsize(f) if os.path.exists(f) else 0 for f in files}
    # Sorted by weight, then name, so ties never depend on the order given.
    ordered = sorted(files, key=lambda f: (-weight[f], f))
    out: list[list[str]] = [[] for _ in range(count)]
    totals = [0] * count
    for f in ordered:
        lightest = totals.index(min(totals))
        out[lightest].append(f)
        totals[lightest] += weight[f]
    return [sorted(share) for share in out]


def main(argv: list[str]) -> int:
    if len(argv) < 4 or not argv[1].isdigit() or not argv[2].isdigit():
        print(__doc__.strip())
        return 1
    count, index = int(argv[1]), int(argv[2])
    if not 1 <= index <= count:
        print(f"Share {index} is not between 1 and {count}.")
        return 1
    for f in shares(argv[3:], count)[index - 1]:
        print(f)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
