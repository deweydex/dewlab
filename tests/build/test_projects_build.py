"""Choose your project (DECISIONS_LOG 7.288): a page's `projects:`
frontmatter names each project with its card and table fields, and each
project is a `<div class="dl-project" data-project="…">` in the page that
opens with its `##` heading. The build writes the cards and the table just
before the first project, gives each project its anchor, and tells the
contents page which cells are whose."""

from __future__ import annotations

import re

import pytest

from helpers import *  # noqa: F401,F403
from helpers import b


def fields(title: str, **extra: str) -> str:
    lines = [f"    title: {title}", f"    question: Why {title.lower()}?",
             f"    make: a {title.lower()} maker", "    maths: slopes", "    data: some numbers"]
    lines += [f"    {key}: {value}" for key, value in extra.items()]
    return "\n".join(lines) + "\n"


PROJECTS = ("projects:\n  sums:\n" + fields("Sums") + "  squares:\n" + fields("Squares")
            + "  own:\n" + fields("Your own", own="true"))


def page(repo, body: str, projects: str = PROJECTS) -> None:
    path = write(repo, body)
    head, rest = path.read_text().split("\n---\n", 1)
    path.write_text(f"{head}\n{projects}---\n{rest}")


def project(key: str, heading: str = "", cell: str = "") -> str:
    heading = heading or f"## The {key} project"
    code = f"\n\n```python exec\nid: {cell}\nx = 1\n```\n" if cell else ""
    return f'<div class="dl-project" data-project="{key}">\n\n{heading}\n\nSome *words*.{code}\n</div>\n\n'


ALL = project("sums", cell="sums-1") + project("squares", cell="squares-1") + project("own")


class TestRendering:
    def test_the_cards_and_table_come_just_before_the_first_project(self, repo):
        page(repo, "# A page\n\nThe shared part.\n\n" + ALL)
        b.build()
        html = built(repo)
        assert html.index("The shared part") < html.index('id="dl-project-chooser"') < html.index('id="project-sums"')
        assert html.count('class="dl-project-card"') == 2
        assert html.count('class="dl-project-card dl-project-card-own"') == 1
        assert '<a class="dl-project-card" href="#project-squares" data-project="squares">' in html
        assert "<td>Why squares?</td>" in html

    def test_each_project_has_its_anchor_and_its_markdown(self, repo):
        page(repo, "# A page\n\n" + ALL)
        b.build()
        html = built(repo)
        assert '<div class="dl-project" data-project="own" id="project-own" data-project-own="true">' in html
        assert "<em>words</em>" in html

    def test_the_contents_page_knows_which_cells_are_whose(self, repo):
        page(repo, "# A page\n\n```python exec\nid: shared\nx = 0\n```\n\n" + ALL)
        b.build()
        tutorial = b.load(next((repo / "tutorials").rglob("sample.md")))
        assert tutorial.project_cells == {"sums": ["sums-1"], "squares": ["squares-1"], "own": []}


class TestRefusals:
    @pytest.mark.parametrize("body, projects, match", [
        (ALL, "projects:\n  Big One:\n" + fields("Big"), "not an id like"),
        (ALL, "projects:\n  sums:\n    title: Sums\n", "has no `question:`"),
        (project("sums") + project("squares"), PROJECTS, "own with no project div"),
        (ALL + project("extra"), PROJECTS, "'extra', which is not in"),
        ('<div class="dl-project" data-project="sums">\n\n## Sums\n\n' + project("squares")
         + "</div>\n\n" + project("own"), PROJECTS, "starts inside"),
        (ALL, "projects:\n  sums:\n" + fields("Sums", picture="missing.svg"), "not in the tutorial's folder"),
    ])
    def test_the_build_says_what_is_wrong(self, repo, body, projects, match):
        page(repo, "# A page\n\n" + body, projects)
        with pytest.raises(b.BuildError, match=re.escape(match)):
            b.build()


class TestShapeThatOnlyGetsANote:
    """How a page lays its projects out is the author's. These build, and the
    ones that cost the reader something say so."""

    def test_divs_in_a_different_order_from_projects_build_and_say_so(self, repo, capsys):
        page(repo, "# A page\n\n" + project("squares") + project("sums") + project("own"))
        b.build()
        assert "not in the order `projects:` lists them" in capsys.readouterr().err
        html = built(repo)
        assert html.index('id="project-squares"') < html.index('id="project-sums"')
        assert html.index('data-project="sums"') < html.index('data-project="squares"')

    def test_a_project_without_a_heading_builds_and_says_what_the_reader_loses(self, repo, capsys):
        page(repo, "# A page\n\n" + project("sums", heading="No heading here.")
             + project("squares") + project("own"))
        b.build()
        err = capsys.readouterr().err
        assert "project 'sums' does not open with a `## ` heading" in err
        assert "project 'squares'" not in err
        assert "No heading here." in built(repo)

    def test_two_own_projects_both_get_the_wide_card(self, repo):
        page(repo, "# A page\n\n" + ALL,
             PROJECTS.replace("  squares:\n", "  squares:\n    own: true\n"))
        b.build()
        assert built(repo).count('class="dl-project-card dl-project-card-own"') == 2

    def test_the_own_project_may_come_anywhere_in_the_list(self, repo):
        first = "projects:\n  own:\n" + fields("Your own", own="true") + "  sums:\n" + fields("Sums")
        page(repo, "# A page\n\n" + project("own") + project("sums"), first)
        b.build()
        html = built(repo)
        assert html.count('class="dl-project-card dl-project-card-own"') == 1
        assert html.count('class="dl-project-card"') == 1

    def test_a_project_with_no_maths_or_data_leaves_those_cells_blank(self, repo):
        lean = "projects:\n  sums:\n    title: Sums\n    question: Why sums?\n    make: a sum\n"
        page(repo, "# A page\n\n" + project("sums"), lean)
        b.build()
        assert "<td>Why sums?</td><td>a sum</td><td></td><td></td>" in built(repo)
