"""A closer's challenge (#316): a ```python challenge fence opens in the
Notebook, and ```html/css/js challenge fences side by side open in the
Workspace as one site. The build shows the starter read-only and writes a
link that carries it in its address, relative to the page's own depth."""

from __future__ import annotations

import json
import re
import urllib.parse

import pytest

from helpers import *  # noqa: F401,F403
from helpers import b

PYTHON = "```python challenge\n# Never below zero.\ntotal = 0\n```\n"
WEB = ('```html challenge\n<p id="n">0</p>\n```\n\n'
       "```css challenge\n#n { color: teal; }\n```\n\n"
       '```js challenge\ndocument.getElementById("n").textContent = 1;\n```\n')


def links(page: str) -> list[tuple[str, dict]]:
    found = re.findall(r'class="dl-btn dl-challenge-open" href="([^"]+)"', page)
    return [(href.split("#", 1)[0],
             json.loads(urllib.parse.unquote(href.split("#challenge=", 1)[1])))
            for href in (h.replace("&amp;", "&") for h in found)]


class TestRendering:
    def test_a_python_starter_opens_in_the_notebook_named_after_the_page(self, repo):
        write(repo, "# A Title\n\n" + PYTHON)
        b.build()
        page = built(repo)
        assert '<div class="dl-challenge" data-target="notebook">' in page
        assert ">Open it in the Notebook</a>" in page
        [(where, starter)] = links(page)
        assert where == "../compose/notebook.html"
        assert starter == {"name": "sample", "page": "A Title",
                           "code": "# Never below zero.\ntotal = 0"}

    def test_the_starter_shows_read_only_and_is_not_a_cell(self, repo):
        write(repo, PYTHON)
        b.build()
        page = built(repo)
        assert '<pre class="dl-static" data-lang="python"><code># Never below zero.' in page
        assert manifest(page)["cells"] == []
        assert '<button type="button" class="dl-btn dl-challenge-save" hidden>' in page
        assert "dlroot:" not in page

    def test_html_css_and_js_side_by_side_are_one_site(self, repo):
        write(repo, WEB)
        b.build()
        page = built(repo)
        [(where, starter)] = links(page)
        assert where == "../compose/workspace.html"
        assert starter["html"] == '<p id="n">0</p>'
        assert starter["css"] == "#n { color: teal; }"
        assert starter["js"].startswith("document.getElementById")
        assert page.count('class="dl-static"') == 3

    def test_a_missing_part_is_empty(self, repo):
        write(repo, "```css challenge\np { color: teal; }\n```\n")
        b.build()
        [(_, starter)] = links(built(repo))
        assert starter["html"] == "" and starter["js"] == ""

    def test_prose_between_them_makes_two_challenges(self, repo):
        write(repo, "```html challenge\n<p>One</p>\n```\n\nAnd another.\n\n"
                    "```html challenge\n<p>Two</p>\n```\n\n" + PYTHON)
        b.build()
        found = links(built(repo))
        assert [where for where, _ in found] == ["../compose/workspace.html",
                                                 "../compose/workspace.html",
                                                 "../compose/notebook.html"]


class TestMistakes:
    @pytest.mark.parametrize("body, match", [
        ("```sql challenge\nselect 1;\n```\n", "not one of python, html, css, js"),
        ("```css challenge\np {}\n```\n\n```css challenge\na {}\n```\n", "two css starters"),
    ])
    def test_the_build_says_what_is_wrong(self, repo, body, match):
        write(repo, body)
        with pytest.raises(b.BuildError, match=match):
            b.build()
