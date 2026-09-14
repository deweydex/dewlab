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


@pytest.fixture()
def site(tmp_path: Path, monkeypatch):
    """A migrated-shape tree: flat tutorials/, courses/, and check.py
    pointed at it."""
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

def test_a_good_tutorial_on_a_course_has_no_problems(site) -> None:
    root, check = site
    tutorial(root, "first-steps", body="```python exec\nid: one\nprint(1)\n```\n")
    course(root, "alpha", {"Start": ["first-steps"]})
    code, out = run_check(check, "tutorials/first-steps")
    assert code == 0 and "No problems" in out
    assert "Listed on: alpha → Start" in out


def test_an_unlisted_tutorial_gets_a_note_saying_how_to_list_it(site) -> None:
    root, check = site
    tutorial(root, "lonely")
    code, out = run_check(check, "tutorials/lonely")
    assert code == 0
    assert "No course lists `lonely` yet" in out and "courses/" in out


def test_an_old_placement_field_is_a_problem_that_says_to_delete_it(site) -> None:
    root, check = site
    tutorial(root, "old", front='title: "Old"\nyear: "2026-2027"\nversion: 2026.09.14.1\nmodule: alpha\nseries: start\n')
    code, out = run_check(check, "tutorials/old")
    assert code == 1
    assert "delete these old lines" in out and "module, series" in out


def test_a_cell_without_an_id_and_two_cells_with_one_id_are_problems(site) -> None:
    root, check = site
    tutorial(root, "cells", body="```python exec\nprint(1)\n```\n\n```python exec\nid: a\n```\n\n```python exec\nid: a\n```\n")
    code, out = run_check(check, "tutorials/cells")
    assert code == 1
    assert "has no `id:` line" in out and "used more than once: a" in out


def test_an_image_inside_a_code_example_is_not_a_missing_image(site) -> None:
    root, check = site
    tutorial(root, "web", body="Write this:\n\n```html\n<img src=\"does-not-exist.jpg\" alt=\"x\">\n```\n\nAnd `![x](also-not.png)` in a span.\n")
    code, out = run_check(check, "tutorials/web")
    assert code == 0, out


def test_a_real_missing_image_is_a_problem(site) -> None:
    root, check = site
    tutorial(root, "pic", body="![A plot](plot.png)\n")
    code, out = run_check(check, "tutorials/pic")
    assert code == 1 and "`plot.png` is not in the folder" in out


def test_a_practice_page_is_known_by_its_frontmatter_not_its_name(site) -> None:
    root, check = site
    tutorial(root, "sql-practice")  # a real tutorial whose id ends in -practice
    tutorial(root, "joins")
    (root / "tutorials" / "joins" / "joins-practice.md").write_text(
        '---\ntitle: "Joins — Practice"\nyear: "2026-2027"\nversion: 2026.09.14.1\npractice_for: joins\n---\n\n**1.** Q.\n')
    course(root, "db", {"SQL": ["sql-practice", "joins"]})
    code, out = run_check(check, "courses/db.yaml")
    assert code == 0, out


def test_a_course_listing_an_unknown_id_is_a_problem_naming_the_series(site) -> None:
    root, check = site
    tutorial(root, "first-steps")
    course(root, "alpha", {"Start": ["first-steps", "frist-steps"]})
    code, out = run_check(check, "courses/alpha.yaml")
    assert code == 1
    assert 'The series "Start" lists `frist-steps`, but there is no folder' in out


def test_a_repeated_title_is_a_note_not_a_problem(site) -> None:
    root, check = site
    tutorial(root, "a")
    tutorial(root, "b")
    course(root, "alpha", {"S": ["a", "b"]})
    code, out = run_check(check, "tutorials/a")
    assert code == 0 and 'same title, "A Title": b' in out


def test_an_unknown_path_gets_a_plain_sentence_not_a_traceback(site) -> None:
    root, check = site
    code, out = run_check(check, "somewhere/else")
    assert code == 1
    assert "I do not know how to check `somewhere/else`" in out


# ------------------------------------------------------ the pull request

def test_the_title_and_description_come_from_what_was_checked(site, monkeypatch) -> None:
    root, check = site
    monkeypatch.setattr(check, "git", lambda *a: None)  # every path counts as new
    title, body = check.describe([("tutorial", "first-steps", "First Steps")], ["tutorials/first-steps/first-steps.md"])
    assert title == "Add tutorial: First Steps"
    assert "- Tutorial **First Steps** (`tutorials/first-steps/`) — new" in body
    assert "`python3 check.py` reported no problems." in body
    assert "- `tutorials/first-steps/first-steps.md`" in body
    title, _ = check.describe([("course", "alpha", "Alpha")], ["courses/alpha.yaml"])
    assert title == "Add course: Alpha"
    title, _ = check.describe([("practice", "joins", "Joins — Practice")], ["tutorials/joins/joins-practice.md"])
    assert title == "Add practice: Joins — Practice"


def test_an_existing_file_makes_it_an_update(site, monkeypatch) -> None:
    root, check = site
    monkeypatch.setattr(check, "git", lambda *a: "tracked" if a[0] == "ls-files" else None)
    title, _ = check.describe([("tutorial", "first-steps", "First Steps")], ["tutorials/first-steps/first-steps.md"])
    assert title == "Update tutorial: First Steps"


def test_the_repository_is_read_from_either_remote_address(site, monkeypatch) -> None:
    root, check = site
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


def test_a_whole_site_check_never_offers(site, monkeypatch, capsys) -> None:
    root, check = site
    tutorial(root, "a")
    course(root, "alpha", {"S": ["a"]})
    monkeypatch.setattr(check, "offer_pull_request", lambda *a, **k: (_ for _ in ()).throw(AssertionError("offered")))
    code = check.main(["check.py", "--pr"])
    assert code == 0


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
