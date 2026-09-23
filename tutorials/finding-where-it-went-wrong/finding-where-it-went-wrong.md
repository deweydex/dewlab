---
title: "Debugging a wrong answer: from symptom to cause"
year: "2026-2027"
version: 2026.09.05.1
covers:
  deciding-what-done-means:
    covers: [CMPS-LO8]
  building-the-pipeline:
    covers: [CMPS-LO8]
    touches: [CMPS-LO10]
  the-symptom-is-not-the-cause:
    covers: [CMPS-LO10]
  what-finding-it-took:
    covers: [CMPS-LO12]
---

# Debugging a wrong answer: from symptom to cause

A program can run without crashing, and still be wrong.

We have met this before. In
[Reading an error message](tutorial:reading-an-error-message), we read
Python's error messages, and met logical errors: code that runs but gives
the wrong answer. In
[Finding bugs in bigger programs](tutorial:when-it-goes-wrong), we
printed values in the middle of a program, tested small pieces on their
own, and checked answers we already knew. If your program stops with an
error message, those two pages are the place to start.

This page is about the other case: no error message, only a wrong
answer. We take those habits a few steps further:

1. We decide how to check the answer *before* we write any code.
2. We follow a wrong answer back, step by step, to the one line that
   causes it.
3. We compare two ways of responding to a bug, and see why only one of
   them fixes it.

## Deciding What Done Means

Here is the problem. We have a list of temperature readings in
Fahrenheit, stored as text. We want their average in Celsius.

Before we write a line of code, we decide what a correct answer looks
like. Suppose we convert and average a reading like `70.0`. We get a
number that looks reasonable. But a number that looks reasonable is not
the same as a correct number. One reasonable-looking number does not
prove that the arithmetic behind it was right.

Two temperatures have answers everyone knows, with no working out:

- Water freezes at `32°F`, which is exactly `0°C`.
- Water boils at `212°F`, which is exactly `100°C`.

So if we give the program the readings `32.0` and `212.0`, the average
should be exactly `50.0`. We decide on this check now, before any code
exists to pass or fail it. Passing it is what "done" will mean for this
problem.

### Your turn

Before you read the next section: if freezing and boiling point were not
already suggested here, what would *you* have chosen to test this
program with?

## Building the Pipeline

A *pipeline* is a program made of stages, where each stage passes its
result on to the next. Ours has three small stages, and each does one job:

1. `parse_readings` turns the text readings into numbers.
2. `fahrenheit_to_celsius` converts one reading to Celsius.
3. `average` finds the average.

`summarize` runs the three stages in order. It uses list comprehensions,
from [Lists: keeping many values in order](tutorial:lists-and-sequences),
to apply a stage to every reading.

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

That number looks reasonable for three everyday readings. But nothing
about it tells us whether it is right. Now let's run the check we decided
on before we wrote any of this. What should it print?

```python exec
id: building-the-pipeline-2
print(summarize(["32.0", "212.0"]))
```

It prints `56.25`, not `50.0`. The program runs without an error, and
gives a number that looks just as reasonable as the first one. This is
why we decided on a known-answer test in advance. Without it, anyone
using this program would have trusted a wrong answer.

### Your turn

1. Try `summarize(["32.0"])`, with the freezing point on its own.
2. Does it come back wrong too?
3. What does that tell you about which of the two readings caught the
   bug?

```python exec
id: building-the-pipeline-3
```

```hint
after: 4 errors
What does the last line of the message say went wrong: a name Python does
not know, or the shape of a line? Which line is it pointing at? Before you
change it, what did you expect `summarize(["32.0"])` to print? Write that
number in your notes, then compare it with what comes back.
```

## The Symptom Is Not the Cause

The *symptom* is what we can see going wrong:
`summarize(["32.0", "212.0"])` should be `50.0`, and it is not.

The symptom is not the *cause*. The cause is the mistake in the code
that produced the wrong number. Something inside the pipeline made a
wrong number. The final average is only where that wrong number came to
the surface.

One way to respond is to fix the symptom directly. We could change
`average` so that this one test passes.

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

The known-answer test now passes. But look at the everyday readings: their
answer has changed too, for no reason that has anything to do with those
three temperatures. `average_patched` takes `6.25` off every average it is
ever asked for, whether that case needed it or not.

