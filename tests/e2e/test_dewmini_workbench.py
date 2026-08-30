"""dewmini's workbench, in a real browser — tabs, the two rails, and the
variable inspector against live Python.

This is the first e2e coverage dewmini has ever had, and the reason it
exists is written in `DECISIONS_LOG.md` 7.96 and 7.97: two rounds of
defects, in code that looked right, none of them catchable without a
browser. Everything here needs one — a tab strip that re-points a live
array, a rail that reserves page width, and an inspector that reads a
Python namespace across a worker boundary are all things that either work
in a browser or do not work at all.

Reuses conftest.py's built site (which already carries `compose/`, since
`build()` copies it wholesale) and its self-hosted Pyodide, and only adds
the one thing that fixture does for the tutorial page and not for this
one: pointing dewmini at that local Pyodide rather than the CDN.

    python3 -m pytest tests/e2e/test_dewmini_workbench.py -q
"""

from __future__ import annotations

import pytest

# The page under test, relative to the built site root.
DEWMINI = "compose/dewmini.html"


@pytest.fixture(scope="session")
def dewmini_url(site_dir, base_url) -> str:
    """dewmini's URL in the served test site, with Pyodide pointed at the
    copy staged beside it.

    conftest's own fixture does this for the tutorial page by finding its
    runtime `<script>`; dewmini boots through `compose/dewmini.js`, one
    directory down, so the base needs the extra `../` — the same relative
    depth that produced a real bug in `DECISIONS_LOG.md` 7.89, which is
    reason enough to write it out rather than assume it.
    """
    page = site_dir / DEWMINI
    assert page.exists(), "build() no longer copies compose/ into the site"
    html = page.read_text()
    if "DEWLAB_PYODIDE_BASE" not in html:
        page.write_text(html.replace(
            "<head>",
            '<head>\n<script>window.DEWLAB_PYODIDE_BASE = "../pyodide/";</script>',
            1,
        ))
    return f"{base_url}/{DEWMINI}"


@pytest.fixture
def dewmini(page, dewmini_url):
    """A fresh dewmini with no saved state.

    Storage is cleared *before* the real load, on a blank page from the
    same origin: clearing after dewmini has already read localStorage
    would leave the page showing state this test then thinks is gone.
    """
    page.goto(dewmini_url)
    page.evaluate("localStorage.clear()")
    page.goto(dewmini_url)
    # The toolbar, not #cells-container: an empty notebook's cell
    # container has zero height, which Playwright counts as hidden.
    page.wait_for_selector(".dm-toolbar")
    return page


def add_python_cell(page, code: str) -> None:
    """Adds a Python cell and types `code` into it."""
    page.click("#add-python-cell")
    editor = page.locator(".dm-cell-python .cm-content").last
    editor.click()
    page.keyboard.insert_text(code)


# --------------------------------------------------------------------- tabs


def test_a_new_notebook_opens_its_own_tab(dewmini):
    """Two notebooks, and the strip appears only once there are two."""
    assert dewmini.locator("#dm-tabs").is_hidden(), "one notebook should show no tab strip"

    dewmini.click("#new-notebook")
    assert dewmini.locator("#dm-tabs").is_visible()
    assert dewmini.locator(".dm-tab").count() == 2


def test_each_tab_keeps_its_own_cells(dewmini):
    """The point of tabs: what is in one notebook stays there.

    This is the test that would have caught the hazard `setCells()` exists
    for — a reassignment that detaches `cells` from the notebook holding
    it looks perfectly fine until you switch away and back.
    """
    add_python_cell(dewmini, "first = 1")
    assert dewmini.locator(".dm-cell").count() == 1

    dewmini.click("#new-notebook")
    assert dewmini.locator(".dm-cell").count() == 0, "a new notebook starts empty"
    add_python_cell(dewmini, "second = 2")
    add_python_cell(dewmini, "third = 3")
    assert dewmini.locator(".dm-cell").count() == 2

    # Back to the first notebook: its one cell, with its own content.
    dewmini.locator(".dm-tab-label").first.click()
    assert dewmini.locator(".dm-cell").count() == 1
    assert "first = 1" in dewmini.locator(".dm-cell-python .cm-content").first.inner_text()

    # And forward again, to prove the second survived the round trip.
    dewmini.locator(".dm-tab-label").nth(1).click()
    assert dewmini.locator(".dm-cell").count() == 2


def test_notebooks_survive_a_reload(dewmini, dewmini_url):
    """Tabs are saved, not just held in memory."""
    add_python_cell(dewmini, "kept = 1")
    dewmini.click("#new-notebook")
    add_python_cell(dewmini, "also_kept = 2")

    dewmini.reload()
    dewmini.wait_for_selector(".dm-toolbar")
    assert dewmini.locator(".dm-tab").count() == 2


def test_work_saved_before_tabs_is_migrated(page, dewmini_url):
    """A reader who left cells under the old single-notebook key finds them
    again — the one-way migration in loadSavedState().

    Written against the real legacy shape (a bare array under
    `dewmini:cells:v1`) rather than a fixture of one, since the whole risk
    here is a mismatch between what was actually stored and what the
    migration expects.
    """
    page.goto(dewmini_url)
    page.evaluate("""() => {
      localStorage.clear();
      localStorage.setItem("dewmini:cells:v1", JSON.stringify([
        {id: "cell-old", type: "python", content: "from_before = 1", output: "", error: false}
      ]));
    }""")
    page.goto(dewmini_url)
    page.wait_for_selector(".dm-cell")

    assert page.locator(".dm-cell").count() == 1
    assert "from_before = 1" in page.locator(".cm-content").first.inner_text()


