"""Links between tutorials, and ids being site-wide."""

from __future__ import annotations

import json
import re
import sys
import urllib.parse
import zipfile
from pathlib import Path

import pytest
import yaml

from helpers import *  # noqa: F401,F403
from helpers import DEWLAB, FRONTMATTER, CELL, COURSE, SERIES, b

class TestCrossLinks:
    """One page carrying every kind of link a tutorial can hold, built once;
    then the five ways a link or an id stops the build, one test each."""

    def test_every_kind_of_link_on_one_page_resolves_to_where_it_points(self, repo):
        write(repo,
              "See [other](tutorial:other).\n\n"
              "See [other](tutorial:other#a-heading).\n\n"
              "See [other](tutorial:other#only-cell).\n\n"
              "See [it](tutorial:twin).\n\n"
              "See [the docs](https://example.org/page).\n",
              slug="sample")
        write(repo, "## A heading\n\n" + CELL, slug="other")
        write(repo, "Mine.\n", slug="twin")
        course(repo, "zz-other", {"S": ["twin"]})
        b.build()
        # A link resolves to a relative href.
        assert 'href="other.html"' in built(repo, "sample")
        # An anchor is kept.
        assert 'href="other.html#a-heading"' in built(repo, "sample")
        # A cell id counts as an anchor.
        assert 'href="other.html#only-cell"' in built(repo, "sample")
        # A link names the same page from any course: `twin` is listed in
        # this course and in another, and its address is the same one.
        assert 'href="twin.html"' in built(repo, "sample")
        # An ordinary link is left alone.
        assert 'href="https://example.org/page"' in built(repo)

    def _unknown_slug(repo):
        write(repo, "See [nowhere](tutorial:nowhere).\n")

    def _unknown_anchor(repo):
        write(repo, "See [other](tutorial:other#absent).\n", slug="sample")
        write(repo, "Other.\n", slug="other")

    def _two_releases_share_a_version_date(repo):
        # A frozen release beside the tutorial is a *version* of it, so the
        # collision that matters is the version, not the id.
        write(repo, "One.\n", slug="same")
        (repo / "tutorials" / "same" / "v2026.08.23.1.md").write_text(
            FRONTMATTER.format(version="2026.08.23.1") + "Two.\n")

    def _a_second_file_with_an_existing_id(repo):
        # Two people create first-steps on two branches and both merge: the
        # filesystem refuses a second folder, and this catches the other
        # way it happens, a file of that name in another folder.
        write(repo, "One.\n", slug="first-steps")
        write(repo, "Two.\n", slug="other")
        (repo / "tutorials" / "other" / "first-steps.md").write_text(
            FRONTMATTER.format(version="2026.08.23.1") + "Again.\n")

    def _a_file_loose_under_tutorials(repo):
        write(repo, "One.\n")
        (repo / "tutorials" / "loose.md").write_text(FRONTMATTER.format(version="2026.08.23.1") + "Prose.\n")

    BROKEN_LINKS = {
        "an unknown tutorial slug": (_unknown_slug, "unknown tutorial"),
        "an unknown anchor": (_unknown_anchor, "no anchor"),
        "two releases sharing a version date": (_two_releases_share_a_version_date, "cannot share a date"),
        "a duplicate id in a second file": (
            _a_second_file_with_an_existing_id,
            r"tutorials/other/first-steps\.md: has the id first-steps, and so does tutorials/first-steps/first-steps\.md",
        ),
        "a .md file loose directly under tutorials/": (_a_file_loose_under_tutorials, "not inside a folder"),
    }

    @pytest.mark.parametrize("case", sorted(BROKEN_LINKS))
    def test_a_broken_link_or_id_fails_the_build(self, repo, case):
        setup, match = self.BROKEN_LINKS[case]
        setup(repo)
        with pytest.raises(b.BuildError, match=match):
            b.build()
