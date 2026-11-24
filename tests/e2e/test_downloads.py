"""A download is put together in the reader's browser (assets/downloads.js)
from the skeletons and shared pieces the build writes. What the browser
saves has to be exactly what builder/downloads.py's own join gives, for one
page and for a course's zip, or a reader takes away a different file from
the one every build test checks."""

from __future__ import annotations

import functools
import io
import threading
import zipfile
from pathlib import Path

import pytest

from conftest import _QuietHandler, _QuietServer, b


@pytest.fixture(scope="module")
def download_site(site_dir: Path, tmp_path_factory):
    """The fixture site built again with its downloads, into a folder of its
    own, so the shared site the other tests use is left as it was."""
    out = tmp_path_factory.mktemp("dewlab-downloads") / "site"
    shared_out = b.cfg.OUT
    b.cfg.OUT = out
    try:
        b.build(clean=True, standalone=True)
    finally:
        b.cfg.OUT = shared_out
    handler = functools.partial(_QuietHandler, directory=str(out))
    with _QuietServer(("127.0.0.1", 0), handler) as server:
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            yield out, f"http://127.0.0.1:{server.server_address[1]}"
        finally:
            server.shutdown()
            thread.join(timeout=5)


def _press(tab, selector: str) -> tuple[str, bytes]:
    with tab.expect_download(timeout=120_000) as info:
        tab.eval_on_selector(selector, "link => link.click()")
    download = info.value
    return download.suggested_filename, Path(download.path()).read_bytes()


def test_one_page_is_saved_exactly_as_the_build_joins_it(browser, download_site):
    out, url = download_site
    tab = browser.new_context(accept_downloads=True).new_page()
    tab.goto(f"{url}/tutorials/third-page.html")
    name, data = _press(tab, "#dl-settings-download a.dl-download")
    assert name == "third-page.html"
    assert data.decode() == b.read_copy(out / "download", "third-page")


@pytest.mark.parametrize("compressed", [True, False])
def test_a_course_is_zipped_in_the_browser_with_every_file_the_build_lists(
        browser, download_site, compressed):
    # Without CompressionStream the zip is stored rather than deflated,
    # and still holds the same files.
    out, url = download_site
    tab = browser.new_context(accept_downloads=True).new_page()
    tab.goto(f"{url}/all-tutorials.html")
    if not compressed:
        tab.evaluate("delete window.CompressionStream")
    name, data = _press(tab, 'a[href="download/fixtures-all.json"]')
    assert name == "fixtures-all.zip"
    archive = zipfile.ZipFile(io.BytesIO(data))
    assert archive.testzip() is None
    files = {entry: archive.read(entry).decode() for entry in archive.namelist()}
    assert files == b.read_archive(out / "download" / "fixtures-all.json")
    method = zipfile.ZIP_DEFLATED if compressed else zipfile.ZIP_STORED
    assert {info.compress_type for info in archive.infolist()} == {method}
