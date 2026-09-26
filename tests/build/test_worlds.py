"""World variants (#315): a task written once per world, inside a
`<div class="dl-world" data-world="…">`, on a page whose `worlds:`
frontmatter says which worlds it offers. The build converts the markdown
inside, gives each variant its group and its world's name, puts a chooser
under the title, and holds each variant's cells and blocks to their
world."""

from __future__ import annotations

import re

import pytest

from helpers import *  # noqa: F401,F403
from helpers import b

WORLDS = """worlds:
  planets: The planets of the solar system.
  sea-floor: A submersible's dive. The numbers are made up.
"""


def page(repo, body: str, worlds: str = WORLDS) -> None:
    """write(), with `worlds` added to the end of the frontmatter."""
    path = write(repo, body)
    head, rest = path.read_text().split("\n---\n", 1)
    path.write_text(f"{head}\n{worlds}---\n{rest}")


def variant(world: str, body: str) -> str:
    return f'<div class="dl-world" data-world="{world}">\n\n{body}\n</div>\n\n'


TASK = variant("planets", "How wide are the *giants*?\n\n```python exec\nid: task--planets\n"
                          "giants = [142984, 120536]\n```\n") + \
       variant("sea-floor", "How deep is the **dive**?\n\n```python exec\nid: task--sea-floor\n"
                            "drops = [540, 610]\n```\n")
SHARED = "```python exec\nid: shared\nstart = 0\n```\n\n"


class TestRendering:
    def test_the_chooser_sits_under_the_title_hidden_until_the_runtime_wires_it(self, repo):
        page(repo, "# A page\n\n" + SHARED + TASK)
        b.build()
        html = built(repo)
        assert html.index("</h1>") < html.index('<fieldset class="dl-world-chooser" hidden>')
        assert html.index("dl-world-chooser") < html.index('data-cell-id="shared"')
        assert '<input type="radio" name="dl-world" value="planets">' in html
        assert '<span class="dl-world-name">Sea floor</span>' in html
        assert "A submersible&#x27;s dive" in html or "A submersible's dive" in html

    def test_markdown_inside_a_variant_is_converted(self, repo):
        page(repo, "# A page\n\n" + TASK)
        b.build()
        html = built(repo)
        assert "<em>giants</em>" in html and "<strong>dive</strong>" in html

    def test_each_variant_has_its_group_and_its_worlds_name(self, repo):
        page(repo, "# A page\n\n" + TASK + SHARED + variant(
            "planets", "```python exec\nid: later--planets\nx = 1\n```\n"))
        b.build()
        html = built(repo)
        assert ('<div class="dl-world" data-world="planets" data-world-group="0">'
                '<p class="dl-world-label">Planets</p>') in html
        assert '<div class="dl-world" data-world="sea-floor" data-world-group="0">' in html
        assert '<div class="dl-world" data-world="planets" data-world-group="1">' in html

    def test_each_variant_counts_from_the_same_number(self, repo):
        page(repo, "# A page\n\n" + SHARED + TASK + SHARED.replace("shared", "after"))
        b.build()
        html = built(repo)
        numbers = re.findall(r'data-cell-id="([^"]+)".*?dl-cell-pill-num">([^<]+)<', html)
        assert numbers == [("shared", "Cell 1"), ("task--planets", "Cell 2"),
                           ("task--sea-floor", "Cell 2"), ("after", "Cell 3")]

    def test_a_page_that_lists_worlds_and_has_no_variants_has_no_chooser(self, repo):
        page(repo, "# A page\n\n" + SHARED)
        b.build()
        assert "dl-world-chooser" not in built(repo)

    def test_a_div_inside_a_code_example_does_not_close_the_variant(self, repo):
        example = "```html\n<div>\n</div>\n</div>\n```\n"
        page(repo, "# A page\n\n" + variant("planets", example + "```python exec\n"
                                                         "id: t--planets\nx = 1\n```\n"))
        b.build()
        assert 'data-world="planets" data-world-group="0"' in built(repo)


class TestMistakes:
    @pytest.mark.parametrize("body, worlds, match", [
        (TASK, "", "no `worlds:` in its frontmatter"),
        (variant("dinosaurs", "Hi."), WORLDS, "world 'dinosaurs', which is not in"),
        (variant("planets", "```python exec\nid: task\nx = 1\n```\n"), WORLDS,
         "ends in `--planets`"),
        (SHARED + variant("planets", "```hint\nfor: shared\nLook again.\n```\n"), WORLDS,
         "a hint in the 'planets' variant belongs to cell 'shared'"),
        (TASK + "```hint\nfor: task--planets\nLook again.\n```\n", WORLDS,
         "outside every world variant belongs to cell 'task--planets'"),
        (TASK + "```python exec\nid: mine\ntests: task--planets\n```\n", WORLDS,
         "different worlds"),
        ('<div class="dl-world" data-world="planets">\n\n'
         + variant("sea-floor", "Hi.") + "</div>\n", WORLDS, "starts inside"),
        ('<div class="dl-world" data-world="planets">\n\nHi.\n', WORLDS, "no </div>"),
        (variant("planets", "One.") + variant("planets", "Two."), WORLDS, "side by side"),
        ("Hi.\n", "worlds:\n  Big Planets: nope\n", "not a key like"),
        ("Hi.\n", "worlds:\n  planets: ''\n", "no line saying"),
        (variant("planets", "One.") + 'Two. <div class="dl-world" data-world="planets">\n\nHi.\n\n</div>\n',
         WORLDS, "a line of its own"),
    ])
    def test_the_build_says_what_is_wrong(self, repo, body, worlds, match):
        page(repo, "# A page\n\n" + body, worlds)
        with pytest.raises(b.BuildError, match=re.escape(match)):
            b.build()


class TestSolutionsPerWorld:
    """check_solutions() runs a page once per world, with the cells a reader
    in that world would run."""

    def test_a_worlds_solution_does_not_see_another_worlds_cells(self, repo):
        body = (variant("planets", "```python exec\nid: t--planets\ngiants = [1]\n```\n")
                + variant("sea-floor", "```python exec\nid: t--sea-floor\ndrops = [2]\n```\n\n"
                                       "```solution\nprint(len(giants))\n```\n"))
        page(repo, "# A page\n\n" + body)
        with pytest.raises(b.BuildError, match="raised NameError"):
            b.build()

    def test_each_worlds_solution_sees_the_shared_cells_and_its_own(self, repo):
        body = SHARED + (
            variant("planets", "```python exec\nid: t--planets\ngiants = [1]\n```\n\n"
                               "```solution\nprint(start + sum(giants))\n```\n")
            + variant("sea-floor", "```python exec\nid: t--sea-floor\ndrops = [2]\n```\n\n"
                                   "```solution\nprint(start + sum(drops))\n```\n"))
        page(repo, "# A page\n\n" + body)
        b.build()
