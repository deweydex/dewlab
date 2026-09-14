"""Versions of a tutorial, and the manifest that identifies a page."""

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

class TestVersionsOfATutorial:
    """A version is a release, not a save (planning/VERSIONS.md)."""

    def release(self, repo, slug: str, version: str, status: str = "live",
                body: str = "Prose.\n") -> Path:
        folder = repo / "tutorials" / slug
        folder.mkdir(parents=True, exist_ok=True)
        path = folder / f"v{version}.md"
        path.write_text(
            f'---\ntitle: "The Tutorial"\n'
            f'year: "2026-2027"\nversion: {version}\n'
            f"status: {status}\n---\n\n{body}"
        )
        if status == "live":
            listed = repo / "tutorials" / "python-fundamentals.order.yaml"
            already = [l.strip("- ").strip() for l in listed.read_text().splitlines()
                       if l.strip().startswith("- ")] if listed.is_file() else []
            if slug not in already:
                set_order(repo, "computational-methods", "python-fundamentals",
                          already + [slug])
        return path

    def out(self, repo, *parts) -> Path:
        return repo.joinpath("site", "tutorials", *parts)

    def test_the_newest_live_version_answers_the_tutorial_url(self, repo):
        # Every link written before versions existed keeps working and keeps
        # meaning "the current one".
        self.release(repo, "thing", "2026.06.02.1", body="Old.\n")
        self.release(repo, "thing", "2026.09.15.1", body="New.\n")
        b.build()
        assert "New." in self.out(repo, "thing.html").read_text()

    def test_an_older_version_is_still_built_and_still_reachable(self, repo):
        self.release(repo, "thing", "2026.06.02.1", body="Old.\n")
        self.release(repo, "thing", "2026.09.15.1", body="New.\n")
        b.build()
        older = self.out(repo, "thing", "v2026.06.02.1.html")
        assert older.is_file()
        assert "Old." in older.read_text()

    def test_an_older_version_says_so_and_points_at_the_newer_one(self, repo):
        self.release(repo, "thing", "2026.06.02.1", body="Old.\n")
        self.release(repo, "thing", "2026.09.15.1", body="New.\n")
        b.build()
        page = self.out(repo, "thing", "v2026.06.02.1.html").read_text()
        assert "2 June 2026 version" in page
        assert "15 September 2026" in page
        assert "../thing.html" in page

    def test_dates_sort_by_date_and_not_as_text(self, repo):
        # 2026.09.02.1 comes before 2026.09.15.1; compared as strings it would
        # come after, because "2" sorts after "1".
        self.release(repo, "thing", "2026.09.02.1", body="Earlier.\n")
        self.release(repo, "thing", "2026.09.15.1", body="Later.\n")
        b.build()
        assert "Later." in self.out(repo, "thing.html").read_text()

    def test_two_releases_on_one_day_are_told_apart_by_the_last_number(self, repo):
        self.release(repo, "thing", "2026.09.15.1", body="Morning.\n")
        self.release(repo, "thing", "2026.09.15.2", body="Afternoon.\n")
        b.build()
        assert "Afternoon." in self.out(repo, "thing.html").read_text()

    def test_a_draft_is_not_built_at_all(self, repo):
        # The site is static and public: anything built has a URL, so the
        # only honest draft is one with no page.
        write(repo, "Prose.\n")
        self.release(repo, "thing", "2026.09.15.1", status="draft", body="Secret.\n")
        b.build()
        assert not self.out(repo, "thing.html").exists()
        assert not self.out(repo, "thing").exists()

    def test_a_beta_is_built_but_is_never_the_default(self, repo):
        # Freeze the live release, mark the working copy beta, and students
        # keep getting the live one until the beta is promoted.
        self.release(repo, "thing", "2026.06.02.1", body="Live.\n")
        self.release(repo, "thing", "2026.09.15.1", status="beta", body="Trying.\n")
        b.build()
        assert "Live." in self.out(repo, "thing.html").read_text()
        beta = self.out(repo, "thing", "v2026.09.15.1.html")
        assert "Trying." in beta.read_text()
        assert "not the tutorial your course uses" in beta.read_text()

    def test_a_beta_is_not_in_the_reading_order(self, repo):
        self.release(repo, "thing", "2026.06.02.1", body="Live.\n")
        self.release(repo, "thing", "2026.09.15.1", status="beta", body="Trying.\n")
        write(repo, "Another.\n", slug="other")
        set_order(repo, "computational-methods", "python-fundamentals",
                  ["thing", "other"])
        b.build()
        page = self.out(repo, "thing.html").read_text()
        route = "".join(re.findall(r"<nav class=\"dl-nav.*?</nav>", page, re.DOTALL))
        assert "other.html" in route
        assert "v2026.09.15.1" not in route
        assert "v2026.09.15.1" not in re.sub(
            r'<script type="application/json".*?</script>', "", page, flags=re.DOTALL)

    def test_only_the_default_teaches_an_outcome(self, repo):
        # A superseded release claims the same coverage as the one that
        # replaced it; counting both would make one outcome look taught twice.
        covers = "covers:\n  a-section:\n    covers: [MIT-1.4]\n"
        for version in ("2026.06.02.1", "2026.09.15.1"):
            path = self.release(repo, "thing", version, body="## A section\n\nProse.\n")
            path.write_text(path.read_text().replace(
                f"status: live\n", f"status: live\n{covers}"))
        b.build()
        data = json.loads(re.search(
            r'<script type="application/json" id="dewlab-tree">(.*?)</script>',
            (repo / "site" / "tree.html").read_text(), re.DOTALL).group(1))
        node = next(n for n in data["nodes"] if n["code"] == "MIT-1.4")
        assert node["state"] == "taught"
        assert "/thing.html#" in node["where"]["href"]

    def test_an_older_release_points_search_at_the_current_one(self, repo):
        # Two releases of one tutorial are near-identical pages; without a
        # canonical link they compete with each other in search results.
        self.release(repo, "thing", "2026.06.02.1")
        self.release(repo, "thing", "2026.09.15.1")
        b.build()
        older = self.out(repo, "thing", "v2026.06.02.1.html").read_text()
        assert '<link rel="canonical" href="../thing.html">' in older

    def test_the_current_one_does_not_point_at_itself(self, repo):
        self.release(repo, "thing", "2026.06.02.1")
        self.release(repo, "thing", "2026.09.15.1")
        b.build()
        assert "canonical" not in self.out(repo, "thing.html").read_text()

    def test_a_version_that_is_not_a_release_date_stops_the_build(self, repo):
        path = write(repo, "Prose.\n")
        path.write_text(path.read_text().replace(
            "version: 2026.08.23.1", "version: 3"))
        with pytest.raises(b.BuildError, match="release date"):
            b.build()


