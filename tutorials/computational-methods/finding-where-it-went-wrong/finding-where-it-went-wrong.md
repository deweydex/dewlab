---
title: "Finding Where It Went Wrong"
slug: finding-where-it-went-wrong
module: computational-methods
module_title: "Computational Methods"
year: "2026-2027"
series: problem-solving
version: 2026.09.05.1
covers:
  deciding-what-done-means:
    covers: [CMPS-LO8]
  building-the-pipeline:
    covers: [CMPS-LO8]
    touches: [CMPS-LO10]
  the-symptom-is-not-the-cause:
    covers: [CMPS-LO10]
  what-finding-it-actually-took:
    covers: [CMPS-LO12]
---

# Finding Where It Went Wrong

A program can run without crashing and still be wrong. This tutorial
builds one small pipeline and decides in advance how to know whether it
worked. Then it follows a real wrong answer back to the one line actually
responsible for it.

## Deciding What Done Means

The problem: take a list of temperature readings in Fahrenheit, as text, and
return their average in Celsius.

Before writing a line of code, decide what a correct answer looks like. A
reading of `70.0` converted and averaged gives some plausible-looking
number, but "plausible-looking" is not the same as "correct". Nothing
about a single reasonable number proves the arithmetic behind it was right.

Two temperatures have a known answer nobody has to compute by hand: water
freezes at `32°F`, which is exactly `0°C`, and boils at `212°F`, which is
exactly `100°C`. A pipeline tested against readings of `32.0` and `212.0`
should report an average of exactly `50.0`. Deciding on this check now,
before any code exists to pass or fail it, is what "done" is going to mean
for this problem.

### Your turn

Before reading the next section: what would *you* have chosen to test this
pipeline against, if freezing and boiling point were not already suggested
here?

## Building the Pipeline

Three small pieces, each doing one job.

```python exec
id: building-the-pipeline-1
def parse_readings(raw_lines):
    """Text readings to floats."""
    return [float(line) for line in raw_lines]

def fahrenheit_to_celsius(f):
    return (f - 32) * 5 / 8

def average(values):
    return sum(values) / len(values)

def summarize(raw_lines):
    readings = parse_readings(raw_lines)
    celsius = [fahrenheit_to_celsius(f) for f in readings]
    return average(celsius)

daily = ["70.0", "75.5", "68.2"]
print(summarize(daily))
```

That number looks entirely reasonable for three everyday readings. Nothing
about it says whether it is right. Now run the check decided on before any
of this was written.

```python exec
id: building-the-pipeline-2
print(summarize(["32.0", "212.0"]))
```

`56.25`, not `50.0`. The pipeline runs without error and produces a
number that looks just as reasonable as the first one. That is exactly
why the known-answer test decided on in advance matters — without it,
this wrong answer would have looked correct to anyone who used it.

### Your turn

Run `summarize(["32.0"])` on its own, the freezing point alone. Does it
also come back wrong? What does that tell you about which of the two
readings in the combined test actually caught the bug?

```python exec
id: building-the-pipeline-3
```

## The Symptom Is Not the Cause

The symptom is clear: `summarize(["32.0", "212.0"])` should be `50.0` and
is not. The symptom is not the cause. Something inside the pipeline
produced a wrong number, and the wrong final average is only where that
wrong number happened to surface.

One response fixes the symptom directly: adjust `average` so that this
one test passes.

```python exec
id: the-symptom-is-not-the-cause-1
def average_patched(values):
    return sum(values) / len(values) - 6.25

def summarize_patched(raw_lines):
    readings = parse_readings(raw_lines)
    celsius = [fahrenheit_to_celsius(f) for f in readings]
    return average_patched(celsius)

print(summarize_patched(["32.0", "212.0"]))
print(summarize_patched(daily))
```

