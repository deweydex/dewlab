"""Toolkit cells: a Python cell marked `toolkit: yes` is loaded into every
later page of its course (docs/WRITING_TUTORIALS.md, "A toolkit the reader
carries from page to page"). The build's half: the header and the
`python toolkit-reference` fence parse, the reference never reaches the
page, a later page's manifest lists earlier pages' entries in course order
and none of its own, and the ways an author can get it wrong fail."""

from __future__ import annotations

import pytest

from helpers import (
    COURSE, SERIES, b, built, course, manifest, practice, set_order, set_series_order,
    write, write_in_series,
)

STUB = """```python exec
id: toolkit-binary
toolkit: yes
def to_binary(n):
    ...
```

```python toolkit-reference
for: toolkit-binary
def to_binary(n):
    return bin(n)[2:]
```
"""

WHOLE = """```python exec
id: toolkit-split
toolkit: yes
def split_evenly(total, parts):
    return total / parts
```
"""

PLAIN = """```python exec
id: plain
print("not a toolkit cell")
```
"""


def names(page: str) -> list[tuple[str, str]]:
    return [(e["tutorial"], e["cell"]) for e in manifest(page).get("toolkit", [])]


class TestParsing:
    def test_the_header_and_the_reference_fence_parse_and_the_reference_is_never_shown(self, repo):
        write(repo, "# One\n\n" + STUB, slug="one")
        b.build()
        page = built(repo, "one")
        # The cell is an ordinary cell on its own page: the stub is what a
        # reader starts from, and the header line is not part of the code.
        cells = manifest(page)["cells"]
        assert [c["id"] for c in cells] == ["toolkit-binary"]
        assert cells[0]["code"] == "def to_binary(n):\n    ..."
        assert "bin(n)[2:]" not in page
        assert "toolkit-reference" not in page
        # A page gets no toolkit of its own cells.
        assert "toolkit" not in manifest(page)

    def test_the_cell_and_its_reference_are_read_off_the_source(self, repo):
        path = write(repo, STUB + PLAIN, slug="one")
        tutorial = b.load(path)
        binary, plain = tutorial.cells
        assert binary.toolkit and not plain.toolkit
        assert binary.reference == "def to_binary(n):\n    return bin(n)[2:]"
        assert binary.toolkit_reference == binary.reference
        whole = b.load(write(repo, WHOLE, slug="two")).cells[0]
        assert whole.reference is None
        assert whole.toolkit_reference == whole.code

    @pytest.mark.parametrize("value, expected", [("yes", True), ("true", True), ("no", False)])
    def test_toolkit_takes_yes_or_no(self, repo, value, expected):
        path = write(repo, f"```python exec\nid: c\ntoolkit: {value}\nx = 1\n```\n", slug="one")
        assert b.load(path).cells[0].toolkit is expected


