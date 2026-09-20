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
    """A version is a release, not a save. The
    manifest of every release lists them all: saved answers are matched
    back on cell id, so which survive a move to another release is knowable
    only if the page knows which cells that release has."""

    CELLS = (
        "## A section\n\n```python exec\nid: one\nprint(1)\n```\n\n"
        "```python exec\nid: two\nprint(2)\n```\n"
    )

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
            # Listed under the default course's series, once, in the order
            # first released — the listing lives in courses/*.yaml.
            already = next((e["tutorials"] for e in
                            read_course(repo, "computational-methods").get("contents", [])
                            if b.series_key(e["title"]) == "python-fundamentals"), [])
            if slug not in already:
                set_order(repo, "computational-methods", "python-fundamentals",
                          already + [slug])
        return path

    def out(self, repo, *parts) -> Path:
        return repo.joinpath("site", "tutorials", *parts)

    def test_two_live_releases_give_a_current_page_and_an_older_one_that_points_forward(self, repo):
        """Two live releases of one tutorial, each with two cells (one shared)
        and each claiming the same outcome. The newer answers the tutorial's
        URL; the older is still built at its own address, says which
        version it is, and points readers and search engines at the current
        one; both manifests list both releases, relative to their own page;
        and the outcome is taught once."""
        covers = "covers:\n  a-section:\n    covers: [MIT-1.4]\n"
        for version, body in (
            ("2026.06.02.1", "Old.\n\n" + self.CELLS),
            ("2026.09.15.1", "New.\n\n" + self.CELLS.replace("id: two", "id: three")),
        ):
            path = self.release(repo, "thing", version, body=body)
            path.write_text(path.read_text().replace(
                "status: live\n", f"status: live\n{covers}"))
        b.build()
        current = self.out(repo, "thing.html").read_text()
        older = self.out(repo, "thing", "v2026.06.02.1.html")

        # The newest live version answers the tutorial URL: every link
        # written before versions existed keeps working and keeps meaning
        # "the current one".
        assert "New." in current
        # An older version is still built and still reachable.
        assert older.is_file()
        assert "Old." in older.read_text()
        # An older version says so and points at the newer one.
        page = older.read_text()
        assert "2 June 2026 version" in page
        assert "15 September 2026" in page
        assert "../thing.html" in page
        # An older release points search at the current one: two releases
        # of one tutorial are near-identical pages; without a canonical link
        # they compete with each other in search results.
        assert '<link rel="canonical" href="../thing.html">' in page
        # The current one does not point at itself.
        assert "canonical" not in current

        # Only the default teaches an outcome. A superseded release claims
        # the same coverage as the one that replaced it; counting both would
        # make one outcome look taught twice.
        data = json.loads(re.search(
            r'<script type="application/json" id="dewlab-tree">(.*?)</script>',
            (repo / "site" / "tree.html").read_text(), re.DOTALL).group(1))
        node = next(n for n in data["nodes"] if n["code"] == "MIT-1.4")
        assert node["state"] == "taught"
        assert "/thing.html#" in node["where"]["href"]

        # The manifest's version list: every release is listed newest first.
        listed = manifest(current)["versions"]
        assert [v["version"] for v in listed] == ["2026.09.15.1", "2026.06.02.1"]
        # Each entry carries the date a reader would read: the dotted form
        # is for the file and the URL; a person gets a date.
        assert [v["date"] for v in listed] == ["15 September 2026", "2 June 2026"]
        # The default is marked and the others are not.
        assert [v["isDefault"] for v in listed] == [True, False]
        # Each url is relative to the page that carries it: the default sits
        # one folder up from its own older releases, so the same list is
        # written twice with different paths in it.
        assert {v["version"]: v["url"] for v in listed} == {
            "2026.09.15.1": "thing.html",
            "2026.06.02.1": "thing/v2026.06.02.1.html",
        }
        from_older = manifest(page)["versions"]
        assert {v["version"]: v["url"] for v in from_older} == {
            "2026.09.15.1": "../thing.html",
            "2026.06.02.1": "v2026.06.02.1.html",
        }
        # Each entry carries that release's cell ids. Without these the page
        # can only warn a reader that their work "may not line up"; with
        # them it can count.
        assert {v["version"]: v["cells"] for v in listed} == {
            "2026.09.15.1": ["one", "three"],
            "2026.06.02.1": ["one", "two"],
        }

    def test_versions_sort_as_numbers_and_not_as_text(self, repo):
        # The year, month and day are zero-padded, so text order and date
        # order agree there; the release number is not. Compared as text,
        # "2026.09.15.10" sorts before "2026.09.15.9".
        self.release(repo, "thing", "2026.09.15.9", body="Ninth.\n")
        self.release(repo, "thing", "2026.09.15.10", body="Tenth.\n")
        b.build()
        assert "Tenth." in self.out(repo, "thing.html").read_text()

    def test_a_beta_is_built_and_reachable_but_neither_the_default_nor_in_the_reading_order(self, repo):
        # Freeze the live release, mark the working copy beta, and students
        # keep getting the live one until the beta is promoted.
        self.release(repo, "thing", "2026.06.02.1", body="Live.\n")
        self.release(repo, "thing", "2026.09.15.1", status="beta", body="Trying.\n")
        write(repo, "Another.\n", slug="other")
        set_order(repo, "computational-methods", "python-fundamentals",
                  ["thing", "other"])
        b.build()
        page = self.out(repo, "thing.html").read_text()
        # A beta is built but is never the default.
        assert "Live." in page
        beta = self.out(repo, "thing", "v2026.09.15.1.html")
        assert "Trying." in beta.read_text()
        assert "not the tutorial your course uses" in beta.read_text()
        # A beta is not in the reading order.
        route = "".join(re.findall(r"<nav class=\"dl-nav.*?</nav>", page, re.DOTALL))
        assert "other.html" in route
        assert "v2026.09.15.1" not in route
        assert "v2026.09.15.1" not in re.sub(
            r'<script type="application/json".*?</script>', "", page, flags=re.DOTALL)
        # A beta is listed as a beta in the manifest's version list. It is
        # reachable, so it belongs in the list; it is not the course, so the
        # list has to say which one it is.
        listed = manifest(page)["versions"]
        assert {v["version"]: v["status"] for v in listed} == {
            "2026.06.02.1": "live", "2026.09.15.1": "beta",
        }

    def test_a_version_that_is_not_a_release_date_stops_the_build(self, repo):
        path = write(repo, "Prose.\n")
        path.write_text(path.read_text().replace(
            "version: 2026.08.23.1", "version: 3"))
        with pytest.raises(b.BuildError, match="release date"):
            b.build()


