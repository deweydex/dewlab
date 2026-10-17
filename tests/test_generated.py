"""dev/generated.py: one command for "is every generated file current".

The real generators are checked by their own scripts; these use stand-in
commands to prove the runner's rules: which stale files fail, which are only
reported, that one that cannot be made always fails, and what --fix runs."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "dev"))

import generated  # noqa: E402


def exits(code: int) -> list[str]:
    return ["-c", f"import sys; sys.exit({code})"]


def writes(marker: Path) -> list[str]:
    return ["-c", f"open({str(marker)!r}, 'w').write('x')"]


@pytest.fixture()
def rows(monkeypatch, tmp_path):
    def use(*entries):
        monkeypatch.setattr(generated, "CHECKS", list(entries))
    return use


def test_everything_current_passes(rows, capsys):
    rows(("a", [exits(0)], [exits(0)], "blocks"), ("b", [exits(0)], [exits(0)], "reports"))
    assert generated.main([]) == 0
    assert capsys.readouterr().out.count("current") == 2


def test_a_stale_file_that_blocks_fails(rows, capsys):
    rows(("pair game", [exits(1)], [exits(0)], "blocks"))
    assert generated.main([]) == 1
    assert "STALE" in capsys.readouterr().out


def test_a_stale_file_that_is_only_reported_does_not_fail_unless_asked(rows, capsys):
    rows(("pictures", [exits(1)], [exits(0)], "reports"))
    assert generated.main([]) == 0
    assert "does not fail" in capsys.readouterr().out
    assert generated.main(["--all"]) == 1


def test_a_file_that_cannot_be_made_always_fails(rows, capsys):
    rows(("map", [exits(2)], [exits(0)], "reports"))
    assert generated.main([]) == 1
    assert "CANNOT BE MADE" in capsys.readouterr().out


def test_one_file_checked_by_several_commands_is_stale_if_any_is(rows):
    rows(("reports", [exits(0), exits(1), exits(0)], [exits(0)], "blocks"))
    assert generated.main([]) == 1


def test_fix_regenerates_only_the_stale_ones(rows, tmp_path, capsys):
    stale, current = tmp_path / "stale", tmp_path / "current"
    rows(("stale one", [exits(1)], [writes(stale)], "blocks"),
         ("current one", [exits(0)], [writes(current)], "blocks"))
    assert generated.main(["--fix"]) == 0
    assert stale.exists() and not current.exists()
    assert "fixed     stale one" in capsys.readouterr().out


def test_every_real_entry_names_scripts_that_exist():
    for name, checks, fixes, effect in generated.CHECKS:
        assert effect in ("blocks", "reports"), name
        for command in [*checks, *fixes]:
            assert (ROOT / command[0]).is_file(), f"{name}: {command[0]}"
