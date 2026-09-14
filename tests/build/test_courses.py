"""Courses and series: reading order, the where-you-are tree, the all-tutorials page, archives, accumulation across series."""

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

class TestNavigation:
    def series(self, repo, count: int = 3, series: str = "s", module: str = "computational-methods",
               order: list[str] | None = None):
        for n in range(1, count + 1):
            path = tutorial_path(repo, f"t{n}", module)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(
                f'---\ntitle: "Tutorial {n}"\n'
                f'year: "2026-2027"\nversion: 2026.08.23.1\n---\n\nProse.\n'
            )
        set_order(repo, module, series,
                  order or [f"t{n}" for n in range(1, count + 1)])

    def page(self, repo, slug, module="computational-methods"):
        return (repo / "site" / "tutorials" / f"{slug}.html").read_text()

    def test_a_middle_tutorial_links_both_ways(self, repo):
        self.series(repo)
        b.build()
        page = self.page(repo, "t2")
        assert '<a class="dl-nav-prev" href="t1.html">Tutorial 1</a>' in page
        assert '<a class="dl-nav-next" href="t3.html">Tutorial 3</a>' in page

    def test_the_first_has_no_previous_and_the_last_no_next(self, repo):
        self.series(repo)
        b.build()
        assert "dl-nav-prev" not in self.page(repo, "t1")
        assert "dl-nav-next" in self.page(repo, "t1")
        assert "dl-nav-next" not in self.page(repo, "t3")
        assert "dl-nav-prev" in self.page(repo, "t3")

    def test_every_page_offers_the_way_back_to_the_contents(self, repo):
        self.series(repo)
        b.build()
        for slug in ("t1", "t2", "t3"):
            assert ('<a class="dl-nav-up" href="../all-tutorials.html">'
                    in self.page(repo, slug))

    def test_the_order_file_decides_the_sequence_not_the_filename(self, repo):
        self.series(repo, order=["t3", "t2", "t1"])
        b.build()
        assert '<a class="dl-nav-next" href="t2.html">' in self.page(repo, "t3")
        assert "dl-nav-next" not in self.page(repo, "t1")

    def test_two_series_do_not_link_into_each_other(self, repo):
        self.series(repo, count=2, series="one")
        path = tutorial_path(repo, "other")
        path.write_text(
            '---\ntitle: "Other"\n'
            'year: "2026-2027"\nversion: 2026.08.23.1\n---\n\nProse.\n'
        )
        set_order(repo, "computational-methods", "two", ["other"])
        b.build()
        assert "dl-nav-prev" not in self.page(repo, "other")
        assert "dl-nav-next" not in self.page(repo, "other")

    def test_a_tutorial_on_no_course_builds_and_is_noted(self, repo, capsys):
        # Not an error — a tutorial may be written before it is placed — but
        # never silent, since nothing on the site will link to it.
        self.series(repo, count=2, order=["t1"])
        b.build()
        page = self.page(repo, "t2")
        assert "dl-nav-prev" not in page and "dl-nav-next" not in page
        assert "dl-nav-up" in page
        assert "no course lists t2" in capsys.readouterr().err

    def test_an_id_with_no_tutorial_behind_it_stops_the_build_naming_the_course_and_line(self, repo):
        # The more dangerous direction: the file looks complete and the
        # series is quietly short.
        self.series(repo, count=2, order=["t1", "t2", "t3"])
        with pytest.raises(b.BuildError, match=r'courses/computational-methods\.yaml: the series "S" lists t3, but there is no folder tutorials/t3/'):
            b.build()

    def test_an_id_listed_twice_in_one_course_stops_the_build(self, repo):
        self.series(repo, count=2, order=["t1", "t2", "t1"])
        with pytest.raises(b.BuildError, match="lists t1 twice"):
            b.build()

    def test_a_draft_listed_in_a_course_is_skipped_with_a_note(self, repo, capsys):
        self.series(repo, count=2)
        path = tutorial_path(repo, "t2")
        path.write_text(path.read_text().replace("version: 2026.08.23.1", "status: draft\nversion: 2026.08.23.1"))
        b.build()
        assert "dl-nav-next" not in self.page(repo, "t1")
        assert "lists t2, which is a draft" in capsys.readouterr().err

    def test_a_practice_page_listed_in_a_course_stops_the_build(self, repo):
        self.series(repo, count=1)
        practice(repo, "t1")
        set_order(repo, COURSE, "s", ["t1", "t1-practice"])
        with pytest.raises(b.BuildError, match="lists t1-practice, which is a page of problems"):
            b.build()

    def test_order_left_in_the_frontmatter_stops_the_build(self, repo):
        # Half-migrated is worse than either state: the field would be
        # ignored in silence, and it is exactly the field somebody would edit.
        self.series(repo, count=1)
        path = tutorial_path(repo, "t1")
        path.write_text(path.read_text().replace("version: 2026.08.23.1", "order: 1\nversion: 2026.08.23.1"))
        with pytest.raises(b.BuildError, match="no longer belongs in frontmatter"):
            b.build()

    def test_a_placement_field_in_the_frontmatter_stops_the_build_and_says_to_delete_it(self, repo):
        # The mistake a contributor copying an old tutorial will make: the
        # build refuses rather than ignores, since an ignored field is a
        # field someone will keep writing.
        self.series(repo, count=1)
        path = tutorial_path(repo, "t1")
        path.write_text(path.read_text().replace("version: 2026.08.23.1", "module: computational-methods\nversion: 2026.08.23.1"))
        with pytest.raises(b.BuildError, match=r"module no longer belongs in frontmatter.*Delete the line"):
            b.build()


