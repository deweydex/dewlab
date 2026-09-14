#!/usr/bin/env python3
"""Check your work before you open a pull request.

    python3 check.py                          check everything
    python3 check.py tutorials/my-tutorial    check one tutorial (and its practice page)
    python3 check.py courses/my-course.yaml   check one course

Every line of output says one thing, in plain words:

    OK       this is fine
    Problem  this will stop the build, or break a page — please fix it
    Note     nothing is broken, but you should know this

The program ends with 1 when there is at least one Problem, and 0 otherwise.
It needs only Python and PyYAML, and it does not build the site, so it runs
in a second. Moved to the repository root in refactor/PLAN.md step 2 and
described for contributors in docs/CHECK_YOUR_WORK.md.
"""
from __future__ import annotations

import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    print("Problem  PyYAML is not installed. Run:  pip install -r requirements-build.txt")
    sys.exit(1)

ROOT = Path(__file__).resolve().parent
if ROOT.name == "refactor":  # while this file still lives in refactor/
    ROOT = ROOT.parent
TUTORIALS = ROOT / "tutorials"
COURSES = ROOT / "courses"

ID_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
VERSION_RE = re.compile(r"^\d{4}\.\d{2}\.\d{2}\.\d+$")
FENCE_RE = re.compile(r"^```(\w+)[ \t]+exec[^\n]*\n(.*?)^```", re.M | re.S)
IMAGE_RE = re.compile(r"!\[[^\]]*\]\(([^)\s]+)\)|<img[^>]+src=\"([^\"]+)\"")
CODE_RE = re.compile(r"```.*?```|`[^`\n]*`", re.S)  # fences and code spans: examples, not images
OLD_FIELDS = ("module", "module_title", "series", "slug")


class Report:
    def __init__(self) -> None:
        self.lines: list[tuple[str, str]] = []

    def ok(self, text: str) -> None:
        self.lines.append(("OK", text))

    def problem(self, text: str) -> None:
        self.lines.append(("Problem", text))

    def note(self, text: str) -> None:
        self.lines.append(("Note", text))

    @property
    def problems(self) -> int:
        return sum(1 for kind, _ in self.lines if kind == "Problem")

    def show(self) -> None:
        for kind, text in self.lines:
            print(f"{kind:8} {text}")


# ----------------------------------------------------------------- reading

def split_frontmatter(text: str) -> tuple[dict | None, str, str | None]:
    """(fields, body, error). fields is None when there is no frontmatter."""
    if not text.startswith("---\n"):
        return None, text, "the file does not start with a --- line"
    end = text.find("\n---\n", 4)
    if end == -1:
        return None, text, "the frontmatter is never closed with a --- line"
    raw = text[4:end]
    try:
        fields = yaml.safe_load(raw) or {}
    except yaml.YAMLError as err:
        return None, text[end + 5:], f"the frontmatter is not valid YAML ({err})"
    if not isinstance(fields, dict):
        return None, text[end + 5:], "the frontmatter is not a list of `key: value` lines"
    return fields, text[end + 5:], None


def read_courses() -> dict[str, dict]:
    courses: dict[str, dict] = {}
    if not COURSES.is_dir():
        return courses
    for path in sorted(COURSES.glob("*.yaml")):
        if path.name in ("index.yaml", "redirects.yaml"):
            continue
        try:
            data = yaml.safe_load(path.read_text()) or {}
        except yaml.YAMLError as err:
            data = {"_error": str(err)}
        courses[path.stem] = data
    return courses


def listed_in(courses: dict[str, dict], ident: str) -> list[str]:
    where = []
    for course_id, course in courses.items():
        for series in course.get("contents") or []:
            if ident in (series.get("tutorials") or []):
                where.append(f"{course_id} → {series.get('title', '?')}")
        if ident in (course.get("mixed") or []):
            where.append(f"{course_id} → mixed problems")
    return where


def all_tutorial_ids() -> list[str]:
    if not TUTORIALS.is_dir():
        return []
    return sorted(p.name for p in TUTORIALS.iterdir() if p.is_dir() and any(p.glob("*.md")))


def is_practice_page(path: Path) -> bool:
    if not path.is_file():
        return False
    fields, _, _ = split_frontmatter(path.read_text())
    return bool(fields and "practice_for" in fields)


def title_of(folder: Path) -> str | None:
    main = folder / f"{folder.name}.md"
    if not main.is_file():
        return None
    fields, _, _ = split_frontmatter(main.read_text())
    return str(fields.get("title")) if fields and fields.get("title") else None


# ------------------------------------------------------------- one tutorial

