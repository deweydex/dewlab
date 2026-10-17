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
It reads each page with the build's own code, so a Problem is exactly what the
build would refuse, in its own words, and a Note is something it would carry on
despite. It writes nothing and does not build the site: a tutorial takes a
second or two, the whole site about half a minute. It needs what the build
needs (pip install -r requirements-build.txt). docs/CHECK_YOUR_WORK.md
describes it for contributors.

When there are no problems it offers to open a pull request: it commits
and pushes the files it checked (after asking), then opens GitHub's own
"new pull request" page with the title and description already written
from what was checked. `--pr` does that without asking; `--no-pr` never
asks. Nothing is sent anywhere except by `git push`, and the pull request
itself is created by the person, on GitHub, when they press the button.
"""
from __future__ import annotations

import re
import subprocess
import sys
import urllib.parse
import webbrowser
from collections import defaultdict
from pathlib import Path

try:
    import yaml

    import build as b
except ImportError:  # pragma: no cover
    print("Problem  A package the build needs is not installed. Run:  pip install -r requirements-build.txt")
    sys.exit(1)

ROOT = Path(__file__).resolve().parent
TUTORIALS = ROOT / "tutorials"
COURSES = ROOT / "courses"

ID_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


class Report:
    def __init__(self) -> None:
        self.lines: list[tuple[str, str]] = []
        self.checked: list[tuple[str, str, str]] = []  # (kind, id, title) — for the pull request

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


# ------------------------------------------------------ the build's own rules
#
# Whether a page is acceptable is the build's decision, not this file's. A
# page is read by the same code the build reads it with: what the build
# refuses is a Problem here, in its own words, and what it carries on despite
# is a Note. There is no second copy of a rule to keep in step with the first
# (DECISIONS_LOG 7.301).

def from_build(report: Report, function, *args):
    """Run part of the build. Its refusal is a Problem and the call returns
    None; what it noted along the way is a Note either way."""
    try:
        return function(*args)
    except b.BuildError as error:
        report.problem(str(error))
        return None
    finally:
        for line in b._NOTE_LINES:
            report.note(line.removeprefix("note: "))
        b._NOTE_LINES.clear()


def read_page(path: Path):
    """One page, read as the build reads it, with the per-page checks the
    build runs after reading: folds, datasets, pictures."""
    page = b.load_page(path, mapped=False)
    b.check_folds(page)
    b.check_datasets(page)
    b.resolve_assets(page, page.body_html)
    return page


def fields_of(path: Path) -> dict:
    """A page's frontmatter, or {} when the build cannot read it. Reading it
    for a glance must not use up a note the page's own check will want to
    show, so the build's notes are left as they were."""
    if not path.is_file():
        return {}
    noted, lines = set(b._NOTED), list(b._NOTE_LINES)
    try:
        return b.split_frontmatter(path.read_text(), path)[0]
    except b.BuildError:
        return {}
    finally:
        b._NOTED.clear()
        b._NOTED.update(noted)
        b._NOTE_LINES[:] = lines


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
        courses[path.stem] = data if isinstance(data, dict) else {}
    return courses


def listed_in(courses: dict[str, dict], ident: str) -> list[str]:
    where = []
    for course_id, course in courses.items():
        for series in course.get("contents") or []:
            if isinstance(series, dict) and ident in (series.get("tutorials") or []):
                where.append(f"{course_id} → {series.get('title', '?')}")
        if ident in (course.get("mixed") or []):
            where.append(f"{course_id} → mixed problems")
    return where


def all_tutorial_ids() -> list[str]:
    if not TUTORIALS.is_dir():
        return []
    return sorted(p.name for p in TUTORIALS.iterdir() if p.is_dir() and any(p.glob("*.md")))


def title_of(folder: Path) -> str | None:
    main = folder / f"{folder.name}.md"
    fields = fields_of(main) if main.is_file() else {}
    return str(fields["title"]) if fields.get("title") else None


# ------------------------------------------------------------- one tutorial

