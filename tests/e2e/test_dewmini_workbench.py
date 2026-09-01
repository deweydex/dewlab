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
    # Match the *assignment*, not the name. This guard used to look for the
    # bare name anywhere in the document, and a comment added upstream
    # explaining what the override does contained it — so the injection
    # silently stopped happening and every test that runs Python failed
    # against a CDN this sandbox blocks. A guard that prose can satisfy is
    # not a guard.
    INJECTED = 'window.DEWLAB_PYODIDE_BASE ='
    if INJECTED not in html:
        html = html.replace(
            "<head>",
            f'<head>\n<script>{INJECTED} "../pyodide/";</script>',
            1,
        )
        page.write_text(html)
    assert INJECTED in page.read_text(), "dewmini would boot from the CDN"
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
    """Adds a Python cell and types `code` into it.

    Through the last insert seam, which is how a reader adds one: the
    toolbar's own Python/Text buttons were removed as duplicates of it.
    """
    page.locator(".dm-insert-btn", has_text="Python").last.click()
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


def test_both_rails_drag_wider_and_the_notebook_gives_up_the_room(dewmini):
    """Split screen, which is the point of two rails you can size.

    Both edges carry the same full-height strip. The left rail relied on
    native `resize: horizontal` until 7.103 — which works, but is a small
    corner grip facing a full-height strip, and hanging either strip outside
    the panel loses half its width to the panel's own overflow clipping.
    So this drags both and checks the notebook actually moves.
    """
    dewmini.click("#dm-library-toggle")
    dewmini.click("#dm-workbench-toggle")

    def drag(handle, dx):
        box = dewmini.locator(handle).bounding_box()
        y = box["y"] + box["height"] / 2
        dewmini.mouse.move(box["x"] + box["width"] / 2, y)
        dewmini.mouse.down()
        dewmini.mouse.move(box["x"] + box["width"] / 2 + dx, y, steps=8)
        dewmini.mouse.up()

    before = dewmini.locator("#dm-library").bounding_box()["width"]
    drag("#dm-library .dl-panel-resize-handle", 140)
    after = dewmini.locator("#dm-library").bounding_box()["width"]
    assert after > before + 100, "the left rail should grow when dragged right"

    right_before = dewmini.locator("#dm-workbench").bounding_box()["width"]
    drag("#dm-workbench .dl-panel-resize-handle", -140)
    right_after = dewmini.locator("#dm-workbench").bounding_box()["width"]
    assert right_after > right_before + 100, "the right rail grows when dragged left"

    # The notebook sits between them rather than under either.
    left = dewmini.locator("#dm-library").bounding_box()
    right = dewmini.locator("#dm-workbench").bounding_box()
    main = dewmini.locator("main").bounding_box()
    assert main["x"] >= left["x"] + left["width"], "the left rail must not cover the notebook"
    assert main["x"] + main["width"] <= right["x"] + 1, "the right rail must not cover it"


def test_a_rails_width_survives_a_reload(dewmini, dewmini_url):
    """A rail dragged to half the screen and back to its default on every
    reload is not a working split screen."""
    dewmini.click("#dm-library-toggle")
    box = dewmini.locator("#dm-library .dl-panel-resize-handle").bounding_box()
    y = box["y"] + box["height"] / 2
    dewmini.mouse.move(box["x"] + box["width"] / 2, y)
    dewmini.mouse.down()
    dewmini.mouse.move(box["x"] + box["width"] / 2 + 150, y, steps=8)
    dewmini.mouse.up()
    widened = dewmini.locator("#dm-library").bounding_box()["width"]

    dewmini.reload()
    dewmini.wait_for_selector(".dm-toolbar")
    dewmini.wait_for_selector("#dm-library", state="visible")
    assert abs(dewmini.locator("#dm-library").bounding_box()["width"] - widened) < 2


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

    # Every button is a kind now — there is no "All", because no chip pressed
    # already means all of them, the same as every other filter row.
    dewmini.locator("#dm-reference-kinds button").nth(1).click()
    assert dewmini.locator("#dm-reference-groups dt").count() < everything
    assert dewmini.locator("#dm-reference-groups .dm-reference-group").count() == 1