class TestTheSeriesRung:
    """The series level of the where-you-are tree (crumb_trail_html()) —
    what the Series panel used to show, now one rung of the tree, with no
    panel or button of its own."""

    def series(self, repo, count: int = 3, series: str = "s", module: str = "computational-methods",
               order: list[str] | None = None):
        for n in range(1, count + 1):
            path = tutorial_path(repo, f"t{n}", module)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(
                f'---\ntitle: "Tutorial {n}"\n'
                f'year: "2026-2027"\nversion: 2026.08.23.1\n---\n\nProse.\n'
            )
        set_order(repo, module, series,
                  order or [f"t{n}" for n in range(1, count + 1)])

    def rung(self, repo, slug, module="computational-methods") -> str:
        page = (repo / "site" / "tutorials" / f"{slug}.html").read_text()
        return re.search(
            r'<details class="dl-crumb-level dl-crumb-level-3" open>.*?</details>', page, re.S
        ).group(0)

    def test_it_lists_every_member_of_the_series_in_order(self, repo):
        self.series(repo)
        b.build()
        rung = self.rung(repo, "t2")
        assert rung.index("Tutorial 1") < rung.index("Tutorial 2") < rung.index("Tutorial 3")

    def test_the_current_tutorial_is_marked_and_not_linked(self, repo):
        self.series(repo)
        b.build()
        assert (
            '<div class="dl-crumb-current dl-crumb-level-4" role="listitem" aria-current="page">Tutorial 2</div>'
            in self.rung(repo, "t2")
        )

    def test_the_others_are_links_to_reach_them(self, repo):
        self.series(repo)
        b.build()
        rung = self.rung(repo, "t2")
        assert '<a href="t1.html">Tutorial 1</a>' in rung
        assert '<a href="t3.html">Tutorial 3</a>' in rung

    def test_the_order_file_decides_the_order_not_the_filename(self, repo):
        self.series(repo, order=["t3", "t2", "t1"])
        b.build()
        rung = self.rung(repo, "t2")
        assert rung.index("Tutorial 3") < rung.index("Tutorial 2") < rung.index("Tutorial 1")

    def test_there_is_no_series_button_or_panel(self, repo):
        self.series(repo)
        b.build()
        page = (repo / "site" / "tutorials" / "t2.html").read_text()
        assert "dl-seriesnav" not in page

    def test_a_tutorial_with_nowhere_in_a_series_to_sit_lists_only_itself(self, repo):
        # An archived tutorial: the same honest shape nav_for() already
        # gives it, since there is nowhere in the series to place it.
        write(repo, "Prose.\n")
        write(repo, "More prose.\n", slug="second")
        path = tutorial_path(repo, "sample")
        path.write_text(path.read_text().replace(
            "version: 2026.08.23.1\n", "version: 2026.08.23.1\nstatus: archived\n"))
        b.build()
        rung = self.rung(repo, "sample")
        assert 'aria-current="page"' in rung
        assert "second.html" not in rung

    def test_a_tutorial_on_no_course_has_no_course_or_series_rung(self, repo):
        write(repo, "Prose.\n")
        write(repo, "More prose.\n", slug="second")
        set_order(repo, COURSE, SERIES, ["second"])
        b.build()
        page = built(repo)
        trail = page[page.index('<nav class="dl-crumbtrail"'):page.index("</nav>")]
        assert "dl-crumb-level-2" not in trail and "dl-crumb-level-3" not in trail
        assert 'aria-current="page">A Title' in trail
        assert "<summary>All tutorials</summary>" in trail


