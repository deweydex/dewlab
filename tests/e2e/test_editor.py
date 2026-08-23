"""The editor page, driven against a fake GitHub.

Every test here injects its own client, so nothing touches the network and no
token is needed. That is the reason `start()` takes a client rather than making
one: a page that could only be tested with real credentials would not be
tested.

    python3 -m pytest tests/e2e/test_editor.py -q
"""

from __future__ import annotations

import json
import re

import pytest

# One small repository, shaped like the real one: two tutorials in a series,
# an order file, and a second series with one tutorial in it.
REPO = {
    "tutorials/fixtures/maths.order.yaml":
        "series: Maths and programming\norder:\n  - first-steps\n  - next-steps\n",
    "tutorials/fixtures/first-steps.md":
        '---\ntitle: "First Steps"\nslug: first-steps\nmodule: fixtures\n'
        'module_title: "Fixtures"\nyear: "2026-2027"\nseries: maths\nversion: 2026.08.23.1\n---\n\n'
        "# First Steps\n\nProse.\n\n## Adding up\n\n```python exec\nid: adding-up-1\n"
        "print(1 + 1)\n```\n",
    "tutorials/fixtures/next-steps.md":
        '---\ntitle: "Next Steps"\nslug: next-steps\nmodule: fixtures\n'
        'module_title: "Fixtures"\nyear: "2026-2027"\nseries: maths\nversion: 2026.08.23.1\n---\n\n'
        "# Next Steps\n\nMore prose.\n",
    "tutorials/fixtures/looking-back.order.yaml":
        "series: Reflections and review\norder:\n  - looking-back\n",
    "tutorials/fixtures/looking-back.md":
        '---\ntitle: "Looking Back"\nslug: looking-back\nmodule: fixtures\n'
        'module_title: "Fixtures"\nyear: "2026-2027"\nseries: looking-back\nversion: 2026.08.23.1\n---\n\n'
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
        f'---\ntitle: "Two Takes"\nslug: {slug}\nmodule: fixtures\n'
        f'module_title: "Fixtures"\nyear: "2026-2027"\nseries: maths\n'
        f"version: {version}\nstatus: {status}\n---\n\n# Two Takes\n\nProse.\n\n"
        "## A section\n\n" + cells
    )


def _cell(cell_id: str) -> str:
    return f"```python exec\nid: {cell_id}\nprint(1)\n```\n\n"


# The same repository with one tutorial already in a folder of releases, which
# is what a tutorial becomes the first time anything is released. The editor
# knew nothing about this shape until step 4 and opened such a tutorial as an
# empty buffer.
VERSIONED = {
    "tutorials/fixtures/maths.order.yaml":
        "series: Maths and programming\norder:\n  - first-steps\n  - two-takes\n",
    "tutorials/fixtures/first-steps.md":
        '---\ntitle: "First Steps"\nslug: first-steps\nmodule: fixtures\n'
        'module_title: "Fixtures"\nyear: "2026-2027"\nseries: maths\n'
        "version: 2026.06.02.1\nstatus: live\n---\n\n# First Steps\n\nProse.\n\n"
        "## Adding up\n\n" + _cell("adding-up-1"),
    "tutorials/fixtures/two-takes/v2026.06.02.1.md":
        _released("two-takes", "2026.06.02.1", _cell("shared-one") + _cell("only-in-june")),
    "tutorials/fixtures/two-takes/v2026.09.15.1.md":
        _released("two-takes", "2026.09.15.1",
                  _cell("shared-one") + _cell("only-in-september")),
    # Retired, with two releases, and so on none of the order files. This is
    # the only shape in which the same tutorial could be listed twice: the
    # off-the-route list is built by walking every markdown file, and a folder
    # of releases is several files describing one tutorial.
    "tutorials/fixtures/old-ways/v2026.01.01.1.md":
        _released("old-ways", "2026.01.01.1", _cell("old-one"), status="archived"),
    "tutorials/fixtures/old-ways/v2026.03.01.1.md":
        _released("old-ways", "2026.03.01.1", _cell("old-two"), status="archived"),
}


