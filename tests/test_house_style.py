"""Student-facing pages do not say what feels natural, right or obvious.

A page cannot know what a reader feels. PEDAGOGICAL_STYLE_GUIDE.md#no-reader-claims
says to state what an idea reads, counts or does instead. This test flags the
common phrases in tutorials and templates. A cell's `id:` line is a contract
and is skipped, so an old id may keep a word that its heading no longer has.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

PHRASES = re.compile(
    r"\bfeels? (?:right|natural|obvious|wrong|strange|odd|fine)\b"
    r"|\bcan feel\b|\bnatural to\b|\bit is natural\b|\bso natural\b"
    r"|\bsounds (?:like|right)\b|\bcan sound like\b|\bobviously\b|\bof course\b"
    r"|\bWhy idea A feels\b"
    r"|\b(?:most|many) people (?:guess|cannot|can't|say|skip|trust|expect|mix|stop|write)\b"
    r"|\bsurprises (?:most|many|some) people\b|\bconfuses many people\b",
    re.IGNORECASE,
)

# Lines that match but do not claim what a reader feels. Keep this short and
# give a reason for each entry.
ALLOWED = {
    # Describes how generated text resembles its source book.
    "A chain keyed on one word writes nonsense that sounds like its book.",
}


def _files():
    yield from sorted((ROOT / "tutorials").glob("*/*.md"))
    yield from sorted((ROOT / "docs" / "templates").glob("*.md"))


def test_pages_do_not_say_what_feels_natural_or_right():
    found = []
    for path in _files():
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if line.lstrip().startswith("id:"):
                continue
            if any(allowed in line for allowed in ALLOWED):
                continue
            if PHRASES.search(line):
                found.append(f"{path.relative_to(ROOT)}:{number}: {line.strip()}")
    assert not found, (
        "These lines say what a reader feels (see "
        "planning/PEDAGOGICAL_STYLE_GUIDE.md#no-reader-claims):\n" + "\n".join(found)
    )