def check_tutorial(folder: Path, courses: dict[str, dict], report: Report, titles: dict[str, list[str]]) -> None:
    ident = folder.name
    report.note(f"— {folder.relative_to(ROOT)} —")
    if not ID_RE.match(ident):
        report.note(f"The folder name `{ident}` is not a tidy id. Small letters, digits and hyphens, like `first-steps`, make an address that is easy to type and share. Once readers have saved work under it, the name cannot change.")
    main = folder / f"{ident}.md"
    if not main.is_file():
        report.problem(f"There is no `{ident}.md` inside the folder. The main file must have the same name as the folder.")
        return
    report.ok(f"The main file `{ident}.md` is there.")

    # every page in the folder, read the way the build reads it
    pages = {}
    for path in sorted(folder.glob("*.md")):
        page = from_build(report, read_page, path)
        if page is not None:
            pages[path.name] = page
    page = pages.get(main.name)
    if page is None:
        return  # the build's own message is above
    report.checked.append(("practice" if page.practice_for else "tutorial", ident, page.title))
    cells = [cell for cell in page.cells]
    if cells:
        report.ok(f"{len(cells)} cell{'s' if len(cells) != 1 else ''}, each with its own id.")
    else:
        report.note("No runnable cells in this tutorial. That is fine for a reading page.")

    # the rules between pages: who a practice or context page belongs to
    registry = {p.slug: p for p in pages.values()}
    for p in list(pages.values()):
        for name in (p.practice_for, *p.practice_across, *p.context_for):
            path = TUTORIALS / str(name) / f"{name}.md"
            if name and name not in registry and path.is_file():
                other = from_build(report, read_page, path)
                if other is not None:
                    registry[other.slug] = other
    together = list(pages.values())
    for rule in (b.practice_pairs, b.mixed_practice, b.context_pages):
        from_build(report, rule, together, registry)

    # a second page in the folder that follows no tutorial is a tutorial of its own
    for name, other in pages.items():
        if other is page or b.VERSION_FILE_RE.match(Path(name).stem):
            continue
        if not (other.practice_for or other.practice_across or other.is_context):
            report.note(f"`{name}` has no `practice_for:`, `context_for:` or `practice_across:`, so it is a tutorial of its own, not a page that follows `{ident}`, and no course lists it.")

    # title collisions across the site
    title = str(page.title or "")
    others = [t for t in titles.get(title, []) if t != ident]
    if title and others:
        report.note(f"Another tutorial has the same title, \"{title}\": {', '.join(others)}. That is allowed, but check it is a different tutorial and not a copy.")

    # advice, not rules
    if page.is_context:
        report.ok(f"A context page for {', '.join(page.context_for)}. It is not listed in a course; it follows those tutorials.")
    elif not page.practice_across and not any(p.practice_for == ident for p in pages.values()):
        report.note(f"No practice page. To add one, create `{ident}-practice.md` in this folder with `practice_for: {ident}`.")
    elif any(p.practice_for == ident for p in pages.values()):
        report.ok("There is a practice page, and it belongs to this tutorial.")

    glossary = folder / f"{ident}.glossary.yaml"
    if glossary.is_file():
        entries = from_build(report, b.own_glossary, page)
        if entries is not None:
            report.ok(f"The glossary has {len(entries)} entr{'y' if len(entries) == 1 else 'ies'}.")

    # where it is listed
    where = listed_in(courses, ident)
    if page.is_context or page.practice_for:
        pass  # it follows its tutorial, not a course
    elif where:
        report.ok("Listed on: " + "; ".join(where) + ".")
    else:
        report.note(f"No course lists `{ident}` yet. The page will build, but nobody will find it from a course page. To list it, add `{ident}` to a `tutorials:` list in a file under `courses/`.")


# --------------------------------------------------------------- one course

