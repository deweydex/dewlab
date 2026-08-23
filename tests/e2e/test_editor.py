"""The editor page, driven against a fake GitHub.

Every test here injects its own client, so nothing touches the network and no
token is needed. That is the reason `start()` takes a client rather than making
one: a page that could only be tested with real credentials would not be
tested.

    python3 -m pytest tests/e2e/test_editor.py -q
"""

from __future__ import annotations

import json

import pytest

# One small repository, shaped like the real one: two tutorials in a series,
# an order file, and a second series with one tutorial in it.
REPO = {
    "tutorials/fixtures/maths.order.yaml":
        "series: Maths and programming\norder:\n  - first-steps\n  - next-steps\n",
    "tutorials/fixtures/first-steps.md":
        '---\ntitle: "First Steps"\nslug: first-steps\nmodule: fixtures\n'
        'module_title: "Fixtures"\nyear: "2026-2027"\nseries: maths\nversion: 1\n---\n\n'
        "# First Steps\n\nProse.\n\n## Adding up\n\n```python exec\nid: adding-up-1\n"
        "print(1 + 1)\n```\n",
    "tutorials/fixtures/next-steps.md":
        '---\ntitle: "Next Steps"\nslug: next-steps\nmodule: fixtures\n'
        'module_title: "Fixtures"\nyear: "2026-2027"\nseries: maths\nversion: 1\n---\n\n'
        "# Next Steps\n\nMore prose.\n",
    "tutorials/fixtures/looking-back.order.yaml":
        "series: Reflections and review\norder:\n  - looking-back\n",
    "tutorials/fixtures/looking-back.md":
        '---\ntitle: "Looking Back"\nslug: looking-back\nmodule: fixtures\n'
        'module_title: "Fixtures"\nyear: "2026-2027"\nseries: looking-back\nversion: 1\n---\n\n'
        "# Looking Back\n\nProse.\n",
}

FAKE_CLIENT = """
(files) => ({
  committed: null,
  listTutorials: async () => ({ base: "basesha", paths: Object.keys(files) }),
  read: async (path) => files[path],
  commit: async (change) => {
    globalThis.__committed = change;
    return "https://github.com/deweydex/dewlab/pull/999";
  },
})
"""


@pytest.fixture
def editor(browser, base_url):
    """The editor page with a fake GitHub behind it, already loaded."""
    context = browser.new_context(viewport={"width": 1280, "height": 950})
    tab = context.new_page()
    tab.goto(f"{base_url}/editor.html")
    tab.wait_for_selector("#dl-editor")
    tab.evaluate(
        """async ({files, factory, url}) => {
             const mod = await import(url);
             const client = eval(factory)(files);
             await mod.start(document.getElementById("dl-editor"), client);
           }""",
        {"files": REPO, "factory": FAKE_CLIENT,
         "url": "./" + _runtime_url(tab)},
    )
    tab.wait_for_selector(".dl-editor-card")
    yield tab
    context.close()


def _runtime_url(tab) -> str:
    """The versioned editor.js the page actually loaded.

    Asset URLs carry a content hash, so hard-coding `assets/editor.js` here
    would import a second, unversioned copy — or nothing at all.
    """
    src = tab.get_attribute('script[src*="editor.js"]', "src")
    assert src, "the editor page loads no editor.js"
    return src


class TestTheListView:
    def test_every_series_and_tutorial_is_listed(self, editor):
        titles = editor.eval_on_selector_all(
            ".dl-editor-open", "e => e.map(b => b.textContent)")
        assert titles == ["First Steps", "Next Steps", "Looking Back"]

    def test_a_series_is_headed_by_its_name_from_the_order_file(self, editor):
        heads = editor.eval_on_selector_all(
            ".dl-editor-series h2", "e => e.map(h => h.textContent)")
        assert "Maths and programming" in heads
        assert "Reflections and review" in heads

    def test_moving_a_tutorial_reorders_it(self, editor):
        editor.click('.dl-editor-card[data-slug="next-steps"] .dl-editor-up')
        titles = editor.eval_on_selector_all(
            ".dl-editor-open", "e => e.map(b => b.textContent)")
        assert titles[:2] == ["Next Steps", "First Steps"]

    def test_moving_past_the_end_does_nothing(self, editor):
        editor.click('.dl-editor-card[data-slug="first-steps"] .dl-editor-up')
        titles = editor.eval_on_selector_all(
            ".dl-editor-open", "e => e.map(b => b.textContent)")
        assert titles[:2] == ["First Steps", "Next Steps"]

    def test_nothing_can_be_committed_until_something_changes(self, editor):
        assert editor.get_attribute("#dl-editor-save", "disabled") is not None
        editor.click('.dl-editor-card[data-slug="next-steps"] .dl-editor-up')
        assert editor.get_attribute("#dl-editor-save", "disabled") is None


class TestInsertingAndCreating:
    def test_inserting_writes_a_tutorial_and_lists_it(self, editor):
        editor.once("dialog", lambda d: d.accept("Halfway There"))
        editor.click(".dl-editor-series:first-of-type .dl-editor-gap:nth-of-type(1) button")
        titles = editor.eval_on_selector_all(
            ".dl-editor-open", "e => e.map(b => b.textContent)")
        assert "Halfway There" in titles

    def test_a_new_tutorial_starts_from_the_house_template(self, editor):
        editor.once("dialog", lambda d: d.accept("Halfway There"))
        editor.click(".dl-editor-series:first-of-type .dl-editor-new")
        written = editor.evaluate(
            "globalThis.dewlabEditor.state.files.get('tutorials/fixtures/halfway-there.md')")
        assert 'title: "Halfway There"' in written
        assert "slug: halfway-there" in written
        # The template carries the house conventions, which is most of its point.
        assert "```python exec" in written
        assert "## Reflection" in written

    def test_a_new_tutorial_inherits_the_module_details_of_its_neighbours(self, editor):
        editor.once("dialog", lambda d: d.accept("Halfway There"))
        editor.click(".dl-editor-series:first-of-type .dl-editor-new")
        written = editor.evaluate(
            "globalThis.dewlabEditor.state.files.get('tutorials/fixtures/halfway-there.md')")
        assert 'module_title: "Fixtures"' in written
        assert 'year: "2026-2027"' in written
        assert "series: maths" in written


