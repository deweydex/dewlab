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

import json

import pytest
from playwright.sync_api import expect

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
    """A fresh dewmini with no saved state, and Web and SQL cells turned on.

    Storage is cleared *before* the real load, on a blank page from the
    same origin: clearing after dewmini has already read localStorage
    would leave the page showing state this test then thinks is gone.

    Web and SQL default off (DECISIONS_LOG.md 7.122) — seeded on here,
    before the real load reads them, because the great majority of this
    suite is testing something else entirely and would otherwise have to
    turn each on for itself. The default-off behaviour, and the toggle
    itself, get their own tests below against a page that does *not* go
    through this fixture.
    """
    page.goto(dewmini_url)
    page.evaluate("""() => {
        localStorage.clear();
        localStorage.setItem('dewmini:celltype-web', 'on');
        localStorage.setItem('dewmini:celltype-sql', 'on');
    }""")
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


def test_settings_and_the_library_share_an_edge(dewmini):
    """Two panels on one edge still close each other — otherwise the second
    simply covers the first. Settings and the Library are that pair now."""
    dewmini.click("#dm-library-toggle")
    assert dewmini.locator("#dm-library").is_visible()

    dewmini.click("#dl-settings-toggle")
    assert dewmini.locator("#dl-settings").is_visible()
    assert dewmini.locator("#dm-library").is_hidden()


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

    before = dewmini.locator("#dm-workbench").bounding_box()["width"]
    drag("#dm-workbench .dl-panel-resize-handle", 140)
    after = dewmini.locator("#dm-workbench").bounding_box()["width"]
    assert after > before + 100, "the left rail should grow when dragged right"

    right_before = dewmini.locator("#dm-library").bounding_box()["width"]
    drag("#dm-library .dl-panel-resize-handle", -140)
    right_after = dewmini.locator("#dm-library").bounding_box()["width"]
    assert right_after > right_before + 100, "the right rail grows when dragged left"

    # The notebook sits between them rather than under either.
    left = dewmini.locator("#dm-workbench").bounding_box()
    right = dewmini.locator("#dm-library").bounding_box()
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


# -------------------------------------------------------- quiet until touched


def _quiet_text_cell(page):
    """Adds a text cell, gives it content, and blurs it so it renders —
    the same setup test_a_text_cell_renders_maths uses."""
    page.locator(".dm-insert-btn", has_text="Text").last.click()
    textarea = page.locator(".dm-textarea").last
    textarea.click()
    page.keyboard.insert_text("A note for the reader.")
    textarea.evaluate("el => el.blur()")
    return page.locator(".dm-cell-text").last


def head_opacity(page, cell) -> str:
    """The cell's .dm-cell-head opacity, after its 0.1s CSS transition has
    had time to settle — reading it immediately after a hover/mouse-move
    can still catch it mid-animation."""
    page.wait_for_timeout(150)
    return cell.locator(".dm-cell-head").evaluate("el => getComputedStyle(el).opacity")


def hover_cell(page, cell):
    """A real mouse move to a point near the cell's own top-left corner
    — inside its header row, above wherever a rendered HTML cell's own
    sandboxed iframe sits. :hover on the outer page does not reliably
    propagate to a cell's ancestors when the cursor sits over a
    cross-origin/sandboxed <iframe> under synthetic (CDP-driven) input,
    even though elementFromPoint confirms the coordinate is genuinely
    inside the cell's own box — a real user's mouse does not have this
    problem, but a test hovering the geometric centre of an HTML cell
    can land squarely inside its iframe and this call needs to be
    reliable regardless of cell type."""
    box = cell.bounding_box()
    page.mouse.move(box["x"] + 15, box["y"] + 15, steps=5)


def test_a_rendered_text_cells_chrome_is_invisible_until_touched(dewmini):
    """DECISIONS_LOG.md 7.115, planning/CELL_IDENTITY.md §4 — a rendered
    text cell reads like part of the page, not a code widget, until a
    reader actually touches it."""
    cell = _quiet_text_cell(dewmini)
    dewmini.mouse.move(5, 5)  # away from the cell entirely
    assert head_opacity(dewmini, cell) == "0"


def test_hovering_the_cell_reveals_its_chrome(dewmini):
    cell = _quiet_text_cell(dewmini)
    dewmini.mouse.move(5, 5)
    assert head_opacity(dewmini, cell) == "0"

    cell.hover()
    assert head_opacity(dewmini, cell) == "1"


def test_tabbing_onto_a_hidden_control_reveals_it_too(dewmini):
    """opacity/pointer-events, not display:none (planning/CELL_IDENTITY.md
    §4) — a keyboard user never needs to hover first."""
    cell = _quiet_text_cell(dewmini)
    dewmini.mouse.move(5, 5)
    assert head_opacity(dewmini, cell) == "0"

    cell.locator(".dm-icon-delete").focus()
    assert head_opacity(dewmini, cell) == "1"


def test_a_python_cells_chrome_is_never_hidden(dewmini):
    """Quiet-until-touched is a text-cell-only affordance — a Python cell
    is meant to be worked on, not read past."""
    add_python_cell(dewmini, "1 + 1")
    dewmini.mouse.move(5, 5)
    cell = dewmini.locator(".dm-cell-python").last
    assert head_opacity(dewmini, cell) == "1"


# ---------------------------------------------------------------- web cells


def _web_cell(page, html="", css=""):
    """Adds a web (merged HTML+CSS) cell, types into whichever of its two
    editors was given content, and clicks Render if there's anything to
    render — the split-view replacement for the old separate
    _html_cell()/_css_cell() helpers (DECISIONS_LOG.md 7.120). Both
    editors are always visible at once, so unlike those helpers there is
    no blur-to-render step; Render is the one explicit trigger."""
    page.locator(".dm-insert-btn", has_text="Web").last.click()
    cell = page.locator(".dm-cell-web").last
    editors = cell.locator(".cm-content")
    if html:
        editors.nth(0).click()
        page.keyboard.insert_text(html)
    if css:
        editors.nth(1).click()
        page.keyboard.insert_text(css)
    if html or css:
        cell.locator(".dm-icon-render").click()
    return cell


def test_a_web_cells_two_editors_are_both_always_visible(dewmini):
    """No Edit/View toggle, unlike the read-not-run types that keep one
    — both the HTML and the CSS editor stay visible and editable
    together, the whole point of merging the two old separate cell
    types (DECISIONS_LOG.md 7.120)."""
    dewmini.locator(".dm-insert-btn", has_text="Web").last.click()
    cell = dewmini.locator(".dm-cell-web").last
    assert cell.locator(".cm-content").count() == 2
    assert cell.locator(".dm-icon-preview").count() == 0
    assert cell.locator(".dm-html-render").is_hidden()


def test_a_web_cells_html_renders_in_a_sandboxed_iframe(dewmini):
    """DECISIONS_LOG.md 7.116/7.120, planning/CELL_IDENTITY.md §8."""
    cell = _web_cell(dewmini, html="<h2>Hello from HTML</h2>")
    frame_el = cell.locator(".dm-html-frame")
    assert frame_el.get_attribute("sandbox") == "allow-scripts"

    frame = frame_el.content_frame
    assert frame.locator("h2").text_content() == "Hello from HTML"


def test_a_web_cells_script_cannot_reach_the_parent_page(dewmini):
    """The whole point of sandbox="allow-scripts" with no
    allow-same-origin: a script inside the cell runs, but in an
    opaque-origin document that cannot touch this page's own window,
    localStorage, or DOM — including a cell imported from a shared
    file, not only one the reader wrote themselves."""
    cell = _web_cell(
        dewmini,
        html='<script>try { window.parent.document.title = "hijacked"; } catch (e) {}</script>',
    )
    dewmini.wait_for_timeout(300)
    assert dewmini.title() != "hijacked"


def test_a_web_cells_css_styles_its_own_html(dewmini):
    """The capability merging the two types unlocks that neither could
    do alone: a CSS rule styling the *same* cell's own markup, not a
    fixed sample page — the pairing the old separate CSS cell's own
    design note explicitly declined to guess at, now not a guess at
    all (DECISIONS_LOG.md 7.120)."""
    cell = _web_cell(
        dewmini,
        html="<h2>Styled</h2><button>Go</button>",
        css="h2 { color: rebeccapurple; } button { background: gold; }",
    )
    frame = cell.locator(".dm-html-frame").content_frame
    assert frame.locator("h2").text_content() == "Styled"
    assert frame.locator("h2").evaluate("el => getComputedStyle(el).color") == "rgb(102, 51, 153)"
    assert frame.locator("button").evaluate(
        "el => getComputedStyle(el).backgroundColor"
    ) == "rgb(255, 215, 0)"


