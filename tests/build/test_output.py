"""What a command-line build prints: one summary line, then the notes the
build carried on despite, together and last, where a teacher reading the end
of the output sees them. -v gives each page and each note as it happens.
(Before, a build printed a line for each of about 1,250 pages and the notes
were somewhere in the middle.)"""

from __future__ import annotations

import sys

import pytest

from helpers import *  # noqa: F401,F403
from helpers import b

CELL = "```python exec\nid: add-up\ndef total_of(values):\n    ...\n```\n"
A_NOTE = CELL + "```hint\nafter: soon\nX.\n```\n"  # an unreadable after: is a note


@pytest.fixture()
def run(repo, monkeypatch, capsys):
    monkeypatch.setattr(b, "NOTES_AT_END", False)  # main() sets it; put it back after
    monkeypatch.setattr(b, "SOURCE_MAP", True)

    def go(*flags):
        monkeypatch.setattr(sys, "argv", ["build.py", "--no-standalone", *flags])
        code = b.main()
        out, err = capsys.readouterr()
        return code, out, err
    return go


def test_a_build_prints_a_summary_and_then_its_notes_together(repo, run):
    write(repo, A_NOTE)
    code, out, err = run()
    assert code == 0
    assert out.strip().endswith("into site/") and "wrote " not in out
    assert err.index("1 note: the build carried on") < err.index("has a term I cannot read")
    assert err.count("has a term I cannot read") == 1


def test_verbose_gives_each_page_and_each_note_as_it_happens(repo, run):
    write(repo, A_NOTE)
    code, out, err = run("-v")
    assert code == 0 and "wrote site/tutorials/sample.html" in out
    assert "has a term I cannot read" in err and "the build carried on" not in err


def test_a_build_with_nothing_to_say_prints_only_its_summary(repo, run):
    write(repo, "Prose.\n")
    code, out, err = run()
    assert code == 0 and "into site/" in out and err == ""


def test_a_failing_build_still_shows_the_notes_before_the_failure(repo, run):
    write(repo, A_NOTE + "```solution\nraise ValueError('the page is wrong')\n```\n")
    code, out, err = run()
    assert code == 1
    assert err.index("has a term I cannot read") < err.index("build failed")
