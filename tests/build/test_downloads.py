"""Downloadable copies and the series and course archives."""

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

class TestTheDownloadableCopy:
    """One tutorial with a cell and no maths, built with `standalone=True`:
    the copy is written beside the site, the page links to it, and
    everything it needs to run travels inside it. Then the two things that
    must not travel: the version list, and data the copy cannot reach."""

    def standalone(self, repo) -> str:
        return (repo / "site" / "download" / "sample.html").read_text()

    def test_a_tutorial_with_a_cell_gets_a_self_contained_copy_the_page_links_to(self, repo_with_assets):
        write(repo_with_assets, "Some prose, and no maths at all.\n\n```python exec\nid: c\n1 + 1\n```\n")
        b.build(standalone=True)
        # It is written beside the site.
        assert (repo_with_assets / "site" / "download" / "sample.html").is_file()
        # The page links to it.
        page = built(repo_with_assets)
        assert 'href="../download/sample.html"' in page
        copy = self.standalone(repo_with_assets)
        # The stylesheet travels inside it.
        assert "--dl-navy" in copy
        # The runtime travels inside it, as a classic script.
        assert "pyodide.js" in copy
        assert len(copy) > 300_000  # confirms the bundle itself is embedded, not a stub
        # It marks itself as standalone.
        assert manifest(copy)["standalone"] is True
        # Nothing is left pointing outside the file.
        assert '<link rel="stylesheet"' not in copy
        assert '<script type="module"' not in copy
        # The Python tools travel inside it.
        assert "toolsSource" in copy
        assert "def check(" in copy
        # A tutorial without maths does not carry the maths fonts.
        assert ".katex-html" not in copy
        assert "data:font/woff2;base64," in copy  # the accessible fonts still do

    def test_the_version_list_does_not_travel_with_it(self, repo_with_assets):
        # Only the default gets a downloadable copy, so the other releases
        # are not on the reader's disk; a picker offering them would be
        # worse than no picker.
        for version in ("2026.06.02.1", "2026.09.15.1"):
            folder = repo_with_assets / "tutorials" / "sample"
            folder.mkdir(parents=True, exist_ok=True)
            (folder / f"v{version}.md").write_text(
                '---\ntitle: "The Tutorial"\n'
                f'year: "2026-2027"\nversion: {version}\n'
                "status: live\n---\n\nProse.\n"
            )
        set_order(repo_with_assets, "computational-methods", "python-fundamentals",
                  ["sample"])
        b.build(standalone=True)
        hosted = (repo_with_assets / "site" / "tutorials" / "sample.html").read_text()
        assert len(manifest(hosted)["versions"]) == 2
        assert "versions" not in manifest(self.standalone(repo_with_assets))

    def test_it_warns_when_a_tutorial_loads_data_it_cannot_carry(self, repo_with_assets, capsys):
        write(repo_with_assets, '```python exec\nid: c\ndf = await load_csv("x.csv")\n```\n')
        b.build(standalone=True)
        assert "cannot reach" in capsys.readouterr().err


