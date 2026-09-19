"""Courses and series: reading order, the where-you-are tree, the all-tutorials page, archives, accumulation across series, and the topic groups file against the real tutorials.

Each test here is one scenario — a small repository, built once (or built
again after one thing changes) — carrying every fact that scenario
establishes. The failure paths, one per error, stay one test each.
"""

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


def write_titled(repo, slug: str, title: str, body: str = "Prose.\n") -> Path:
    """A tutorial with a title of its own, listed by no course until a
    course file names it (write() lists everything it has written)."""
    path = tutorial_path(repo, slug)
    path.write_text(
        f'---\ntitle: "{title}"\n'
        f'year: "2026-2027"\nversion: 2026.08.23.1\n---\n\n{body}'
    )
    return path


def series(repo, count: int = 3, series: str = "s", order: list[str] | None = None):
    """t1 … t<count>, titled "Tutorial n", under the series `series` of
    the default course, in `order` (the numbered order unless given)."""
    for n in range(1, count + 1):
        write_titled(repo, f"t{n}", f"Tutorial {n}")
    set_order(repo, COURSE, series, order or [f"t{n}" for n in range(1, count + 1)])


def page(repo, slug: str) -> str:
    return (repo / "site" / "tutorials" / f"{slug}.html").read_text()


def series_rung(repo, slug: str) -> str:
    """The series level of the page's where-you-are tree."""
    return re.search(
        r'<details class="dl-crumb-level dl-crumb-level-3" open>.*?</details>', page(repo, slug), re.S
    ).group(0)


def archive(repo, slug: str = "sample") -> Path:
    path = tutorial_path(repo, slug)
    path.write_text(path.read_text().replace(
        "version: 2026.08.23.1\n", "version: 2026.08.23.1\nstatus: archived\n"))
    # Still listed in the course file: the course's Archive is where it
    # goes, off the route.
    return path


