"""Editing a page where it stands, part two: a cell, a fold and a table
(assets/inpage-edit.js).

The first half is test_inpage_editor.py, and everything these tests stand on
(the small site, the fake GitHub, the `editing` fixture) is defined there.
The file is in two so CI can run the halves on separate machines: each test
loads a page in a fresh browser, which takes about five seconds, and one file
of forty-one was most of the browser job.
"""

from __future__ import annotations

from pathlib import Path

from test_inpage_editor import (  # noqa: F401  (pytest fixtures and helpers, imported)
    base_url,
    chromium,
    editing,
    leave,
    page_text,
    site,
    start,
    type_into,
)

DEWLAB = Path(__file__).resolve().parents[2]


def cell_save(page):
    page.click("#dl-edit-save")
    page.wait_for_function("document.getElementById('dl-edit-status').textContent.includes('pull/999')")


def test_a_cell_opens_with_its_id_fixed_and_its_code_in_a_code_editor(editing):
    page, fake, manifest = editing
    start(page)
    page.click("main#dl-body > .dl-cell")
    page.wait_for_selector(".dl-inplace-cell .cm-content")
    assert "id: only" in page.inner_text(".dl-cell-id")
    assert page.inner_text(".dl-inplace-cell .cm-content").splitlines()[0] == "hint: Try it."
    assert page.input_value(".dl-inplace-cell textarea") == "Look again."


def test_changing_a_cells_code_and_hint_changes_those_lines_of_the_file_and_nothing_else(editing):
    page, fake, manifest = editing
    start(page)
    page.click("main#dl-body > .dl-cell")
    page.wait_for_selector(".dl-inplace-cell .cm-content")
    page.click(".dl-inplace-cell .cm-content")
    page.keyboard.press("Control+End")
    page.keyboard.type("  # shows 1")
    page.fill(".dl-inplace-cell textarea", "Look harder.")
    leave(page)
    page.wait_for_function("document.getElementById('dl-edit-status').textContent.startsWith('1 block changed')")
    cell_save(page)
    assert fake.blobs[0] == fake.source.replace("print(1)\n```", "print(1)  # shows 1\n```").replace("Look again.", "Look harder.")


def test_a_cells_id_cannot_be_changed_and_the_block_stays_open_until_it_is_put_right(editing):
    page, fake, manifest = editing
    start(page)
    page.click("main#dl-body > .dl-cell")
    page.wait_for_selector(".dl-inplace-cell .cm-content")
    page.click(".dl-inplace-cell .cm-content")
    page.keyboard.press("Control+Home")
    page.keyboard.type("id: renamed\n")
    leave(page)
    page.wait_for_function("document.getElementById('dl-edit-status').textContent.includes('id cannot be changed')")
    assert page.is_visible(".dl-inplace-cell")
    assert page.is_disabled("#dl-edit-save")
    assert fake.blobs == []


def test_a_cell_opened_and_left_alone_is_not_an_edit(editing):
    page, fake, manifest = editing
    start(page)
    page.click("main#dl-body > .dl-cell")
    page.wait_for_selector(".dl-inplace-cell .cm-content")
    leave(page)
    page.wait_for_function("document.getElementById('dl-edit-status').textContent.startsWith('No changes')")
    assert page.evaluate("document.querySelectorAll('.dl-inplace-cell').length") == 0


def test_clicking_run_on_a_cell_while_editing_opens_the_editor_and_runs_nothing(editing):
    page, fake, manifest = editing
    start(page)
    runs = page.evaluate("document.querySelectorAll('.dl-cell .dl-cell-output:not(:empty)').length")
    page.click("main#dl-body > .dl-cell .dl-cell-runline", force=True)
    page.wait_for_selector(".dl-inplace-cell")
    assert page.evaluate("document.querySelectorAll('.dl-cell .dl-cell-output:not(:empty)').length") == runs


