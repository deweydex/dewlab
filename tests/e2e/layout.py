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


def point_build_at(monkeypatch, root: Path) -> None:
    """Have the build read a test's own tutorials and courses from `root` and
    write its site there, with the real setup files, data, assets and shell:
    what a browser test of the real runtime wants."""
    import build as b

    real = b.REPO
    fresh = b.Config(root)
    fresh.use(root, SETUP=real / "setup", DATA=real / "data", ASSETS=real / "assets")
    for name in ("ROOT", "TUTORIALS", "COURSES", "OUT", "SETUP", "DATA", "ASSETS", "SHELL"):
        monkeypatch.setattr(b.cfg, name, getattr(fresh, name))