class TestNavigation:
    """A course of two series — three tutorials in one, one in the other
    — for previous/next/up between the pages, the series rung of the
    where-you-are tree (crumb_trail_html()), and the headings on the
    contents page; then the same files with the course file's order
    reversed. The placement mistakes that stop the build, and the ones
    that only print a note, are one test each."""

    def test_a_course_of_two_series_links_and_lists_its_pages_in_the_course_files_order(self, repo):
        series(repo)
        write_titled(repo, "looking-back", "Looking Back")
        set_order(repo, COURSE, "Reflections and review", ["looking-back"])
        b.build()
        # A middle tutorial links both ways.
        middle = page(repo, "t2")
        assert '<a class="dl-nav-prev" href="t1.html">Tutorial 1</a>' in middle
        assert '<a class="dl-nav-next" href="t3.html">Tutorial 3</a>' in middle
        # The first has no previous and the last no next.
        assert "dl-nav-prev" not in page(repo, "t1")
        assert "dl-nav-next" in page(repo, "t1")
        assert "dl-nav-next" not in page(repo, "t3")
        assert "dl-nav-prev" in page(repo, "t3")
        # Every page offers the way back to the contents.
        for slug in ("t1", "t2", "t3"):
            assert ('<a class="dl-nav-up" href="../all-tutorials.html">'
                    in page(repo, slug))
        # The series rung lists every member of the series, in order.
        rung = series_rung(repo, "t2")
        assert rung.index("Tutorial 1") < rung.index("Tutorial 2") < rung.index("Tutorial 3")
        # The current tutorial is marked and not linked.
        assert (
            '<div class="dl-crumb-current dl-crumb-level-4" role="listitem" aria-current="page">Tutorial 2</div>'
            in rung
        )
        # The others are links to reach them.
        assert '<a href="t1.html">Tutorial 1</a>' in rung
        assert '<a href="t3.html">Tutorial 3</a>' in rung
        # Two series do not link into each other.
        assert "dl-nav-prev" not in page(repo, "looking-back")
        assert "dl-nav-next" not in page(repo, "looking-back")
        # A series is headed by its name, not its key: until a course had
        # two series nobody saw that the heading was the key.
        index = (repo / "site" / "all-tutorials.html").read_text()
        assert "<h3>Reflections and review</h3>" in index
        assert "<h3>reflections-and-review</h3>" not in index
        # And the key, not the heading, names the zip and the page's series.
        assert 'content="reflections-and-review"' in built(repo, "looking-back")

        # The course file decides the sequence, not the filename.
        set_order(repo, COURSE, "s", ["t3", "t2", "t1"])
        b.build()
        assert '<a class="dl-nav-next" href="t2.html">' in page(repo, "t3")
        assert "dl-nav-next" not in page(repo, "t1")
        rung = series_rung(repo, "t2")
        assert rung.index("Tutorial 3") < rung.index("Tutorial 2") < rung.index("Tutorial 1")
        # The contents page lists them in that order too.
        index = (repo / "site" / "all-tutorials.html").read_text()
        assert index.index("Tutorial 2") < index.index("Tutorial 1")

    def test_a_tutorial_on_no_course_builds_and_is_noted(self, repo, capsys):
        # Not an error — a tutorial may be written before it is placed — but
        # never silent, since nothing on the site will link to it.
        series(repo, count=2, order=["t1"])
        b.build()
        unplaced = page(repo, "t2")
        assert "dl-nav-prev" not in unplaced and "dl-nav-next" not in unplaced
        assert "dl-nav-up" in unplaced
        assert "no course lists t2" in capsys.readouterr().err

    def test_an_id_with_no_tutorial_behind_it_stops_the_build_naming_the_course_and_line(self, repo):
        # The more dangerous direction: the file looks complete and the
        # series is quietly short.
        series(repo, count=2, order=["t1", "t2", "t3"])
        with pytest.raises(b.BuildError, match=r'courses/computational-methods\.yaml: the series "S" lists t3, but there is no folder tutorials/t3/'):
            b.build()

    def test_an_id_listed_twice_in_one_course_stops_the_build(self, repo):
        series(repo, count=2, order=["t1", "t2", "t1"])
        with pytest.raises(b.BuildError, match="lists t1 twice"):
            b.build()

    def test_a_draft_listed_in_a_course_is_skipped_with_a_note(self, repo, capsys):
        series(repo, count=2)
        path = tutorial_path(repo, "t2")
        path.write_text(path.read_text().replace("version: 2026.08.23.1", "status: draft\nversion: 2026.08.23.1"))
        b.build()
        assert "dl-nav-next" not in page(repo, "t1")
        assert "lists t2, which is a draft" in capsys.readouterr().err

    def test_a_practice_page_listed_in_a_course_stops_the_build(self, repo):
        series(repo, count=1)
        practice(repo, "t1")
        set_order(repo, COURSE, "s", ["t1", "t1-practice"])
        with pytest.raises(b.BuildError, match="lists t1-practice, which is a page of problems"):
            b.build()

    def test_order_left_in_the_frontmatter_stops_the_build(self, repo):
        # Half-migrated is worse than either state: the field would be
        # ignored in silence, and it is exactly the field somebody would edit.
        series(repo, count=1)
        path = tutorial_path(repo, "t1")
        path.write_text(path.read_text().replace("version: 2026.08.23.1", "order: 1\nversion: 2026.08.23.1"))
        with pytest.raises(b.BuildError, match="no longer belongs in frontmatter"):
            b.build()

    def test_a_placement_field_in_the_frontmatter_stops_the_build_and_says_to_delete_it(self, repo):
        # The mistake a contributor copying an old tutorial will make: the
        # build refuses rather than ignores, since an ignored field is a
        # field someone will keep writing.
        series(repo, count=1)
        path = tutorial_path(repo, "t1")
        path.write_text(path.read_text().replace("version: 2026.08.23.1", "module: computational-methods\nversion: 2026.08.23.1"))
        with pytest.raises(b.BuildError, match=r"module no longer belongs in frontmatter.*Delete the line"):
            b.build()


