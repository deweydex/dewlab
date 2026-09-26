"""What every file in tests/build/ shares: the `repo` fixture (a temporary
tree build.py is pointed at, since it resolves paths from module-level
globals) and the helpers that write tutorials and course files into it in
the layout the build reads — `tutorials/<id>/<id>.md`, and one course file
per course under `courses/`.

The default course is `computational-methods`, with one series, "Python
fundamentals". `write()` lists every tutorial it has written there, so the
common one-tutorial test needs no course file of its own; `course()`
writes any other course; `set_order()` is the older name for putting a
list of ids under a series heading, kept because a hundred tests call it.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import pytest
import yaml

DEWLAB = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(DEWLAB))

import build as b  # noqa: E402

SHELL = (DEWLAB / "assets" / "shell.html").read_text()
ABOUT_PAGE = (DEWLAB / "pages" / "about.md").read_text()
HOME_PAGE = (DEWLAB / "pages" / "home.md").read_text()
FEATURES_PAGE = (DEWLAB / "pages" / "features.md").read_text()
# Every other page under pages/, copied as it is: the build writes each one
# SITE_PAGES lists, and fails on one without its file.
OTHER_PAGES = {path.name: path.read_text() for path in (DEWLAB / "pages").glob("*.md")
               if path.stem not in ("about", "home", "features")}

COURSE = "computational-methods"
SERIES = "python-fundamentals"

FRONTMATTER = """---
title: "A Title"
year: "2026-2027"
version: {version}
---

"""


@pytest.fixture()
def repo_with_assets(repo):
    # Separate from `repo`: copying the vendor bundles costs a moment, and
    # only the standalone-export tests need the real assets.
    import shutil

    shutil.rmtree(repo / "assets")
    shutil.copytree(DEWLAB / "assets", repo / "assets")
    return repo


def outside_style_and_script(page: str) -> str:
    """A standalone page with its inlined stylesheet and runtime cut out,
    since both name the site's own classes in their selectors."""
    page = re.sub(r"<style>.*?</style>", "", page, flags=re.DOTALL)
    return re.sub(r"<script>.*?</script>", "", page, flags=re.DOTALL)


@pytest.fixture()
def repo(tmp_path, monkeypatch):
    for name in ("tutorials", "courses", "setup", "data", "assets", "pages"):
        (tmp_path / name).mkdir(parents=True)
    (tmp_path / "assets" / "shell.html").write_text(SHELL)
    (tmp_path / "pages" / "about.md").write_text(ABOUT_PAGE)
    (tmp_path / "pages" / "home.md").write_text(HOME_PAGE)
    (tmp_path / "pages" / "features.md").write_text(FEATURES_PAGE)
    for name, text in OTHER_PAGES.items():
        (tmp_path / "pages" / name).write_text(text)

    monkeypatch.setattr(b, "ROOT", tmp_path)
    monkeypatch.setattr(b, "TUTORIALS", tmp_path / "tutorials")
    monkeypatch.setattr(b, "COURSES", tmp_path / "courses")
    monkeypatch.setattr(b, "SETUP", tmp_path / "setup")
    monkeypatch.setattr(b, "DATA", tmp_path / "data")
    monkeypatch.setattr(b, "ASSETS", tmp_path / "assets")
    monkeypatch.setattr(b, "SHELL", tmp_path / "assets" / "shell.html")
    monkeypatch.setattr(b, "OUT", tmp_path / "site")
    monkeypatch.setattr(b, "PAGES", tmp_path / "pages")
    course(tmp_path, COURSE, {}, title="Computational Methods")
    return tmp_path


# ------------------------------------------------------------------ courses

def series_title(key: str) -> str:
    """"python-fundamentals" → "Python fundamentals": the heading a key
    came from, for the tests that only ever knew the key."""
    return key.replace("-", " ").capitalize()


def read_course(repo: Path, ident: str) -> dict:
    path = repo / "courses" / f"{ident}.yaml"
    return yaml.safe_load(path.read_text()) if path.is_file() else {}


def save_course(repo: Path, ident: str, data: dict) -> Path:
    path = repo / "courses" / f"{ident}.yaml"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True))
    index = repo / "courses" / "index.yaml"
    listed = (yaml.safe_load(index.read_text()) or {}).get("order", []) if index.is_file() else []
    if ident not in listed:
        listed.append(ident)
        index.write_text("order:\n" + "".join(f"  - {c}\n" for c in listed))
    return path


def course(repo: Path, ident: str, series: dict[str, list[str]],
           title: str | None = None, mixed: list[str] | None = None, **fields) -> Path:
    """`courses/<ident>.yaml` from {"Series title": [ids, …]}, listed in
    `courses/index.yaml` (appended, if not there already)."""
    data = {
        "title": title or ident.replace("-", " ").title(),
        "code": fields.pop("code", "X1 · QQI Level 5"),
        "status": fields.pop("status", "beta"),
        "card": fields.pop("card", f"A card for {ident}."),
        "description": fields.pop("description", f"A description of {ident}."),
        **fields,
        "contents": [{"title": name, "tutorials": list(ids)} for name, ids in series.items()],
    }
    if mixed:
        data["mixed"] = list(mixed)
    return save_course(repo, ident, data)


