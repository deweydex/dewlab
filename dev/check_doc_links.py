#!/usr/bin/env python3
"""Check that the repository's own documentation does not point at files that
are not there.

The build already refuses to publish a tutorial whose `tutorial:` link goes
nowhere, on the grounds that a dead link is a bug rather than a warning. This
applies the same standard to the documents *about* the project — README,
ARCHITECTURE, CONTRIBUTING, CLAUDE.md, the skills in `.claude/skills/`, and
everything in `docs/` and `planning/` — which
had no such check and had drifted accordingly: renamed files still cited by
their old paths, retired documents cited as though current, a planning index
that had fallen behind the directory it indexes.

What it checks, and deliberately nothing more:

- **Relative links to files in the repository.** `[text](../build.py)`,
  `[text](./EXERCISES.md#section)`, and bare paths in link position. A link
  to a file that does not exist fails.
- **Inline code spans that name a repository path.** `` `planning/EXERCISES.md` ``
  is how these documents usually refer to each other — far more often than
  through a markdown link — so a checker that only read links would have
  missed most of the drift it exists to catch. A backticked path is only
  treated as a claim about a file when it looks like one: it has a directory
  separator or a known extension, and no spaces.

- **Citations of the two writing guides.** `planning/PEDAGOGICAL_STYLE_GUIDE.md`
  and `docs/WRITING_TUTORIALS.md` are cited from code comments, tests, skills
  and planning documents, by anchor: `PEDAGOGICAL_STYLE_GUIDE.md#voice`. Every
  such anchor, in every file in the repository, has to exist in the guide it
  names, as an `<a id>` or a heading. A citation of the style guide by section
  number fails outright. The guide used to be cited that way, and a number
  goes stale silently the first time a section moves: one entry in
  `DECISIONS_LOG.md` cited a section eleven that never existed.

What it does not check: external URLs (that needs the network, and a link rot
check is a different job with a different failure mode), anchors in any other
document, and prose that merely mentions a filename without marking it as a
path.

    python3 dev/check_doc_links.py

Prints one line per problem and exits 1 if there are any, so CI can run it the
same way it runs `curriculum_map.py --check`.
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

DOC_ROOTS = ("docs", "planning", ".github", ".claude/skills")
DOC_FILES = ("README.md", "ARCHITECTURE.md", "CONTRIBUTING.md", "LICENSE.md",
             "CLAUDE.md")

HISTORY = {
    "DECISIONS_LOG.md",
    "QUESTIONS.md",
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

GENERATED_PAGES = {"index.html", "tree.html", "topics.html", "about.html",
                   "editor.html", "all-notes.html", "search-index.json",
                   "reference-index.json", "routes.json"}

# Docs in these folders aren't held to link currency: generated or
# per-module content, not architecture prose. A link from an active doc
# into either is still checked — only a stale link *within* one of these
# goes unnoticed.
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
    first = target.strip("/").split("/")[0]
    if first and not (ROOT / first).exists():
        return None
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


# The two guides whose anchors are checked wherever they are cited. A
# citation names the file, not its folder: `PEDAGOGICAL_STYLE_GUIDE.md#voice`.
ANCHORED = {
    "PEDAGOGICAL_STYLE_GUIDE.md": ROOT / "planning" / "PEDAGOGICAL_STYLE_GUIDE.md",
    "WRITING_TUTORIALS.md": ROOT / "docs" / "WRITING_TUTORIALS.md",
}
ANCHOR_CITE_RE = re.compile(
    r"\b(" + "|".join(re.escape(name) for name in ANCHORED) + r")#([\w-]+)")
# `(#stuck)` inside one of the guides: a link to its own section.
SELF_LINK_RE = re.compile(r"\]\(#([\w-]+)\)")
HTML_ID_RE = re.compile(r'<a id="([^"]+)"')
HEADING_RE = re.compile(r"^#{1,6}\s+(.+?)\s*$", re.M)
# A fenced example: a `# comment` inside one is not a heading.
FENCE_RE = re.compile(r"^(```+|~~~+).*?^\1\s*$", re.M | re.S)

# The style guide cited by number: its file name, or the words "style
# guide", followed by a section sign or the word "section" and a digit; a
# section sign and a number followed by "of" and the guide; or an old
# numbered heading's slug after the file name. Backticks, a closing bracket
# or a possessive may sit between the name and the number.
NUMBERED_CITE_RE = re.compile(
    r"PEDAGOGICAL_STYLE_GUIDE\.md(?:#\d|[`')\]]*(?:'s)?,?\s*(?:§\s*\d|section\s+\d))"
    r"|style\s+guide(?:'s)?,?\s+(?:§\s*\d|section\s+\d)"
    r"|§\s*\d+\s+of\s+(?:the\s+style\s+guide|`?PEDAGOGICAL_STYLE_GUIDE)",
    re.I,
)

# Every file a citation could sit in. The vendored and generated trees are
# skipped: nothing in them is written by hand.
CITING_SUFFIXES = {".md", ".py", ".yaml", ".yml", ".js", ".mjs", ".txt",
                   ".html", ".css", ".toml"}
NOT_CITING = GENERATED + ("assets/vendor/", ".git/", ".pytest_cache/")


def slug(heading: str) -> str:
    """A heading's anchor, the way GitHub makes one."""
    text = re.sub(r"<[^>]+>|[`*_]", "", heading).strip().lower()
    return re.sub(r"[^\w\- ]", "", text).replace(" ", "-")


