"""The page templates in docs/templates/ are real pages, and have to build.

They make one small series, "Running totals", on a course of their own: a
tutorial and its practice page, a closer look, a making task, a project
brief, and a mixed set. They are never published; this installs them in
the fixture's temporary repository and builds them there, so a template
that stops building fails here, not in the hands of the first author who
copies it.
"""

from __future__ import annotations

import re
import shutil

import yaml

from helpers import *  # noqa: F401,F403
from helpers import DEWLAB, b

TEMPLATES = DEWLAB / "docs" / "templates"
SERIES = ["running-totals", "where-the-total-starts", "a-total-you-can-see",
          "a-scale-model-of-the-solar-system"]
MIXED = ["mixed-running-totals"]


def pages():
    """Every template, without the README that lists them."""
    return [p for p in sorted(TEMPLATES.glob("*.md")) if p.name != "README.md"]


def frontmatter(path):
    return yaml.safe_load(path.read_text().split("---\n", 2)[1])


def install(repo):
    for path in pages():
        folder = frontmatter(path).get("practice_for") or path.stem
        (repo / "tutorials" / folder).mkdir(parents=True, exist_ok=True)
        shutil.copy(path, repo / "tutorials" / folder / path.name)
    course(repo, "templates", {"Running totals": SERIES}, mixed=MIXED)


def test_every_template_is_one_the_test_knows():
    """A new template has to join the series or the mixed list above, or it
    would be installed and never listed."""
    stems = {p.stem for p in pages()}
    practice = {p.stem for p in pages() if frontmatter(p).get("practice_for")}
    assert stems - practice == set(SERIES) | set(MIXED)


def test_every_template_builds(repo):
    install(repo)
    b.build()
    for slug in SERIES + MIXED + ["running-totals-practice"]:
        page = repo / "site" / "tutorials" / f"{slug}.html"
        assert page.is_file(), slug


def test_every_world_variant_has_its_own_cell_id():
    """A variant's cell id is the section's, then two hyphens and the world,
    and every world the page offers has one for each task."""
    for path in pages():
        worlds = list((frontmatter(path).get("worlds") or {}).keys())
        if not worlds:
            continue
        ids = re.findall(r"^id: (\S+)--(\S+)$", path.read_text(), re.M)
        assert ids, path.name
        by_task: dict[str, set[str]] = {}
        for task, world in ids:
            by_task.setdefault(task, set()).add(world)
        for task, found in by_task.items():
            assert found == set(worlds), (path.name, task)


def test_the_templates_readme_names_every_template():
    readme = (TEMPLATES / "README.md").read_text()
    for path in pages():
        assert f"({path.name})" in readme, path.name
