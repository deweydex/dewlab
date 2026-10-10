"""Editing a page where it stands (assets/inpage-edit.js).

A small site is built with the source map on and served over HTTP. The browser
runs with service workers blocked so that its calls to api.github.com can be
answered by a fake GitHub in this file: the real client code runs, nothing
touches the network, and no token is real. The fake records what was committed
so each test can say what the repository would have received.
"""

from __future__ import annotations

import base64
import functools
import hashlib
import http.server
import json
import re
import shutil
import socketserver
import threading
from pathlib import Path

import pytest

DEWLAB = Path(__file__).resolve().parents[2]

PAGE = (
    '---\ntitle: "A Page"\nyear: "2026-2027"\nversion: 2026.08.23.1\n---\n\n'
    "# A Page\n\n"
    "First paragraph, with *emphasis* and `code`.\n\n"
    "Second paragraph.\n\n"
    "A paragraph with maths, $x + 1$, in it.\n\n"
    "- one\n- two\n\n"
    "{{include: setup/shared.md}}\n\n"
    "```python exec\nid: only\nprint(1)\n```\n"
)
COURSE = (
    "title: Fixtures\ncode: X1\nstatus: beta\ncard: A card.\ndescription: A description.\n"
    "contents:\n  - title: One\n    tutorials: [a-page]\n"
)
REPO = "/repos/deweydex/dewlab"


@pytest.fixture(scope="module")
def site(tmp_path_factory):
    sys_path = str(DEWLAB)
    import sys
    if sys_path not in sys.path:
        sys.path.insert(0, sys_path)
    import build as b

    root = tmp_path_factory.mktemp("dewlab-edit")
    (root / "tutorials" / "a-page").mkdir(parents=True)
    (root / "tutorials" / "a-page" / "a-page.md").write_text(PAGE)
    (root / "courses").mkdir()
    (root / "courses" / "fixtures.yaml").write_text(COURSE)
    (root / "courses" / "index.yaml").write_text("order:\n  - fixtures\n")
    (root / "setup").mkdir()
    (root / "setup" / "shared.md").write_text("> A shared note.")
    (root / "data").mkdir()
    shutil.copytree(DEWLAB / "assets", root / "assets")
    shutil.copytree(DEWLAB / "planning" / "curriculum", root / "planning" / "curriculum")
    (root / "pages").mkdir()
    for page in (DEWLAB / "pages").glob("*.md"):
        shutil.copy(page, root / "pages" / page.name)

    patch = pytest.MonkeyPatch()
    for name, value in {
        "ROOT": root, "TUTORIALS": root / "tutorials", "COURSES": root / "courses",
        "SETUP": root / "setup", "DATA": root / "data", "ASSETS": root / "assets",
        "SHELL": root / "assets" / "shell.html", "OUT": root / "site",
        "PAGES": root / "pages",
        "TOPIC_DATA": root / "planning" / "curriculum" / "topics.yaml",
        "TOPIC_GROUPS_DATA": root / "planning" / "curriculum" / "topic-groups.yaml",
        "OUTCOME_DATA": root / "planning" / "curriculum" / "outcomes.yaml",
        "SOURCE_MAP": True,
    }.items():
        patch.setattr(b, name, value)
    b.build(clean=True, standalone=True)
    patch.undo()
    return root


class _Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


class _Server(socketserver.TCPServer):
    allow_reuse_address = True

    def handle_error(self, request, client_address):
        pass


@pytest.fixture(scope="module")
def base_url(site):
    handler = functools.partial(_Quiet, directory=str(site / "site"))
    with _Server(("127.0.0.1", 0), handler) as server:
        threading.Thread(target=server.serve_forever, daemon=True).start()
        try:
            yield f"http://127.0.0.1:{server.server_address[1]}"
        finally:
            server.shutdown()


@pytest.fixture(scope="module")
def chromium(browser):
    """The session's browser from conftest.py. It is shared, not started here:
    Playwright's sync API cannot start twice in one process."""
    return browser


