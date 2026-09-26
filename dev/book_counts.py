"""Make data/book-chapters.csv and data/book-characters.csv from the six
novels already in data/.

    python3 dev/book_counts.py

Both are counted, not fetched, so they have no recipe and no live source;
data/book-chapters.yaml and data/book-characters.yaml point here for how
they were made. A chapter is whatever the book marks as one (Frankenstein's
four opening letters included), numbered from 1 through the whole novel.
Anything shorter than MIN_WORDS between two headings is a table of
contents, not a chapter, and is left out.

A character is counted wherever their name, as written in the patterns
below, appears: "he", "she" and "I" are not counted, so a narrator is
nearly invisible, and a name two people share is split where the book
splits it ("Miss Bingley" is not Mr Bingley). Frankenstein's creature has
no name, and so no row, which is a finding of its own.
"""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
MIN_WORDS = 100
WORD = re.compile(r"[A-Za-z]+(?:'[A-Za-z]+)?")

# For each book: what a chapter heading looks like, on a line of its own,
# and each character's name as the book writes it.
BOOKS = {
    "pride-and-prejudice": (r"Chapter \d+", {
        "Elizabeth": r"\b(?:Elizabeth|Lizzy|Eliza)\b",
        "Darcy": r"\bDarcy\b",
        "Jane": r"\bJane\b",
        "Mr Bingley": r"(?<!Miss )\bBingley\b",
        "Miss Bingley": r"\bMiss Bingley\b|\bCaroline\b",
        "Wickham": r"\bWickham\b",
        "Lydia": r"\bLydia\b",
        "Mr Collins": r"\bCollins\b",
        "Charlotte": r"\bCharlotte\b",
        "Mrs Bennet": r"\bMrs\. Bennet\b",
        "Mr Bennet": r"\bMr\. Bennet\b",
        "Lady Catherine": r"\bLady Catherine\b",
    }),
    "frankenstein": (r"(?:Letter|Chapter) \d+", {
        "Victor": r"\bVictor\b",
        "Elizabeth": r"\bElizabeth\b",
        "Clerval": r"\b(?:Clerval|Henry)\b",
        "Justine": r"\bJustine\b",
        "William": r"\bWilliam\b",
        "Walton": r"\bWalton\b",
        "Felix": r"\bFelix\b",
        "Safie": r"\bSafie\b",
    }),
    "the-time-machine": (r"[IVX]+|EPILOGUE|Epilogue", {
        "the Time Traveller": r"\bTime Traveller\b",
        "Weena": r"\bWeena\b",
        "Filby": r"\bFilby\b",
        "the Psychologist": r"\bPsychologist\b",
        "the Medical Man": r"\bMedical Man\b",
        "the Eloi": r"\bEloi\b",
        "the Morlocks": r"\bMorlocks?\b",
    }),
    "the-war-of-the-worlds": (r"[IVX]+\.", {
        "the Martians": r"\bMartians?\b",
        "Ogilvy": r"\bOgilvy\b",
        "the curate": r"\bcurate\b",
        "the artilleryman": r"\bartilleryman\b",
        "my brother": r"\bmy brother\b",
        "my wife": r"\bmy wife\b",
    }),
    "a-princess-of-mars": (r"CHAPTER [IVXL]+", {
        "John Carter": r"\bCarter\b",
        "Dejah Thoris": r"\bDejah Thoris\b",
        "Tars Tarkas": r"\bTars Tarkas\b",
        "Sola": r"\bSola\b",
        "Woola": r"\bWoola\b",
        "Sarkoja": r"\bSarkoja\b",
        "Kantos Kan": r"\bKantos Kan\b",
        "Tal Hajus": r"\bTal Hajus\b",
    }),
    "the-lost-world": (r"CHAPTER [IVXL]+", {
        "Malone": r"\bMalone\b",
        "Challenger": r"\bChallenger\b",
        "Summerlee": r"\bSummerlee\b",
        "Lord John Roxton": r"\b(?:Roxton|Lord John)\b",
        "Gladys": r"\bGladys\b",
        "Zambo": r"\bZambo\b",
        "McArdle": r"\bMcArdle\b",
    }),
}


def chapters(book: str, heading: str) -> list[str]:
    """The novel's chapters, in order: the text between one heading and the
    next, inside Project Gutenberg's own start and end lines."""
    text = (DATA / f"{book}.txt").read_text(encoding="utf-8")
    text = text.split("*** START OF", 1)[1].split("\n", 1)[1]
    text = text.split("*** END OF", 1)[0]
    parts = re.split(rf"(?m)^[ \t]*(?:{heading})[ \t]*$", text)
    return [part for part in parts[1:] if len(WORD.findall(part)) >= MIN_WORDS]


def main() -> int:
    chapter_rows, character_rows = [], []
    for book, (heading, characters) in BOOKS.items():
        found = chapters(book, heading)
        print(f"{book}: {len(found)} chapters", file=sys.stderr)
        for number, text in enumerate(found, start=1):
            chapter_rows.append([book, number, len(WORD.findall(text))])
            for name, pattern in characters.items():
                character_rows.append([book, number, name, len(re.findall(pattern, text))])
    for name, header, rows in [
        ("book-chapters.csv", ["book", "chapter", "words"], chapter_rows),
        ("book-characters.csv", ["book", "chapter", "character", "mentions"], character_rows),
    ]:
        with open(DATA / name, "w", newline="") as handle:
            writer = csv.writer(handle, lineterminator="\n")
            writer.writerow(header)
            writer.writerows(rows)
    return 0


if __name__ == "__main__":
    sys.exit(main())