class TestAllTutorialsPage:
    """The contents page at the site root. One prose tutorial, from an
    empty site to a page on two courses (with its own tree and
    downloadable copy checked on the way); the order courses come in;
    and the notes the build prints about titles and outcomes that
    repeat."""

    def test_one_prose_tutorial_from_an_empty_site_to_a_page_on_two_courses(self, repo_with_assets):
        repo = repo_with_assets
        # No tutorials means no all-tutorials page.
        assert b.build() == []
        assert not (repo / "site" / "all-tutorials.html").exists()

        # A heading in the body, so the page has an <h1> to place the
        # "also part of" line under.
        write(repo, "# Sample\n\nProse.\n")
        b.build(standalone=True)
        # The contents page is written at the site root.
        assert (repo / "site" / "all-tutorials.html").is_file()
        index = (repo / "site" / "all-tutorials.html").read_text()
        # Its links reach the pages they name.
        assert 'href="tutorials/sample.html"' in index
        assert (repo / "site" / "tutorials" / "sample.html").is_file()
        # It needs no Python runtime.
        assert manifest(index)["cells"] == []
        # The course is headed by the title in its file.
        assert '<h2 class="dl-module-heading">Computational Methods</h2>' in index
        # A prose-only tutorial carries no progress data attributes.
        assert "data-cells" not in index
        page = built(repo)
        # On no other course, the page has no "also part of" line.
        assert "dl-also-part-of" not in page
        # Its tree is three rungs plus a plain line with nothing to open.
        assert page.count('<details class="dl-crumb-level') == 3
        assert 'class="dl-crumb-current dl-crumb-level-4" role="listitem" aria-current="page">A Title</div>' in page
        # No <ul> or <li> reaches the page: the same trap
        # report_doors_links() already avoided. A real <li> here would
        # silently inflate any test elsewhere that counts a page's own
        # list items, since this markup reaches every tutorial page.
        # role="list"/"listitem" on plain divs instead. (The page has
        # other, unrelated <ul>s of its own — the search results box, the
        # contents fold — so this checks only the crumb trail's own markup.)
        start = page.index('<nav class="dl-crumbtrail"')
        end = page.index("</nav>", start) + len("</nav>")
        trail = page[start:end]
        assert "<ul" not in trail
        assert "<li" not in trail
        assert 'role="list"' in trail
        # A downloadable copy drops every rung that links to another file;
        # only the contents rung, whose links stay inside the file, may
        # survive (TestTheContentsOfAPage covers that it does). The
        # standalone build inlines the whole stylesheet and runtime, which
        # name the classes in their own selectors — so only the markup
        # outside both is checked.
        markup = outside_style_and_script((repo / "site" / "download" / "sample.html").read_text())
        for rung in ("dl-crumb-level-2", "dl-crumb-level-3", "All tutorials</summary>", "dl-crumb-practice"):
            assert rung not in markup

        # The same id may be listed in two courses. We chose not to share
        # series by reference: listing an id twice is how a tutorial sits
        # on two courses, and each course's list is its own to drift.
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
        # And "also part of" now lists the other course, under the title.
        line = ('<p class="dl-also-part-of">This page is also part of '
                '<a href="../zz-other.html">Other Course</a>.</p>')
        assert line in page
        assert page.index("</h1>") < page.index(line) < page.index("Prose.")

    def course_headings(self, repo) -> list[str]:
        # By the heading rather than by substring: the id also appears in
        # every href below it, so a plain `index()` finds the link, not the
        # heading. (The class keeps its older name, dl-module-heading.)
        page = (repo / "site" / "all-tutorials.html").read_text()
        return re.findall(r'<h2 class="dl-module-heading">(.*?)</h2>', page)

    def test_courses_appear_in_the_order_the_index_gives_and_one_it_leaves_out_lands_last(self, repo):
        # Alphabetical by file name is not an order anybody chose.
        write(repo, "Prose.\n")
        write(repo, "Elsewhere.\n", slug="t1")
        course(repo, "zz-later-module", {"S": ["t1"]}, title="Later Module")
        index = repo / "courses" / "index.yaml"
        index.write_text("order:\n  - computational-methods\n  - zz-later-module\n")
        b.build()
        assert self.course_headings(repo) == ["Computational Methods", "Later Module"]

        index.write_text("order:\n  - zz-later-module\n  - computational-methods\n")
        b.build()
        assert self.course_headings(repo) == ["Later Module", "Computational Methods"]

        # A course the index leaves out lands last rather than breaking the page.
        index.write_text("order:\n  - zz-later-module\n")
        b.build()
        assert self.course_headings(repo) == ["Later Module", "Computational Methods"]

    def test_an_index_naming_a_course_with_no_file_stops_the_build(self, repo):
        write(repo, "Prose.\n")
        (repo / "courses" / "index.yaml").write_text("order:\n  - computational-methods\n  - nowhere\n")
        with pytest.raises(b.BuildError, match="there is no courses/nowhere.yaml"):
            b.build()

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


