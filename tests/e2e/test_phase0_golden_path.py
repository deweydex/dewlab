"""One Pyodide boot per session, so this is one file of e2e assertions
rather than a suite split across modules; fast tests live in
tests/test_tutorial_tools.py."""

from __future__ import annotations

import json

import pytest

from conftest import _open_settings_tab
from pathlib import Path

FIXTURE = Path(__file__).resolve().parent / "fixture" / "rendering-tour.md"


def output_selector(cell_id: str) -> str:
    return f".dl-cell[data-cell-id='{cell_id}'] .dl-output"


def js_string(text: str) -> str:
    """json.dumps, not repr — a selector with an apostrophe would otherwise
    become a silent syntax error inside wait_for_function."""
    return json.dumps(text)


def run(page, cell_id: str) -> str:
    selector = output_selector(cell_id)
    page.evaluate(f"dewlab.runCell({js_string(cell_id)})")
    page.wait_for_function(
        f"document.querySelector({js_string(selector)}).children.length > 0",
        timeout=60_000,
    )
    return page.inner_html(selector)


def test_the_page_loads_its_shared_assets_rather_than_inlining_them(page):
    """DECISIONS.md: shared external CSS/JS, not fully inlined."""
    hrefs = page.eval_on_selector_all(
        "link[rel=stylesheet], script[src]",
        "els => els.map(e => e.href || e.src)",
    )
    # The URL carries a content hash, so match the path and ignore the query.
    assert any("/assets/tutorial-style.css" in h for h in hrefs)
    assert any("/assets/tutorial-runtime.js" in h for h in hrefs)

    background = page.eval_on_selector(
        "body", "el => getComputedStyle(el).backgroundColor"
    )
    assert background not in ("rgba(0, 0, 0, 0)", "")


def test_every_exec_cell_became_an_editor_with_line_numbers(page):
    """Counted against the fixture rather than a fixed number, so adding a
    cell to rendering-tour.md does not fail a test that isn't about counting."""
    text = FIXTURE.read_text()
    expected = text.count("```python exec") + text.count("```sql exec")
    cells = page.query_selector_all(".dl-cell")
    assert len(cells) == expected
    assert len(page.query_selector_all(".dl-cell .cm-editor")) == expected
    assert page.query_selector(".dl-cell .cm-lineNumbers") is not None


def test_python_started_with_no_console_errors(page):
    assert page.is_hidden("#dl-status")
    assert page.inner_text("#dl-status-text") == ""
    assert page.problems == []


def test_plain_cell_prints_and_shows_its_last_expression(page):
    output = run(page, "plain-python")
    assert "counting: 0" in output
    assert "counting: 2" in output
    assert "1024" in output


def test_numpy_runs(page):
    output = run(page, "numpy-basics")
    assert "mean: 12.875" in output
    assert "25." in output  # 12.5 * 2


def test_a_sql_cells_select_renders_as_a_table_and_a_python_cell_can_read_it(page):
    """The editor holds real SQL text; the wrapper tutorial-runtime.js builds
    around it before it reaches Python is what makes _run_sql_cell() render
    this table, not anything in the fixture. The shared db is one
    connection, seeded once at boot, so a SQL cell's CREATE TABLE/INSERT is
    visible to a Python cell on the same page, the same guarantee dewmini's
    own SQL cell type already gives."""
    output = run(page, "sql-basics")
    assert "<table" in output
    assert "spider" in output
    assert "dog" in output
    assert "hen" not in output, "the WHERE legs > 2 filter should have excluded it"

    output = run(page, "sql-read-from-python")
    assert "<table" in output
    assert ">3<" in output, "3 rows were inserted"


def site_editor(page, name: str):
    return f".dl-site-editor[data-site-name='{name}']"


def test_a_site_editors_panes_match_what_the_fixture_declares(page):
    """Panes are optional; a page with a JS pane gets a Run button and a
    console, one without does not."""
    hero = site_editor(page, "hero")
    quiet = site_editor(page, "quiet")
    assert len(page.query_selector_all(f"{hero} .dl-site-pane")) == 3
    assert len(page.query_selector_all(f"{quiet} .dl-site-pane")) == 2
    assert page.query_selector(f"{hero} .dl-btn-site-run") is not None
    assert page.query_selector(f"{quiet} .dl-btn-site-run") is None
    assert page.query_selector(f"{hero} .dl-site-console-output") is not None
    assert page.query_selector(f"{quiet} .dl-site-console-output") is None