def test_an_empty_html_half_falls_back_to_the_fixed_preview(dewmini):
    """A CSS-only web cell — the old standalone CSS cell's own use case
    — still has something real to style before the reader has written
    any markup of their own (DECISIONS_LOG.md 7.117/7.120)."""
    cell = _web_cell(dewmini, css="h2 { color: rebeccapurple; }")
    frame = cell.locator(".dm-html-frame").content_frame
    assert frame.locator("h2").evaluate("el => getComputedStyle(el).color") == "rgb(102, 51, 153)"


def test_rendering_a_web_cell_only_happens_on_render_click(dewmini):
    """Explicit, not on blur, unlike the two types this replaces — two
    editors both auto-rendering on their own focusout would fire twice
    for one edit (DECISIONS_LOG.md 7.120)."""
    dewmini.locator(".dm-insert-btn", has_text="Web").last.click()
    cell = dewmini.locator(".dm-cell-web").last
    editor = cell.locator(".cm-content").first
    editor.click()
    dewmini.keyboard.insert_text("<p>Not rendered yet</p>")
    editor.evaluate("el => el.blur()")
    assert cell.locator(".dm-html-render").is_hidden()

    cell.locator(".dm-icon-render").click()
    assert cell.locator(".dm-html-render").is_visible()


def test_a_web_cells_chrome_is_also_quiet_until_touched(dewmini):
    cell = _web_cell(dewmini, html="<p>Hi</p>")
    # _web_cell() leaves focus inside whichever editor it typed into —
    # there's no blur-to-render step to do that for it here, unlike the
    # old _html_cell()/_css_cell() helpers. :focus-within keeps the
    # chrome visible while focus is still there, correctly, so this has
    # to move focus away itself before checking quiet-until-touched.
    dewmini.evaluate("document.activeElement.blur()")
    dewmini.mouse.move(5, 5)
    assert head_opacity(dewmini, cell) == "0"

    hover_cell(dewmini, cell)
    assert head_opacity(dewmini, cell) == "1"


def test_a_web_cell_survives_a_reload(dewmini):
    _web_cell(dewmini, html="<p>Saved HTML</p>", css="p { color: teal; }")
    dewmini.reload()
    dewmini.wait_for_selector(".dm-toolbar")
    assert dewmini.locator(".dm-cell-web").count() == 1
    frame = dewmini.locator(".dm-cell-web .dm-html-frame").content_frame
    assert "Saved HTML" in frame.locator("p").text_content()
    assert frame.locator("p").evaluate("el => getComputedStyle(el).color") == "rgb(0, 128, 128)"


def test_a_web_cell_can_be_collapsed_and_duplicated(dewmini):
    cell = _web_cell(dewmini, html="<p>Some markup</p>")
    hover_cell(dewmini, cell)
    cell.locator(".dm-collapse-toggle").click()
    assert cell.locator(".dm-cell-content").is_hidden()
    assert cell.locator(".dm-cell-collapsed-summary").is_visible()

    cell.locator(".dm-icon-duplicate").click()
    assert dewmini.locator(".dm-cell-web").count() == 2


def test_old_html_and_css_cells_migrate_to_web_cells_on_load(dewmini):
    """A notebook saved before 7.120 could hold standalone `html`/`css`
    cells — both retired in favour of the merged `web` type. Each old
    cell becomes its own new `web` cell independently: an old HTML
    cell's markup becomes the new cell's HTML half with an empty CSS
    half, and vice versa — never merged into one cell, since guessing
    which HTML an old CSS cell was written to style is exactly the
    ambiguity DECISIONS_LOG.md 7.120 declines to resolve."""
    dewmini.evaluate(
        """() => {
            localStorage.setItem("dewmini:notebooks:v1", JSON.stringify({
                active: "nb-1",
                notebooks: [{
                    id: "nb-1", name: "Notebook",
                    cells: [
                        { id: "c1", type: "html", content: "<p>Old HTML cell</p>", output: "", error: false },
                        { id: "c2", type: "css", content: "h2 { color: rebeccapurple; }", output: "", error: false },
                    ],
                }],
            }));
        }"""
    )
    dewmini.reload()
    dewmini.wait_for_selector(".dm-toolbar")

    cells = dewmini.locator(".dm-cell-web")
    assert cells.count() == 2

    first_frame = cells.nth(0).locator(".dm-html-frame").content_frame
    assert "Old HTML cell" in first_frame.locator("p").text_content()

    second_frame = cells.nth(1).locator(".dm-html-frame").content_frame
    assert second_frame.locator("h2").evaluate("el => getComputedStyle(el).color") == "rgb(102, 51, 153)"


# ---------------------------------------------------------------- sql cells


def add_sql_cell(page, script: str) -> None:
    """Adds a SQL cell and types `script` into it — the SQL counterpart of
    add_python_cell() above. Unlike _html_cell()/_css_cell(), no blur: a
    SQL cell has no rendered/editor toggle to fall into (it keeps
    Python-shaped chrome, RUNS_AGAINST_SESSION), so there is nothing to
    render until the reader actually clicks Run."""
    page.locator(".dm-insert-btn", has_text="SQL").last.click()
    editor = page.locator(".dm-cell-sql .cm-content").last
    editor.click()
    page.keyboard.insert_text(script)


def test_a_sql_cells_chrome_is_never_hidden(dewmini):
    """Python-shaped chrome, not HTML/CSS-shaped: a SQL cell runs against
    the shared session, so quiet-until-touched (a read-not-run affordance)
    does not apply to it — the same rule test_a_python_cells_chrome_is_
    never_hidden() above checks for Python."""
    add_sql_cell(dewmini, "select 1")
    dewmini.mouse.move(5, 5)
    cell = dewmini.locator(".dm-cell-sql").last
    assert head_opacity(dewmini, cell) == "1"
    assert cell.locator(".dm-icon-preview").count() == 0
    assert cell.locator(".dm-cell-runline").count() == 1


def test_a_multi_statement_sql_script_renders_only_its_last_statement(dewmini):
    """planning/CELL_IDENTITY.md §8 — a SQL cell is a script (CREATE,
    INSERT, ..., SELECT), not a single query the way run_query() is; only
    the final statement's own result renders, here the SELECT's table."""
    add_sql_cell(
        dewmini,
        "CREATE TABLE t (id INTEGER, name TEXT);\n"
        "INSERT INTO t VALUES (1, 'ada'), (2, 'alan');\n"
        "SELECT * FROM t ORDER BY id;",
    )
    dewmini.locator(".dm-cell-sql .dm-icon-run").last.click()
    dewmini.wait_for_selector(".dm-cell-sql .dm-cell-output table", timeout=90_000)
    text = dewmini.locator(".dm-cell-sql .dm-cell-output").last.inner_text()
    assert "ada" in text and "alan" in text


def test_a_non_select_sql_statement_reports_rows_affected(dewmini):
    """The console-style fallback _run_sql_cell() gives a script that ends
    in a CREATE/INSERT/UPDATE/DELETE rather than a SELECT."""
    add_sql_cell(dewmini, "CREATE TABLE t (id INTEGER);\nINSERT INTO t VALUES (1), (2), (3);")
    dewmini.locator(".dm-cell-sql .dm-icon-run").last.click()
    dewmini.wait_for_selector(".dm-cell-sql .dm-cell-output:not(.dm-empty)", timeout=90_000)
    assert "3 rows affected" in dewmini.locator(".dm-cell-sql .dm-cell-output").last.inner_text()


def test_a_python_cell_can_read_what_a_sql_cell_wrote(dewmini):
    """The whole reason SQL cells run on Python's own sqlite3 rather than a
    separate engine (DECISIONS_LOG.md, the sql.js → Python/sqlite3 pivot):
    the shared `db` connection is available to an ordinary Python cell
    under the same name, with no plumbing of its own."""
    add_sql_cell(dewmini, "CREATE TABLE t (id INTEGER, name TEXT);\nINSERT INTO t VALUES (1, 'grace');")
    dewmini.locator(".dm-cell-sql .dm-icon-run").last.click()
    dewmini.wait_for_selector(".dm-cell-sql .dm-cell-output:not(.dm-empty)", timeout=90_000)

    add_python_cell(dewmini, "import pandas as pd\npd.read_sql('select * from t', db)")
    dewmini.locator(".dm-cell-python .dm-icon-run").last.click()
    dewmini.wait_for_selector(".dm-cell-python .dm-cell-output table", timeout=90_000)
    assert "grace" in dewmini.locator(".dm-cell-python .dm-cell-output").last.inner_text()


