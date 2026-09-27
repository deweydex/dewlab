"""Choose your project (DECISIONS_LOG 7.283), on the fixture's
`choosing-a-project` page: the cards and the table come before the
projects, the projects start closed, a card opens its project and nothing
else, the choice is remembered, and a project counts towards progress only
once one of its cells has run."""

from __future__ import annotations

import pytest

from test_compare import _open, _serve

PAGE = "tutorials/choosing-a-project.html"


@pytest.fixture
def tab(browser, base_url, site_dir):
    # _serve points the page at the Pyodide the fixture site serves.
    context, tab = _open(browser, f"{base_url}/{PAGE}", _serve(site_dir, standalone=False, path=PAGE),
                         page=PAGE)
    tab.evaluate("localStorage.clear()")
    tab.reload()
    tab.wait_for_function("globalThis.dewlab !== undefined", timeout=30_000)
    try:
        yield tab
    finally:
        context.close()


def closed(tab, key: str) -> bool:
    return tab.evaluate(
        f"document.getElementById('project-{key}').classList.contains('dl-project-closed')")


def test_the_cards_and_table_come_first_and_the_projects_start_closed(tab):
    assert tab.locator(".dl-project-grid .dl-project-card").count() == 2
    assert tab.locator(".dl-project-card-own").count() == 1
    assert tab.locator(".dl-project-table tbody tr").count() == 3
    assert "How fast do squares grow?" in tab.inner_text(".dl-project-grid")
    for key in ("sums", "squares", "own"):
        assert closed(tab, key)
    # Closed shows the heading, as a button, and hides the rest.
    assert tab.locator("#project-sums .dl-project-toggle").is_visible()
    assert not tab.locator("#project-sums .dl-cell").is_visible()
    assert tab.get_attribute("#project-sums .dl-project-toggle", "aria-expanded") == "false"


def test_a_card_opens_its_project_only_and_it_is_remembered(tab):
    tab.click(".dl-project-card[data-project='squares']")
    assert not closed(tab, "squares")
    assert closed(tab, "sums")
    assert tab.locator("#project-squares .dl-cell").is_visible()
    assert tab.get_attribute("#project-squares .dl-project-toggle", "aria-expanded") == "true"
    tab.reload()
    tab.wait_for_function("globalThis.dewlab !== undefined", timeout=30_000)
    assert not closed(tab, "squares")
    assert closed(tab, "sums")


def test_the_heading_opens_and_closes_and_the_back_link_returns(tab):
    tab.click("#project-sums .dl-project-toggle")
    assert not closed(tab, "sums")
    assert tab.get_attribute("#project-sums .dl-project-back a", "href") == "#dl-project-chooser"
    tab.click("#project-sums .dl-project-toggle")
    assert closed(tab, "sums")


def test_a_project_counts_towards_progress_once_started(tab):
    # Python boots on the first run, which can take a while.
    tab.evaluate("dewlab.runCell('shared-opening')")
    tab.wait_for_function("document.getElementById('dl-progress-summary').textContent.includes('1 of 1')",
                          timeout=240_000)
    tab.click(".dl-project-card[data-project='sums']")
    tab.evaluate("dewlab.runCell('project-sums-1')")
    tab.wait_for_function("document.getElementById('dl-progress-summary').textContent.includes('2 of 2')",
                          timeout=120_000)