def _open(browser, base_url, files):
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
        {"files": files, "factory": FAKE_CLIENT, "url": "./" + _runtime_url(tab)},
    )
    tab.wait_for_selector(".dl-editor-card")
    return context, tab


@pytest.fixture
def editor(browser, base_url):
    """The editor page with a fake GitHub behind it, already loaded."""
    context, tab = _open(browser, base_url, REPO)
    yield tab
    context.close()


@pytest.fixture
def versioned(browser, base_url):
    """The editor over a repository where one tutorial has two releases."""
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

    def test_renaming_a_cell_id_warns_that_student_work_is_orphaned(self, editor):
        """The one thing the editor knows that the build cannot: by the time
        the build runs, the rename has already happened."""
        self.open_first(editor)
        editor.fill(".dl-editor-body",
                    editor.input_value(".dl-editor-body").replace("adding-up-1", "adding-up-2"))
        warning = editor.inner_text(".dl-editor-report")
        assert "orphaned" in warning
        assert "adding-up-1" in warning

    def test_and_says_that_releasing_is_the_way_not_to(self, editor):
        """It used to say the work was thrown away full stop, which stopped
        being true the day releases arrived — and made this box argue with the
        proposal underneath it."""
        self.open_first(editor)
        editor.fill(".dl-editor-body",
                    editor.input_value(".dl-editor-body").replace("adding-up-1", "adding-up-2"))
        warning = editor.inner_text(".dl-editor-report")
        assert "Released instead, nothing is orphaned" in warning

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


