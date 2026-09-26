"""The predict block (#313): a ```predict fence after a cell becomes a
guess drawn above that cell, and a page with any has a surprises section at
its end for the runtime to fill. Two new hint signals go with it: `unsure`
and `guess differed`."""

from __future__ import annotations

import re

import pytest

from helpers import *  # noqa: F401,F403
from helpers import b

CELL = """```python exec
id: spending
spent = 0
for day in [3, 4, 5]:
    spent = spent + day
print(spent)
```
"""

CHOICE = """```predict
What will the last line print?

- 12
  - The total starts once, before the loop, and every day adds to it.
- 5
  - This is what you would see if the total started again each time round.
    [A closer look](https://example.org/closer)
- Something else
```
"""


def cell_spec(page: str, ident: str) -> dict:
    return next(c for c in manifest(page)["cells"] if c["id"] == ident)


class TestRendering:
    def test_the_guess_is_drawn_above_its_cell(self, repo):
        write(repo, CELL + CHOICE)
        b.build()
        page = built(repo)
        assert page.index('class="dl-predict"') < page.index('data-cell-id="spending"')
        assert 'id="dl-predict-spending"' in page

    def test_a_choice_is_radio_buttons_with_each_note_hidden_until_the_run(self, repo):
        write(repo, CELL + CHOICE)
        b.build()
        page = built(repo)
        assert page.count('type="radio" name="dl-predict-spending"') == 3
        assert '<span class="dl-predict-option-text">12</span>' in page
        notes = re.findall(r'<div class="dl-predict-note" data-option="(\d)" hidden>(.*?)</div>', page)
        assert [n for n, _ in notes] == ["0", "1"]
        assert 'href="https://example.org/closer"' in notes[1][1]

    def test_the_three_ways_of_being_sure_and_the_route_when_not(self, repo):
        write(repo, CELL + CHOICE)
        b.build()
        page = built(repo)
        for key in ("sure", "hunch", "unsure"):
            assert f'data-sure="{key}"' in page
        assert "I’m not sure yet" in page
        assert "Make a guess now" in page and "Run it and see" in page
        assert "Guess first, or just run it." in page

    def test_a_number_has_a_box_and_its_tolerance(self, repo):
        write(repo, CELL + "```predict\ntype: number\ntolerance: 0.5\n\nHow much?\n```\n")
        b.build()
        page = built(repo)
        assert 'data-type="number" data-tolerance="0.5"' in page
        assert 'class="dl-predict-value" inputmode="decimal"' in page

    def test_with_no_list_it_is_a_sentence(self, repo):
        write(repo, CELL + "```predict\nWhat will `spent` hold at the end?\n```\n")
        b.build()
        page = built(repo)
        assert 'data-type="text"' in page
        assert cell_spec(page, "spending")["predict"] == "text"

    def test_a_page_with_a_guess_ends_with_its_surprises(self, repo):
        write(repo, CELL + CHOICE)
        b.build()
        page = built(repo)
        assert '<section class="dl-surprises" hidden' in page
        assert page.index("dl-surprises") > page.index('data-cell-id="spending"')

    def test_a_page_without_one_has_none(self, repo):
        write(repo, CELL)
        b.build()
        assert "dl-surprises" not in built(repo)

    def test_no_word_in_the_block_judges(self, repo):
        write(repo, CELL + CHOICE)
        b.build()
        block = built(repo).split('<div class="dl-predict"')[1].split('<div class="dl-cell"')[0]
        for word in ("correct", "wrong", "not yet", "right answer", "incorrect"):
            assert word not in block.lower()


class TestSignals:
    @pytest.mark.parametrize("after, canonical", [
        ("unsure", "unsure:1"),
        ("not sure", "unsure:1"),
        ("guess differed", "guess-differed:1"),
        ("2 guess differed", "guess-differed:2"),
        ("unsure and 3 errors", "unsure:1 errors:3"),
    ])
    def test_a_hint_can_wait_for_either_moment(self, repo, after, canonical):
        write(repo, CELL + CHOICE + f"```hint\nafter: {after}\nWhich line runs first?\n```\n")
        b.build()
        assert f'data-after="{canonical}"' in built(repo)


class TestMistakes:
    @pytest.mark.parametrize("body, match", [
        (CHOICE, "no exec cell above it"),
        (CELL + CHOICE.replace("```predict\n", "```predict\nfor: nowhere\n"), "does not have: 'nowhere'"),
        (CELL + "```predict\ntype: essay\n\nWhy?\n```\n", "type: essay"),
        (CELL + "```predict\ntype: choice\n\nWhich?\n```\n", "no options"),
        (CELL + "```predict\nWhich?\n\n- only one\n```\n", "offers one option"),
        (CELL + "```predict\ntolerance: 1\n\nWhich?\n\n- a\n- b\n```\n", "only a `type: number`"),
        (CELL + "```predict\ntype: number\ntolerance: lots\n\nHow many?\n```\n", "write a number"),
        (CELL + "```predict\nWhich?\n\n- a\n- b\nstray words\n```\n", "neither an option"),
        (CELL + "```predict\nWhich?\n\n- a long option\n  that wraps\n- b\n```\n", None),
        (CELL + "```predict\n- a\n- b\n```\n", "asks no question"),
        (CELL + CHOICE + CHOICE, "two predict blocks"),
    ])
    def test_the_build_says_what_is_wrong(self, repo, body, match):
        write(repo, body)
        if match is None:  # a wrapped option is not a mistake: it builds
            b.build()
            assert "a long option that wraps</span>" in built(repo)
            return
        with pytest.raises(b.BuildError, match=match):
            b.build()
