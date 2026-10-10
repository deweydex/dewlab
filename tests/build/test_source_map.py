"""The source map (source_map.py): which range of a page's markdown file each
top-level block of the rendered page came from.

It is the foundation of editing a page where it stands
(planning/IN_PAGE_EDITOR.md). The properties that matter, in order: it never
changes how a page reads; each range really is the block it labels; and
splicing new text over one range changes that block and nothing else.
"""

from __future__ import annotations

import re
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import pytest

from helpers import DEWLAB, b, built, write

sys.path.insert(0, str(DEWLAB))
import source_map as sm  # noqa: E402


def kinds(body: str) -> list[str]:
    return [block.kind for block in sm.blocks(body)]


def pieces(body: str) -> list[str]:
    return [body[block.start:block.end] for block in sm.blocks(body)]


class TestBlocks:
    """How a page's markdown is cut into blocks."""

    def test_paragraphs_headings_and_lists_are_blocks_in_order(self):
        body = "# Title\n\nA paragraph\nover two lines.\n\n- one\n- two\n\nAnother.\n"
        assert kinds(body) == ["heading", "paragraph", "list", "paragraph"]
        assert pieces(body)[1] == "A paragraph\nover two lines."

    def test_a_list_with_blank_lines_between_its_items_is_one_block(self):
        body = "1. First\n\n2. Second\n\n   carried on\n\nAfter.\n"
        assert kinds(body) == ["list", "paragraph"]

    def test_a_list_that_starts_on_the_line_after_a_paragraph_line_is_its_own_block(self):
        body = "Intro line\n1. One\n2. Two\n"
        assert kinds(body) == ["paragraph", "list"]

    def test_a_fence_is_one_block_and_blank_lines_inside_it_do_not_split_it(self):
        body = "Before.\n\n```python\nx = 1\n\ny = 2\n```\n\nAfter.\n"
        assert kinds(body) == ["paragraph", "fence:python", "paragraph"]

    def test_a_hint_solution_and_inputs_fence_belong_to_the_cell_above(self):
        body = ("```python exec\nid: c\nx = 1\n```\n\n```hint\nfor: c\nLook.\n```\n\n"
                "```solution\nx = 2\n```\n\nNext.\n")
        assert kinds(body) == ["fence:cell", "paragraph"]
        assert pieces(body)[0].count("```") == 6

    def test_the_panes_of_one_site_editor_are_one_block(self):
        body = ("```html site\nsite: demo\n<p>a</p>\n```\n\n"
                "```css site\nsite: demo\np { color: red; }\n```\n\n"
                "```html site\nsite: other\n<p>b</p>\n```\n")
        assert kinds(body) == ["fence:site:demo", "fence:site:other"]

    def test_world_variants_side_by_side_are_one_block(self):
        body = ('<div class="dl-world" data-world="a">\n\nOne.\n\n</div>\n\n'
                '<div class="dl-world" data-world="b">\n\nTwo.\n\n</div>\n')
        assert kinds(body) == ["html:world"]

    def test_a_fold_with_blank_lines_inside_is_one_block(self):
        body = '<details class="dl-hint">\n<summary>s</summary>\n\nBody.\n\n1. one\n</details>\n\nAfter.\n'
        assert kinds(body) == ["html:details", "paragraph"]

    def test_tags_shown_in_code_do_not_unbalance_a_fold(self):
        body = ('<details class="dl-answer">\n<summary>a</summary>\n\n'
                "Use `<details>` for this.\n\n```html\n<details>\n```\n\n</details>\n\nAfter.\n")
        assert kinds(body) == ["html:details", "paragraph"]

    def test_a_fence_indented_under_a_list_item_is_part_of_the_list(self):
        body = "1. Step\n\n   ```css\n   a { b: c; }\n   ```\n\nAfter.\n"
        assert kinds(body) == ["list", "paragraph"]

    def test_display_maths_with_a_blank_line_inside_is_one_block(self):
        body = "Before.\n\n$$\na = 1\n\nb = 2\n$$\n\nAfter.\n"
        assert kinds(body) == ["paragraph", "paragraph", "paragraph"]
        assert pieces(body)[1].startswith("$$") and pieces(body)[1].endswith("$$")

    def test_a_setext_heading_is_a_heading(self):
        assert kinds("Title\n-----\n\nText.\n") == ["heading", "paragraph"]