class TestTheSeriesArchive:
    """A series of two maths tutorials becomes one archive, with a
    start-here page and a download button on the contents page, and each
    copy inside it runs, carries its fonts, and has no navigation; a
    practice page follows its tutorial into it and is counted. A series of
    one is offered in the singular; a build without the copies offers
    nothing at all. The two helpers that need no build (the filename slug,
    the readable size) are here too."""

    def two_tutorials(self, repo):
        for n in (1, 2):
            path = tutorial_path(repo, f"t{n}")
            path.write_text(
                f'---\ntitle: "T{n}"\n'
                f'year: "2026-2027"\nversion: 2026.08.23.1\n---\n\nAn equation: $x^2$.\n'
            )
        set_order(repo, "computational-methods", "Core skills", ["t1", "t2"])

    def archive(self, repo) -> Path:
        return repo / "site" / "download" / "computational-methods-core-skills.zip"

    def test_a_series_of_two_becomes_one_archive_with_a_start_here_page_the_contents_page_offers(self, repo_with_assets):
        self.two_tutorials(repo_with_assets)
        b.build(standalone=True)
        # A series is gathered into one archive.
        assert self.archive(repo_with_assets).is_file()
        with zipfile.ZipFile(self.archive(repo_with_assets)) as archive:
            # It holds every downloadable copy in the series.
            assert sorted(archive.namelist()) == [
                "computational-methods-core-skills/0-start-here.html",
                "computational-methods-core-skills/01-t1.html",
                "computational-methods-core-skills/02-t2.html",
            ]
            page = archive.read("computational-methods-core-skills/01-t1.html").decode()
            start_here = archive.read(
                "computational-methods-core-skills/0-start-here.html"
            ).decode()
        # What it holds still runs.
        assert "pyodide.js" in page
        assert "--dl-navy" in page
        # The start-here page links to every file, in order.
        first = start_here.index("01-t1.html")
        second = start_here.index("02-t2.html")
        assert first < second
        assert 'href="01-t1.html"' in start_here
        assert 'href="02-t2.html"' in start_here
        # The contents page offers it.
        index = (repo_with_assets / "site" / "all-tutorials.html").read_text()
        assert 'href="download/computational-methods-core-skills.zip"' in index
        assert "Download all 2" in index
        # The download link sits above the list, not below it.
        link = index.index('href="download/computational-methods-core-skills.zip"')
        listing = index.index('<ol class="dl-contents">')
        assert link < listing
        # The download link is a button with a hidden icon.
        assert (
            '<a class="dl-download" href="download/computational-methods-core-skills.zip" '
            'download><span class="dl-download-icon" aria-hidden="true"></span>'
            "Download all 2" in index
        )
        # The copy of a tutorial in a series: navigation is dropped rather
        # than left broken, and the maths fonts travel with a maths tutorial.
        page = (repo_with_assets / "site" / "download" / "t1.html").read_text()
        assert "<nav" not in page
        assert "data:font/woff2;base64," in page

    def test_a_practice_page_follows_its_tutorial_into_the_archive_and_into_the_count(self, repo_with_assets):
        self.two_tutorials(repo_with_assets)
        practice_path = tutorial_path(repo_with_assets, "t1-practice")
        practice_path.write_text(
            '---\ntitle: "T1 practice"\n'
            'year: "2026-2027"\n'
            'version: 2026.08.23.1\npractice_for: t1\n'
            '---\n\n**1.** A question.\n'
        )
        b.build(standalone=True)
        with zipfile.ZipFile(self.archive(repo_with_assets)) as archive:
            names = sorted(archive.namelist())
        # The practice page follows its tutorial.
        assert names == [
            "computational-methods-core-skills/0-start-here.html",
            "computational-methods-core-skills/01-t1.html",
            "computational-methods-core-skills/02-t1-practice.html",
            "computational-methods-core-skills/03-t2.html",
        ]
        # The count includes practice pages: zip_sequence() places them right
        # after their tutorial, so the download count must include them too,
        # or it undersells the zip.
        index = (repo_with_assets / "site" / "all-tutorials.html").read_text()
        assert "Download all 3" in index
        assert "Download all 2" not in index

    def test_a_series_of_one_is_offered_in_the_singular(self, repo_with_assets):
        # "Download all 1" reads oddly in the plural, and a series of one
        # stopped being hypothetical once reflections got its own.
        path = tutorial_path(repo_with_assets, "t1")
        path.write_text(
            '---\ntitle: "One"\n'
            'year: "2026-2027"\nversion: 2026.08.23.1\n---\n\nProse.\n'
        )
        set_order(repo_with_assets, "computational-methods", "core-skills", ["t1"])
        b.build(standalone=True)
        index = (repo_with_assets / "site" / "all-tutorials.html").read_text()
        assert "Download this one as a single file" in index
        assert "Download all 1" not in index

    def test_a_build_without_the_copies_offers_nothing_to_download(self, repo_with_assets):
        self.two_tutorials(repo_with_assets)
        b.build()
        # No copy is written unless asked.
        assert not (repo_with_assets / "site" / "download").exists()
        # Neither the series archive nor the course archive is offered.
        index = (repo_with_assets / "site" / "all-tutorials.html").read_text()
        assert ".zip" not in index
        assert "computational-methods-all.zip" not in index

    def test_a_name_and_a_size_are_written_for_people(self, tmp_path):
        # A series name written for people becomes a filename.
        assert b.series_slug("MIT-PDP", "Maths & Programming") == "mit-pdp-maths-programming"
        # A size is reported in units a person reads.
        small = tmp_path / "small"
        small.write_bytes(b"x" * 4000)
        big = tmp_path / "big"
        big.write_bytes(b"x" * 2_500_000)
        assert b.readable_size(small) == "4 KB"
        assert b.readable_size(big) == "2 MB"


