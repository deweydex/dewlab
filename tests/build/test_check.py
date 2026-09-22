"""Proof for check.py — the contributor's tool — on small trees: each
Problem against a fixture the build also refuses, each Note against one it
accepts, and the pull-request offer's promises.

    python3 -m pytest tests/build/test_check.py -q
"""
from __future__ import annotations

import importlib
import io
import subprocess
import sys
from pathlib import Path

import pytest

DEWLAB = Path(__file__).resolve().parent.parent.parent

from helpers import b  # noqa: E402  (the `repo` fixture comes from conftest)


@pytest.fixture()
def site(tmp_path: Path, monkeypatch):
    """A tree in the shape the build reads: flat tutorials/<id>/<id>.md,
    one course file per course under courses/, and check.py pointed at
    it."""
    root = tmp_path / "repo"
    (root / "tutorials").mkdir(parents=True)
    (root / "courses").mkdir()
    sys.path.insert(0, str(DEWLAB))
    check = importlib.import_module("check")
    importlib.reload(check)
    monkeypatch.setattr(check, "ROOT", root)
    monkeypatch.setattr(check, "TUTORIALS", root / "tutorials")
    monkeypatch.setattr(check, "COURSES", root / "courses")
    return root, check


def tutorial(root: Path, ident: str, body: str = "Prose.\n", front: str = 'title: "A Title"\nyear: "2026-2027"\nversion: 2026.09.14.1\n') -> Path:
    folder = root / "tutorials" / ident
    folder.mkdir(exist_ok=True)
    path = folder / f"{ident}.md"
    path.write_text(f"---\n{front}---\n\n# A Title\n\n{body}")
    return path


def course(root: Path, ident: str, series: dict[str, list[str]], extra: str = "") -> Path:
    path = root / "courses" / f"{ident}.yaml"
    lines = [f"title: {ident.title()}", "code: X1", "status: beta", "card: A card.", "description: A description.", "contents:"]
    for title, ids in series.items():
        lines.append(f"  - title: {title}")
        lines.append(f"    tutorials: [{', '.join(ids)}]")
    path.write_text("\n".join(lines) + "\n" + extra)
    (root / "courses" / "index.yaml").write_text(f"order:\n  - {ident}\n")
    return path


def run_check(check, *args: str) -> tuple[int, str]:
    out = io.StringIO()
    real = sys.stdout
    sys.stdout = out
    try:
        code = check.main(["check.py", *args, "--no-pr"])
    finally:
        sys.stdout = real
    return code, out.getvalue()


# ------------------------------------------------------------ the checks

def test_a_good_tree_has_no_problems_only_notes_and_a_whole_site_check_never_offers(site, monkeypatch) -> None:
    """One tree, every kind of thing check.py accepts: a listed tutorial
    with a cell, one no course lists, one whose only image is inside a code
    example, a real tutorial whose id ends in -practice beside a practice
    page, and two tutorials sharing a title. Checked one path at a time,
    then all at once."""
    root, check = site
    tutorial(root, "first-steps", body="```python exec\nid: one\nprint(1)\n```\n")
    tutorial(root, "lonely")
    tutorial(root, "web", body="Write this:\n\n```html\n<img src=\"does-not-exist.jpg\" alt=\"x\">\n```\n\nAnd `![x](also-not.png)` in a span.\n")
    tutorial(root, "sql-practice")  # a real tutorial whose id ends in -practice
    tutorial(root, "joins")
    (root / "tutorials" / "joins" / "joins-practice.md").write_text(
        '---\ntitle: "Joins — Practice"\nyear: "2026-2027"\nversion: 2026.09.14.1\npractice_for: joins\n---\n\n**1.** Q.\n')
    tutorial(root, "a")
    tutorial(root, "b")
    course(root, "alpha", {"Start": ["first-steps"], "SQL": ["sql-practice", "joins"], "S": ["a", "b"]})

    # A good tutorial on a course has no problems.
    code, out = run_check(check, "tutorials/first-steps")
    assert code == 0 and "No problems" in out
    assert "Listed on: alpha → Start" in out

    # An unlisted tutorial gets a note saying how to list it.
    code, out = run_check(check, "tutorials/lonely")
    assert code == 0
    assert "No course lists `lonely` yet" in out and "courses/" in out

    # An image inside a code example is not a missing image.
    code, out = run_check(check, "tutorials/web")
    assert code == 0, out

    # A practice page is known by its frontmatter, not its name.
    code, out = run_check(check, "courses/alpha.yaml")
    assert code == 0, out

    # A repeated title is a note, not a problem.
    code, out = run_check(check, "tutorials/a")
    assert code == 0 and 'same title, "A Title": b' in out

    # A whole-site check never offers a pull request.
    monkeypatch.setattr(check, "offer_pull_request", lambda *a, **k: (_ for _ in ()).throw(AssertionError("offered")))
    code = check.main(["check.py", "--pr"])
    assert code == 0


