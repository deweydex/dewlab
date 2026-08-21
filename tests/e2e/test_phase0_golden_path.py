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
    assert any(h.endswith("/assets/tutorial-style.css") for h in hrefs)
    assert any(h.endswith("/assets/tutorial-runtime.js") for h in hrefs)

    # And the stylesheet actually applied, rather than 404ing quietly.
    background = page.eval_on_selector(
        "body", "el => getComputedStyle(el).backgroundColor"
    )
    assert background not in ("rgba(0, 0, 0, 0)", "")


def test_version_metadata_is_in_the_page(page):
    """Phase 2's compare-on-load reads this. It has to be there from Phase 0."""
    assert page.get_attribute("meta[name=tutorial-version]", "content") == "1"
    assert page.get_attribute("meta[name=tutorial-slug]", "content") == "phase0-harness"


def test_every_exec_cell_became_an_editor_with_line_numbers(page):
    cells = page.query_selector_all(".dl-cell")
    assert len(cells) == 7
    assert len(page.query_selector_all(".dl-cell .cm-editor")) == 7
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


def test_the_texture_panel_switches_theme_and_the_editors_follow(page):
    page.click("#dl-texture-toggle")
    page.click("#dl-texture .dl-seg[data-texture=theme] button[data-value=light]")
    light_keyword_colour = keyword_colour(page)

    page.click("#dl-texture .dl-seg[data-texture=theme] button[data-value=dark]")
    dark_keyword_colour = keyword_colour(page)

    assert page.get_attribute("html", "data-theme") == "dark"
    # The editor stays transparent by design, so the cell's own panel colour
    # shows through. What the theme switch changes is the syntax colours.
    assert dark_keyword_colour != light_keyword_colour

    page.click("#dl-texture .dl-seg[data-texture=font] button[data-value=mono]")
    assert page.get_attribute("html", "data-font") == "mono"


def test_texture_choices_survive_a_reload(page, base_url):
    page.click("#dl-texture-toggle")
    page.click("#dl-texture .dl-seg[data-texture=theme] button[data-value=dark]")
    page.reload()
    page.wait_for_selector("html[data-theme=dark]", timeout=5_000)
