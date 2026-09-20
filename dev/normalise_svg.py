"""Map an SVG's literal colours onto dewlab's theme tokens.

Serves two producers: graphviz/matplotlib output from our own generators, and
a draw.io export from a contributor.

draw.io needs more than a colour swap. A current export is already
theme-aware, but against the wrong signal: it writes `style="fill:
light-dark(rgb(0,0,0), rgb(255,255,255))"` and `var(--ge-adaptive-bg,
#ffffff)`. `light-dark()` resolves against the `color-scheme` property, which
follows the operating system — not dewlab's own `data-theme`, which a reader
sets in the settings panel and which is allowed to disagree with the OS. It
is also blind to `data-contrast="high"`. So a style property that would win
over the attribute beneath it gets stripped, and the attribute gets mapped.
"""
import re, sys, pathlib, colorsys

INK   = {"#000000", "#000", "black", "#1a1a1a", "#1b1b1f", "rgb(0, 0, 0)"}
PAPER = {"#ffffff", "#fff", "white", "#fdfcfa", "rgb(255, 255, 255)"}
MUTED = {"#5f6b7a", "#6b6b76", "#808080", "gray", "grey"}
RULE  = {"#e2ddd5", "#d6d6de", "#cccccc", "#ccc"}
CELL  = {"#f6f4f0", "#f1f1f6", "#fbfaf8"}

LOOKUP = {v.lower(): tok for group, tok in
          [(INK, "currentColor"), (PAPER, "var(--dl-bg)"), (MUTED, "var(--dl-muted)"),
           (RULE, "var(--dl-rule)"), (CELL, "var(--dl-cell-bg)")] for v in group}

HIGHLIGHT = ["var(--dl-highlight-bg)", "var(--dl-highlight-green)",
             "var(--dl-highlight-blue)", "var(--dl-highlight-pink)"]
TYPE_INK  = ["var(--dl-type-python)", "var(--dl-type-sql)",
             "var(--dl-type-css)", "var(--dl-type-js)"]

# Style properties that would override the presentation attribute beneath them.
COLOUR_PROPS = ("fill", "stroke", "color", "stop-color", "flood-color")
# Of those, the two that are also presentation attributes we can hoist into.
HOISTABLE = ("fill", "stroke")


def _bucket(hex_colour):
    r, g, b = (int(hex_colour[i:i + 2], 16) / 255 for i in (1, 3, 5))
    h, _, s = colorsys.rgb_to_hls(r, g, b)
    if s < 0.12:
        return None
    deg = h * 360
    return 0 if (deg < 70 or deg >= 330) else 1 if deg < 170 else 2 if deg < 260 else 3


def _first_argument(text):
    """The first comma-separated argument, counting nesting.

    `light-dark(rgb(0, 0, 0), rgb(255, 255, 255))` has commas inside its own
    first argument, so splitting on the first one finds `rgb(0`.
    """
    depth = 0
    for i, char in enumerate(text):
        if char == "(":
            depth += 1
        elif char == ")":
            if depth == 0:
                return text[:i]
            depth -= 1
        elif char == "," and depth == 0:
            return text[:i]
    return text


def _token(value, is_fill, unmapped):
    key = value.strip().lower()
    # draw.io writes `light-dark(light, dark)`, which resolves against
    # `color-scheme` — the operating system's preference, not the reader's
    # own `data-theme`. Take the light value and map it like any other.
    if key.startswith("light-dark("):
        key = _first_argument(key[len("light-dark("):]).strip()
    # A producer's own custom property is not a token of ours. Only pass
    # through a var() that already points at the site's palette.
    if key.startswith("var(--ge-") or key.startswith("var(--dl-"):
        if key.startswith("var(--dl-"):
            return value.strip()
        fallback = re.search(r",\s*([^)]+)\)", key)
        key = fallback.group(1).strip() if fallback else key
    if key in ("none", "transparent") or key == "currentcolor":
        return key
    key = re.sub(r"rgb\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)",
                 lambda m: "#%02x%02x%02x" % tuple(int(g) for g in m.groups()), key)
    if key in LOOKUP:
        return LOOKUP[key]
    if re.fullmatch(r"#[0-9a-f]{3}", key):
        key = "#" + "".join(c * 2 for c in key[1:])
    if re.fullmatch(r"#[0-9a-f]{6}", key):
        bucket = _bucket(key)
        if bucket is None:
            return "var(--dl-muted)"
        return (HIGHLIGHT if is_fill else TYPE_INK)[bucket]
    unmapped.add(value)
    return value