This is called *pragmatic problem-solving*. Pragmatic problem-solving
treats the symptom in front of it. It makes that one symptom go away, and
it breaks the next case that does not share the same symptom.

The other way to respond asks a different question. Where, exactly, does
a wrong number first appear?

We can check each stage of the pipeline against what that stage alone
should give. This narrows the search, a little like binary search in
[Searching a list: linear and binary search](tutorial:finding-things):

1. Check the stage in the middle.
2. If its output is right, the fault must be in a later stage.
3. If its output is wrong, the fault is in that stage, or in an earlier
   one.
4. Check the middle of the stages that are left, and repeat until only
   one stage is left.

What should each of these two lines print, if the stage is correct?

```python exec
id: the-symptom-is-not-the-cause-2
print(parse_readings(["212.0"]))
print(fahrenheit_to_celsius(212.0))
```

`parse_readings` gives `[212.0]`, exactly as it should. But `212°F` in
Celsius should be `100.0`, and it is not. So the fault is not in parsing,
and it is not in averaging. It is in the one line inside
`fahrenheit_to_celsius` that does the conversion. The formula divides by
`8`, where it should divide by `9`.

This is called *semantic analysis*. Semantic analysis finds the real
cause of a symptom, instead of only making the symptom disappear.

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

The known-answer test now passes for a real reason. The answer for the
everyday readings changes too. It was wrong all along, and now it is
right. Nothing was adjusted only to make one test pass.

### Your turn

A second pipeline has a bug somewhere in it. This time, you are not told
where.

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

Use the same known-answer readings to check each stage of `summarize_v2`
in turn. Keep going until you find the stage that disagrees with what it
alone should give.

```python exec
id: the-symptom-is-not-the-cause-5
```

```hint
after: 4 runs
Which stage have you checked so far, and what did it alone return? For
`["32.0", "212.0"]`, what should `parse_readings` give back, what should
each reading be in Celsius, and what should the average of those two be?
Write the three expected values down before you run the next check.
```

```hint
after: 8 runs
title: some steps
1. Print `parse_readings(["32.0", "212.0"])` and compare it with what you
   expected.
2. Print `fahrenheit_to_celsius_fixed(212.0)` and `fahrenheit_to_celsius_fixed(32.0)`.
3. Print `average_v2` of those two Celsius values. What should the average
   of two numbers be, and what did it give?

**Think about:** which stage was the first to disagree with your expected
value, and why the stages after it could not have been the cause.

**Try this next:** call `average_v2` with a list of one reading. What
happens, and what does that tell you about the line inside it?
```

## What Finding It Took

None of the steps above was hard on its own. Reading a value from a
function, and comparing it with an answer worked out by hand, needs no
special skill. What made the difference was a handful of habits, used in
order. Each one has a name.

**Lateral thinking.** We tested with freezing and boiling point, not
with three ordinary daily readings. *Lateral thinking* is choosing a test
or an approach that nothing in the problem suggested. An easier, more
obvious test would have missed the bug completely. The freezing-point
check on its own showed that.

**A methodical approach.** We checked each stage of the pipeline in turn.
We did not stare at the final wrong number and guess. A *methodical
approach* asks the same question at each stage, in order, until one stage
disagrees.

**Logical reasoning.** Each answer along the way narrowed down where the
fault could be. *Logical reasoning* is using what one check has ruled out
to decide what to check next. On this page it did real work. It was not
only a definition.

**Initiative.** *Initiative* is starting a check that nobody asked for.
It is the reason there was a known-answer test to fail in the first
place. Nobody required one. It would have been easy to run the program
once, see a reasonable-looking number, and stop there.

**Persistence.** The pragmatic patch made the one visible test pass.
*Persistence* is not stopping there, and going on until the real cause
is found.

These five habits are not separate techniques to learn by heart. You
have already seen every one of them at work on this page.

### Your turn

Think of a time you fixed something, in code or anywhere else, when at
first you were not sure what was wrong. Which of these habits helped you
get there?

## Where to Read More

McConnell, S. (2004). *Code Complete* (2nd ed.). Microsoft Press. Chapter
23 covers debugging as a discipline in its own right, including exactly
the stage-by-stage isolation this page demonstrates.

Zeller, A. (2009). *Why Programs Fail: A Guide to Systematic Debugging*
(2nd ed.). Morgan Kaufmann. A full treatment of narrowing a fault by
halving the search space, the same idea this page calls binary search
debugging.