class TestAllTutorialsPage:
    def test_it_is_written_at_the_site_root(self, repo):
        write(repo, "Prose.\n")
        b.build()
        assert (repo / "site" / "all-tutorials.html").is_file()

    def test_it_lists_every_tutorial_in_order(self, repo):
        for n in (1, 2):
            path = tutorial_path(repo, f"t{n}")
            path.write_text(
                f'---\ntitle: "Tutorial {n}"\n'
                f'year: "2026-2027"\nversion: 2026.08.23.1\n---\n\nProse.\n'
            )
        set_order(repo, "computational-methods", "s", ["t2", "t1"])
        b.build()
        index = (repo / "site" / "all-tutorials.html").read_text()
        assert index.index("Tutorial 2") < index.index("Tutorial 1")

    def test_the_links_reach_the_pages_they_name(self, repo):
        write(repo, "Prose.\n")
        b.build()
        index = (repo / "site" / "all-tutorials.html").read_text()
        assert 'href="tutorials/sample.html"' in index
        assert (repo / "site" / "tutorials" / "sample.html").is_file()

    def test_it_needs_no_python_runtime(self, repo):
        write(repo, "Prose.\n")
        b.build()
        assert manifest((repo / "site" / "all-tutorials.html").read_text())["cells"] == []

    def test_a_tutorial_with_cells_carries_its_progress_data_attributes(self, repo):
        # tutorial-runtime.js's progress indicator (planning/PROGRESS_INDICATORS.md)
        # reads these with no fetch.
        write(repo, CELL, slug="one")
        b.build()
        index = (repo / "site" / "all-tutorials.html").read_text()
        assert 'data-id="one"' in index
        assert 'data-cells="1"' in index

    def test_a_prose_only_tutorial_carries_no_progress_data_attributes(self, repo):
        write(repo, "Prose.\n", slug="one")
        b.build()
        index = (repo / "site" / "all-tutorials.html").read_text()
        assert "data-cells" not in index

    def module_headings(self, repo) -> list[str]:
        # By the heading rather than by substring: the slug also appears in
        # every href below it, so a plain `index()` finds the link, not the heading.
        page = (repo / "site" / "all-tutorials.html").read_text()
        return re.findall(r'<h2 class="dl-module-heading">(.*?)</h2>', page)

    def test_courses_appear_in_the_order_the_index_gives(self, repo):
        # Alphabetical by file name is not an order anybody chose.
        write(repo, "Prose.\n")
        write(repo, "Elsewhere.\n", slug="t1")
        course(repo, "zz-later-module", {"S": ["t1"]}, title="Later Module")
        index = repo / "courses" / "index.yaml"
        index.write_text("order:\n  - computational-methods\n  - zz-later-module\n")
        b.build()
        assert self.module_headings(repo) == ["Computational Methods", "Later Module"]

        index.write_text("order:\n  - zz-later-module\n  - computational-methods\n")
        b.build()
        assert self.module_headings(repo) == ["Later Module", "Computational Methods"]

    def test_a_course_the_index_leaves_out_lands_last_rather_than_breaking_the_page(self, repo):
        write(repo, "Prose.\n")
        write(repo, "Elsewhere.\n", slug="t1")
        course(repo, "zz-later-module", {"S": ["t1"]}, title="Later Module")
        (repo / "courses" / "index.yaml").write_text("order:\n  - zz-later-module\n")
        b.build()
        assert self.module_headings(repo) == ["Later Module", "Computational Methods"]

    def test_an_index_naming_a_course_with_no_file_stops_the_build(self, repo):
        write(repo, "Prose.\n")
        (repo / "courses" / "index.yaml").write_text("order:\n  - computational-methods\n  - nowhere\n")
        with pytest.raises(b.BuildError, match="there is no courses/nowhere.yaml"):
            b.build()

    def test_a_series_is_headed_by_its_name_not_its_filename(self, repo):
        # A module with two series shows a heading per series, and until one
        # had two nobody saw that the heading was the slug.
        write(repo, "Prose.\n")
        second = tutorial_path(repo, "looking-back")
        second.write_text(
            '---\ntitle: "Looking Back"\n'
            'year: "2026-2027"\nversion: 2026.08.23.1\n---\n\nProse.\n'
        )
        set_order(repo, "computational-methods", "Reflections and review", ["looking-back"])
        # `write` re-lists every markdown file it finds, so put the first series
        # back to just its own.
        set_order(repo, "computational-methods", "python-fundamentals", ["sample"])
        b.build()
        index = (repo / "site" / "all-tutorials.html").read_text()
        assert "<h3>Reflections and review</h3>" in index
        assert "<h3>reflections-and-review</h3>" not in index
        # And the key, not the heading, names the zip and the page's series.
        assert 'content="reflections-and-review"' in built(repo, "looking-back")

    def test_a_course_is_headed_by_the_title_in_its_file(self, repo):
        write(repo, "Prose.\n")
        b.build()
        assert ('<h2 class="dl-module-heading">Computational Methods</h2>'
                in (repo / "site" / "all-tutorials.html").read_text())

    def test_the_same_id_may_be_listed_in_two_courses(self, repo):
        """We chose not to share series by reference: listing an id twice
        is how a tutorial sits on two courses, and each course's list is
        its own to drift."""
        write(repo, "Prose.\n")
        course(repo, "zz-other", {"Also": ["sample"]}, title="Other Course")
        b.build()
        index = (repo / "site" / "all-tutorials.html").read_text()
        assert index.count('href="tutorials/sample.html"') == 2
        other = (repo / "site" / "zz-other.html").read_text()
        assert 'href="tutorials/sample.html"' in other
        # One page, one address: the tree it carries is the first course's.
        page = built(repo)
        trail = page[page.index('<nav class="dl-crumbtrail"'):page.index("</nav>")]
        assert 'data-courses="computational-methods zz-other"' in trail
        assert "<summary>Computational Methods</summary>" in trail
        assert "Other Course</summary>" not in trail

    def test_also_part_of_lists_the_other_courses_and_nothing_when_there_are_none(self, repo):
        write(repo, "# Sample\n\nProse.\n")
        b.build()
        assert "dl-also-part-of" not in built(repo)
        course(repo, "zz-other", {"Also": ["sample"]}, title="Other Course")
        b.build()
        page = built(repo)
        line = ('<p class="dl-also-part-of">This page is also part of '
                '<a href="../zz-other.html">Other Course</a>.</p>')
        assert line in page
        assert page.index("</h1>") < page.index(line) < page.index("Prose.")

    def test_a_repeated_title_is_warned_about_naming_both_and_their_courses(self, repo, capsys):
        # A warning, never an error: two courses may each have a "Joins".
        write(repo, "One.\n", slug="one")
        write(repo, "Two.\n", slug="two")
        b.build()
        err = capsys.readouterr().err
        assert 'two pages share the title "A Title"' in err
        assert "tutorials/one/one.md (on computational-methods)" in err
        assert "tutorials/two/two.md (on computational-methods)" in err

    def test_tutorials_covering_the_same_outcomes_are_reported(self, repo, capsys):
        # Coverage, not titles, is the signal; three shared outcomes is the line.
        claim = "covers:\n  a:\n    covers: [MIT-1.1, MIT-1.2, MIT-1.3]\n"
        for slug in ("one", "two"):
            path = write(repo, "## A\n\nProse.\n", slug=slug)
            add_frontmatter(path, claim)
        b.build()
        err = capsys.readouterr().err
        assert "tutorials/one/one.md and tutorials/two/two.md both cover MIT-1.1, MIT-1.2, MIT-1.3" in err
        add_frontmatter(write(repo, "## A\n\nProse.\n", slug="three"),
                        "covers:\n  a:\n    covers: [MIT-1.1, MIT-1.2]\n")
        b.build()
        reported = [line for line in capsys.readouterr().err.splitlines() if "both cover" in line]
        assert reported and all("three" not in line for line in reported)

    def test_no_tutorials_means_no_all_tutorials_page(self, repo):
        assert b.build() == []
        assert not (repo / "site" / "all-tutorials.html").exists()