def test_the_reference_offers_subject_and_level_up_front(dewmini):
    """Two facets on the surface, both derived at build time — subject from
    the outcome codes a tutorial claims, level from the prerequisite depth of
    the topic tree. The fixture claims one outcome from each module, so both
    subjects are present."""
    dewmini.click("#dm-library-toggle")
    dewmini.wait_for_function(
        "document.querySelectorAll('#dm-reference-subjects button').length > 0",
        timeout=15_000,
    )
    subjects = dewmini.locator("#dm-reference-subjects button").all_inner_texts()
    assert any("Maths" in chip for chip in subjects)
    assert any("Computing" in chip for chip in subjects)

    # Every chip carries its own count, so a filter that would empty the list
    # says so before it is pressed.
    assert all(any(ch.isdigit() for ch in chip) for chip in subjects)
    assert dewmini.locator("#dm-reference-levels button").count() > 0


def test_a_subject_narrows_the_list_to_its_own_count(dewmini):
    """The count on the chip is the promise; this is the check that the list
    keeps it."""
    dewmini.click("#dm-library-toggle")
    dewmini.wait_for_function(
        "document.querySelectorAll('#dm-reference-subjects button').length > 0",
        timeout=15_000,
    )
    chip = dewmini.locator("#dm-reference-subjects button").first
    promised = int("".join(ch for ch in chip.inner_text() if ch.isdigit()))
    chip.click()
    assert dewmini.locator("#dm-reference-groups dt").count() == promised


def test_the_topics_row_opens_in_flow_rather_than_over_the_results(dewmini):
    """Josh's ask, and the reason this is a `<details>` in the normal flow and
    not a popover: opening it must push the results down, never sit on top of
    them. Measured, because "looks fine" is exactly how an overlay ships."""
    dewmini.click("#dm-library-toggle")
    dewmini.wait_for_selector("#dm-reference-topics-wrap")

    wrap = dewmini.locator("#dm-reference-topics-wrap")
    assert wrap.evaluate("el => !el.open"), "it should start closed"

    before = dewmini.locator("#dm-reference-groups").bounding_box()["y"]
    wrap.locator("summary").click()
    dewmini.wait_for_function(
        "document.getElementById('dm-reference-topics-wrap').open"
    )

    row = dewmini.locator("#dm-reference-topics").bounding_box()
    after = dewmini.locator("#dm-reference-groups").bounding_box()["y"]
    assert after > before, "opening it should push the results down"
    assert row["y"] + row["height"] <= after + 1, "the row must not overlap them"


def test_the_topics_summary_says_how_many_are_on(dewmini):
    """Folded-away filters that are silently active are a trap. The summary
    reports its own state, so a list narrowed by something out of sight still
    explains itself."""
    dewmini.click("#dm-library-toggle")
    dewmini.wait_for_function(
        "document.querySelectorAll('#dm-reference-kinds button').length > 1",
        timeout=15_000,
    )
    summary = dewmini.locator("#dm-reference-topics-summary")
    assert summary.inner_text().strip() == "Topics"

    dewmini.locator("#dm-reference-topics-wrap summary").click()
    topics = dewmini.locator("#dm-reference-topics button")
    if topics.count() == 0:
        pytest.skip("the fixture's tutorials belong to no curated topic group")
    topics.first.click()
    assert "1" in summary.inner_text()


