#!/usr/bin/env python3
"""Which CI jobs a pull request's changed files can affect.

    python3 dev/ci_scope.py changed.txt >> "$GITHUB_OUTPUT"

`changed.txt` holds one changed path per line. Prints one `name=true` or
`name=false` line for each job that is decided by the files:

    code      anything that is not a document about the project: runs the unit
              tests, lint, the build, the solutions and the glossary check
    browser   what the browser tests build pages from, or run: assets, the
              build, the real pages, setup snippets, datasets, the curriculum
              files the page smoke test reads, the browser tests themselves
    bundle    what the committed vendor bundles are built from

The rule is to run a job when a file it reads has changed, and never to
guess which test a file "belongs to": a test that is wrongly left out is a
regression nobody sees. Where a rule is unclear, it runs. A push to `main`
and a manual run run everything (the workflow decides that, not this file).
"""

from __future__ import annotations

import re
import sys

# A change only to documents about the project runs the house-style reports
# and nothing else: no page reads them.
DOCUMENTS = re.compile(r"^(planning/|docs/|\.claude/|[^/]+\.md$)")

# Two parts of planning/ are read by the build, so they count as code.
READ_BY_BUILD = re.compile(r"^planning/(curriculum/|feedback\.yaml$)")

# The browser tests build sites of their own from tests/e2e/fixture and a few
# small pages they write, with the real assets, setup snippets and datasets,
# and the page smoke test also builds the real pages/ and reads the real
# topics and outcomes. A tutorial is never read; the solutions checker, the
# preview server and the download writers are not run by a browser test.
BROWSER = re.compile(
    r"^(assets/|compose/|setup/|data/|pages/|vendor-src/|tests/e2e/"
    r"|planning/curriculum/(topics|outcomes|topic-groups)\.yaml$"
    r"|build\.py$|source_map\.py$|requirements-(build|e2e)\.txt$|pytest\.ini$"
    r"|builder/(?!solutions|solution_runner|serve|downloads))"
)

# Files that decide what runs, or how: a change to one of them runs every job,
# since a mistake in them is a job that quietly stops running.
EVERYTHING = re.compile(r"^(\.github/workflows/tests\.yml|dev/(ci_scope|shard)\.py)$")

# The standalone bundle is the runtime, and everything the runtime imports,
# rebuilt as one file; it is committed, so a source edit leaves it stale.
BUNDLE = re.compile(r"^(vendor-src/|assets/vendor/|assets/[^/]+\.(js|mjs)$)")


def scope(changed: list[str]) -> dict[str, bool]:
    files = [f.strip() for f in changed if f.strip()]
    code = [f for f in files if not DOCUMENTS.match(f) or READ_BY_BUILD.match(f)]
    everything = any(EVERYTHING.match(f) for f in code)
    return {
        "code": bool(code),
        "browser": everything or any(BROWSER.match(f) for f in code),
        "bundle": everything or any(BUNDLE.match(f) for f in code),
    }


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(__doc__.strip())
        return 1
    with open(argv[1], encoding="utf-8") as listing:
        outcome = scope(listing.read().splitlines())
    for name, value in outcome.items():
        print(f"{name}={'true' if value else 'false'}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
