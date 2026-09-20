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
    and whether anything points back. A tutorial links to every page of
    problems that names it: its own practice page first, then any mixed set
    that draws on it, described as for later since a mixed set may assume
    tutorials this reader hasn't met yet. Two scenarios build the pages
    and check everything about them: a mixed set alone, on one course, and
    a tutorial with both kinds of page, on two courses. The rest are the
    ways a page can be wrong, one build error each."""

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

    def test_a_mixed_set_draws_on_two_of_three_tutorials_and_sits_off_their_reading_order(self, repo):
        write(repo, "One.\n", slug="one")
        write(repo, "Two.\n", slug="two")
        write(repo, "Zed.\n", slug="zed")  # sorts after "two", so it is not one's next
        self.practice(repo, "mixed", practice_across=["one", "two"])
        b.build()
        # The mixed set points back at every tutorial it draws on.
        text = (repo / "site" / "tutorials" / "mixed.html").read_text()
        assert "dl-practice-back" in text
        assert "one.html" in text and "two.html" in text
        # It is off the reading order. Asserted on the navigation rather
        # than the whole page: the tutorial does link to a mixed set that
        # names it, from the practice box at the end. It must not offer
        # that as the next thing to read.
        page = built(repo, "one")
        nav = re.findall(r"<nav class=\"dl-nav[^\"]*\">.*?</nav>", page, re.S)
        assert nav, "the tutorial has no navigation at all"
        assert any("two.html" in bar for bar in nav)
        assert not any("mixed.html" in bar for bar in nav)
        # It is not offered as this tutorial's own practice. Mixed-set links
        # were added after tutorials already linked to their own practice;
        # a reader still has to be able to tell the two apart.
        assert "dl-practice-mixed" in page
        assert "Practice problems for this tutorial" not in page
        assert "once more of the course is behind you" in page
        # The tutorial links to the mixed set that names it.
        assert "mixed.html" in page
        # It names the other tutorials the set draws on, so a reader can
        # tell whether it is for them yet.
        assert "It also draws on A Title" in page
        # A tutorial no mixed set names gets no such link.
        assert "dl-practice-mixed" not in built(repo, "zed")
        # The contents page lists mixed sets.
        index = (repo / "site" / "all-tutorials.html").read_text()
        assert "Mixed problems" in index
        assert "dl-mixed" in index
        assert "mixed.html" in index
        # No course file lists it under `mixed:`, so it goes with its first
        # tutorial's course.
        assert 'href="tutorials/mixed.html"' in (repo / "site" / "computational-methods.html").read_text()

    def test_a_tutorial_with_its_own_practice_and_a_mixed_set_links_both_and_follows_the_course_files(self, repo):
        # Two courses; the second lists both tutorials and puts the mixed
        # set under `mixed:`.
        write(repo, "One.\n", slug="one")
        write(repo, "Two.\n", slug="two")
        practice(repo, "one")
        practice(repo, "mixed", practice_across=["one", "two"])
        course(repo, "zz-other", {"S": ["one", "two"]}, mixed=["mixed"])
        b.build()
        page = built(repo, "one")
        # A page of problems is off the reading order: the next page after
        # `one` is `two`, not its own problems, which are linked another way.
        assert '<a class="dl-nav-next" href="two.html">' in page
        assert "one-practice.html" in page
        # The tutorial links to its problems, and they link back.
        assert "dl-practice-link" in page
        assert "dl-practice-back" in built(repo, "one-practice")
        # Both kinds of link appear together.
        assert "one-practice.html" in page and "mixed.html" in page
        # Its own practice page comes first: it is the one for now.
        assert page.index("one-practice.html") < page.index("mixed.html")
        # A practice page follows its tutorial onto every course: both
        # course pages link it, and its manifest says both.
        for course_page in ("computational-methods.html", "zz-other.html"):
            assert 'href="tutorials/one-practice.html"' in (repo / "site" / course_page).read_text()
        assert manifest(built(repo, "one-practice"))["courses"] == ["computational-methods", "zz-other"]
        # A mixed set is listed where the course file says, under `mixed:`.
        other = (repo / "site" / "zz-other.html").read_text()
        assert "Mixed problems" in other and 'href="tutorials/mixed.html"' in other
        assert 'href="tutorials/mixed.html"' not in (repo / "site" / "computational-methods.html").read_text()

    def _two_pages_claim_one_tutorial(self, repo):
        write(repo, "One.\n", slug="one")
        self.practice(repo, "one-practice", practice_for="one")
        self.practice(repo, "more-practice", practice_for="one")

    def _covers_declared_on_a_practice_page(self, repo):
        write(repo, "One.\n", slug="one")
        path = self.practice(repo, "one-practice", practice_for="one")
        path.write_text(path.read_text().replace(
            "practice_for: one\n",
            "practice_for: one\ncovers:\n  a-question:\n    covers: [MIT-1.1]\n"))

    def _mixed_naming_one_tutorial(self, repo):
        write(repo, "One.\n", slug="one")
        self.practice(repo, "mixed", practice_across=["one"])

    def _mixed_naming_a_non_mixed_page(self, repo):
        write(repo, "One.\n", slug="one")
        course(repo, "zz-other", {}, mixed=["one"])

    def _mixed_naming_a_nonexistent_slug(self, repo):
        write(repo, "One.\n", slug="one")
        self.practice(repo, "mixed", practice_across=["one", "nowhere"])

    def _mixed_naming_a_practice_page(self, repo):
        write(repo, "One.\n", slug="one")
        write(repo, "Two.\n", slug="two")
        self.practice(repo, "one-practice", practice_for="one")
        self.practice(repo, "mixed", practice_across=["two", "one-practice"])

    def _mixed_naming_itself(self, repo):
        write(repo, "One.\n", slug="one")
        self.practice(repo, "mixed", practice_across=["one", "mixed"])

    def _repeated_slug_in_practice_across(self, repo):
        write(repo, "One.\n", slug="one")
        write(repo, "Two.\n", slug="two")
        self.practice(repo, "mixed", practice_across=["one", "two", "one"])

    def _both_practice_for_and_practice_across(self, repo):
        write(repo, "One.\n", slug="one")
        write(repo, "Two.\n", slug="two")
        self.practice(repo, "mixed", practice_for="one",
                      practice_across=["one", "two"])

    ERRORS = {
        "two pages claim one tutorial": (_two_pages_claim_one_tutorial, "has one page of problems"),
        "a practice page declares covers": (_covers_declared_on_a_practice_page, "declares `covers:`"),
        "a mixed set names one tutorial": (_mixed_naming_one_tutorial, "practice_for is for"),
        "mixed: names a page that is not a mixed set": (_mixed_naming_a_non_mixed_page, "lists one under `mixed:`, and it is not a mixed problem set"),
        "a mixed set names a slug that does not exist": (_mixed_naming_a_nonexistent_slug, "there is no folder tutorials/nowhere/"),
        "a mixed set names a page of problems": (_mixed_naming_a_practice_page, "itself a page of problems"),
        "a mixed set names itself": (_mixed_naming_itself, "which is itself"),
        "a repeated slug in practice_across": (_repeated_slug_in_practice_across, "more than once"),
        "a page sets both practice_for and practice_across": (_both_practice_for_and_practice_across, "cannot do both"),
    }

    @pytest.mark.parametrize("case", sorted(ERRORS))
    def test_a_broken_page_of_problems_fails_the_build(self, repo, case):
        setup, match = self.ERRORS[case]
        setup(self, repo)
        with pytest.raises(b.BuildError, match=match):
            b.build()