def test_no_rail_text_shrinks_below_twelve_pixels(dewmini):
    """The Texture slider scales the whole rail, which is the point — but at
    its floor the filter chips were rendering at 10.2px. Every small label
    now carries a `max(…, 12px)` floor, and this is what holds it."""
    dewmini.click("#dm-library-toggle")
    dewmini.wait_for_function(
        "document.querySelectorAll('#dm-reference-subjects button').length > 0",
        timeout=15_000,
    )
    # Drive the root size to the slider's own minimum.
    dewmini.evaluate(
        "() => document.documentElement.style.setProperty('--dl-font-size', '16px')"
    )
    smallest = dewmini.evaluate(
        """() => {
            const rail = document.querySelector('.dm-library');
            let min = Infinity;
            for (const el of rail.querySelectorAll('*')) {
                if (!el.textContent.trim()) continue;
                const size = parseFloat(getComputedStyle(el).fontSize);
                if (size < min) min = size;
            }
            return min;
        }"""
    )
    assert smallest >= 12, f"something in the rail renders at {smallest}px"


def test_a_blank_cell_is_reachable_from_an_empty_notebook(dewmini):
    """The seam is drawn even with nothing to sit between.

    It used to be suppressed while the toolbar carried its own Python/Text
    buttons. Removing those as duplicates would have left no way at all to
    start a *blank* cell — only "Start with imports", which arrives with
    three lines already in it. This is the test that says so.
    """
    assert dewmini.locator(".dm-cell").count() == 0
    assert dewmini.locator(".dm-insert").count() == 1, "one seam, over an empty notebook"

    dewmini.locator(".dm-insert-btn", has_text="Python").click()
    assert dewmini.locator(".dm-cell").count() == 1
    assert dewmini.locator(".dm-cell-python .cm-content").inner_text().strip() == ""


def test_the_toolbar_offers_openings_not_a_second_way_to_add_a_cell(dewmini):
    """Josh's ask: the toolbar's Python and Text buttons duplicated the
    seams below, so they went, and the space went to the two openings that
    previously only existed on an empty notebook."""
    toolbar = dewmini.locator(".dm-toolbar")
    assert toolbar.locator("#dm-show-example").is_visible()
    assert toolbar.locator("#dm-add-imports").is_visible()
    assert toolbar.locator("#add-practice").is_visible()
    assert toolbar.locator("#add-python-cell").count() == 0
    assert toolbar.locator("#add-text-cell").count() == 0

    # And they still do what they say, with cells already present — which is
    # the state their old home (the empty-notebook block) could never reach.
    dewmini.locator(".dm-insert-btn", has_text="Python").click()
    dewmini.click("#dm-add-imports")
    assert dewmini.locator(".dm-cell").count() == 2
    assert "import pandas" in dewmini.locator(".dm-cell-python .cm-content").last.inner_text()


# --------------------------------------------------------------------- data


def test_a_dataset_writes_the_code_to_load_it(dewmini):
    """Picking a dataset adds a runnable cell rather than explaining how."""
    dewmini.click("#dm-library-toggle")
    dewmini.wait_for_selector(".dm-dataset")

    dewmini.locator(".dm-dataset button").first.click()
    assert dewmini.locator(".dm-cell").count() == 1
    assert "load_csv" in dewmini.locator(".cm-content").first.inner_text()


# ----------------------------------------------------------------- running


def test_editing_a_run_cell_shows_the_stale_flag_on_the_run_line(dewmini):
    """DECISIONS_LOG.md 7.105 / planning/CELL_IDENTITY.md §3 — the run-
    line's "edited since" flag appears the moment a run cell's code
    changes, and disappears the moment it runs again."""
    add_python_cell(dewmini, "6 * 7")  # a bare expression, so it actually prints something
    dewmini.locator(".dm-cell .dm-icon-run").first.click()
    dewmini.wait_for_selector(".dm-cell-output:not(.dm-empty)", timeout=90_000)
    assert "edited since" not in dewmini.locator(".dm-cell-runline").first.inner_text(), \
        "nothing to be stale about yet"

    editor = dewmini.locator(".dm-cell-python .cm-content").first
    editor.click()
    dewmini.keyboard.press("End")
    dewmini.keyboard.insert_text(" + 1")
    assert "edited since" in dewmini.locator(".dm-cell-runline").first.inner_text()

    dewmini.locator(".dm-cell .dm-icon-run").first.click()
    dewmini.wait_for_function(
        "!document.querySelector('.dm-cell-runline').textContent.includes('edited since')"
    )


