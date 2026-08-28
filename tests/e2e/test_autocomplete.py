"""Code completion, hover docs, and signature help inside a cell, in a real
browser.

Static completion — keywords, builtins, and whatever a student has already
typed in the cell — comes from `@codemirror/lang-python`'s own
`globalCompletion`/`localCompletionSource`, wired in
vendor-src/codemirror-entry.js. It works before Pyodide has finished
booting, which the first class below checks by never running a cell at all.

Live-namespace completion (`pageNamesCompletion`, assets/tutorial-runtime.js)
reads whatever names are actually defined in tutorial_tools._page_globals
right now, and hover docs / signature help (`docFor`/`signatureFor`) read a
real `inspect.getdoc()`/`inspect.signature()` off a real object — all three
only meaningfully testable once a cell has actually run.

`docFor`/`signatureFor` also check `__builtins__` now (planning/
CELL_TOOLTIPS.md option a — TestBuiltinTooltips), and hover docs/signature
help fall back to Jedi's static analysis for a name that has never been
executed (option c — TestPreRunTooltips), loaded in the background well
after boot() finishes (`dewlab.jediReady()`).

    python3 -m pytest tests/e2e/test_autocomplete.py -q
"""

from __future__ import annotations

import json


def cell_content(page, cell_id: str):
    return page.locator(f".dl-cell[data-cell-id='{cell_id}'] .dl-editor .cm-content")


def completion_labels(page):
    return page.eval_on_selector_all(
        ".cm-tooltip-autocomplete .cm-completionLabel", "els => els.map(e => e.textContent)"
    )


def js_string(text: str) -> str:
    return json.dumps(text)


def hover_at_text(page, cell_id: str, needle: str, *, last: bool = False) -> None:
    """Hovers the exact document position of `needle` inside a cell, found
    through the editor's own `view.coordsAtPos()` rather than a DOM text
    locator. get_by_text works for a name CodeMirror gives its own
    highlighting span (a user-defined function name, say) but not for one
    that renders as bare text beside other tokens — "len" inside "len([1,
    2, 3])" has no span of its own, so no element's accessible text is
    ever exactly "len". Going through the editor's own coordinates sidesteps
    the question of how a token happened to be split into elements."""
    coords = page.evaluate(f"""
        (() => {{
            const cell = dewlab.cells.find(c => c.id === {js_string(cell_id)});
            const view = cell.editor.view;
            const doc = view.state.doc.toString();
            const idx = doc.{"lastIndexOf" if last else "indexOf"}({js_string(needle)});
            if (idx === -1) return null;
            const start = view.coordsAtPos(idx);
            const end = view.coordsAtPos(idx + {js_string(needle)}.length);
            return {{ x: (start.left + end.right) / 2, y: (start.top + start.bottom) / 2 }};
        }})()
    """)
    assert coords is not None, f"{needle!r} not found in cell {cell_id!r}"
    page.mouse.move(coords["x"], coords["y"])


def run(page, cell_id: str) -> None:
    """Run a cell and wait for it to actually finish, the same way
    test_phase0_golden_path.py does."""
    selector = f".dl-cell[data-cell-id='{cell_id}'] .dl-output"
    page.evaluate(f"dewlab.runCell({js_string(cell_id)})")
    page.wait_for_function(
        f"document.querySelector({js_string(selector)}).children.length > 0",
        timeout=60_000,
    )


def test_typing_a_partial_keyword_offers_it(page):
    cell = cell_content(page, "plain-python")
    cell.click()
    page.keyboard.press("Control+End")
    page.keyboard.type("\ndef")
    page.wait_for_selector(".cm-tooltip-autocomplete")
    assert "def" in completion_labels(page)


def test_accepting_a_completion_inserts_it(page):
    """closeBrackets already auto-pairs the "(" typed below, so the buffer
    reads len(list) once the completion replaces "lis" with "list" —
    checked as one string rather than "list(" for that reason."""
    cell = cell_content(page, "plain-python")
    cell.click()
    page.keyboard.press("Control+End")
    page.keyboard.type("\nlen(")
    page.keyboard.type("lis")
    page.wait_for_selector(".cm-tooltip-autocomplete")
    page.keyboard.press("Enter")
    assert "len(list)" in cell.inner_text()


