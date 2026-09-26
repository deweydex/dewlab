---
title: "The equals sign: a closer look at =, == and maths"
year: "2026-2027"
version: 2026.09.26.1
---

# The equals sign: a closer look at =, == and maths

In [Making decisions](tutorial:making-decisions), one equals sign gave a
name a value, and two equals signs asked a question. In maths, one equals
sign says that two things are the same. That is three jobs for one sign.
Here are two ideas about what `=` does in Python. Both are reasonable, and
they cannot both be true.

**Idea A.** `=` means what it means in maths. `score = score + 5` says
that `score` and `score + 5` are the same, so it can never be true.

**Idea B.** `=` is an instruction. Python calculates the right-hand side,
and then gives the answer the name on the left.

## An experiment

The two ideas predict different things for this cell. Idea A says the
second line is impossible, so Python stops with an error. Idea B says
Python adds 5 to 10 and gives `score` the new value, 15.

```python exec
id: an-experiment-1
score = 10
score = score + 5
print(score)
```

```predict
type: choice

Which will you see?

- An error
  - This is what idea A predicts.
- 15
  - This is what idea B predicts.
- 10
```

Run it. It prints 15, as idea B predicts. The second line was not a
statement about `score`. It was an instruction, and Python ran it once.

Now let's ask the question that idea A had in mind. `==` asks whether two
values are equal, and answers `True` or `False`. What will this print?

```python exec
id: an-experiment-2
score = 15
print(score == score + 5)
```

```predict
type: choice

What will it print?

- True
- False
```

It prints `False`. 15 is not the same as 20. The maths statement "score
equals score plus 5" is false, and `==` says so. `=` never asks this
question.

## Why idea A feels right

In maths, $x = 5$ and $5 = x$ say the same thing. The sign works both
ways, and it states a fact. Most of us met `=` in maths for years before we
met it in a program, so the maths meaning comes first.

Here is a way to see that Python's `=` does not work both ways. This cell
is meant to fail.

```python exec
id: why-idea-a-feels-right-1
score = 15
15 = score
```

Python stops with a `SyntaxError`. Python can give a name a
value. It cannot give the number 15 a value. The error message even asks whether you
meant `==`.

Fortran used `=` for this instruction in 1957, and most languages since
have done the same. Some, such as Pascal, write `:=` instead, so that `=`
can keep its maths meaning.

## Where else it happens

An `if` needs a question, so it needs `==`. What happens here?

```python exec
id: where-else-it-happens-1
score = 15
if score = 15:
    print("Fifteen!")
```

Python stops before it runs anything, and asks again whether you meant
`==`. Can you make the cell print `Fifteen!`?

<details class="dl-answer"><summary>one change that does it</summary>

Write `if score == 15:`. One equals sign gives a value. Two ask a question.

</details>

## Where to read more

Python's own tutorial shows `=` and `==` side by side in its first pages:
[An informal introduction to Python](https://docs.python.org/3/tutorial/introduction.html).
