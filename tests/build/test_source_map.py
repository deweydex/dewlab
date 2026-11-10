"""The source map (source_map.py): which range of a page's markdown file each
top-level block of the rendered page came from.

It is the foundation of editing a page where it stands.
The properties that matter, in order: it never
changes how a page reads; each range really is the block it labels; and
splicing new text over one range changes that block and nothing else.
"""

from __future__ import annotations

import hashlib
import re
import subprocess
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import pytest

from helpers import DEWLAB, b, built, manifest, write

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
        monkeypatch.setattr(b.cfg, "SOURCE_MAP", True)

    PAGE = ("# A page\n\nFirst paragraph.\n\n- one\n- two\n\n"
            '<details class="dl-hint"><summary>stuck?</summary>\n\nTry it.\n\n</details>\n\n'
            "```python exec\nid: only\nprint(1)\n```\n\nLast.\n")

    def test_each_block_carries_the_range_of_its_own_text(self, repo):
        path = write(repo, self.PAGE)
        b.build()
        text = path.read_text()
        got = re.findall(r"<(\w+)[^>]* data-md=\"(\d+):(\d+)\"", built(repo))
        assert [tag for tag, *_ in got] == ["h1", "p", "ul", "details", "p", "div", "p"]
        starts = [text[int(s):int(e)] for _, s, e in got]
        assert starts[0] == "# A page"
        assert starts[1] == "First paragraph."
        assert starts[2] == "- one\n- two"
        assert starts[3].startswith('<details class="dl-hint">') and starts[3].endswith("</details>")
        assert starts[4] == "Try it."          # the block inside the fold
        assert starts[5].startswith("```python exec") and starts[5].endswith("```")
        assert starts[6] == "Last."

    def test_the_blocks_inside_a_fold_carry_their_own_ranges_and_sit_inside_it(self, repo):
        path = write(repo, '<details class="dl-answer"><summary>answer</summary>\n\n'
                           'One.\n\n- a\n- b\n\n```python\nx = 1\n```\n\n</details>\n')
        b.build()
        page = built(repo)
        text = path.read_text()
        fold = re.search(r"<details[^>]* data-md=\"\d+:\d+\">(.*?)</details>", page, re.S).group(1)
        inner = re.findall(r"<(\w+)[^>]* data-md=\"(\d+):(\d+)\"", fold)
        assert [tag for tag, *_ in inner] == ["p", "ul", "pre"]
        assert [text[int(s):int(e)] for _, s, e in inner] == ["One.", "- a\n- b", "```python\nx = 1\n```"]

    def test_the_map_changes_nothing_else_about_the_page(self, repo, monkeypatch):
        write(repo, self.PAGE)
        b.build()
        mapped = built(repo)
        monkeypatch.setattr(b.cfg, "SOURCE_MAP", False)
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


class TestWhatEditThisPageReads:
    """The page's manifest says which file and blob the block ranges point into
    (assets/inpage-edit.js fetches that blob, so the offsets are always true)."""

    def test_a_mapped_page_names_its_file_and_the_git_blob_it_was_built_from(self, repo, monkeypatch):
        monkeypatch.setattr(b.cfg, "SOURCE_MAP", True)
        path = write(repo, "# A page\n\nText.\n")
        b.build()
        edit = manifest(built(repo))["edit"]
        data = path.read_bytes()
        assert edit["path"] == "tutorials/sample/sample.md"
        assert edit["sha"] == hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()
        assert edit["title"] == "A Title"
        assert edit["module"].startswith("../assets/inpage-edit.js?v=")
        assert edit["editor"].startswith("../assets/vendor/milkdown.bundle.js?v=")

    def test_the_sha_is_the_one_git_itself_gives_the_file(self, repo, monkeypatch):
        monkeypatch.setattr(b.cfg, "SOURCE_MAP", True)
        path = write(repo, "# A page\n\nText.\n")
        b.build()
        git = subprocess.run(["git", "hash-object", str(path)], capture_output=True, text=True)
        assert manifest(built(repo))["edit"]["sha"] == git.stdout.strip()

    def test_a_page_built_without_the_map_has_no_edit_entry(self, repo):
        write(repo, "# A page\n\nText.\n")
        b.build()
        assert "edit" not in manifest(built(repo))
        assert "data-md=" not in built(repo)

    def test_the_settings_section_is_in_the_page_and_hidden_until_the_manifest_says_so(self, repo):
        write(repo, "# A page\n\nText.\n")
        b.build()
        page = built(repo)
        assert re.search(r'<div class="dl-settings-foot" id="dl-settings-edit" hidden>', page)
        assert "manifest.edit" in page


