"""Two helpers the browser tests share for writing a site in the layout
build.py reads: `tutorials/<id>/<id>.md`, and one course file per course
under `courses/`."""

from __future__ import annotations

from pathlib import Path


def write_tutorial(root: Path, slug: str, text: str) -> Path:
    path = root / "tutorials" / slug / f"{slug}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    return path


def write_course(root: Path, course: str, series_title: str, ids: list[str],
                 title: str | None = None) -> Path:
    path = root / "courses" / f"{course}.yaml"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        f"title: {title or course.replace('-', ' ').title()}\n"
        f"contents:\n  - title: {series_title}\n    tutorials:\n"
        + "".join(f"      - {i}\n" for i in ids)
    )
    return path