class FakeGitHub:
    """Answers the calls the editor makes, and keeps what it was sent."""

    def __init__(self, source: str, main_sha: str | None = None):
        self.source = source
        self.blob_sha = None  # set from the page's own manifest
        self.main_file_sha = main_sha
        self.blobs: list[str] = []
        self.refs: list[dict] = []
        self.patches: list[dict] = []
        self.pulls: list[dict] = []

    def __call__(self, route):
        request = route.request
        path = request.url.split("https://api.github.com", 1)[1]
        method = request.method
        body = json.loads(request.post_data) if request.post_data else {}

        def reply(data, status=200):
            route.fulfill(status=status, content_type="application/json", body=json.dumps(data))

        if method == "GET" and re.fullmatch(rf"{REPO}/git/blobs/\w+", path):
            return reply({"content": base64.b64encode(self.source.encode()).decode(), "encoding": "base64"})
        if method == "GET" and path.startswith(f"{REPO}/contents/"):
            return reply({"sha": self.main_file_sha or self.blob_sha})
        if method == "GET" and path == f"{REPO}/git/ref/heads/main":
            return reply({"object": {"sha": "basesha"}})
        if method == "GET" and re.fullmatch(rf"{REPO}/git/ref/heads/edit/.*", path):
            return reply({"object": {"sha": "tip1"}})
        if method == "GET" and path == f"{REPO}/git/commits/tip1":
            return reply({"tree": {"sha": "tree1"}})
        if method == "POST" and path == f"{REPO}/git/blobs":
            self.blobs.append(body["content"])
            return reply({"sha": f"blob{len(self.blobs)}"})
        if method == "POST" and path == f"{REPO}/git/trees":
            return reply({"sha": f"tree{len(self.blobs)}"})
        if method == "POST" and path == f"{REPO}/git/commits":
            return reply({"sha": f"commit{len(self.blobs)}"})
        if method == "POST" and path == f"{REPO}/git/refs":
            self.refs.append(body)
            return reply({})
        if method == "PATCH" and "/git/refs/heads/" in path:
            self.patches.append(body)
            return reply({})
        if method == "POST" and path == f"{REPO}/pulls":
            self.pulls.append(body)
            return reply({"html_url": "https://github.com/deweydex/dewlab/pull/999"})
        return reply({"message": f"unexpected {method} {path}"}, status=500)


@pytest.fixture()
def editing(chromium, base_url, site):
    """(page, fake) with a token stored, service workers blocked, GitHub faked."""
    context = chromium.new_context(viewport={"width": 1200, "height": 900}, service_workers="block")
    context.add_init_script("localStorage.setItem('dewlab:editor:token', 'a-token')")
    fake = FakeGitHub((site / "tutorials" / "a-page" / "a-page.md").read_text())
    context.route("https://api.github.com/**", fake)
    page = context.new_page()
    problems: list[str] = []
    # The site's own service-worker script reads `registration.scope`, which
    # does not exist while the test blocks service workers. That is the test's
    # doing, not the page's.
    page.on("pageerror", lambda error: problems.append(str(error))
            if "reading 'scope'" not in str(error) else None)
    page.goto(f"{base_url}/tutorials/a-page.html")
    page.wait_for_load_state("networkidle")
    manifest = page.evaluate("JSON.parse(document.getElementById('dewlab-manifest').textContent)")
    fake.blob_sha = manifest["edit"]["sha"]
    yield page, fake, manifest
    context.close()
    assert not problems, problems


def start(page):
    page.click("#dl-settings-toggle")
    page.click("#dl-edit-toggle")
    page.wait_for_selector("body.dl-editing")


def type_into(page, selector, text):
    page.click(selector)
    page.wait_for_selector(".dl-inplace .ProseMirror")
    page.keyboard.press("Control+End")
    page.keyboard.type(text)


