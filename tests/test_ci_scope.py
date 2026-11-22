"""dev/ci_scope.py: which CI jobs a change can affect. A wrong answer here
is a job that did not run on a change that broke it, so the cases below are
the kinds of change this repository sees."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "dev"))
import ci_scope  # noqa: E402


@pytest.mark.parametrize("files, code, browser, bundle", [
    # Words only: the house-style reports, nothing else.
    (["docs/FAQ.md", "README.md", "planning/EXERCISES.md", ".claude/skills/x/SKILL.md"], False, False, False),
    # A tutorial or a course: the build, the solutions and the glossary, but
    # no browser test reads one, and no bundle is made from one.
    (["tutorials/first-steps/first-steps.md", "courses/computational-methods.yaml"], True, False, False),
    (["tutorials/a/a.glossary.yaml"], True, False, False),
    # Tooling no page depends on.
    (["dev/check_video_links.py", "check.py", "new.py", "ruff.toml", "requirements-dev.txt"], True, False, False),
    (["builder/solutions.py", "builder/solution_runner.py", "builder/serve.py", "builder/downloads.py"], True, False, False),
    # What a page is built from, and what a browser runs.
    (["assets/tutorial-style.css"], True, True, False),
    (["assets/shell.html"], True, True, False),
    (["assets/tutorial-runtime.js"], True, True, True),
    (["assets/vendor/standalone.bundle.js"], True, True, True),
    (["vendor-src/package.json"], True, True, True),
    (["builder/main.py"], True, True, False),
    (["builder/finding.py", "builder/config.py"], True, True, False),
    (["build.py"], True, True, False),
    (["compose/dewmini.js"], True, True, False),
    (["pages/about.md"], True, True, False),
    (["data/co2-emissions.csv"], True, True, False),
    (["setup/cube.py"], True, True, False),
    (["tests/e2e/test_map.py"], True, True, False),
    # The curriculum files the build reads count as code; only the three the
    # page smoke test reads reach the browser.
    (["planning/curriculum/outcomes.yaml"], True, True, False),
    (["planning/curriculum/review/pairs/x.md"], True, False, False),
    (["planning/feedback.yaml"], True, False, False),
    # CI's own definition runs everything it defines.
    ([".github/workflows/tests.yml"], True, True, True),
    (["dev/ci_scope.py"], True, True, True),
    (["dev/shard.py"], True, True, True),
    ([".github/workflows/video-links.yml"], True, False, False),
    # A mixed change is as large as its largest part.
    (["docs/FAQ.md", "assets/tutorial-style.css"], True, True, False),
    (["tutorials/a/a.md", "dev/x.py"], True, False, False),
    ([], False, False, False),
])
def test_what_a_change_runs(files, code, browser, bundle):
    assert ci_scope.scope(files) == {"code": code, "browser": browser, "bundle": bundle}


def test_it_prints_the_lines_a_workflow_appends_to_its_outputs(tmp_path, capsys):
    listing = tmp_path / "changed.txt"
    listing.write_text("tutorials/a/a.md\n\ndocs/FAQ.md\n")
    assert ci_scope.main(["ci_scope.py", str(listing)]) == 0
    assert capsys.readouterr().out.split() == ["code=true", "browser=false", "bundle=false"]