The known-answer test now passes. The everyday reading from before has
quietly changed too, for no reason connected to anything real about those
three temperatures. `average_patched` subtracts `6.25` from every average
it is ever asked for, whether that particular case needed it or not.
This is *pragmatic problem-solving*: it treats the symptom in front of
it, and it breaks the next case that does not happen to share that
symptom.

The other response asks where, exactly, a wrong number first appears.
Each stage of the pipeline can be checked against what it alone should
produce. That narrows the search, the way a reader halves a search range
in binary search. Check the middle stage, then move toward whichever
half still disagrees with what is expected.

```python exec
id: the-symptom-is-not-the-cause-2
print(parse_readings(["212.0"]))
print(fahrenheit_to_celsius(212.0))
```

`parse_readings` reports `[212.0]`, exactly as it should. `212°F` converted
to Celsius should be `100.0`. It is not. The fault is not in parsing, and
it is not in averaging — it is on the one line inside
`fahrenheit_to_celsius` doing the conversion itself. This is *semantic
analysis*: not making the visible symptom disappear, but finding the
actual cause of it.

```python exec
id: the-symptom-is-not-the-cause-3
def fahrenheit_to_celsius_fixed(f):
    return (f - 32) * 5 / 9

def summarize_fixed(raw_lines):
    readings = parse_readings(raw_lines)
    celsius = [fahrenheit_to_celsius_fixed(f) for f in readings]
    return average(celsius)

print(summarize_fixed(["32.0", "212.0"]))
print(summarize_fixed(daily))
```

The known-answer test now passes for a real reason. The everyday reading
changes too, because it was quietly wrong the whole time, not because
anything was tuned to make one test happy.

### Your turn

A second pipeline has a bug somewhere in it, and this time you are not
told where.

```python exec
id: the-symptom-is-not-the-cause-4
def average_v2(values):
    return sum(values) / (len(values) - 1)

def summarize_v2(raw_lines):
    readings = parse_readings(raw_lines)
    celsius = [fahrenheit_to_celsius_fixed(f) for f in readings]
    return average_v2(celsius)

print(summarize_v2(["32.0", "212.0"]))
```

Using the same known-answer test, check each stage of `summarize_v2` in
turn until you find the one that disagrees with what it alone should
produce.

```python exec
id: the-symptom-is-not-the-cause-5
```

## What Finding It Actually Took

None of the steps above were difficult on their own. Reading a value off a
function and comparing it to a hand-worked answer takes no special skill.
What made the difference was a handful of habits, applied in order.

Choosing freezing and boiling point over three ordinary daily readings was
a small act of *lateral thinking*. Nothing about the problem statement
suggested it. An easier, more obvious test would have missed the bug
entirely, as the freezing-point-only check earlier in this tutorial
showed.

Checking each pipeline stage in turn, rather than staring at the final
wrong number and guessing, was a *methodical approach*. The same
question got asked, stage by stage, until one stage disagreed. Each
answer along the way narrowed where the fault had to be. That is
*logical reasoning* doing real work, not just sitting as a definition on
a page.

*Initiative* is the reason a known-answer test existed to fail in the
first place. Nobody required writing one, and it would have been easy to
run the pipeline once, see a plausible-looking number, and stop there.
*Persistence* is what stops the pragmatic patch from being the last step
taken, once it makes the one visible test pass. All five habits named in
this outcome are not separate techniques to memorise. This tutorial's
own walk-through already showed every one of them in action.

### Your turn

Recall a time you fixed something, code or otherwise, without being sure
at first what was actually wrong. Which of the habits named above
appears in how you got there?

## Where to Read More

McConnell, S. (2004). *Code Complete* (2nd ed.). Microsoft Press. Chapter
23 covers debugging as a discipline in its own right, including exactly
the stage-by-stage isolation this page demonstrates.

Zeller, A. (2009). *Why Programs Fail: A Guide to Systematic Debugging*
(2nd ed.). Morgan Kaufmann. A full treatment of narrowing a fault by
halving the search space, the same idea this page calls binary search
debugging.
