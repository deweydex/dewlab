"""Running every solution on a page, the way a reader's browser would.

Not part of a build. `python3 check.py` runs it for the pages it is given
(or for the whole site), and CI runs it on every pull request. A build only
writes pages; this is what says the code on them works.
"""

from __future__ import annotations

from pathlib import Path
import concurrent.futures
import functools
import hashlib
import json
import os
import subprocess
import sys
import threading

from builder.config import REPO, cfg
from builder.main import (
    BuildError,
    Cell,
    Tutorial,
    data_index,
    fail,
    read_site,
    say,
    toolkit_for,
)


# Every solution is run before a reader can see it (#312), in a separate
# Python so a page's code never runs inside the checker itself.
# Each cell gets SOLUTION_CELL_SECONDS where the platform can enforce it
# (a deliberate endless loop on a page about the Stop button is a cell
# that fails, not a build that hangs); the whole page gets the rest.
# The runtime module the runner imports: always the build's own copy, since
# it is part of the build rather than of the content being built.
RUNTIME_TOOLS = REPO / "assets"


SOLUTION_CELL_SECONDS = 20


SOLUTION_PAGE_SECONDS = 180


# The program that runs a page: a file of its own, so it can be read and
# linted like any other, and so a page's code never runs in this process.
RUNNER = Path(__file__).with_name("solution_runner.py")


# A page whose solutions all ran clean last time, with the same cells, the
# same toolkit, the same data, the same runtime and the same packages, will
# run clean again, and running them takes minutes for a whole site. The key is
# a hash of exactly those things, so there is nothing to invalidate by hand:
# an edit to a cell, a dataset, tutorial_tools.py or an installed package is
# a different key and the page runs. Only a clean pass is kept. A failure, or
# a solution skipped for a package this Python lacks, runs every time, so
# the cache can hide nothing a fresh run would have said. `check.py --no-cache`
# turns it off (cfg.SOLUTION_CACHE), and `--refresh-cache` runs every page and
# keeps what was clean (cfg.SOLUTION_CACHE_REUSE): a push to main does that,
# so what it learned is checked fresh and is what pull requests start from.


def _cache_dir() -> Path:
    return Path(os.environ.get("DEWLAB_BUILD_CACHE") or cfg.ROOT / ".build-cache") / "solutions"


@functools.lru_cache(maxsize=None)
def _tree_fingerprint(root: Path) -> str:
    """A hash of every file under `root`, by relative path and content."""
    digest = hashlib.sha256()
    for path in sorted(p for p in root.rglob("*") if p.is_file()):
        digest.update(str(path.relative_to(root)).encode())
        digest.update(path.read_bytes())
    return digest.hexdigest()


@functools.lru_cache(maxsize=None)
def _environment_fingerprint() -> str:
    """The Python and every installed package, by version."""
    from importlib import metadata
    installed = sorted({(d.metadata["Name"] or "").lower(): d.version
                        for d in metadata.distributions()}.items())
    return f"{sys.version}\n{installed}"


def _solution_key(job: dict) -> str:
    """What a page's solution check depends on, as one hash. The job's two
    absolute paths are left out so a checkout elsewhere has the same key."""
    stable = {name: value for name, value in job.items() if name not in ("assets", "data")}
    digest = hashlib.sha256()
    for part in (json.dumps(stable, sort_keys=True), RUNNER.read_text(),
                 (RUNTIME_TOOLS / "tutorial_tools.py").read_text(),
                 _tree_fingerprint(cfg.DATA) if cfg.DATA.is_dir() else "",
                 _environment_fingerprint()):
        digest.update(part.encode())
        digest.update(b"\0")
    return digest.hexdigest()


def check_solutions(tutorial: Tutorial, toolkit: list[dict]) -> None:
    """Run every solution on the page, with its inputs, before a reader can
    open it (#312).

    The page's own Python cells run first, in order, as a reader's would
    (the toolkit before them, as the page loads it), in a separate Python
    process with the runtime's own `tutorial_tools`. A cell that fails as
    written is fine: plenty fail on purpose, or wait for the reader. Then
    `tutorial_tools.compare()`, the function the comparison button calls,
    runs each solution. A solution that raises fails the build, and so
    does an input the solution side cannot even name (a NameError or
    SyntaxError there is a typo in the page, not an outcome worth showing).
    Any other error an input raises is an outcome, and the table shows it.

    A Python without a package the page imports (a contributor's machine
    without pandas, say, or the publish job, which installs only
    requirements-build.txt) is noted and skipped, not failed: that says
    nothing about the solution. That holds when the import is in a cell
    above the solution, too: once a cell stops at a missing package,
    every solution below it is noted and skipped, since the names that
    cell would have made are missing as well.

    A page with world variants (#315) runs once per world, with the cells
    a reader in that world would run: every cell outside a variant, and
    that world's variants. Each world's solutions are checked in its own
    run, and the solutions outside every variant in the first."""
    worlds = list(dict.fromkeys(cell.world for cell in tutorial.cells if cell.world))
    for position, world in enumerate(worlds or [None]):
        seen = [cell for cell in tutorial.cells if cell.world in (None, world)]

        def checked(cell: Cell) -> bool:
            return bool(cell.solutions) and (
                cell.world == world or (cell.world is None and position == 0))

        last = max((i for i, cell in enumerate(seen) if checked(cell)), default=None)
        if last is not None:
            _run_solutions(tutorial, toolkit, seen[: last + 1], checked)


