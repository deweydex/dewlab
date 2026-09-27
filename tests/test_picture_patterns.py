"""The pattern layer `dev/graphics/palette.py` adds to a tinted picture.

A reader who cannot tell the tints apart turns on "Patterns in pictures"
(DECISIONS_LOG 7.283); these check what the generator writes for that
setting to show. The stylesheet's half, that the layer stays hidden until
the setting or high contrast is on, is checked in the browser tests.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "dev" / "graphics"))

from palette import FILL_AMBER, FILL_BLUE, FILL_GREEN, add_patterns  # noqa: E402

PICTURE = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">'
    f'<rect x="0" y="0" width="30" height="30" fill="{FILL_AMBER}" stroke="#333" stroke-width="2"/>'
    f'<rect x="40" y="0" width="30" height="30" fill="{FILL_BLUE}"/>'
    f'<path d="M0 50 H30 V80 Z" fill="{FILL_GREEN}"/>'
    '<rect x="0" y="90" width="30" height="5" fill="none" stroke="#333"/>'
    '</svg>'
)


def overlays(svg: str) -> list[str]:
    return re.findall(r'<[^>]*class="dl-pattern"[^>]*>', svg)


def test_each_tinted_shape_gets_one_hidden_patterned_copy():
    patterned = add_patterns(PICTURE, "dlp-test")
    copies = overlays(patterned)
    assert len(copies) == 3
    assert all('aria-hidden="true"' in copy and 'stroke="none"' in copy for copy in copies)
    # The copy sits where its shape sits, and loses the shape's outline.
    assert '<rect x="0" y="0" width="30" height="30" fill="url(#dlp-test-stripes)"' in patterned
    assert "stroke-width" not in copies[0]


def test_each_tint_has_its_own_pattern_and_only_the_used_ones_are_defined():
    patterned = add_patterns(PICTURE, "dlp-test")
    ids = re.findall(r'<pattern id="([^"]+)"', patterned)
    assert ids == ["dlp-test-back-stripes", "dlp-test-cross", "dlp-test-stripes"]
    assert "dots" not in patterned


def test_the_tints_themselves_are_untouched():
    patterned = add_patterns(PICTURE, "dlp-test")
    without_layer = re.sub(r'<defs class="dl-pattern-defs">.*?</defs>', "", patterned)
    without_layer = re.sub(r'<[^>]*class="dl-pattern"[^>]*>', "", without_layer)
    assert without_layer == PICTURE


def test_a_picture_with_no_tints_comes_back_as_it_was():
    plain = '<svg viewBox="0 0 10 10"><rect width="10" height="10" fill="#fff"/></svg>'
    assert add_patterns(plain, "dlp-test") == plain


def test_a_bead_is_too_small_to_carry_a_pattern():
    beads = (
        '<svg viewBox="0 0 100 100">'
        f'<circle cx="10" cy="10" r="4" fill="{FILL_AMBER}"/>'
        f'<circle cx="50" cy="50" r="20" fill="{FILL_AMBER}"/>'
        '</svg>'
    )
    copies = overlays(add_patterns(beads, "dlp-test"))
    assert len(copies) == 1 and 'r="20"' in copies[0]


def test_every_picture_script_adds_the_pattern_layer():
    # A script that writes pictures without it would ship tints a reader
    # with the setting on cannot tell apart. `finished()` adds the layer,
    # and changes nothing in a picture with no tints, so every script
    # writes through it.
    graphics = Path(__file__).resolve().parent.parent / "dev" / "graphics"
    writers = [path for path in sorted(graphics.glob("*.py"))
               if "for relative, draw in sorted(DIAGRAMS.items())" in path.read_text()]
    assert len(writers) >= 14
    missing = [path.name for path in writers if "finished(relative, draw)" not in path.read_text()]
    assert missing == []


def test_no_two_pictures_share_a_pattern_id():
    # Several pictures are inlined on one page, where a shared id would let
    # one picture's pattern stand in for another's.
    tutorials = Path(__file__).resolve().parent.parent / "tutorials"
    owner: dict[str, Path] = {}
    for picture in sorted(tutorials.glob("*/*.svg")):
        for pattern_id in set(re.findall(r'<pattern id="([^"]+)"', picture.read_text())):
            assert pattern_id not in owner, f"{picture} and {owner[pattern_id]} share {pattern_id}"
            owner[pattern_id] = picture
    assert owner
