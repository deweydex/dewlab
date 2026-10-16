"""The page templates in docs/templates/ are real pages, and have to build.

They make one small series, "Running totals", on a course of their own: a
tutorial and its practice page, a closer look, a making task, a project
brief, and a mixed set. They are never published; this installs them in
the fixture's temporary repository and builds them there, so a template
that stops building fails here, not in the hands of the first author who
copies it.
"""

from __future__ import annotations

import pytest

import shutil

import yaml

from helpers import *  # noqa: F401,F403
from helpers import DEWLAB, b

TEMPLATES = DEWLAB / "docs" / "templates"


def pages():
    """Every template, without the README that lists them."""
    return [p for p in sorted(TEMPLATES.glob("*.md")) if p.name != "README.md"]


def frontmatter(path):
    return yaml.safe_load(path.read_text().split("---\n", 2)[1])


# Read off the templates themselves, so a new template is built without a
# change here: a page of problems follows its tutorial, a mixed set goes
# under `mixed:`, a context page follows what it names, the rest are a series.
def _kind(path):
    meta = frontmatter(path)
    if meta.get("practice_for"):
        return "practice"
    if meta.get("practice_across"):
        return "mixed"
    if meta.get("context_for"):
        return "context"
    return "series"


SERIES = [p.stem for p in pages() if _kind(p) == "series"]
MIXED = [p.stem for p in pages() if _kind(p) == "mixed"]


def install(repo):
    for path in pages():
        folder = frontmatter(path).get("practice_for") or path.stem
        (repo / "tutorials" / folder).mkdir(parents=True, exist_ok=True)
        shutil.copy(path, repo / "tutorials" / folder / path.name)
    course(repo, "templates", {"Running totals": SERIES}, mixed=MIXED)


@pytest.mark.advisory
def test_every_template_builds(repo):
    install(repo)
    b.build()
    for slug in [p.stem for p in pages()]:
        page = repo / "site" / "tutorials" / f"{slug}.html"
        assert page.is_file(), slug
