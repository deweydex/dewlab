---
title: "Starting a total: a closer look at total = 0"
year: "2026-2027"
version: 2026.11.04.3
---

# Starting a total: a closer look at total = 0

In [Repeating steps with loops](tutorial:repeating-yourself#sigma-notation-mathematics-meets-loops),
`total = 0` sat above every *loop*{.term} that added things up. What happens when
that line moves inside the loop? Here are two ideas. Both are reasonable,
and they cannot both be true.

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
for day in range(1, 4):
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

## What the line does under each idea

Idea A reads `total = 0` as a statement about the name `total`. It
creates the name once, and the name keeps that start from then on. A
proof that says "let $t = 0$" works like this: it is said once, and it holds
through the rest of the argument.

Idea B reads `total = 0` as an action. Python takes one line at a time,
and each line does its work whenever Python reaches it. `total = 0` means
"make `total` 0, now". Inside a loop, Python reaches the line every time
round, so `total` goes back to 0 every time round.

The two ideas differ in what happens on the second day. Idea A leaves
`total` at 10. Idea B sets it to 0 again before adding 10. The cell below
lets us change the number of days and watch the end total.

```python exec
id: what-the-line-does-under-each-idea-1
days = slider("days", 1, 10, step=1, value=3, id="days").value

for day in range(1, days + 1):
    total = 0
    print("day", day, "starts at", total)
    total = total + 10
print("at the end:", total)
print("if the line ran only once, the end would be:", days * 10)
```

Move the slider to a few values. What does the end total depend on? Which
line would you move so that it depends on the number of days?

## Where else it happens

The same thing happens with anything a loop is meant to collect. What do
you think this prints?

```python exec
id: where-else-it-happens-1
letters = ""
for letter in "SEA":
    letters = ""
    letters = letters + letter
print(letters)
```

```predict
type: text

What will `letters` hold at the end?
```

It prints `A`. Every time round, `letters = ""` empties it, and only the
last letter is left. What would you move to make it hold all three
letters?

## Where to read more

Python Tutor, by Philip Guo, runs a program one line at a time and draws
each name and its value as it changes. Paste either loop from this page
into [pythontutor.com](https://pythontutor.com/) and watch `total`
become 0 again.
