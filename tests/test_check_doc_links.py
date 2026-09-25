"""The guide-citation half of `dev/check_doc_links.py`: an anchor that is
not in the guide it names fails, and so does a citation of the style guide
by section number. The strings that should fail are built from parts, so
this file does not trip the check it tests when the repository is scanned."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "dev"))

import check_doc_links as cdl  # noqa: E402

GUIDE = "PEDAGOGICAL_STYLE_GUIDE.md"
SECTION = "§"


def guides(tmp_path):
    guide = tmp_path / GUIDE
    guide.write_text(
        "# Pedagogical style guide\n\n"
        '<a id="voice"></a>\n## Voice\n\n'
        "See [the checklist](#checklist) and [nowhere](#nowhere).\n\n"
        '<a id="checklist"></a>\n## Before a page ships\n\n'
        "```python\n# Not a heading\n```\n")
    return {GUIDE: guide}


def problems(tmp_path, text):
    doc = tmp_path / "doc.md"
    doc.write_text(text)
    return cdl.citation_problems(files=[doc], guides=guides(tmp_path))


def test_an_anchor_or_a_heading_slug_resolves(tmp_path):
    assert problems(tmp_path, f"Read `{GUIDE}#voice`, then "
                              f"`{GUIDE}#before-a-page-ships`.\n") == []


def test_a_missing_anchor_fails(tmp_path):
    found = problems(tmp_path, f"Read `{GUIDE}#tone`.\n")
    assert len(found) == 1 and f"{GUIDE}#tone" in found[0]


def test_a_comment_in_a_fence_is_not_a_heading(tmp_path):
    assert problems(tmp_path, f"`{GUIDE}#not-a-heading`\n")


def test_the_guide_own_links_are_checked(tmp_path):
    found = cdl.citation_problems(files=[tmp_path / GUIDE],
                                  guides=guides(tmp_path))
    assert found == [f"{tmp_path / GUIDE}:6: cites {GUIDE}#nowhere, and "
                     f"{GUIDE} has no such anchor"]


def test_every_numbered_form_fails(tmp_path):
    for text in (f"`{GUIDE}` {SECTION}4",
                 f"{GUIDE} section 4",
                 f"({GUIDE}#6-practice-pages)",
                 "the style" " guide's section 3",
                 f"(style guide {SECTION}11)",
                 "style" " guide, section 6",
                 f"{SECTION}4 of `{GUIDE}`"):
        assert problems(tmp_path, text + "\n"), text


def test_a_citation_wrapped_across_two_lines_fails(tmp_path):
    found = problems(tmp_path, f"written the way `{GUIDE}`\n{SECTION}5 says\n")
    assert found and found[0].endswith(("section number; cite its anchor "
                                        f"instead, as {GUIDE}#voice"))
    assert ":1:" in found[0]


def test_history_told_without_a_citation_passes(tmp_path):
    assert problems(tmp_path, "the style guide's voice section (then "
                              f"{SECTION}4), and ARCHITECTURE.md {SECTION}2\n") == []


def test_the_repository_is_clean():
    assert cdl.citation_problems() == []
