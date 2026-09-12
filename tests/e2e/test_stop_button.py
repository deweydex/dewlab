"""`dewlab.canStop()` is true only once cross-origin isolation has landed for this page, so every test here waits for it rather than assuming coi-serviceworker.js's first-visit reload already happened."""

from __future__ import annotations

import json


def cell_content(page, cell_id: str):
    return page.locator(f".dl-cell[data-cell-id='{cell_id}'] .dl-editor .cm-content")


def output_selector(cell_id: str) -> str:
    return f".dl-cell[data-cell-id='{cell_id}'] .dl-output"


def run_button(page, cell_id: str):
    return page.locator(f".dl-cell[data-cell-id='{cell_id}'] .dl-btn-run")


def js_string(text: str) -> str:
    return json.dumps(text)


def test_the_page_is_cross_origin_isolated(page):
    """Guards the precondition every test below assumes: without it, Stop silently falls back to a plain, un-stoppable Run and nothing else here would catch that."""
    page.wait_for_function("dewlab.canStop()", timeout=30_000)
    assert page.evaluate("window.crossOriginIsolated") is True
    assert page.evaluate("typeof SharedArrayBuffer") == "function"


def test_stopping_a_genuine_infinite_loop(page):
    page.wait_for_function("dewlab.canStop()", timeout=30_000)
    cell = cell_content(page, "plain-python")
    cell.click()
    page.keyboard.press("Control+End")
    page.keyboard.insert_text("\ncounter = 0\nwhile True:\n    counter += 1")

    btn = run_button(page, "plain-python")
    btn_selector = js_string(".dl-cell[data-cell-id='plain-python'] .dl-btn-run .dl-btn-label")
    btn.click()
    page.wait_for_function(
        f"document.querySelector({btn_selector}).textContent === 'Stop'",
        timeout=10_000,
    )

    page.wait_for_timeout(1_000)
    btn.click()  # the same button, now meaning Stop

    page.wait_for_function(
        f"document.querySelector({js_string(output_selector('plain-python'))}).innerText.includes('Stopped.')",
        timeout=20_000,
    )
    assert btn.locator(".dl-btn-label").inner_text() == "Run"
    assert not btn.is_disabled()


def test_a_stopped_cell_can_be_run_again(page):
    """The worker survives an interrupt rather than needing a reboot — run_cell() catches KeyboardInterrupt like any other exception."""
    page.wait_for_function("dewlab.canStop()", timeout=30_000)
    cell = cell_content(page, "plain-python")
    cell.click()
    page.keyboard.press("Control+End")
    page.keyboard.insert_text("\nwhile True:\n    pass")

    btn = run_button(page, "plain-python")
    btn_selector = js_string(".dl-cell[data-cell-id='plain-python'] .dl-btn-run .dl-btn-label")
    btn.click()
    page.wait_for_function(
        f"document.querySelector({btn_selector}).textContent === 'Stop'",
        timeout=10_000,
    )
    page.wait_for_timeout(1_000)
    btn.click()
    page.wait_for_function(
        f"document.querySelector({js_string(output_selector('plain-python'))}).innerText.includes('Stopped.')",
        timeout=20_000,
    )

    page.locator(".dl-cell[data-cell-id='plain-python'] .dl-btn-reset").click()
    cell.click()
    page.keyboard.press("Control+End")
    page.keyboard.insert_text("\n2 + 2")
    btn.click()
    page.wait_for_function(
        f"document.querySelector({js_string(output_selector('plain-python'))}).innerText.trim().endsWith('4')",
        timeout=15_000,
    )