def test_a_sql_cells_output_survives_a_reload(dewmini):
    add_sql_cell(dewmini, "select 6 * 7 as answer;")
    dewmini.locator(".dm-cell-sql .dm-icon-run").last.click()
    dewmini.wait_for_selector(".dm-cell-sql .dm-cell-output table", timeout=90_000)

    dewmini.reload()
    dewmini.wait_for_selector(".dm-toolbar")
    assert dewmini.locator(".dm-cell-sql").count() == 1
    assert "42" in dewmini.locator(".dm-cell-sql .dm-cell-output").last.inner_text()


def test_a_sql_cell_can_be_collapsed_and_duplicated(dewmini):
    add_sql_cell(dewmini, "select 1;")
    cell = dewmini.locator(".dm-cell-sql").last
    cell.locator(".dm-collapse-toggle").click()
    assert cell.locator(".dm-cell-content").is_hidden()
    assert cell.locator(".dm-cell-collapsed-summary").is_visible()

    cell.locator(".dm-icon-duplicate").click()
    assert dewmini.locator(".dm-cell-sql").count() == 2


def test_a_bad_sql_statement_shows_an_error_not_a_silent_failure(dewmini):
    add_sql_cell(dewmini, "select * from a_table_that_does_not_exist;")
    dewmini.locator(".dm-cell-sql .dm-icon-run").last.click()
    dewmini.wait_for_selector(".dm-cell-sql .dm-cell-output:not(.dm-empty)", timeout=90_000)
    cell = dewmini.locator(".dm-cell-sql").last
    assert "dm-error" in (cell.get_attribute("class") or "")


# ----------------------------------------------------------- javascript cells


def add_js_cell(page, code: str) -> None:
    """Adds a JavaScript cell and types `code` into it — the JS counterpart
    of add_python_cell()/add_sql_cell() above. Python-shaped chrome, like
    SQL: no blur, nothing renders until Run."""
    page.locator(".dm-insert-btn", has_text="JS").last.click()
    editor = page.locator(".dm-cell-javascript .cm-content").last
    editor.click()
    page.keyboard.insert_text(code)


def test_a_js_cells_chrome_is_never_hidden(dewmini):
    """Python-shaped chrome, same reasoning as SQL's own version of this
    test — a JavaScript cell runs against a shared session too, so
    quiet-until-touched does not apply to it."""
    add_js_cell(dewmini, "1 + 1")
    dewmini.mouse.move(5, 5)
    cell = dewmini.locator(".dm-cell-javascript").last
    assert head_opacity(dewmini, cell) == "1"
    assert cell.locator(".dm-icon-preview").count() == 0
    assert cell.locator(".dm-cell-runline").count() == 1


def test_console_log_is_captured_as_the_cells_output(dewmini):
    add_js_cell(dewmini, "console.log('hello from JS', 6 * 7);")
    dewmini.locator(".dm-cell-javascript .dm-icon-run").last.click()
    dewmini.wait_for_selector(".dm-cell-javascript .dm-cell-output:not(.dm-empty)", timeout=30_000)
    text = dewmini.locator(".dm-cell-javascript .dm-cell-output").last.inner_text()
    assert "hello from JS 42" in text


def test_rerunning_a_let_declaring_cell_does_not_throw(dewmini):
    """The whole reason a JS cell's code runs through indirect eval rather
    than an inserted <script> tag (compose/js-cell-engine.js's own file
    banner, DECISIONS_LOG.md 7.119): a top-level `let` declared by a
    <script> tag joins the realm's one permanent global lexical scope, so
    re-running an edited cell — an entirely ordinary thing to do — would
    throw "Identifier has already been declared" on its second run.
    Indirect eval's own top-level `let` lives in a scope private to that
    one call, so this must never happen."""
    add_js_cell(dewmini, "let total = 0;\nfor (let i = 1; i <= 5; i++) { total += i; }\nconsole.log('total', total);")
    cell = dewmini.locator(".dm-cell-javascript").last
    cell.locator(".dm-icon-run").click()
    dewmini.wait_for_selector(".dm-cell-javascript .dm-cell-output:not(.dm-empty)", timeout=30_000)
    assert "total 15" in cell.locator(".dm-cell-output").inner_text()
    assert "dm-error" not in (cell.get_attribute("class") or "")

    cell.locator(".dm-icon-run").click()
    dewmini.wait_for_timeout(500)
    assert "total 15" in cell.locator(".dm-cell-output").inner_text()
    assert "dm-error" not in (cell.get_attribute("class") or ""), \
        "re-running an unchanged `let`-declaring cell must not throw"


def test_var_declared_in_one_cell_is_visible_to_a_later_one(dewmini):
    """The one form of cross-cell persistence indirect eval still gives —
    var/function declarations become real global-object properties, the
    same as a <script> tag's own would, just without the redeclaration
    risk `let`/`const` carry (see the test above)."""
    add_js_cell(dewmini, "var shared = 10;")
    dewmini.locator(".dm-cell-javascript .dm-icon-run").last.click()
    dewmini.wait_for_timeout(500)

    add_js_cell(dewmini, "console.log('shared is', shared + 1);")
    dewmini.locator(".dm-cell-javascript .dm-icon-run").last.click()
    dewmini.wait_for_selector(".dm-cell-javascript .dm-cell-output:not(.dm-empty)", timeout=30_000)
    assert "shared is 11" in dewmini.locator(".dm-cell-javascript .dm-cell-output").last.inner_text()


def test_a_thrown_error_shows_in_the_cells_output(dewmini):
    add_js_cell(dewmini, "thisNameDoesNotExist();")
    cell = dewmini.locator(".dm-cell-javascript").last
    cell.locator(".dm-icon-run").click()
    dewmini.wait_for_selector(".dm-cell-javascript .dm-cell-output:not(.dm-empty)", timeout=30_000)
    assert "dm-error" in (cell.get_attribute("class") or "")
    assert "thisNameDoesNotExist" in cell.locator(".dm-cell-output").inner_text()


def test_a_js_cells_output_survives_a_reload(dewmini):
    add_js_cell(dewmini, "console.log('reload me');")
    dewmini.locator(".dm-cell-javascript .dm-icon-run").last.click()
    dewmini.wait_for_selector(".dm-cell-javascript .dm-cell-output:not(.dm-empty)", timeout=30_000)

    dewmini.reload()
    dewmini.wait_for_selector(".dm-toolbar")
    assert dewmini.locator(".dm-cell-javascript").count() == 1
    assert "reload me" in dewmini.locator(".dm-cell-javascript .dm-cell-output").last.inner_text()


def test_a_js_cell_can_be_collapsed_and_duplicated(dewmini):
    add_js_cell(dewmini, "1;")
    cell = dewmini.locator(".dm-cell-javascript").last
    cell.locator(".dm-collapse-toggle").click()
    assert cell.locator(".dm-cell-content").is_hidden()
    assert cell.locator(".dm-cell-collapsed-summary").is_visible()

    cell.locator(".dm-icon-duplicate").click()
    assert dewmini.locator(".dm-cell-javascript").count() == 2


def test_restart_python_tears_down_the_js_session_too(dewmini):
    """planning/CELL_IDENTITY.md §8 — the JS session is torn down and
    recreated on Restart Python exactly like the Pyodide interpreter is.
    A var surviving a restart would mean it wasn't really recreated."""
    add_js_cell(dewmini, "var survivesRestart = 42;")
    dewmini.locator(".dm-cell-javascript .dm-icon-run").last.click()
    dewmini.wait_for_timeout(500)

    dewmini.click("#dl-settings-toggle")
    dewmini.wait_for_selector("#settings-restart-python")
    dewmini.once("dialog", lambda d: d.accept())
    dewmini.click("#settings-restart-python")
    dewmini.wait_for_timeout(1000)
    dewmini.click("#dl-settings-toggle")

    add_js_cell(dewmini, "console.log('survivesRestart is', typeof survivesRestart);")
    cell = dewmini.locator(".dm-cell-javascript").last
    cell.locator(".dm-icon-run").click()
    dewmini.wait_for_selector(".dm-cell-javascript .dm-cell-output:not(.dm-empty)", timeout=30_000)
    assert "survivesRestart is undefined" in cell.locator(".dm-cell-output").last.inner_text()


