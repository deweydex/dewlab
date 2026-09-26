"""The predict block (#313), on the fixture's `predicting` page: a loop
that starts its total again each time round (a choice, with two hints
waiting for `unsure` and `guess differed`), a number, and a word.

Driven on both paths, like the comparison: the hosted page with Python in
a Worker, and the same page as a download would have it, on the main
thread."""

from __future__ import annotations

import pytest

from test_compare import _open, _serve

PAGE = "tutorials/predicting.html"


@pytest.fixture(params=["worker", "main-thread"])
def tab(request, browser, base_url, site_dir):
    route = _serve(site_dir, standalone=request.param == "main-thread", path=PAGE)
    context, tab = _open(browser, f"{base_url}/{PAGE}", route, page=PAGE)
    tab.evaluate("localStorage.clear()")
    try:
        yield tab
    finally:
        context.close()


def block(tab, cell):
    return tab.locator(f"#dl-predict-{cell}")


def run(tab, cell):
    tab.locator(f".dl-cell[data-cell-id='{cell}'] .dl-btn-run").click()
    wait_for_run(tab, cell)


def wait_for_run(tab, cell):
    tab.wait_for_function(
        f"""() => {{
          const el = document.querySelector(".dl-cell[data-cell-id='{cell}'] .dl-cell-runline");
          const label = document.querySelector(".dl-cell[data-cell-id='{cell}'] .dl-btn-run .dl-btn-label");
          return el && /^Ran /.test(el.textContent) && label && label.textContent === "Run";
        }}""",
        timeout=240_000,
    )


def choose(tab, cell, option):
    block(tab, cell).locator(f".dl-predict-options input[value='{option}']").check()


def sure(tab, cell, how):
    block(tab, cell).locator(f".dl-predict-sure-btn[data-sure='{how}']").click()


class TestPredict:
    def test_a_different_guess_sits_beside_the_output_and_is_never_called_wrong(self, tab):
        choose(tab, "predict-spending", 0)
        sure(tab, "predict-spending", "sure")
        run(tab, "predict-spending")
        after = block(tab, "predict-spending").locator(".dl-predict-after")
        assert after.is_visible()
        assert after.locator(".dl-predict-your").inner_text() == "12"
        assert after.locator(".dl-predict-output").inner_text() == "5"
        assert after.locator(".dl-predict-match").is_hidden()
        assert after.locator(".dl-predict-note[data-option='0']").is_visible()
        assert after.locator(".dl-predict-note[data-option='1']").is_hidden()
        assert after.locator(".dl-predict-which").is_visible()
        text = block(tab, "predict-spending").inner_text().lower()
        for word in ("wrong", "incorrect", "not yet", "correct"):
            assert word not in text

    def test_a_different_guess_brings_the_hint_that_waits_for_it(self, tab):
        choose(tab, "predict-spending", 0)
        run(tab, "predict-spending")
        assert tab.locator("#dl-staged-predict-spending-1").is_visible()
        assert tab.locator("#dl-staged-predict-spending-0").is_hidden()

    def test_a_matching_guess_may_be_confirmed(self, tab):
        choose(tab, "predict-spending", 1)
        run(tab, "predict-spending")
        after = block(tab, "predict-spending").locator(".dl-predict-after")
        assert after.locator(".dl-predict-match").is_visible()
        assert after.locator(".dl-predict-note[data-option='1']").is_visible()
        assert tab.locator(".dl-surprises").is_hidden()

    def test_not_sure_yet_opens_the_first_hint_and_offers_two_ways_on(self, tab):
        sure(tab, "predict-spending", "unsure")
        route = block(tab, "predict-spending").locator(".dl-predict-unsure")
        assert route.is_visible()
        assert route.locator(".dl-predict-hint-open").is_visible()
        first = tab.locator("#dl-staged-predict-spending-0")
        assert first.is_visible()
        assert first.evaluate("el => el.open")
        route.locator(".dl-predict-run").click()
        wait_for_run(tab, "predict-spending")
        after = block(tab, "predict-spending").locator(".dl-predict-after")
        assert after.locator(".dl-predict-your").inner_text() == "no guess"
        assert after.locator(".dl-predict-which").is_visible()

    def test_surprises_list_the_differences_and_the_unsure(self, tab):
        choose(tab, "predict-spending", 0)
        run(tab, "predict-spending")
        sure(tab, "predict-number", "unsure")
        surprises = tab.locator(".dl-surprises")
        assert surprises.is_visible()
        items = surprises.locator("li").all_inner_texts()
        assert items == ["Cell 1: you guessed 12, and it printed 5.",
                         "Cell 2: you were not sure yet."]

    def test_a_number_is_compared_as_a_number(self, tab):
        block(tab, "predict-number").locator(".dl-predict-value").fill("1,024")
        run(tab, "predict-number")
        assert block(tab, "predict-number").locator(".dl-predict-match").is_visible()
        block(tab, "predict-number").locator(".dl-predict-value").fill("1000")
        run(tab, "predict-number")
        assert block(tab, "predict-number").locator(".dl-predict-match").is_hidden()

    def test_case_counts_in_a_word(self, tab):
        block(tab, "predict-word").locator(".dl-predict-value").fill("sea")
        run(tab, "predict-word")
        assert block(tab, "predict-word").locator(".dl-predict-match").is_hidden()
        block(tab, "predict-word").locator(".dl-predict-value").fill("SEA")
        run(tab, "predict-word")
        assert block(tab, "predict-word").locator(".dl-predict-match").is_visible()

    def test_a_prediction_is_saved_with_its_cell_and_comes_back(self, tab):
        choose(tab, "predict-spending", 0)
        sure(tab, "predict-spending", "hunch")
        run(tab, "predict-spending")
        saved = tab.evaluate("globalThis.dewlab.readSaved()")
        cell = next(c for c in saved["cells"] if c["task_id"] == "predict-spending")
        assert cell["prediction"]["guess"] == {"option": 0, "text": "12"}
        assert cell["prediction"]["sure"] == "hunch"
        assert cell["prediction"]["outcome"]["output"] == "5"
        tab.reload()
        tab.wait_for_function("globalThis.dewlab !== undefined", timeout=30_000)
        assert block(tab, "predict-spending").locator("input[value='0']").is_checked()
        pressed = block(tab, "predict-spending").locator(".dl-predict-sure-btn[aria-pressed='true']")
        assert pressed.get_attribute("data-sure") == "hunch"
        assert block(tab, "predict-spending").locator(".dl-predict-output").inner_text() == "5"
        assert tab.locator(".dl-surprises li").count() == 1

    def test_no_errors_on_the_page(self, tab):
        choose(tab, "predict-spending", 0)
        run(tab, "predict-spending")
        assert tab.problems == []
