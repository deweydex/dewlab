"""A ```question fence: multiple-choice and fill-in-the-blank, the
header checks each type has, and the id space it shares with cells."""

from __future__ import annotations

import pytest

from helpers import *  # noqa: F401,F403
from helpers import b


MULTIPLE_CHOICE = """```question
id: right-angle
type: multiple-choice
correct: 2

Which of these is a right angle?

- 45 degrees
- 90 degrees
- 180 degrees
```
"""

FILL_IN_THE_BLANK = """```question
id: angle-names
type: fill-in-the-blank

An angle of 90 degrees is a {right angle|straight angle|acute angle}.
The {mitochondrion} is the site of aerobic respiration.
```
"""


class TestMultipleChoice:
    """The markup a multiple-choice question builds, and what the
    runtime reads off it: a prompt, one button per option in the order
    written, and the correct one marked by a data attribute rather than
    its position, so shuffling the buttons at runtime never disturbs
    which one is right."""

    def test_the_prompt_every_option_and_the_correct_one_reach_the_page(self, repo):
        write(repo, MULTIPLE_CHOICE)
        b.build()
        page = built(repo)
        assert 'class="dl-question" id="dl-question-right-angle"' in page
        assert 'data-question-id="right-angle"' in page
        assert 'data-question-type="multiple-choice"' in page
        assert "<p>Which of these is a right angle?</p>" in page
        # Three options, in the order written, none pre-marked but the
        # page's own answer, which `correct:` (or `answer:`) names. The
        # runtime shows it only when asked, and never as a verdict (#314).
        assert page.count('class="dl-question-option"') == 3
        assert '<button type="button" class="dl-question-option" data-option="1">45 degrees</button>' in page
        assert '<button type="button" class="dl-question-option" data-option="2" data-answer="true">90 degrees</button>' in page
        assert '<button type="button" class="dl-question-option" data-option="3">180 degrees</button>' in page
        assert page.count('data-answer="true"') == 1
        assert "data-correct" not in page
        # A button that asks for the page's answer, starting disabled
        # (nothing is chosen yet), and a closed feedback slot holding only
        # the line the runtime shows when the reader chose the same.
        assert ('<button type="button" class="dl-btn dl-question-check" disabled>'
                "Show the page\u2019s answer</button>") in page
        assert ('<div class="dl-question-feedback" hidden>'
                '<p class="dl-question-same" hidden>You chose the same as the page.</p></div>') in page

    def test_answer_names_the_pages_answer_and_notes_wait_hidden(self, repo):
        write(repo, "```question\nid: q\ntype: multiple-choice\nanswer: 2\n\n"
                     "Which is a right angle?\n\n"
                     "- 45 degrees\n  - Half of one: a square's corner cut in two.\n"
                     "- 90 degrees, the corner\n  of a square\n```\n")
        b.build()
        page = built(repo)
        # A plain indented line wraps its option; it is not a note.
        assert 'data-option="2" data-answer="true">90 degrees, the corner of a square</button>' in page
        assert ('<div class="dl-question-note" data-option="1" hidden>'
                "Half of one: a square's corner cut in two.</div>") in page
        assert 'data-option="2" hidden' not in page

    def test_markdown_and_escaping_survive_in_the_prompt_and_an_option(self, repo):
        write(repo, "```question\nid: q\ntype: multiple-choice\ncorrect: 1\n\n"
                     "Which prints `<b>`?\n\n"
                     "- `print(\"<b>\")`\n"
                     "- `print(\"&\")`\n```\n")
        b.build()
        page = built(repo)
        assert "Which prints <code>&lt;b&gt;</code>?" in page
        assert '<code>print("&lt;b&gt;")</code>' in page

    @pytest.mark.parametrize(
        "body,match",
        [
            ("```question\nid: q\ntype: multiple-choice\n\nQ?\n\n- a\n- b\n```\n",
             "no `answer:` line"),
            ("```question\nid: q\ntype: multiple-choice\ncorrect: 9\n\nQ?\n\n- a\n- b\n```\n",
             "does not name one of its 2 options"),
            ("```question\nid: q\ntype: multiple-choice\ncorrect: 1\n\nQ?\n\n- only one\n```\n",
             "fewer than two options"),
        ],
        ids=["no-correct-line", "correct-names-nothing", "too-few-options"],
    )
    def test_a_broken_correct_line_or_option_count_fails_the_build(self, repo, body, match):
        write(repo, body)
        with pytest.raises(b.BuildError, match=match):
            b.build()