class TestTheCourseArchive:
    """One archive per course file (a "module" on the contents page):
    every series numbered as a single sequence, a practice page still
    behind its tutorial, and the course's mixed problem sets at the end.
    Each scenario matches the whole listing, so they stay apart."""

    def practice(self, repo, slug: str, **frontmatter) -> Path:
        path = tutorial_path(repo, slug)
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
        return path

    def archive(self, repo) -> Path:
        return repo / "site" / "download" / "computational-methods-all.zip"

    def test_two_series_become_one_archive_numbered_as_a_single_sequence(self, repo_with_assets):
        write(repo_with_assets, "One.\n", slug="one")
        write_in_series(repo_with_assets, "Two.\n", slug="two", series="simulation")
        set_order(repo_with_assets, "computational-methods", "simulation", ["two"])
        b.build(standalone=True)
        # It gathers every series in the course.
        assert self.archive(repo_with_assets).is_file()
        with zipfile.ZipFile(self.archive(repo_with_assets)) as archive:
            names = sorted(archive.namelist())
        # Numbering does not restart between series.
        assert names == [
            "computational-methods/0-start-here.html",
            "computational-methods/01-one.html",
            "computational-methods/02-two.html",
        ]
        # The contents page offers it.
        index = (repo_with_assets / "site" / "all-tutorials.html").read_text()
        assert 'href="download/computational-methods-all.zip"' in index
        assert "Download every tutorial and practice page in this module" in index

    def test_practice_still_follows_its_tutorial(self, repo_with_assets):
        write(repo_with_assets, "One.\n", slug="one")
        self.practice(repo_with_assets, "one-practice", practice_for="one")
        write_in_series(repo_with_assets, "Two.\n", slug="two", series="simulation")
        set_order(repo_with_assets, "computational-methods", "simulation", ["two"])
        b.build(standalone=True)
        with zipfile.ZipFile(self.archive(repo_with_assets)) as archive:
            names = sorted(archive.namelist())
        assert names == [
            "computational-methods/0-start-here.html",
            "computational-methods/01-one.html",
            "computational-methods/02-one-practice.html",
            "computational-methods/03-two.html",
        ]

    def test_a_mixed_set_lands_at_the_end(self, repo_with_assets):
        write(repo_with_assets, "One.\n", slug="one")
        write_in_series(repo_with_assets, "Two.\n", slug="two", series="simulation")
        set_order(repo_with_assets, "computational-methods", "simulation", ["two"])
        self.practice(repo_with_assets, "mixed", practice_across=["one", "two"])
        b.build(standalone=True)
        with zipfile.ZipFile(self.archive(repo_with_assets)) as archive:
            names = sorted(archive.namelist())
            start_here = archive.read("computational-methods/0-start-here.html").decode()
        assert names == [
            "computational-methods/0-start-here.html",
            "computational-methods/01-one.html",
            "computational-methods/02-two.html",
            "computational-methods/03-mixed.html",
        ]
        assert "Mixed problems" in start_here
        assert start_here.index("02-two.html") < start_here.index("03-mixed.html")


class TestDownloadsDoNotCollide:
    """An id is site-wide, so the download folder is flat: one copy per
    page at download/<id>.html, and a tutorial listed on two courses has
    one copy, not one per course, while each course's archive gathers its
    own listing."""

    def test_a_tutorial_on_two_courses_has_one_copy_and_a_place_in_each_archive(self, repo_with_assets):
        write(repo_with_assets, "One.\n", slug="first-steps")
        write(repo_with_assets, "Two.\n", slug="second")
        course(repo_with_assets, "zz-other", {"Intro": ["first-steps"]})
        b.build(standalone=True)
        # Every page has one downloadable copy, by its id.
        pages = list((repo_with_assets / "site" / "tutorials").rglob("*.html"))
        copies = [
            p for p in (repo_with_assets / "site" / "download").rglob("*.html")
            if "dewmini" not in p.parts
        ]
        assert len(copies) == len(pages) == 2
        assert (repo_with_assets / "site" / "download" / "first-steps.html").is_file()
        page = built(repo_with_assets, "first-steps")
        assert 'href="../download/first-steps.html"' in page
        # Each course archive gathers its own listing.
        with zipfile.ZipFile(repo_with_assets / "site" / "download" / "zz-other-all.zip") as archive:
            assert archive.namelist() == ["zz-other/01-first-steps.html", "zz-other/0-start-here.html"]
        with zipfile.ZipFile(repo_with_assets / "site" / "download" / "computational-methods-all.zip") as archive:
            assert sorted(archive.namelist()) == [
                "computational-methods/0-start-here.html",
                "computational-methods/01-first-steps.html",
                "computational-methods/02-second.html",
            ]