def test_html_and_css_are_live_but_javascript_waits_for_the_run_button(page):
    """The iframe is sandboxed without allow-same-origin, so this reads
    through Playwright's own frame handle — proving the live rebuild reached
    the page a reader would actually see, not just the editor's own DOM.
    HTML/CSS are live, JavaScript is a program that runs when asked, the
    same rule dewmini's own Site tab follows."""
    hero = site_editor(page, "hero")
    css_pane = f"{hero} .dl-site-pane[data-lang='css'] .cm-content"
    page.click(css_pane)
    page.keyboard.press("Control+a")
    page.keyboard.insert_text("#go { background: rgb(1, 2, 3); }")
    frame = page.query_selector(f"{hero} .dl-site-frame").content_frame()
    frame.wait_for_selector("#go")
    frame.wait_for_function(
        "() => getComputedStyle(document.querySelector('#go')).backgroundColor"
        " === 'rgb(1, 2, 3)'",
        timeout=10_000,
    )

    frame = page.query_selector(f"{hero} .dl-site-frame").content_frame()
    frame.wait_for_selector("#out")
    assert frame.inner_text("#out") == "not yet"

    page.click(f"{hero} .dl-btn-site-run")
    page.wait_for_function(
        "(sel) => document.querySelector(sel).textContent.includes('script loaded')",
        arg=f"{hero} .dl-site-console-output",
        timeout=10_000,
    )
    frame = page.query_selector(f"{hero} .dl-site-frame").content_frame()
    frame.click("#go")
    frame.wait_for_function(
        "() => document.querySelector('#out').textContent === 'clicked'",
        timeout=10_000,
    )


def test_a_site_editors_js_error_gets_a_friendly_hint(page):
    hero = site_editor(page, "hero")
    js_pane = f"{hero} .dl-site-pane[data-lang='js'] .cm-content"
    page.click(js_pane)
    page.keyboard.press("Control+a")
    page.keyboard.insert_text("undefinedThing.explode();")
    page.click(f"{hero} .dl-btn-site-run")
    console_selector = f"{hero} .dl-site-console-output"
    page.wait_for_function(
        "(sel) => document.querySelector(sel).querySelector('.dl-error') !== null",
        arg=console_selector,
        timeout=10_000,
    )
    html = page.inner_html(console_selector)
    assert "dl-error-hint" in html
    assert "dl-site-goto" in html


def test_clearing_a_site_editor_puts_its_starter_code_back_in_every_pane(page):
    hero = site_editor(page, "hero")
    html_pane = f"{hero} .dl-site-pane[data-lang='html'] .cm-content"
    page.click(html_pane)
    page.keyboard.press("Control+a")
    page.keyboard.insert_text("<p>edited</p>")

    page.once("dialog", lambda dialog: dialog.accept())
    page.click(f"{hero} .dl-btn-site-clear")
    assert "edited" not in page.eval_on_selector(html_pane, "el => el.textContent")


def test_declining_the_clear_confirmation_leaves_the_edit_in_place(page):
    hero = site_editor(page, "hero")
    html_pane = f"{hero} .dl-site-pane[data-lang='html'] .cm-content"
    page.click(html_pane)
    page.keyboard.press("Control+a")
    page.keyboard.insert_text("<p>edited</p>")

    page.once("dialog", lambda dialog: dialog.dismiss())
    page.click(f"{hero} .dl-btn-site-clear")
    assert "edited" in page.eval_on_selector(html_pane, "el => el.textContent")