class TestTheVersionListInTheManifest:
    """Saved answers are matched back on cell id, so which survive a move to
    another release is knowable only if the page knows which cells that
    release has (planning/VERSIONS.md)."""

    release = TestVersionsOfATutorial.release
    out = TestVersionsOfATutorial.out

    CELLS = (
        "## A section\n\n```python exec\nid: one\nprint(1)\n```\n\n"
        "```python exec\nid: two\nprint(2)\n```\n"
    )

    def test_one_release_carries_no_list(self, repo):
        # A picker with a single entry is furniture, and every tutorial would
        # pay for it in bytes and in clutter.
        write(repo, "Prose.\n")
        b.build()
        assert "versions" not in manifest(built(repo))

    def test_every_release_is_listed_newest_first(self, repo):
        self.release(repo, "thing", "2026.06.02.1")
        self.release(repo, "thing", "2026.09.15.1")
        b.build()
        listed = manifest(self.out(repo, "thing.html").read_text())["versions"]
        assert [v["version"] for v in listed] == ["2026.09.15.1", "2026.06.02.1"]

    def test_each_entry_carries_the_date_a_reader_would_read(self, repo):
        # The dotted form is for the file and the URL; a person gets a date.
        self.release(repo, "thing", "2026.06.02.1")
        self.release(repo, "thing", "2026.09.15.1")
        b.build()
        listed = manifest(self.out(repo, "thing.html").read_text())["versions"]
        assert [v["date"] for v in listed] == ["15 September 2026", "2 June 2026"]

    def test_the_default_is_marked_and_the_others_are_not(self, repo):
        self.release(repo, "thing", "2026.06.02.1")
        self.release(repo, "thing", "2026.09.15.1")
        b.build()
        listed = manifest(self.out(repo, "thing.html").read_text())["versions"]
        assert [v["isDefault"] for v in listed] == [True, False]

    def test_a_beta_is_listed_as_a_beta(self, repo):
        # It is reachable, so it belongs in the list; it is not the course,
        # so the list has to say which one it is.
        self.release(repo, "thing", "2026.06.02.1")
        self.release(repo, "thing", "2026.09.15.1", status="beta")
        b.build()
        listed = manifest(self.out(repo, "thing.html").read_text())["versions"]
        assert {v["version"]: v["status"] for v in listed} == {
            "2026.06.02.1": "live", "2026.09.15.1": "beta",
        }

    def test_each_url_is_relative_to_the_page_that_carries_it(self, repo):
        # The default sits one folder up from its own older releases, so the
        # same list is written twice with different paths in it.
        self.release(repo, "thing", "2026.06.02.1")
        self.release(repo, "thing", "2026.09.15.1")
        b.build()

        from_default = manifest(self.out(repo, "thing.html").read_text())["versions"]
        assert {v["version"]: v["url"] for v in from_default} == {
            "2026.09.15.1": "thing.html",
            "2026.06.02.1": "thing/v2026.06.02.1.html",
        }

        older = self.out(repo, "thing", "v2026.06.02.1.html").read_text()
        from_older = manifest(older)["versions"]
        assert {v["version"]: v["url"] for v in from_older} == {
            "2026.09.15.1": "../thing.html",
            "2026.06.02.1": "v2026.06.02.1.html",
        }

    def test_each_entry_carries_that_release_s_cell_ids(self, repo):
        # Without these the page can only warn a reader that their work "may
        # not line up"; with them it can count.
        self.release(repo, "thing", "2026.06.02.1", body=self.CELLS)
        self.release(repo, "thing", "2026.09.15.1",
                     body=self.CELLS.replace("id: two", "id: three"))
        b.build()
        listed = manifest(self.out(repo, "thing.html").read_text())["versions"]
        assert {v["version"]: v["cells"] for v in listed} == {
            "2026.09.15.1": ["one", "three"],
            "2026.06.02.1": ["one", "two"],
        }


class TestTheManifestIdentifiesThePage:
    def test_it_carries_the_id_and_every_course_that_lists_the_page(self, repo):
        # Saved work is keyed on the id, which is site-wide; the courses are
        # what the runtime draws the chrome for.
        write(repo, "Prose.\n")
        course(repo, "zz-other", {"S": ["sample"]})
        b.build()
        page = (repo / "site" / "tutorials" / "sample.html").read_text()
        assert manifest(page)["id"] == "sample"
        assert manifest(page)["slug"] == "sample"
        assert manifest(page)["courses"] == ["computational-methods", "zz-other"]
        assert "legacy" not in manifest(page)

    def test_it_carries_the_old_key_where_the_page_had_an_older_address(self, repo):
        # What the runtime renames a reader's saved work from, once.
        write(repo, "Prose.\n")
        (repo / "courses" / "redirects.yaml").write_text(
            "tutorials/old-module/sample.html: tutorials/sample.html\n")
        b.build()
        assert manifest(built(repo))["legacy"] == "old-module:sample"
