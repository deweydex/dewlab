---
title: "Debugging a wrong answer: from symptom to cause — Practice"
practice_for: finding-where-it-went-wrong
year: "2026-2027"
version: 2026.09.05.1
---

# Debugging a wrong answer: from symptom to cause — Practice

The answers are hidden in folds under each problem. Several problems ask
you to predict what the code will do before you run it. Try to answer
before you check. Being wrong, and finding out why, teaches you more than
being right by accident.

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

**1.** `98.6°F` is normal human body temperature. It should convert to
`37.0°C`.

1. Using the tutorial's buggy converter, predict
   `fahrenheit_to_celsius_buggy(98.6)` before you run it.
2. Does this everyday-looking reading catch the bug?

```python exec
id: choosing-a-test-that-catches-it-1
```

<details class="dl-answer"><summary>answer</summary>

It gives `41.625`, not `37.0`. So yes, it catches the bug. The answer is
far enough out that it does not even look reasonable. The tutorial's daily
readings happened to look reasonable, even though they were wrong. This
one does not.

</details>

**2.** Freezing point on its own did not catch the bug. After taking away
32, the value is `0`, and `0` divided by anything is still `0`.

`-40°F` is exactly `-40°C`. It is the one temperature where Fahrenheit and
Celsius agree. Before you run it, predict: does this one reading catch the
bug? Why?

```python exec
id: choosing-a-test-that-catches-it-2
hint: The bug is in the arithmetic after the -32 step, so anything other than exactly 32 is worth trying.
```

<details class="dl-answer"><summary>answer</summary>

Yes. `fahrenheit_to_celsius_buggy(-40.0)` gives `-45.0`, not `-40.0`.
With `32°F`, the value going into the division was zero. Here it is not
zero, so dividing by the wrong number changes the answer. Freezing point
is the one input that hides this bug. Almost any other reading shows it.

</details>

## Narrowing Down a Different Bug

**3.** In this pipeline, the bug is in the parsing stage, not in the
conversion.

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

Can you find exactly where this one goes wrong? Check each stage on its
own, the way the tutorial checked `fahrenheit_to_celsius`.

```python exec
id: bisecting-a-different-bug-2
hint: Call parse_readings_buggy(["212.0"]) directly, on its own, before touching the conversion step at all.
```

<details class="dl-answer"><summary>answer</summary>

`parse_readings_buggy(["212.0"])` returns `[12.0]`, not `[212.0]`. The
slice `line[1:]` drops the first character of the text before turning it
into a number, so `"212.0"` becomes `"12.0"`.

The conversion stage did nothing wrong here.
`fahrenheit_to_celsius(12.0)` correctly converts the reading it was given.
That reading was already wrong. The fault is in `parse_readings_buggy`,
one stage earlier than the fault in the tutorial's example.

</details>

## Naming the Difference

**4.** A website feels slow. Two developers respond in different ways.

- The first adds a loading spinner, a small moving picture, so that people
  notice the wait less.
- The second measures which parts of the code take the most time. They
  find a request to the database that runs once for every item, when it
  should run once in total. They fix that request.

Which developer used pragmatic problem-solving, and which used semantic
analysis?

<details class="dl-answer"><summary>answer</summary>

The spinner is pragmatic problem-solving. The symptom, a wait that bothers
people, is less noticeable. But the slow request still runs exactly as
before.

Finding and fixing the request is semantic analysis. It deals with why
the site is slow, and not only with how the slowness feels. Both
developers may have been asked to make the same complaint go away. Only
one of them removed its cause.

</details>

**5.** The tutorial tested with freezing and boiling point, not with three
ordinary daily readings. It called that choice *lateral thinking*. In
your own words, why is it lateral thinking, and not good luck?

<details class="dl-answer"><summary>answer</summary>

Nothing in the problem, "average some Fahrenheit readings in Celsius",
points to freezing or boiling point. They are not the readings a
thermometer usually shows. The obvious plan is to test with the kind of
readings the pipeline will handle every day. Choosing freezing and
boiling point means not following that plan.

It was not luck, because the choice was made on purpose. Freezing and
boiling point are two of the very few conversions anyone can give exactly,
without a calculator. That is what makes them useful as a check. An
everyday reading like `70°F` has no exact answer that people remember. So
a wrong answer that looked reasonable would have nothing to be checked
against.

</details>