def test_a_site_editors_edit_survives_a_reload(page):
    """The `siteEditors` array in saveNow()'s own record -- unlike a cell's
    output_html, cheap to rebuild, so only the pane text and whether Run had
    been pressed travel here, not the rendered preview itself."""
    hero = site_editor(page, "hero")
    css_pane = f"{hero} .dl-site-pane[data-lang='css'] .cm-content"
    page.click(css_pane)
    page.keyboard.press("Control+End")
    page.keyboard.insert_text("\n#go { color: red; }")
    page.wait_for_function("globalThis.dewlab.readSaved() !== null", timeout=10_000)

    page.reload()
    page.wait_for_function("globalThis.dewlab !== undefined", timeout=30_000)
    page.wait_for_function(
        "document.querySelectorAll('.dl-btn-run:not([disabled])').length > 0",
        timeout=240_000,
    )
    assert "color: red" in page.eval_on_selector(css_pane, "el => el.textContent")


def test_matplotlib_renders_a_figure_without_leaking_its_repr(page):
    """`plt.title(...)` returns a Text. A notebook prints it; dewlab doesn't."""
    output = run(page, "matplotlib-figure")
    assert 'src="data:image/png;base64,' in output
    height = page.eval_on_selector(
        f"{output_selector('matplotlib-figure')} img",
        "el => el.naturalHeight",
    )
    assert height > 50, "the figure decoded to a real image"
    assert "matplotlib" not in output
    assert "Text(" not in output
    assert "dl-repr" not in output


def test_plt_show_renders_the_figure_rather_than_warning(page):
    """The warning a non-interactive backend raises is noise under a plot that
    worked, and it arrives in the cell's error colour. It should not appear."""
    output = run(page, "matplotlib-show")
    assert "non-interactive" not in output
    assert "UserWarning" not in output
    assert "after the plot" in output
    height = page.eval_on_selector(
        f"{output_selector('matplotlib-show')} img",
        "el => el.naturalHeight",
    )
    assert height > 50, "the figure decoded to a real image"


def test_pandas_and_a_show_cell_share_one_namespace_and_render_correctly(page):
    """One run of pandas-table followed by tools-show covers the dataframe
    render, the shared namespace across cells, and show()/show_table()
    rendering, all from the same two cells. (check() went in #314.)"""
    output = run(page, "pandas-table")
    assert "<table" in output
    assert "Ireland" in output
    assert "Kenya" not in output, "the filter should have excluded Kenya"

    output = run(page, "tools-show")
    assert "<table" in output, "the later cell could not see df"
    assert "show() renders anything" in output
    assert "First three rows" in output
    assert "dl-check" not in output


def test_an_error_shows_the_students_line_and_does_not_stop_the_page(page):
    output = run(page, "error-traceback")
    assert "dl-error" in output
    assert "TypeError" in output
    assert "total += value" in output
    assert "eval_code_async" not in output
    assert "tutorial_tools" not in output

    output = run(page, "plain-python")
    assert "1024" in output


def test_a_text_box_and_a_dropdown_render_but_a_button_still_cannot(page):
    """A hosted page runs Pyodide in a Worker. `text_input` and `dropdown`
    work there — the page watches the control and posts each change back —
    but `button` has to call Python the moment it is clicked, with no cell
    running, and that needs a DOM reference the Worker cannot hold."""
    run(page, "tools-widgets")
    scope = output_selector("tools-widgets")
    assert page.locator(f"{scope} input[type=text]").count() == 1
    assert page.locator(f"{scope} select").count() == 1
    assert "button() needs a page running Pyodide on the main thread" in page.inner_text(scope)


def test_a_typed_value_reaches_the_worker_and_the_next_run_reads_it(page):
    """The whole round trip: the page's own listener posts what was typed,
    the Worker remembers it, and the next run sees it. Nothing here is
    synchronous — the value arrives between runs, not during one."""
    assert "answer is 42" in run(page, "tools-widget-roundtrip")
    box = page.locator(f"{output_selector('tools-widget-roundtrip')} input[type=text]")
    box.fill("7")
    assert "answer is 7" in run(page, "tools-widget-roundtrip")


def test_rerunning_a_cell_replaces_its_output_rather_than_appending(page):
    first = run(page, "plain-python")
    second = run(page, "plain-python")
    assert first.count("counting: 0") == second.count("counting: 0") == 1


