---
title: "Finding Where It Went Wrong — Practice"
slug: finding-where-it-went-wrong-practice
practice_for: finding-where-it-went-wrong
module: computational-methods
module_title: "Computational Methods"
year: "2026-2027"
series: problem-solving
version: 2026.09.05.1
---

# Finding Where It Went Wrong — Practice

Answers are folded. Several of these ask you to predict an output before
running anything. Resist checking first — being wrong and finding out why
is worth more than being right by accident.

```python exec
id: setup-1
def parse_readings(raw_lines):
    return [float(line) for line in raw_lines]

def fahrenheit_to_celsius_buggy(f):
    return (f - 32) * 5 / 8

def fahrenheit_to_celsius(f):
    return (f - 32) * 5 / 9

def average(values):
    return sum(values) / len(values)
```

## Choosing a Test That Catches It

**1.** Using the tutorial's buggy converter, predict
`fahrenheit_to_celsius_buggy(98.6)` before running it — ordinary human body
temperature, which should convert to `37.0`. Does this everyday-looking
reading catch the bug?

```python exec
id: choosing-a-test-that-catches-it-1
```

<details class="dl-answer"><summary>answer</summary>

`41.625`, not `37.0` — yes, it catches the bug, and by a wide enough margin
that "plausible-looking" would not have saved it here either. The tutorial's
own daily readings happened to look reasonable regardless; this one does
not.

</details>

**2.** Freezing point alone did not catch the bug, because `0` divided any
way is still `0`. `-40°F` is exactly `-40°C` — the one temperature where
Fahrenheit and Celsius agree. Predict whether this single reading catches
the bug, and why, before running it.

```python exec
id: choosing-a-test-that-catches-it-2
hint: The bug is in the arithmetic after the -32 step, so anything other than exactly 32 is worth trying.
```

<details class="dl-answer"><summary>answer</summary>

Yes. `fahrenheit_to_celsius_buggy(-40.0)` gives `-45.0`, not `-40.0`. Unlike
`32°F`, the value going into the buggy division here is not zero, so the
wrong denominator actually changes the answer. Freezing point is the one
input that happens to hide this particular bug; almost anything else does
not.

</details>

## Bisecting a Different Bug

**3.** A different pipeline has its bug in `parse_readings` instead of in
the conversion:

```python exec
id: bisecting-a-different-bug-1
def parse_readings_buggy(raw_lines):
    return [float(line[1:]) for line in raw_lines]

def summarize_q3(raw_lines):
    readings = parse_readings_buggy(raw_lines)
    celsius = [fahrenheit_to_celsius(f) for f in readings]
    return average(celsius)

print(summarize_q3(["212.0"]))
```

Check each stage by hand, the way the tutorial checked `fahrenheit_to_celsius`
directly, to find exactly where this one goes wrong.

```python exec
id: bisecting-a-different-bug-2
hint: Call parse_readings_buggy(["212.0"]) directly, on its own, before touching the conversion step at all.
```

<details class="dl-answer"><summary>answer</summary>

`parse_readings_buggy(["212.0"])` returns `[12.0]`, not `[212.0]` —
`line[1:]` drops the first character of the text before turning it into a
number, so `"212.0"` becomes `"12.0"`. The conversion step did nothing
wrong here: `fahrenheit_to_celsius(12.0)` is correctly computing the
Celsius value for the wrong Fahrenheit reading it was handed. The fault is in
`parse_readings_buggy`, one stage earlier than the wrong number's stage in
the tutorial's own example.

</details>

## Naming the Difference

**4.** A website feels slow. One developer adds a loading spinner so the
wait feels less noticeable. Another profiles the code and finds a database
query running once per item instead of once overall, then fixes that
query. Which developer practised pragmatic problem-solving, and which
practised semantic analysis?

<details class="dl-answer"><summary>answer</summary>

The spinner is pragmatic problem-solving: the symptom, a wait that
bothers users, becomes less visible, and the actual slow query keeps
running exactly as before. Finding and fixing the per-item query is
semantic analysis: it addresses why the site is slow, not just how the
slowness is experienced. Both developers may have been asked to make the
same complaint disappear, but only one of them changed the reason it existed.

</details>

**5.** In your own words: why does the tutorial call choosing freezing and
boiling point, rather than three ordinary daily readings, an act of
*lateral thinking* rather than just good luck?

<details class="dl-answer"><summary>answer</summary>

Nothing about the problem statement, "average some Fahrenheit readings in
Celsius," points toward freezing or boiling point specifically. They are
not the readings a thermometer would usually report. Choosing them means
not following the obvious plan: testing with whatever readings the
pipeline is actually meant to handle day to day.

It was not luck because the choice was made on purpose. Freezing and boiling
point are two of the very few Fahrenheit-to-Celsius conversions anyone can
state exactly without a calculator. That is exactly what makes them
useful as a check. An everyday reading like `70°F` has no memorable exact
answer to compare against, so a bug hiding behind a plausible-looking
wrong number would have nothing to be caught by.

</details>