# -------------------------------------------------------------------- rails


def test_both_rails_can_be_open_at_once(dewmini):
    """The whole point of two rails: a definition open beside your own work.

    dewmini's previous panel logic closed whatever else was open, which was
    right when both panels shared the right edge and is wrong now.
    """
    dewmini.click("#dm-library-toggle")
    dewmini.click("#dm-workbench-toggle")

    assert dewmini.locator("#dm-library").is_visible()
    assert dewmini.locator("#dm-workbench").is_visible()

    # And the page reserves room on both sides rather than being covered.
    assert dewmini.evaluate("document.documentElement.hasAttribute('data-dl-panel-left')")
    assert dewmini.evaluate("document.documentElement.hasAttribute('data-dl-panel-right')")


def test_settings_and_workbench_share_an_edge(dewmini):
    """Two panels on one edge still close each other — otherwise the second
    simply covers the first."""
    dewmini.click("#dm-workbench-toggle")
    assert dewmini.locator("#dm-workbench").is_visible()

    dewmini.click("#dl-settings-toggle")
    assert dewmini.locator("#dl-settings").is_visible()
    assert dewmini.locator("#dm-workbench").is_hidden()


def test_a_rail_survives_clicking_your_own_notebook(dewmini):
    """A docked rail is a pane, not a popover.

    Dismiss-on-outside-click is right for something floating over the page
    and actively wrong for something the page has made room for: every
    click on your own code would close the reference you opened to read
    while writing it.
    """
    dewmini.click("#dm-library-toggle")
    add_python_cell(dewmini, "x = 1")
    assert dewmini.locator("#dm-library").is_visible()


# ---------------------------------------------------------------- reference


def test_the_reference_searches_every_tutorials_terms(dewmini):
    """The cross-tutorial index, filtered live."""
    dewmini.click("#dm-library-toggle")
    dewmini.wait_for_function(
        "document.querySelectorAll('#dm-reference-groups dt').length > 0",
        timeout=15_000,
    )
    everything = dewmini.locator("#dm-reference-groups dt").count()
    # The fixture glossary's own entries, across several kinds. Against the
    # real repository this is 248; here it is however many the fixture
    # defines, so the assertion is about the pipeline working, not a count.
    assert everything >= 5, "the index should carry the fixture's terms"

    dewmini.fill("#dm-reference-search", "cell")
    dewmini.wait_for_function(
        f"document.querySelectorAll('#dm-reference-groups dt').length < {everything}"
    )
    assert dewmini.locator("#dm-reference-groups dt").count() > 0


def test_the_reference_filters_by_kind(dewmini):
    """Category navigation: one button per kind, and they narrow the list."""
    dewmini.click("#dm-library-toggle")
    dewmini.wait_for_function(
        "document.querySelectorAll('#dm-reference-kinds button').length > 1",
        timeout=15_000,
    )
    everything = dewmini.locator("#dm-reference-groups dt").count()

    # The first button is "All"; the second is whichever kind comes first.
    dewmini.locator("#dm-reference-kinds button").nth(1).click()
    assert dewmini.locator("#dm-reference-groups dt").count() < everything
    assert dewmini.locator("#dm-reference-groups .dm-reference-group").count() == 1


# --------------------------------------------------------------------- data


def test_a_dataset_writes_the_code_to_load_it(dewmini):
    """Picking a dataset adds a runnable cell rather than explaining how."""
    dewmini.click("#dm-library-toggle")
    dewmini.wait_for_selector(".dm-dataset")

    dewmini.locator(".dm-dataset button").first.click()
    assert dewmini.locator(".dm-cell").count() == 1
    assert "load_csv" in dewmini.locator(".cm-content").first.inner_text()


# ---------------------------------------------------------------- variables


def test_the_inspector_shows_what_a_cell_actually_made(dewmini):
    """The inspector against live Python — the part that cannot be faked.

    Runs a cell defining several types, then reads them back out of the
    Workbench: name, type, and the summary describe_globals() produced on
    the other side of the worker boundary.
    """
    dewmini.click("#dm-workbench-toggle")
    add_python_cell(dewmini, "answer = 42\nnames = ['ada', 'alan']\ngreeting = 'hello'")

    dewmini.locator(".dm-cell .dm-icon-run").first.click()
    dewmini.wait_for_function(
        "document.querySelectorAll('#dm-variables .dm-variable').length >= 3",
        timeout=90_000,
    )

    shown = dewmini.locator("#dm-variables").inner_text()
    assert "answer" in shown and "42" in shown
    assert "names" in shown and "2 items" in shown
    assert "greeting" in shown and "str" in shown


def test_the_inspector_folds_away_functions_and_modules(dewmini):
    """A student's own data first; the furniture tucked under a summary.

    The seeded names (show, check, load_csv…) are in the namespace from
    boot, and would otherwise bury the two variables a reader came to see.
    """
    dewmini.click("#dm-workbench-toggle")
    add_python_cell(dewmini, "mine = 1")

    dewmini.locator(".dm-cell .dm-icon-run").first.click()
    dewmini.wait_for_selector("#dm-variables .dm-variables-other", timeout=90_000)

    folded = dewmini.locator("#dm-variables .dm-variables-other")
    assert not folded.locator("summary").inner_text().startswith("0")
    # The reader's own variable is not inside the folded section.
    assert "mine" not in folded.inner_text()