class TestTheManifestIdentifiesThePage:
    release = TestVersionsOfATutorial.release
    out = TestVersionsOfATutorial.out

    def test_a_lone_release_listed_twice_carries_its_id_and_courses_and_no_version_list_while_a_draft_beside_it_is_not_built(self, repo):
        # One live release of `sample`, listed on a second course too, and a
        # draft of another tutorial in the same tree.
        write(repo, "Prose.\n")
        course(repo, "zz-other", {"S": ["sample"]})
        self.release(repo, "thing", "2026.09.15.1", status="draft", body="Secret.\n")
        b.build()
        # It carries the id and every course that lists the page. Saved work
        # is keyed on the id, which is site-wide; the courses are what the
        # runtime draws the chrome for.
        page = (repo / "site" / "tutorials" / "sample.html").read_text()
        assert manifest(page)["id"] == "sample"
        assert manifest(page)["slug"] == "sample"
        assert manifest(page)["courses"] == ["computational-methods", "zz-other"]
        assert "legacy" not in manifest(page)
        # One release carries no list: a picker with a single entry is
        # furniture, and every tutorial would pay for it in bytes and in
        # clutter.
        assert "versions" not in manifest(built(repo))
        # A draft is not built at all. The site is static and public:
        # anything built has a URL, so the only honest draft is one with no
        # page.
        assert not self.out(repo, "thing.html").exists()
        assert not self.out(repo, "thing").exists()

    def test_it_carries_the_old_key_where_the_page_had_an_older_address(self, repo):
        # What the runtime renames a reader's saved work from, once.
        write(repo, "Prose.\n")
        (repo / "courses" / "redirects.yaml").write_text(
            "tutorials/old-module/sample.html: tutorials/sample.html\n")
        b.build()
        assert manifest(built(repo))["legacy"] == "old-module:sample"