def test_run_above_resets_the_namespace_first(dewmini):
    """DECISIONS_LOG.md 7.106 — 'Run above' starts from a clean interpreter,
    so running it twice from the same edited cells gives the same answer
    both times rather than an answer that keeps growing."""
    add_python_cell(dewmini, "counter = 1")
    add_python_cell(dewmini, "counter = counter + 1\ncounter")

    def run_above_on_second_cell():
        cell = dewmini.locator(".dm-cell").nth(1)
        cell.locator(".dm-icon-more").click()
        cell.locator('.dm-cell-run-menu-item[data-run-menu="above"]').click()
        dewmini.wait_for_function(
            "document.querySelectorAll('.dm-cell')[1]"
            ".querySelector('.dm-cell-output').innerText.trim().length > 0",
            timeout=90_000,
        )

    run_above_on_second_cell()
    first_output = dewmini.locator(".dm-cell-output").nth(1).inner_text().strip()
    assert first_output == "2"

    run_above_on_second_cell()
    second_output = dewmini.locator(".dm-cell-output").nth(1).inner_text().strip()
    assert second_output == "2", "a second 'Run above' should reset, not accumulate"


def test_run_below_keeps_what_came_before_it(dewmini):
    """DECISIONS_LOG.md 7.106 — 'Run below' must not reset the namespace:
    its whole point is keeping what an earlier cell already defined."""
    add_python_cell(dewmini, "shared = 100\nshared")
    add_python_cell(dewmini, "shared = shared + 1\nshared")

    # Only the first cell runs on its own — the second cell's own "shared"
    # exists solely because "Run below" is about to reuse what this left
    # behind, not because it ran as part of the same batch.
    dewmini.locator(".dm-cell .dm-icon-run").first.click()
    dewmini.wait_for_selector(".dm-cell-output:not(.dm-empty)", timeout=90_000)

    second_cell = dewmini.locator(".dm-cell").nth(1)
    second_cell.locator(".dm-icon-more").click()
    second_cell.locator('.dm-cell-run-menu-item[data-run-menu="below"]').click()
    dewmini.wait_for_function(
        "document.querySelectorAll('.dm-cell')[1]"
        ".querySelector('.dm-cell-output').innerText.trim().length > 0",
        timeout=90_000,
    )

    assert "101" in dewmini.locator(".dm-cell-output").nth(1).inner_text()
    assert "dm-error" not in (second_cell.get_attribute("class") or "")


def test_restart_and_run_all_reruns_from_a_clean_start(dewmini):
    """DECISIONS_LOG.md 7.108 — one button, both halves: a real restart,
    then every cell run again from the top."""
    add_python_cell(dewmini, "value = 6 * 7\nvalue")
    dewmini.once("dialog", lambda dialog: dialog.accept())
    dewmini.click("#dl-settings-toggle")
    dewmini.click("#settings-restart-run-all")
    dewmini.wait_for_function(
        "document.querySelector('.dm-cell-output')?.innerText.includes('42')",
        timeout=90_000,
    )


# -------------------------------------------------------------------- maths


def test_a_text_cell_renders_maths(dewmini):
    """DECISIONS_LOG.md 7.107 — $…$ in a text cell renders through the
    same lazily-loaded KaTeX bundle a tutorial page uses."""
    dewmini.locator(".dm-insert-btn", has_text="Text").last.click()
    textarea = dewmini.locator(".dm-textarea").last
    textarea.click()
    dewmini.keyboard.insert_text("Solve $x^2 + 1 = 0$ for x.")
    textarea.evaluate("el => el.blur()")  # triggers showRendered(), same as clicking away

    dewmini.wait_for_selector(".dl-math .katex", timeout=15_000)
    assert dewmini.locator(".dl-math .katex").count() >= 1


