"""Context pages: optional background reading beside a tutorial."""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from helpers import (
    FRONTMATTER, b, built, course, glossary, manifest, practice, tutorial_path, write,
)


class TestContextPages:
    """A context page names the tutorial(s) it gives background for with
    `context_for:`. It is off the reading order the way a practice page is:
    each tutorial it names links to it after its practice link, and it links
    back at the top. One scenario builds a context page for two tutorials
    and checks everything about it; one checks the single-tutorial wording;
    the rest are the ways a context page can be wrong, one build error each."""

    def context(self, repo, slug: str, front: str = "", context_for=None) -> Path:
        """`tutorials/<slug>/<slug>.md` with `context_for:` — one id as a
        string, several as a list — and any extra frontmatter lines."""
        path = tutorial_path(repo, slug)
        if isinstance(context_for, list):
            front = "context_for:\n" + "".join(f"  - {s}\n" for s in context_for) + front
        elif context_for is not None:
            front = f"context_for: {context_for}\n" + front
        path.write_text(
            FRONTMATTER.format(version="2026.08.23.1").replace(
                "---\n\n", front + "---\n\n", 1)
            + "Where this idea is used.\n"
        )
        return path

    def test_a_context_page_for_two_tutorials_is_linked_both_ways_and_sits_off_the_route(self, repo, capsys):
        write(repo, "One.\n", slug="one")
        write(repo, "Two.\n", slug="two")
        practice(repo, "one")
        glossary(repo, "one", [{"term": "x", "kind": "concept", "definition": "First."}])
        glossary(repo, "two", [{"term": "y", "kind": "concept", "definition": "Second."}])
        self.context(repo, "why", context_for=["one", "two"])
        glossary(repo, "why", [{"term": "z", "kind": "concept", "definition": "Aside."}])
        b.build()

        # The tutorial links to it, after its own practice link.
        page = built(repo, "one")
        assert '<div class="dl-context-link"><p><a href="why.html">A Title</a> — ' in page
        assert "background reading, for when you want to know more" in page
        assert "Nothing in it is needed to finish this tutorial." in page
        assert page.index('class="dl-practice-link"') < page.index('class="dl-context-link"')
        assert "dl-context-link" in built(repo, "two")

        # It links back to both, at the top, and says it is optional.
        why = built(repo, "why")
        assert '<p class="dl-context-back">Background for <a href="one.html">' in why
        assert 'and <a href="two.html">' in why
        assert "Nothing here is needed to finish those tutorials." in why
        assert "dl-context-link" not in why and "dl-practice-link" not in why

        # Off the reading order: one's next is two, and why has no prev/next.
        assert '<a class="dl-nav-next" href="two.html">' in page
        nav = re.findall(r"<nav class=\"dl-nav[^\"]*\">.*?</nav>", why, re.S)
        assert not any("dl-nav-next" in bar or "dl-nav-prev" in bar for bar in nav)

        # Its crumbs sit under its first tutorial's series, and that
        # tutorial's own rung lists it with a tag.
        assert manifest(why)["courses"] == ["computational-methods"]
        assert "Python fundamentals" in why
        assert 'class="dl-crumb-context"' in page and "dl-crumb-tag" in page

        # Its reference is the union of its tutorials', then its own terms.
        assert [e["term"] for e in manifest(why)["glossary"]][-1] == "z"
        assert {e["term"] for e in manifest(why)["glossary"]} == {"x", "y", "z"}

        # The contents page lists it beside each tutorial, tagged.
        index = (repo / "site" / "all-tutorials.html").read_text()
        assert index.count('class="dl-contents-context" href="tutorials/why.html"') == 2
        assert '<span class="dl-contents-tag">context</span>' in index

        # Not a search result, not on the reference index, not noted as
        # missing from a course.
        search = json.loads((repo / "site" / "assets" / "search-index.json").read_text())
        assert "why" not in {entry["id"] for entry in search}
        reference = json.loads((repo / "site" / "assets" / "reference-index.json").read_text())
        assert "z" not in {entry["term"] for entry in reference}
        assert "no course lists why" not in capsys.readouterr().err

    def test_a_context_page_for_one_tutorial_says_that_tutorial(self, repo):
        write(repo, "One.\n", slug="one")
        self.context(repo, "why", context_for="one")
        b.build()
        why = built(repo, "why")
        assert '<p class="dl-context-back">Background for <a href="one.html">A Title</a>. ' in why
        assert "Nothing here is needed to finish that tutorial." in why
        assert "dl-context-link" in built(repo, "one")

    def _unknown_id(self, repo):
        write(repo, "One.\n", slug="one")
        self.context(repo, "why", context_for=["one", "nowhere"])

    def _names_a_practice_page(self, repo):
        write(repo, "One.\n", slug="one")
        practice(repo, "one")
        self.context(repo, "why", context_for="one-practice")

    def _names_another_context_page(self, repo):
        write(repo, "One.\n", slug="one")
        self.context(repo, "why", context_for="one")
        self.context(repo, "why-more", context_for="why")

    def _names_itself(self, repo):
        write(repo, "One.\n", slug="one")
        self.context(repo, "why", context_for=["one", "why"])

    def _names_an_id_twice(self, repo):
        write(repo, "One.\n", slug="one")
        self.context(repo, "why", context_for=["one", "one"])

    def _declares_covers(self, repo):
        write(repo, "One.\n", slug="one")
        self.context(repo, "why", context_for="one",
                     front="covers:\n  a-section:\n    covers: [MIT-1.1]\n")

    def _listed_in_a_course(self, repo):
        write(repo, "One.\n", slug="one")
        self.context(repo, "why", context_for="one")
        course(repo, "zz-other", {"S": ["one", "why"]})

    def _also_sets_practice_for(self, repo):
        write(repo, "One.\n", slug="one")
        self.context(repo, "why", context_for="one", front="practice_for: one\n")

    def _also_sets_practice_across(self, repo):
        write(repo, "One.\n", slug="one")
        write(repo, "Two.\n", slug="two")
        self.context(repo, "why", context_for="one",
                     front="practice_across:\n  - one\n  - two\n")

    ERRORS = {
        "names an id with no tutorial": (_unknown_id, "there is no folder tutorials/nowhere/"),
        "names a practice page": (_names_a_practice_page, "which is a page of problems"),
        "names another context page": (_names_another_context_page, "itself a context page"),
        "names itself": (_names_itself, "naming why, which is itself"),
        "names an id twice": (_names_an_id_twice, "more than once"),
        "declares covers": (_declares_covers, "is a context page and declares `covers:`"),
        "is listed in a course": (_listed_in_a_course, "which is a context page"),
        "also sets practice_for": (_also_sets_practice_for, "one page cannot be both"),
        "also sets practice_across": (_also_sets_practice_across, "one page cannot be both"),
    }

    @pytest.mark.parametrize("case", sorted(ERRORS))
    def test_a_broken_context_page_fails_the_build(self, repo, case):
        setup, match = self.ERRORS[case]
        setup(self, repo)
        with pytest.raises(b.BuildError, match=match):
            b.build()
