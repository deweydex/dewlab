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
    def test_a_link_resolves_to_a_relative_href(self, repo):
        write(repo, "See [other](tutorial:other).\n", slug="sample")
        write(repo, "Other.\n", slug="other")
        b.build()
        assert 'href="other.html"' in built(repo, "sample")

    def test_an_anchor_is_kept(self, repo):
        write(repo, "See [other](tutorial:other#a-heading).\n", slug="sample")
        write(repo, "## A heading\n", slug="other")
        b.build()
        assert 'href="other.html#a-heading"' in built(repo, "sample")

    def test_a_cell_id_counts_as_an_anchor(self, repo):
        write(repo, "See [other](tutorial:other#only-cell).\n", slug="sample")
        write(repo, CELL, slug="other")
        b.build()
        assert 'href="other.html#only-cell"' in built(repo, "sample")

    def test_an_unknown_slug_fails_the_build(self, repo):
        write(repo, "See [nowhere](tutorial:nowhere).\n")
        with pytest.raises(b.BuildError, match="unknown tutorial"):
            b.build()

    def test_an_unknown_anchor_fails_the_build(self, repo):
        write(repo, "See [other](tutorial:other#absent).\n", slug="sample")
        write(repo, "Other.\n", slug="other")
        with pytest.raises(b.BuildError, match="no anchor"):
            b.build()

    def test_two_releases_with_one_version_fail_the_build(self, repo):
        # A frozen release beside the tutorial is a *version* of it, so the
        # collision that matters is the version, not the id.
        write(repo, "One.\n", slug="same")
        (repo / "tutorials" / "same" / "v2026.08.23.1.md").write_text(
            FRONTMATTER.format(version="2026.08.23.1") + "Two.\n")
        with pytest.raises(b.BuildError, match="cannot share a date"):
            b.build()

    def test_a_second_file_with_an_existing_id_stops_the_build_and_names_the_other(self, repo):
        # Two people create first-steps on two branches and both merge: the
        # filesystem refuses a second folder, and this catches the other
        # way it happens, a file of that name in another folder.
        write(repo, "One.\n", slug="first-steps")
        write(repo, "Two.\n", slug="other")
        (repo / "tutorials" / "other" / "first-steps.md").write_text(
            FRONTMATTER.format(version="2026.08.23.1") + "Again.\n")
        with pytest.raises(b.BuildError, match=r"tutorials/other/first-steps\.md: has the id first-steps, and so does tutorials/first-steps/first-steps\.md"):
            b.build()

    def test_a_file_loose_under_tutorials_stops_the_build(self, repo):
        write(repo, "One.\n")
        (repo / "tutorials" / "loose.md").write_text(FRONTMATTER.format(version="2026.08.23.1") + "Prose.\n")
        with pytest.raises(b.BuildError, match="not inside a folder"):
            b.build()

    def test_a_link_names_the_same_page_from_any_course(self, repo):
        write(repo, "See [it](tutorial:twin).\n", slug="here")
        write(repo, "Mine.\n", slug="twin")
        course(repo, "zz-other", {"S": ["twin"]})
        b.build()
        assert 'href="twin.html"' in built(repo, "here")

    def test_an_ordinary_link_is_left_alone(self, repo):
        write(repo, "See [the docs](https://example.org/page).\n")
        b.build()
        assert 'href="https://example.org/page"' in built(repo)