def test_maths_survives_a_dollar_sign_that_is_not_maths(dewmini):
    """The same guard build.py's own INLINE_MATH_RE carries: a bare "$5" in
    ordinary prose is money, not a broken formula, and should render as
    plain text rather than as a stray, unrendered "$"."""
    dewmini.locator(".dm-insert-btn", has_text="Text").last.click()
    textarea = dewmini.locator(".dm-textarea").last
    textarea.click()
    dewmini.keyboard.insert_text("It cost $5 or $6, either way.")
    textarea.evaluate("el => el.blur()")

    rendered = dewmini.locator(".dm-doc-render").last
    assert "$5 or $6" in rendered.inner_text()
    assert rendered.locator(".dl-math").count() == 0


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


# ------------------------------------------------- the .py round trip


def add_text_cell(page, prose: str) -> None:
    """Adds a text cell, types `prose` into it, and lets it settle.

    The blur matters. A text cell's textarea hides on blur and its
    rendered markdown takes its place, which is usually shorter — so
    everything below the cell moves up. A click begun before that
    happens presses on one element and releases over another, and is
    lost. Leaving the cell deliberately, and waiting for the collapse,
    keeps the tests below measuring what they mean to measure. (The same
    shift is visible to a reader; see planning/OPEN_QUESTIONS.md.)
    """
    page.locator(".dm-insert-btn", has_text="Text").last.click()
    box = page.locator(".dm-cell-text textarea").last
    box.click()
    page.keyboard.insert_text(prose)
    page.keyboard.press("Tab")
    box.wait_for(state="hidden")


def export_python(page, tmp_path):
    """Clicks the .py download and returns the file's text.

    Through the Settings panel, which is where a reader finds it.
    """
    page.click("#dl-settings-toggle")
    with page.expect_download() as caught:
        page.click("#download-python")
    written = tmp_path / "exported.py"
    caught.value.save_as(written)
    page.click("#dl-settings-toggle")
    return written


def import_file(page, path):
    """Loads a .py or .ipynb through the real file input, as picking a
    file from the Settings panel does."""
    page.set_input_files("#import-ipynb-file", str(path))
    page.wait_for_selector(".dm-tab")


def cell_kinds_and_text(page):
    """Every cell in the visible notebook, as (kind, text) pairs.

    The kind is read from the cell element's own class — createCellElement()
    writes `dm-cell dm-cell-<type>` onto one div, so a descendant lookup for
    `.dm-cell-python` inside a `.dm-cell` finds nothing and silently calls
    every cell a text cell.
    """
    page.wait_for_selector(".dm-cell")
    out = []
    for cell in page.locator(".dm-cell").all():
        classes = cell.get_attribute("class") or ""
        if "dm-cell-python" in classes.split():
            cell.locator(".cm-content").wait_for()
            out.append(("python", cell.locator(".cm-content").inner_text()))
        else:
            out.append(("text", cell.locator("textarea").input_value()))
    return out


def test_a_notebook_exported_as_python_comes_back_the_same(dewmini, tmp_path):
    """The .py round trip, which had no test of any kind before this one.

    `downloadAsPython()` and `parsePyCells()` are each other's inverse and
    neither was covered, so the behaviour was free to drift. Includes the
    two cases that make the reverse tricky: a code cell containing its own
    `#` comment, which must not be mistaken for note prose, and a note
    with a blank line in it, which is written out as a bare `#`.
    """
    add_text_cell(dewmini, "A note.\n\nWith a blank line in it.")
    add_python_cell(dewmini, "# a real comment\ntotal = 1 + 1")
    add_python_cell(dewmini, "total * 2")

    before = cell_kinds_and_text(dewmini)
    assert [kind for kind, _ in before] == ["text", "python", "python"]

    exported = export_python(dewmini, tmp_path)
    import_file(dewmini, exported)

    assert cell_kinds_and_text(dewmini) == before