def leave(page):
    """Click somewhere that is not a block, so the open block loses focus and closes."""
    page.click("#dl-edit-status")


def test_the_page_names_its_source_and_the_button_is_there_but_the_editor_is_not_loaded(editing, site):
    page, fake, manifest = editing
    assert manifest["edit"]["path"] == "tutorials/a-page/a-page.md"
    assert page.is_visible("#dl-settings-edit") is False  # the Settings panel itself is closed
    page.click("#dl-settings-toggle")
    assert page.is_visible("#dl-edit-toggle")
    assert page.evaluate("typeof window.dlEditSession") == "undefined"
    assert not page.evaluate("[...document.scripts].some(s => s.src.includes('inpage-edit'))")


def test_the_save_and_discard_buttons_appear_only_while_editing(editing):
    page, fake, manifest = editing
    page.click("#dl-settings-toggle")
    assert not page.is_visible("#dl-edit-save")
    page.click("#dl-edit-toggle")
    page.wait_for_selector("body.dl-editing")
    assert page.is_visible("#dl-edit-save") and page.is_visible("#dl-edit-discard")
    page.click("#dl-edit-toggle")  # now says "Stop editing"
    page.wait_for_function("!document.body.classList.contains('dl-editing')")
    assert not page.is_visible("#dl-edit-save")


def test_a_hash_edit_address_starts_editing_without_the_button(chromium, base_url, site):
    context = chromium.new_context(viewport={"width": 1200, "height": 900}, service_workers="block")
    context.add_init_script("localStorage.setItem('dewlab:editor:token', 'a-token')")
    source = site / "tutorials" / "a-page" / "a-page.md"
    fake = FakeGitHub(source.read_text())
    data = source.read_bytes()
    fake.blob_sha = hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()
    context.route("https://api.github.com/**", fake)
    page = context.new_page()
    page.goto(f"{base_url}/tutorials/a-page.html#edit")
    page.wait_for_selector("body.dl-editing", timeout=15000)
    context.close()


def test_a_narrow_screen_is_told_the_editor_needs_a_larger_one(chromium, base_url):
    context = chromium.new_context(viewport={"width": 600, "height": 900}, service_workers="block")
    page = context.new_page()
    page.goto(f"{base_url}/tutorials/a-page.html")
    page.click("#dl-settings-toggle")
    page.click("#dl-edit-toggle")
    page.wait_for_function("document.getElementById('dl-edit-status').textContent.includes('larger screen')")
    assert page.evaluate("document.body.classList.contains('dl-editing')") is False
    context.close()


def test_a_heading_and_a_plain_paragraph_edit_in_place_and_the_rest_is_locked_or_source(editing):
    page, fake, manifest = editing
    start(page)
    modes = page.evaluate("""[...document.querySelectorAll('main#dl-body > [data-md]')]
        .map(n => [n.tagName.toLowerCase(), n.dataset.dlEdit])""")
    assert modes == [["h1", "rich"], ["p", "rich"], ["p", "rich"], ["p", "source"],
                     ["ul", "source"], ["blockquote", ""], ["div", ""]]


def test_typing_in_a_paragraph_changes_that_paragraph_of_the_file_and_nothing_else(editing, site):
    page, fake, manifest = editing
    original = fake.source
    start(page)
    type_into(page, "main#dl-body > p:nth-of-type(2)", " Added.")
    leave(page)
    page.wait_for_function("document.getElementById('dl-edit-status').textContent.startsWith('1 block changed')")
    page.click("#dl-edit-save")
    page.wait_for_function("document.getElementById('dl-edit-status').textContent.includes('pull/999')")

    assert len(fake.blobs) == 1
    saved = fake.blobs[0]
    assert saved == original.replace("Second paragraph.", "Second paragraph. Added.")
    assert fake.refs and fake.refs[0]["ref"].startswith("refs/heads/edit/a-page-")
    assert fake.pulls[0]["draft"] is True


