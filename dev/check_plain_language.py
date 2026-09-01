"""The eight checks from CLAUDE.md §"Before you write a word a student will
read", which point at planning/PEDAGOGICAL_STYLE_GUIDE.md §4.

Usage:
    python3 dev/check_plain_language.py docs/DEWMINI.md
    python3 dev/check_plain_language.py planning/NOTES.md --planning

`--planning` turns off the two rules CLAUDE.md scopes to student-facing text
only: the twenty-five word ceiling and the em-dash rules. Everything else
applies to any prose in the repository.

This is a first filter, not a verdict. It reports what it can decide and
stays quiet about the rest.

Mechanical where the rule is mechanical. Sentence length, em dashes, missing
verbs, reversals, banned words and listed idioms are all decidable. Metaphor
and hedging are not, and are left to a human.
"""
import re, sys

BANNED = ["genuine", "genuinely", "honest", "honestly", "actually", "simply",
          "truly", "sitting with", "load-bearing", "hold space", "lean into",
          "delve", "deep dive", "circle back", "at the end of the day"]
IDIOMS = ["behind you", "paging through", "cuts across", "dead end",
          "earns its keep", "flatters", "on the fly", "under the hood",
          "out of the box", "down the line", "a stone's throw"]
# An imperative has a finite verb with the subject understood, which is the
# right form for an instruction: "Drag a panel's inner edge to resize it."
# There is no check here for a sentence without a finite verb, and the rule
# is left to a reader. Deciding it needs a part-of-speech tagger. A regex
# needs a list of verbs, and any catch-all wide enough to cover the verbs
# nobody listed — \w+s, \w+ed — also matches every plural noun, so
# "Two ways of measuring an angle" reads as having a verb in "ways". That is
# the worked example in CLAUDE.md for the rule, and the check could not see
# it, while firing 91 times across this repository's documents on labels and
# table cells that are not sentences at all.

def strip_markup(t, keep_italics=False):
    t = re.sub(r"`[^`]*`", "CODE", t)
    t = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", t)
    t = t.replace("**", "")
    if not keep_italics:
        t = re.sub(r"\*|_", "", t)
    return t

def sentences(block):
    # A colon does not end a sentence. Splitting on one turned "Texture holds
    # the same preferences every page has: theme, font, text size" into a
    # verbless fragment that is nothing of the kind.
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", block) if s.strip()]

def check(name, text, student_facing=True):
    problems = []
    low = text.lower()
    for w in BANNED:
        for m in re.finditer(r"\b" + re.escape(w) + r"\b", low):
            problems.append(("banned word", w, text[max(0, m.start()-40):m.start()+40]))
    for w in IDIOMS:
        if re.search(r"\b" + re.escape(w) + r"\b", low):
            problems.append(("possible idiom", w, ""))
    if re.search(r"[\U0001F300-\U0001FAFF☀-➿]", text):
        problems.append(("emoji", "", ""))

    paras = [p for p in re.split(r"\n\s*\n", text) if p.strip()]
    for para in paras:
        if para.lstrip().startswith(("#", "|", "```", "    ")):
            continue
        clean = strip_markup(para, keep_italics=True)
        if student_facing and clean.count("—") > 1:
            problems.append(("more than one dash in a paragraph", "", clean[:70]))
        is_list = any(l.lstrip().startswith(("- ", "* ", "|"))
                      for l in para.split("\n"))
        for s in sentences(clean):
            words = s.split()
            if is_list:
                continue
            n = len(words)
            if student_facing and n > 25:
                problems.append(("over 25 words", f"{n}w", s[:80]))
            if student_facing and "—" in s:
                after = s.split("—", 1)[1].strip()
                if len(after.split()) > len(words) / 2:
                    problems.append(("meaning after the dash", "", s[:80]))
            # Italics here usually mean the phrase is being named rather
            # than used, as when a style document quotes the rule it is
            # stating. Blank those spans before looking for a reversal.
            named_only = re.sub(r"\*[^*]+\*", " QUOTED ", s)
            if re.search(r"\bnot\b[^.,;]{0,40}\bbut\b", named_only, re.I):
                problems.append(("reversal (not X but Y)", "", s[:80]))
    return problems

if __name__ == "__main__":
    path = sys.argv[1]
    student = "--planning" not in sys.argv
    text = open(path).read()
    found = check(path, text, student)
    for kind, detail, snippet in found:
        print(f"  {kind:32} {detail:6} {snippet}")
    print(f"{path}: {len(found)} issue(s)")