class TestStatus:
    """Draft, beta, live, archived — set from the editor rather than by hand.

    The field on its own would be trivial. What makes it worth automating is
    that only a live tutorial is on the reading order, and the build refuses an
    order file listing anything else — so the line has to move with the field
    or the next build stops."""

    def status_of(self, editor, slug: str) -> str:
        return editor.evaluate(
            """(slug) => {
                 const text = globalThis.dewlabEditor.state.files.get(
                   `tutorials/fixtures/${slug}.md`);
                 const m = /^status:\\s*(\\S+)/m.exec(text);
                 return m ? m[1] : "live";
               }""", slug)

    def order_of(self, editor) -> list:
        return editor.evaluate(
            """() => [...globalThis.dewlabEditor.state.series.values()]
                 .find((s) => s.name === "maths").order""")

    def test_every_tutorial_shows_its_status(self, editor):
        assert editor.eval_on_selector_all(
            '.dl-editor-card[data-slug="first-steps"] .dl-editor-status-option',
            "e => e.map(b => b.textContent)") == ["draft", "beta", "live", "archived"]

    def test_live_is_the_one_marked_when_nothing_says_otherwise(self, editor):
        assert editor.get_attribute(
            '.dl-editor-card[data-slug="first-steps"] '
            '.dl-editor-status-option[data-status="live"]', "aria-pressed") == "true"

    def test_setting_a_status_writes_the_field(self, editor):
        editor.click('.dl-editor-card[data-slug="first-steps"] '
                     '.dl-editor-status-option[data-status="beta"]')
        assert self.status_of(editor, "first-steps") == "beta"

    def test_leaving_live_takes_it_out_of_the_reading_order(self, editor):
        assert "first-steps" in self.order_of(editor)
        editor.click('.dl-editor-card[data-slug="first-steps"] '
                     '.dl-editor-status-option[data-status="archived"]')
        assert "first-steps" not in self.order_of(editor)

    def test_returning_to_live_puts_it_back(self, editor):
        editor.click('.dl-editor-card[data-slug="first-steps"] '
                     '.dl-editor-status-option[data-status="draft"]')
        assert "first-steps" not in self.order_of(editor)
        editor.click('.dl-editor-off[data-slug="first-steps"] '
                     '.dl-editor-status-option[data-status="live"]')
        assert "first-steps" in self.order_of(editor)

    def test_a_tutorial_off_the_route_is_still_listed(self, editor):
        """Otherwise setting something to draft is a one-way trip: it drops out
        of the order file and out of the list at once, with no way back to it."""
        editor.click('.dl-editor-card[data-slug="first-steps"] '
                     '.dl-editor-status-option[data-status="draft"]')
        assert editor.query_selector('.dl-editor-off[data-slug="first-steps"]')
        titles = editor.eval_on_selector_all(
            ".dl-editor-open", "e => e.map(b => b.textContent)")
        assert "First Steps" in titles

    def test_the_status_change_commits_both_files_together(self, editor):
        """Either file alone leaves the repository contradicting itself, and
        the build stops on exactly that."""
        editor.click('.dl-editor-card[data-slug="first-steps"] '
                     '.dl-editor-status-option[data-status="archived"]')
        editor.once("dialog", lambda d: d.accept("Retire first steps"))
        editor.click("#dl-editor-save")
        editor.wait_for_function("globalThis.__committed !== undefined")
        paths = sorted(f["path"] for f in editor.evaluate("globalThis.__committed.files"))
        assert paths == [
            "tutorials/fixtures/first-steps.md",
            "tutorials/fixtures/maths.order.yaml",
        ]
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
    """Pure functions, driven directly, because the interesting cases are about
    dates and a browser test cannot move the clock without lying about it."""

    def call(self, editor, expression):
        return editor.evaluate(f"() => {{ const m = globalThis.__editorModule; return {expression}; }}")

    def test_a_release_is_dated_today(self, editor):
        got = self.call(editor, "m.nextVersion([], new Date(2026, 8, 15))")
        assert got == "2026.09.15.1"

    def test_the_trailing_number_is_computed_not_typed(self, editor):
        """Publish, spot something, publish again. Rare, and exactly the case
        that would otherwise collide."""
        got = self.call(
            editor,
            'm.nextVersion(["2026.09.15.1", "2026.09.15.2"], new Date(2026, 8, 15))')
        assert got == "2026.09.15.3"

    def test_yesterdays_releases_do_not_raise_todays_number(self, editor):
        got = self.call(
            editor, 'm.nextVersion(["2026.09.14.7"], new Date(2026, 8, 15))')
        assert got == "2026.09.15.1"

    def test_releases_sort_by_date_and_not_as_text(self, editor):
        """2026.09.02.1 comes before 2026.09.15.1. As strings it comes after."""
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
    def test_it_opens_the_newest_live_one(self, versioned):
        """It used to open an empty buffer. `pathOf` looked for
        `tutorials/<module>/<slug>.md` and a tutorial with a second release does
        not have one — it is a folder of releases."""
        versioned.click('.dl-editor-card[data-slug="two-takes"] .dl-editor-open')
        where = versioned.inner_text(".dl-editor-one .dl-editor-where")
        assert where == "tutorials/fixtures/two-takes/v2026.09.15.1.md"

    def test_the_body_is_the_one_students_are_reading(self, versioned):
        versioned.click('.dl-editor-card[data-slug="two-takes"] .dl-editor-open')
        body = versioned.input_value(".dl-editor-body")
        assert "only-in-september" in body
        assert "only-in-june" not in body

    def test_it_says_which_release_and_how_many_there_are(self, versioned):
        versioned.click('.dl-editor-card[data-slug="two-takes"] .dl-editor-open')
        assert "2026.09.15.1" in versioned.inner_text(".dl-editor-version")
        assert "2" in versioned.inner_text(".dl-editor-version")

    def test_a_tutorial_off_the_route_is_listed_once_however_many_releases(self, versioned):
        """The off-the-route list is built by walking every markdown file, and
        a folder of releases is several files describing one tutorial. Without
        the guard, a retired tutorial with three releases is three cards, each
        of which opens the same thing."""
        cards = versioned.eval_on_selector_all(
            '.dl-editor-off', "e => e.map(c => c.dataset.slug)")
        assert cards == ["old-ways"]

    def test_and_the_one_card_opens_its_newest_release(self, versioned):
        versioned.click('.dl-editor-off[data-slug="old-ways"] .dl-editor-open')
        where = versioned.inner_text(".dl-editor-one .dl-editor-where")
        assert where == "tutorials/fixtures/old-ways/v2026.03.01.1.md"


