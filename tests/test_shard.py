"""dev/shard.py: the browser tests split across machines. A file left out of
every share is a test that never runs, so the rule that matters is that the
shares always add up to exactly the files given."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "dev"))
import shard  # noqa: E402


@pytest.fixture()
def files(tmp_path):
    sizes = {"big": 900, "mid_a": 400, "mid_b": 400, "small_a": 100, "small_b": 90, "tiny": 10}
    out = []
    for name, size in sizes.items():
        path = tmp_path / f"{name}.py"
        path.write_text("x" * size)
        out.append(str(path))
    return out


@pytest.mark.parametrize("count", [1, 2, 3, 4, 6, 9])
def test_every_file_is_in_exactly_one_share(files, count):
    dealt = shard.shares(files, count)
    assert len(dealt) == count
    assert sorted(f for share in dealt for f in share) == sorted(files)


def test_the_heaviest_file_gets_a_share_to_itself_while_the_rest_balance(files):
    dealt = shard.shares(files, 3)
    weights = [sum(Path(f).stat().st_size for f in share) for share in dealt]
    assert any(len(share) == 1 and Path(share[0]).name == "big.py" for share in dealt)
    assert max(weights) == 900  # no share is heavier than the one file that cannot be split
    assert sorted(weights)[:2] == [500, 500]  # and the rest are shared evenly


def test_the_same_files_always_give_the_same_shares_whatever_order_they_come_in(files):
    assert shard.shares(files, 3) == shard.shares(list(reversed(files)), 3)


def test_more_shares_than_files_leaves_some_empty_and_loses_none(files):
    dealt = shard.shares(files, 9)
    assert sum(1 for share in dealt if not share) == 3


def test_it_prints_one_share_a_line_and_refuses_a_share_that_does_not_exist(files, capsys):
    assert shard.main(["shard.py", "2", "1", *files]) == 0
    printed = capsys.readouterr().out.split()
    assert printed and set(printed) <= set(files)
    assert shard.main(["shard.py", "2", "3", *files]) == 1
    assert shard.main(["shard.py"]) == 1