def test_run_all_runs_python_and_javascript_cells_together(dewmini):
    """RUNS_AGAINST_SESSION covers both — "Run all" should not silently
    skip one type just because the two run through different engines."""
    add_js_cell(dewmini, "console.log('js ran');")
    add_python_cell(dewmini, "print('py ran')")
    dewmini.locator("#run-all").click()
    dewmini.wait_for_function(
        "document.querySelectorAll('.dm-cell-output')[1]?.innerText.trim().length > 0",
        timeout=90_000,
    )
    texts = dewmini.locator(".dm-cell-output").all_inner_texts()
    assert any("js ran" in t for t in texts)
    assert any("py ran" in t for t in texts)


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


# ------------------------------------------------------------------ storage


def test_a_full_storage_keeps_the_code_and_says_what_it_dropped(dewmini):
    """When localStorage fills, saveState() gives up outputs rather than
    giving up silently. See "Keeping your work" in docs/DEWMINI.md.

    The old version wrapped its one `setItem` in an empty `catch`, so a
    student with a few figures crossed the browser's ~5 MB limit and their
    work simply stopped being saved: no error on screen, and a reload back
    to whatever had been stored before the first failed write.

    This fills storage from the page itself rather than mocking `setItem`,
    because the behaviour under test *is* the browser's real quota — a
    stubbed throw would prove only that the catch block runs.
    """
    # Fill storage to the brim, then hand back one chunk. What is left is
    # room for the notebook's code and nowhere near room for its output.
    headroom = dewmini.evaluate(
        """() => {
          const chunk = "x".repeat(64 * 1024);
          let i = 0;
          try {
            for (; i < 200; i += 1) localStorage.setItem(`filler:${i}`, chunk);
          } catch {}
          if (i === 0) return 0;
          localStorage.removeItem(`filler:${i - 1}`);
          return i;
        }"""
    )
    assert headroom > 0, "this browser let us write 200 chunks — the quota is not what we assumed"

    # An output far larger than the single chunk of headroom left above.
    add_python_cell(dewmini, 'print("y" * 300000)')
    dewmini.locator(".dm-cell .dm-icon-run").first.click()
    dewmini.wait_for_selector(".dm-cell-output:not(.dm-empty)", timeout=90_000)

    # The reader is told, and told that the code is the part that survived.
    # The notice, not the status line: a run posts "Ran." to that line the
    # instant after the save, which is exactly why this has its own place.
    notice = dewmini.locator("#storage-notice")
    notice.wait_for(state="visible", timeout=30_000)
    assert "code is saved" in notice.inner_text()
    assert "run that cell again" in notice.inner_text()

    # The part that actually mattered: work done *after* the oversized
    # output still gets saved. Under the old empty `catch` every write
    # from here on failed — the payload always carried that output — so
    # this second cell would never reach storage and a reload would find
    # one cell, not two.
    add_python_cell(dewmini, "written_after = 1")

    dewmini.reload()
    dewmini.wait_for_selector(".dm-cell")
    assert dewmini.locator(".dm-cell").count() == 2, "the save stopped working after the big output"
    text = dewmini.locator(".cm-content").all_inner_texts()
    assert any('print("y" * 300000)' in t for t in text)
    assert any("written_after = 1" in t for t in text)
    # The code came back; the output it could not store did not.
    assert dewmini.locator(".dm-cell-output").first.inner_text().strip() == ""


def test_an_ordinary_save_says_nothing_about_storage(dewmini):
    """The degraded path must not leak into the normal one: a small
    notebook saves in silence, as it always did."""
    add_python_cell(dewmini, "small = 1")
    dewmini.locator(".dm-cell .dm-icon-run").first.click()
    dewmini.wait_for_function(
        "document.querySelectorAll('.dm-cell').length === 1", timeout=90_000
    )
    assert dewmini.locator("#storage-notice").is_hidden()
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


# --------------------------------------------------- outputs in a .ipynb

# A 1x1 transparent PNG. Small enough to write inline, real enough that a
# browser renders it — so an image can be tested without paying for a
# matplotlib figure on every run.
TINY_PNG = (
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk"
    "YPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="
)

# What real Jupyter leaves in a traceback: terminal colour codes, which are
# instructions to a terminal and line noise in a browser.
ANSI_TRACEBACK = "\x1b[0;31mZeroDivisionError\x1b[0m: division by zero"


def import_file(page, path):
    """Loads a .ipynb or .py through the real file input, which is what
    picking a file from the Settings panel does."""
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
# ------------------------------------------- importing a workspace file


def run_first_cell_and_wait(page, index=0):
    """Runs one cell by index and waits for its output to arrive."""
    page.locator(".dm-cell .dm-icon-run").nth(index).click()
    page.wait_for_function(
        "(i) => {"
        " const out = document.querySelectorAll('.dm-cell-output')[i];"
        " return out && out.innerText.trim().length > 0;"
        "}",
        arg=index,
        timeout=120_000,
    )
    return page.locator(".dm-cell-output").nth(index).inner_text().strip()


def test_a_workspace_file_can_be_imported(dewmini):
    """The whole point of putting the mount on `sys.path`: a .py file a
    student writes in the workspace is importable by name.

    Before this, the workspace was readable and not importable — a
    student could have two Python files and no way to use one from the
    other, which is exactly the step this is meant to teach.
    """
    add_python_cell(
        dewmini,
        'open("/mnt/dewmini/shapes.py", "w").write("def area(side):\\n    return side * side\\n")\n'
        "import shapes\n"
        "shapes.area(4)",
    )

    assert run_first_cell_and_wait(dewmini) == "16"


def test_an_edited_import_is_reported_and_can_be_re_read(dewmini):
    """The failure that comes free with importing, and the answer to it.

    Python keeps an imported module in `sys.modules` and hands back the
    remembered one rather than re-reading the file, so a student who
    fixes their .py and runs the cell again gets the same wrong answer
    with nothing on screen to explain it. dewmini says so, and offers to
    re-read — rather than reloading silently, which would teach nothing
    about behaviour they will meet in every other Python environment.
    """
    add_python_cell(
        dewmini,
        'open("/mnt/dewmini/tools.py", "w").write("def double(n):\\n    return n + n\\n")\n'
        "import tools\n"
        "tools.double(5)",
    )
    assert run_first_cell_and_wait(dewmini) == "10"

    # The student edits the file — here, from another cell, which is the
    # only way to write into the workspace before a file editor exists.
    add_python_cell(
        dewmini,
        'open("/mnt/dewmini/tools.py", "w").write("def double(n):\\n    return n * 2 + 100\\n")\n'
        '"edited"',
    )
    run_first_cell_and_wait(dewmini, 1)

    # Nothing has been said yet, and the old version is still what runs.
    add_python_cell(dewmini, "tools.double(5)")
    assert run_first_cell_and_wait(dewmini, 2) == "10", "Python should still be using the old module"

    # The run above is what noticed. The notice names the file.
    notice = dewmini.locator("#stale-imports-notice")
    notice.wait_for(state="visible", timeout=30_000)
    assert "tools.py" in notice.inner_text()

    dewmini.click("#reload-stale-imports")
    assert notice.is_hidden()

    # Waiting for the new value rather than for "some output": the old
    # output is still on screen when the re-run starts, so a check for
    # non-empty text can read the previous answer and pass by luck.
    dewmini.locator(".dm-cell .dm-icon-run").nth(2).click()
    dewmini.wait_for_function(
        "document.querySelectorAll('.dm-cell-output')[2].innerText.trim() === '110'",
        timeout=120_000,
    )
def export_ipynb(page, tmp_path, name="exported.ipynb"):
    """Clicks the .ipynb download and returns the parsed notebook."""
    page.click("#dl-settings-toggle")
    with page.expect_download() as caught:
        page.click("#download-ipynb")
    written = tmp_path / name
    caught.value.save_as(written)
    page.click("#dl-settings-toggle")
    return json.loads(written.read_text())


def write_ipynb(path, cells):
    """Writes a minimal but valid nbformat 4 notebook."""
    path.write_text(json.dumps({
        "nbformat": 4,
        "nbformat_minor": 5,
        "metadata": {},
        "cells": cells,
    }))
    return path


def code_cell(source, outputs):
    return {
        "cell_type": "code",
        "metadata": {},
        "execution_count": 1,
        "source": [source],
        "outputs": outputs,
    }