def set_order(repo: Path, ident: str, series: str, ids: list[str]) -> Path:
    """Put `ids`, in that order, under the series `series` (a key such as
    python-fundamentals, or a title) of course `ident` — writing the course
    file, and the series heading, if either is new."""
    data = read_course(repo, ident)
    if not data:
        course(repo, ident, {})
        data = read_course(repo, ident)
    key = b.series_key(series)
    contents = data.setdefault("contents", [])
    for entry in contents:
        if b.series_key(entry["title"]) == key:
            entry["tutorials"] = list(ids)
            break
    else:
        contents.append({"title": series if series != key else series_title(key),
                         "tutorials": list(ids)})
    return save_course(repo, ident, data)


def set_series_order(repo: Path, ident: str, keys: list[str]) -> Path:
    """Reorder the course's series so that `keys` come first, in that order
    — the order a reference accumulates in (build.py's series_chain())."""
    data = read_course(repo, ident)
    by_key = {b.series_key(e["title"]): e for e in data.get("contents", [])}
    rest = [e for k, e in by_key.items() if k not in keys]
    data["contents"] = [by_key[k] for k in keys if k in by_key] + rest
    return save_course(repo, ident, data)


def set_mixed(repo: Path, ident: str, ids: list[str]) -> Path:
    data = read_course(repo, ident)
    data["mixed"] = list(ids)
    return save_course(repo, ident, data)


# ---------------------------------------------------------------- tutorials

def tutorial_path(repo: Path, slug: str, course: str | None = None) -> Path:
    """`tutorials/<slug>/<slug>.md`, folder made. `course` is accepted and
    ignored: where a tutorial sits is a course file's business, and a
    hundred older calls still pass one."""
    path = repo / "tutorials" / slug / f"{slug}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def is_practice_file(path: Path) -> bool:
    """A page no course file may list: a page of problems or a context page."""
    text = path.read_text()
    return "practice_for" in text or "practice_across" in text or "context_for" in text


def listed_tutorials(repo: Path) -> list[str]:
    """Every id with a file behind it and no practice or context line,
    sorted — what write() keeps the default course listing."""
    return sorted(
        folder.name for folder in (repo / "tutorials").iterdir()
        if folder.is_dir() and (folder / f"{folder.name}.md").is_file()
        and not is_practice_file(folder / f"{folder.name}.md")
    )


def write(repo: Path, body: str, slug: str = "sample",
          version: str = "2026.08.23.1") -> Path:
    path = tutorial_path(repo, slug)
    path.write_text(FRONTMATTER.format(version=version) + body)
    # Keep the default course listing whatever has been written so far.
    set_order(repo, COURSE, SERIES, listed_tutorials(repo))
    return path


def write_in_series(repo: Path, body: str, slug: str, series: str,
                     version: str = "2026.08.23.1") -> Path:
    """Like write(), but listed under another series of the default course
    — appended to that series, in the order written."""
    path = tutorial_path(repo, slug)
    path.write_text(FRONTMATTER.format(version=version) + body)
    data = read_course(repo, COURSE)
    key = b.series_key(series)
    already = next((e["tutorials"] for e in data.get("contents", [])
                    if b.series_key(e["title"]) == key), [])
    set_order(repo, COURSE, series, already + [slug])
    return path


def practice(repo: Path, slug: str, body: str = "**1.** A question.\n", **frontmatter) -> Path:
    """`tutorials/<slug>/<slug>-practice.md` with `practice_for: <slug>`
    unless `frontmatter` says otherwise (`practice_across=[…]` for a mixed
    set, written to its own folder `tutorials/<name>/<name>.md`)."""
    if "practice_across" in frontmatter:
        path = tutorial_path(repo, slug)
    else:
        frontmatter.setdefault("practice_for", slug)
        path = repo / "tutorials" / slug / f"{slug}-practice.md"
        path.parent.mkdir(parents=True, exist_ok=True)
    extra = "".join(
        f"{key}: {value}\n" if not isinstance(value, list)
        else f"{key}:\n" + "".join(f"  - {v}\n" for v in value)
        for key, value in frontmatter.items()
    )
    path.write_text(
        FRONTMATTER.format(version="2026.08.23.1").replace(
            "version: 2026.08.23.1\n", f"version: 2026.08.23.1\n{extra}")
        + body
    )
    return path


def built(repo: Path, slug: str = "sample") -> str:
    return (repo / "site" / "tutorials" / f"{slug}.html").read_text()


def glossary(repo: Path, slug: str, entries: list[dict]) -> Path:
    path = repo / "tutorials" / slug / f"{slug}.glossary.yaml"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.dump({"entries": entries}))
    return path


def asset(repo: Path, slug: str, name: str, content: bytes = b"x",
          course: str | None = None) -> Path:
    path = repo / "tutorials" / slug / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content)
    return path


def dataset(repo: Path, name: str, source: str = "Some source",
            license: str = "CC0", description: str = "A dataset.",
            with_csv: bool = True, with_txt: bool = False,
            with_attribution: bool = True) -> None:
    if with_csv:
        (repo / "data" / f"{name}.csv").write_text("a,b\n1,2\n")
    if with_txt:
        (repo / "data" / f"{name}.txt").write_text("Some plain text.\n")
    if with_attribution:
        (repo / "data" / f"{name}.yaml").write_text(
            f'source: "{source}"\nlicense: "{license}"\ndescription: "{description}"\n'
        )


def add_frontmatter(path: Path, extra: str) -> None:
    # write()'s frontmatter template has no room for fields most tests never need.
    path.write_text(path.read_text().replace("version:", f"{extra}version:", 1))


def manifest(page: str) -> dict:
    raw = re.search(r'id="dewlab-manifest">(.*?)</script>', page, re.S).group(1)
    return json.loads(raw)


CELL = """```python exec
id: only-cell
print("hello")
```
"""