def test_a_name_the_student_already_typed_is_offered(page):
    """localCompletionSource: names defined earlier in the same cell, not
    only Python's own builtins."""
    cell = cell_content(page, "plain-python")
    cell.click()
    page.keyboard.press("Control+End")
    page.keyboard.type("\nsome_reading_value = 1\nsome_read")
    page.wait_for_selector(".cm-tooltip-autocomplete")
    assert "some_reading_value" in completion_labels(page)


def test_escape_closes_the_completion_without_inserting_it(page):
    cell = cell_content(page, "plain-python")
    cell.click()
    page.keyboard.press("Control+End")
    page.keyboard.type("\npri")
    page.wait_for_selector(".cm-tooltip-autocomplete")
    page.keyboard.press("Escape")
    page.wait_for_selector(".cm-tooltip-autocomplete", state="hidden")
    assert "pri" in cell.inner_text()
    assert "print" not in cell.inner_text().split("\n")[-1]


class TestLiveNamespaceCompletion:
    """pageNamesCompletion reads tutorial_tools._page_globals — the actual
    dict every cell runs against — so a name only really exists here once a
    cell defining it has run, not just been typed."""

    def test_a_name_defined_by_running_a_cell_is_offered(self, page):
        cell = cell_content(page, "plain-python")
        cell.click()
        page.keyboard.press("Control+End")
        page.keyboard.type("\nsome_named_thing = 42")
        run(page, "plain-python")
        page.keyboard.press("Control+End")
        page.keyboard.type("\nsome_named_")
        page.wait_for_selector(".cm-tooltip-autocomplete")
        assert "some_named_thing" in completion_labels(page)


class TestHoverDocs:
    """docFor (assets/tutorial-runtime.js) reads a real inspect.getdoc() off
    a real object living in the interpreter actually running the page's
    cells — there is nothing bundled here to fall out of date."""

    def test_hovering_a_name_shows_its_own_real_docstring(self, page):
        cell = cell_content(page, "plain-python")
        cell.click()
        page.keyboard.press("Control+End")
        page.keyboard.type('\ndef helper_fn():\n    """my own real docstring"""\n')
        run(page, "plain-python")
        cell.get_by_text("helper_fn", exact=True).first.hover()
        page.wait_for_selector(".cm-dewlab-doc-tooltip")
        assert "my own real docstring" in page.inner_text(".cm-dewlab-doc-tooltip")

    def test_hovering_a_name_that_was_never_run_shows_nothing(self, page):
        cell = cell_content(page, "plain-python")
        cell.click()
        page.keyboard.press("Control+End")
        page.keyboard.type("\ntotally_undefined_name_xyz = 1")
        page.keyboard.press("Escape")
        cell.get_by_text("totally_undefined_name_xyz", exact=False).first.hover()
        page.wait_for_timeout(600)
        assert page.locator(".cm-dewlab-doc-tooltip").count() == 0


class TestBuiltinTooltips:
    """docFor and signatureFor (assets/tutorial-runtime.js) were widened to
    also check __builtins__ — planning/CELL_TOOLTIPS.md option (a) — a
    lookup one step further than tutorial_tools._page_globals, not a
    redesign. Typed with insert_text() rather than type(): closeBrackets
    auto-pairs "(" as a student types it, which is exactly what these tests
    need to watch happen, but it makes type() unreliable for multi-line
    bodies elsewhere in this class (indentOnInput adds its own indent on
    top of any typed by hand, and closing a typed triple-quoted string
    fights the same auto-pairing) — insert_text() bypasses that keystroke
    handling entirely, the way a paste would."""

    def test_hovering_a_builtin_shows_its_docstring(self, page):
        cell = cell_content(page, "plain-python")
        cell.click()
        page.keyboard.press("Control+End")
        page.keyboard.insert_text("\nlen([1, 2, 3])")
        hover_at_text(page, "plain-python", "len")
        page.wait_for_selector(".cm-dewlab-doc-tooltip")
        assert "Return the number of items" in page.inner_text(".cm-dewlab-doc-tooltip")

    def test_typing_a_builtin_call_shows_its_signature(self, page):
        cell = cell_content(page, "plain-python")
        cell.click()
        page.keyboard.press("Control+End")
        page.keyboard.insert_text("\nlen")
        page.keyboard.type("(")  # the real keystroke closeBrackets reacts to
        page.wait_for_selector(".cm-dewlab-signature-tooltip")
        assert "len(" in page.inner_text(".cm-dewlab-signature-tooltip")

    def test_signature_help_disappears_once_the_call_closes(self, page):
        cell = cell_content(page, "plain-python")
        cell.click()
        page.keyboard.press("Control+End")
        page.keyboard.insert_text("\nlen")
        page.keyboard.type("(")
        page.wait_for_selector(".cm-dewlab-signature-tooltip")
        page.keyboard.type("[1]")
        page.wait_for_selector(".cm-dewlab-signature-tooltip", state="hidden")

    def test_signature_help_bolds_the_argument_the_cursor_is_in(self, page):
        """Typing past the first comma should move the bolded parameter
        from "first" to "second"."""
        cell = cell_content(page, "plain-python")
        cell.click()
        page.keyboard.press("Control+End")
        page.keyboard.insert_text("\ndef two_args(first, second):\n    pass\n")
        run(page, "plain-python")
        page.keyboard.press("Control+End")
        page.keyboard.insert_text("\ntwo_args(1, ")
        page.wait_for_selector(".cm-dewlab-signature-tooltip")
        bold = page.inner_text(".cm-dewlab-signature-tooltip strong")
        assert bold == "second"