def test_every_problem_in_one_tutorial_is_named_and_so_is_an_unknown_path(site) -> None:
    """One tutorial carrying every mistake check.py calls a Problem, a
    course listing an id with no folder, and a path that is neither."""
    root, check = site
    tutorial(root, "old",
             front='title: "Old"\nyear: "2026-2027"\nversion: 2026.09.14.1\nmodule: alpha\nseries: start\n',
             body="```python exec\nprint(1)\n```\n\n```python exec\nid: a\n```\n\n```python exec\nid: a\n```\n\n![A plot](plot.png)\n")
    tutorial(root, "first-steps")
    course(root, "alpha", {"Start": ["first-steps", "frist-steps"]})

    code, out = run_check(check, "tutorials/old")
    # An old placement field is a problem that says to delete it.
    assert code == 1
    assert "delete these old lines" in out and "module, series" in out
    # A cell without an id, and two cells with one id, are problems.
    assert code == 1
    assert "has no `id:` line" in out and "used more than once: a" in out
    # A real missing image is a problem.
    assert code == 1 and "`plot.png` is not in the folder" in out

    # A course listing an unknown id is a problem naming the series.
    code, out = run_check(check, "courses/alpha.yaml")
    assert code == 1
    assert 'The series "Start" lists `frist-steps`, but there is no folder' in out

    # An unknown path gets a plain sentence, not a traceback.
    code, out = run_check(check, "somewhere/else")
    assert code == 1
    assert "I do not know how to check `somewhere/else`" in out


# ------------------------------------------------------ the pull request

def test_the_title_and_description_come_from_what_was_checked_and_the_repository_from_the_remote(site, monkeypatch) -> None:
    root, check = site
    # Every path counts as new.
    monkeypatch.setattr(check, "git", lambda *a: None)
    title, body = check.describe([("tutorial", "first-steps", "First Steps")], ["tutorials/first-steps/first-steps.md"])
    assert title == "Add tutorial: First Steps"
    assert "- Tutorial **First Steps** (`tutorials/first-steps/`) — new" in body
    assert "`python3 check.py` reported no problems." in body
    assert "- `tutorials/first-steps/first-steps.md`" in body
    title, _ = check.describe([("course", "alpha", "Alpha")], ["courses/alpha.yaml"])
    assert title == "Add course: Alpha"
    title, _ = check.describe([("practice", "joins", "Joins — Practice")], ["tutorials/joins/joins-practice.md"])
    assert title == "Add practice: Joins — Practice"
    # An existing file makes it an update.
    monkeypatch.setattr(check, "git", lambda *a: "tracked" if a[0] == "ls-files" else None)
    title, _ = check.describe([("tutorial", "first-steps", "First Steps")], ["tutorials/first-steps/first-steps.md"])
    assert title == "Update tutorial: First Steps"
    # The repository is read from either remote address.
    monkeypatch.setattr(check, "git", lambda *a: "https://github.com/deweydex/dewlab.git")
    assert check.repository_slug() == "deweydex/dewlab"
    monkeypatch.setattr(check, "git", lambda *a: "git@github.com:deweydex/dewlab.git")
    assert check.repository_slug() == "deweydex/dewlab"


def test_on_main_it_says_to_make_a_branch_and_touches_nothing(site, monkeypatch, capsys) -> None:
    root, check = site
    calls: list[tuple] = []
    def fake_git(*a):
        calls.append(a)
        return {"remote": "https://github.com/deweydex/dewlab", "rev-parse": "main"}.get(a[0])
    monkeypatch.setattr(check, "git", fake_git)
    report = check.Report()
    report.checked = [("tutorial", "first-steps", "First Steps")]
    check.offer_pull_request(report, "yes")
    out = capsys.readouterr().out
    assert "git switch -c my-change" in out
    assert not any(a[0] in ("add", "commit", "push") for a in calls)


