"""Where the build reads from and writes to, and its three switches.

One object, `cfg`, that every part of the build reads at the moment it needs
a path. A test points the build at a small site by changing `cfg` (all of it
with `cfg.use(folder)`, or one attribute), and nothing else has to know.
"""

from __future__ import annotations

from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


class Config:
    def __init__(self, root: Path = REPO):
        self.use(root)
        # When true, every page carries `data-md="START:END"` on each
        # top-level block, the byte range of the markdown file that produced
        # it (source_map.py), and its manifest says which file and blob that
        # is, which is what "Edit this page" works from. A build from the
        # command line turns it on (`--no-source-map` leaves it out). It is
        # off here so that code which calls load() or build() directly, the
        # tests above all, gets the plain page.
        self.SOURCE_MAP = False
        # Whether a page whose solutions ran clean is remembered
        # (builder/solutions.py), and whether a page that is remembered is
        # skipped. `check.py --no-cache` does neither, so every page runs and
        # nothing is kept; `--refresh-cache` runs every page and keeps what
        # was clean, which is how a push to main fills the cache that pull
        # requests start from.
        self.SOLUTION_CACHE = True
        self.SOLUTION_CACHE_REUSE = True
        # Whether notes are kept and printed together when the build ends
        # (the command line) or printed as they happen (everything else).
        self.NOTES_AT_END = False

    def use(self, root: Path, **others: Path) -> None:
        """Read from, and write under, `root`. A keyword names one folder to
        take from somewhere else: `use(tmp, ASSETS=REPO / "assets")`."""
        curriculum = root / "planning" / "curriculum"
        self.ROOT = root
        self.TUTORIALS = root / "tutorials"
        self.COURSES = root / "courses"
        self.SETUP = root / "setup"
        self.DATA = root / "data"
        self.ASSETS = root / "assets"
        self.COMPOSE = root / "compose"
        self.TOPIC_GAME = root / "topic_tree_game"
        self.TOPIC_EDITOR = root / "topic_editor"
        self.OUT = root / "site"
        self.PAGES = root / "pages"
        self.MATH_BASICS_DATA = curriculum / "math-basics.yaml"
        self.PYTHON_BASICS_DATA = curriculum / "python-basics.yaml"
        self.TOPIC_DATA = curriculum / "topics.yaml"
        self.SCOPE_DATA = curriculum / "out-of-scope.yaml"
        self.TOPIC_GROUPS_DATA = curriculum / "topic-groups.yaml"
        self.OUTCOME_DATA = curriculum / "outcomes.yaml"
        for name, path in others.items():
            if not hasattr(self, name):
                raise AttributeError(f"the build has no path called {name}")
            setattr(self, name, path)
        self.SHELL = others.get("SHELL", self.ASSETS / "shell.html")


cfg = Config()
