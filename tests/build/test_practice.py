"""Pages of problems: one per tutorial, or drawing on several."""

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

class TestPagesOfProblems:
    """A practice page belongs to a tutorial, or draws on several. Both
    shapes are the same mechanically; what differs is what they point at,
    and whether anything points back."""

    def practice(self, repo, slug: str, **frontmatter) -> Path:
        path = tutorial_path(repo, f"{slug}")
        extra = "".join(
            f"{key}: {value}\n" if not isinstance(value, list)
            else f"{key}:\n" + "".join(f"  - {v}\n" for v in value)
            for key, value in frontmatter.items()
        )
        path.write_text(
            FRONTMATTER.format(version="2026.08.23.1").replace(
                "version: 2026.08.23.1\n", f"version: 2026.08.23.1\n{extra}")
            + "**1.** A question.\n"
        )
        listed = sorted(
            p.stem for p in path.parent.parent.glob("*/*.md")
            if "practice_for" not in p.read_text()
            and "practice_across" not in p.read_text()
        )
        set_order(repo, "computational-methods", "python-fundamentals", listed)
        return path

    def test_a_page_of_problems_is_off_the_reading_order(self, repo):
        write(repo, "One.\n", slug="one")
        write(repo, "Two.\n", slug="two")
        self.practice(repo, "one-practice", practice_for="one")
        b.build()
        page = built(repo, "one")
        assert "two.html" in page
        assert "dl-nav-next" in page
        assert "one-practice.html" in page

    def test_the_tutorial_links_to_its_problems_and_back(self, repo):
        write(repo, "One.\n", slug="one")
        self.practice(repo, "one-practice", practice_for="one")
        b.build()
        assert "dl-practice-link" in built(repo, "one")
        assert "dl-practice-back" in built(repo, "one-practice")

    def test_two_pages_cannot_claim_the_same_tutorial(self, repo):
        write(repo, "One.\n", slug="one")
        self.practice(repo, "one-practice", practice_for="one")
        self.practice(repo, "more-practice", practice_for="one")
        with pytest.raises(b.BuildError, match="has one page of problems"):
            b.build()

    def test_a_page_of_problems_declaring_coverage_is_an_error(self, repo):
        write(repo, "One.\n", slug="one")
        path = self.practice(repo, "one-practice", practice_for="one")
        path.write_text(path.read_text().replace(
            "practice_for: one\n",
            "practice_for: one\ncovers:\n  a-question:\n    covers: [MIT-1.1]\n"))
        with pytest.raises(b.BuildError, match="declares `covers:`"):
            b.build()

    def test_a_mixed_set_draws_on_several_tutorials(self, repo):
        write(repo, "One.\n", slug="one")
        write(repo, "Two.\n", slug="two")
        self.practice(repo, "mixed", practice_across=["one", "two"])
        page = (repo / "site" / "tutorials" / "mixed.html")
        b.build()
        text = page.read_text()
        assert "dl-practice-back" in text
        assert "one.html" in text and "two.html" in text

    def test_a_mixed_set_is_off_the_reading_order(self, repo):
        # Asserted on the navigation rather than the whole page: the tutorial
        # does link to a mixed set that names it, from the practice box at
        # the end. It must not offer that as the next thing to read.
        write(repo, "One.\n", slug="one")
        write(repo, "Two.\n", slug="two")
        self.practice(repo, "mixed", practice_across=["one", "two"])
        b.build()
        page = built(repo, "one")
        nav = re.findall(r"<nav class=\"dl-nav[^\"]*\">.*?</nav>", page, re.S)
        assert nav, "the tutorial has no navigation at all"
        assert any("two.html" in bar for bar in nav)
        assert not any("mixed.html" in bar for bar in nav)

    def test_a_mixed_set_is_not_offered_as_this_tutorial_own_practice(self, repo):
        # Mixed-set links were added after tutorials already linked to their
        # own practice; a reader still has to be able to tell the two apart.
        write(repo, "One.\n", slug="one")
        write(repo, "Two.\n", slug="two")
        self.practice(repo, "mixed", practice_across=["one", "two"])
        b.build()
        page = built(repo, "one")
        assert "dl-practice-mixed" in page
        assert "Practice problems for this tutorial" not in page
        assert "once more of the course is behind you" in page

    def test_the_contents_page_lists_mixed_sets(self, repo):
        write(repo, "One.\n", slug="one")
        write(repo, "Two.\n", slug="two")
        self.practice(repo, "mixed", practice_across=["one", "two"])
        b.build()
        index = (repo / "site" / "all-tutorials.html").read_text()
        assert "Mixed problems" in index
        assert "dl-mixed" in index
        assert "mixed.html" in index

    def test_a_mixed_set_naming_one_tutorial_is_an_error(self, repo):
        write(repo, "One.\n", slug="one")
        self.practice(repo, "mixed", practice_across=["one"])
        with pytest.raises(b.BuildError, match="practice_for is for"):
            b.build()

    def test_a_practice_page_follows_its_tutorial_onto_every_course(self, repo):
        # Two courses, one tutorial, one practice page: both course pages
        # link it, and its manifest says both.
        write(repo, "One.\n", slug="one")
        practice(repo, "one")
        course(repo, "zz-other", {"S": ["one"]})
        b.build()
        for page in ("computational-methods.html", "zz-other.html"):
            assert 'href="tutorials/one-practice.html"' in (repo / "site" / page).read_text()
        assert manifest(built(repo, "one-practice"))["courses"] == ["computational-methods", "zz-other"]

    def test_a_mixed_set_is_listed_where_the_course_file_says_under_mixed(self, repo):
        write(repo, "One.\n", slug="one")
        write(repo, "Two.\n", slug="two")
        practice(repo, "mixed", practice_across=["one", "two"])
        course(repo, "zz-other", {"S": ["one", "two"]}, mixed=["mixed"])
        b.build()
        other = (repo / "site" / "zz-other.html").read_text()
        assert "Mixed problems" in other and 'href="tutorials/mixed.html"' in other
        assert 'href="tutorials/mixed.html"' not in (repo / "site" / "computational-methods.html").read_text()

    def test_a_mixed_set_no_course_lists_goes_with_its_first_tutorials_course(self, repo):
        write(repo, "One.\n", slug="one")
        write(repo, "Two.\n", slug="two")
        practice(repo, "mixed", practice_across=["one", "two"])
        b.build()
        assert 'href="tutorials/mixed.html"' in (repo / "site" / "computational-methods.html").read_text()

    def test_mixed_naming_a_page_that_is_not_a_mixed_set_is_an_error(self, repo):
        write(repo, "One.\n", slug="one")
        course(repo, "zz-other", {}, mixed=["one"])
        with pytest.raises(b.BuildError, match="lists one under `mixed:`, and it is not a mixed problem set"):
            b.build()

    def test_a_mixed_set_naming_a_slug_that_does_not_exist_is_an_error(self, repo):
        write(repo, "One.\n", slug="one")
        self.practice(repo, "mixed", practice_across=["one", "nowhere"])
        with pytest.raises(b.BuildError, match="there is no folder tutorials/nowhere/"):
            b.build()

    def test_a_mixed_set_naming_a_page_of_problems_is_an_error(self, repo):
        write(repo, "One.\n", slug="one")
        write(repo, "Two.\n", slug="two")
        self.practice(repo, "one-practice", practice_for="one")
        self.practice(repo, "mixed", practice_across=["two", "one-practice"])
        with pytest.raises(b.BuildError, match="itself a page of problems"):
            b.build()

    def test_a_mixed_set_naming_itself_is_an_error(self, repo):
        write(repo, "One.\n", slug="one")
        self.practice(repo, "mixed", practice_across=["one", "mixed"])
        with pytest.raises(b.BuildError, match="which is itself"):
            b.build()

    def test_a_repeated_slug_is_an_error(self, repo):
        write(repo, "One.\n", slug="one")
        write(repo, "Two.\n", slug="two")
        self.practice(repo, "mixed", practice_across=["one", "two", "one"])
        with pytest.raises(b.BuildError, match="more than once"):
            b.build()

    def test_a_page_cannot_be_both_kinds_at_once(self, repo):
        write(repo, "One.\n", slug="one")
        write(repo, "Two.\n", slug="two")
        self.practice(repo, "mixed", practice_for="one",
                      practice_across=["one", "two"])
        with pytest.raises(b.BuildError, match="cannot do both"):
            b.build()


