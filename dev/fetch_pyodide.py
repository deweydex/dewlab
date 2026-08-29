#!/usr/bin/env python3
"""Download a trimmed, self-hosted Pyodide into dev/pyodide/.

Three uses:

  * the e2e tests serve it, so they never depend on a CDN being reachable from
    wherever they run;
  * it is the escape hatch for OPEN_QUESTIONS.md 32 — if a school network turns
    out to block the CDN, this same directory is what gets committed under
    assets/ and pointed at with DEWLAB_PYODIDE_BASE;
  * build.py's write_mini_ide_bundle() (planning/MINI_IDE_REDESIGN.md Phase 7)
    points --out at assets/vendor/pyodide/ instead, with --packages widened to
    include sqlite3, to make the downloadable Mini IDE bundle work offline
    after its first run.

"Trimmed" means the core runtime plus only the wheels the baseline packages
actually need, resolved from Pyodide's own lockfile — numpy/pandas/matplotlib
plus jedi (which pulls in parso, for pre-run tooltips). That is about 32 MB
against roughly 400 MB for the full distribution.

    python3 dev/fetch_pyodide.py
"""

from __future__ import annotations

import argparse
import json
import shutil
import tarfile
import tempfile
import urllib.request
from pathlib import Path

PYODIDE_VERSION = "0.28.3"
RELEASE = (
    "https://github.com/pyodide/pyodide/releases/download/"
    "{v}/pyodide-{v}.tar.bz2"
)
BASELINE = ["numpy", "pandas", "matplotlib", "jedi"]  # parso comes along as jedi's own dependency
CORE = [
    "pyodide.js",
    "pyodide.mjs",
    "pyodide.asm.js",
    "pyodide.asm.wasm",
    "python_stdlib.zip",
    "pyodide-lock.json",
]


def resolve(lock: dict, roots: list[str]) -> set[str]:
    """Every package needed to load `roots`, following Pyodide's own depends.

    This is a breadth-first graph walk, written iteratively with a plain
    list (`pending`) as a stack rather than recursively: start with the
    packages the caller actually asked for (`roots`), and repeatedly take
    one out of `pending`, record it as `found`, and add whatever *it*
    depends on back onto `pending` to be processed in turn. `if name in
    found: continue` is what stops the same package being processed twice
    when two different packages both depend on it (numpy, say, needed by
    both pandas and matplotlib) — without that check, a package with many
    dependents could be re-walked many times, or the loop could even run
    forever if two packages depended on each other.
    """
    packages = lock["packages"]
    found: set[str] = set()
    pending = list(roots)
    while pending:
        name = pending.pop()
        if name in found or name not in packages:
            continue
        found.add(name)
        pending.extend(packages[name].get("depends", []))
    return found


def main() -> None:
    """The command-line entry point. Downloads the official Pyodide
    release archive to a temporary directory, works out exactly which
    package wheels are actually needed (via `resolve()` above), and
    copies only the core runtime files plus those wheels into `--out` —
    leaving the much larger full distribution behind in the temporary
    directory, which is cleaned up automatically once the `with
    tempfile.TemporaryDirectory()` block ends.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", default=PYODIDE_VERSION)
    parser.add_argument(
        "--packages", nargs="*", default=BASELINE,
        help="packages to keep, with their dependencies (default: the baseline three)",
    )
    parser.add_argument(
        "--out", type=Path, default=Path(__file__).resolve().parent / "pyodide",
    )
    args = parser.parse_args()

    url = RELEASE.format(v=args.version)
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        archive = tmp_path / "pyodide.tar.bz2"
        print(f"downloading {url}")
        urllib.request.urlretrieve(url, archive)  # noqa: S310 - fixed https URL

        print("extracting")
        with tarfile.open(archive) as tar:
            tar.extractall(tmp_path, filter="data")
        dist = tmp_path / "pyodide"

        lock = json.loads((dist / "pyodide-lock.json").read_text())
        wanted = resolve(lock, args.packages)

        if args.out.exists():
            shutil.rmtree(args.out)
        args.out.mkdir(parents=True)

        for name in CORE:
            shutil.copy2(dist / name, args.out / name)

        total = 0
        for name in sorted(wanted):
            wheel = lock["packages"][name]["file_name"]
            source = dist / wheel
            if source.exists():
                shutil.copy2(source, args.out / wheel)
                total += source.stat().st_size

    size = sum(f.stat().st_size for f in args.out.rglob("*") if f.is_file())
    print(
        f"{args.out}: {len(wanted)} packages "
        f"({total / 1e6:.1f} MB of wheels, {size / 1e6:.1f} MB total)"
    )


if __name__ == "__main__":
    main()
