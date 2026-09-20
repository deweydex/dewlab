"""start() takes a client rather than building one, so every test here
injects a fake and nothing touches the network or needs a token."""

from __future__ import annotations

import json
import re

import pytest

REPO = {
    "courses/fixtures.yaml":
        "title: Fixtures\ncontents:\n"
        "  - title: Maths and programming\n    tutorials:\n"
        "      - first-steps\n"
        "      - next-steps\n"
        "  - title: Reflections and review\n    tutorials:\n"
        "      - looking-back\n",
    "tutorials/first-steps/first-steps.md":
        '---\ntitle: "First Steps"\n'
        'year: "2026-2027"\nversion: 2026.08.23.1\n---\n\n'
        "# First Steps\n\nProse.\n\n## Adding up\n\n```python exec\nid: adding-up-1\n"
        "print(1 + 1)\n```\n",
    "tutorials/next-steps/next-steps.md":
        '---\ntitle: "Next Steps"\n'
        'year: "2026-2027"\nversion: 2026.08.23.1\n---\n\n'
        "# Next Steps\n\nMore prose.\n",
    "tutorials/looking-back/looking-back.md":
        '---\ntitle: "Looking Back"\n'
        'year: "2026-2027"\nversion: 2026.08.23.1\n---\n\n'
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


def _released(slug: str, version: str, cells: str, status: str = "live") -> str:
    return (
        f'---\ntitle: "Two Takes"\nyear: "2026-2027"\n'
        f"version: {version}\nstatus: {status}\n---\n\n# Two Takes\n\nProse.\n\n"
        "## A section\n\n" + cells
    )


def _cell(cell_id: str) -> str:
    return f"```python exec\nid: {cell_id}\nprint(1)\n```\n\n"


VERSIONED = {
    "courses/fixtures.yaml":
        "title: Fixtures\ncontents:\n"
        "  - title: Maths and programming\n    tutorials:\n"
        "      - first-steps\n"
        "      - two-takes\n",
    "tutorials/first-steps/first-steps.md":
        '---\ntitle: "First Steps"\nyear: "2026-2027"\n'
        "version: 2026.06.02.1\nstatus: live\n---\n\n# First Steps\n\nProse.\n\n"
        "## Adding up\n\n" + _cell("adding-up-1"),
    "tutorials/two-takes/v2026.06.02.1.md":
        _released("two-takes", "2026.06.02.1", _cell("shared-one") + _cell("only-in-june")),
    "tutorials/two-takes/v2026.09.15.1.md":
        _released("two-takes", "2026.09.15.1",
                  _cell("shared-one") + _cell("only-in-september")),
    "tutorials/old-ways/v2026.01.01.1.md":
        _released("old-ways", "2026.01.01.1", _cell("old-one"), status="archived"),
    "tutorials/old-ways/v2026.03.01.1.md":
        _released("old-ways", "2026.03.01.1", _cell("old-two"), status="archived"),
}


def _open(browser, base_url, files, factory=FAKE_CLIENT):
    context = browser.new_context(viewport={"width": 1280, "height": 950})
    tab = context.new_page()
    tab.goto(f"{base_url}/editor.html")
    tab.wait_for_selector("#dl-editor")
    tab.evaluate(
        """async ({files, factory, url}) => {
             const mod = await import(url);
             globalThis.__editorModule = mod;
             const client = eval(factory)(files);
             await mod.start(document.getElementById("dl-editor"), client);
           }""",
        {"files": files, "factory": factory, "url": "./" + _runtime_url(tab)},
    )
    tab.wait_for_selector(".dl-editor-card")
    return context, tab


@pytest.fixture
def editor(browser, base_url):
    context, tab = _open(browser, base_url, REPO)
    yield tab
    context.close()


@pytest.fixture
def versioned(browser, base_url):
    context, tab = _open(browser, base_url, VERSIONED)
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


def _big_repo(count: int) -> dict:
    """40 crosses load()'s READ_CONCURRENCY batch boundary (16, in
    assets/editor.js) more than once; each tutorial's title carries its own
    index so a batch mix-up would actually be caught."""
    order = [f"tutorial-{i:03d}" for i in range(count)]
    files = {
        "courses/fixtures.yaml":
            "title: Fixtures\ncontents:\n  - title: Big\n    tutorials:\n"
            + "".join(f"      - {slug}\n" for slug in order),
    }
    for i, slug in enumerate(order):
        files[f"tutorials/{slug}/{slug}.md"] = (
            f'---\ntitle: "Tutorial number {i}"\nyear: "2026-2027"\n'
            f"version: 2026.08.23.1\n---\n\n# Tutorial number {i}\n\nProse.\n"
        )
    return files


SLOW_CLIENT = """
(files) => ({
  committed: null,
  listTutorials: async () => ({ base: "basesha", paths: Object.keys(files) }),
  read: async (path) => {
    await new Promise((resolve) => setTimeout(resolve, Math.random() * 20));
    return files[path];
  },
  commit: async () => "x",
})
"""


class TestLoadingManyTutorialsAtOnce:
    @pytest.mark.parametrize("factory", [FAKE_CLIENT, SLOW_CLIENT],
                             ids=["resolves_in_order", "resolves_out_of_order"])
    def test_every_tutorial_in_a_large_repo_loads_with_the_right_content(self, browser, base_url, factory):
        files = _big_repo(40)
        context, tab = _open(browser, base_url, files, factory=factory)
        try:
            titles = tab.eval_on_selector_all(
                ".dl-editor-open", "e => e.map(b => b.textContent)")
            assert len(titles) == 40
            assert set(titles) == {f"Tutorial number {i}" for i in range(40)}
        finally:
            context.close()


class TestTheListView:
    def test_every_series_and_tutorial_is_listed(self, editor):
        titles = editor.eval_on_selector_all(
            ".dl-editor-open", "e => e.map(b => b.textContent)")
        assert titles == ["First Steps", "Next Steps", "Looking Back"]

    def test_a_series_is_headed_by_its_course_and_its_name_from_the_course_file(self, editor):
        heads = editor.eval_on_selector_all(
            ".dl-editor-series h2", "e => e.map(h => h.textContent)")
        assert "Fixtures — Maths and programming" in heads
        assert "Fixtures — Reflections and review" in heads

    @pytest.mark.parametrize("slug, expected", [
        ("next-steps", ["Next Steps", "First Steps"]),
        ("first-steps", ["First Steps", "Next Steps"]),
    ], ids=["reorders_it", "past_the_end_does_nothing"])
    def test_moving_a_tutorial_with_the_up_control(self, editor, slug, expected):
        editor.click(f'.dl-editor-card[data-slug="{slug}"] .dl-editor-up')
        titles = editor.eval_on_selector_all(
            ".dl-editor-open", "e => e.map(b => b.textContent)")
        assert titles[:2] == expected

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

    def test_a_new_tutorial_starts_from_the_house_template_and_carries_only_what_is_its_own(self, editor):
        """Where it sits is a line in the course file, added alongside."""
        editor.once("dialog", lambda d: d.accept("Halfway There"))
        editor.click(".dl-editor-series:first-of-type .dl-editor-new")
        written = editor.evaluate(
            "globalThis.dewlabEditor.state.files.get('tutorials/halfway-there/halfway-there.md')")
        assert 'title: "Halfway There"' in written
        assert "```python exec" in written
        assert "## Reflection" in written
        assert 'year: "2026-2027"' in written
        for field in ("slug:", "module:", "module_title:", "series:"):
            assert field not in written
        listed = editor.evaluate(
            """() => [...globalThis.dewlabEditor.state.series.values()]
                 .find((s) => s.name === "maths-and-programming").order""")
        assert listed == ["first-steps", "next-steps", "halfway-there"]

    def test_an_id_that_is_taken_is_refused_and_says_where_it_is(self, editor):
        editor.once("dialog", lambda d: d.accept("Looking Back"))
        editor.click(".dl-editor-series:first-of-type .dl-editor-new")
        assert "The id looking-back is taken" in editor.inner_text("#dl-editor-status")
        assert "Fixtures" in editor.inner_text("#dl-editor-status")
        assert editor.get_attribute("#dl-editor-save", "disabled") is not None


class TestEditingWhatIsInside:
    """No <textarea> to fill() — globalThis.dewlabEditor exposes getBody()/
    editBody() instead. editBody(), not setBody(), because a few tests below
    compare against what was on screen when opened, which setBody's remount
    would reset."""

    def open_first(self, editor):
        editor.click('.dl-editor-card[data-slug="first-steps"] .dl-editor-open')
        editor.wait_for_selector(".dl-editor-body")

    def body_of(self, editor) -> str:
        return editor.evaluate("() => globalThis.dewlabEditor.getBody()")

    def edit_body(self, editor, text: str) -> None:
        editor.evaluate("(md) => globalThis.dewlabEditor.editBody(md)", text)

    def test_a_tutorial_opens_with_its_body_and_not_its_frontmatter(self, editor):
        self.open_first(editor)
        body = self.body_of(editor)
        assert body.startswith("# First Steps")
        assert "slug: first-steps" not in body

    def test_the_report_counts_what_the_build_will_see(self, editor):
        self.open_first(editor)
        assert "1 runnable cell" in editor.inner_text("#dl-editor-report")

    def test_renaming_a_cell_id_warns_that_student_work_is_orphaned_and_that_releasing_is_the_way_not_to(self, editor):
        """The one thing the editor knows that the build cannot: by the time
        the build runs, the rename has already happened. The second half of
        this used to say the work was thrown away full stop, until releases
        arrived and made this box argue with the proposal underneath it."""
        self.open_first(editor)
        self.edit_body(editor, self.body_of(editor).replace("adding-up-1", "adding-up-2"))
        warning = editor.inner_text(".dl-editor-report")
        assert "orphaned" in warning
        assert "adding-up-1" in warning
        assert "Released instead, nothing is orphaned" in warning

    @pytest.mark.parametrize("markdown, expected", [
        ("# T\n\n```python exec\nid: a-1\nprint(1)\n", "opened and never closed"),
        ("# T\n\n```python exec\nid: a-1\nprint(1)\n```\n\n"
         "```python exec\nid: a-1\nprint(2)\n```\n", "used 2 times"),
        ("# T\n\n```python exec\nprint(1)\n```\n", "has no id"),
        # The editor has to draw the cell/illustrative-fence line exactly
        # where build.py draws it.
        ("# T\n\n```python\nprint(1)\n```\n", "0 runnable cells"),
    ], ids=["unclosed_fence", "duplicate_id", "no_id", "illustrative_fence_not_a_cell"])
    def test_the_report_surfaces_a_problem_before_it_reaches_the_build(self, editor, markdown, expected):
        self.open_first(editor)
        self.edit_body(editor, markdown)
        assert expected in editor.inner_text("#dl-editor-report")


LINKS = {
    "courses/fixtures.yaml":
        "title: Fixtures\ncontents:\n"
        "  - title: Maths and programming\n    tutorials:\n"
        "      - first-steps\n",
    "tutorials/first-steps/first-steps.md":
        '---\ntitle: "First Steps"\n'
        'year: "2026-2027"\nversion: 2026.08.23.1\n---\n\n'
        "# First Steps\n\n## A Grid of Numbers\n\n"
        "```python exec\nid: adding-up-1\n# not a heading\nprint(1)\n```\n\nProse after the cell.\n",
    "courses/other.yaml":
        "title: Other\ncontents:\n"
        "  - title: Other\n    tutorials:\n"
        "      - next-steps\n",
    "tutorials/next-steps/next-steps.md":
        '---\ntitle: "Next Steps"\n'
        'year: "2026-2027"\nversion: 2026.08.23.1\n---\n\n'
        "# Next Steps\n\nProse.\n",
}


@pytest.fixture
def links(browser, base_url):
    context, tab = _open(browser, base_url, LINKS)
    yield tab
    context.close()


class TestTutorialLinkChecking:
    """A dead `tutorial:slug#anchor` link is the one thing build.py already
    refuses that the editor's own report did not catch — this closes that
    gap so it surfaces here rather than after a commit fails CI."""

    def open_first(self, tab):
        tab.click('.dl-editor-card[data-slug="first-steps"] .dl-editor-open')
        tab.wait_for_selector(".dl-editor-body")

    def edit_body(self, tab, text: str) -> None:
        tab.evaluate("(md) => globalThis.dewlabEditor.editBody(md)", text)

    @pytest.mark.parametrize("markdown, expected, present", [
        ("# T\n\nSee [it](tutorial:nope-not-real).\n",
         "does not match any tutorial", True),
        ("# T\n\nSee [it](tutorial:next-steps).\n",
         "does not match", False),
        # Appends to the body rather than replacing it outright, since
        # first-steps is both the tutorial being edited and the one
        # supplying the anchor being linked to — replacing it would delete
        # that anchor.
        ("# First Steps\n\n## A Grid of Numbers\n\n"
         "See [it](tutorial:first-steps#a-grid-of-numbers).\n\n"
         "```python exec\nid: adding-up-1\nprint(1)\n```\n",
         "no heading or cell", False),
        ("# First Steps\n\n## A Grid of Numbers\n\n"
         "See [it](tutorial:first-steps#adding-up-1).\n\n"
         "```python exec\nid: adding-up-1\nprint(1)\n```\n",
         "no heading or cell", False),
        ("# T\n\nSee [it](tutorial:first-steps#not-a-real-anchor).\n",
         'no heading or cell "not-a-real-anchor"', True),
    ], ids=["unknown_tutorial", "real_tutorial_other_course",
            "real_heading_anchor", "real_cell_anchor", "missing_anchor"])
    def test_link_checking_reports_or_clears_a_link(self, links, markdown, expected, present):
        self.open_first(links)
        self.edit_body(links, markdown)
        report = links.inner_text("#dl-editor-report")
        if present:
            assert expected in report
        else:
            assert expected not in report

    def test_a_python_comment_is_not_mistaken_for_a_heading(self, links):
        """build.py strips fences before scanning for headings, so a `#`
        comment inside a cell is never confused with one; the editor has to
        do the same on raw source rather than count it as a third heading."""
        self.open_first(links)
        report = links.inner_text("#dl-editor-report")
        assert "2 headings" in report
        assert "3 headings" not in report


class TestLinkPicker:
    """Search-and-insert a `[title](tutorial:slug#anchor)` link, rather than
    typing a slug from memory and finding out it was wrong only from
    TestTutorialLinkChecking's report, after the fact."""

    def open(self, tab, slug):
        tab.click(f'.dl-editor-card[data-slug="{slug}"] .dl-editor-open')
        tab.wait_for_selector(".dl-editor-body .ProseMirror")

    def open_picker(self, tab):
        # Clicking the ProseMirror root itself and pressing Control+End was
        # not reliable once a fixture's last cell was a code fence: Crepe's
        # CodeMirror node view can end up with the caret instead, so the
        # link ends up inside the cell, unmarked (code nodes carry no
        # marks) — clicking the trailing paragraph directly, whatever it
        # says, puts the caret in real prose at the true end of the
        # document without depending on Control+End's cross-node behaviour.
        tab.click(".dl-editor-body .ProseMirror p:last-of-type")
        tab.keyboard.press("End")
        tab.click("text=Link to another tutorial")
        tab.wait_for_selector(".dl-editor-linkpicker-row")

    def body_of(self, tab) -> str:
        return tab.evaluate("() => globalThis.dewlabEditor.getBody()")

    def test_opening_the_picker_lists_every_tutorial(self, links):
        self.open(links, "first-steps")
        self.open_picker(links)
        rows = links.inner_text(".dl-editor-linkpicker-results")
        assert "Next Steps" in rows
        # The id and the course beside each title, since two tutorials may
        # share a title.
        assert "next-steps · Other" in rows
        assert "first-steps · Fixtures" in rows

    def test_searching_narrows_to_matching_tutorials(self, links):
        self.open(links, "first-steps")
        self.open_picker(links)
        links.fill(".dl-editor-linkpicker-search", "next")
        rows = links.locator(".dl-editor-linkpicker-row")
        assert rows.count() == 1
        assert "Next Steps" in rows.inner_text()

    def test_a_query_matching_nothing_says_so(self, links):
        self.open(links, "first-steps")
        self.open_picker(links)
        links.fill(".dl-editor-linkpicker-search", "zzzznope")
        assert "No tutorials match" in links.inner_text(".dl-editor-linkpicker-results")

    def test_picking_a_tutorial_inserts_a_link_to_it_and_closes_the_picker(self, links):
        self.open(links, "first-steps")
        self.open_picker(links)
        links.fill(".dl-editor-linkpicker-search", "next")
        links.click(".dl-editor-linkpicker-pick")
        assert "[Next Steps](tutorial:next-steps)" in self.body_of(links)
        assert not links.is_visible(".dl-editor-linkpicker-row")

    def test_a_heading_and_a_cell_anchor_are_both_offered(self, links):
        self.open(links, "next-steps")
        self.open_picker(links)
        links.fill(".dl-editor-linkpicker-search", "first")
        results = links.inner_text(".dl-editor-linkpicker-results")
        assert "a-grid-of-numbers" in results
        assert "adding-up-1" in results

    def test_picking_an_anchor_inserts_the_anchored_link(self, links):
        self.open(links, "next-steps")
        self.open_picker(links)
        links.fill(".dl-editor-linkpicker-search", "first")
        links.click('.dl-editor-linkpicker-anchor:text-is("adding-up-1")')
        assert "[First Steps](tutorial:first-steps#adding-up-1)" in self.body_of(links)


class TestCodeCompletion:
    """A `python exec` block is Crepe's own CodeMirror, wired to the same
    static completion sources tutorial-runtime.js gives a student
    (see test_autocomplete.py) — an author gets the same completions
    writing a cell as a student gets running it."""

    def open_first(self, editor):
        editor.click('.dl-editor-card[data-slug="first-steps"] .dl-editor-open')
        editor.wait_for_selector(".milkdown-code-block .cm-content")

    def code_cell(self, editor):
        return editor.locator(".milkdown-code-block .cm-content")

    def completion_labels(self, editor):
        return editor.eval_on_selector_all(
            ".cm-tooltip-autocomplete .cm-completionLabel", "els => els.map(e => e.textContent)")

    def test_typing_a_partial_builtin_offers_it(self, editor):
        self.open_first(editor)
        cell = self.code_cell(editor)
        cell.click()
        editor.keyboard.press("Control+End")
        editor.keyboard.type("\nlis")
        editor.wait_for_selector(".cm-tooltip-autocomplete")
        assert "list" in self.completion_labels(editor)

    def test_accepting_a_completion_inserts_it(self, editor):
        self.open_first(editor)
        cell = self.code_cell(editor)
        cell.click()
        editor.keyboard.press("Control+End")
        editor.keyboard.type("\nlis")
        editor.wait_for_selector(".cm-tooltip-autocomplete")
        editor.keyboard.press("Enter")
        assert "list" in cell.inner_text()


class TestCrepeIsActuallyThemed:
    """tutorial-style.css defines Crepe's --crepe-* custom properties itself,
    without one of Crepe's own skins — undefined, they silently produced two
    live bugs: a transparent slash menu, and no visible cursor at all."""

    def open_first(self, editor):
        editor.click('.dl-editor-card[data-slug="first-steps"] .dl-editor-open')
        editor.wait_for_selector(".dl-editor-body .ProseMirror")

    def test_the_slash_menu_is_not_transparent(self, editor):
        self.open_first(editor)
        editor.click(".dl-editor-body .ProseMirror p:has-text('Prose.')")
        editor.keyboard.press("End")
        editor.keyboard.type("\n/")
        editor.wait_for_selector(".milkdown-slash-menu[data-show='true']")
        background = editor.eval_on_selector(
            ".milkdown-slash-menu", "el => getComputedStyle(el).backgroundColor")
        assert background not in ("rgba(0, 0, 0, 0)", "transparent")

    def test_a_visible_cursor_is_drawn_in_place_of_the_hidden_native_one(self, editor):
        """The native caret is deliberately hidden (prosemirror-virtual-cursor
        draws its own instead) — this checks that replacement, not the
        native one."""
        self.open_first(editor)
        editor.click(".dl-editor-body .ProseMirror p:has-text('Prose.')")
        editor.wait_for_selector(".dl-editor-body .prosemirror-virtual-cursor")
        info = editor.eval_on_selector(
            ".dl-editor-body .prosemirror-virtual-cursor",
            "el => { const cs = getComputedStyle(el); "
            "return {color: cs.borderLeftColor, opacity: cs.opacity, width: el.getBoundingClientRect().width}; }")
        assert info["color"] not in ("rgba(0, 0, 0, 0)", "transparent")
        assert float(info["opacity"]) > 0
        assert info["width"] > 0


class TestCommitting:
    def test_a_reorder_commits_the_course_file_opens_a_pr_on_a_new_branch_and_goes_quiet(self, editor):
        editor.click('.dl-editor-card[data-slug="next-steps"] .dl-editor-up')
        editor.once("dialog", lambda d: d.accept("Put next steps first"))
        editor.click("#dl-editor-save")
        editor.wait_for_function("globalThis.__committed !== undefined")
        change = editor.evaluate("globalThis.__committed")
        assert change["message"] == "Put next steps first"
        assert change["base"] == "basesha"
        assert [f["path"] for f in change["files"]] == ["courses/fixtures.yaml"]
        written = change["files"][0]["text"]
        assert written.index("next-steps") < written.index("first-steps")
        # The rest of the file — the title, the other series — is as it was.
        assert "title: Fixtures" in written
        assert "  - title: Reflections and review\n    tutorials:\n      - looking-back\n" in written
        # The commit lands on a new branch, never on main.
        assert change["branch"].startswith("editor/")
        assert change["branch"] != "main"
        # And the save button goes quiet again afterwards.
        editor.wait_for_selector("#dl-editor-save[disabled]")
        assert "pull/999" in editor.inner_text("#dl-editor-status")

    def test_an_insertion_commits_both_the_tutorial_and_the_course_file(self, editor):
        """Two files in one commit, because either alone leaves the repository
        describing a course that does not exist."""
        editor.once("dialog", lambda d: d.accept("Halfway There"))
        editor.click(".dl-editor-series:first-of-type .dl-editor-new")
        editor.once("dialog", lambda d: d.accept("Add halfway there"))
        editor.click("#dl-editor-save")
        editor.wait_for_function("globalThis.__committed !== undefined")
        paths = sorted(f["path"] for f in editor.evaluate("globalThis.__committed.files"))
        assert paths == [
            "courses/fixtures.yaml",
            "tutorials/halfway-there/halfway-there.md",
        ]


class TestStatus:
    """A tutorial keeps its line in the course file whatever its status —
    the build reads the status and puts a draft, a beta or an archived
    tutorial off the reading order itself — so a status change is one
    field in one file."""

    def status_of(self, editor, slug: str) -> str:
        return editor.evaluate(
            """(slug) => {
                 const text = globalThis.dewlabEditor.state.files.get(
                   `tutorials/${slug}/${slug}.md`);
                 const m = /^status:\\s*(\\S+)/m.exec(text);
                 return m ? m[1] : "live";
               }""", slug)

    def order_of(self, editor) -> list:
        return editor.evaluate(
            """() => [...globalThis.dewlabEditor.state.series.values()]
                 .find((s) => s.name === "maths-and-programming").order""")

    def test_every_tutorial_shows_its_status_with_live_marked_when_nothing_says_otherwise(self, editor):
        assert editor.eval_on_selector_all(
            '.dl-editor-card[data-slug="first-steps"] .dl-editor-status-option',
            "e => e.map(b => b.textContent)") == ["draft", "beta", "live", "archived"]
        assert editor.get_attribute(
            '.dl-editor-card[data-slug="first-steps"] '
            '.dl-editor-status-option[data-status="live"]', "aria-pressed") == "true"

    def test_setting_a_status_writes_the_field_and_keeps_its_line_in_the_course_file(self, editor):
        assert "first-steps" in self.order_of(editor)
        editor.click('.dl-editor-card[data-slug="first-steps"] '
                     '.dl-editor-status-option[data-status="archived"]')
        assert self.status_of(editor, "first-steps") == "archived"
        assert "first-steps" in self.order_of(editor)
        assert editor.query_selector('.dl-editor-card[data-slug="first-steps"]')

    def test_a_tutorial_no_course_lists_is_still_shown(self, browser, base_url):
        """Otherwise a tutorial written before it is placed is invisible
        here, with no way to reach it."""
        files = dict(REPO)
        files["tutorials/unlisted/unlisted.md"] = (
            '---\ntitle: "Unlisted"\nyear: "2026-2027"\nversion: 2026.08.23.1\n---\n\n# Unlisted\n')
        context, tab = _open(browser, base_url, files)
        try:
            assert tab.query_selector('.dl-editor-off[data-slug="unlisted"]')
            heading = tab.inner_text('.dl-editor-series[data-course=""] h2')
            assert heading == "On no course yet"
        finally:
            context.close()

    def test_the_status_change_commits_the_tutorial_alone(self, editor):
        editor.click('.dl-editor-card[data-slug="first-steps"] '
                     '.dl-editor-status-option[data-status="archived"]')
        editor.once("dialog", lambda d: d.accept("Retire first steps"))
        editor.click("#dl-editor-save")
        editor.wait_for_function("globalThis.__committed !== undefined")
        paths = sorted(f["path"] for f in editor.evaluate("globalThis.__committed.files"))
        assert paths == ["tutorials/first-steps/first-steps.md"]
        written = next(f for f in editor.evaluate("globalThis.__committed.files")
                       if f["path"].endswith(".md"))["text"]
        assert "status: archived" in written

    def test_the_field_lands_above_covers_rather_than_inside_it(self, editor):
        """`covers:` has indented children, and anything written below them
        would be read as one of them."""
        written = editor.evaluate(
            """() => {
                 const meta = 'title: "T"\\nslug: t\\nversion: 2026.08.23.1\\n'
                   + 'covers:\\n  a-section:\\n    covers: [MIT-1.4]';
                 return globalThis.dewlabEditor.setFrontmatterField(meta, "status", "beta");
               }""")
        assert written.index("status: beta") < written.index("covers:")


class TestVersionArithmetic:
    """Driven directly rather than through the UI, since the interesting
    cases are about dates and a browser test cannot move the clock."""

    def call(self, editor, expression):
        return editor.evaluate(f"() => {{ const m = globalThis.__editorModule; return {expression}; }}")

    def test_a_release_is_dated_today(self, editor):
        got = self.call(editor, "m.nextVersion([], new Date(2026, 8, 15))")
        assert got == "2026.09.15.1"

    def test_the_trailing_number_is_computed_not_typed(self, editor):
        """Publish, spot something, publish again same day — rare, and
        exactly the case that would otherwise collide."""
        got = self.call(
            editor,
            'm.nextVersion(["2026.09.15.1", "2026.09.15.2"], new Date(2026, 8, 15))')
        assert got == "2026.09.15.3"

    def test_yesterdays_releases_do_not_raise_todays_number(self, editor):
        got = self.call(
            editor, 'm.nextVersion(["2026.09.14.7"], new Date(2026, 8, 15))')
        assert got == "2026.09.15.1"

    def test_releases_sort_by_date_and_not_as_text(self, editor):
        assert self.call(editor, 'm.isNewer("2026.09.15.1", "2026.09.02.1")') is True
        assert self.call(editor, 'm.isNewer("2026.09.02.1", "2026.09.15.1")') is False
        assert self.call(editor, 'm.isNewer("2026.09.15.10", "2026.09.15.9")') is True

    def test_a_cell_appearing_or_going_is_what_tells_a_release_from_an_edit(self, editor):
        moved = self.call(
            editor,
            'm.cellsChanged("```python exec\\nid: a\\n1\\n```\\n",'
            ' "```python exec\\nid: b\\n1\\n```\\n")')
        assert moved == {"added": ["b"], "removed": ["a"]}

    def test_prose_moving_is_not_a_change_of_cells(self, editor):
        moved = self.call(
            editor,
            'm.cellsChanged("Before.\\n\\n```python exec\\nid: a\\n1\\n```\\n",'
            ' "After, rewritten.\\n\\n```python exec\\nid: a\\n2\\n```\\n")')
        assert moved == {"added": [], "removed": []}


class TestOpeningATutorialWithSeveralReleases:
    def test_it_opens_the_newest_live_one_with_its_own_body_and_version_label(self, versioned):
        """It used to open an empty buffer: `pathOf` looked for a single
        `tutorials/<id>.md`, and a tutorial with a second release
        is a folder of releases instead."""
        versioned.click('.dl-editor-card[data-slug="two-takes"] .dl-editor-open')
        where = versioned.inner_text(".dl-editor-one .dl-editor-where")
        assert where == "tutorials/two-takes/v2026.09.15.1.md"
        # The body is the one students are reading.
        body = versioned.evaluate("() => globalThis.dewlabEditor.getBody()")
        assert "only-in-september" in body
        assert "only-in-june" not in body
        # It says which release and how many there are.
        assert "2026.09.15.1" in versioned.inner_text(".dl-editor-version")
        assert "2" in versioned.inner_text(".dl-editor-version")

    def test_a_tutorial_off_the_route_is_listed_once_however_many_releases(self, versioned):
        """Without a guard, walking every markdown file to build the
        off-the-route list would turn a tutorial's several release files
        into that many duplicate cards, all opening the same tutorial."""
        cards = versioned.eval_on_selector_all(
            '.dl-editor-off', "e => e.map(c => c.dataset.slug)")
        assert cards == ["old-ways"]

    def test_and_the_one_card_opens_its_newest_release(self, versioned):
        versioned.click('.dl-editor-off[data-slug="old-ways"] .dl-editor-open')
        where = versioned.inner_text(".dl-editor-one .dl-editor-where")
        assert where == "tutorials/old-ways/v2026.03.01.1.md"


class TestReleasing:
    def edit(self, tab, slug, text):
        tab.click(f'.dl-editor-card[data-slug="{slug}"] .dl-editor-open')
        tab.evaluate("(md) => globalThis.dewlabEditor.setBody(md)", text)

    def files(self, tab):
        return {f["path"]: f["text"] for f in tab.evaluate("globalThis.__committed.files")}

    def release(self, tab):
        """Waits for #dl-editor-status to change, since release() reads
        Crepe's live markdown asynchronously and its effects land a beat
        after the click returns — but status() updates on every path it can
        take, success or refusal, so that text change is a reliable signal
        regardless of which one this hits."""
        before = tab.eval_on_selector(
            "#dl-editor-status", "e => e.textContent"
        ) if tab.query_selector("#dl-editor-status") else None
        tab.click("#dl-editor-release")
        tab.wait_for_function(
            "(before) => { const e = document.getElementById('dl-editor-status'); "
            "return e && e.textContent !== before; }",
            arg=before,
        )

    def commit(self, tab, message="A release"):
        tab.once("dialog", lambda d: d.accept(message))
        tab.click("#dl-editor-save")
        tab.wait_for_function("globalThis.__committed !== undefined")

    def test_releasing_adds_a_frozen_copy_of_what_students_have_and_a_new_release_of_the_edits(self, versioned):
        """Freezing the edits instead would make the release a copy of the
        very thing it exists to let a reader go back from."""
        self.edit(versioned, "first-steps", "# First Steps\n\nRewritten.\n")
        self.release(versioned)
        self.commit(versioned)
        files = self.files(versioned)

        current = "tutorials/first-steps/first-steps.md"
        frozen = "tutorials/first-steps/v2026.06.02.1.md"
        assert files[current] is not None
        assert frozen in files
        assert len([p for p in files if p.startswith("tutorials/first-steps/")]) == 2

        # The frozen copy is what students have, not what was typed, and it
        # keeps the tutorial's own name.
        frozen_text = files[frozen]
        assert "Rewritten." not in frozen_text
        assert "adding-up-1" in frozen_text
        assert "version: 2026.06.02.1" in frozen_text

        # The new release carries the edits, a new version, and records
        # what it replaced.
        new = files[current]
        assert "Rewritten." in new
        assert re.search(r"^version: \d{4}\.\d{2}\.\d{2}\.\d+$", new, re.M)
        assert "version: 2026.06.02.1" not in new
        assert "supersedes: 2026.06.02.1" in new

    def test_releasing_a_folder_writes_only_the_new_release(self, versioned):
        """The older release files are already frozen at their own versions,
        so the commit has nothing to say about either."""
        self.edit(versioned, "two-takes", "# Two Takes\n\nA third take.\n")
        self.release(versioned)
        self.commit(versioned)
        files = self.files(versioned)
        assert "tutorials/two-takes/v2026.06.02.1.md" not in files
        assert "tutorials/two-takes/v2026.09.15.1.md" not in files
        written = [p for p in files if p.startswith("tutorials/two-takes/")]
        assert len(written) == 1
        assert "A third take." in files[written[0]]
        assert "supersedes: 2026.09.15.1" in files[written[0]]

    def test_and_the_release_it_came_from_goes_back_to_what_students_have(self, versioned):
        self.edit(versioned, "two-takes", "# Two Takes\n\nA third take.\n")
        self.release(versioned)
        held = versioned.evaluate(
            "() => globalThis.dewlabEditor.state.files"
            ".get('tutorials/two-takes/v2026.09.15.1.md')")
        assert "A third take." not in held
        assert "only-in-september" in held

    def test_the_course_file_is_not_touched_by_a_release(self, versioned):
        """A course file lists ids, not releases — a new version of a
        tutorial is not a new tutorial."""
        self.edit(versioned, "first-steps", "# First Steps\n\nRewritten.\n")
        self.release(versioned)
        self.commit(versioned)
        assert "courses/fixtures.yaml" not in self.files(versioned)

    def test_releasing_with_nothing_changed_is_refused(self, versioned):
        versioned.click('.dl-editor-card[data-slug="first-steps"] .dl-editor-open')
        self.release(versioned)
        assert "identical" in versioned.inner_text("#dl-editor-status")
        assert versioned.get_attribute("#dl-editor-save", "disabled") is not None

    def test_a_tutorial_that_is_not_live_is_not_released(self, versioned):
        """A draft has no page for anybody to go back to; a beta becomes
        live through the status control, not by being released."""
        versioned.click('.dl-editor-card[data-slug="first-steps"] '
                        '.dl-editor-status-option[data-status="beta"]')
        self.edit(versioned, "first-steps", "# First Steps\n\nRewritten.\n")
        self.release(versioned)
        assert "Only a live tutorial" in versioned.inner_text("#dl-editor-status")


class TestTheProposal:
    def set_body(self, tab, text: str) -> None:
        tab.evaluate("(md) => globalThis.dewlabEditor.setBody(md)", text)

    def test_changing_the_cells_says_this_is_probably_a_release(self, versioned):
        versioned.click('.dl-editor-card[data-slug="first-steps"] .dl-editor-open')
        self.set_body(versioned,
                       "# First Steps\n\n## Adding up\n\n"
                       "```python exec\nid: adding-up-2\nprint(1)\n```\n")
        report = versioned.inner_text("#dl-editor-report")
        assert "usually a release rather than an edit" in report

    def test_the_release_you_just_made_does_not_announce_itself(self, versioned):
        """Without a guard, a file with nothing committed yet has no last
        release to compare with, so the release just made reports every
        cell in it as new."""
        versioned.click('.dl-editor-card[data-slug="first-steps"] .dl-editor-open')
        self.set_body(versioned,
                       "# First Steps\n\n## Adding up\n\n"
                       "```python exec\nid: adding-up-2\nprint(1)\n```\n")
        versioned.click("#dl-editor-release")
        versioned.wait_for_function(
            "!document.querySelector('#dl-editor-report').textContent.includes('usually a release')"
        )

    def test_a_newly_created_tutorial_says_nothing_about_its_cells(self, editor):
        editor.once("dialog", lambda d: d.accept("Brand New"))
        editor.click(".dl-editor-series:first-of-type .dl-editor-gap:nth-of-type(1) button")
        editor.click('.dl-editor-card[data-slug="brand-new"] .dl-editor-open')
        assert "usually a release" not in editor.inner_text("#dl-editor-report")

    def test_moving_prose_stays_quiet(self, versioned):
        """A version per save is the thing the whole design rejects, so an edit
        that is only an edit gets no ceremony."""
        versioned.click('.dl-editor-card[data-slug="first-steps"] .dl-editor-open')
        self.set_body(versioned,
                       "# First Steps\n\nRewritten prose.\n\n## Adding up\n\n"
                       "```python exec\nid: adding-up-1\nprint(2)\n```\n")
        report = versioned.inner_text("#dl-editor-report")
        assert "usually a release" not in report