def test_a_printed_output_reaches_the_exported_ipynb(dewmini, tmp_path):
    """`downloadAsIpynb()` wrote `outputs: []` for every code cell, so a
    notebook exported from dewmini carried none of its results.

    Asserted on nbformat's own shape rather than only through a round
    trip: the whole reason for using the published format is that other
    programs read it, and a round trip closes just as neatly on a shape
    only dewmini understands.
    """
    add_python_cell(dewmini, 'print("forty two")')
    dewmini.locator(".dm-cell .dm-icon-run").first.click()
    dewmini.wait_for_selector(".dm-cell-output:not(.dm-empty)", timeout=120_000)

    notebook = export_ipynb(dewmini, tmp_path)
    outputs = notebook["cells"][0]["outputs"]

    assert len(outputs) == 1
    assert outputs[0]["output_type"] == "stream"
    assert outputs[0]["name"] == "stdout"
    assert "forty two" in "".join(outputs[0]["text"])


def test_an_imported_notebooks_outputs_are_shown(dewmini, tmp_path):
    """`parseIpynbCells()` set every imported cell's output to the empty
    string, so a student who opened a notebook lost every result it came
    with and was told nothing about it."""
    path = write_ipynb(tmp_path / "with_results.ipynb", [code_cell(
        "print('from the file')\n",
        [{"output_type": "stream", "name": "stdout", "text": ["from the file\n"]}],
    )])

    import_file(dewmini, path)

    output = dewmini.locator(".dm-cell-output").first
    output.wait_for(state="visible")
    assert "from the file" in output.inner_text()


def test_an_image_survives_the_round_trip_as_a_png(dewmini, tmp_path):
    """A figure has to travel as a real `image/png`, not as HTML with a
    base64 string buried in it — that is the difference between another
    notebook tool showing a picture and showing markup.

    Goes in as a file and back out as one, which exercises both
    translations without paying for a matplotlib figure.
    """
    path = write_ipynb(tmp_path / "with_figure.ipynb", [code_cell(
        "plot()\n",
        [{"output_type": "display_data", "data": {"image/png": TINY_PNG}, "metadata": {}}],
    )])

    import_file(dewmini, path)
    assert dewmini.locator(".dm-cell-output img").count() == 1

    notebook = export_ipynb(dewmini, tmp_path, "round-tripped.ipynb")
    outputs = notebook["cells"][0]["outputs"]
    assert len(outputs) == 1
    assert "image/png" in outputs[0]["data"], "the figure came back as something other than an image"
    assert "".join(outputs[0]["data"]["image/png"]).strip() == TINY_PNG


def test_html_output_from_an_imported_notebook_cannot_bring_anything_active(dewmini, tmp_path):
    """An imported .ipynb is a file from anywhere, and its HTML outputs go
    into the page. Only an allow-list is safe here: a list of things to
    remove is as good as its author's imagination, and a list of things
    to keep fails closed.

    The table's real content has to survive, or the sanitising has simply
    replaced one broken behaviour with another.
    """
    hostile = (
        "<table><tr><td>keep this number</td></tr></table>"
        "<script>window.__ranFromNotebook = true;</script>"
        '<img src="x" onerror="window.__ranFromNotebook = true">'
        '<img src="https://example.invalid/tracker.gif">'
        '<a href="javascript:void(0)">a link</a>'
    )
    path = write_ipynb(tmp_path / "hostile.ipynb", [code_cell(
        "frame\n",
        [{"output_type": "display_data", "data": {"text/html": [hostile]}, "metadata": {}}],
    )])

    import_file(dewmini, path)

    output = dewmini.locator(".dm-cell-output").first
    output.wait_for(state="visible")

    assert "keep this number" in output.inner_text(), "the table's own content was thrown away"
    assert output.locator("script").count() == 0
    assert output.locator("img").count() == 0, "neither <img> here has a source worth keeping"
    assert output.locator("a").count() == 0, "an anchor is not on the allow-list"
    assert dewmini.evaluate("window.__ranFromNotebook === true") is False


def test_an_error_output_from_a_file_reads_as_an_error(dewmini, tmp_path):
    """nbformat's `error` output carries the exception separately from its
    traceback, and real Jupyter leaves terminal colour codes in that
    traceback."""
    path = write_ipynb(tmp_path / "with_error.ipynb", [code_cell(
        "1 / 0\n",
        [{
            "output_type": "error",
            "ename": "ZeroDivisionError",
            "evalue": "division by zero",
            "traceback": [ANSI_TRACEBACK],
        }],
    )])

    import_file(dewmini, path)

    output = dewmini.locator(".dm-cell-output").first
    output.wait_for(state="visible")
    shown = output.inner_text()
    assert "ZeroDivisionError" in shown and "division by zero" in shown
    assert "0;31m" not in shown, "terminal colour codes reached the page"
    assert output.locator(".dl-error").count() == 1


# --------------------------------------------------------------- file view


def switch_view(page, which: str) -> None:
    """Switches between the cells view and the file view."""
    page.locator(f"#dm-view-{which}").click()


def test_the_file_view_shows_the_notebook_as_one_python_file(dewmini):
    """Two cells become one document with the markers between them."""
    add_python_cell(dewmini, "x = 1")
    add_python_cell(dewmini, "print(x)")
    switch_view(dewmini, "file")

    text = dewmini.locator(".dm-fileview-editor .cm-content").inner_text()
    assert "# %%" in text
    assert "x = 1" in text
    assert "print(x)" in text
    # One editor for the whole file, not one per cell.
    assert dewmini.locator(".dm-cell").count() == 0


def test_a_text_cell_survives_the_round_trip_as_a_comment(dewmini):
    """A note goes out commented and comes back as a note, not as code."""
    add_python_cell(dewmini, "x = 1")
    dewmini.locator(".dm-insert-btn", has_text="Text").last.click()
    dewmini.locator(".dm-cell-text textarea").last.fill("A note about x")
    dewmini.locator("h1").click()  # blur, so the text cell commits

    switch_view(dewmini, "file")
    text = dewmini.locator(".dm-fileview-editor .cm-content").inner_text()
    assert "# %% [markdown]" in text
    assert "# A note about x" in text

    switch_view(dewmini, "cells")
    kinds = dewmini.evaluate(
        "() => [...document.querySelectorAll('.dm-cell')]"
        ".map(c => c.className.includes('dm-cell-text') ? 'text' : 'python')"
    )
    assert kinds == ["python", "text"]


def test_a_round_trip_through_the_file_view_keeps_outputs(dewmini):
    """The point of merging by content: an untouched cell keeps its result.

    parsePyCells() mints a fresh id for every cell it reads, and a cell's
    output is stored under its id. Without the merge, one look at the file
    view would silently empty every output in the notebook.
    """
    add_python_cell(dewmini, "print('kept')")
    before = run_first_cell_and_wait(dewmini)
    assert before == "kept"

    switch_view(dewmini, "file")
    switch_view(dewmini, "cells")

    assert dewmini.locator(".dm-cell-output").first.inner_text().strip() == "kept"


def test_a_blank_cell_survives_a_round_trip_through_the_file_view(dewmini):
    """A cell with nothing in it yet is not "no cell" — parsePyCells() must
    not read an empty stretch between two `# %%` markers as absent.

    Regression test: flush() inside parsePyCells() used to skip any cell
    whose content was blank after trimming, with no way to tell "no marker
    asked for a cell here" apart from "a marker did, and it is just empty
    right now". A reader who inserted a fresh cell and glanced at the file
    view, or cleared one out while editing, lost it the moment the view
    switched back.
    """
    add_python_cell(dewmini, "x = 1")
    dewmini.locator(".dm-insert-btn", has_text="Python").last.click()  # left blank

    assert dewmini.locator(".dm-cell").count() == 2

    switch_view(dewmini, "file")
    switch_view(dewmini, "cells")

    assert dewmini.locator(".dm-cell").count() == 2


def test_editing_in_the_file_view_reaches_the_cells(dewmini):
    """Text typed into the file becomes a cell when the view switches back."""
    add_python_cell(dewmini, "x = 1")
    switch_view(dewmini, "file")

    editor = dewmini.locator(".dm-fileview-editor .cm-content")
    editor.click()
    dewmini.keyboard.press("Control+End")
    dewmini.keyboard.insert_text("\n# %%\ny = 2\n")

    switch_view(dewmini, "cells")
    contents = dewmini.evaluate(
        "() => [...document.querySelectorAll('.dm-cell .cm-content')]"
        ".map(e => e.innerText.trim())"
    )
    assert any("y = 2" in c for c in contents)


