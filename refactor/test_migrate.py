"""Proof for refactor/migrate_tutorials.py, on a small tree shaped like the
real one: two modules that both have `first-steps`, each with a practice
page, order files, a series chain, modules.yaml and a home card. Deleted
with this folder.

    python3 -m pytest refactor/test_migrate.py -q
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest
import yaml

HERE = Path(__file__).resolve().parent
SCRIPT = HERE / "migrate_tutorials.py"

FRONT = "---\ntitle: \"{title}\"\nslug: {slug}\nmodule: {module}\nmodule_title: \"{mt}\"\nyear: \"2026-2027\"\nseries: {series}\nversion: 2026.09.01.1\n{extra}---\n\n# {title}\n\n{body}"


def tutorial(root: Path, module: str, slug: str, series: str, title: str, body: str = "Prose.\n", extra: str = "") -> Path:
    folder = root / "tutorials" / module / slug
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f"{slug}.md"
    path.write_text(FRONT.format(title=title, slug=slug, module=module, mt=module.title(), series=series, extra=extra, body=body))
    return path


@pytest.fixture()
def tree(tmp_path: Path) -> Path:
    root = tmp_path / "repo"
    (root / "refactor").mkdir(parents=True)
    (root / "refactor" / "migrate_tutorials.py").write_text(SCRIPT.read_text())
    (root / "build.py").write_text("MODULE_INFO = {'alpha': {'code': 'A1', 'description': ['Alpha.']}}\n")
    (root / "pages").mkdir()
    (root / "pages" / "home.md").write_text(
        "---\ntitle: home\n---\n\n```card\nurl: alpha.html\nstatus: beta\nmeta: A1 · QQI Level 5\n### Alpha\nThe alpha course.\n```\n\n"
        "```card\nurl: beta.html\nmeta: B1\n### Beta\nThe beta course.\n```\n")
    # alpha: two series, chained; first-steps has a practice page and a link
    tutorial(root, "alpha", "first-steps", "start", "First Steps", body="See [next](tutorial:second-steps).\n")
    tutorial(root, "alpha", "second-steps", "start", "Second Steps")
    tutorial(root, "alpha", "deeper", "more", "Deeper")
    (root / "tutorials" / "alpha" / "first-steps" / "first-steps-practice.md").write_text(
        FRONT.format(title="First Steps — Practice", slug="first-steps-practice", module="alpha", mt="Alpha",
                     series="start", extra="practice_for: first-steps\n", body="**1.** A question.\n"))
    (root / "tutorials" / "alpha" / "first-steps" / "v2026.08.01.1.md").write_text(
        FRONT.format(title="First Steps", slug="first-steps", module="alpha", mt="Alpha", series="start", extra="", body="Old.\n")
        .replace("2026.09.01.1", "2026.08.01.1"))
    (root / "tutorials" / "alpha" / "start.order.yaml").write_text("series: Start Here\norder:\n  - first-steps\n  - second-steps\n")
    (root / "tutorials" / "alpha" / "more.order.yaml").write_text("series: More\norder:\n  - deeper\n")
    (root / "tutorials" / "alpha" / "series.yaml").write_text("order:\n  - start\n  - more\n")
    # beta: its own first-steps, with a practice page and a mixed set naming it
    tutorial(root, "beta", "first-steps", "basics", "First Steps", body="Beta's own.\n")
    (root / "tutorials" / "beta" / "first-steps" / "first-steps-practice.md").write_text(
        FRONT.format(title="First Steps — Practice", slug="first-steps-practice", module="beta", mt="Beta",
                     series="basics", extra="practice_for: first-steps\n", body="**1.** Q.\n"))
    tutorial(root, "beta", "tables", "basics", "Tables")
    tutorial(root, "beta", "mixed", "basics", "Mixed Problems", extra="practice_across:\n  - first-steps\n  - tables\n", body="**1.** Q.\n")
    (root / "tutorials" / "beta" / "basics.order.yaml").write_text("series: Basics\norder:\n  - first-steps\n  - tables\n")
    (root / "tutorials" / "modules.yaml").write_text("order:\n  - beta\n  - alpha\n")
    (root / "tutorials" / "alpha" / ".gitkeep").write_text("")  # as two real module folders have
    subprocess.run(["git", "init", "-q"], cwd=root, check=True)
    subprocess.run(["git", "add", "-A"], cwd=root, check=True)
    subprocess.run(["git", "-c", "user.email=t@t", "-c", "user.name=t", "commit", "-q", "-m", "base"], cwd=root, check=True)
    return root


def run(root: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, "refactor/migrate_tutorials.py", *args], cwd=root, capture_output=True, text=True)


def test_a_collision_stops_apply_until_it_has_a_rename(tree: Path) -> None:
    result = run(tree, "--apply")
    assert result.returncode == 1
    assert "first-steps: alpha, beta" in result.stdout
    assert "--rename" in result.stdout
    assert not (tree / "courses").exists()


def test_the_dry_run_writes_nothing(tree: Path) -> None:
    result = run(tree, "--rename", "beta/first-steps=first-steps-b")
    assert result.returncode == 0, result.stdout + result.stderr
    assert "dry run: nothing written" in result.stdout
    assert (tree / "tutorials" / "alpha" / "first-steps").is_dir()
    assert not (tree / "courses").exists()


def test_apply_flattens_strips_and_writes_courses(tree: Path) -> None:
    result = run(tree, "--rename", "beta/first-steps=first-steps-b", "--apply")
    assert result.returncode == 0, result.stdout + result.stderr
    assert sorted(p.name for p in (tree / "tutorials").iterdir()) == [
        "deeper", "first-steps", "first-steps-b", "mixed", "second-steps", "tables"]
    front = (tree / "tutorials" / "first-steps" / "first-steps.md").read_text().split("---")[1]
    for gone in ("module:", "module_title:", "series:", "slug:"):
        assert gone not in front
    assert "title: \"First Steps\"" in front and "version: 2026.09.01.1" in front
    # the release file was moved and stripped too
    old = (tree / "tutorials" / "first-steps" / "v2026.08.01.1.md").read_text()
    assert "module:" not in old.split("---")[1]
    courses = {p.stem: yaml.safe_load(p.read_text()) for p in (tree / "courses").glob("*.yaml")}
    assert courses["index"] == {"order": ["beta", "alpha"]}
    alpha = courses["alpha"]
    assert alpha["title"] == "Alpha" and alpha["code"] == "A1" and alpha["card"] == "The alpha course."
    assert [s["title"] for s in alpha["contents"]] == ["Start Here", "More"]  # series.yaml order
    assert alpha["contents"][0]["tutorials"] == ["first-steps", "second-steps"]
    beta = courses["beta"]
    assert beta["code"] == "B1"  # from the home card, since MODULE_INFO has no beta
    assert beta["contents"][0]["tutorials"] == ["first-steps-b", "tables"]
    assert beta["mixed"] == ["mixed"]
    assert not list((tree / "tutorials").rglob("*.order.yaml"))
    assert not (tree / "tutorials" / "modules.yaml").exists()
    assert not (tree / "tutorials" / "alpha").exists()  # the old module folder, .gitkeep and all
    assert not (tree / "tutorials" / "beta").exists()


def test_a_rename_carries_practice_for_and_links_with_it(tree: Path) -> None:
    """The renamed tutorial's own practice page, and a mixed set in the
    same module, must follow the rename — otherwise they point at the
    other module's tutorial of that name. check.py found this on the first
    real dry run."""
    run(tree, "--rename", "beta/first-steps=first-steps-b", "--apply")
    practice = (tree / "tutorials" / "first-steps-b" / "first-steps-b-practice.md").read_text()
    assert "practice_for: first-steps-b" in practice
    mixed = (tree / "tutorials" / "mixed" / "mixed.md").read_text()
    assert "  - first-steps-b\n" in mixed and "  - first-steps\n" not in mixed
    # and alpha's own practice page and link are untouched
    assert "practice_for: first-steps\n" in (tree / "tutorials" / "first-steps" / "first-steps-practice.md").read_text()
    assert "(tutorial:second-steps)" in (tree / "tutorials" / "first-steps" / "first-steps.md").read_text()


def test_every_old_address_gets_a_redirect(tree: Path) -> None:
    run(tree, "--rename", "beta/first-steps=first-steps-b", "--apply")
    redirects = yaml.safe_load((tree / "courses" / "redirects.yaml").read_text())
    assert redirects["tutorials/alpha/first-steps.html"] == "tutorials/first-steps.html"
    assert redirects["tutorials/alpha/first-steps-practice.html"] == "tutorials/first-steps-practice.html"
    assert redirects["tutorials/alpha/first-steps/v2026.08.01.1.html"] == "tutorials/first-steps/v2026.08.01.1.html"
    assert redirects["tutorials/beta/first-steps.html"] == "tutorials/first-steps-b.html"
    assert redirects["tutorials/beta/first-steps-practice.html"] == "tutorials/first-steps-b-practice.html"
    assert redirects["alpha.html"] == "courses/alpha.html"


def test_a_migrated_tree_reports_nothing_to_do(tree: Path) -> None:
    run(tree, "--rename", "beta/first-steps=first-steps-b", "--apply")
    again = run(tree)
    assert again.returncode == 0
    assert "nothing to migrate" in again.stdout
