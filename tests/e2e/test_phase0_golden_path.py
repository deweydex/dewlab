"""Phase 0's golden path, in a real browser against a real Pyodide.

BUILD_PLAN.md's Phase 0 asks for one thing to be true before anything else is
built: that the shell template loads the shared assets, that
`loadPackage(['numpy', 'pandas', 'matplotlib'])` succeeds with no micropip step,
and that a plain `exec` cell renders its output underneath itself. That is what
this file checks, plus the widget bridge that was built on top of it.

Slow by nature — one Pyodide boot for the session — so it is one file of
end-to-end assertions rather than a suite. The fast tests live next door in
tests/test_tutorial_tools.py.
"""

from __future__ import annotations

import json
from pathlib import Path

FIXTURE = Path(__file__).resolve().parent / "fixture" / "rendering-tour.md"


def output_selector(cell_id: str) -> str:
    return f".dl-cell[data-cell-id='{cell_id}'] .dl-output"


def js_string(text: str) -> str:
    """A JavaScript string literal. json.dumps quotes and escapes correctly;
    Python's repr does not, and a selector containing an apostrophe silently
    becomes a syntax error inside wait_for_function."""
    return json.dumps(text)


def run(page, cell_id: str) -> str:
    """Run one cell and return the HTML its output area ended up with."""
    selector = output_selector(cell_id)
    page.evaluate(f"dewlab.runCell({js_string(cell_id)})")
    page.wait_for_function(
        f"document.querySelector({js_string(selector)}).children.length > 0",
        timeout=60_000,
    )
    return page.inner_html(selector)


# --------------------------------------------------------------- the shell


def test_the_page_loads_its_shared_assets_rather_than_inlining_them(page):
    """DECISIONS.md: shared external CSS/JS, not fully inlined."""
    hrefs = page.eval_on_selector_all(
        "link[rel=stylesheet], script[src]",
        "els => els.map(e => e.href || e.src)",
    )
    # The URL carries a content hash, so match the path and ignore the query.
    assert any("/assets/tutorial-style.css" in h for h in hrefs)
    assert any("/assets/tutorial-runtime.js" in h for h in hrefs)

    # And the stylesheet actually applied, rather than 404ing quietly.
    background = page.eval_on_selector(
        "body", "el => getComputedStyle(el).backgroundColor"
    )
    assert background not in ("rgba(0, 0, 0, 0)", "")


def test_version_metadata_is_in_the_page(page):
    """Phase 2's compare-on-load reads this. It has to be there from Phase 0."""
    assert page.get_attribute("meta[name=tutorial-version]", "content") == "2026.08.23.1"
    assert page.get_attribute("meta[name=tutorial-slug]", "content") == "rendering-tour"


def test_every_exec_cell_became_an_editor_with_line_numbers(page):
    """One editor per exec cell in the fixture, and no editor without a cell.

    Counted against the fixture rather than a fixed number, so adding a cell to
    rendering-tour.md does not fail a test that is not about counting."""
    expected = FIXTURE.read_text().count("```python exec")
    cells = page.query_selector_all(".dl-cell")
    assert len(cells) == expected
    assert len(page.query_selector_all(".dl-cell .cm-editor")) == expected
    # Line numbers are one of the affordances DECISIONS.md calls free.
    assert page.query_selector(".dl-cell .cm-lineNumbers") is not None


def test_python_started_with_no_console_errors(page):
    assert page.inner_text("#dl-status") == ""
    assert page.problems == []


# ------------------------------------------------------- the execution path


def test_plain_cell_prints_and_shows_its_last_expression(page):
    output = run(page, "plain-python")
    assert "counting: 0" in output
    assert "counting: 2" in output
    assert "1024" in output


def test_numpy_runs(page):
    output = run(page, "numpy-basics")
    assert "mean: 12.875" in output
    assert "25." in output  # 12.5 * 2