def test_the_file_view_survives_a_reload(dewmini, dewmini_url):
    """Which view you left a notebook in is part of the notebook."""
    add_python_cell(dewmini, "x = 1")
    switch_view(dewmini, "file")
    dewmini.goto(dewmini_url)
    dewmini.wait_for_selector(".dm-fileview-editor")
    assert dewmini.locator("#dm-view-file").get_attribute("aria-pressed") == "true"


def test_running_the_file_runs_the_whole_thing_in_order(dewmini):
    """A file runs top to bottom, with its output in one place."""
    add_python_cell(dewmini, "a = 2")
    add_python_cell(dewmini, "print(a * 3)")
    switch_view(dewmini, "file")

    dewmini.locator(".dm-fileview-run").click()
    dewmini.wait_for_function(
        "() => {"
        " const out = document.querySelector('.dm-fileview-output');"
        " return out && out.innerText.trim() === '6';"
        "}",
        timeout=120_000,
    )


# ------------------------------------------------------------ file manager


def write_workspace_file(page, name: str, text: str) -> None:
    """Writes a file into the workspace from a Python cell, and waits.

    Through a cell rather than through the filesystem interface directly,
    because that is how a student's own file gets there, and it also
    guarantees Python has started before the Files panel is asked for a
    listing.
    """
    add_python_cell(page, f"open({name!r}, 'w').write({text!r})")
    run_first_cell_and_wait(page, page.locator(".dm-cell").count() - 1)


def open_files_panel(page):
    page.locator("#dm-workbench-toggle").click()
    page.wait_for_selector("#settings-file-list li")


def test_a_py_file_in_the_workspace_opens_as_a_file(dewmini):
    """Clicking a .py opens it in a tab, showing it as a file."""
    write_workspace_file(dewmini, "shapes.py", "def area(r):\n    return 3.14 * r * r\n")
    open_files_panel(dewmini)

    dewmini.locator(".dm-filelist-item-name", has_text="shapes.py").click()
    dewmini.wait_for_selector(".dm-fileview-editor")

    assert dewmini.locator("#dm-view-file").get_attribute("aria-pressed") == "true"
    assert "def area" in dewmini.locator(".dm-fileview-editor .cm-content").inner_text()


def test_an_ipynb_in_the_workspace_opens_as_cells(dewmini):
    """A notebook file opens rendered, because that format carries outputs."""
    notebook = (
        '{"nbformat": 4, "nbformat_minor": 5, "metadata": {}, "cells": ['
        '{"cell_type": "code", "execution_count": null, "metadata": {},'
        ' "source": ["print(\\"from a file\\")"], "outputs": []}]}'
    )
    write_workspace_file(dewmini, "saved.ipynb", notebook)
    open_files_panel(dewmini)

    dewmini.locator(".dm-filelist-item-name", has_text="saved.ipynb").click()
    dewmini.wait_for_selector(".dm-cell")

    assert dewmini.locator("#dm-view-cells").get_attribute("aria-pressed") == "true"
    contents = dewmini.evaluate(
        "() => [...document.querySelectorAll('.dm-cell .cm-content')]"
        ".map(e => e.innerText)"
    )
    assert any("from a file" in c for c in contents)


def test_editing_an_opened_file_writes_back_to_the_workspace(dewmini):
    """The difference between a file manager and an import button."""
    write_workspace_file(dewmini, "notes.py", "x = 1\n")
    open_files_panel(dewmini)
    dewmini.locator(".dm-filelist-item-name", has_text="notes.py").click()
    dewmini.wait_for_selector(".dm-fileview-editor")

    editor = dewmini.locator(".dm-fileview-editor .cm-content")
    editor.click()
    dewmini.keyboard.press("Control+End")
    dewmini.keyboard.insert_text("\ny = 2\n")

    # The write is debounced, so give it a moment to land. Then read the
    # file back from a notebook of its own: this tab is showing a file, and
    # a file view has no insert seams to add a cell through.
    dewmini.wait_for_timeout(1500)
    dewmini.locator("#new-notebook").click()
    add_python_cell(dewmini, "print(open('notes.py').read())")
    shown = run_first_cell_and_wait(dewmini)
    # Exact, not a substring: the bug this guards against (DECISIONS_LOG.md
    # 7.125) left "y = 2" present too, just sitting under an unasked-for
    # "# %%" the file never had before dewmini opened it.
    assert shown == "x = 1\ny = 2"


def test_a_markerless_file_stays_markerless_after_editing(dewmini):
    """A plain script a cell's own open(name, "w") wrote — no "# %%" in
    it anywhere — keeps it that way after a round trip through the file
    view. Opening or editing it must not turn it into something that
    looks like a notebook export the reader never asked for."""
    write_workspace_file(dewmini, "plain.py", "x = 1\n")
    open_files_panel(dewmini)
    dewmini.locator(".dm-filelist-item-name", has_text="plain.py").click()
    dewmini.wait_for_selector(".dm-fileview-editor")

    # The marker must be absent the moment the file is only *opened*,
    # before any edit — parsePyCells()'s markerless fallback and
    # cellsToPercentText()'s single-cell case are meant to agree on this,
    # and the file view seeds itself from the latter.
    assert "# %%" not in dewmini.locator(".dm-fileview-editor .cm-content").inner_text()

    editor = dewmini.locator(".dm-fileview-editor .cm-content")
    editor.click()
    dewmini.keyboard.press("Control+End")
    dewmini.keyboard.insert_text("\ny = 2\n")
    dewmini.wait_for_timeout(1500)

    dewmini.locator("#new-notebook").click()
    add_python_cell(dewmini, "print(open('plain.py').read())")
    shown = run_first_cell_and_wait(dewmini)
    assert shown == "x = 1\ny = 2"


def test_a_multi_cell_file_keeps_its_markers(dewmini):
    """The marker is load-bearing the moment there is more than one
    cell to tell apart — omitting it there would merge two cells back
    into one on the next open."""
    write_workspace_file(dewmini, "multi.py", "# %%\nx = 1\n\n# %%\ny = 2\n")
    open_files_panel(dewmini)
    dewmini.locator(".dm-filelist-item-name", has_text="multi.py").click()
    dewmini.wait_for_selector(".dm-fileview-editor")
    dewmini.wait_for_timeout(1500)  # settle any debounced write before re-reading

    dewmini.locator("#new-notebook").click()
    add_python_cell(dewmini, "print(open('multi.py').read())")
    shown = run_first_cell_and_wait(dewmini)
    assert shown.count("# %%") == 2


def test_renaming_a_file_follows_the_tab_that_is_open_on_it(dewmini):
    """A tab left pointing at the old name would recreate it on the next key."""
    write_workspace_file(dewmini, "before.py", "x = 1\n")
    open_files_panel(dewmini)
    dewmini.locator(".dm-filelist-item-name", has_text="before.py").click()
    dewmini.wait_for_selector(".dm-fileview-editor")

    dewmini.once("dialog", lambda d: d.accept("after.py"))
    dewmini.locator(".dm-filelist-item-rename").first.click()
    dewmini.wait_for_selector(".dm-filelist-item-name:has-text('after.py')")

    names = dewmini.locator(".dm-filelist-item-name").all_inner_texts()
    assert "before.py" not in names


def test_a_file_dewmini_cannot_open_says_so_and_stays_put(dewmini):
    """Guessing how to read a .csv as code would break the data file."""
    write_workspace_file(dewmini, "readings.csv", "a,b\n1,2\n")
    open_files_panel(dewmini)

    tabs_before = dewmini.locator(".dm-tab").count()
    dewmini.locator(".dm-filelist-item-name", has_text="readings.csv").click()

    assert "opens .py, .ipynb and .html" in dewmini.locator("#dm-status").inner_text()
    assert dewmini.locator(".dm-tab").count() == tabs_before


def test_a_file_a_cell_writes_lands_in_the_workspace(dewmini):
    """A plain open(...) in a cell writes where the Files panel looks.

    Python's own working directory used to be a temporary folder nothing
    in the interface showed. A student writing open("notes.txt", "w") put
    the file somewhere they could not see, could not import from, and lost
    on the next reload, while the Files panel called itself a real
    filesystem a cell can write to.
    """
    add_python_cell(dewmini, "open('notes.txt', 'w').write('hello')\nprint('written')")
    assert run_first_cell_and_wait(dewmini) == "written"

    open_files_panel(dewmini)
    names = dewmini.locator(".dm-filelist-item-name").all_inner_texts()
    assert "notes.txt" in names