def keyword_colour(page) -> str:
    return page.eval_on_selector(
        ".dl-cell .cm-keyword, .dl-cell .cm-line span",
        "el => getComputedStyle(el).color",
    )


def test_the_settings_panel_switches_theme_font_and_width(page):
    _open_settings_tab(page, "appearance")
    page.click("#dl-settings-reading .dl-seg[data-texture=theme] button[data-value=light]")
    light_keyword_colour = keyword_colour(page)

    page.click("#dl-settings-reading .dl-seg[data-texture=theme] button[data-value=dark]")
    dark_keyword_colour = keyword_colour(page)

    assert page.get_attribute("html", "data-theme") == "dark"
    # The editor stays transparent by design, so the cell's own panel colour
    # shows through. What the theme switch changes is the syntax colours.
    assert dark_keyword_colour != light_keyword_colour

    page.click("#dl-settings-reading .dl-seg[data-texture=font] button[data-value=mono]")
    assert page.get_attribute("html", "data-font") == "mono"

    page.click(
        '#dl-settings-reading .dl-seg[data-texture=width] button[data-value="56"]'
    )
    assert page.eval_on_selector(
        ":root", "el => getComputedStyle(el).getPropertyValue('--dl-line-width').trim()"
    ) == "56rem"
    # The slider and the presets are two views of one number, not two settings.
    assert page.input_value("#dl-texture-width") == "56"


def test_no_chrome_height_is_published_when_nothing_sits_above_the_page(page):
    """The status line and anchored jumps measure from this. With no bar
    above the page it has to read as zero, not the stylesheet's default —
    otherwise a jump lands a heading 6rem too low."""
    assert page.locator("#dl-chrome").count() == 0
    published = page.eval_on_selector(
        ":root", "el => getComputedStyle(el).getPropertyValue('--dl-chrome-h').trim()"
    )
    assert published == "0px"


def test_the_pages_own_rung_of_the_tree_jumps_to_a_section(page):
    page.click(".dl-crumb-level-4 > summary")
    first = page.get_attribute(".dl-crumb-level-4 a", "href")
    page.click(".dl-crumb-level-4 a")
    assert page.evaluate("location.hash") == first
    # Nothing sticky sits above the page now, so the heading lands at the top.
    top = page.eval_on_selector(first.lstrip("#") and f"[id='{first[1:]}']",
                                "el => el.getBoundingClientRect().top")
    assert top >= -1, "the heading landed above the top of the viewport"


def test_the_contents_page_never_scrolls_sideways(browser, base_url):
    # "The contents page" is all-tutorials.html (write_all_tutorials_page()
    # in build.py) — index.html is the home page, a separate page since
    # the redesign (DECISIONS_LOG.md 7.175) split the two apart.
    for width in (1400, 900, 390):
        context = browser.new_context(viewport={"width": width, "height": 800})
        tab = context.new_page()
        tab.goto(f"{base_url}/all-tutorials.html")
        tab.wait_for_selector(".dl-contents", timeout=10_000)
        overflow = tab.evaluate(
            "document.documentElement.scrollWidth - document.documentElement.clientWidth"
        )
        assert overflow <= 1, f"the page scrolls sideways at {width}px"
        context.close()


def test_every_box_on_the_map_is_a_link_to_a_tutorial(browser, base_url):
    context = browser.new_context(viewport={"width": 1400, "height": 900})
    tab = context.new_page()
    tab.goto(f"{base_url}/tree.html")
    tab.wait_for_selector("svg.dl-map", timeout=10_000)
    hrefs = tab.eval_on_selector_all(
        "svg.dl-map a.dl-map-node", "els => els.map(e => e.getAttribute('href'))"
    )
    assert hrefs, "the map has no nodes"
    tab.click("svg.dl-map a.dl-map-node")
    tab.wait_for_load_state()
    assert hrefs[0].split("/")[-1] in tab.url
    context.close()


def test_texture_choices_survive_a_reload(page, base_url):
    _open_settings_tab(page, "appearance")
    page.click("#dl-settings-reading .dl-seg[data-texture=theme] button[data-value=dark]")
    page.reload()
    page.wait_for_selector("html[data-theme=dark]", timeout=5_000)


