---
title: "Starting a total: a closer look at total = 0"
year: "2026-2027"
version: 2026.09.26.1
---

<!-- TEMPLATE: a closer look. One misconception, taught as an experiment.
Both ideas make a prediction, only one matches what happens, and then the
page explains why the other idea is so natural to hold (#closer-look). A
predict block elsewhere links here from the option that shows this
misconception. The page never says the reader held it. -->

# Starting a total: a closer look at total = 0

On [Running totals](tutorial:running-totals), a loop printed the width of
Mars when it was meant to print the width of four planets. One line had
moved. Here are two ideas about what that line does. Both are reasonable,
and they can't both be true.

**Idea A.** `total = 0` creates the name `total`. It happens once, however
many times the line is reached.

**Idea B.** Python runs a line each time it reaches it. A line inside a
loop is reached every time round.

## An experiment

The two ideas predict different things for this loop. Idea A says the
total keeps growing: it starts at 0, 10 and 20 on the three days, and ends
at 30. Idea B says every day starts again: 0, 0 and 0, and it ends at 10.

```python exec
id: an-experiment-1
for day in [1, 2, 3]:
    total = 0
    print("day", day, "starts at", total)
    total = total + 10
print("at the end:", total)
```

```predict
type: choice

Which will you see?

- 0, 10, 20, and 30 at the end
  - This is what idea A predicts.
- 0, 0, 0, and 10 at the end
  - This is what idea B predicts.
- Something else
```

Run it. Idea B matches what happens: every day starts again at 0.

Can you find a change to the loop that makes idea A's prediction come
true? There is one, and it moves one line.

<details class="dl-answer"><summary>one change that does it</summary>

Move `total = 0` above the `for` line. Then it runs once, before the loop,
and the total grows: 0, 10 and 20, and 30 at the end.

</details>

## Why idea A feels right

Idea A is how mathematics works. When a proof says "let $t = 0$", that is
true from then on, everywhere in the argument. It is not said again at
every step. Writing something down once and having it stay true is what
"let" means.

A recipe works the same way. "Start with an empty bowl" is said once, and
nobody empties the bowl again at every step. So a line that looks like
preparation feels like something that happens once, before the real work.

Python reads a program differently. It does not look at the whole program
and decide what is true. It goes through it line by line, and each line is
an action it takes when it reaches it. `total = 0` is not a fact about
`total`. It is an instruction: make `total` 0, now.

## Where else it happens

The same thing happens with anything a loop is meant to collect. What do
you think this prints?

```python exec
id: where-else-it-happens-1
found = []
for word in ["sea", "sky", "sand"]:
    found = []
    found.append(word)
print(found)
```

```predict
type: text

What will `found` hold at the end?
```

What would you move to make it hold all three words?