class TestPracticeIsReachable:
    """A tutorial links to every page of problems that names it: its own
    practice page first, then any mixed set that draws on it, described as
    for later since a mixed set may assume tutorials this reader hasn't met yet."""

    def practice(self, repo, slug: str, **frontmatter) -> Path:
        return TestPagesOfProblems().practice(repo, slug, **frontmatter)

    def test_a_tutorial_links_to_a_mixed_set_that_names_it(self, repo):
        write(repo, "One.\n", slug="one")
        write(repo, "Two.\n", slug="two")
        self.practice(repo, "mixed", practice_across=["one", "two"])
        b.build()
        page = built(repo, "one")
        assert "dl-practice-mixed" in page
        assert "mixed.html" in page

    def test_it_names_the_other_tutorials_the_set_draws_on(self, repo):
        """So a reader can tell whether it is for them yet."""
        write(repo, "One.\n", slug="one")
        write(repo, "Two.\n", slug="two")
        self.practice(repo, "mixed", practice_across=["one", "two"])
        b.build()
        page = built(repo, "one")
        assert "It also draws on A Title" in page

    def test_a_tutorial_no_mixed_set_names_gets_no_such_link(self, repo):
        write(repo, "One.\n", slug="one")
        write(repo, "Two.\n", slug="two")
        write(repo, "Three.\n", slug="three")
        self.practice(repo, "mixed", practice_across=["one", "two"])
        b.build()
        assert "dl-practice-mixed" not in built(repo, "three")

    def test_both_kinds_of_link_appear_together(self, repo):
        write(repo, "One.\n", slug="one")
        write(repo, "Two.\n", slug="two")
        self.practice(repo, "one-practice", practice_for="one")
        self.practice(repo, "mixed", practice_across=["one", "two"])
        b.build()
        page = built(repo, "one")
        assert "one-practice.html" in page and "mixed.html" in page
        # Its own practice page comes first: it is the one for now.
        assert page.index("one-practice.html") < page.index("mixed.html")