def check_course(path: Path, courses: dict[str, dict], report: Report) -> None:
    course_id = path.stem
    report.note(f"— {path.relative_to(ROOT)} —")
    course = from_build(report, b.read_course, path)
    if course is None:
        return
    report.checked.append(("course", course_id, course.title))
    if not ID_RE.match(course_id):
        report.note(f"The file name `{course_id}` is not a tidy id. Small letters, digits and hyphens make an address that is easy to type.")
    if not course.contents:
        # The build accepts a course with no series; it is a course with
        # nothing on it yet, not a mistake.
        report.note("No series under `contents:` yet, so the course lists nothing. "
                    "Add a series with a title and its tutorials when you are ready.")
    for key in ("code", "card", "description"):
        if not getattr(course, key):
            report.note(f"No `{key}:`. The course page or its card will be missing that text.")
    known = set(all_tutorial_ids())
    total = 0
    for series in course.contents:
        if not series.ids:
            report.note(f"The series \"{series.title}\" lists no tutorials yet, so the course page leaves it out.")
        for ident in series.ids:
            total += 1
            fields = fields_of(TUTORIALS / ident / f"{ident}.md")
            if ident not in known:
                report.problem(f"The series \"{series.title}\" lists `{ident}`, but there is no folder `tutorials/{ident}/`.")
            elif fields.get("practice_for"):
                report.note(f"`{ident}` is a practice page (it has `practice_for:`). It follows its tutorial, so this line is left out.")
            elif fields.get("context_for"):
                report.note(f"`{ident}` is a context page (it has `context_for:`). It follows its tutorial, so this line is left out.")
    for ident in course.mixed:
        fields = fields_of(TUTORIALS / ident / f"{ident}.md")
        if not (TUTORIALS / ident).is_dir():
            report.problem(f"`mixed:` names `{ident}`, but there is no folder `tutorials/{ident}/`.")
        elif not fields.get("practice_across"):
            report.note(f"`mixed:` names `{ident}`, which is not a mixed problem set (it has no `practice_across:`), so the line is left out.")
    if not report.problems:
        report.ok(f"{len(course.contents)} series, {total} tutorials, every id found.")
    index = COURSES / "index.yaml"
    if index.is_file():
        order = (yaml.safe_load(index.read_text()) or {}).get("order") or []
        if course_id in order:
            report.ok(f"Listed in `courses/index.yaml` at position {order.index(course_id) + 1}.")
        else:
            report.note(f"`courses/index.yaml` does not list `{course_id}`, so it will appear last. Add it where you want it.")
    else:
        report.note("There is no `courses/index.yaml`, so courses appear in alphabetical order.")


# ------------------------------------------------------------ pull request

def git(*args: str) -> str | None:
    """stdout of a git command, or None when git says no."""
    try:
        done = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True)
    except FileNotFoundError:
        return None
    return done.stdout.strip() if done.returncode == 0 else None


def repository_slug() -> str | None:
    """`owner/name` from the origin remote, for https or ssh addresses."""
    url = git("remote", "get-url", "origin")
    if not url:
        return None
    match = re.search(r"github\.com[:/]([^/]+)/([^/]+?)(?:\.git)?/?$", url)
    return f"{match.group(1)}/{match.group(2)}" if match else None


def changed_paths(items: list[tuple[str, str, str]]) -> list[str]:
    """Every file under the checked tutorials and courses that git sees as
    new or changed — what the pull request should carry."""
    wanted = []
    for kind, ident, _ in items:
        wanted.append(f"tutorials/{ident}/" if kind != "course" else f"courses/{ident}.yaml")
    if any(kind == "course" for kind, _, _ in items):
        wanted.append("courses/index.yaml")
    status = git("status", "--porcelain", "--", *wanted) or ""
    paths = []
    for line in status.splitlines():
        # `XY path`; git() has trimmed the output, so a modified file's
        # leading space is gone — split on the first run of spaces instead
        # of counting columns. A rename reads `old -> new`; keep `new`.
        parts = line.strip().split(None, 1)
        if len(parts) == 2:
            paths.append(parts[1].split(" -> ")[-1].strip())
    return sorted(set(paths))


def describe(items: list[tuple[str, str, str]], paths: list[str]) -> tuple[str, str]:
    """A title and a description for the pull request, from what was
    checked. Short, in plain words, and true to the context: one tutorial,
    a practice page, a course, or several things at once."""
    tutorials = [(i, t) for k, i, t in items if k == "tutorial"]
    practice = [(i, t) for k, i, t in items if k == "practice"]
    courses = [(i, t) for k, i, t in items if k == "course"]
    new = {p for p in paths if git("ls-files", "--error-unmatch", p) is None}
    if len(tutorials) == 1 and not courses:
        ident, title = tutorials[0]
        verb = "Add" if f"tutorials/{ident}/{ident}.md" in new else "Update"
        head = f"{verb} tutorial: {title}"
    elif len(courses) == 1 and not tutorials:
        ident, title = courses[0]
        verb = "Add" if f"courses/{ident}.yaml" in new else "Update"
        head = f"{verb} course: {title}"
    elif practice and not tutorials and not courses:
        head = "Add practice: " + ", ".join(t for _, t in practice)
    else:
        head = "Add tutorials and courses" if new else "Update tutorials and courses"
    lines = ["## What this changes", ""]
    for ident, title in tutorials:
        lines.append(f"- Tutorial **{title}** (`tutorials/{ident}/`)" + (" — new" if f"tutorials/{ident}/{ident}.md" in new else ""))
    for ident, title in practice:
        lines.append(f"- Practice page **{title}** (`tutorials/{ident}/`)")
    for ident, title in courses:
        lines.append(f"- Course **{title}** (`courses/{ident}.yaml`)" + (" — new" if f"courses/{ident}.yaml" in new else ""))
    lines += ["", "## Checks", "", "`python3 check.py` reported no problems.", "", "## Files", ""]
    lines += [f"- `{p}`" for p in paths]
    lines += ["", "Opened from `check.py`."]
    return head, "\n".join(lines)


