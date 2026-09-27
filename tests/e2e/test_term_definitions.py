"""Definitions on hover (#339, DECISIONS_LOG 7.273), on the fixture's
`third-page`, the one page here with a glossary: a term the author
italicised, and a later use marked `*cell*{.term}`, show their definitions
on hover, focus and tap; an unmarked use, an italic naming no term, and a
function name stay plain; and the Settings switch turns it off."""

from __future__ import annotations

import pytest

from test_compare import _open

PAGE = "tutorials/third-page.html"
VARIABLE = "#dl-body em.dl-def:text-is('variable')"
POPOVER = ".dl-def-popover"


@pytest.fixture
def tab(browser, base_url):
    context, tab = _open(browser, f"{base_url}/{PAGE}", page=PAGE)
    try:
        yield tab
    finally:
        context.close()


def test_only_the_marked_terms_are_marked(tab):
    marked = tab.eval_on_selector_all("#dl-body em.dl-def", "els => els.map(e => e.textContent)")
    assert sorted(marked) == ["cell", "variable"]
    plain = tab.eval_on_selector_all("#dl-body em:not(.dl-def)", "els => els.map(e => e.textContent)")
    assert "emphasis" in plain and "print" in plain
    # A later use is not an introduction: plain type, dotted line only.
    style = "el => getComputedStyle(el).fontStyle"
    assert tab.eval_on_selector("#dl-body em.dl-def:text-is('cell')", style) == "normal"
    assert tab.eval_on_selector(VARIABLE, style) == "italic"


def test_hover_shows_the_definition(tab):
    tab.hover(VARIABLE)
    tab.wait_for_selector(f"{POPOVER}:not([hidden])")
    assert "A name for a value" in tab.inner_text(POPOVER)
    tab.mouse.move(0, 0)
    tab.wait_for_selector(POPOVER, state="hidden")


def test_focus_describes_it_and_enter_opens_the_reference(tab):
    described = tab.eval_on_selector(
        VARIABLE, "el => document.getElementById(el.getAttribute('aria-describedby')).textContent"
    )
    assert "A name for a value" in described
    tab.focus(VARIABLE)
    tab.wait_for_selector(f"{POPOVER}:not([hidden])")
    tab.keyboard.press("Enter")
    tab.wait_for_selector("#dl-reference:not([hidden])")
    assert tab.input_value("#dl-reference-search") == "variable"


def test_a_tap_shows_it(browser, base_url):
    context = browser.new_context(has_touch=True, service_workers="block")
    try:
        tab = context.new_page()
        tab.goto(f"{base_url}/{PAGE}")
        tab.wait_for_function("globalThis.dewlab !== undefined", timeout=30_000)
        tab.tap("#dl-body em.dl-def:text-is('cell')")
        tab.wait_for_selector(f"{POPOVER}:not([hidden])")
        assert "piece of Python" in tab.inner_text(POPOVER)
    finally:
        context.close()


def test_the_setting_turns_it_off(tab):
    tab.evaluate("document.querySelector('[data-definitions] button[data-value=off]').click()")
    assert tab.locator("#dl-body em.dl-def").count() == 0
    assert tab.get_attribute("#dl-body em:text-is('variable')", "tabindex") is None
    tab.reload()
    tab.wait_for_function("globalThis.dewlab !== undefined", timeout=30_000)
    assert tab.locator("#dl-body em.dl-def").count() == 0