class TestFillInTheBlank:
    """A sentence with `{...}` gaps: a plain typing box for a single
    word, a dropdown — first item correct — when the author offers a
    choice, both gaps checkable in one pass over the sentence they sit
    in."""

    def test_a_choice_gap_becomes_a_select_and_a_plain_gap_an_input(self, repo):
        write(repo, FILL_IN_THE_BLANK)
        b.build()
        page = built(repo)
        assert 'class="dl-question" id="dl-question-angle-names"' in page
        assert 'data-question-type="fill-in-the-blank"' in page
        # The select's first option is the correct one, marked the same
        # way a multiple-choice option is.
        assert ('<select class="dl-question-gap-select">'
                '<option data-answer="true">right angle</option>'
                '<option>straight angle</option>'
                '<option>acute angle</option></select>') in page
        # A gap with no "|" is a typing box, its expected word on the
        # input itself.
        assert '<input type="text" class="dl-question-gap-input" data-expected="mitochondrion"' in page
        # One Check for the whole sentence, not one per gap.
        assert page.count("dl-question-check") == 1

    def test_gaps_keep_the_sentence_around_them_and_their_own_order(self, repo):
        write(repo, "```question\nid: q\ntype: fill-in-the-blank\n\n"
                     "First {one}, then {two}.\n```\n")
        b.build()
        page = built(repo)
        prompt = page[page.index('dl-question-prompt'):page.index("dl-question-check")]
        assert prompt.index('data-expected="one"') < prompt.index('data-expected="two"')
        assert "First" in prompt and ", then" in prompt and "." in prompt

    @pytest.mark.parametrize(
        "body,match",
        [
            ("```question\nid: q\ntype: fill-in-the-blank\n\nNo gaps here.\n```\n",
             r"no \{\.\.\.\} gap"),
            ("```question\nid: q\ntype: fill-in-the-blank\n\nAn {unclosed gap.\n```\n",
             "unclosed"),
        ],
        ids=["no-gap", "unclosed-brace"],
    )
    def test_a_missing_or_unclosed_gap_fails_the_build(self, repo, body, match):
        write(repo, body)
        with pytest.raises(b.BuildError, match=match):
            b.build()


class TestQuestionChecks:
    """The checks any question fence gets, regardless of type: an id,
    a recognised type, and an id no cell or other question on the page
    already uses — cells and questions are one saved-work record."""

    @pytest.mark.parametrize(
        "body,match",
        [
            ("```question\ntype: multiple-choice\ncorrect: 1\n\nQ?\n\n- a\n- b\n```\n",
             "no `id:` line"),
            ("```question\nid: q\ntype: essay\n\nWrite an essay.\n```\n",
             "not one of"),
        ],
        ids=["missing-id", "unrecognised-type"],
    )
    def test_a_question_missing_its_id_or_naming_an_unknown_type_fails_the_build(self, repo, body, match):
        write(repo, body)
        with pytest.raises(b.BuildError, match=match):
            b.build()

    @pytest.mark.parametrize(
        "body",
        [
            "```python exec\nid: shared\n1\n```\n\n"
            "```question\nid: shared\ntype: multiple-choice\ncorrect: 1\n\nQ?\n\n- a\n- b\n```\n",
            "```question\nid: same\ntype: multiple-choice\ncorrect: 1\n\nQ?\n\n- a\n- b\n```\n\n"
            "```question\nid: same\ntype: fill-in-the-blank\n\n{gap}\n```\n",
        ],
        ids=["cell-vs-question", "question-vs-question"],
    )
    def test_an_id_shared_with_a_cell_or_another_question_fails_the_build(self, repo, body):
        write(repo, body)
        with pytest.raises(b.BuildError, match="shares its id"):
            b.build()

    def test_a_footnote_inside_a_question_fails_the_build(self, repo):
        # A question fence is converted on its own, so a footnote written
        # in one cannot reach the foot of the page -- see no_footnotes_in().
        write(repo, "```question\nid: q\ntype: multiple-choice\ncorrect: 1\n\n"
                    "Which one[^why]?\n\n- a\n- b\n```\n\n[^why]: Because.\n")
        with pytest.raises(b.BuildError, match="has a footnote in it"):
            b.build()

    def test_a_question_between_two_cells_leaves_neither_lost(self, repo):
        write(repo, "```python exec\nid: one\n1\n```\n\n"
                     + MULTIPLE_CHOICE +
                     "\n```python exec\nid: two\n2\n```\n")
        b.build()
        page = built(repo)
        cells = manifest(page)["cells"]
        assert [c["id"] for c in cells] == ["one", "two"]
        assert page.index('data-cell-id="one"') < page.index('id="dl-question-right-angle"')
        assert page.index('id="dl-question-right-angle"') < page.index('data-cell-id="two"')



class TestQuestionMaths:
    """convert_prose_with_math() — the same self-contained extract-then-
    place dance the tutorial body's own maths gets, applied here since a
    question's prompt and options convert on their own, with no shared
    page-level maths list to append to."""

    def test_maths_works_in_a_multiple_choice_prompt_and_option_and_in_a_fill_in_the_blank_sentence(
        self, repo
    ):
        write(repo, r"```question" "\n"
                    "id: q\n"
                    "type: multiple-choice\n"
                    "correct: 1\n\n"
                    r"Which equals $2^3$?" "\n\n"
                    r"- $8$" "\n"
                    "- $6$\n"
                    "```\n")
        b.build()
        page = built(repo)
        assert '<span class="dl-math">2^3</span>' in page
        assert '<button type="button" class="dl-question-option" data-option="1" data-answer="true"><span class="dl-math">8</span></button>' in page
        assert manifest(page)["math"] is True

        write(repo, "```question\nid: q\ntype: fill-in-the-blank\n\n"
                    r"When $r = 2$, the area is {four} times $\pi$." + "\n```\n")
        b.build()
        page = built(repo)
        assert '<span class="dl-math">r = 2</span>' in page
        assert '<span class="dl-math">\\pi</span>' in page
        assert 'data-expected="four"' in page

    def test_a_dollar_sign_inside_a_gap_is_not_mistaken_for_maths(self, repo):
        # Gaps are tokenised before convert_prose_with_math ever sees the
        # text, so a price offered as one of the choices is gone from
        # what maths extraction looks at.
        write(repo, "```question\nid: q\ntype: fill-in-the-blank\n\n"
                    "It costs {$5|$10}.\n```\n")
        b.build()
        page = built(repo)
        assert "dl-math" not in page
        assert "<option data-answer=\"true\">$5</option>" in page
