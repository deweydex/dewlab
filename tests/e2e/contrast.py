"""WCAG contrast math, shared by every test that measures a real rendered
colour against its background rather than trusting a value in the CSS.
Written once here after it turned up copy-pasted, function for function,
between test_contrast.py and an earlier version of test_highlight_wrapping.py.
"""

from __future__ import annotations


def _channel(value):
    v = value / 255
    return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4


def relative_luminance(rgb):
    r, g, bl = (_channel(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * bl


def contrast_ratio(fg, bg):
    """WCAG's own formula, so the number here is the number that is cited."""
    high, low = sorted((relative_luminance(fg), relative_luminance(bg)), reverse=True)
    return (high + 0.05) / (low + 0.05)


def parse_rgb(value):
    inner = value[value.index("(") + 1:value.index(")")]
    return tuple(int(float(part)) for part in inner.split(",")[:3])


AA_MINIMUM = 4.5