def every_problem(tutorials: list[Tutorial], toolkits: list[list[dict]]) -> list[str]:
    """check_solutions() for every page, several pages at once, and what each
    page that failed said, in page order.

    Each page's check is a Python process of its own, so this spends its
    time waiting rather than working. Pages run side by side on threads, one
    per core; each thread only starts a process and waits for it. Every page
    finishes before anything is reported, so one wrong solution does not
    hide the next. Notes about a skipped solution may print in a different
    order.
    """
    def one(tutorial: Tutorial, toolkit: list[dict]) -> str:
        try:
            check_solutions(tutorial, toolkit)
        except BuildError as refusal:
            return str(refusal)
        return ""

    workers = min(len(tutorials), os.cpu_count() or 1)
    if workers <= 1:
        said = [one(tutorial, toolkit) for tutorial, toolkit in zip(tutorials, toolkits)]
    else:
        with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
            said = list(pool.map(one, tutorials, toolkits))
    return [problem for problem in said if problem]


def _run_solutions(tutorial: Tutorial, toolkit: list[dict], seen: list[Cell], checked) -> None:
    """One separate Python for check_solutions(): the cells in `seen`, in
    order, each followed by its solutions where `checked(cell)` says so."""
    cells = []
    for cell in seen:
        if cell.type != "python":
            continue
        cells.append({"id": cell.id, "code": cell.code}
                     | ({"typed": cell.typed} if cell.typed else {}))
        if not checked(cell):
            continue
        cases = [{"expr": case.expr, "label": case.label}
                 for case in (cell.inputs.cases if cell.inputs else [])]
        # Every solution, not only the first one the comparison uses. Each
        # runs in its own copy of the namespace the cell above left.
        for solution in cell.solutions:
            cells.append({"id": cell.id, "code": "", "solution": solution.code,
                          "inputs": cases}
                         | ({"typed": cell.typed} if cell.typed else {}))
    job = {
        "assets": str(RUNTIME_TOOLS), "data": str(cfg.DATA), "sqlite": tutorial.has_sql,
        # A web address data/ keeps a copy of runs against that copy, as a
        # page offline would (#324).
        "addresses": {entry["live"]["url"]: file_name
                      for file_name, entry in data_index().items() if entry.get("address")},
        "seconds": SOLUTION_CELL_SECONDS,
        "toolkit": [entry["reference"] for entry in toolkit],
        "cells": cells,
    }
    marker = _cache_dir() / _solution_key(job) if cfg.SOLUTION_CACHE else None
    if marker is not None and cfg.SOLUTION_CACHE_REUSE and marker.is_file():
        return
    try:
        done = subprocess.run(
            [sys.executable, str(RUNNER)], input=json.dumps(job),
            capture_output=True, text=True, timeout=SOLUTION_PAGE_SECONDS, cwd=cfg.ROOT,
        )
    except subprocess.TimeoutExpired:
        fail(tutorial.path, f"the build ran this page's cells to check its solutions, "
                            f"and they did not finish in {SOLUTION_PAGE_SECONDS} seconds")
    if done.returncode != 0:
        fail(tutorial.path, "the build could not run this page's solutions:\n"
                            + done.stderr.strip()[-2000:])
    clean = True  # nothing skipped: only then is the result worth keeping
    for entry in json.loads(done.stdout or "[]"):
        result, cell = entry["result"], entry["cell"]
        problem = result.get("solutionError")
        if problem and problem.startswith("ModuleNotFoundError"):
            say(f"note: could not check the solution for cell {cell!r} in "
                  f"{tutorial.path.relative_to(cfg.ROOT)}: {problem}")
            clean = False
            continue
        if result.get("missingModule"):
            # A cell above it stopped at an import, so the names it would
            # have made are missing too, and a NameError here would blame
            # the solution for this Python's missing package.
            say(f"note: could not check the solution for cell {cell!r} in "
                  f"{tutorial.path.relative_to(cfg.ROOT)}: an earlier cell raised "
                  f"{result['missingModule']}")
            clean = False
            continue
        if problem and problem.startswith("EOFError"):
            # The solution is not wrong; the build cannot type for it. Nothing
            # was checked, so nothing is kept.
            say(f"note: could not check the solution for cell {cell!r} in "
                  f"{tutorial.path.relative_to(cfg.ROOT)}: it calls input() and nobody can type "
                  "in the build. Give the cell a ```typed block with enough lines to check it")
            clean = False
            continue
        if problem:
            fail(tutorial.path, f"the solution for cell {cell!r} raised {problem} when the "
                                "build ran it after the page's earlier cells")
        for row in result.get("rows", []):
            error = row.get("solution", {}).get("error", "")
            if error.startswith(("NameError", "SyntaxError")):
                fail(tutorial.path, f"the input `{row['input']}` for cell {cell!r} gives "
                                    f"{error} with the solution — is it spelled as the "
                                    "page spells it?")
    if clean and marker is not None:
        marker.parent.mkdir(parents=True, exist_ok=True)
        temporary = marker.with_suffix(f".{os.getpid()}.{threading.get_ident()}")
        temporary.write_text(tutorial.slug)
        temporary.replace(marker)


def problems_in(site, folders: set[str] | None = None) -> tuple[int, list[str]]:
    """Run the solutions on every page of a site read by read_site(), or on
    the pages in the named tutorial folders. Returns how many pages had a
    solution to run, and what each page that failed said."""
    chosen = [t for t in site.tutorials
              if (folders is None or t.path.parent.name in folders)
              and any(cell.solutions for cell in t.cells)]
    toolkits = [toolkit_for(t, site.registry, site.groups) for t in chosen]
    return len(chosen), every_problem(chosen, toolkits)


def check_site(folders: set[str] | None = None) -> int:
    """read_site(), then problems_in(): the whole site is read either way,
    since a page's toolkit comes from the pages before it in its course.
    Returns how many pages it ran; the first wrong solution raises
    BuildError."""
    ran, problems = problems_in(read_site(), folders)
    if problems:
        raise BuildError(problems[0])
    return ran
