"""Widgets in the Notebook (7.268): a text box's value reaches Python in
the Worker, and a slider runs its own cell and survives a redraw. The
same page-side code as a tutorial page (assets/cell-widgets.js), driven
here through the Notebook's own engine."""

from __future__ import annotations

from test_dewmini_workbench import add_python_cell, dewmini, dewmini_url  # noqa: F401

OUTPUT = ".dm-cell-output"
STRIP = ".dm-cell .dl-slider-strip"


def run_first_cell(page) -> None:
    page.locator(".dm-cell .dm-icon-run").first.click()


def wait_for_output(page, text: str) -> None:
    page.wait_for_function(
        f"[...document.querySelectorAll({OUTPUT!r})].some(o => o.textContent.includes({text!r}))",
        timeout=120_000,
    )


def test_what_a_reader_types_reaches_the_next_run(dewmini):
    add_python_cell(dewmini, 'name = text_input("Name", value="Ada", id="name")\nprint("hello", name.value)')
    run_first_cell(dewmini)
    wait_for_output(dewmini, "hello Ada")

    dewmini.locator(f"{OUTPUT} input[type=text]").fill("Grace")
    run_first_cell(dewmini)
    wait_for_output(dewmini, "hello Grace")


def test_a_slider_runs_its_cell_and_survives_a_redraw(dewmini):
    add_python_cell(dewmini, 'amp = slider("Amp", 1, 5, value=2, id="amp")\nprint("amp is", amp.value)')
    run_first_cell(dewmini)
    wait_for_output(dewmini, "amp is 2")
    assert dewmini.locator(f"{STRIP} input[type=range]").count() == 1
    assert dewmini.locator(f"{OUTPUT} .dl-slider").count() == 0

    dewmini.locator(f"{STRIP} input[type=range]").focus()
    dewmini.keyboard.press("ArrowRight")
    wait_for_output(dewmini, "amp is 3")

    # Switching tabs redraws the cell; its slider comes back where it was.
    dewmini.click("#new-notebook")
    dewmini.locator(".dm-tab").first.click()
    dewmini.wait_for_selector(f"{STRIP} input[type=range]")
    assert dewmini.locator(f"{STRIP} input[type=range]").input_value() == "3"

    dewmini.locator(f"{STRIP} input[type=range]").focus()
    dewmini.keyboard.press("ArrowRight")
    wait_for_output(dewmini, "amp is 4")
    assert dewmini.locator(f"{STRIP} input[type=range]").count() == 1