class TestTheCrumbTrail:
    """crumb_trail_html() — the corner dock's expandable "all tutorials /
    module / series / tutorial / contents" tree, replacing the old
    plain-text crumbs for a real tutorial page."""

    def test_it_is_four_rungs_deep_the_last_opening_onto_the_sections(self, repo):
        write(repo, "## One\n\nProse.\n\n## Two\n\nProse.\n")
        b.build()
        page = built(repo)
        assert page.count('<details class="dl-crumb-level') == 4
        own = re.search(r'<details class="dl-crumb-level dl-crumb-level-4">.*?</details>', page, re.DOTALL).group(0)
        assert 'href="#one"' in own and 'href="#two"' in own
        assert "2 sections" in own

    def test_and_three_plus_a_plain_line_with_nothing_to_open(self, repo):
        write(repo, "Some prose.\n")
        b.build()
        page = built(repo)
        assert page.count('<details class="dl-crumb-level') == 3
        assert 'class="dl-crumb-current dl-crumb-level-4" role="listitem" aria-current="page">A Title</div>' in page

    def test_the_series_level_lists_its_siblings_and_marks_the_current_one(self, repo_with_assets):
        for slug, title in [("t1", "First One"), ("t2", "Second One")]:
            path = tutorial_path(repo_with_assets, slug)
            path.write_text(
                f'---\ntitle: "{title}"\n'
                f'year: "2026-2027"\nversion: 2026.08.23.1\n---\n\nProse.\n'
            )
        set_order(repo_with_assets, "computational-methods", "s", ["t1", "t2"])
        b.build()
        page = (repo_with_assets / "site" / "tutorials" / "t2.html").read_text()
        assert "First One" in page
        assert '<div class="dl-crumb-current dl-crumb-level-4" role="listitem" aria-current="page">Second One</div>' in page

    def series_rung(self, page: str) -> str:
        return re.search(
            r'<details class="dl-crumb-level dl-crumb-level-3" open>.*?</details>\s*</nav>', page, re.DOTALL
        ).group(0)

    def test_the_pages_own_rung_is_its_line_in_the_series_list(self, repo_with_assets):
        """The title carries the caret, so the page is not printed twice —
        once bold in the series list and once again as a rung beneath."""
        for slug, title, body in [("t1", "First One", "Prose.\n"), ("t2", "Second One", "## One\n\nA.\n\n## Two\n\nB.\n")]:
            path = tutorial_path(repo_with_assets, slug)
            path.write_text(
                f'---\ntitle: "{title}"\n'
                f'year: "2026-2027"\nversion: 2026.08.23.1\n---\n\n{body}'
            )
        set_order(repo_with_assets, "computational-methods", "s", ["t1", "t2"])
        b.build()
        page = (repo_with_assets / "site" / "tutorials" / "t2.html").read_text()
        series = self.series_rung(page)
        assert (
            '<div role="listitem"><details class="dl-crumb-level dl-crumb-level-4">'
            '<summary aria-current="page">Second One<span class="dl-crumb-count">2 sections</span></summary>'
        ) in series
        trail = page[page.index('<nav class="dl-crumbtrail"'):]
        trail = trail[:trail.index("</nav>")]
        assert trail.count(">Second One<") == 1

    def test_a_page_of_problems_sits_one_level_under_its_tutorial(self, repo):
        """Josh: "not sure where practice goes". Under the tutorial it
        belongs to: the tutorial's own rung lists its practice, and the
        practice page's tree shows it beneath a plain link back."""
        write(repo, "## One\n\nA.\n\n## Two\n\nB.\n", slug="one")
        path = tutorial_path(repo, "one-practice")
        path.write_text(
            FRONTMATTER.format(version="2026.08.23.1").replace(
                "version: 2026.08.23.1\n", "version: 2026.08.23.1\npractice_for: one\n")
            + "**1.** A question.\n"
        )
        b.build()
        own = re.search(r'<details class="dl-crumb-level dl-crumb-level-4">.*?</details>', built(repo, "one"), re.DOTALL).group(0)
        assert '<div role="listitem" class="dl-crumb-practice"><a href="one-practice.html">A Title</a></div>' in own
        series = self.series_rung(built(repo, "one-practice"))
        assert (
            '<div role="listitem"><a href="one.html">A Title</a><div role="list">'
            '<div class="dl-crumb-current dl-crumb-level-4" role="listitem" aria-current="page">A Title</div>'
            '</div></div>'
        ) in series
        assert "dl-crumb-practice" not in series

    def test_no_ul_or_li_reaches_the_page(self, repo):
        """The same trap report_doors_links() already avoided: a real <li>
        here would silently inflate any test elsewhere that counts a
        page's own list items, since this markup reaches every tutorial
        page. role="list"/"listitem" on plain divs instead. (The page has
        other, unrelated <ul>s of its own — the search results box, the
        contents fold — so this checks only the crumb trail's own markup.)
        """
        write(repo, "Some prose.\n")
        b.build()
        page = built(repo)
        start = page.index('<nav class="dl-crumbtrail"')
        end = page.index("</nav>", start) + len("</nav>")
        trail = page[start:end]
        assert "<ul" not in trail
        assert "<li" not in trail
        assert 'role="list"' in trail

    def test_a_downloadable_copy_drops_every_rung_that_links_to_another_file(
        self, repo_with_assets
    ):
        """Only the contents rung, whose links stay inside the file, may
        survive (TestTheContentsOfAPage covers that it does)."""
        write(repo_with_assets, "Some prose.\n")
        b.build(standalone=True)
        page = (repo_with_assets / "site" / "download" / "sample.html").read_text()
        # The standalone build inlines the whole stylesheet and runtime,
        # which name the classes in their own selectors — so only the
        # markup outside both is checked.
        markup = outside_style_and_script(page)
        for rung in ("dl-crumb-level-2", "dl-crumb-level-3", "All tutorials</summary>", "dl-crumb-practice"):
            assert rung not in markup