class TestWhatALaterPageGets:
    def test_earlier_pages_entries_arrive_in_course_order_and_the_pages_own_do_not(self, repo):
        write(repo, STUB, slug="one")
        write(repo, WHOLE + PLAIN.replace("id: plain", "id: plain-2"), slug="two")
        write(repo, "```python exec\nid: toolkit-three\ntoolkit: yes\ndef three():\n"
                    "    return 3\n```\n", slug="three")
        set_order(repo, COURSE, SERIES, ["one", "two", "three"])
        b.build()

        assert "toolkit" not in manifest(built(repo, "one"))
        assert names(built(repo, "two")) == [("one", "toolkit-binary")]
        assert names(built(repo, "three")) == [("one", "toolkit-binary"), ("two", "toolkit-split")]

        entry, split = manifest(built(repo, "three"))["toolkit"]
        assert entry == {
            "tutorial": "one", "title": "A Title", "cell": "toolkit-binary",
            "reference": "def to_binary(n):\n    return bin(n)[2:]",
        }
        # No reference fence: the cell's own code is the reference.
        assert split["reference"] == "def split_evenly(total, parts):\n    return total / parts"

    def test_the_order_is_the_course_files_across_series(self, repo):
        write(repo, "One.\n", slug="later")
        write_in_series(repo, STUB, slug="first", series="basics")
        set_order(repo, COURSE, SERIES, ["later"])
        set_series_order(repo, COURSE, ["basics", SERIES])
        b.build()
        assert names(built(repo, "later")) == [("first", "toolkit-binary")]

        set_series_order(repo, COURSE, [SERIES, "basics"])
        b.build()
        assert "toolkit" not in manifest(built(repo, "later"))

    def test_a_page_on_two_courses_takes_the_first_course_with_a_toolkit_before_it(self, repo):
        write(repo, STUB, slug="one")
        write(repo, WHOLE, slug="bills")
        write(repo, "Shared.\n", slug="shared")
        # The default course lists nothing with a toolkit before `shared`;
        # the second course does.
        set_order(repo, COURSE, SERIES, ["shared", "one"])
        course(repo, "zz-other", {"Start": ["bills", "shared"]})
        b.build()
        assert names(built(repo, "shared")) == [("bills", "toolkit-split")]

    def test_a_practice_page_loads_its_tutorials_toolkit_and_everything_before(self, repo):
        write(repo, STUB, slug="one")
        write(repo, WHOLE, slug="two")
        set_order(repo, COURSE, SERIES, ["one", "two"])
        practice(repo, "two")
        b.build()
        assert names(built(repo, "two-practice")) == [
            ("one", "toolkit-binary"), ("two", "toolkit-split")]

    def test_a_mixed_page_loads_every_listed_tutorials_toolkit_and_everything_before_the_latest(self, repo):
        def toolkit_cell(name: str) -> str:
            return f"```python exec\nid: tk-{name}\ntoolkit: yes\ndef {name}():\n    return 1\n```\n"

        for slug in ("zero", "one", "three", "four"):
            write(repo, toolkit_cell(slug), slug=slug)
        write(repo, PLAIN, slug="two")
        set_order(repo, COURSE, SERIES, ["zero", "one", "two", "three", "four"])
        # Listed out of course order on purpose: the course decides the order.
        practice(repo, "mixed", practice_across=["three", "one"])
        b.build()
        assert names(built(repo, "mixed")) == [
            ("zero", "tk-zero"), ("one", "tk-one"), ("three", "tk-three")]


class TestMistakes:
    def test_a_reference_for_a_cell_that_does_not_exist_fails(self, repo):
        write(repo, STUB.replace("for: toolkit-binary", "for: toolkit-binery"), slug="one")
        with pytest.raises(b.BuildError, match="toolkit-binery.*no cell with that id"):
            b.build()

    def test_a_reference_for_a_cell_that_is_not_a_toolkit_cell_fails(self, repo):
        write(repo, STUB.replace("toolkit: yes\n", ""), slug="one")
        with pytest.raises(b.BuildError, match="not a toolkit cell"):
            b.build()

    def test_two_references_for_one_cell_fail(self, repo):
        reference = STUB.split("\n\n", 1)[1]
        write(repo, STUB + "\n" + reference, slug="one")
        with pytest.raises(b.BuildError, match="two toolkit-reference fences"):
            b.build()

    def test_a_reference_with_no_for_line_fails(self, repo):
        write(repo, "```python toolkit-reference\ndef f():\n    pass\n```\n", slug="one")
        with pytest.raises(b.BuildError, match="needs a `for:` line"):
            b.build()

    def test_an_unknown_toolkit_value_fails(self, repo):
        write(repo, "```python exec\nid: c\ntoolkit: maybe\nx = 1\n```\n", slug="one")
        with pytest.raises(b.BuildError, match="toolkit: maybe"):
            b.build()

    def test_a_sql_cell_cannot_be_a_toolkit_cell(self, repo):
        write(repo, "```sql exec\nid: q\ntoolkit: yes\nSELECT 1;\n```\n", slug="one")
        with pytest.raises(b.BuildError, match="only a Python cell"):
            b.build()
