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
    def test_it_is_written_beside_the_site(self, repo_with_assets):
        write(repo_with_assets, "Some prose.\n")
        b.build(standalone=True)
        assert (repo_with_assets / "site" / "download" / "sample.html").is_file()

    def test_it_is_not_written_unless_asked(self, repo_with_assets):
        write(repo_with_assets, "Some prose.\n")
        b.build()
        assert not (repo_with_assets / "site" / "download").exists()

    def test_the_page_links_to_it(self, repo_with_assets):
        write(repo_with_assets, "Some prose.\n")
        b.build(standalone=True)
        page = built(repo_with_assets)
        assert 'href="../download/sample.html"' in page

    def standalone(self, repo) -> str:
        return (repo / "site" / "download" / "sample.html").read_text()

    def test_nothing_is_left_pointing_outside_the_file(self, repo_with_assets):
        write(repo_with_assets, "```python exec\nid: c\n1 + 1\n```\n")
        b.build(standalone=True)
        page = self.standalone(repo_with_assets)
        assert '<link rel="stylesheet"' not in page
        assert '<script type="module"' not in page

    def test_the_stylesheet_travels_inside_it(self, repo_with_assets):
        write(repo_with_assets, "Some prose.\n")
        b.build(standalone=True)
        assert "--dl-navy" in self.standalone(repo_with_assets)

    def test_the_runtime_travels_inside_it_as_a_classic_script(self, repo_with_assets):
        write(repo_with_assets, "Some prose.\n")
        b.build(standalone=True)
        page = self.standalone(repo_with_assets)
        assert "pyodide.js" in page
        assert len(page) > 300_000  # confirms the bundle itself is embedded, not a stub

    def test_the_python_tools_travel_inside_it(self, repo_with_assets):
        write(repo_with_assets, "```python exec\nid: c\n1 + 1\n```\n")
        b.build(standalone=True)
        page = self.standalone(repo_with_assets)
        assert "toolsSource" in page
        assert "def check(" in page

    def test_it_marks_itself_as_standalone(self, repo_with_assets):
        write(repo_with_assets, "Some prose.\n")
        b.build(standalone=True)
        assert manifest(self.standalone(repo_with_assets))["standalone"] is True

    def test_maths_fonts_travel_with_a_maths_tutorial(self, repo_with_assets):
        write(repo_with_assets, "An equation: $x^2$.\n")
        b.build(standalone=True)
        assert "data:font/woff2;base64," in self.standalone(repo_with_assets)

    def test_a_tutorial_without_maths_does_not_carry_them(self, repo_with_assets):
        write(repo_with_assets, "No maths at all.\n")
        b.build(standalone=True)
        page = self.standalone(repo_with_assets)
        assert ".katex-html" not in page
        assert "data:font/woff2;base64," in page  # the accessible fonts still do

    def test_navigation_is_dropped_rather_than_left_broken(self, repo_with_assets):
        for n in (1, 2):
            path = tutorial_path(repo_with_assets, f"t{n}")
            path.write_text(
                f'---\ntitle: "T{n}"\n'
                f'year: "2026-2027"\nversion: 2026.08.23.1\n---\n\nProse.\n'
            )
        set_order(repo_with_assets, "computational-methods", "s", ["t1", "t2"])
        b.build(standalone=True)
        page = (repo_with_assets / "site" / "download" / "t1.html").read_text()
        assert "<nav" not in page

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
    def two_tutorials(self, repo):
        for n in (1, 2):
            path = tutorial_path(repo, f"t{n}")
            path.write_text(
                f'---\ntitle: "T{n}"\n'
                f'year: "2026-2027"\nversion: 2026.08.23.1\n---\n\nProse.\n'
            )
        set_order(repo, "computational-methods", "Core skills", ["t1", "t2"])

    def archive(self, repo) -> Path:
        return repo / "site" / "download" / "computational-methods-core-skills.zip"

    def test_a_series_is_gathered_into_one_archive(self, repo_with_assets):
        self.two_tutorials(repo_with_assets)
        b.build(standalone=True)
        assert self.archive(repo_with_assets).is_file()

    def test_it_holds_every_downloadable_copy_in_the_series(self, repo_with_assets):
        self.two_tutorials(repo_with_assets)
        b.build(standalone=True)
        with zipfile.ZipFile(self.archive(repo_with_assets)) as archive:
            assert sorted(archive.namelist()) == [
                "computational-methods-core-skills/0-start-here.html",
                "computational-methods-core-skills/01-t1.html",
                "computational-methods-core-skills/02-t2.html",
            ]

    def test_what_it_holds_still_runs(self, repo_with_assets):
        self.two_tutorials(repo_with_assets)
        b.build(standalone=True)
        with zipfile.ZipFile(self.archive(repo_with_assets)) as archive:
            page = archive.read("computational-methods-core-skills/01-t1.html").decode()
        assert "pyodide.js" in page
        assert "--dl-navy" in page

    def test_the_start_here_page_links_to_every_file_in_order(self, repo_with_assets):
        self.two_tutorials(repo_with_assets)
        b.build(standalone=True)
        with zipfile.ZipFile(self.archive(repo_with_assets)) as archive:
            start_here = archive.read(
                "computational-methods-core-skills/0-start-here.html"
            ).decode()
        first = start_here.index("01-t1.html")
        second = start_here.index("02-t2.html")
        assert first < second
        assert 'href="01-t1.html"' in start_here
        assert 'href="02-t2.html"' in start_here

    def test_a_practice_page_follows_its_tutorial(self, repo_with_assets):
        self.two_tutorials(repo_with_assets)
        practice_path = tutorial_path(repo_with_assets, "t1-practice", "computational-methods")
        practice_path.write_text(
            '---\ntitle: "T1 practice"\n'
            'year: "2026-2027"\n'
            'version: 2026.08.23.1\npractice_for: t1\n'
            '---\n\n**1.** A question.\n'
        )
        b.build(standalone=True)
        with zipfile.ZipFile(self.archive(repo_with_assets)) as archive:
            names = sorted(archive.namelist())
        assert names == [
            "computational-methods-core-skills/0-start-here.html",
            "computational-methods-core-skills/01-t1.html",
            "computational-methods-core-skills/02-t1-practice.html",
            "computational-methods-core-skills/03-t2.html",
        ]

    def test_the_contents_page_offers_it(self, repo_with_assets):
        self.two_tutorials(repo_with_assets)
        b.build(standalone=True)
        index = (repo_with_assets / "site" / "all-tutorials.html").read_text()
        assert 'href="download/computational-methods-core-skills.zip"' in index
        assert "Download all 2" in index

    def test_the_count_includes_practice_pages(self, repo_with_assets):
        # zip_sequence() places practice pages right after their tutorial, so
        # the download count must include them too, or it undersells the zip.
        self.two_tutorials(repo_with_assets)
        practice_path = tutorial_path(repo_with_assets, "t1-practice", "computational-methods")
        practice_path.write_text(
            '---\ntitle: "T1 practice"\n'
            'year: "2026-2027"\n'
            'version: 2026.08.23.1\npractice_for: t1\n'
            '---\n\n**1.** A question.\n'
        )
        b.build(standalone=True)
        index = (repo_with_assets / "site" / "all-tutorials.html").read_text()
        assert "Download all 3" in index
        assert "Download all 2" not in index

    def test_the_download_link_sits_above_the_list_not_below_it(self, repo_with_assets):
        self.two_tutorials(repo_with_assets)
        b.build(standalone=True)
        index = (repo_with_assets / "site" / "all-tutorials.html").read_text()
        link = index.index('href="download/computational-methods-core-skills.zip"')
        listing = index.index('<ol class="dl-contents">')
        assert link < listing

    def test_the_download_link_is_a_button_with_a_hidden_icon(self, repo_with_assets):
        self.two_tutorials(repo_with_assets)
        b.build(standalone=True)
        index = (repo_with_assets / "site" / "all-tutorials.html").read_text()
        assert (
            '<a class="dl-download" href="download/computational-methods-core-skills.zip" '
            'download><span class="dl-download-icon" aria-hidden="true"></span>'
            "Download all 2" in index
        )

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

    def test_a_build_without_the_copies_offers_nothing_to_download(self, repo):
        self.two_tutorials(repo)
        b.build()
        index = (repo / "site" / "all-tutorials.html").read_text()
        assert ".zip" not in index
        assert not (repo / "site" / "download").exists()

    def test_a_series_name_written_for_people_becomes_a_filename(self):
        assert b.series_slug("MIT-PDP", "Maths & Programming") == "mit-pdp-maths-programming"

    def test_a_size_is_reported_in_units_a_person_reads(self, tmp_path):
        small = tmp_path / "small"
        small.write_bytes(b"x" * 4000)
        big = tmp_path / "big"
        big.write_bytes(b"x" * 2_500_000)
        assert b.readable_size(small) == "4 KB"
        assert b.readable_size(big) == "2 MB"