def test_a_block_that_was_opened_and_left_unchanged_is_not_an_edit(editing):
    page, fake, manifest = editing
    start(page)
    page.click("main#dl-body > p:nth-of-type(2)")
    page.wait_for_selector(".dl-inplace .ProseMirror")
    leave(page)
    page.wait_for_function("document.getElementById('dl-edit-status').textContent.startsWith('No changes')")
    assert page.is_disabled("#dl-edit-save")
    assert page.evaluate("document.querySelectorAll('.dl-inplace').length") == 0
    assert page.is_visible("main#dl-body > p:nth-of-type(2)")


def test_opening_a_paragraph_moves_nothing_on_the_page(editing):
    page, fake, manifest = editing
    start(page)
    page.click("#dl-settings-toggle")  # close Settings, so nothing overlaps
    tops = "[...document.querySelectorAll('main#dl-body > [data-md]:not([hidden])')].map(n => Math.round(n.getBoundingClientRect().top + scrollY))"
    before = page.evaluate(tops)
    page.click("main#dl-body > p:nth-of-type(1)")
    page.wait_for_selector(".dl-inplace .ProseMirror")
    after = page.evaluate(tops)
    assert before == after


def test_a_block_with_maths_edits_as_its_markdown(editing):
    page, fake, manifest = editing
    start(page)
    page.click("main#dl-body > p:nth-of-type(3)")
    box = page.wait_for_selector("textarea.dl-inplace-source")
    assert box.input_value() == "A paragraph with maths, $x + 1$, in it."
    box.fill("A paragraph with maths, $x + 2$, in it.")
    leave(page)
    page.wait_for_function("document.getElementById('dl-edit-status').textContent.startsWith('1 block changed')")
    page.click("#dl-edit-save")
    page.wait_for_function("document.getElementById('dl-edit-status').textContent.includes('pull/999')")
    assert fake.blobs[0] == fake.source.replace("$x + 1$", "$x + 2$")


def test_a_second_save_in_one_session_adds_a_commit_to_the_same_pull_request(editing):
    page, fake, manifest = editing
    start(page)
    type_into(page, "main#dl-body > p:nth-of-type(2)", " One.")
    leave(page)
    page.click("#dl-edit-save")
    page.wait_for_function("document.getElementById('dl-edit-status').textContent.includes('pull/999')")
    type_into(page, "main#dl-body > p:nth-of-type(1)", " Two.")
    leave(page)
    page.wait_for_function("document.getElementById('dl-edit-status').textContent.startsWith('2 blocks changed')")
    page.click("#dl-edit-save")
    page.wait_for_function("document.getElementById('dl-edit-status').textContent.startsWith('Saved')")
    assert len(fake.pulls) == 1 and len(fake.refs) == 1 and len(fake.patches) == 1
    assert fake.blobs[1] == fake.source.replace("Second paragraph.", "Second paragraph. One.").replace(
        "`code`.", "`code`. Two.")


def test_a_page_that_changed_on_main_since_the_build_is_not_saved_over(editing):
    page, fake, manifest = editing
    fake.main_file_sha = "somebody-elses-sha"
    start(page)
    type_into(page, "main#dl-body > p:nth-of-type(2)", " Added.")
    leave(page)
    page.click("#dl-edit-save")
    page.wait_for_function("document.getElementById('dl-edit-status').textContent.includes('changed on GitHub')")
    assert fake.blobs == [] and fake.pulls == []


def test_discard_puts_the_page_back_as_it_was(editing):
    page, fake, manifest = editing
    start(page)
    before = page.inner_text("main#dl-body")
    type_into(page, "main#dl-body > p:nth-of-type(2)", " Added.")
    leave(page)
    page.click("#dl-edit-discard")
    page.wait_for_function("document.getElementById('dl-edit-status').textContent.startsWith('No changes')")
    assert page.inner_text("main#dl-body") == before


