"""Tests for the report-pattern grouping logic in dev/report_patterns.py and
the labelling logic in dev/label_report.py.

Neither script's actual GitHub API calls are exercised here — that needs a
live repository, which is exactly what the workflow itself provides when it
runs. What is worth protecting with a fast test is the part a live run
cannot easily catch a regression in until reports are already piling up:
parsing an issue-form body back into fields, and the threshold arithmetic
that decides whether something is a pattern at all.

    python3 -m pytest tests/test_report_patterns.py -q
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "dev"))

import label_report  # noqa: E402
import report_patterns  # noqa: E402

ISSUE_BODY = """### What kind of thing is this?

It gives an error, and I have tried resetting the cell, running the cells above it, and reloading the page

### Page

computational-methods/first-steps

### Version

2026.09.01.2

### Cell

sum-list

### The cell's code

total = sum(price)

### What the cell showed

NameError: name 'price' is not defined

### Browser

Firefox 142, Windows

### What happened

Fails before I change anything.
"""


class TestParseFields:
    def test_reads_every_field_by_its_label(self):
        fields = report_patterns.parse_fields(ISSUE_BODY)
        assert fields["Page"] == "computational-methods/first-steps"
        assert fields["Cell"] == "sum-list"
        assert fields["What kind of thing is this?"].startswith("It gives an error")
        assert fields["What happened"] == "Fails before I change anything."

    def test_empty_body_gives_no_fields(self):
        assert report_patterns.parse_fields("") == {}

    def test_label_report_uses_the_same_parser(self):
        # Both scripts read the same rendered body; a change to one parser
        # without the other is exactly the drift worth catching here.
        assert label_report.parse_fields(ISSUE_BODY) == report_patterns.parse_fields(ISSUE_BODY)


class TestKindLabel:
    def test_error_kind(self):
        assert label_report.kind_label(
            "It gives an error, and I have tried resetting the cell"
        ) == "kind: error"

    def test_wrong_or_unclear_kind(self):
        assert label_report.kind_label("The page is wrong, or I could not follow it") == "kind: unclear"

    def test_anything_else_falls_back_to_question(self):
        assert label_report.kind_label("A question, an idea, or something else") == "kind: question"
        assert label_report.kind_label("") == "kind: question"


class TestPageLabel:
    def test_short_page_is_untouched(self):
        assert label_report.page_label("web/selectors") == "page: web/selectors"

    def test_long_page_is_truncated_to_githubs_own_limit(self):
        long_page = "a-very-long-module-name/an-even-longer-tutorial-slug-name"
        name = label_report.page_label(long_page)
        assert len(name) <= 50


def issue(number: int, cell: str = "", days_old: int = 0) -> dict:
    return {"number": number, "title": f"[report] #{number}", "cell": cell}


class TestWorthAPattern:
    def test_below_every_threshold_is_not_a_pattern(self):
        assert not report_patterns.worth_a_pattern([issue(1), issue(2)])

    def test_three_reports_on_one_page_is_a_pattern(self):
        assert report_patterns.worth_a_pattern([issue(1), issue(2), issue(3)])

    def test_two_reports_on_the_same_cell_is_a_pattern_even_with_few_reports(self):
        assert report_patterns.worth_a_pattern([issue(1, cell="sum-list"), issue(2, cell="sum-list")])

    def test_two_reports_on_different_cells_is_not_a_pattern(self):
        assert not report_patterns.worth_a_pattern([issue(1, cell="sum-list"), issue(2, cell="other-cell")])


class TestPatternBody:
    def test_carries_the_marker_github_search_relies_on(self):
        body = report_patterns.pattern_body("web/selectors", [issue(1), issue(2), issue(3)])
        match = report_patterns.MARKER_RE.search(body)
        assert match and match.group("page") == "web/selectors"

    def test_groups_by_cell_and_flags_the_one_at_threshold(self):
        body = report_patterns.pattern_body(
            "computational-methods/first-steps",
            [issue(1, cell="sum-list"), issue(2, cell="sum-list"), issue(3)],
        )
        assert "#1, #2" in body
        assert "at or over the per-cell threshold" in body
        assert "#3" in body
        assert "Not tied to one cell" in body