def test_a_plain_script_imports_as_one_python_cell(dewmini, tmp_path):
    """A file with none of dewmini's markers — anything written anywhere
    else — arrives whole rather than being cut up by guesswork."""
    script = tmp_path / "plain.py"
    script.write_text("import math\n\n# not a cell marker\nprint(math.pi)\n")

    import_file(dewmini, script)

    cells = cell_kinds_and_text(dewmini)
    assert len(cells) == 1
    assert cells[0][0] == "python"
    assert "import math" in cells[0][1] and "print(math.pi)" in cells[0][1]


def test_an_exported_file_uses_the_percent_format(dewmini, tmp_path):
    """The markers are the ones other editors
    read, not ones dewmini invented for itself.

    Asserted on the file's bytes rather than only through the round trip:
    a round trip closes just as neatly on a private format, which is the
    thing this change exists to stop.
    """
    add_text_cell(dewmini, "A heading.")
    add_python_cell(dewmini, "value = 1")

    written = export_python(dewmini, tmp_path).read_text()

    assert "# %% [markdown]" in written
    assert "\n# %%\nvalue = 1" in written
    assert "---- cell" not in written and "---- note" not in written
    # The file is still ordinary Python: nothing outside a comment.
    for line in written.splitlines():
        assert line.startswith("#") or not line.strip() or "value = 1" in line


def test_a_percent_file_written_elsewhere_imports_as_cells(dewmini, tmp_path):
    """The point of the format: a file dewmini never wrote still opens as
    cells. Uses the shapes other tools actually produce — a marker with a
    title after it, a `[markdown]` cell, and imports sitting above the
    first marker.
    """
    foreign = tmp_path / "from_vscode.py"
    foreign.write_text(
        "import math\n"
        "\n"
        "# %% [markdown]\n"
        "# What this does.\n"
        "\n"
        "# %% Compute it tags=[\"slow\"]\n"
        "answer = math.sqrt(16)\n"
    )

    import_file(dewmini, foreign)

    cells = cell_kinds_and_text(dewmini)
    assert [kind for kind, _ in cells] == ["python", "text", "python"]
    # Code above the first marker is kept, not discarded.
    assert "import math" in cells[0][1]
    assert cells[1][1] == "What this does."
    # A marker's title and tags are not mistaken for a text cell.
    assert "answer = math.sqrt(16)" in cells[2][1]



def test_exporting_twice_does_not_grow_the_notebook(dewmini, tmp_path):
    """The export writes a short header explaining what `# %%` means. It
    sits above the first marker so it is not a cell — otherwise it would
    import as a note, be written out again above a fresh copy of itself,
    and a reader who exported and reopened their work a few times would
    accumulate one note per round trip.
    """
    add_python_cell(dewmini, "value = 1")

    first = export_python(dewmini, tmp_path)
    import_file(dewmini, first)
    after_one = cell_kinds_and_text(dewmini)

    second = tmp_path / "again.py"
    dewmini.click("#dl-settings-toggle")
    with dewmini.expect_download() as caught:
        dewmini.click("#download-python")
    caught.value.save_as(second)
    dewmini.click("#dl-settings-toggle")
    import_file(dewmini, second)

    assert cell_kinds_and_text(dewmini) == after_one
    assert second.read_text().count("dewmini export") == 1


def test_a_leading_comment_from_another_file_is_kept(dewmini, tmp_path):
    """dewmini's own header is discarded on import by matching its first
    line. A comment block someone else wrote — a licence notice, an
    attribution — is not dewmini's to throw away.
    """
    foreign = tmp_path / "licensed.py"
    foreign.write_text(
        "# Copyright 2026 Somebody Else.\n"
        "# Licensed under the MIT licence.\n"
        "\n"
        "# %%\n"
        "print('hello')\n"
    )

    import_file(dewmini, foreign)

    cells = cell_kinds_and_text(dewmini)
    assert len(cells) == 2, "the licence header was dropped"
    assert "Copyright 2026 Somebody Else." in cells[0][1]
    assert "MIT licence" in cells[0][1]