class TestReleasing:
    def edit(self, tab, slug, text):
        tab.click(f'.dl-editor-card[data-slug="{slug}"] .dl-editor-open')
        tab.fill(".dl-editor-body", text)

    def files(self, tab):
        return {f["path"]: f["text"] for f in tab.evaluate("globalThis.__committed.files")}

    def commit(self, tab, message="A release"):
        tab.once("dialog", lambda d: d.accept(message))
        tab.click("#dl-editor-save")
        tab.wait_for_function("globalThis.__committed !== undefined")

    def test_a_single_file_tutorial_becomes_a_folder_of_releases(self, versioned):
        """A tutorial becomes a folder the moment it has a second release, and
        not before. Most never do."""
        self.edit(versioned, "first-steps", "# First Steps\n\nRewritten.\n")
        versioned.click("#dl-editor-release")
        self.commit(versioned)
        files = self.files(versioned)

        assert files["tutorials/fixtures/first-steps.md"] is None
        frozen = "tutorials/fixtures/first-steps/v2026.06.02.1.md"
        assert frozen in files
        assert len([p for p in files if p.startswith("tutorials/fixtures/first-steps/")]) == 2

    def test_the_frozen_copy_is_what_students_have_not_what_was_typed(self, versioned):
        """The whole point. Freezing the edits would make the release a copy of
        the thing it exists to let a reader go back from."""
        self.edit(versioned, "first-steps", "# First Steps\n\nRewritten.\n")
        versioned.click("#dl-editor-release")
        self.commit(versioned)
        frozen = self.files(versioned)["tutorials/fixtures/first-steps/v2026.06.02.1.md"]
        assert "Rewritten." not in frozen
        assert "adding-up-1" in frozen
        assert "version: 2026.06.02.1" in frozen

    def test_the_new_release_carries_the_edits_and_a_new_version(self, versioned):
        self.edit(versioned, "first-steps", "# First Steps\n\nRewritten.\n")
        versioned.click("#dl-editor-release")
        self.commit(versioned)
        files = self.files(versioned)
        new = next(text for path, text in files.items()
                   if path.startswith("tutorials/fixtures/first-steps/")
                   and "v2026.06.02.1" not in path)
        assert "Rewritten." in new
        assert re.search(r"^version: \d{4}\.\d{2}\.\d{2}\.\d+$", new, re.M)
        assert "version: 2026.06.02.1" not in new

    def test_the_new_release_records_what_it_replaced(self, versioned):
        """After two releases nothing else says which one this replaced."""
        self.edit(versioned, "first-steps", "# First Steps\n\nRewritten.\n")
        versioned.click("#dl-editor-release")
        self.commit(versioned)
        new = next(text for path, text in self.files(versioned).items()
                   if path.startswith("tutorials/fixtures/first-steps/")
                   and "v2026.06.02.1" not in path)
        assert "supersedes: 2026.06.02.1" in new

    def test_releasing_a_folder_writes_only_the_new_release(self, versioned):
        """Both older files are already frozen at their own versions, so the
        commit has nothing to say about either. The edits went to the new one
        and the buffer they came from went back to what students have."""
        self.edit(versioned, "two-takes", "# Two Takes\n\nA third take.\n")
        versioned.click("#dl-editor-release")
        self.commit(versioned)
        files = self.files(versioned)
        assert "tutorials/fixtures/two-takes/v2026.06.02.1.md" not in files
        assert "tutorials/fixtures/two-takes/v2026.09.15.1.md" not in files
        written = [p for p in files if p.startswith("tutorials/fixtures/two-takes/")]
        assert len(written) == 1
        assert "A third take." in files[written[0]]
        assert "supersedes: 2026.09.15.1" in files[written[0]]

    def test_and_the_release_it_came_from_goes_back_to_what_students_have(self, versioned):
        self.edit(versioned, "two-takes", "# Two Takes\n\nA third take.\n")
        versioned.click("#dl-editor-release")
        held = versioned.evaluate(
            "() => globalThis.dewlabEditor.state.files"
            ".get('tutorials/fixtures/two-takes/v2026.09.15.1.md')")
        assert "A third take." not in held
        assert "only-in-september" in held

    def test_the_order_file_is_not_touched_by_a_release(self, versioned):
        """An order file lists slugs, not releases. A new version of a tutorial
        is not a new tutorial."""
        self.edit(versioned, "first-steps", "# First Steps\n\nRewritten.\n")
        versioned.click("#dl-editor-release")
        self.commit(versioned)
        assert "tutorials/fixtures/maths.order.yaml" not in self.files(versioned)

    def test_releasing_with_nothing_changed_is_refused(self, versioned):
        versioned.click('.dl-editor-card[data-slug="first-steps"] .dl-editor-open')
        versioned.click("#dl-editor-release")
        assert "identical" in versioned.inner_text("#dl-editor-status")
        assert versioned.get_attribute("#dl-editor-save", "disabled") is not None

    def test_a_tutorial_that_is_not_live_is_not_released(self, versioned):
        """A draft has no page for anybody to go back to, and a beta becomes
        live with the status control rather than by being released."""
        versioned.click('.dl-editor-card[data-slug="first-steps"] '
                        '.dl-editor-status-option[data-status="beta"]')
        self.edit(versioned, "first-steps", "# First Steps\n\nRewritten.\n")
        versioned.click("#dl-editor-release")
        assert "Only a live tutorial" in versioned.inner_text("#dl-editor-status")