class TestTheModuleArchive:
    """One archive per module: every series numbered as a single sequence,
    plus module-wide mixed problem sets."""

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

    def test_it_gathers_every_series_in_the_module(self, repo_with_assets):
        write(repo_with_assets, "One.\n", slug="one")
        write_in_series(repo_with_assets, "Two.\n", slug="two", series="simulation")
        set_order(repo_with_assets, "computational-methods", "simulation", ["two"])
        b.build(standalone=True)
        assert self.archive(repo_with_assets).is_file()

    def test_numbering_does_not_restart_between_series(self, repo_with_assets):
        write(repo_with_assets, "One.\n", slug="one")
        write_in_series(repo_with_assets, "Two.\n", slug="two", series="simulation")
        set_order(repo_with_assets, "computational-methods", "simulation", ["two"])
        b.build(standalone=True)
        with zipfile.ZipFile(self.archive(repo_with_assets)) as archive:
            names = sorted(archive.namelist())
        assert names == [
            "computational-methods/0-start-here.html",
            "computational-methods/01-one.html",
            "computational-methods/02-two.html",
        ]

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

    def test_the_contents_page_offers_it(self, repo_with_assets):
        write(repo_with_assets, "One.\n", slug="one")
        write_in_series(repo_with_assets, "Two.\n", slug="two", series="simulation")
        set_order(repo_with_assets, "computational-methods", "simulation", ["two"])
        b.build(standalone=True)
        index = (repo_with_assets / "site" / "all-tutorials.html").read_text()
        assert 'href="download/computational-methods-all.zip"' in index
        assert "Download every tutorial and practice page in this module" in index

    def test_a_build_without_the_copies_offers_no_module_download(self, repo):
        write(repo, "One.\n", slug="one")
        b.build()
        index = (repo / "site" / "all-tutorials.html").read_text()
        assert "computational-methods-all.zip" not in index