def test_a_file_a_cell_writes_can_then_be_imported(dewmini):
    """The workspace is both the working directory and on the import path."""
    add_python_cell(dewmini, "open('shapes.py', 'w').write('def area(r):\\n    return 3 * r * r\\n')\nprint('written')")
    assert run_first_cell_and_wait(dewmini) == "written"

    add_python_cell(dewmini, "import shapes\nprint(shapes.area(2))")
    assert run_first_cell_and_wait(dewmini, 1) == "12"


def test_the_project_is_on_the_left_and_the_reference_on_the_right(dewmini):
    """Files and variables dock left; the reference docks right."""
    dewmini.click("#dm-workbench-toggle")
    dewmini.click("#dm-library-toggle")

    workbench = dewmini.locator("#dm-workbench").bounding_box()
    library = dewmini.locator("#dm-library").bounding_box()
    assert workbench["x"] < library["x"], "files and variables belong on the left"

    # And the sections really are where the division says they are.
    assert dewmini.locator("#dm-workbench #settings-file-list").count() == 1
    assert dewmini.locator("#dm-workbench #dm-variables").count() == 1
    assert dewmini.locator("#dm-library #dm-reference-section").count() == 1


# --------------------------------------------------------------------- site


def test_an_html_file_in_the_workspace_opens_as_a_site(dewmini):
    """A .html opens split-screen: its own editor plus a live preview,
    not as a file view or as cells (planning/DEWMINI_WORKBENCH.md §10)."""
    write_workspace_file(dewmini, "index.html", "<h1>Hello site</h1>")
    open_files_panel(dewmini)

    dewmini.locator(".dm-filelist-item-name", has_text="index.html").click()
    dewmini.wait_for_selector(".dm-siteview")

    assert dewmini.locator(".dm-siteview-pane").count() == 3
    frame = dewmini.locator(".dm-siteview-frame").content_frame
    assert frame.locator("h1").text_content() == "Hello site"


def test_a_site_discovers_matching_css_and_js_files(dewmini):
    """No fixed three names — a same-base-name .css and .js beside the
    .html open with it, because a site can be built from nothing, not
    only from index.html/style.css/script.js."""
    write_workspace_file(dewmini, "page.css", "h1 { color: rebeccapurple; }")
    write_workspace_file(dewmini, "page.js", "document.querySelector('h1').textContent += '!';")
    write_workspace_file(dewmini, "page.html", "<h1>Hi</h1>")
    open_files_panel(dewmini)

    dewmini.locator(".dm-filelist-item-name", has_text="page.html").click()
    dewmini.wait_for_selector(".dm-siteview")

    panes = dewmini.locator(".dm-siteview-pane")
    assert "rebeccapurple" in panes.nth(1).locator(".cm-content").inner_text()
    assert "textContent" in panes.nth(2).locator(".cm-content").inner_text()

    frame = dewmini.locator(".dm-siteview-frame").content_frame
    assert frame.locator("h1").text_content() == "Hi!"
    assert frame.locator("h1").evaluate(
        "el => getComputedStyle(el).color"
    ) == "rgb(102, 51, 153)"


def test_a_site_with_no_css_or_js_still_opens(dewmini):
    """A lone .html is still a whole site — the CSS and JS panes are
    just empty, not an error and not a reason to refuse opening it."""
    write_workspace_file(dewmini, "lonely.html", "<p>Just me</p>")
    open_files_panel(dewmini)

    dewmini.locator(".dm-filelist-item-name", has_text="lonely.html").click()
    dewmini.wait_for_selector(".dm-siteview")

    panes = dewmini.locator(".dm-siteview-pane")
    assert panes.nth(1).locator(".cm-content").inner_text().strip() == ""
    assert panes.nth(2).locator(".cm-content").inner_text().strip() == ""
    frame = dewmini.locator(".dm-siteview-frame").content_frame
    assert frame.locator("p").text_content() == "Just me"


def test_editing_a_sites_html_updates_the_preview_live(dewmini):
    """Split-screen means the preview follows typing, not a separate
    Render press the way a Web cell needs — a site is what a reader
    keeps looking at while they work, not a one-shot question."""
    write_workspace_file(dewmini, "index.html", "<p>Before</p>")
    open_files_panel(dewmini)
    dewmini.locator(".dm-filelist-item-name", has_text="index.html").click()
    dewmini.wait_for_selector(".dm-siteview")

    editor = dewmini.locator(".dm-siteview-pane").nth(0).locator(".cm-content")
    editor.click()
    dewmini.keyboard.press("Control+A")
    dewmini.keyboard.insert_text("<p>After</p>")

    # Not el.contentDocument from the parent page's own JS: the sandboxed
    # iframe has no allow-same-origin, so it is a genuinely different,
    # opaque origin, and the parent cannot read into it that way (it just
    # sees null, forever). Playwright's own content_frame reaches inside
    # via the DevTools protocol instead, which real page script cannot do.
    frame = dewmini.locator(".dm-siteview-frame").content_frame
    expect(frame.locator("p")).to_have_text("After")


def test_editing_a_sites_css_writes_back_to_its_own_file(dewmini):
    """The CSS and JS halves each save to their own file, not into the
    HTML file or into localStorage alone."""
    write_workspace_file(dewmini, "index.html", "<h1>Hi</h1>")
    open_files_panel(dewmini)
    dewmini.locator(".dm-filelist-item-name", has_text="index.html").click()
    dewmini.wait_for_selector(".dm-siteview")

    css_editor = dewmini.locator(".dm-siteview-pane").nth(1).locator(".cm-content")
    css_editor.click()
    dewmini.keyboard.insert_text("h1 { color: gold; }")

    # Two debounces stack before this is durable: scheduleWorkspaceWrite()'s
    # own 600ms, then dewmini-fs.js's internal sync debounce on top of that
    # (the same reasoning the earlier standalone Site design noted, and
    # discarded along with it — DECISIONS_LOG.md 7.121).
    dewmini.wait_for_timeout(3000)

    dewmini.locator("#new-notebook").click()
    add_python_cell(dewmini, "print(open('index.css').read())")
    shown = run_first_cell_and_wait(dewmini)
    assert "gold" in shown


def test_a_site_survives_a_reload(dewmini, dewmini_url):
    """A site tab is still open, on the same three files, after a reload —
    the same durability every other workspace-backed tab already has."""
    write_workspace_file(dewmini, "index.html", "<h1>Hi</h1>")
    open_files_panel(dewmini)
    dewmini.locator(".dm-filelist-item-name", has_text="index.html").click()
    dewmini.wait_for_selector(".dm-siteview")
    dewmini.wait_for_timeout(3000)

    dewmini.goto(dewmini_url)
    dewmini.wait_for_selector(".dm-siteview")
    frame = dewmini.locator(".dm-siteview-frame").content_frame
    assert frame.locator("h1").text_content() == "Hi"


def test_the_cell_toolbar_hides_for_a_site_tab(dewmini):
    """Cells/File, Run all and the rest are about a notebook of Python
    cells, which a site tab does not have."""
    write_workspace_file(dewmini, "index.html", "<h1>Hi</h1>")
    open_files_panel(dewmini)
    dewmini.locator(".dm-filelist-item-name", has_text="index.html").click()
    dewmini.wait_for_selector(".dm-siteview")

    assert dewmini.locator("#run-all").is_hidden()
    assert dewmini.locator("#dm-view-cells").is_hidden()

    dewmini.locator(".dm-tab-label", has_text="Notebook").first.click()
    assert dewmini.locator("#run-all").is_visible()


# ---------------------------------------------------------------- cell types


def fresh_page(page, dewmini_url):
    """A page with truly empty storage — unlike the `dewmini` fixture,
    which seeds Web and SQL on for the rest of this suite's convenience
    (DECISIONS_LOG.md 7.122). The default-off behaviour can only be seen
    from a page that fixture never touched."""
    page.goto(dewmini_url)
    page.evaluate("localStorage.clear()")
    page.goto(dewmini_url)
    page.wait_for_selector(".dm-toolbar")
    return page


def open_cell_type_settings(page):
    page.click("#dl-settings-toggle")
    page.wait_for_selector("#dl-settings-cell-types")