def test_stopping_with_unsaved_changes_asks_first_and_cancel_keeps_them(editing):
    page, fake, manifest = editing
    start(page)
    type_into(page, "main#dl-body > p:nth-of-type(2)", " Added.")
    leave(page)
    messages = []
    page.on("dialog", lambda dialog: (messages.append(dialog.message), dialog.dismiss()))
    page.click("#dl-edit-toggle")  # "Stop editing"
    page.wait_for_timeout(200)
    assert messages and "not saved" in messages[0]
    assert page.evaluate("document.body.classList.contains('dl-editing')")
    assert page.inner_text("#dl-edit-status").startswith("1 block changed")


def test_stopping_with_unsaved_changes_and_agreeing_puts_the_page_back(editing):
    page, fake, manifest = editing
    start(page)
    before = page.inner_text("main#dl-body")
    type_into(page, "main#dl-body > p:nth-of-type(2)", " Added.")
    leave(page)
    page.on("dialog", lambda dialog: dialog.accept())
    page.click("#dl-edit-toggle")
    page.wait_for_function("!document.body.classList.contains('dl-editing')")
    assert page.inner_text("main#dl-body") == before
    assert fake.blobs == []


def test_stopping_after_saving_does_not_ask(editing):
    page, fake, manifest = editing
    start(page)
    type_into(page, "main#dl-body > p:nth-of-type(2)", " Added.")
    leave(page)
    page.click("#dl-edit-save")
    page.wait_for_function("document.getElementById('dl-edit-status').textContent.startsWith('Saved')")
    asked = []
    page.on("dialog", lambda dialog: (asked.append(dialog.message), dialog.dismiss()))
    page.click("#dl-edit-toggle")
    page.wait_for_function("!document.body.classList.contains('dl-editing')")
    assert asked == []
    page.wait_for_function("document.getElementById('dl-edit-status').textContent.includes('pull/999')")


def test_forgetting_the_token_removes_it_and_hides_the_button(editing):
    page, fake, manifest = editing
    page.click("#dl-settings-toggle")
    assert page.is_visible("#dl-edit-forget")
    page.click("#dl-edit-forget")
    assert page.evaluate("localStorage.getItem('dewlab:editor:token')") is None
    assert not page.is_visible("#dl-edit-forget")
    assert "forgotten" in page.inner_text("#dl-edit-status")


def test_without_a_token_the_page_asks_for_one_and_keeps_it_when_given(chromium, base_url, site):
    context = chromium.new_context(viewport={"width": 1200, "height": 900}, service_workers="block")
    source = site / "tutorials" / "a-page" / "a-page.md"
    fake = FakeGitHub(source.read_text())
    data = source.read_bytes()
    fake.blob_sha = hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()
    context.route("https://api.github.com/**", fake)
    page = context.new_page()
    page.goto(f"{base_url}/tutorials/a-page.html")
    page.click("#dl-settings-toggle")
    assert not page.is_visible("#dl-edit-forget")
    page.click("#dl-edit-toggle")
    page.fill("#dl-edit-token", "pasted-token")
    page.click("#dl-edit-gate button[type=submit]")
    page.wait_for_selector("body.dl-editing")
    assert page.evaluate("localStorage.getItem('dewlab:editor:token')") == "pasted-token"
    assert page.is_visible("#dl-edit-forget")
    context.close()


def test_a_downloaded_copy_carries_no_editor(site):
    copies = list((site / "site" / "download").rglob("a-page*.html"))
    assert copies, "no downloadable copy was built"
    for copy in copies:
        # Outside the inlined stylesheet and runtime, which may mention the editor.
        html = re.sub(r"<(style|script)\b.*?</\1>", "", copy.read_text(), flags=re.DOTALL)
        assert 'id="dl-settings-edit"' not in html and "inpage-edit" not in html
        assert "data-md=" not in html and "dl-edit:" not in html