class TestTheProposal:
    def test_changing_the_cells_says_this_is_probably_a_release(self, versioned):
        versioned.click('.dl-editor-card[data-slug="first-steps"] .dl-editor-open')
        versioned.fill(".dl-editor-body",
                       "# First Steps\n\n## Adding up\n\n"
                       "```python exec\nid: adding-up-2\nprint(1)\n```\n")
        report = versioned.inner_text("#dl-editor-report")
        assert "usually a release rather than an edit" in report

    def test_the_release_you_just_made_does_not_announce_itself(self, versioned):
        """A file with nothing committed behind it has no last release to
        compare with. Without the guard, the release made a second ago reports
        that every cell in it is new."""
        versioned.click('.dl-editor-card[data-slug="first-steps"] .dl-editor-open')
        versioned.fill(".dl-editor-body",
                       "# First Steps\n\n## Adding up\n\n"
                       "```python exec\nid: adding-up-2\nprint(1)\n```\n")
        versioned.click("#dl-editor-release")
        versioned.wait_for_selector("#dl-editor-report")
        assert "usually a release" not in versioned.inner_text("#dl-editor-report")

    def test_a_newly_created_tutorial_says_nothing_about_its_cells(self, editor):
        editor.once("dialog", lambda d: d.accept("Brand New"))
        editor.click(".dl-editor-series:first-of-type .dl-editor-gap:nth-of-type(1) button")
        editor.click('.dl-editor-card[data-slug="brand-new"] .dl-editor-open')
        assert "usually a release" not in editor.inner_text("#dl-editor-report")

    def test_moving_prose_stays_quiet(self, versioned):
        """A version per save is the thing the whole design rejects, so an edit
        that is only an edit gets no ceremony."""
        versioned.click('.dl-editor-card[data-slug="first-steps"] .dl-editor-open')
        versioned.fill(".dl-editor-body",
                       "# First Steps\n\nRewritten prose.\n\n## Adding up\n\n"
                       "```python exec\nid: adding-up-1\nprint(2)\n```\n")
        report = versioned.inner_text("#dl-editor-report")
        assert "usually a release" not in report