def anchors_of(path: Path) -> set[str]:
    text = path.read_text()
    return set(HTML_ID_RE.findall(text)) | {
        slug(h) for h in HEADING_RE.findall(FENCE_RE.sub("", text))}


def skipped(folder: str) -> bool:
    return any(folder.startswith(skip) or f"/{skip}" in folder
               for skip in NOT_CITING)


def citing_files() -> list[Path]:
    found = []
    for folder, subfolders, names in os.walk(ROOT):
        here = Path(folder)
        # Pruned in place, so a skipped tree is never walked at all.
        subfolders[:] = sorted(
            name for name in subfolders
            if not skipped((here / name).relative_to(ROOT).as_posix() + "/"))
        found += [here / name for name in sorted(names)
                  if Path(name).suffix.lower() in CITING_SUFFIXES]
    return found


def citation_problems(files: list[Path] | None = None,
                      guides: dict[str, Path] | None = None) -> list[str]:
    """Guide anchors that do not exist, and style-guide section numbers."""
    guides = ANCHORED if guides is None else guides
    anchors = {name: anchors_of(path) for name, path in guides.items()}
    found: list[str] = []
    for path in citing_files() if files is None else files:
        try:
            text = path.read_text()
        except UnicodeDecodeError:
            continue
        own = next((name for name, guide in guides.items()
                    if guide.resolve() == path.resolve()), None)
        where = path.relative_to(ROOT) if path.is_relative_to(ROOT) else path
        for number, line in enumerate(text.splitlines(), start=1):
            cited = ANCHOR_CITE_RE.findall(line)
            if own:
                cited += [(own, a) for a in SELF_LINK_RE.findall(line)]
            for name, anchor in cited:
                if name in anchors and anchor not in anchors[name]:
                    found.append(f"{where}:{number}: cites {name}#{anchor}, "
                                 f"and {name} has no such anchor")
        # Over the whole text, not line by line: a wrapped line can put the
        # guide's name at the end of one line and the number on the next.
        for match in NUMBERED_CITE_RE.finditer(text):
            number = text.count("\n", 0, match.start()) + 1
            found.append(f"{where}:{number}: cites the style guide by "
                         "section number; cite its anchor instead, as "
                         "PEDAGOGICAL_STYLE_GUIDE.md#voice")
    return found


def main() -> int:
    found = [problem for doc in documents() for problem in problems_in(doc)]
    found += citation_problems()
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
