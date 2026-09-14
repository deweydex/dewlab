#!/usr/bin/env python3
"""The document swap for refactor/DOCS.md §2: every edit as an exact
old-to-new replacement.

    python3 refactor/apply_docs.py --check    # every old passage present, once
    python3 refactor/apply_docs.py --apply    # make the edits

`--check` is the default and writes nothing. It fails, naming the file and
the first line of the passage, if any old text is missing or appears more
than once — which is what happens when a document has been edited since
this table was written, and the cue to update the table rather than run it.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# (file, old, new). Old must occur exactly once. Keep each entry small
# enough to read; a whole section is replaced only where the section
# changes whole.
EDITS: list[tuple[str, str, str]] = [
    # ---------------------------------------------------------------- CLAUDE.md
    ("CLAUDE.md",
     "set into it; `build.py` turns `tutorials/**/*.md` into `site/`, and the Python\n",
     "set into it; `build.py` turns `tutorials/*/*.md` and `courses/*.yaml` into\n"
     "`site/`, and the Python\n"),
    ("CLAUDE.md",
     "**Cell ids are a contract.** Once a tutorial has been in front of a class, a\n"
     "cell id is the key somebody's saved work lives under. Renaming one throws that\n"
     "work away.\n",
     "**Cell ids are a contract, and so is a tutorial's id.** Once a tutorial has\n"
     "been in front of a class, a cell id is the key somebody's saved work lives\n"
     "under, and the tutorial's id — its folder name — is the address of the page\n"
     "and the other half of that key. Renaming either throws that work away.\n"),

    # ----------------------------------------------------------- ARCHITECTURE.md
    ("ARCHITECTURE.md",
     "`build.py` is a single script that reads `tutorials/**/*.md` and writes\n",
     "`build.py` is a single script that reads `tutorials/*/*.md` and `courses/*.yaml`\n"
     "and writes\n"),
    ("ARCHITECTURE.md",
     "A tutorial is a folder, `tutorials/<module>/<slug>/`, holding its markdown at\n"
     "`<slug>.md`, its practice page,",
     "A tutorial is a folder, `tutorials/<id>/`, holding its markdown at\n"
     "`<id>.md`, its practice page,"),
    ("ARCHITECTURE.md",
     "   `archived_of()` read the `.order.yaml` files and each tutorial's\n"
     "   frontmatter to work out reading order, the current release, which\n"
     "   tutorial a practice page belongs to, and what's retired. A slug listed in\n"
     "   an order file with no tutorial behind it, or a series with no order file,\n"
     "   fails the build here rather than surfacing as a broken \"next\" link.\n",
     "   `archived_of()` read `courses/*.yaml` and each tutorial's frontmatter to\n"
     "   work out reading order, the current release, which tutorial a practice\n"
     "   page belongs to, and what's retired. An id listed in a course file with\n"
     "   no tutorial behind it fails the build here rather than surfacing as a\n"
     "   broken \"next\" link; a tutorial on no course builds, and is noted.\n"),
    ("ARCHITECTURE.md",
     "  student saved last (`localStorage`, keyed `dewlab:progress:<module>:<slug>`,\n",
     "  student saved last (`localStorage`, keyed `dewlab:progress:<id>`,\n"),
    ("ARCHITECTURE.md",
     "`.claude/skills/tutorial-glossary/SKILL.md`), walking each series in\n"
     "`<series>.order.yaml` order and, where a module's `series.yaml` says so\n"
     "(`series_chain()`), every earlier series in that module too — so a\n"
     "tutorial's manifest only ever carries what it and everything before it\n"
     "actually taught.\n",
     "`.claude/skills/tutorial-glossary/SKILL.md`), walking the series of the\n"
     "course the reader is following in the course file's order, and every\n"
     "earlier series of that course — so a tutorial's manifest only ever\n"
     "carries what it and everything before it on that course actually taught.\n"),

    # ------------------------------------------------- docs/WRITING_TUTORIALS.md
    ("docs/WRITING_TUTORIALS.md",
     "A tutorial is a folder, at `tutorials/<module>/<slug>/`, holding everything\n"
     "that belongs to it:\n"
     "\n"
     "```text\n"
     "tutorials/computational-methods/working-with-tables/\n",
     "A tutorial is a folder, at `tutorials/<id>/`, holding everything that\n"
     "belongs to it. The folder name is the tutorial's id: the address of its\n"
     "page, how other tutorials link to it, and the key its readers' saved work\n"
     "lives under. It is unique across the whole site and it never changes.\n"
     "\n"
     "```text\n"
     "tutorials/working-with-tables/\n"),
    ("docs/WRITING_TUTORIALS.md",
     "The tutorial itself is `<slug>.md`, and it opens with frontmatter, then\n"
     "ordinary prose and code.\n",
     "The tutorial itself is `<id>.md`, and it opens with frontmatter, then\n"
     "ordinary prose and code. Nothing in the file says which course or series\n"
     "it is in — that is written in `courses/`, described in the next section.\n"),
    ("docs/WRITING_TUTORIALS.md",
     "```markdown\n"
     "---\n"
     "title: \"Working With a Table\"\n"
     "slug: working-with-tables\n"
     "module: computational-methods\n"
     "module_title: \"Computational Methods\"\n"
     "year: \"2026-2027\"\n"
     "series: python-fundamentals\n"
     "version: 2026.08.24.1\n"
     "---\n"
     "```\n",
     "```markdown\n"
     "---\n"
     "title: \"Working With a Table\"\n"
     "year: \"2026-2027\"\n"
     "version: 2026.08.24.1\n"
     "---\n"
     "```\n"),
    ("docs/WRITING_TUTORIALS.md",
     "| `slug` | The filename of the built page, and how other tutorials link to this one. |\n"
     "| `module` | Which subject this belongs to. It is also the folder name. Any value you like — a new module is a new folder, not a code change. |\n"
     "| `module_title` | The readable name for the module, shown on the contents page. |\n"
     "| `year` | An academic year like `2026-2027`, since the programme is scoped a year at a time. |\n"
     "| `series` | Groups tutorials that are meant to be worked through in order. |\n",
     "| `year` | An academic year like `2026-2027`, since the programme is scoped a year at a time. |\n"),
    ("docs/WRITING_TUTORIALS.md",
     "## Where a tutorial sits in its series\n"
     "\n"
     "Not in the frontmatter. Each series has one file beside its tutorials listing\n"
     "them in reading order:\n"
     "\n"
     "```yaml\n"
     "# tutorials/computational-methods/python-fundamentals.order.yaml\n"
     "series: Python fundamentals\n"
     "order:\n"
     "  - first-steps\n"
     "  - working-with-tables\n"
     "```\n"
     "\n"
     "Moving a tutorial is moving a line, and inserting one is adding a line. Nothing\n"
     "else changes: no renumbering, no editing every file after it. That is the whole\n"
     "reason reading order is not a field on each tutorial.\n"
     "\n"
     "The build checks it both ways. A tutorial the file forgets stops the build, and\n"
     "so does a slug with no tutorial behind it. The second check is the one worth\n"
     "having, because a file that looks complete beside a series that is quietly short\n"
     "is a mistake nobody notices.\n"
     "\n"
     "Slugs are unique within a module, not across the site — the built path already\n"
     "carries the module, so two modules may each have a `first-steps`. A `tutorial:`\n"
     "link looks in its own module first.\n"
     "\n"
     "A series may also list a tutorial that lives in another module, written as\n"
     "`module/slug`:\n"
     "\n"
     "```yaml\n"
     "# tutorials/programming-design-principles/programming-foundations.order.yaml\n"
     "series: Programming Foundations\n"
     "order:\n"
     "  - mit-pdp-maths-prog-integration/first-steps\n"
     "  - mit-pdp-maths-prog-integration/storing-and-computing\n"
     "```\n"
     "\n"
     "That is how one module offers a route through tutorials another module owns —\n"
     "Programming and Design Principles is the programming half of the integrated\n"
     "course, read on its own — without a second copy of any file. The tutorial keeps\n"
     "its one page, its one URL, its own module in the tree and its own previous and\n"
     "next; it simply appears in this series' list and downloads as well. A module\n"
     "made only of borrowed tutorials has no frontmatter to take its title from, so\n"
     "its title lives in `MODULE_INFO` in `build.py`, with its code and description.\n",
     "## Where a tutorial sits: courses and series\n"
     "\n"
     "Not in the tutorial. A course (what the site calls a module) is one file under\n"
     "`courses/`, and a series is a heading in it with the tutorials listed in\n"
     "reading order:\n"
     "\n"
     "```yaml\n"
     "# courses/computational-methods.yaml\n"
     "title: Computational Methods and Problem Solving\n"
     "code: 5N0554 · QQI Level 5\n"
     "status: beta\n"
     "card: |\n"
     "  We work through matrices, simulation, algorithms and debugging, in Python.\n"
     "description: |\n"
     "  This module is Computational Methods and Problem Solving (5N0554). …\n"
     "contents:\n"
     "  - title: Python fundamentals\n"
     "    tutorials: [first-steps-cm, working-with-tables]\n"
     "  - title: Matrices\n"
     "    tutorials: [grid-of-numbers, multiplying-grids, what-a-matrix-does-to-a-picture]\n"
     "```\n"
     "\n"
     "To put a tutorial on a course, add its id to a list. To move it, move the\n"
     "line. To take it off, remove the line; the tutorial still builds at its own\n"
     "address, and the build notes that nothing lists it. The same tutorial may be\n"
     "listed in as many courses as want it — Programming and Design Principles is\n"
     "the programming half of the integrated course, read on its own, and its\n"
     "course file simply lists the same ids. The tutorial keeps its one page and\n"
     "its one address; a reader following either course sees that course's tree\n"
     "and previous and next.\n"
     "\n"
     "The build refuses an id it cannot find, naming the course file and the line,\n"
     "and refuses a second folder with an id that already exists, naming the\n"
     "tutorial that has it. It warns, without stopping, when two tutorials share a\n"
     "title, and when two tutorials cover much the same outcomes — both are worth\n"
     "a look, neither is necessarily wrong.\n"
     "\n"
     "`courses/index.yaml` lists the courses in the order they appear on the front\n"
     "page and the contents page. A course's card on the front page is generated\n"
     "from its `card:` text; nothing is written by hand in `pages/home.md`.\n"),
    ("docs/WRITING_TUTORIALS.md",
     "```yaml\n"
     "title: \"A Grid of Numbers — Practice\"\n"
     "slug: grid-of-numbers-practice\n"
     "practice_for: grid-of-numbers\n"
     "module: computational-methods\n"
     "module_title: \"Computational Methods\"\n"
     "year: \"2026-2027\"\n"
     "series: matrices\n"
     "version: 2026.08.24.1\n"
     "```\n",
     "```yaml\n"
     "title: \"A Grid of Numbers — Practice\"\n"
     "practice_for: grid-of-numbers\n"
     "year: \"2026-2027\"\n"
     "version: 2026.08.24.1\n"
     "```\n"
     "\n"
     "A practice page is never listed in a course file: it follows its tutorial onto\n"
     "every course that lists it.\n"),
    ("docs/WRITING_TUTORIALS.md",
     "A **mixed problem set** draws on several tutorials at once, declared with\n"
     "`practice_across:` instead:\n",
     "A **mixed problem set** draws on several tutorials at once, declared with\n"
     "`practice_across:` instead, and listed in the course file under `mixed:` so\n"
     "the course page knows to show it:\n"),
    ("docs/WRITING_TUTORIALS.md",
     "`<slug>/v<version>.html`, frozen as it was.",
     "`<id>/v<version>.html`, frozen as it was."),
    ("docs/WRITING_TUTORIALS.md",
     "## Adding a new module\n"
     "\n"
     "Make a folder under `tutorials/` and put tutorials in it whose `module` field\n"
     "matches the folder name. That is the whole procedure. Nothing keeps a list of\n"
     "modules that needs updating.\n",
     "## Adding a new module\n"
     "\n"
     "A module is a course file. Create `courses/<id>.yaml` with a `title`, a\n"
     "`code`, a `status`, the `card` text for the front page, a `description` for\n"
     "the course's own page, and `contents` — its series, each with its tutorials\n"
     "in order — then add the id to `courses/index.yaml` where it should appear.\n"
     "That is the whole procedure: nothing in `build.py`, nothing in any tutorial.\n"
     "The tutorials it lists may already be on another course.\n"),
    ("docs/WRITING_TUTORIALS.md",
     "every tutorial by title, slug or module and inserts a real link at the cursor,\n",
     "every tutorial by title, id or course and inserts a real link at the cursor,\n"),

    # ------------------------------------------ docs/tutorial-runtime-explained.md
    ("docs/tutorial-runtime-explained.md",
     "(`dewlab:custom-cells:<module>:<slug>`), and its own save/restore\n",
     "(`dewlab:custom-cells:<id>`), and its own save/restore\n"),

    # ---------------------------------------------- planning/REFERENCE_PANEL.md
    ("planning/REFERENCE_PANEL.md",
     "(2) already exists: `<series>.order.yaml`'s `order:` list, the same one `nav_for()`\n"
     "uses for previous/next navigation.",
     "(2) already exists: the course file's series lists under `courses/`, the same\n"
     "ones `nav_for()` uses for previous/next navigation."),
    ("planning/REFERENCE_PANEL.md",
     "`<series>.order.yaml` gives exactly that, but only within one series. Series\n"
     "within a module have no defined order relative to each other by default\n"
     "(`write_index` lists them `sorted()` by name — alphabetical, not curricular,\n"
     "and unrelated to this ordering) — but a module may add\n"
     "`tutorials/<module>/series.yaml` (`order:`, a list of series slugs) to state\n"
     "its own curricular order, purely for reference purposes.\n"
     "\n"
     "**A reference draws from the current series, up to and including the\n"
     "current tutorial's own position, plus every earlier series `series.yaml`\n"
     "lists before this one** (`series_chain()`, `DECISIONS_LOG.md` 7.66) — never\n"
     "from another module. `tutorials/computational-methods/series.yaml` lists\n"
     "`python-fundamentals` before `matrices`, so matrices' reference does\n"
     "include what fundamentals introduced. A series left off the list — or a\n"
     "module with no `series.yaml` at all — gets series-only accumulation. That's\n"
     "what a series with no fixed curricular position needs: `reflections-and-review`,\n"
     "in `mit-pdp-maths-prog-integration`, is revisited whenever a reader wants\n"
     "rather than sitting at one point in the course (that series' own\n"
     "`.order.yaml` says so), so it is never listed anywhere.\n",
     "A course file gives exactly that: its series in curricular order, and each\n"
     "series' tutorials in reading order.\n"
     "\n"
     "**A reference draws from the current series, up to and including the\n"
     "current tutorial's own position, plus every earlier series of the course the\n"
     "reader is following** (`DECISIONS_LOG.md` 7.66, then 7.172) — never from a\n"
     "course they are not on. `courses/computational-methods.yaml` lists Python\n"
     "fundamentals before Matrices, so a matrices tutorial's reference includes\n"
     "what fundamentals introduced. A tutorial on two courses accumulates along\n"
     "whichever course the reader has chosen (the tree's course rung is the\n"
     "switch), and the page is built with the first course's accumulation so it is\n"
     "right before any script runs. `reflections-and-review`, in the integrated\n"
     "course, is revisited whenever a reader wants rather than sitting at one point\n"
     "in the course; it is listed last in that course file, which gives it the\n"
     "whole course's vocabulary and disturbs nothing before it.\n"),
    ("planning/REFERENCE_PANEL.md",
     "`practice_across` name the tutorial(s) it tests instead of appearing in\n"
     "`<series>.order.yaml`'s narrative position.",
     "`practice_across` name the tutorial(s) it tests instead of appearing in\n"
     "a course file's series list."),
    ("planning/REFERENCE_PANEL.md",
     "A new sibling file, `tutorials/<module>/<slug>.glossary.yaml` — beside the\n",
     "A new sibling file, `tutorials/<id>/<id>.glossary.yaml` — beside the\n"),
    ("planning/REFERENCE_PANEL.md",
     "# tutorials/computational-methods/what-a-matrix-does-to-a-picture.glossary.yaml\n",
     "# tutorials/what-a-matrix-does-to-a-picture/what-a-matrix-does-to-a-picture.glossary.yaml\n"),
    ("planning/REFERENCE_PANEL.md",
     "`build.py`, per series, in `<series>.order.yaml` order:\n",
     "`build.py`, per course, series by series in the course file's order:\n"),

    # ------------------------------------------------------------- the skills
    (".claude/skills/cell-code-review/SKILL.md",
     "1. **The tutorial itself**, read whole — `tutorials/<module>/<slug>.md` or\n"
     "   `tutorials/<module>/<slug>/<slug>.md` for a tutorial with releases. Not\n",
     "1. **The tutorial itself**, read whole — `tutorials/<id>/<id>.md`. Not\n"),
    (".claude/skills/triage-report/SKILL.md",
     "2. **The page it names, at the version it names** — `tutorials/<module>/<slug>/<slug>.md`\n",
     "2. **The page it names, at the version it names** — `tutorials/<id>/<id>.md`\n"),
    (".claude/skills/tutorial-glossary/SKILL.md",
     "1. **The tutorial itself** — `tutorials/<module>/<slug>.md`, or\n"
     "   `tutorials/<module>/<slug>/<slug>.md` if it has releases (read the\n",
     "1. **The tutorial itself** — `tutorials/<id>/<id>.md` (read the\n"),
    (".claude/skills/tutorial-glossary/SKILL.md",
     "`tutorials/<module>/<slug>.glossary.yaml`:\n",
     "`tutorials/<id>/<id>.glossary.yaml`:\n"),
]

HOME_CARDS_START = "```card\nurl: mit-pdp-maths-prog-integration.html\n"
HOME_CARDS_END = "```card\nurl: all-tutorials.html\n"


def swap_home_cards(text: str) -> str:
    """The six course-card fences in pages/home.md become one generated
    block; the two other cards on the page stay."""
    start = text.find(HOME_CARDS_START)
    end = text.find(HOME_CARDS_END)
    if start == -1 or end == -1 or end < start:
        raise SystemExit("pages/home.md: the course cards are not where this script expects them")
    return text[:start] + "[[course-cards]]\n\n" + text[end:]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--apply", action="store_true", help="make the edits; without it, only check")
    parser.add_argument("--check", action="store_true", help="the default: verify every old passage, write nothing")
    args = parser.parse_args()

    problems: list[str] = []
    texts: dict[str, str] = {}
    for file, old, new in EDITS:
        path = ROOT / file
        if file not in texts:
            if not path.is_file():
                problems.append(f"{file}: missing")
                continue
            texts[file] = path.read_text()
        count = texts[file].count(old)
        if count != 1:
            first = old.strip().split("\n")[0]
            problems.append(f"{file}: expected once, found {count}: {first!r}")
            continue
        texts[file] = texts[file].replace(old, new)
    home = ROOT / "pages" / "home.md"
    home_text = home.read_text()
    if HOME_CARDS_START not in home_text or HOME_CARDS_END not in home_text:
        problems.append("pages/home.md: course cards not found")

    if problems:
        print("\n".join(problems), file=sys.stderr)
        sys.exit(1)
    print(f"{len(EDITS)} edits across {len(texts)} files, plus the course cards in pages/home.md: all found.")
    if not args.apply:
        print("check only: nothing written. Add --apply to write.")
        return
    for file, text in texts.items():
        (ROOT / file).write_text(text)
    home.write_text(swap_home_cards(home_text))
    print("applied.")


if __name__ == "__main__":
    main()
