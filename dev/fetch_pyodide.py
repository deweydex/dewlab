#!/usr/bin/env python3
"""Download a trimmed, self-hosted Pyodide into dev/pyodide/.

Two uses:

  * the e2e tests serve it, so they never depend on a CDN being reachable from
    wherever they run;
  * it is the escape hatch for OPEN_QUESTIONS.md 32 — if a school network turns
    out to block the CDN, this same directory is what gets committed under
    assets/ and pointed at with DEWLAB_PYODIDE_BASE.

"Trimmed" means the core runtime plus only the wheels the baseline packages
actually need, resolved from Pyodide's own lockfile. That is about 30 MB
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
BASELINE = ["numpy", "pandas", "matplotlib"]
CORE = [
    "pyodide.js",
    "pyodide.mjs",
    "pyodide.asm.js",
    "pyodide.asm.wasm",
    "python_stdlib.zip",
    "pyodide-lock.json",
]


def resolve(lock: dict, roots: list[str]) -> set[str]:
    """Every package needed to load `roots`, following Pyodide's own depends."""
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