class TestTheCrumbTrail:
    """crumb_trail_html() — the corner dock's expandable "all tutorials /
    course / series / tutorial / contents" tree on pages with something
    in them: a series whose pages have sections, a cell and a page of
    problems, and a series of two plain pages for the siblings line.
    (The plain page's tree, and what a downloadable copy drops, are in
    TestAllTutorialsPage's one-tutorial scenario.)"""

    def series_rung_to_nav(self, page: str) -> str:
        return re.search(
            r'<details class="dl-crumb-level dl-crumb-level-3" open>.*?</details>\s*</nav>', page, re.DOTALL
        ).group(0)

    def test_a_series_whose_pages_have_sections_a_cell_and_a_page_of_problems(self, repo_with_assets):
        repo = repo_with_assets
        write_titled(repo, "t1", "First One")
        write_titled(repo, "t2", "Second One", "## One\n\nA.\n\n## Two\n\nB.\n")
        path = tutorial_path(repo, "one")
        path.write_text(FRONTMATTER.format(version="2026.08.23.1") + "## One\n\nA.\n\n## Two\n\nB.\n\n" + CELL)
        path = tutorial_path(repo, "one-practice")
        path.write_text(
            FRONTMATTER.format(version="2026.08.23.1").replace(
                "version: 2026.08.23.1\n", "version: 2026.08.23.1\npractice_for: one\n")
            + "**1.** A question.\n"
        )
        set_order(repo, COURSE, "s", ["t1", "t2", "one"])
        b.build()
        # The tree is four rungs deep, the last opening onto the sections.
        page = built(repo, "one")
        assert page.count('<details class="dl-crumb-level') == 4
        own = re.search(r'<details class="dl-crumb-level dl-crumb-level-4">.*?</details>', page, re.DOTALL).group(0)
        assert 'href="#one"' in own and 'href="#two"' in own
        assert "2 sections" in own
        # A tutorial with cells carries its progress data attributes on
        # the contents page: tutorial-runtime.js's progress indicator
        # reads these with no fetch.
        index = (repo / "site" / "all-tutorials.html").read_text()
        assert 'data-id="one"' in index
        assert 'data-cells="1"' in index
        # A page of problems sits one level under its tutorial. Josh: "not
        # sure where practice goes". Under the tutorial it belongs to: the
        # tutorial's own rung lists its practice, and the practice page's
        # tree shows it beneath a plain link back.
        assert '<div role="listitem" class="dl-crumb-practice"><a href="one-practice.html">A Title</a></div>' in own
        series = self.series_rung_to_nav(built(repo, "one-practice"))
        assert (
            '<div role="listitem"><a href="one.html">A Title</a><div role="list">'
            '<div class="dl-crumb-current dl-crumb-level-4" role="listitem" aria-current="page">A Title</div>'
            '</div></div>'
        ) in series
        assert "dl-crumb-practice" not in series
        # The page's own rung is its line in the series list: the title
        # carries the caret, so the page is not printed twice — once bold
        # in the series list and once again as a rung beneath.
        page = (repo / "site" / "tutorials" / "t2.html").read_text()
        series = self.series_rung_to_nav(page)
        assert (
            '<div role="listitem"><details class="dl-crumb-level dl-crumb-level-4">'
            '<summary aria-current="page">Second One<span class="dl-crumb-count">2 sections</span></summary>'
        ) in series
        trail = page[page.index('<nav class="dl-crumbtrail"'):]
        trail = trail[:trail.index("</nav>")]
        assert trail.count(">Second One<") == 1

    def test_the_series_level_lists_its_siblings_and_marks_the_current_one(self, repo_with_assets):
        for slug, title in [("t1", "First One"), ("t2", "Second One")]:
            write_titled(repo_with_assets, slug, title)
        set_order(repo_with_assets, "computational-methods", "s", ["t1", "t2"])
        b.build()
        page = (repo_with_assets / "site" / "tutorials" / "t2.html").read_text()
        assert "First One" in page
        assert '<div class="dl-crumb-current dl-crumb-level-4" role="listitem" aria-current="page">Second One</div>' in page