class TestArchivedTutorials:
    """Archiving retires a tutorial without deleting the page — deleting it
    would strand any student whose saved work is keyed to a URL that no
    longer exists."""

    def archive(self, repo, slug: str = "sample") -> Path:
        path = tutorial_path(repo, f"{slug}")
        path.write_text(path.read_text().replace(
            "version: 2026.08.23.1\n", "version: 2026.08.23.1\nstatus: archived\n"))
        # Still listed in the course file: the course's Archive is where it
        # goes, off the route.
        return path

    def test_an_archived_tutorial_is_still_built(self, repo):
        write(repo, "Prose.\n")
        write(repo, "More prose.\n", slug="second")
        self.archive(repo)
        b.build()
        page = repo / "site" / "tutorials" / "sample.html"
        assert page.is_file()

    def test_it_says_it_is_no_longer_part_of_the_course(self, repo):
        write(repo, "# Sample\n\nThe body of it.\n")
        write(repo, "More prose.\n", slug="second")
        self.archive(repo)
        b.build()
        page = (repo / "site" / "tutorials" / "sample.html").read_text()
        assert "no longer part of the course" in page
        # And the notice comes before the tutorial, not after it.
        assert page.index("dl-archived") < page.index("The body of it.")

    def test_it_is_not_in_the_reading_order(self, repo):
        write(repo, "Prose.\n")
        write(repo, "More prose.\n", slug="second")
        self.archive(repo)
        b.build()
        page = (repo / "site" / "tutorials" / "sample.html").read_text()
        assert "dl-nav-prev" not in page
        assert "dl-nav-next" not in page
        assert "dl-nav-up" in page

    def test_the_live_tutorials_close_up_behind_it(self, repo):
        # No gap, because the order file no longer lists the archived one.
        for slug in ("one", "two", "three"):
            write(repo, "Prose.\n", slug=slug)
        self.archive(repo, "two")
        b.build()
        page = (repo / "site" / "tutorials" / "one.html").read_text()
        assert "three.html" in page
        assert "two.html" not in page

    def test_the_contents_page_lists_it_under_an_archive_heading(self, repo):
        write(repo, "Prose.\n")
        write(repo, "More prose.\n", slug="second")
        self.archive(repo)
        b.build()
        index = (repo / "site" / "all-tutorials.html").read_text()
        assert "Archive" in index
        assert 'href="tutorials/sample.html"' in index
        # Below the live series, not among it.
        assert index.index("second.html") < index.index("sample.html")

    def test_one_no_course_lists_is_still_built_and_listed_nowhere(self, repo):
        write(repo, "Prose.\n")
        write(repo, "More prose.\n", slug="second")
        self.archive(repo)
        set_order(repo, COURSE, SERIES, ["second"])
        b.build()
        assert (repo / "site" / "tutorials" / "sample.html").is_file()
        assert "Archive" not in (repo / "site" / "all-tutorials.html").read_text()

    def test_an_unknown_status_stops_the_build(self, repo):
        path = write(repo, "Prose.\n")
        path.write_text(path.read_text().replace(
            "version: 2026.08.23.1\n", "version: 2026.08.23.1\nstatus: retired\n"))
        with pytest.raises(b.BuildError, match="status"):
            b.build()

    def test_it_teaches_nothing_the_map_can_point_at(self, repo):
        # A student picking a topic today cannot be sent there, so counting
        # it would make the map claim coverage nothing on the course provides.
        path = write(repo, "## A section\n\nProse.\n")
        path.write_text(path.read_text().replace(
            "version: 2026.08.23.1\n", "version: 2026.08.23.1\ncovers:\n  a-section:\n    covers: [MIT-1.4]\n"))
        write(repo, "More prose.\n", slug="second")
        b.build()
        taught = json.loads(re.search(
            r'<script type="application/json" id="dewlab-tree">(.*?)</script>',
            (repo / "site" / "tree.html").read_text(), re.DOTALL).group(1))
        assert next(n for n in taught["nodes"] if n["code"] == "MIT-1.4")["state"] == "taught"

        self.archive(repo)
        b.build()
        taught = json.loads(re.search(
            r'<script type="application/json" id="dewlab-tree">(.*?)</script>',
            (repo / "site" / "tree.html").read_text(), re.DOTALL).group(1))
        assert next(n for n in taught["nodes"] if n["code"] == "MIT-1.4")["state"] != "taught"