def test_pandas_dataframe_renders_as_a_table(page):
    output = run(page, "pandas-table")
    assert "<table" in output
    assert "Ireland" in output
    assert "Kenya" not in output, "the filter should have excluded Kenya"


def test_matplotlib_renders_a_figure_beneath_the_cell(page):
    output = run(page, "matplotlib-figure")
    assert 'src="data:image/png;base64,' in output
    height = page.eval_on_selector(
        f"{output_selector('matplotlib-figure')} img",
        "el => el.naturalHeight",
    )
    assert height > 50, "the figure decoded to a real image"


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


def test_a_plot_does_not_leak_matplotlib_object_reprs(page):
    """`plt.title(...)` returns a Text. A notebook prints it; dewlab doesn't."""
    output = run(page, "matplotlib-figure")
    assert "matplotlib" not in output
    assert "Text(" not in output
    assert "dl-repr" not in output


def test_a_cell_ending_in_check_does_not_print_a_bare_bool(page):
    """The cell's last line is a failing check. Its verdict is the last thing
    shown — not a bare `False` underneath saying the same in worse words."""
    run(page, "pandas-table")
    output = run(page, "tools-show-check")
    assert "dl-check-fail" in output

    last_class = page.eval_on_selector(
        output_selector("tools-show-check"),
        "el => el.lastElementChild.className",
    )
    assert "dl-check" in last_class, f"cell ended with {last_class!r}"


def test_cells_share_one_namespace_in_document_order(page):
    """The notebook model: a later cell sees what an earlier one defined."""
    run(page, "pandas-table")  # defines df
    output = run(page, "tools-show-check")
    assert "<table" in output, "the later cell could not see df"


def test_an_error_shows_the_students_own_line_not_dewlabs_plumbing(page):
    output = run(page, "error-traceback")
    assert "dl-error" in output
    assert "TypeError" in output
    assert "total += value" in output
    assert "eval_code_async" not in output
    assert "tutorial_tools" not in output


def test_an_error_does_not_stop_the_page(page):
    run(page, "error-traceback")
    output = run(page, "plain-python")
    assert "1024" in output


# ------------------------------------------------------- the widget bridge


def test_show_and_show_table_and_check_render(page):
    run(page, "pandas-table")
    output = run(page, "tools-show-check")
    assert "show() renders anything" in output
    assert "First three rows" in output
    assert "dl-check-pass" in output
    assert "dl-check-fail" in output
    assert output.count("dl-check-pass") == 2, "0.1 + 0.2 should pass against 0.3"


def test_widgets_render_and_the_button_calls_back(page):
    run(page, "tools-widgets")
    scope = output_selector("tools-widgets")

    page.fill(f"{scope} input[type=text]", "Ada")
    page.select_option(f"{scope} select", "imperial")
    page.click(f"{scope} .dl-widget button")

    page.wait_for_function(
        f"document.querySelector({js_string(scope)}).innerText.includes('Hello Ada')",
        timeout=15_000,
    )
    assert "using imperial units" in page.inner_text(scope)


def test_rerunning_a_cell_keeps_what_the_student_typed(page):
    """A re-run rebuilds the widgets. It must not silently discard the input."""
    run(page, "tools-widgets")
    scope = output_selector("tools-widgets")

    page.fill(f"{scope} input[type=text]", "Grace")
    page.select_option(f"{scope} select", "imperial")

    run(page, "tools-widgets")

    assert page.input_value(f"{scope} input[type=text]") == "Grace"
    assert page.eval_on_selector(f"{scope} select", "el => el.value") == "imperial"


def test_rerunning_a_cell_replaces_its_output_rather_than_appending(page):
    first = run(page, "plain-python")
    second = run(page, "plain-python")
    assert first.count("counting: 0") == second.count("counting: 0") == 1


# ---------------------------------------------------------- texture panel