def test_the_address_carries_the_title_and_body_and_the_branch(site, monkeypatch, capsys) -> None:
    root, check = site
    answers = {"remote": "https://github.com/deweydex/dewlab.git", "rev-parse": "my-change",
               "status": " M tutorials/first-steps/first-steps.md\n", "ls-files": "tracked",
               "add": "", "commit": "", "push": "", "log": "", "symbolic-ref": "origin/main", "diff": ""}
    def fake_git(*a):
        if a[0] == "rev-parse" and a[-1] == "@{u}":
            return "origin/my-change"
        return answers.get(a[0])
    monkeypatch.setattr(check, "git", fake_git)
    monkeypatch.setattr(check.webbrowser, "open", lambda url: True)
    report = check.Report()
    report.checked = [("tutorial", "first-steps", "First Steps")]
    check.offer_pull_request(report, "yes")
    out = capsys.readouterr().out
    assert "https://github.com/deweydex/dewlab/compare/main...my-change?quick_pull=1&title=Update+tutorial%3A+First+Steps&body=" in out


# ------------------------------------------------ the tool's promise, proven

MISTAKES = {
    # name: (frontmatter, body, course listing) — one mistake each, of a
    # kind check.py covers. `None` for a value keeps the good default.
    "an old placement field": ('title: "T"\nyear: "2026-2027"\nversion: 2026.09.14.1\nmodule: alpha\n', None, None),
    "a version that is not a release date": ('title: "T"\nyear: "2026-2027"\nversion: 1\n', None, None),
    "a missing title": ('year: "2026-2027"\nversion: 2026.09.14.1\n', None, None),
    "a cell with no id": (None, "```python exec\nprint(1)\n```\n", None),
    "two cells with one id": (None, "```python exec\nid: a\nprint(1)\n```\n\n```python exec\nid: a\nprint(2)\n```\n", None),
    "an image that is not in the folder": (None, "![A plot](plot.png)\n", None),
    "a course listing an id with no folder": (None, None, ["good", "gone"]),
    "a course listing an id twice": (None, None, ["good", "good"]),
}


@pytest.mark.parametrize("mistake", sorted(MISTAKES))
def test_everything_check_calls_a_problem_the_build_also_refuses(repo, monkeypatch, mistake):
    """check.py says "No problems" only about a tree the build accepts, and
    every Problem it reports is a build failure: both run over one tree
    with one mistake in it, and both refuse. The good tree passes both."""
    import importlib
    sys.path.insert(0, str(DEWLAB))
    check = importlib.import_module("check")
    importlib.reload(check)
    monkeypatch.setattr(check, "ROOT", repo)
    monkeypatch.setattr(check, "TUTORIALS", repo / "tutorials")
    monkeypatch.setattr(check, "COURSES", repo / "courses")

    front, body, listing = MISTAKES[mistake]
    tutorial(repo, "good", body=body or "Prose.\n", front=front or 'title: "Good"\nyear: "2026-2027"\nversion: 2026.09.14.1\n')
    course(repo, "alpha", {"Start": listing or ["good"]})

    code, out = run_check(check)
    assert code == 1, f"check.py saw no problem in {mistake}:\n{out}"
    with pytest.raises(b.BuildError):
        b.build()


def test_everything_check_and_the_build_both_accept_a_good_tree(repo, monkeypatch):
    import importlib
    sys.path.insert(0, str(DEWLAB))
    check = importlib.import_module("check")
    importlib.reload(check)
    monkeypatch.setattr(check, "ROOT", repo)
    monkeypatch.setattr(check, "TUTORIALS", repo / "tutorials")
    monkeypatch.setattr(check, "COURSES", repo / "courses")
    tutorial(repo, "good", body="```python exec\nid: one\nprint(1)\n```\n")
    course(repo, "alpha", {"Start": ["good"]})
    code, out = run_check(check)
    assert code == 0, out
    assert b.build()


def test_a_context_page_is_not_a_problem_but_listing_one_in_a_course_is(site) -> None:
    """A context page follows the tutorial it gives background for, the way
    a practice page does: check.py does not call it unlisted, and does not
    offer it a practice page. A course that lists it is a problem, as the
    build also says."""
    root, check = site
    tutorial(root, "joins")
    tutorial(root, "why-joins", front='title: "Why Joins"\nyear: "2026-2027"\nversion: 2026.09.14.1\ncontext_for: joins\n')
    course(root, "alpha", {"SQL": ["joins"]})

    code, out = run_check(check, "tutorials/why-joins")
    assert code == 0, out
    assert "A context page for joins" in out
    assert "No course lists" not in out and "No practice page" not in out

    code, out = run_check(check)
    assert code == 0, out
    assert "0 tutorials on no course" in out

    course(root, "alpha", {"SQL": ["joins", "why-joins"]})
    code, out = run_check(check, "courses/alpha.yaml")
    assert code == 1
    assert "`why-joins` is a context page" in out