def test_web_and_sql_default_off_javascript_defaults_on(page, dewmini_url):
    """A reader turns on what they mean to use, rather than finding
    every cell type dewmini knows about crowded onto every seam."""
    fresh_page(page, dewmini_url)
    buttons = page.locator(".dm-insert-btn").all_inner_texts()
    assert "Web" not in buttons
    assert "SQL" not in buttons
    assert "JS" in buttons


def test_turning_on_a_cell_type_adds_it_to_the_seam(page, dewmini_url):
    fresh_page(page, dewmini_url)
    open_cell_type_settings(page)
    page.click('.dl-seg[data-dm="celltype-web"] button[data-value="on"]')
    page.click("#dl-settings-close")

    assert "Web" in page.locator(".dm-insert-btn").all_inner_texts()


def test_turning_a_type_off_does_not_touch_a_cell_already_there(dewmini):
    """Only what a reader can *add* changes — a cell already in the
    notebook keeps showing and keeps running."""
    cell = _web_cell(dewmini, html="<p>Still here</p>")
    frame = cell.locator(".dm-html-frame").content_frame
    assert frame.locator("p").text_content() == "Still here"

    open_cell_type_settings(dewmini)
    dewmini.click('.dl-seg[data-dm="celltype-web"] button[data-value="off"]')
    dewmini.click("#dl-settings-close")

    assert dewmini.locator(".dm-cell-web").count() == 1
    assert "Web" not in dewmini.locator(".dm-insert-btn").all_inner_texts()
    assert cell.locator(".dm-html-frame").content_frame.locator("p").text_content() == "Still here"


def test_a_cell_type_toggle_survives_a_reload(dewmini, dewmini_url):
    open_cell_type_settings(dewmini)
    dewmini.click('.dl-seg[data-dm="celltype-sql"] button[data-value="off"]')
    dewmini.click("#dl-settings-close")

    dewmini.goto(dewmini_url)
    dewmini.wait_for_selector(".dm-toolbar")
    assert "SQL" not in dewmini.locator(".dm-insert-btn").all_inner_texts()


# ---------------------------------------------------- settings radiogroups


def open_texture_settings(page):
    page.click("#dl-settings-toggle")
    page.wait_for_selector('.dl-seg[data-texture="theme"]')


def test_the_theme_group_announces_itself_as_a_radiogroup(dewmini):
    """Every .dl-seg is a mutually-exclusive single-choice group, not a row
    of independent toggle buttons — DECISIONS_LOG.md 7.130."""
    open_texture_settings(dewmini)
    group = dewmini.locator('.dl-seg[data-texture="theme"]')
    expect(group).to_have_attribute("role", "radiogroup")

    buttons = group.locator("button")
    for i in range(buttons.count()):
        expect(buttons.nth(i)).to_have_attribute("role", "radio")

    # "auto" (system) is the default theme, so it starts out checked.
    expect(group.locator('button[data-value="system"]')).to_have_attribute("aria-checked", "true")
    expect(group.locator('button[data-value="light"]')).to_have_attribute("aria-checked", "false")


def test_arrow_right_moves_focus_and_selection_together(dewmini):
    open_texture_settings(dewmini)
    group = dewmini.locator('.dl-seg[data-texture="theme"]')
    group.locator('button[data-value="system"]').focus()

    dewmini.keyboard.press("ArrowRight")

    light = group.locator('button[data-value="light"]')
    expect(light).to_have_attribute("aria-checked", "true")
    expect(light).to_be_focused()
    expect(group.locator('button[data-value="system"]')).to_have_attribute("aria-checked", "false")


def test_arrow_right_wraps_from_the_last_option_to_the_first(dewmini):
    open_texture_settings(dewmini)
    group = dewmini.locator('.dl-seg[data-texture="theme"]')
    last = group.locator('button[data-value="dark"]')
    last.click()
    last.focus()

    dewmini.keyboard.press("ArrowRight")

    first = group.locator('button[data-value="system"]')
    expect(first).to_have_attribute("aria-checked", "true")
    expect(first).to_be_focused()


class TestStatusAnnouncer:
    """#dm-status is `role="status" aria-live="polite"` — a live region
    only announces on an actual text change, so running the same cell
    twice in a row, both times ending "Ran.", needs updateStatus()'s
    clear-then-set-on-next-tick to be heard the second time too."""

    def wait_for_status(self, page, text: str, timeout: int = 5_000):
        page.wait_for_function(
            "text => document.getElementById('dm-status').textContent === text",
            arg=text,
            timeout=timeout,
        )

    def test_running_the_same_cell_twice_announces_both_times(self, dewmini):
        page = dewmini
        add_python_cell(page, "print('hi')")
        run_first_cell_and_wait(page)
        self.wait_for_status(page, "Ran.")

        page.evaluate("document.getElementById('dm-status').textContent = 'sentinel'")
        run_first_cell_and_wait(page)
        self.wait_for_status(page, "Ran.")


# ------------------------------------------------------ site: console and Run


def open_site(page, html: str, js: str, name: str = "page") -> None:
    """A .html with a same-name .js beside it, opened as a site."""
    write_workspace_file(page, f"{name}.js", js)
    write_workspace_file(page, f"{name}.html", html)
    open_files_panel(page)
    page.locator(".dm-filelist-item-name", has_text=f"{name}.html").click()
    page.wait_for_selector(".dm-siteview")


def site_console_lines(page):
    return page.locator(".dm-siteview-console-line")


def test_a_sites_script_logs_and_errors_into_its_console(dewmini):
    """The console under the preview shows what the script printed and
    the error it raised, with the pane line the error came from, and a
    plain-language second line (DECISIONS_LOG.md 7.134)."""
    open_site(dewmini, "<h1>Hi</h1>", 'console.log("start", { a: 1 });\nnope();\nconsole.log("never");')
    lines = site_console_lines(dewmini)
    lines.nth(1).wait_for()
    assert lines.count() == 2
    assert lines.nth(0).inner_text() == 'start {"a":1}'
    assert "ReferenceError: nope is not defined (JavaScript, line 2)" in lines.nth(1).inner_text()
    assert "does not know a name called nope" in dewmini.locator(".dm-siteview-console-output .dl-error-hint").inner_text()


def test_a_sites_javascript_runs_on_run_not_on_typing(dewmini):
    """HTML and CSS stay live; the JavaScript pane waits for Run, and the
    preview keeps the last-run script until then."""
    open_site(dewmini, "<h1>Hi</h1>", 'console.log("first");')
    site_console_lines(dewmini).first.wait_for()
    assert site_console_lines(dewmini).first.inner_text() == "first"

    js_editor = dewmini.locator(".dm-siteview-pane").nth(2).locator(".cm-content")
    js_editor.click()
    dewmini.keyboard.press("Control+A")
    js_editor.fill('console.log("typed");')
    dewmini.wait_for_timeout(400)
    assert site_console_lines(dewmini).first.inner_text() == "first"

    # A live HTML edit redraws with the *last-run* script, not the typed one.
    html_editor = dewmini.locator(".dm-siteview-pane").nth(0).locator(".cm-content")
    html_editor.click()
    dewmini.keyboard.press("Control+A")
    html_editor.fill("<h1>Changed</h1>")
    frame = dewmini.locator(".dm-siteview-frame").content_frame
    frame.locator("h1", has_text="Changed").wait_for()
    site_console_lines(dewmini).first.wait_for()
    assert site_console_lines(dewmini).first.inner_text() == "first"

    dewmini.locator(".dm-siteview-run").click()
    dewmini.locator(".dm-siteview-console-line", has_text="typed").wait_for()
    assert site_console_lines(dewmini).count() == 1


def test_ctrl_enter_in_the_javascript_pane_runs_it(dewmini):
    open_site(dewmini, "<p>x</p>", 'console.log("first");')
    site_console_lines(dewmini).first.wait_for()
    js_editor = dewmini.locator(".dm-siteview-pane").nth(2).locator(".cm-content")
    js_editor.click()
    dewmini.keyboard.press("Control+A")
    js_editor.fill('console.log("keys");')
    js_editor.press("Control+Enter")
    dewmini.locator(".dm-siteview-console-line", has_text="keys").wait_for()


def test_go_to_line_selects_the_failing_line(dewmini):
    open_site(dewmini, "<p>x</p>", 'var a = 1;\nnope();')
    dewmini.locator(".dm-siteview-goto").first.wait_for()
    dewmini.locator(".dm-siteview-goto").first.click()
    assert dewmini.evaluate("() => window.getSelection().toString()") == "nope();"