class TestArchivedTutorials:
    """Archiving retires a tutorial without deleting the page — deleting it
    would strand any student whose saved work is keyed to an address that
    no longer exists. One scenario, built before and after archiving: two
    archived tutorials among live ones (still built, off the reading
    order, under the contents page's Archive heading, a notice before
    the body, the live ones closing up, the map no longer counting what
    they cover); then an archived one that no course lists; and the
    status the build refuses."""

    def test_archived_tutorials_are_built_off_the_route_and_listed_under_archive(self, repo):
        # `sample` teaches an outcome; one, two and three are a live series.
        path = write(repo, "# Sample\n\nThe body of it.\n\n## A section\n\nProse.\n")
        path.write_text(path.read_text().replace(
            "version: 2026.08.23.1\n", "version: 2026.08.23.1\ncovers:\n  a-section:\n    covers: [MIT-1.4]\n"))
        write(repo, "More prose.\n", slug="second")
        for slug in ("one", "two", "three"):
            write(repo, "Prose.\n", slug=slug)
        b.build()
        # Live, the map counts what it covers.
        taught = json.loads(re.search(
            r'<script type="application/json" id="dewlab-tree">(.*?)</script>',
            (repo / "site" / "tree.html").read_text(), re.DOTALL).group(1))
        assert next(n for n in taught["nodes"] if n["code"] == "MIT-1.4")["state"] == "taught"

        archive(repo)
        archive(repo, "two")
        b.build()
        # An archived tutorial is still built.
        path = repo / "site" / "tutorials" / "sample.html"
        assert path.is_file()
        page = path.read_text()
        # It says it is no longer part of the course, before the tutorial,
        # not after it.
        assert "no longer part of the course" in page
        assert page.index("dl-archived") < page.index("The body of it.")
        # It is not in the reading order.
        assert "dl-nav-prev" not in page
        assert "dl-nav-next" not in page
        assert "dl-nav-up" in page
        # Its series rung lists only itself: the same honest shape nav_for()
        # gives it, since there is nowhere in the series to place it.
        rung = series_rung(repo, "sample")
        assert 'aria-current="page"' in rung
        assert "second.html" not in rung
        # The contents page lists it under an Archive heading.
        index = (repo / "site" / "all-tutorials.html").read_text()
        assert "Archive" in index
        assert 'href="tutorials/sample.html"' in index
        # Below the live series, not among it.
        assert index.index("second.html") < index.index("sample.html")
        # The live tutorials close up behind an archived one — no gap: the
        # course file still lists it, and the build takes it off the route.
        page = (repo / "site" / "tutorials" / "one.html").read_text()
        assert "three.html" in page
        assert "two.html" not in page
        # It teaches nothing the map can point at: a student picking a
        # topic today cannot be sent there, so counting it would make the
        # map claim coverage nothing on the course provides.
        taught = json.loads(re.search(
            r'<script type="application/json" id="dewlab-tree">(.*?)</script>',
            (repo / "site" / "tree.html").read_text(), re.DOTALL).group(1))
        assert next(n for n in taught["nodes"] if n["code"] == "MIT-1.4")["state"] != "taught"

    def test_one_no_course_lists_is_still_built_listed_nowhere_and_has_no_course_or_series_rung(self, repo):
        write(repo, "Prose.\n")
        write(repo, "More prose.\n", slug="second")
        archive(repo)
        set_order(repo, COURSE, SERIES, ["second"])
        b.build()
        assert (repo / "site" / "tutorials" / "sample.html").is_file()
        assert "Archive" not in (repo / "site" / "all-tutorials.html").read_text()
        # A tutorial on no course has no course or series rung.
        page = built(repo)
        trail = page[page.index('<nav class="dl-crumbtrail"'):page.index("</nav>")]
        assert "dl-crumb-level-2" not in trail and "dl-crumb-level-3" not in trail
        assert 'aria-current="page">A Title' in trail
        assert "<summary>All tutorials</summary>" in trail

    def test_an_unknown_status_stops_the_build(self, repo):
        path = write(repo, "Prose.\n")
        path.write_text(path.read_text().replace(
            "version: 2026.08.23.1\n", "version: 2026.08.23.1\nstatus: retired\n"))
        with pytest.raises(b.BuildError, match="status"):
            b.build()


class TestTopicGroupsMatchRealTutorials:
    """Checked directly against real tutorials on disk, since a sandboxed
    build's tiny fixture set can't hold topic-groups.yaml to account —
    write_topics_page() itself only warns on a mismatch for exactly that reason."""

    def real_tutorial_keys(self) -> set[str]:
        # A practice page is identified by its `practice_for:` field, not a
        # `-practice` suffix — `sql-practice` is itself a real, standalone
        # tutorial.
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
    series by series in the course file's order — planning/REFERENCE_PANEL.md.
    Two series with a term each, built in each order; and a tutorial on
    two courses, which carries nothing from the other one."""

    def test_a_later_series_inherits_an_earlier_ones_glossary_and_the_course_file_says_which_is_earlier(self, repo):
        write(repo, "One.\n", slug="one")
        glossary(repo, "one", [{"term": "x", "kind": "concept", "definition": "First."}])
        write_in_series(repo, "Two.\n", slug="two", series="matrices")
        set_order(repo, "computational-methods", "matrices", ["two"])
        glossary(repo, "two", [{"term": "y", "kind": "concept", "definition": "Second."}])
        set_series_order(repo, "computational-methods", ["python-fundamentals", "matrices"])
        b.build()
        assert [e["term"] for e in manifest(built(repo, "two"))["glossary"]] == ["x", "y"]

        # The course file's order decides which series is earlier.
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
