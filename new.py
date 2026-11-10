#!/usr/bin/env python3
"""Start a new tutorial from the templates.

    python3 new.py my-tutorial "A title for it"
    python3 new.py my-tutorial "A title for it" --no-practice

Makes the folder tutorials/my-tutorial/ with two pages in it, copied from
docs/templates/: the tutorial, and its practice page. Each copy has your id,
your title, today's date as its version, and this school year. Everything
else is the template's, with its notes to you in <!-- --> comments: replace
the content, and delete each note when you have read it.

It changes nothing that already exists, and puts the page on no course.
docs/CHECK_YOUR_WORK.md says what to do next.
"""
from __future__ import annotations

import datetime
import re
import sys

try:
    import build as b
except ModuleNotFoundError:
    print("A package the build needs is not installed. Run:  pip install -r requirements-build.txt")
    sys.exit(1)

cfg = b.cfg
TEMPLATES = b.REPO / "docs" / "templates"
TUTORIAL, PRACTICE = "running-totals.md", "running-totals-practice.md"
ID_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def school_year(day: datetime.date) -> str:
    """The school year a day falls in, as the pages write it: "2026-2027"
    from August to the following July."""
    start = day.year if day.month >= 8 else day.year - 1
    return f"{start}-{start + 1}"


def first_version(day: datetime.date) -> str:
    return f"{day.year}.{day.month:02d}.{day.day:02d}.1"


def from_template(text: str, title: str, day: datetime.date, practice_for: str | None = None) -> str:
    """A template with its frontmatter and its heading made yours."""
    opening, frontmatter, body = text.split("---\n", 2)
    quoted = '"' + title.replace("\\", "\\\\").replace('"', '\\"') + '"'
    fields = {"title": quoted, "year": f'"{school_year(day)}"', "version": first_version(day)}
    if practice_for:
        fields["practice_for"] = practice_for
    for name, value in fields.items():
        frontmatter, found = re.subn(rf"^{name}:.*$", lambda _m: f"{name}: {value}", frontmatter, count=1, flags=re.M)
        if not found:
            frontmatter += f"{name}: {value}\n"
    body = re.sub(r"^# .*$", lambda _m: f"# {title}", body, count=1, flags=re.M)
    return f"{opening}---\n{frontmatter}---\n{body}"


def create(ident: str, title: str, practice: bool = True, day: datetime.date | None = None) -> list:
    """Write the pages and return their paths. Raises ValueError, with words
    for the person at the keyboard, when it should not go ahead."""
    day = day or datetime.date.today()
    if not ID_RE.match(ident):
        raise ValueError(f"`{ident}` cannot be an id. Use small letters, digits and hyphens, like `first-steps`. "
                         "The id is the web address and the name readers' work is saved under, so choose it once.")
    folder = cfg.TUTORIALS / ident
    if folder.exists():
        raise ValueError(f"tutorials/{ident} is already there. Choose another id, or edit that tutorial.")
    if not title.strip():
        raise ValueError("Give the tutorial a title, in quotes, after its id.")
    folder.mkdir(parents=True)
    written = []
    page = folder / f"{ident}.md"
    page.write_text(from_template((TEMPLATES / TUTORIAL).read_text(), title.strip(), day))
    written.append(page)
    if practice:
        page = folder / f"{ident}-practice.md"
        page.write_text(from_template((TEMPLATES / PRACTICE).read_text(), f"{title.strip()} — Practice", day,
                                      practice_for=ident))
        written.append(page)
    return written


def main(argv: list[str]) -> int:
    practice = "--no-practice" not in argv
    args = [a for a in argv[1:] if a != "--no-practice"]
    if len(args) != 2 or args[0].startswith("-"):
        print(__doc__.strip())
        return 1
    try:
        written = create(args[0], args[1], practice)
    except ValueError as problem:
        print(problem)
        return 1
    for path in written:
        print(f"Made {path.relative_to(cfg.ROOT)}")
    ident = args[0]
    print()
    print("They are copies of the Running totals templates, so they build and run as they are.")
    print("Next:")
    print("  1. Replace the content with yours. Delete each <!-- --> note when you have read it.")
    print(f"  2. python3 check.py tutorials/{ident}")
    print(f"  3. Add `{ident}` to a `tutorials:` list in a file under courses/, so a course page links to it.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