def open_tree(browser, base_url, width=1400):
    context = browser.new_context(viewport={"width": width, "height": 900})
    tab = context.new_page()
    tab.goto(f"{base_url}/tree.html")
    tab.wait_for_function("globalThis.dewlabTree !== undefined", timeout=10_000)
    return context, tab


def test_the_tree_draws_every_topic_and_its_prerequisites(browser, base_url):
    context, tab = open_tree(browser, base_url)
    nodes = tab.eval_on_selector_all(".dl-tree-node", "e => e.length")
    edges = tab.eval_on_selector_all(".dl-tree-edge", "e => e.length")
    assert nodes == tab.evaluate("globalThis.dewlabTree.data.nodes.length")
    assert edges == tab.evaluate(
        "globalThis.dewlabTree.data.nodes.reduce((n, t) => n + t.needs.length, 0)"
    )
    context.close()


def test_choosing_a_topic_shows_what_it_is_and_lights_its_path(browser, base_url):
    context, tab = open_tree(browser, base_url)
    tab.click('.dl-tree-node[data-code="MIT-6.8a"]')
    panel = tab.inner_text("#dl-tree-detail")
    assert "Searching" in panel
    # inner_text is what the reader sees, and these headings are uppercased by
    # the stylesheet — so compare against that rather than against the source.
    assert "WHERE IT TURNS UP" in panel
    assert "NEEDS FIRST" in panel
    assert tab.eval_on_selector_all(".dl-tree-uses li", "e => e.length") >= 2
    assert tab.eval_on_selector_all(".dl-tree-edge.is-lit", "e => e.length") == 2
    context.close()


@pytest.mark.parametrize("code, taught", [("MIT-5.10", True), ("MIT-3.6", False)])
def test_a_topic_says_whether_it_is_taught(browser, base_url, code, taught):
    """The fixture claims MIT-5.10 in its matplotlib section, so that topic —
    and only a topic some tutorial claims — offers a way to read it; a topic
    nobody teaches says so instead."""
    context, tab = open_tree(browser, base_url)
    tab.click(f'.dl-tree-node[data-code="{code}"]')
    if taught:
        href = tab.get_attribute(".dl-tree-goto", "href")
        assert href and href.endswith("#matplotlib")
    else:
        assert tab.query_selector(".dl-tree-goto") is None
        assert "Not written yet" in tab.inner_text("#dl-tree-detail")
    context.close()


@pytest.mark.parametrize(
    "code, jump_selector, checks_opens_list",
    [("MIT-6.8a", ".dl-tree-jump", False), ("MIT-3.2", ".dl-tree-opens button", True)],
)
def test_clicking_a_related_topic_in_the_panel_moves_the_selection(
    browser, base_url, code, jump_selector, checks_opens_list
):
    """A prerequisite click and an "opens up" click both move the tree's
    selection off the topic that offered them; "opens up" also exercises the
    map's promise that somebody can ask "where do I go next?" — that is the
    edges pointing away from a topic rather than towards it."""
    context, tab = open_tree(browser, base_url)
    tab.click(f'.dl-tree-node[data-code="{code}"]')
    if checks_opens_list:
        panel = tab.inner_text("#dl-tree-detail")
        assert "OPENS UP" in panel
        opens = tab.eval_on_selector_all(".dl-tree-opens button", "e => e.map(b => b.textContent)")
        assert "Limits" in opens
    tab.click(jump_selector)
    assert tab.evaluate("globalThis.dewlabTree.chosen()") != code
    context.close()


def test_scrolling_zooms_and_dragging_moves(browser, base_url):
    context, tab = open_tree(browser, base_url)
    before = tab.evaluate("({...globalThis.dewlabTree.view})")

    tab.mouse.move(500, 500)
    tab.mouse.wheel(0, -240)
    tab.wait_for_timeout(120)
    zoomed = tab.evaluate("globalThis.dewlabTree.view.scale")
    assert zoomed > before["scale"]

    tab.mouse.move(700, 600)
    tab.mouse.down()
    tab.mouse.move(560, 520, steps=6)
    tab.mouse.up()
    tab.wait_for_timeout(120)
    moved = tab.evaluate("({...globalThis.dewlabTree.view})")
    assert (moved["x"], moved["y"]) != (before["x"], before["y"])
    context.close()