def keyword_colour(page) -> str:
    return page.eval_on_selector(
        ".dl-cell .cm-keyword, .dl-cell .cm-line span",
        "el => getComputedStyle(el).color",
    )


def test_the_settings_panel_switches_theme_and_the_editors_follow(page):
    page.click("#dl-settings-toggle")
    page.click("#dl-settings-texture .dl-seg[data-texture=theme] button[data-value=light]")
    light_keyword_colour = keyword_colour(page)

    page.click("#dl-settings-texture .dl-seg[data-texture=theme] button[data-value=dark]")
    dark_keyword_colour = keyword_colour(page)

    assert page.get_attribute("html", "data-theme") == "dark"
    # The editor stays transparent by design, so the cell's own panel colour
    # shows through. What the theme switch changes is the syntax colours.
    assert dark_keyword_colour != light_keyword_colour

    page.click("#dl-settings-texture .dl-seg[data-texture=font] button[data-value=mono]")
    assert page.get_attribute("html", "data-font") == "mono"


def test_the_width_presets_set_the_measure(page):
    page.click("#dl-settings-toggle")
    page.click(
        '#dl-settings-texture .dl-seg[data-texture=width] button[data-value="56"]'
    )
    assert page.eval_on_selector(
        ":root", "el => getComputedStyle(el).getPropertyValue('--dl-line-width').trim()"
    ) == "56rem"
    # The slider and the presets are two views of one number, not two settings.
    assert page.input_value("#dl-texture-width") == "56"


def test_the_minimal_header_is_shorter_and_keeps_every_link(page):
    def chrome_height():
        return page.eval_on_selector(".dl-chrome", "el => el.getBoundingClientRect().height")

    def links():
        return page.eval_on_selector_all(".dl-nav-top a", "els => els.map(e => e.href)")

    full_height, full_links = chrome_height(), links()

    page.click("#dl-settings-toggle")
    page.click("#dl-settings-texture .dl-seg[data-texture=header] button[data-value=minimal]")
    page.keyboard.press("Escape")

    assert page.get_attribute("html", "data-header") == "minimal"
    assert chrome_height() < full_height, "minimal should be shorter, that is the point"
    assert links() == full_links, "minimal hides nothing — it only takes less room"


def test_the_chrome_height_is_published_for_everything_below_it(page):
    """The status line, the settings panel and anchored jumps all measure from
    this. A wrong value puts a heading underneath the header."""
    published = page.eval_on_selector(
        ":root", "el => getComputedStyle(el).getPropertyValue('--dl-chrome-h').trim()"
    )
    measured = page.eval_on_selector(".dl-chrome", "el => el.getBoundingClientRect().height")
    assert abs(float(published.replace("px", "")) - measured) <= 1


def test_the_contents_list_jumps_to_a_section(page):
    page.click(".dl-toc > summary")
    first = page.get_attribute(".dl-toc nav a", "href")
    page.click(".dl-toc nav a")
    assert page.evaluate("location.hash") == first
    # The sticky chrome must not be sitting on top of the heading it landed on.
    top = page.eval_on_selector(first.lstrip("#") and f"[id='{first[1:]}']",
                                "el => el.getBoundingClientRect().top")
    chrome = page.eval_on_selector(".dl-chrome", "el => el.getBoundingClientRect().bottom")
    assert top >= chrome - 1, "the heading landed underneath the sticky header"


def test_the_contents_page_never_scrolls_sideways(browser, base_url):
    """It carries an introduction and a list now, and neither is wide — but the
    rule is worth holding onto whatever the page contains."""
    for width in (1400, 900, 390):
        context = browser.new_context(viewport={"width": width, "height": 800})
        tab = context.new_page()
        tab.goto(f"{base_url}/index.html")
        tab.wait_for_selector(".dl-contents", timeout=10_000)
        overflow = tab.evaluate(
            "document.documentElement.scrollWidth - document.documentElement.clientWidth"
        )
        assert overflow <= 1, f"the page scrolls sideways at {width}px"
        context.close()


