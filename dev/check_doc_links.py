#!/usr/bin/env python3
"""Check that the repository's own documentation does not point at files that
are not there.

The build already refuses to publish a tutorial whose `tutorial:` link goes
nowhere, on the grounds that a dead link is a bug rather than a warning. This
applies the same standard to the documents *about* the project — README,
ARCHITECTURE, CONTRIBUTING, and everything in `docs/` and `planning/` — which
had no such check and had drifted accordingly: renamed files still cited by
their old paths, retired documents cited as though current, a planning index
that had fallen behind the directory it indexes.

What it checks, and deliberately nothing more:

- **Relative links to files in the repository.** `[text](../build.py)`,
  `[text](./STATUS.md#section)`, and bare paths in link position. A link to a
  file that does not exist fails.
- **Inline code spans that name a repository path.** `` `planning/STATUS.md` ``
  is how these documents usually refer to each other — far more often than
  through a markdown link — so a checker that only read links would have
  missed most of the drift it exists to catch. A backticked path is only
  treated as a claim about a file when it looks like one: it has a directory
  separator or a known extension, and no spaces.

What it does not check: external URLs (that needs the network, and a link rot
check is a different job with a different failure mode), anchors within a
file, and prose that merely mentions a filename without marking it as a path.

    python3 dev/check_doc_links.py

Prints one line per problem and exits 1 if there are any, so CI can run it the
same way it runs `curriculum_map.py --check`.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# The documents this governs. Tutorials are left out on purpose: their links
# are `tutorial:slug` references that build.py already resolves and validates,
# and they are checked far more strictly there than anything here could manage.
DOC_ROOTS = ("docs", "planning", ".github")
DOC_FILES = ("README.md", "ARCHITECTURE.md", "CONTRIBUTING.md", "LICENSE.md")

# Records of what was decided *then*, as against descriptions of how things are
# *now*. A decision-log entry naming `planning/CHEAT_SHEETS.md` is not stale —
# that was the file's name when the entry was written, and rewriting it to the
# current name would make the record say something that was never true. Only
# documents that claim to describe the present are held to the present.
HISTORY = {
    "DECISIONS_LOG.md",
    "QUESTIONS.md",
    "planning/VERSIONING_AND_PROGRESS.md",   # superseded; says so at the top
    "planning/WHAT_IS_LEFT_TO_WRITE.md",     # retired; says so in its title
    "planning/DOCS_AND_COMMENTS_PASS.md",    # the record of a finished pass
    "planning/MINI_IDE_REDESIGN.md",         # a shipped plan, phase by phase
    "planning/BUILD_PLAN.md",                # likewise
}

# [text](target) — the target only, and only up to a # or a space.
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s#]+)")

# `some/path.md` — a backticked span with no spaces in it.
CODE_RE = re.compile(r"`([^`\s]+)`")

# Extensions that make a backticked span a claim about a file. A span like
# `numpy` or `--check` is not a path and must not be read as one.
PATH_SUFFIXES = {".md", ".py", ".js", ".css", ".html", ".yaml", ".yml",
                 ".json", ".txt", ".csv", ".ipynb", ".mjs", ".jsonc", ".toml"}

# Paths that are real and deliberately absent from a clean checkout: build
# output, fetched runtimes, and the like. Each is gitignored.
GENERATED = ("site/", "dev/pyodide/", "assets/vendor/pyodide/",
             "node_modules/", "__pycache__/")

# Pages build.py writes rather than files anyone edits. A document naming one
# is describing the built site, which is exactly where they do exist.
GENERATED_PAGES = {"index.html", "tree.html", "topics.html", "about.html",
                   "editor.html"}

# Documents whose subject is material in another repository: the QQI module
# descriptors in `deweydex/everlearning` and the worksheets in
# `deweydex/Mathematics`. They name files by their real names, which are simply
# not names in this repository.
ELSEWHERE = ("planning/curriculum/", "planning/outlines/")

# Referred to by name in prose about other projects, or as a shape rather than
# a file: `<slug>.md` is a pattern, not a path.
PLACEHOLDER_RE = re.compile(r"[<>{}*]")


def is_generated(target: str) -> bool:
    return any(target.startswith(prefix) or f"/{prefix}" in target
               for prefix in GENERATED)


def looks_like_a_path(span: str) -> bool:
    """Whether a backticked span is claiming a file exists.

    Conservative on purpose. A false positive here is a build failure over a
    word in a sentence, which would teach people to distrust the check; a
    false negative is one stale reference that stays stale.
    """
    if PLACEHOLDER_RE.search(span) or span.startswith(("http", "#", "-")):
        return False
    # A naming convention rather than a file: `.order.yaml` and `.glossary.yaml`
    # describe what a file is called, not one that exists. A real dotted path
    # (`.github/workflows/tests.yml`) has a separator and is kept.
    if span.startswith(".") and "/" not in span:
        return False
    suffix = Path(span).suffix.lower()
    if suffix in PATH_SUFFIXES:
        return True
    # A directory, written with a trailing slash: `planning/outlines/`.
    return span.endswith("/") and "/" in span.rstrip("/")


_BASENAMES: set[str] | None = None


def known_basenames() -> set[str]:
    """Every filename in the repository, ignoring where it sits.

    These documents refer to a file by its bare name far more often than by
    its path — `tutorial_tools.py`, not `assets/tutorial_tools.py` — and a
    reader is expected to know where it lives. Checking those by name is still
    worth doing: it is what catches a file that was renamed or deleted, which
    is the drift this exists for. Checking them by *path* would only flag the
    house style.
    """
    global _BASENAMES
    if _BASENAMES is None:
        _BASENAMES = {
            path.name for path in ROOT.rglob("*")
            if path.is_file()
            and not is_generated(str(path.relative_to(ROOT)))
            and ".git/" not in str(path.relative_to(ROOT))
        }
    return _BASENAMES


def resolve(doc: Path, target: str) -> Path | None:
    """Where a reference points, or None if it is not ours to check."""
    if target.startswith(("http://", "https://", "mailto:", "tutorial:",
                          "topic:", "//")):
        return None
    if is_generated(target):
        return None
    # A page the build writes rather than a file anyone edits, named by URL:
    # `/editor.html`.
    if Path(target).name in GENERATED_PAGES:
        return None
    # A path into another repository — `deweydex/Mathematics/...`,
    # `PDP_MIT_2026_2027_Integrated/...` — which `planning/EXERCISES.md` and the
    # curriculum notes both draw from. Recognised by its first segment naming
    # nothing at the root of this one, which is what makes it a claim about
    # somewhere else rather than a stale claim about here.
    first = target.strip("/").split("/")[0]
    if first and not (ROOT / first).exists():
        return None
    # Repository-relative (`planning/STATUS.md`) or document-relative
    # (`./STATUS.md`, `../build.py`). Try the document's own directory first,
    # since that is what a markdown link means, then the repository root,
    # which is how a backticked path is nearly always written.
    # Written from the repository root, as a layout diagram does: `/tutorials/`.
    if target.startswith("/"):
        return (ROOT / target.lstrip("/")).resolve()
    if target.startswith(("./", "../")):
        return (doc.parent / target).resolve()
    from_doc = (doc.parent / target).resolve()
    if from_doc.exists():
        return from_doc
    return (ROOT / target).resolve()


def documents() -> list[Path]:
    found = [ROOT / name for name in DOC_FILES if (ROOT / name).is_file()]
    for folder in DOC_ROOTS:
        found.extend(sorted((ROOT / folder).rglob("*.md")))
    return [doc for doc in found
            if str(doc.relative_to(ROOT)) not in HISTORY]


def problems_in(doc: Path) -> list[str]:
    found: list[str] = []
    elsewhere = str(doc.relative_to(ROOT)).startswith(ELSEWHERE)
    for number, line in enumerate(doc.read_text().splitlines(), start=1):
        # A link target is only checked when it looks like a file or a folder.
        # `![alt](path)` in a document explaining markdown syntax is an
        # illustration, not a claim that a file called "path" exists.
        targets = [(t, "link") for t in LINK_RE.findall(line)
                   if "/" in t or Path(t).suffix.lower() in PATH_SUFFIXES]
        targets += [(t, "path") for t in CODE_RE.findall(line)
                    if looks_like_a_path(t)]
        for target, kind in targets:
            # A bare filename in a code span is a name, not a location: it is
            # checked for existing at all, anywhere.
            if kind == "path" and "/" not in target:
                if target in GENERATED_PAGES or elsewhere:
                    continue
                if target not in known_basenames():
                    found.append(
                        f"{doc.relative_to(ROOT)}:{number}: names {target!r}, "
                        "and no such file is in the repository"
                    )
                continue
            if elsewhere:
                continue
            resolved = resolve(doc, target)
            if resolved is None or resolved.exists():
                continue
            found.append(
                f"{doc.relative_to(ROOT)}:{number}: {kind} to {target!r}, "
                "which is not in the repository"
            )
    return found


def main() -> int:
    found = [problem for doc in documents() for problem in problems_in(doc)]
    for problem in found:
        print(problem)
    if found:
        print(f"\n{len(found)} stale reference(s). Either the path moved and "
              "the document did not, or the document is describing something "
              "that no longer exists.")
        return 1
    print(f"{len(documents())} documents, no stale references.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