class TestDownloadsDoNotCollide:
    """An id is site-wide, so the download folder is flat: one copy per
    page at download/<id>.html, and a tutorial listed on two courses has
    one copy, not one per course."""

    def test_every_page_has_one_downloadable_copy_by_its_id(self, repo_with_assets):
        write(repo_with_assets, "One.\n", slug="first-steps")
        write(repo_with_assets, "Two.\n", slug="second")
        course(repo_with_assets, "zz-other", {"Intro": ["first-steps"]})
        b.build(standalone=True)
        pages = list((repo_with_assets / "site" / "tutorials").rglob("*.html"))
        copies = [
            p for p in (repo_with_assets / "site" / "download").rglob("*.html")
            if "dewmini" not in p.parts
        ]
        assert len(copies) == len(pages) == 2
        assert (repo_with_assets / "site" / "download" / "first-steps.html").is_file()
        page = built(repo_with_assets, "first-steps")
        assert 'href="../download/first-steps.html"' in page

    def test_each_course_archive_gathers_its_own_listing(self, repo_with_assets):
        write(repo_with_assets, "One.\n", slug="first-steps")
        write(repo_with_assets, "Two.\n", slug="second")
        course(repo_with_assets, "zz-other", {"Intro": ["first-steps"]})
        b.build(standalone=True)
        with zipfile.ZipFile(repo_with_assets / "site" / "download" / "zz-other-all.zip") as archive:
            assert archive.namelist() == ["zz-other/01-first-steps.html", "zz-other/0-start-here.html"]
        with zipfile.ZipFile(repo_with_assets / "site" / "download" / "computational-methods-all.zip") as archive:
            assert sorted(archive.namelist()) == [
                "computational-methods/0-start-here.html",
                "computational-methods/01-first-steps.html",
                "computational-methods/02-second.html",
            ]