def test_every_box_on_the_map_is_a_link_to_a_tutorial(browser, base_url):
    """The tutorial map lives on the tree page now, under the topic tree."""
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
    page.click("#dl-settings-toggle")
    page.click("#dl-settings-texture .dl-seg[data-texture=theme] button[data-value=dark]")
    page.reload()
    page.wait_for_selector("html[data-theme=dark]", timeout=5_000)


# ------------------------------------------------------------- the topic tree

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
    tab.click('.dl-tree-node[data-code="MIT-6.8"]')
    panel = tab.inner_text("#dl-tree-detail")
    assert "Searching and sorting" in panel
    # inner_text is what the reader sees, and these headings are uppercased by
    # the stylesheet — so compare against that rather than against the source.
    assert "WHERE IT TURNS UP" in panel
    assert "NEEDS FIRST" in panel
    assert tab.eval_on_selector_all(".dl-tree-uses li", "e => e.length") >= 2
    # What it needs and what needs it. Divide and conquer used to hang off this
    # one; it now sits beside it, taught inside searching and inside sorting
    # rather than before or after either — so only one edge runs backward, to
    # iterating by index. The second lit edge runs forward: CMPS-LO5
    # (algorithmic complexity, not yet taught) names MIT-6.8 as a prerequisite
    # in topics.yaml, and an arrow into an untaught topic is exactly what the
    # map is for — see topics.yaml's own docstring on `needs`.
    assert tab.eval_on_selector_all(".dl-tree-edge.is-lit", "e => e.length") == 2
    context.close()


def test_a_topic_that_is_taught_links_to_the_tutorial(browser, base_url):
    """The fixture claims MIT-5.10 in its matplotlib section, so that topic —
    and only a topic some tutorial claims — offers a way to read it."""
    context, tab = open_tree(browser, base_url)
    tab.click('.dl-tree-node[data-code="MIT-5.10"]')
    href = tab.get_attribute(".dl-tree-goto", "href")
    assert href and href.endswith("#matplotlib")
    context.close()


def test_a_topic_nobody_teaches_says_so_instead(browser, base_url):
    context, tab = open_tree(browser, base_url)
    tab.click('.dl-tree-node[data-code="MIT-3.6"]')
    assert tab.query_selector(".dl-tree-goto") is None
    assert "Not written yet" in tab.inner_text("#dl-tree-detail")
    context.close()


def test_a_prerequisite_in_the_panel_moves_the_selection(browser, base_url):
    context, tab = open_tree(browser, base_url)
    tab.click('.dl-tree-node[data-code="MIT-6.8"]')
    tab.click(".dl-tree-jump")
    assert tab.evaluate("globalThis.dewlabTree.chosen()") != "MIT-6.8"
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


def test_a_topic_says_what_it_opens_up(browser, base_url):
    """The map exists so somebody can ask "where do I go next?", and that is the
    edges pointing away from a topic rather than towards it."""
    context, tab = open_tree(browser, base_url)
    tab.click('.dl-tree-node[data-code="MIT-3.2"]')
    panel = tab.inner_text("#dl-tree-detail")
    assert "OPENS UP" in panel
    opens = tab.eval_on_selector_all(".dl-tree-opens button", "e => e.map(b => b.textContent)")
    assert "Limits" in opens
    # And choosing one of them moves the selection, same as a prerequisite does.
    tab.click(".dl-tree-opens button")
    assert tab.evaluate("globalThis.dewlabTree.chosen()") != "MIT-3.2"
    context.close()


def test_the_tree_page_never_scrolls_sideways(browser, base_url):
    for width in (1400, 900, 390):
        context, tab = open_tree(browser, base_url, width)
        overflow = tab.evaluate(
            "document.documentElement.scrollWidth - document.documentElement.clientWidth"
        )
        assert overflow <= 1, f"the tree page scrolls sideways at {width}px"
        context.close()