class TestTheMapOnAPage:
    @pytest.fixture(autouse=True)
    def _on(self, monkeypatch):
        monkeypatch.setattr(b, "SOURCE_MAP", True)

    PAGE = ("# A page\n\nFirst paragraph.\n\n- one\n- two\n\n"
            '<details class="dl-hint"><summary>stuck?</summary>\n\nTry it.\n\n</details>\n\n'
            "```python exec\nid: only\nprint(1)\n```\n\nLast.\n")

    def test_each_block_carries_the_range_of_its_own_text(self, repo):
        path = write(repo, self.PAGE)
        b.build()
        text = path.read_text()
        got = re.findall(r"<(\w+)[^>]* data-md=\"(\d+):(\d+)\"", built(repo))
        assert [tag for tag, *_ in got] == ["h1", "p", "ul", "details", "div", "p"]
        starts = [text[int(s):int(e)] for _, s, e in got]
        assert starts[0] == "# A page"
        assert starts[1] == "First paragraph."
        assert starts[2] == "- one\n- two"
        assert starts[3].startswith('<details class="dl-hint">') and starts[3].endswith("</details>")
        assert starts[4].startswith("```python exec") and starts[4].endswith("```")
        assert starts[5] == "Last."

    def test_the_map_changes_nothing_else_about_the_page(self, repo, monkeypatch):
        write(repo, self.PAGE)
        b.build()
        mapped = built(repo)
        monkeypatch.setattr(b, "SOURCE_MAP", False)
        b.build()
        assert sm.strip(mapped) == built(repo)
        assert "dl-src" not in mapped

    def test_no_marker_comment_is_left_on_the_page(self, repo):
        write(repo, self.PAGE + "\n[ref]: http://example.com\n")
        b.build()
        assert "<!--dl-src" not in built(repo)

    def test_splicing_new_text_over_one_range_changes_that_block_and_no_other(self, repo, monkeypatch):
        path = write(repo, self.PAGE)
        b.build()
        before = sm.strip(built(repo))
        text = path.read_text()
        start, end = map(int, re.search(r'<p data-md="(\d+):(\d+)">First', built(repo)).groups())
        path.write_text(sm.splice(text, [(start, end, "A **changed** paragraph.")]))
        b.build()
        after = sm.strip(built(repo))
        assert "<p>A <strong>changed</strong> paragraph.</p>" in after
        assert after.replace("<p>A <strong>changed</strong> paragraph.</p>", "<p>First paragraph.</p>") == before

    def test_a_page_the_map_would_change_has_none_and_says_so(self, repo, monkeypatch, capsys):
        write(repo, "# A page\n\nText.\n")
        monkeypatch.setattr(sm, "attach", lambda page: page.replace("<p>", "<p class='x'>"))
        b.build()
        assert "data-md" not in built(repo) and "class='x'" not in built(repo)
        assert "would change how the page reads" in capsys.readouterr().err


class TestSplice:
    def test_edits_apply_from_the_end_so_earlier_offsets_stay_true(self):
        assert sm.splice("abcdef", [(0, 1, "X"), (4, 6, "YYY")]) == "XbcdYYY"

    def test_overlapping_edits_are_refused(self):
        with pytest.raises(ValueError):
            sm.splice("abcdef", [(0, 3, "x"), (2, 4, "y")])


def _check_page(path: str) -> tuple[str, str]:
    """In a worker process: the page built with the map and stripped, against
    the page built without it; and whether every range lies inside the file."""
    page = Path(path)
    b.SOURCE_MAP = False
    plain = b.load(page).body_html
    b.SOURCE_MAP = True
    mapped = b.load(page).body_html
    if "data-md" not in mapped and "data-md" in plain:
        return path, "lost"
    if sm.strip(mapped) != plain:
        return path, "changed"
    size = len(page.read_text())
    last = -1
    for start, end in re.findall(r' data-md="(\d+):(\d+)"', mapped):
        start, end = int(start), int(end)
        if not (0 <= start < end <= size) or start < last:
            return path, "range outside the file or out of order"
        last = end
    return path, ""


def test_every_real_page_reads_the_same_with_the_map_and_has_sound_ranges():
    """Across every tutorial in the repository, so a new kind of markup the
    tokenizer misreads is found here rather than on a teacher's page. The
    build would drop the map for such a page (see load()), so this reports
    where the tokenizer needs teaching, not a page that is broken."""
    files = sorted(str(p) for p in (DEWLAB / "tutorials").glob("*/*.md"))
    with ProcessPoolExecutor() as pool:
        problems = [(p.replace(str(DEWLAB) + "/", ""), why)
                    for p, why in pool.map(_check_page, files, chunksize=8) if why]
    assert not problems, problems