class TestEditingWhatIsInside:
    def open_first(self, editor):
        editor.click('.dl-editor-card[data-slug="first-steps"] .dl-editor-open')
        editor.wait_for_selector(".dl-editor-body")

    def test_a_tutorial_opens_with_its_body_and_not_its_frontmatter(self, editor):
        self.open_first(editor)
        body = editor.input_value(".dl-editor-body")
        assert body.startswith("# First Steps")
        assert "slug: first-steps" not in body

    def test_the_report_counts_what_the_build_will_see(self, editor):
        self.open_first(editor)
        assert "1 runnable cell" in editor.inner_text("#dl-editor-report")

    def test_renaming_a_cell_id_warns_that_student_work_is_lost(self, editor):
        """The one thing the editor knows that the build cannot: by the time
        the build runs, the rename has already happened."""
        self.open_first(editor)
        editor.fill(".dl-editor-body",
                    editor.input_value(".dl-editor-body").replace("adding-up-1", "adding-up-2"))
        warning = editor.inner_text(".dl-editor-danger")
        assert "throws away the work every student saved" in warning
        assert "adding-up-1" in warning

    def test_an_unclosed_fence_is_reported_before_it_reaches_the_build(self, editor):
        self.open_first(editor)
        editor.fill(".dl-editor-body", "# T\n\n```python exec\nid: a-1\nprint(1)\n")
        assert "opened and never closed" in editor.inner_text("#dl-editor-report")

    def test_two_cells_sharing_an_id_are_reported(self, editor):
        self.open_first(editor)
        editor.fill(
            ".dl-editor-body",
            "# T\n\n```python exec\nid: a-1\nprint(1)\n```\n\n"
            "```python exec\nid: a-1\nprint(2)\n```\n")
        assert 'used 2 times' in editor.inner_text("#dl-editor-report")

    def test_a_cell_with_no_id_is_reported(self, editor):
        self.open_first(editor)
        editor.fill(".dl-editor-body", "# T\n\n```python exec\nprint(1)\n```\n")
        assert "has no id" in editor.inner_text("#dl-editor-report")

    def test_an_illustrative_fence_is_not_counted_as_a_cell(self, editor):
        """`python exec` makes a cell; a plain fence is illustrative code. The
        editor has to draw that line exactly where build.py draws it."""
        self.open_first(editor)
        editor.fill(".dl-editor-body", "# T\n\n```python\nprint(1)\n```\n")
        assert "0 runnable cells" in editor.inner_text("#dl-editor-report")


class TestCommitting:
    def test_a_reorder_commits_the_order_file_and_opens_a_pull_request(self, editor):
        editor.click('.dl-editor-card[data-slug="next-steps"] .dl-editor-up')
        editor.once("dialog", lambda d: d.accept("Put next steps first"))
        editor.click("#dl-editor-save")
        editor.wait_for_function("globalThis.__committed !== undefined")
        change = editor.evaluate("globalThis.__committed")
        assert change["message"] == "Put next steps first"
        assert change["base"] == "basesha"
        assert [f["path"] for f in change["files"]] == ["tutorials/fixtures/maths.order.yaml"]
        written = change["files"][0]["text"]
        assert written.index("next-steps") < written.index("first-steps")
        # The series' own name survives the rewrite; only the list changes.
        assert "series: Maths and programming" in written

    def test_the_commit_lands_on_a_new_branch_never_on_main(self, editor):
        editor.click('.dl-editor-card[data-slug="next-steps"] .dl-editor-up')
        editor.once("dialog", lambda d: d.accept("Put next steps first"))
        editor.click("#dl-editor-save")
        editor.wait_for_function("globalThis.__committed !== undefined")
        branch = editor.evaluate("globalThis.__committed.branch")
        assert branch.startswith("editor/")
        assert branch != "main"

    def test_an_insertion_commits_both_the_tutorial_and_the_order_file(self, editor):
        """Two files in one commit, because either alone leaves the repository
        describing a series that does not exist."""
        editor.once("dialog", lambda d: d.accept("Halfway There"))
        editor.click(".dl-editor-series:first-of-type .dl-editor-new")
        editor.once("dialog", lambda d: d.accept("Add halfway there"))
        editor.click("#dl-editor-save")
        editor.wait_for_function("globalThis.__committed !== undefined")
        paths = sorted(f["path"] for f in editor.evaluate("globalThis.__committed.files"))
        assert paths == [
            "tutorials/fixtures/halfway-there.md",
            "tutorials/fixtures/maths.order.yaml",
        ]

    def test_the_save_button_goes_quiet_again_afterwards(self, editor):
        editor.click('.dl-editor-card[data-slug="next-steps"] .dl-editor-up')
        editor.once("dialog", lambda d: d.accept("Put next steps first"))
        editor.click("#dl-editor-save")
        editor.wait_for_function("globalThis.__committed !== undefined")
        editor.wait_for_selector("#dl-editor-save[disabled]")
        assert "pull/999" in editor.inner_text("#dl-editor-status")
