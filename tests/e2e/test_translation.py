"""Browser translation leaves code, what a cell printed, and maths alone
(#317): the runtime marks them `translate="no"`, and the prose around them
translates as usual. `pages/reading-helpers.md` tells a reader so."""

from __future__ import annotations


def test_code_output_and_maths_are_kept_from_translation(page):
    marked = page.evaluate(
        """() => ({
             editors: [...document.querySelectorAll('.dl-editor')].every((el) => el.translate === false),
             outputs: [...document.querySelectorAll('.dl-output')].every((el) => el.translate === false),
             code: [...document.querySelectorAll('#dl-body code, #dl-body pre')].every((el) => el.translate === false),
             maths: [...document.querySelectorAll('.dl-math')].every((el) => el.translate === false),
             counts: [document.querySelectorAll('.dl-editor').length,
                      document.querySelectorAll('.dl-math').length],
             prose: document.querySelector('#dl-body p').translate,
           })"""
    )
    assert marked["editors"] and marked["outputs"] and marked["code"] and marked["maths"]
    assert marked["counts"][0] > 0 and marked["counts"][1] > 0
    assert marked["prose"] is True


def test_a_cell_of_your_own_is_kept_from_translation_too(page):
    page.evaluate("globalThis.dewlab.addCustomCell('python', 'print(1)')")
    assert page.evaluate(
        "[...document.querySelectorAll('.dl-editor')].every((el) => el.translate === false)"
    )