def test_fit_brings_the_whole_tree_back(browser, base_url):
    context, tab = open_tree(browser, base_url)
    tab.mouse.move(500, 500)
    for _ in range(4):
        tab.mouse.wheel(0, -240)
    tab.wait_for_timeout(120)
    tab.click("#dl-tree-fit")
    tab.wait_for_timeout(120)
    assert tab.evaluate("globalThis.dewlabTree.view.scale") <= 1.01
    context.close()


def test_the_zoom_buttons_do_something(browser, base_url):
    """They did not. The frame starts a pan on any press that is not a topic,
    and capturing the pointer swallowed the click — so the +, − and fit buttons
    were decorative, and nothing noticed because every test that used them
    happened to pass anyway."""
    context, tab = open_tree(browser, base_url)
    start = tab.evaluate("globalThis.dewlabTree.view.scale")
    tab.click("#dl-tree-in")
    tab.wait_for_timeout(120)
    bigger = tab.evaluate("globalThis.dewlabTree.view.scale")
    assert bigger > start
    tab.click("#dl-tree-out")
    tab.wait_for_timeout(120)
    assert tab.evaluate("globalThis.dewlabTree.view.scale") < bigger
    context.close()


def test_the_zoom_controls_do_not_cover_any_topic(browser, base_url):
    """They used to float over the canvas, which meant they sat on top of
    whichever topics happened to land under them and took the clicks meant for
    those topics — invisibly, and differently at every zoom level."""
    context, tab = open_tree(browser, base_url)
    overlapping = tab.evaluate("""() => {
      const controls = document.querySelector(".dl-tree-controls").getBoundingClientRect();
      return [...document.querySelectorAll(".dl-tree-node")].filter((node) => {
        const box = node.getBoundingClientRect();
        return box.left < controls.right && box.right > controls.left
            && box.top < controls.bottom && box.bottom > controls.top;
      }).map((n) => n.dataset.code);
    }""")
    assert overlapping == []
    context.close()


def test_fit_really_fits_on_a_phone(browser, base_url):
    """The zoom floor and the tree's width have to agree. They did not: a floor
    tuned against the old horizontal tree left the vertical one clipped off the
    right-hand edge of a phone, with "fit" unable to do anything about it."""
    context, tab = open_tree(browser, base_url, width=390)
    tab.click("#dl-tree-fit")
    tab.wait_for_timeout(150)
    drawn = tab.evaluate(
        "globalThis.dewlabTree.data.width * globalThis.dewlabTree.view.scale"
    )
    frame = tab.eval_on_selector("#dl-tree", "e => e.getBoundingClientRect().width")
    assert drawn <= frame, f"{drawn}px of tree in a {frame}px frame"
    context.close()


def test_the_tree_reads_downwards(browser, base_url):
    """Every node sits below everything it needs, on screen and not merely in
    the data — the one promise the vertical layout makes to a reader."""
    context, tab = open_tree(browser, base_url)
    upward = tab.evaluate("""() => {
      const by = new Map(globalThis.dewlabTree.data.nodes.map((n) => [n.code, n]));
      const wrong = [];
      for (const node of by.values()) {
        for (const need of node.needs) {
          const box = document.querySelector(`.dl-tree-node[data-code="${node.code}"]`);
          const above = document.querySelector(`.dl-tree-node[data-code="${need}"]`);
          if (!box || !above) continue;
          if (above.getBoundingClientRect().top >= box.getBoundingClientRect().top) {
            wrong.push(`${node.code} needs ${need}`);
          }
        }
      }
      return wrong;
    }""")
    assert upward == []
    context.close()


def test_the_tree_page_never_scrolls_sideways(browser, base_url):
    for width in (1400, 900, 390):
        context, tab = open_tree(browser, base_url, width)
        overflow = tab.evaluate(
            "document.documentElement.scrollWidth - document.documentElement.clientWidth"
        )
        assert overflow <= 1, f"the tree page scrolls sideways at {width}px"
        context.close()