def check_tutorial(folder: Path, courses: dict[str, dict], report: Report, titles: dict[str, list[str]]) -> None:
    ident = folder.name
    report.note(f"— {folder.relative_to(ROOT)} —")
    if not ID_RE.match(ident):
        report.problem(f"The folder name `{ident}` is not a valid id. Use small letters, digits and hyphens, like `first-steps`.")
    main = folder / f"{ident}.md"
    if not main.is_file():
        report.problem(f"There is no `{ident}.md` inside the folder. The main file must have the same name as the folder.")
        return
    report.ok(f"The main file `{ident}.md` is there.")

    text = main.read_text()
    fields, body, error = split_frontmatter(text)
    if error:
        report.problem(f"`{ident}.md`: {error}.")
        return
    assert fields is not None
    for key in ("title", "year", "version"):
        if not fields.get(key):
            report.problem(f"`{ident}.md`: the frontmatter needs `{key}:`.")
    if fields.get("version") and not VERSION_RE.match(str(fields["version"])):
        report.problem(f"`{ident}.md`: `version:` must look like `2026.09.14.1` (year.month.day.number).")
    old = [k for k in OLD_FIELDS if k in fields]
    if old:
        report.problem(f"`{ident}.md`: delete these old lines from the frontmatter: {', '.join(old)}. Where a tutorial sits is written in `courses/`, not here.")
    if not any(k in fields for k in OLD_FIELDS) and all(fields.get(k) for k in ("title", "year", "version")):
        report.ok("The frontmatter has title, year and version, and nothing about placement.")

    # cells
    ids: list[str] = []
    for match in FENCE_RE.finditer(body):
        header = match.group(2).split("\n", 1)[0]
        got = re.match(r"^id:\s*(\S+)", header)
        if not got:
            report.problem(f"`{ident}.md`: a `{match.group(1)} exec` cell has no `id:` line. Every cell needs one, as its first line.")
        else:
            ids.append(got.group(1))
    repeated = [cid for cid, n in Counter(ids).items() if n > 1]
    if repeated:
        report.problem(f"`{ident}.md`: these cell ids are used more than once: {', '.join(repeated)}. Each id must be unique on the page.")
    if ids and not repeated:
        report.ok(f"{len(ids)} cell{'s' if len(ids) != 1 else ''}, each with its own id.")
    elif not ids:
        report.note("No runnable cells in this tutorial. That is fine for a reading page.")

    # images — in the prose only; an <img> inside a code example is a lesson,
    # not a picture the page shows (the build makes the same distinction)
    for match in IMAGE_RE.finditer(CODE_RE.sub(" ", body)):
        src = match.group(1) or match.group(2)
        if src.startswith(("http://", "https://", "data:")):
            continue
        if not (folder / src).is_file():
            report.problem(f"`{ident}.md`: the image `{src}` is not in the folder.")

    # title collisions across the site
    title = str(fields.get("title") or "")
    others = [t for t in titles.get(title, []) if t != ident]
    if title and others:
        report.note(f"Another tutorial has the same title, \"{title}\": {', '.join(others)}. That is allowed, but check it is a different tutorial and not a copy.")

    # practice page
    practice = folder / f"{ident}-practice.md"
    if practice.is_file():
        pf, _, perr = split_frontmatter(practice.read_text())
        if perr:
            report.problem(f"`{practice.name}`: {perr}.")
        else:
            assert pf is not None
            target = pf.get("practice_for")
            if not target:
                report.problem(f"`{practice.name}`: a practice page needs `practice_for: {ident}` in its frontmatter.")
            elif target != ident:
                if not (TUTORIALS / str(target)).is_dir():
                    report.problem(f"`{practice.name}`: `practice_for: {target}` names a tutorial that does not exist.")
                else:
                    report.note(f"`{practice.name}` practises `{target}`, not `{ident}`. Is that what you meant?")
            else:
                report.ok(f"The practice page `{practice.name}` belongs to this tutorial.")
            if "covers" in pf:
                report.problem(f"`{practice.name}`: a practice page must not have `covers:`. Its tutorial says what is taught.")
            old = [k for k in OLD_FIELDS if k in pf]
            if old:
                report.problem(f"`{practice.name}`: delete these old lines: {', '.join(old)}.")
    else:
        report.note(f"No practice page. To add one, create `{ident}-practice.md` in this folder with `practice_for: {ident}`.")

    # glossary
    glossary = folder / f"{ident}.glossary.yaml"
    if glossary.is_file():
        try:
            data = yaml.safe_load(glossary.read_text()) or {}
            entries = data.get("entries") or []
            bad = [e for e in entries if not (isinstance(e, dict) and e.get("term") and e.get("definition"))]
            if bad:
                report.problem(f"`{glossary.name}`: {len(bad)} entr{'y' if len(bad) == 1 else 'ies'} without a `term:` or a `definition:`.")
            else:
                report.ok(f"The glossary has {len(entries)} entr{'y' if len(entries) == 1 else 'ies'}.")
        except yaml.YAMLError as err:
            report.problem(f"`{glossary.name}` is not valid YAML ({err}).")

    # where it is listed
    where = listed_in(courses, ident)
    if where:
        report.ok("Listed on: " + "; ".join(where) + ".")
    else:
        report.note(f"No course lists `{ident}` yet. The page will build, but nobody will find it from a course page. To list it, add `{ident}` to a `tutorials:` list in a file under `courses/`.")


# --------------------------------------------------------------- one course

