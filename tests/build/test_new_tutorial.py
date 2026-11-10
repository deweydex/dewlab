"""new.py: starting a tutorial from the templates. What it makes has to
build, and its solutions have to run, or the first thing a new author meets
is a page that is broken before they have typed a word."""

from __future__ import annotations

import datetime
import importlib
import sys

import pytest

from helpers import *  # noqa: F401,F403
from helpers import DEWLAB, b, course

DAY = datetime.date(2026, 11, 10)


@pytest.fixture()
def new(repo):
    sys.path.insert(0, str(DEWLAB))
    return importlib.reload(importlib.import_module("new"))


def test_it_makes_a_tutorial_and_its_practice_page_that_build_and_run(repo, new):
    written = new.create("adding-up", 'Adding "up" as you go', day=DAY)
    assert [p.name for p in written] == ["adding-up.md", "adding-up-practice.md"]
    page, practice = (p.read_text() for p in written)
    assert 'title: "Adding \\"up\\" as you go"' in page and "version: 2026.11.10.1" in page
    assert 'year: "2026-2027"' in page and '\n# Adding "up" as you go\n' in page
    assert "practice_for: adding-up" in practice and "— Practice" in practice

    course(repo, COURSE, {"start": ["adding-up"]})
    b.build()
    assert (repo / "site" / "tutorials" / "adding-up.html").is_file()
    assert (repo / "site" / "tutorials" / "adding-up-practice.html").is_file()
    assert b.solutions.check_site() == 2


def test_a_school_year_runs_from_august(new):
    assert new.school_year(datetime.date(2026, 7, 31)) == "2025-2026"
    assert new.school_year(datetime.date(2026, 8, 1)) == "2026-2027"


def test_it_refuses_an_id_that_is_taken_or_is_not_an_id_and_writes_nothing(repo, new):
    new.create("adding-up", "A title", practice=False, day=DAY)
    assert not (repo / "tutorials" / "adding-up" / "adding-up-practice.md").exists()
    before = (repo / "tutorials" / "adding-up" / "adding-up.md").read_text()
    with pytest.raises(ValueError, match="already there"):
        new.create("adding-up", "Another title", day=DAY)
    assert (repo / "tutorials" / "adding-up" / "adding-up.md").read_text() == before
    for bad in ("Adding Up", "adding_up", "-adding"):
        with pytest.raises(ValueError, match="cannot be an id"):
            new.create(bad, "A title", day=DAY)
    assert sorted(p.name for p in (repo / "tutorials").iterdir()) == ["adding-up"]