def test_an_edited_block_opens_again_when_clicked(editing):
    page, fake, manifest = editing
    start(page)
    type_into(page, "main#dl-body > p:nth-of-type(2)", " Added.")
    leave(page)
    page.click(".dl-inplace[data-edited]")
    page.wait_for_function("!document.querySelector('.dl-inplace[data-edited] .ProseMirror').getAttribute('contenteditable') === false || document.querySelector('.dl-inplace[data-edited] .ProseMirror').getAttribute('contenteditable') === 'true'")
    page.keyboard.press("Control+End")
    page.keyboard.type(" Again.")
    leave(page)
    page.click("#dl-edit-save")
    page.wait_for_function("document.getElementById('dl-edit-status').textContent.includes('pull/999')")
    assert fake.blobs[0] == fake.source.replace("Second paragraph.", "Second paragraph. Added. Again.")


def test_every_cell_in_the_repository_parses_and_goes_back_together_unchanged(editing):
    """inpage-cell.js against all the cells people have written, so a shape of
    cell it cannot cut apart is found here and not on a teacher's page."""
    import sys
    if str(DEWLAB) not in sys.path:
        sys.path.insert(0, str(DEWLAB))
    import source_map as sm

    blocks = []
    for path in sorted((DEWLAB / "tutorials").glob("*/*.md")):
        text = path.read_text()
        body = text.find("\n---", 3) + 4
        blocks += [text[body + b.start:body + b.end] for b in sm.blocks(text[body:]) if b.kind == "fence:cell"]
    page, fake, manifest = editing
    result = page.evaluate("""async (blocks) => {
        const m = await import('/assets/inpage-cell.js');
        const bad = [];
        for (const text of blocks) {
            const parsed = m.parseCellBlock(text);
            if (!parsed || m.buildCellBlock(parsed, parsed.parts.map((p) => p.text)) !== text) bad.push(text.slice(0, 80));
        }
        return bad;
    }""", blocks)
    assert len(blocks) > 1000
    assert result == []


def test_editing_opens_every_fold_and_stopping_closes_them_again(editing):
    page, fake, manifest = editing
    assert page.evaluate("document.querySelector('details.dl-hint').open") is False
    start(page)
    assert page.evaluate("document.querySelector('details.dl-hint').open") is True
    page.click("#dl-edit-toggle")
    page.wait_for_function("!document.body.classList.contains('dl-editing')")
    assert page.evaluate("document.querySelector('details.dl-hint').open") is False


def test_the_blocks_inside_a_fold_edit_like_the_page_around_it(editing):
    page, fake, manifest = editing
    start(page)
    type_into(page, "details.dl-hint > p", " Then the second.")
    leave(page)
    page.click("#dl-edit-save")
    page.wait_for_function("document.getElementById('dl-edit-status').textContent.includes('pull/999')")
    assert fake.blobs[0] == fake.source.replace("Try the first step.", "Try the first step. Then the second.")


def test_a_list_and_a_code_fence_inside_a_fold_are_editable(editing):
    page, fake, manifest = editing
    start(page)
    modes = page.evaluate("""[...document.querySelectorAll('details.dl-hint > [data-md]')]
        .map(n => [n.tagName.toLowerCase(), n.dataset.dlEdit])""")
    assert modes == [["summary", "summary"], ["p", "rich"], ["ul", "rich"], ["pre", "source"]]


def test_a_folds_title_edits_in_place_and_clicking_it_does_not_fold_it(editing):
    page, fake, manifest = editing
    start(page)
    page.click("details.dl-hint > summary")
    box = page.wait_for_selector("summary input.dl-inplace-summary")
    assert box.input_value() == "stuck?"
    assert page.evaluate("document.querySelector('details.dl-hint').open") is True
    box.fill("stuck? try this")
    leave(page)
    page.click("#dl-edit-save")
    page.wait_for_function("document.getElementById('dl-edit-status').textContent.includes('pull/999')")
    assert fake.blobs[0] == fake.source.replace("<summary>stuck?</summary>", "<summary>stuck? try this</summary>")


