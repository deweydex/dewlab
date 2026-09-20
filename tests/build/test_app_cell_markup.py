"""An `html app`/`css app`/`js app` fence: a full-stack cell whose
JavaScript can reach the page's own shared `db`. Shares its fence
grammar with a site editor — `id:`/`app:` headers,
consecutive panes grouped by name — but is a separate cell kind rather than
a third site-pane language, since a site editor's sandboxed iframe exists
specifically to block the channel this needs."""

from __future__ import annotations

import pytest

from helpers import *  # noqa: F401,F403
from helpers import CELL, b


APP_HTML = """```html app
id: reader-html
app: reader
<ul id="list"></ul>
```
"""


APP_CSS = """```css app
id: reader-css
app: reader
li { color: red; }
```
"""


APP_JS = """```js app
id: reader-js
app: reader
const rows = await dlQuery("SELECT name FROM readers");
console.log(rows);
```
"""


class TestAppCells:
    """Scenarios: a js pane alone (the only pane a full-stack cell actually
    requires); all three panes together; two different cells with a cell
    between them; and the headers, groupings and manifest keys that follow
    or fail the build the same way a site editor's own do."""

    def test_a_solo_js_pane_becomes_a_cell_whose_starter_code_travels_in_the_manifest(self, repo):
        write(repo, APP_JS)
        b.build()
        page = built(repo)
        assert 'class="dl-app-cell" data-app-name="reader"' in page
        assert 'data-lang="js"' in page
        assert 'class="dl-editor"' in page
        # html and css panes are optional — the js pane needed neither.
        assert 'data-lang="html"' not in page
        assert 'data-lang="css"' not in page
        cells = manifest(page)["appCells"]
        assert cells == [{
            "name": "reader",
            "panes": {"js": {
                "id": "reader-js",
                "code": 'const rows = await dlQuery("SELECT name FROM readers");\nconsole.log(rows);',
            }},
        }]
        # A full-stack cell needs sqlite even with no sql exec cell at all.
        assert manifest(page)["needsSqlite"] is True

    def test_three_consecutive_panes_share_one_cell_with_a_run_button(self, repo):
        write(repo, APP_HTML + APP_CSS + APP_JS)
        b.build()
        page = built(repo)
        assert page.count('data-app-name="reader"') == 1
        assert page.count('class="dl-app-pane"') == 3
        assert "dl-btn-app-run" in page
        assert "dl-btn-app-clear" in page

    @pytest.mark.parametrize(
        "body,match",
        [
            (APP_HTML + APP_CSS, "has no js pane"),
            ("```php app\nid: c\napp: reader\n<?php ?>\n```\n", "not one of"),
            ("```js app\napp: reader\nconsole.log(1);\n```\n", "no `id:` line"),
            ("```js app\nid: c\nconsole.log(1);\n```\n", "no `app:` line"),
            (APP_JS + "```js app\nid: reader-js-2\napp: reader\nconsole.log(2);\n```\n",
             "two js panes"),
            (APP_HTML + "\ntext in between\n\n" + APP_JS, "not consecutive"),
            ("```js app\nid: dup\napp: reader\nconsole.log(1);\n```\n\n"
             "```python exec\nid: dup\nprint(1)\n```\n", "share the id"),
        ],
        ids=[
            "no-js-pane", "unknown-language", "no-id", "no-app-name",
            "duplicate-language", "non-consecutive", "id-collides-with-a-cell",
        ],
    )
    def test_a_broken_pane_or_header_fails_the_build(self, repo, body, match):
        write(repo, body)
        with pytest.raises(b.BuildError, match=match):
            b.build()

    def test_two_different_cells_with_a_cell_between_them_both_render_unconfused(self, repo):
        write(repo, APP_JS + CELL + "```js app\nid: aside-js\napp: aside\nconsole.log(2);\n```\n")
        b.build()
        page = built(repo)
        assert 'data-app-name="reader"' in page
        assert 'data-app-name="aside"' in page
        assert [c["name"] for c in manifest(page)["appCells"]] == ["reader", "aside"]
        assert manifest(page)["cells"][0]["id"] == "only-cell"

    def test_a_tutorial_with_no_app_cells_carries_no_appcells_key(self, repo):
        write(repo, CELL)
        b.build()
        assert "appCells" not in manifest(built(repo))
