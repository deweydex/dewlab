"""Every address the site used to have still opens the right page:
courses/redirects.yaml becomes one small page per line, and a line that
would point at nothing, or sit on top of a real page, stops the build."""

from __future__ import annotations

import pytest

from helpers import *  # noqa: F401,F403
from helpers import b


def redirects(repo, lines: str):
    (repo / "courses" / "redirects.yaml").write_text(lines)


def test_every_old_address_has_a_stub_that_points_at_a_page_that_exists(repo):
    write(repo, "Prose.\n")
    redirects(repo, "tutorials/old-module/sample.html: tutorials/sample.html\n"
                    "old-module.html: computational-methods.html\n")
    written = b.build()
    stub = repo / "site" / "tutorials" / "old-module" / "sample.html"
    assert stub in written
    page = stub.read_text()
    assert '<meta http-equiv="refresh" content="0; url=../sample.html">' in page
    assert '<a href="../sample.html">open it here</a>' in page
    assert 'url=computational-methods.html' in (repo / "site" / "old-module.html").read_text()


def test_a_line_pointing_at_nothing_stops_the_build(repo):
    write(repo, "Prose.\n")
    redirects(repo, "tutorials/old-module/sample.html: tutorials/smaple.html\n")
    with pytest.raises(b.BuildError, match="this build wrote no page at tutorials/smaple.html"):
        b.build()


def test_a_line_sitting_on_a_real_page_stops_the_build(repo):
    write(repo, "Prose.\n")
    write(repo, "Other.\n", slug="other")
    redirects(repo, "tutorials/other.html: tutorials/sample.html\n")
    with pytest.raises(b.BuildError, match="the build writes a page at tutorials/other.html"):
        b.build()


def test_no_redirects_file_writes_no_stubs(repo):
    write(repo, "Prose.\n")
    b.build()
    assert not (repo / "site" / "tutorials" / "old-module").exists()


def test_a_page_left_by_an_earlier_build_is_not_a_real_page(repo):
    """A build without --clean keeps whatever an earlier build wrote. A
    file at an old address is then the page the address used to be, not
    a page this build wrote, and the line retiring it must not be
    refused: the stub replaces the file."""
    write(repo, "Prose.\n")
    stale = repo / "site" / "tutorials" / "old-module" / "sample.html"
    stale.parent.mkdir(parents=True)
    stale.write_text("<p>the page as it was before the address moved</p>")
    redirects(repo, "tutorials/old-module/sample.html: tutorials/sample.html\n")
    written = b.build()
    assert stale in written
    assert 'url=../sample.html' in stale.read_text()


def test_the_notebook_and_the_workspace_keep_their_old_addresses(repo_with_assets):
    # dewmini and dewmini web became the Notebook and the Workspace. Their
    # old pages are hand-written redirects in compose/, not lines in
    # redirects.yaml: they keep a query string and a hash, which a
    # redirects.yaml stub cannot.
    write(repo_with_assets, "Prose.\n")
    b.build(standalone=True)
    compose = repo_with_assets / "site" / "compose"
    for old, new in (("dewmini.html", "notebook.html"), ("dewminiweb.html", "workspace.html")):
        assert (compose / new).is_file()
        stub = (compose / old).read_text()
        assert f'location.replace("{new}" + location.search + location.hash)' in stub
        assert f'<meta http-equiv="refresh" content="0; url={new}">' in stub
        assert f'<a href="{new}">open it here</a>' in stub
        # A stub, not a second copy of the page.
        assert "dewmini.js" not in stub and "dewminiweb.js" not in stub
    # The offline copy is new at download/notebook/, and carries no stubs:
    # nobody has a bookmark into a folder they have just unzipped.
    bundle = repo_with_assets / "site" / "download" / "notebook"
    assert (bundle / "compose" / "notebook.html").is_file()
    assert not (bundle / "compose" / "dewmini.html").exists()
    assert not (bundle / "compose" / "dewminiweb.html").exists()
    assert 'window.location.replace("compose/notebook.html")' in (bundle / "index.html").read_text()
    assert (repo_with_assets / "site" / "download" / "notebook.zip").is_file()
    assert not (repo_with_assets / "site" / "download" / "dewmini").exists()
