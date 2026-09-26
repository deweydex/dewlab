"""The world switcher (#315), on the fixture's `choosing-a-world` page: a
shared cell, one task in two worlds (planets and pixels), each with a
number to guess, a shared cell after it, and a task written for the
planets world only.

The choice is per page and kept in the browser, each variant's cells have
their own ids, and what the page runs, lists and exports follows the
world on show."""

from __future__ import annotations

import json

import pytest

from contrast import AA_MINIMUM, contrast_ratio, parse_rgb
from test_compare import _open, _serve

PAGE = "tutorials/choosing-a-world.html"


@pytest.fixture
def tab(browser, base_url, site_dir):
    route = _serve(site_dir, standalone=False, path=PAGE)
    context, tab = _open(browser, f"{base_url}/{PAGE}", route, page=PAGE)
    tab.evaluate("localStorage.clear()")
    tab.reload()
    tab.wait_for_function("globalThis.dewlab !== undefined", timeout=30_000)
    try:
        yield tab
    finally:
        context.close()


def cell(tab, ident):
    return tab.locator(f".dl-cell[data-cell-id='{ident}']")


def choose(tab, world):
    tab.locator(f".dl-world-chooser input[value='{world}']").check()


def wait_for_output(tab, ident):
    tab.wait_for_function(
        f"""() => {{
          const el = document.querySelector(".dl-cell[data-cell-id='{ident}'] .dl-cell-runline");
          return el && /^Ran /.test(el.textContent);
        }}""",
        timeout=240_000,
    )


class TestChoosing:
    def test_the_page_starts_in_the_world_it_teaches_in(self, tab):
        chooser = tab.locator(".dl-world-chooser")
        assert chooser.is_visible()
        assert chooser.locator("input[value='planets']").is_checked()
        assert cell(tab, "world-task--planets").is_visible()
        assert cell(tab, "world-task--pixels").is_hidden()
        # The label naming each variant's world is for a page without
        # JavaScript; with the chooser on show it would only repeat it.
        assert tab.locator(".dl-world-label").first.is_hidden()

    def test_choosing_swaps_the_variants_and_is_remembered_for_the_page(self, tab):
        choose(tab, "pixels")
        assert cell(tab, "world-task--pixels").is_visible()
        assert cell(tab, "world-task--planets").is_hidden()
        # A task with no pixels variant shows the page's own world's.
        assert cell(tab, "one-world--planets").is_visible()
        # Cells every world shares stay.
        assert cell(tab, "world-start").is_visible() and cell(tab, "world-end").is_visible()
        tab.reload()
        tab.wait_for_function("globalThis.dewlab !== undefined", timeout=30_000)
        assert tab.locator(".dl-world-chooser input[value='pixels']").is_checked()
        assert cell(tab, "world-task--pixels").is_visible()

    def test_each_variant_counts_from_the_same_number(self, tab):
        def number(ident):
            return cell(tab, ident).locator(".dl-cell-pill-num").inner_text()
        assert number("world-start") == "Cell 1"
        assert number("world-task--planets") == "Cell 2"
        assert number("world-task--pixels") == "Cell 2"
        assert number("world-end") == "Cell 3"
        assert number("one-world--planets") == "Cell 4"

    def test_each_world_keeps_its_own_work(self, tab):
        planets = "globalThis.dewlab.cells.find((c) => c.id === 'world-task--planets')"
        pixels = "globalThis.dewlab.cells.find((c) => c.id === 'world-task--pixels')"
        tab.evaluate(f"{planets}.editor.setValue('print(\"mine, in planets\")')")
        choose(tab, "pixels")
        # A variant that started hidden still takes typing once shown.
        editor = cell(tab, "world-task--pixels").locator(".cm-content")
        editor.click()
        tab.keyboard.press("End")
        tab.keyboard.type("  # mine")
        choose(tab, "planets")
        assert tab.evaluate(f"{planets}.getCode()") == 'print("mine, in planets")'
        assert tab.evaluate(f"{pixels}.getCode()").endswith("# mine")
        tab.evaluate("globalThis.dewlab.saveNow()")
        saved = tab.evaluate("globalThis.dewlab.readSaved()")
        assert saved["world"] == "planets"
        codes = {c["task_id"]: c["student_code"] for c in saved["cells"]}
        assert codes["world-task--planets"] == 'print("mine, in planets")'
        assert codes["world-task--pixels"].endswith("# mine")


class TestWhatFollowsTheWorld:
    def test_running_everything_above_runs_the_world_on_show(self, tab):
        choose(tab, "pixels")
        last = cell(tab, "one-world--planets")
        last.locator(".dl-btn-more").click()
        last.locator("[data-run-menu='above']").click()
        wait_for_output(tab, "one-world--planets")
        assert cell(tab, "world-task--pixels").locator(".dl-output").inner_text().strip() == "3"
        assert cell(tab, "world-task--planets").locator(".dl-output").inner_text().strip() == ""
        assert cell(tab, "world-end").locator(".dl-output").inner_text().strip() == "11"

    def test_surprises_list_only_the_world_on_show(self, tab):
        tab.locator("#dl-predict-world-task--planets .dl-predict-value").fill("5")
        cell(tab, "world-task--planets").locator(".dl-btn-run").click()
        wait_for_output(tab, "world-task--planets")
        items = tab.locator(".dl-surprises li").all_inner_texts()
        assert items == ["Cell 2: you guessed 5, and it printed 263520."]
        choose(tab, "pixels")
        assert tab.locator(".dl-surprises").is_hidden()

    def test_the_notebook_has_the_chosen_world(self, tab):
        choose(tab, "pixels")
        with tab.expect_download() as download:
            tab.evaluate("globalThis.dewlab.downloadAsIpynb()")
        notebook = json.loads(open(download.value.path()).read())
        sources = ["".join(c["source"]) for c in notebook["cells"]]
        assert sources[0].endswith("World: Pixels")
        code = "\n".join(sources)
        assert "sprite" in code and "widths" not in code
        assert 'print("planets")' in code

    @pytest.mark.parametrize("scheme", ["light", "dark"])
    def test_the_choosers_muted_text_is_readable(self, tab, scheme):
        """Each world's line and the note under them are muted text on the
        chooser's own background, and meet AA in both schemes."""
        tab.emulate_media(color_scheme=scheme)
        for selector in (".dl-world-line", ".dl-world-note"):
            fg, bg = tab.evaluate(
                """(sel) => [getComputedStyle(document.querySelector(sel)).color,
                             getComputedStyle(document.querySelector(".dl-world-chooser"))
                               .backgroundColor]""",
                selector,
            )
            ratio = contrast_ratio(parse_rgb(fg), parse_rgb(bg))
            assert ratio >= AA_MINIMUM, f"{scheme}: {selector} {fg} on {bg} is {ratio:.2f}:1"

    def test_no_errors_on_the_page(self, tab):
        choose(tab, "pixels")
        choose(tab, "planets")
        assert tab.problems == []