class TestPreRunTooltips:
    """planning/CELL_TOOLTIPS.md option (c): Jedi, loaded in the background
    after boot() (dewlab.jediReady()), answers hover docs and signature help
    for a name that has never been executed — the one gap docFor/signatureFor
    cannot structurally close, since they only ever read a live namespace."""

    SOURCE = (
        "\ndef average(numbers):\n"
        '    """Return the mean of numbers."""\n'
        "    return sum(numbers) / len(numbers)\n\n"
        "average"
    )

    def test_hovering_a_just_written_function_shows_its_docstring(self, page):
        page.wait_for_function("dewlab.jediReady()", timeout=30_000)
        cell = cell_content(page, "plain-python")
        cell.click()
        page.keyboard.press("Control+End")
        page.keyboard.insert_text(self.SOURCE)
        # Never run — Jedi is the only thing that could possibly answer this.
        hover_at_text(page, "plain-python", "average", last=True)
        page.wait_for_selector(".cm-dewlab-doc-tooltip")
        assert "Return the mean of numbers" in page.inner_text(".cm-dewlab-doc-tooltip")

    def test_signature_help_works_before_the_cell_has_run(self, page):
        page.wait_for_function("dewlab.jediReady()", timeout=30_000)
        cell = cell_content(page, "plain-python")
        cell.click()
        page.keyboard.press("Control+End")
        page.keyboard.insert_text(self.SOURCE)
        page.keyboard.type("(")
        page.wait_for_selector(".cm-dewlab-signature-tooltip")
        assert "average(" in page.inner_text(".cm-dewlab-signature-tooltip")

    def test_a_genuinely_unknown_name_gets_nothing_from_jedi_either(self, page):
        page.wait_for_function("dewlab.jediReady()", timeout=30_000)
        cell = cell_content(page, "plain-python")
        cell.click()
        page.keyboard.press("Control+End")
        page.keyboard.insert_text("\ncompletely_made_up_name_no_such_thing")
        page.keyboard.type("(")
        page.wait_for_timeout(600)
        assert page.locator(".cm-dewlab-signature-tooltip").count() == 0

    def test_live_answer_is_still_used_once_the_cell_has_run(self, page):
        """Not a case where Jedi and the live interpreter could disagree —
        both read the same docstring — but this proves the composed
        dewlab.hoverDoc() a student's editor actually calls keeps working
        the same way dewlab.docFor() alone already does, rather than the
        Jedi fallback somehow taking over once a name goes live."""
        page.wait_for_function("dewlab.jediReady()", timeout=30_000)
        cell = cell_content(page, "plain-python")
        cell.click()
        page.keyboard.press("Control+End")
        page.keyboard.insert_text('\ndef labelled():\n    """post-run docstring"""\n')
        run(page, "plain-python")
        doc = page.evaluate("dewlab.hoverDoc('labelled', '', 1, 0)")
        assert "post-run docstring" in doc