class TestTopicGroupsMatchRealTutorials:
    """Checked directly against real tutorials on disk, since a sandboxed
    build's tiny fixture set can't hold topic-groups.yaml to account —
    write_topics_page() itself only warns on a mismatch for exactly that reason."""

    def real_tutorial_keys(self) -> set[tuple[str, str]]:
        # A practice page is identified by its `practice_for:` field, not a
        # `-practice` suffix — `sql-practice` is itself a real, standalone
        # tutorial (dewlab/database-methods).
        seen = set()
        for path in (DEWLAB / "tutorials").glob("*/*.md"):
            if b.VERSION_FILE_RE.match(path.stem):
                continue
            front = path.read_text().split("---", 2)[1]
            meta = yaml.safe_load(front)
            if meta.get("practice_for"):
                continue
            seen.add(path.stem)
        return seen

    def groups(self) -> list[dict]:
        data = yaml.safe_load(
            (DEWLAB / "planning" / "curriculum" / "topic-groups.yaml").read_text()
        )
        return data["groups"]

    def test_every_real_tutorial_is_reachable_from_some_group(self):
        referenced = {
            ref for group in self.groups() for ref in group["tutorials"]
        }
        missing = self.real_tutorial_keys() - referenced
        assert not missing, f"not reachable from the topics page: {sorted(missing)}"

    def test_every_reference_names_a_tutorial_that_actually_exists(self):
        real = self.real_tutorial_keys()
        for group in self.groups():
            for ref in group["tutorials"]:
                assert isinstance(ref, str), f'{group["key"]!r} names {ref!r}; a group lists ids'
                assert ref in real, f'{group["key"]!r} names {ref}, which is not a tutorial'

    def test_every_group_has_a_key_a_name_an_intro_and_something_in_it(self):
        seen_keys = set()
        for group in self.groups():
            assert group.get("key"), "a group with no key can't be linked to"
            assert group["key"] not in seen_keys, f'duplicate group key {group["key"]!r}'
            seen_keys.add(group["key"])
            assert group.get("name"), f'{group["key"]}: no heading'
            assert group.get("intro", "").strip(), f'{group["key"]}: no intro'
            assert group.get("tutorials"), f'{group["key"]}: lists nothing'


