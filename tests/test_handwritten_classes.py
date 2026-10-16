"""Every `dl-` class an author writes by hand has a rule behind it.

A tutorial can write raw HTML in its body — a hint fold, a section
wrapper, a diagram built out of the thing it describes (`.dl-boxmodel`
and the rest of the `.dl-drawn` family). Python-Markdown passes that
through untouched and the build never looks at the class names, so a
renamed or mistyped one produces a page that is valid, silent, and
unstyled: nested divs with no colours and no layout, which reads as a
stack of empty boxes rather than as a broken reference.

This is the only thing standing between that and a reader, so it scans
the real content rather than a fixture.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent

# A fenced block is what a cell's own code lives in — a site editor's
# `<div class="box">`, or a runtime class a page happens to quote — and
# none of it is markup the build puts on the page.
FENCE_RE = re.compile(r"^```.*?^```", re.S | re.M)
CLASS_ATTR_RE = re.compile(r'class="([^"]*)"')
CSS_SELECTOR_RE = re.compile(r"\.(dl-[A-Za-z0-9_-]+)")


def _defined() -> set[str]:
    return set(CSS_SELECTOR_RE.findall((REPO / "assets/tutorial-style.css").read_text()))


def _used(root: Path = REPO) -> dict[str, list[Path]]:
    sources: dict[str, list[Path]] = {}
    files = sorted((root / "tutorials").rglob("*.md")) + sorted((root / "pages").glob("*.md"))
    for path in files:
        body = FENCE_RE.sub("", path.read_text())
        for attr in CLASS_ATTR_RE.findall(body):
            for name in attr.split():
                if name.startswith("dl-"):
                    sources.setdefault(name, []).append(path.relative_to(root))
    return sources


@pytest.mark.advisory
def test_every_hand_written_dl_class_is_styled():
    defined = _defined()
    missing = {
        name: paths for name, paths in _used().items() if name not in defined
    }
    assert not missing, "\n".join(
        f"{name} is written in {', '.join(str(p) for p in paths)} "
        "but assets/tutorial-style.css has no rule for it"
        for name, paths in sorted(missing.items())
    )


def test_the_scan_finds_markup_classes_and_skips_fenced_code(tmp_path):
    # Guards the scanner itself: a regex that quietly stopped matching would
    # make the test above pass on everything, including a real break.
    page = tmp_path / "tutorials" / "a" / "a.md"
    page.parent.mkdir(parents=True)
    page.write_text('<div class="dl-boxmodel x">\n\n```html\n<p class="dl-in-code">\n```\n')
    used = _used(tmp_path)
    assert used == {"dl-boxmodel": [Path("tutorials/a/a.md")]}