def test_a_code_fence_inside_a_fold_edits_as_its_markdown(editing):
    page, fake, manifest = editing
    start(page)
    page.click("details.dl-hint > pre")
    box = page.wait_for_selector("textarea.dl-inplace-source")
    assert box.input_value() == "```python\nx = 1\n```"
    box.fill("```python\nx = 2\n```")
    leave(page)
    page.click("#dl-edit-save")
    page.wait_for_function("document.getElementById('dl-edit-status').textContent.includes('pull/999')")
    assert fake.blobs[0] == fake.source.replace("x = 1", "x = 2")


def test_discarding_puts_a_changed_fold_title_back(editing):
    page, fake, manifest = editing
    start(page)
    page.click("details.dl-hint > summary")
    page.fill("summary input.dl-inplace-summary", "changed")
    leave(page)
    page.click("#dl-edit-discard")
    page.wait_for_function("document.getElementById('dl-edit-status').textContent.startsWith('No changes')")
    assert page.inner_text("details.dl-hint > summary") == "stuck?"


def test_a_tables_cells_each_edit_in_place_and_show_their_markdown(editing):
    page, fake, manifest = editing
    start(page)
    modes = page.evaluate("""[...document.querySelectorAll('main#dl-body > table td, main#dl-body > table th')]
        .map(n => n.dataset.dlEdit)""")
    assert modes == ["tablecell"] * 8
    page.click("main#dl-body > table tbody tr:nth-child(2) td:nth-child(1)")
    assert page.inner_text("main#dl-body > table tbody tr:nth-child(2) td:nth-child(1)") == "*three*"
    assert page.evaluate("document.activeElement.tagName") == "TD"


def test_changing_one_cell_changes_only_that_cell_and_keeps_the_padding(editing):
    page, fake, manifest = editing
    start(page)
    page.click("main#dl-body > table tbody tr:nth-child(1) td:nth-child(2)")
    page.keyboard.press("Control+A")
    page.keyboard.type("2")
    page.keyboard.press("Enter")
    page.wait_for_function("document.getElementById('dl-edit-status').textContent.startsWith('1 block changed')")
    page.click("#dl-edit-save")
    page.wait_for_function("document.getElementById('dl-edit-status').textContent.includes('pull/999')")
    assert fake.blobs[0] == fake.source.replace("| one  | two  |", "| one  | 2  |")


def test_an_empty_cell_can_be_filled_and_a_typed_pipe_is_escaped(editing):
    page, fake, manifest = editing
    start(page)
    page.click("main#dl-body > table tbody tr:nth-child(3) td:nth-child(1)")
    page.keyboard.type("a | b")
    page.keyboard.press("Enter")
    page.click("#dl-edit-save")
    page.wait_for_function("document.getElementById('dl-edit-status').textContent.includes('pull/999')")
    assert fake.blobs[0] == fake.source.replace("| | `a|b` |", "| a \\| b| `a|b` |")


def test_a_cell_opened_and_left_alone_is_not_an_edit_and_is_put_back(editing):
    page, fake, manifest = editing
    start(page)
    page.click("main#dl-body > table tbody tr:nth-child(2) td:nth-child(2)")
    leave(page)
    page.wait_for_function("document.getElementById('dl-edit-status').textContent.startsWith('No changes')")
    assert page.evaluate("document.querySelector('main#dl-body > table tbody tr:nth-child(2) td:nth-child(2) .dl-math') !== null")


def test_table_cells_are_found_in_the_markdown_by_their_text(editing):
    page, fake, manifest = editing
    result = page.evaluate("""async () => {
        const m = await import('/assets/inpage-table.js');
        const text = '| A | B |\\n|---|---|\\n| a \\\\| b | `x|y` |\\n|  | z |';
        const rows = m.parseTable(text);
        return [rows.map((r) => r.map((c) => text.slice(c.start, c.end))), m.parseTable('not a table'), m.cellText(' a | b\\n c ')];
    }""")
    assert result[0] == [["A", "B"], ["a \\| b", "`x|y`"], ["", "z"]]
    assert result[1] is None
    assert result[2] == "a \\| b c"