class TestCrossSeriesGlossary:
    """A reference accumulates through the course the reader is following,
    series by series in the course file's order — planning/REFERENCE_PANEL.md."""

    def test_a_later_series_inherits_an_earlier_ones_glossary(self, repo):
        write(repo, "One.\n", slug="one")
        glossary(repo, "one", [{"term": "x", "kind": "concept", "definition": "First."}])
        write_in_series(repo, "Two.\n", slug="two", series="matrices")
        set_order(repo, "computational-methods", "matrices", ["two"])
        glossary(repo, "two", [{"term": "y", "kind": "concept", "definition": "Second."}])
        set_series_order(repo, "computational-methods", ["python-fundamentals", "matrices"])
        b.build()
        assert [e["term"] for e in manifest(built(repo, "two"))["glossary"]] == ["x", "y"]

    def test_the_course_files_order_decides_which_series_is_earlier(self, repo):
        write(repo, "One.\n", slug="one")
        glossary(repo, "one", [{"term": "x", "kind": "concept", "definition": "First."}])
        write_in_series(repo, "Two.\n", slug="two", series="matrices")
        glossary(repo, "two", [{"term": "y", "kind": "concept", "definition": "Second."}])
        set_series_order(repo, "computational-methods", ["matrices", "python-fundamentals"])
        b.build()
        assert [e["term"] for e in manifest(built(repo, "two"))["glossary"]] == ["y"]
        assert [e["term"] for e in manifest(built(repo, "one"))["glossary"]] == ["y", "x"]

    def test_accumulation_follows_the_course_file_order_and_not_another_course(self, repo):
        # Two courses share a tutorial; the other one puts a maths series
        # before it. The page is built for its first course, and carries
        # nothing from the other.
        write(repo, "One.\n", slug="one")
        glossary(repo, "one", [{"term": "x", "kind": "concept", "definition": "First."}])
        write(repo, "Two.\n", slug="two")
        glossary(repo, "two", [{"term": "y", "kind": "concept", "definition": "Second."}])
        set_order(repo, COURSE, SERIES, ["two"])
        course(repo, "zz-other", {"Maths": ["one"], "Then": ["two"]})
        b.build()
        assert [e["term"] for e in manifest(built(repo, "two"))["glossary"]] == ["y"]