def ask(question: str) -> bool:
    if not sys.stdin.isatty():
        return False
    try:
        answer = input(f"{question} [y/N] ").strip().lower()
    except EOFError:
        return False
    return answer in ("y", "yes")


def offer_pull_request(report: Report, mode: str) -> None:
    """mode: "ask", "yes" or "no"."""
    if mode == "no" or not report.checked:
        return
    slug = repository_slug()
    branch = git("rev-parse", "--abbrev-ref", "HEAD")
    if not slug or not branch:
        print("To open a pull request, this folder needs to be a git clone of the GitHub repository.")
        return
    if branch in ("main", "master"):
        print(f"You are on the `{branch}` branch. Make a branch for your change first:")
        print("    git switch -c my-change")
        print("Then run this command again, and I will help you open the pull request.")
        return
    paths = changed_paths(report.checked)
    what = ", ".join(t for _, _, t in report.checked)
    if mode == "ask":
        print()
        if not ask(f"Open a pull request for {what}?"):
            print("No problem. When you are ready, run this command again — or add `--pr` — and I will")
            print("write the pull request from whatever you have changed by then.")
            return
    if paths:
        print("These files will go in the commit:")
        for p in paths:
            print(f"    {p}")
        if mode == "ask" and not ask("Commit and push them now?"):
            print("Nothing committed. Run again with `--pr` when you are ready.")
            return
        title, _ = describe(report.checked, paths)
        if git("add", "--", *paths) is None or git("commit", "-q", "-m", title) is None:
            print("Problem  git could not commit. Run `git status` to see why, then try again.")
            return
    upstream = git("rev-parse", "--abbrev-ref", "@{u}")
    if not upstream or git("log", "--oneline", "@{u}..HEAD"):
        if git("push", "-u", "origin", branch) is None:
            print(f"Problem  git could not push. Try:  git push -u origin {branch}")
            return
    all_paths = paths or (git("diff", "--name-only", "origin/main...HEAD") or "").splitlines()
    title, body = describe(report.checked, all_paths)
    base = git("symbolic-ref", "--short", "refs/remotes/origin/HEAD") or "origin/main"
    base = base.split("/", 1)[-1]
    query = urllib.parse.urlencode({"quick_pull": "1", "title": title, "body": body})
    url = f"https://github.com/{slug}/compare/{base}...{branch}?{query}"
    print()
    print("Your pull request page is ready. The title and description are filled in;")
    print("read them, change anything you like, and press the green button.")
    print(f"    {url}")
    if mode == "ask" or sys.stdin.isatty():
        try:
            webbrowser.open(url)
        except Exception:  # pragma: no cover — a browser is a convenience
            pass


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
    def follows_another(i: str) -> bool:
        fields = fields_of(TUTORIALS / i / f"{i}.md")
        return bool(fields.get("practice_across") or fields.get("context_for"))
    unlisted = [i for i in ids if i not in listed and not i.endswith("-practice")
                and not follows_another(i)]
    report.note("— summary —")
    report.note(f"{len(ids)} tutorials, {len(courses)} courses, {len(unlisted)} tutorial{'s' if len(unlisted) != 1 else ''} on no course.")


def main(argv: list[str]) -> int:
    with b.collecting_notes():
        return run(argv)


def run(argv: list[str]) -> int:
    report = Report()
    mode = "ask"
    if "--pr" in argv:
        mode = "yes"
    if "--no-pr" in argv:
        mode = "no"
    argv = [a for a in argv if a not in ("--pr", "--no-pr")]
    if len(argv) <= 1:
        check_everything(report)
        mode = "no"  # a whole-site check is not one change to send
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
    if mode != "no":
        offer_pull_request(report, mode)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