def _rewrite_tag(tag, unmapped):
    """Map a single element's colours, hoisting style declarations into
    attributes rather than deleting them.

    Deleting is the tempting shortcut and it is wrong. matplotlib writes
    almost everything as `style="fill: none; stroke: #000000"`, and a
    stripped `fill: none` leaves the element inheriting the root's fill —
    every outline becomes a filled blob. Hoisting keeps `none` meaning none.
    """
    style = re.search(r'\sstyle="([^"]*)"', tag)
    hoisted = {}
    if style:
        kept = []
        for decl in style.group(1).split(";"):
            if ":" not in decl:
                if decl.strip():
                    kept.append(decl)
                continue
            prop, value = decl.split(":", 1)
            name = prop.strip().lower()
            if name in HOISTABLE:
                hoisted[name] = _token(value, name == "fill", unmapped)
            elif name not in COLOUR_PROPS:
                kept.append(decl)
        replacement = f' style="{";".join(kept)}"' if any(d.strip() for d in kept) else ""
        tag = tag[:style.start()] + replacement + tag[style.end():]

    tag = re.sub(
        r'\s(fill|stroke)="([^"]+)"',
        lambda m: "" if m.group(1) in hoisted
        else f' {m.group(1)}="{_token(m.group(2), m.group(1) == "fill", unmapped)}"',
        tag)
    if hoisted:
        insert = "".join(f' {name}="{value}"' for name, value in sorted(hoisted.items()))
        tag = tag[:-2] + insert + "/>" if tag.endswith("/>") else tag[:-1] + insert + ">"
    return tag


def normalise(svg, unmapped=None):
    unmapped = set() if unmapped is None else unmapped
    cut = svg.index(">", svg.index("<svg")) + 1
    head, body = svg[:cut], svg[cut:]
    # draw.io ships a <style> block defining its own adaptive background
    # against color-scheme. Every reference to it is about to be rewritten,
    # so the block is dead, and leaving it invites it coming back to life.
    body = re.sub(r"<style[^>]*>.*?</style>", "", body, flags=re.S)
    body = re.sub(r"<[a-zA-Z][^>]*>",
                  lambda m: _rewrite_tag(m.group(0), unmapped), body)
    # `fill` is an inherited presentation attribute, and a producer omits it
    # wherever the colour is the SVG default of black. Nothing to rewrite, so
    # the text stays black and disappears on a dark background while the
    # checker reports every colour mapped. Setting the default on the root
    # catches all of them at once; anything that wants no fill says so.
    head = re.sub(r'\sfill="[^"]*"', "", head)
    head = re.sub(r'\sstyle="[^"]*"', "", head)
    head = head.replace(
        "<svg",
        '<svg fill="currentColor" style="color: var(--dl-fg); color-scheme: normal"', 1)
    return head + body, unmapped


ROOT = pathlib.Path(__file__).resolve().parent.parent


def paints_its_own_background(svg):
    """True for a diagram that opens with a full-bleed opaque rect.

    A hand-drawn SVG that paints its own background is a light card by
    choice, not an oversight: its text sits on a colour it controls, in every
    theme. Flagging those is how a checker teaches people to ignore it.
    """
    match = re.search(r"<rect\b[^>]*>", svg)
    if not match:
        return False
    rect = match.group(0)
    fill = re.search(r'fill="([^"]+)"', rect)
    return bool(
        fill
        and fill.group(1).lower() not in ("none", "transparent")
        and re.search(r'\bwidth="(100%|\d+)"', rect)
        and re.search(r'\bheight="(100%|\d+)"', rect)
    )


def needs_work(svg):
    """What is still literal in an SVG that has supposedly been normalised."""
    _, unmapped = normalise(svg)
    problems = set(unmapped)
    cut = svg.index(">", svg.index("<svg")) + 1
    head, body = svg[:cut], svg[cut:]
    if 'fill="currentColor"' not in head and not paints_its_own_background(body):
        problems.add("root has no fill default: text with no fill attribute stays black")
    for prop in COLOUR_PROPS:
        if re.search(rf'style="[^"]*\b{prop}\s*:', body):
            problems.add(f"inline style sets {prop}, which beats the attribute")
    if re.search(r"<style[^>]*>", body):
        problems.add("carries its own <style> block")
    return sorted(problems)


def main(argv):
    """`--check` over every committed SVG, or one file in and one file out."""
    if argv and argv[0] == "--check":
        failed = 0
        for path in sorted(ROOT.rglob("*.svg")):
            relative = str(path.relative_to(ROOT))
            # site/ is generated, and dewmark is its own project.
            if relative.startswith(("site/", "dewmark/")):
                continue
            problems = needs_work(path.read_text())
            if problems:
                failed += 1
                print(f"{path.relative_to(ROOT)}:")
                for problem in problems:
                    print(f"    {problem}")
        if failed:
            print(f"\n{failed} SVG(s) need `python3 dev/normalise_svg.py <in> <out>`.")
        return 1 if failed else 0
    source, target = pathlib.Path(argv[0]), pathlib.Path(argv[1])
    out, unmapped = normalise(source.read_text())
    target.write_text(out)
    print(f"{source}: unmapped ->", sorted(unmapped) or "none")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