def check_course(path: Path, courses: dict[str, dict], report: Report) -> None:
    course_id = path.stem
    report.note(f"— {path.relative_to(ROOT)} —")
    course = courses.get(course_id)
    if course is None:
        try:
            course = yaml.safe_load(path.read_text()) or {}
        except yaml.YAMLError as err:
            report.problem(f"The file is not valid YAML ({err}).")
            return
    if "_error" in course:
        report.problem(f"The file is not valid YAML ({course['_error']}).")
        return
    if not ID_RE.match(course_id):
        report.problem(f"The file name `{course_id}` is not a valid id. Use small letters, digits and hyphens.")
    for key in ("title", "contents"):
        if not course.get(key):
            report.problem(f"The course needs `{key}:`.")
    for key in ("code", "card", "description"):
        if not course.get(key):
            report.note(f"No `{key}:`. The course page or its card will be missing that text.")
    known = set(all_tutorial_ids())
    seen: Counter[str] = Counter()
    for n, series in enumerate(course.get("contents") or [], start=1):
        if not isinstance(series, dict) or not series.get("title"):
            report.problem(f"Series {n} needs a `title:`.")
            continue
        listed = series.get("tutorials") or []
        if not listed:
            report.problem(f"The series \"{series['title']}\" lists no tutorials.")
        for ident in listed:
            seen[ident] += 1
            if ident not in known:
                report.problem(f"The series \"{series['title']}\" lists `{ident}`, but there is no folder `tutorials/{ident}/`.")
            elif is_practice_page(TUTORIALS / ident / f"{ident}.md"):
                report.problem(f"`{ident}` is a practice page (it has `practice_for:`). Practice pages are not listed in courses; they follow their tutorial.")
    for ident, n in seen.items():
        if n > 1:
            report.problem(f"`{ident}` is listed {n} times in this course. List it once.")
    for ident in course.get("mixed") or []:
        folder = TUTORIALS / ident
        if not folder.is_dir():
            report.problem(f"`mixed:` names `{ident}`, but there is no folder `tutorials/{ident}/`.")
        else:
            fields, _, _ = split_frontmatter((folder / f"{ident}.md").read_text()) if (folder / f"{ident}.md").is_file() else (None, "", None)
            if not fields or "practice_across" not in fields:
                report.problem(f"`mixed:` names `{ident}`, which is not a mixed problem set (it has no `practice_across:`).")
    if not report.problems:
        total = sum(seen.values())
        report.ok(f"{len(course.get('contents') or [])} series, {total} tutorials, every id found.")
    index = COURSES / "index.yaml"
    if index.is_file():
        order = (yaml.safe_load(index.read_text()) or {}).get("order") or []
        if course_id in order:
            report.ok(f"Listed in `courses/index.yaml` at position {order.index(course_id) + 1}.")
        else:
            report.note(f"`courses/index.yaml` does not list `{course_id}`, so it will appear last. Add it where you want it.")
    else:
        report.note("There is no `courses/index.yaml`, so courses appear in alphabetical order.")


# -------------------------------------------------------------- everything

def check_everything(report: Report) -> None:
    courses = read_courses()
    ids = all_tutorial_ids()
    titles: dict[str, list[str]] = defaultdict(list)
    for ident in ids:
        title = title_of(TUTORIALS / ident)
        if title:
            titles[title].append(ident)
    for ident in ids:
        check_tutorial(TUTORIALS / ident, courses, report, titles)
    for course_id in courses:
        check_course(COURSES / f"{course_id}.yaml", courses, report)
    listed = {i for c in courses.values() for s in c.get("contents") or [] for i in s.get("tutorials") or []}
    unlisted = [i for i in ids if i not in listed and not i.endswith("-practice")
                and "practice_across" not in ((split_frontmatter((TUTORIALS / i / f"{i}.md").read_text())[0] or {}) if (TUTORIALS / i / f"{i}.md").is_file() else {})]
    report.note(f"— summary —")
    report.note(f"{len(ids)} tutorials, {len(courses)} courses, {len(unlisted)} tutorial{'s' if len(unlisted) != 1 else ''} on no course.")


def main(argv: list[str]) -> int:
    report = Report()
    if len(argv) <= 1:
        check_everything(report)
    else:
        courses = read_courses()
        ids = all_tutorial_ids()
        titles: dict[str, list[str]] = defaultdict(list)
        for ident in ids:
            title = title_of(TUTORIALS / ident)
            if title:
                titles[title].append(ident)
        for arg in argv[1:]:
            path = (ROOT / arg).resolve() if not Path(arg).is_absolute() else Path(arg)
            if path.is_dir() and path.parent == TUTORIALS:
                check_tutorial(path, courses, report, titles)
            elif path.is_file() and path.parent == COURSES and path.suffix == ".yaml":
                check_course(path, courses, report)
            elif path.is_file() and path.parent.parent == TUTORIALS:
                check_tutorial(path.parent, courses, report, titles)
            else:
                report.problem(f"I do not know how to check `{arg}`. Give a tutorial folder (tutorials/name) or a course file (courses/name.yaml).")
    report.show()
    print()
    if report.problems:
        print(f"{report.problems} problem{'s' if report.problems != 1 else ''} to fix.")
        return 1
    print("No problems. You can open a pull request.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