class TestSplice:
    def test_edits_apply_from_the_end_so_earlier_offsets_stay_true(self):
        assert sm.splice("abcdef", [(0, 1, "X"), (4, 6, "YYY")]) == "XbcdYYY"

    def test_overlapping_edits_are_refused(self):
        with pytest.raises(ValueError):
            sm.splice("abcdef", [(0, 3, "x"), (2, 4, "y")])


def _range_problem(ranges: list[tuple[int, int]], size: int) -> str:
    """What is wrong with a page's ranges, read in page order, or "" if nothing.

    Sound means: every range lies inside the file, and any two ranges are either
    apart or one wholly inside the other. A fold's range holds the ranges of the
    blocks inside it (source_map.mark() marks those too), so nesting is right;
    two ranges that share only part of their text never are.
    """
    open_ranges: list[tuple[int, int]] = []   # the folds this range may sit inside
    for start, end in ranges:
        if not (0 <= start < end <= size):
            return f"range {start}:{end} is outside the file"
        while open_ranges and start >= open_ranges[-1][1]:
            open_ranges.pop()
        if open_ranges:
            outer_start, outer_end = open_ranges[-1]
            if start < outer_start:
                return f"range {start}:{end} comes after {outer_start}:{outer_end} but starts before it"
            if end > outer_end:
                return f"range {start}:{end} overlaps {outer_start}:{outer_end}"
            if (start, end) == (outer_start, outer_end):
                return f"range {start}:{end} is on two blocks"
        open_ranges.append((start, end))
    return ""


class TestSoundRanges:
    """The rule the every-real-page test holds each page's ranges to."""

    def test_ranges_one_after_another_are_sound(self):
        assert _range_problem([(0, 5), (7, 12), (12, 20)], 20) == ""

    def test_blocks_inside_a_fold_and_a_fold_inside_a_fold_are_sound(self):
        assert _range_problem([(0, 5), (7, 60), (20, 25), (27, 50), (30, 40), (42, 48), (52, 55), (62, 70)], 70) == ""

    def test_two_ranges_that_share_only_part_of_their_text_are_refused(self):
        assert "overlaps" in _range_problem([(0, 10), (5, 15)], 20)
        assert "overlaps" in _range_problem([(0, 30), (5, 15), (10, 20)], 40)

    def test_a_range_out_of_page_order_is_refused(self):
        assert "starts before" in _range_problem([(10, 20), (30, 40), (0, 5)], 40)

    def test_a_range_past_the_end_of_the_file_or_empty_is_refused(self):
        assert "outside" in _range_problem([(0, 5), (7, 21)], 20)
        assert "outside" in _range_problem([(5, 5)], 20)

    def test_one_range_on_two_blocks_is_refused(self):
        assert "two blocks" in _range_problem([(0, 10), (0, 10)], 20)


def _check_page(path: str) -> tuple[str, str]:
    """In a worker process: the page built with the map and stripped, against
    the page built without it; and what is wrong with its ranges, if anything."""
    page = Path(path)
    b.cfg.SOURCE_MAP = False
    plain = b.load(page).body_html
    b.cfg.SOURCE_MAP = True
    mapped = b.load(page).body_html
    if "data-md" not in mapped and "data-md" in plain:
        return path, "lost"
    if sm.strip(mapped) != plain:
        return path, "changed"
    ranges = [(int(start), int(end))
              for start, end in re.findall(r' data-md="(\d+):(\d+)"', mapped)]
    return path, _range_problem(ranges, len(page.read_text()))


@pytest.mark.advisory
def test_every_real_page_reads_the_same_with_the_map_and_has_sound_ranges():
    """Across every tutorial in the repository, so a new kind of markup the
    tokenizer misreads is found here rather than on a teacher's page. The
    build would drop the map for a page it changed (see load()), so that half
    reports where the tokenizer needs teaching, not a page that is broken.

    The ranges are the other half, and the build does not check them. A
    teacher editing a page where it stands has each block written back over
    its own range. Two ranges that overlap without one holding the other mean
    saving one block writes over part of its neighbour; a range past the end
    of the file means the save lands on the wrong text. Blocks inside a fold
    do sit inside the fold's range, and that is sound (_range_problem())."""
    files = sorted(str(p) for p in (DEWLAB / "tutorials").glob("*/*.md"))
    with ProcessPoolExecutor() as pool:
        problems = [(p.replace(str(DEWLAB) + "/", ""), why)
                    for p, why in pool.map(_check_page, files, chunksize=8) if why]
    assert not problems, problems
