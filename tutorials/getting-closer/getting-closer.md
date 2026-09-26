---
title: "Getting closer: limits"
year: "2026-2027"
version: 2026.09.25.1
covers:
  halfway-to-the-door:
    covers: [MIT-3.5]
    touches: [MIT-1.1, PDP-LO6]
  a-rule-with-a-hole-in-it:
    covers: [MIT-3.5]
    touches: [MIT-3.2]
  closer-from-both-sides:
    covers: [MIT-3.5]
    touches: [PDP-LO8]
  when-the-two-sides-disagree:
    covers: [MIT-3.5]
    touches: [PDP-LO4]
  a-limit-at-infinity:
    covers: [MIT-3.5]
    touches: [MIT-1.1]
  when-the-floats-run-out:
    covers: [MIT-3.5]
    touches: [MIT-1.4]
---

# Getting closer: limits

You stand 8 metres from a door. You walk half the way there, and stop.
Then you walk half of what is left, and stop again, and again. Do you
ever reach the door? Your legs say yes. The arithmetic says every walk
leaves half of the gap still to go. If that argument makes your head
hurt a little, good: people have argued about it for about 2,500 years.
This page is about the number your steps are heading for, and it is
the idea that the rest of this unit is built on.

On this page we:

- follow a walk that gets closer to a door, and name the number it
  heads for
- meet a rule with a hole in it, and ask what belongs in the hole
- close in on a number from both sides, with a loop that halves the
  step
- see what happens at the sharp edge of a shape on a screen, where the
  two sides disagree
- find a limit far away, at infinity, and meet the number $e$
- see where Python's floats stop getting closer

> **The space we're in.** The real numbers, with Python's floats
> standing in for them. We are allowed to take as many steps as we
> like, each smaller than the last, and to watch where the values go.
> One thing usually goes unsaid: in the maths, the steps can shrink for
> ever, but a float has a smallest step. The last section is about
> where that matters.

## Warm-up

The first question is from
[Doubling and halving](tutorial:doubling-and-halving#halving-down-to-1),
and the second from
[Drawing a rule](tutorial:drawing-a-rule#rules-with-gaps-and-rules-that-race).

```question
id: getting-closer-warm-up-1
type: fill-in-the-blank

Halve 1 three times and you get $\frac{1}{8}$, which is $2^{-3}$. As a
decimal, $2^{-3}$ is {0.125}.
```

```question
id: getting-closer-warm-up-2
type: multiple-choice
answer: 2

`plot_rule(one_over, -5, 5)` stopped with a `ZeroDivisionError`. Why?

- `plot_rule` cannot draw negative numbers.
  - The graph drew negative inputs; the problem is one input only.
- One of its points was exactly 0, and $\frac{1}{0}$ has no value.
  - Some point in the range was exactly 0, and 1 divided by 0 has no value.
- The graph of $\frac{1}{x}$ is too steep to draw.
  - Steep is fine to draw; the trouble is one point with no value at all.
```

## Halfway to the door

The first walk takes you 4 metres. The second takes you half of the 4
metres left, so you have come 6. Then 7, then 7.5. Before you run the
cell, guess how far you have come after ten walks.

```python exec
id: getting-closer-door-1
door = 8
walked = 0
this_walk = door / 2
for walk in range(1, 11):
    walked = walked + this_walk
    print(walk, walked)
    this_walk = this_walk / 2
```

After ten walks you have come 7.9921875 metres. You never reach 8: each
walk covers half of what is left, so half is always still to go. After
$k$ walks, what is left is $8 \times 2^{-k}$, a
[negative exponent](tutorial:doubling-and-halving#halving-down-to-1)
counting halvings. But what is left can be made as small as we like.
After 20 walks it is less than a hundredth of a millimetre.

<aside class="dl-note" id="getting-closer-note-zeno">

**Zeno's paradox.** The Greek thinker Zeno of Elea, who lived in the
5th century BC, told a story like this walk to argue that moving from
one place to another should be impossible. The idea of a limit, which
this page builds, is one of the answers mathematicians later gave him.

</aside>

The distances walked, 4, 6, 7, 7.5, and so on, are a sequence, as on
[A row of numbers](tutorial:a-row-of-numbers#counting-from-0): values
in order, $w_1, w_2, w_3, \dots$. A *limit* of a sequence is a number
the values get as close to as we like, and stay that close, if we go
far enough along. This walk's limit is 8. Mathematicians write

$$\lim_{k \to \infty} w_k = 8$$

and say "the limit of $w_k$, as $k$ goes to infinity, is 8". Infinity,
$\infty$, is not a number we reach. "$k$ goes to infinity" means $k$
keeps growing, past any number you name.

## A rule with a hole in it

Here is a rule that behaves well everywhere except at one point:

$$f(x) = \frac{x^2 - 4}{x - 2}$$

The cell works it out for five values of $x$. Look for a pattern in
the answers before you run it.

```python exec
id: getting-closer-hole-1
def hole_rule(x):
    """Return (x squared, take away 4), divided by (x take away 2)."""
    return (x ** 2 - 4) / (x - 2)

for x in [0, 1, 1.5, 2.5, 3]:
    print(x, hole_rule(x))
```

Each answer is 2 more than $x$. There is a reason. On
[Drawing a rule](tutorial:drawing-a-rule#a-tool-that-draws-any-rule),
$x^2 - 4$ was $(x - 2)(x + 2)$. So the rule is
$\frac{(x - 2)(x + 2)}{x - 2}$, and the $x - 2$ on top cancels the
$x - 2$ below, leaving $x + 2$.

That cancelling works for every $x$ except one. What will happen at
$x = 2$? This cell is meant to stop with an error.

```python exec
id: getting-closer-hole-2
print(hole_rule(2))
```

The last line says `ZeroDivisionError: division by zero`. At $x = 2$
the rule asks for $\frac{0}{0}$, which has no value. So 2 is outside
the rule's domain. Let's draw the rule with `plot_rule` and mark the
missing point with an open circle, the usual sign for "no value here".
What shape do you expect?

```python exec
id: getting-closer-hole-3
import matplotlib.pyplot as plt

plot_rule(hole_rule, -1, 4.5)
plt.plot(2, 4, "o", markerfacecolor="white", color="C0")
```

A straight line, $y = x + 2$, with one point missing. `plot_rule`
worked out 401 points, and none of them was exactly 2, so nothing
stopped it. The picture could never show the hole by itself: one
missing point has no width. We drew the circle by hand.

The line has a hole at $(2, 4)$. The rule has no value at 2, but
everything around the hole points at 4. The next section makes that
idea exact.

## Closer from both sides

Let's close in on 2, from the left and from the right, as the walk
closed in on the door. The step starts at 1 and halves on each row.
The middle column is the rule just left of 2, and the last column is
just right. What will each column do?

```python exec
id: getting-closer-sides-1
step = 1
for row in range(10):
    print(step, hole_rule(2 - step), hole_rule(2 + step))
    step = step / 2
```

The middle column climbs, 3, 3.5, 3.75, towards 4 from below. The last
column falls, 5, 4.5, 4.25, towards 4 from above. Both sides head for
the same number. The *limit of a function* at a point $a$ is the number
its values get as close to as we like, when $x$ is close enough to $a$,
from either side. We write

$$\lim_{x \to 2} \frac{x^2 - 4}{x - 2} = 4$$

and say "the limit, as $x$ approaches 2, is 4". The value at 2 itself
plays no part. The rule has none, and the limit is still 4.

We will close in on several more numbers, so let's give the loop a
name. `approach` is a tool for this page only. It prints the same kind
of table for any rule and any point `a`.

```python exec
id: getting-closer-sides-2
def approach(rule, a, rows=10):
    """Print rule just left and just right of a, halving the step on each row."""
    step = 1
    for row in range(rows):
        print(step, rule(a - step), rule(a + step))
        step = step / 2
```

Here is a rule we cannot cancel: $\frac{\sin x}{x}$, with $x$ in
radians, as on
[Going round in circles](tutorial:going-round-in-circles#python-measures-angles-another-way).
At $x = 0$ it is $\frac{0}{0}$ again. Guess where it is heading, then
run it.

```python exec
id: getting-closer-sides-3
import math

def sine_over_x(x):
    """Return the sine of x, divided by x."""
    return math.sin(x) / x

approach(sine_over_x, 0)
```

Both columns are the same, since the rule gives the same value at $-x$
as at $x$, and both head for 1. So
$\lim_{x \to 0} \frac{\sin x}{x} = 1$. No algebra found that answer.
The table did.

### Your turn

1. Close in on 2 for $\frac{x^3 - 8}{x - 2}$. Write it as a function,
   then call `approach`. What limit do you see?
2. Try `approach(hole_rule, 3)`. There is no hole at 3. How does the
   limit compare with `hole_rule(3)`?

```python exec
id: getting-closer-sides-your-turn
# Your rule, and approach
```

## When the two sides disagree

A computer draws a black square on a white screen. Follow a line
across the square's right-hand edge, and measure along it in
millimetres, with the edge at 1 mm. Each point's brightness is 0 inside
the square, where it is black, and 255 outside, where it is white, as
on [Everything is ones and zeros](tutorial:everything-is-ones-and-zeros).
The point exactly on the edge counts as black. What happens close to
the edge? Predict both columns before you run it.

```python exec
id: getting-closer-disagree-1
def brightness(position_mm):
    """Return the brightness along the line: 0 (black) up to the edge at 1 mm, 255 (white) after it."""
    if position_mm <= 1:
        return 0
    return 255

approach(brightness, 1, rows=5)
```

The left column stays at 0 and the right column stays at 255, however
small the step. Each side has a limit of its own. A *one-sided limit*
is the number a rule heads for from one side only. From the left, it
is written $\lim_{x \to 1^-}$, and from the right, $\lim_{x \to 1^+}$:

$$\lim_{x \to 1^-} \text{brightness}(x) = 0 \qquad \lim_{x \to 1^+} \text{brightness}(x) = 255$$

The small minus sign means "from below", and the plus means "from
above". A limit from both sides exists only when the two one-sided
limits exist and agree. Here they do not, so the brightness has no
limit at the edge. That jump is what makes an edge an edge, and a
program that finds edges in a photo looks for exactly this.

Compare this with the hole. There, the rule had no value at 2, but it
had a limit. Here, the brightness has a value at the edge,
`brightness(1)` is 0, but it has no limit. A value and a limit answer two different
questions: "what is here?" and "what is everything near here heading
for?"

A side can also fail to settle at all. On
[Drawing a rule](tutorial:drawing-a-rule#rules-with-gaps-and-rules-that-race),
$\frac{1}{x}$ raced away near 0. What do you expect from `approach`?

```python exec
id: getting-closer-disagree-2
def one_over(x):
    """Return 1 divided by x."""
    return 1 / x

approach(one_over, 0)
```

Each halving of the step doubles the size of the answer: $-512$ and
512 on the last row, and it keeps going past any number. Neither side
settles, so neither side has a limit. You will sometimes see
$\lim_{x \to 0^+} \frac{1}{x} = \infty$. It is a short way to say
"grows past any number", not a limit that is a number.

## A limit at infinity

Far away from 0, $\frac{1}{x}$ does the opposite: it creeps towards 0.
$\frac{1}{10}$ is 0.1, $\frac{1}{1000}$ is 0.001, and it is never 0.
So

$$\lim_{x \to \infty} \frac{1}{x} = 0$$

This is a *limit at infinity*: where a rule heads as $x$ grows past any
number. The walk to the door was one too.

Here is one with a surprise in it, and a question somebody really
asked. On
[Doubling and halving](tutorial:doubling-and-halving#how-long-to-double),
a count grew by the same percent once a year: compound growth. Now
picture a bank that pays 100% a
year, which no real bank does. €1 becomes €2 after a year.

Suppose the bank pays half of that, 50%, every six months instead. After
six months you have €1.50, and the second 50% is paid on the €1.50, so
the year ends at $1.5^2 = €2.25$. Paid monthly, $\frac{1}{12}$ of 100%
each month, the year ends at $(1 + \frac{1}{12})^{12}$ euro. Paid $n$
times, it ends at

$$\left(1 + \frac{1}{n}\right)^n$$

If the bank pays every day, every hour, every minute, does your euro
grow without end? Pause and guess before you run it.

```python exec
id: getting-closer-infinity-1
for times in [1, 2, 12, 365, 8760, 525600, 1000000]:
    print(times, (1 + 1 / times) ** times)
print(math.e)
```

Paying more often helps less and less. Daily gives €2.7146, and every
minute gives €2.7183. The values settle on a number that starts
2.71828. This limit is the number *e*:

$$e = \lim_{n \to \infty} \left(1 + \frac{1}{n}\right)^n \approx 2.71828$$

Python keeps it as `math.e`. Like $\pi$, $e$ has decimals that never
end or repeat. It turns up wherever something grows or shrinks
smoothly, all the time, and not in yearly jumps. The next page meets
it again, in a falling hailstone.

<aside class="dl-note" id="getting-closer-note-bernoulli">

**A question about interest.** In 1683, Jacob Bernoulli asked this
question about a bank's interest, and showed that the answer lies
between 2 and 3. The letter $e$ for it was chosen later, by Leonhard
Euler.

</aside>

## When the floats run out

The table stopped at a million. Is more always better? Here is the same
rule, paid a trillion times and more. Predict the last line before you
run it.

```python exec
id: getting-closer-floats-1
for times in [10 ** 12, 10 ** 15, 10 ** 16]:
    print(times, (1 + 1 / times) ** times)
```

The values get worse, not better: 2.71852, then 3.035, then 1.0. I
think this is the strangest result on the page: more payments, and
the euro shrinks back to 1. The maths is not wrong. The floats are. On
[How a computer stores a number](tutorial:how-a-computer-stores-a-number#reading-e-16),
the gap between two neighbouring floats near 1 was about
$2.2 \times 10^{-16}$. So $1 + 10^{-16}$ has no float of its own:
Python keeps it as 1, and 1 to any power is 1. At $10^{15}$, the kept
value of $1 + 10^{-15}$ is a tiny way off, and raising it to the power
$10^{15}$ makes that tiny error large.

The hole at 2 runs into the same wall. This cell is meant to stop with
an error. Which line will print before it does?

```python exec
id: getting-closer-floats-2
tiny = 1e-16
print(2 + tiny == 2)
print(hole_rule(2 + tiny))
```

`True`, and then the `ZeroDivisionError` from before. $2 + 10^{-16}$
is stored as 2, so we are back at the hole.

In the maths, a step can shrink for ever. With floats, it cannot: past
a certain size, the step is lost. So a table of values closing in is
strong evidence of a limit. It is not a proof, and it only works while
the step is well above the size of the float gaps. The next page needs
exactly this. It picks a step of one millionth, and says why.

### Your turn

1. Change the first cell of this section to try `10 ** 9` and
   `10 ** 10`. Are they still close to `math.e`?
2. Try `approach(hole_rule, 2, rows=60)`. On which row does it stop,
   and why that row?

```python exec
id: getting-closer-floats-your-turn
# Your experiments here
```

<details class="dl-why"><summary>Why this way?</summary>

This page found every limit from a table: values closing in from both
sides, until the columns settled.

The other way is to define a limit with algebra. Mathematicians use a
definition with two small numbers, $\varepsilon$ and $\delta$: for any
distance $\varepsilon$ from the limit, however small, there is a
distance $\delta$ from the point that keeps the values that close. That
definition proves a limit, where a table only suggests one, and all of
later calculus rests on it.

We used tables because a table is something you can run and watch,
and "getting closer" is an idea about a sequence of values. The cost is
that a table can be fooled, as the last section showed, and you have
now seen the evidence for a limit without its proof.

</details>

## Four questions, looking back

| The question | On this page |
|---|---|
| What is named here? | a limit, $\lim_{x \to a}$; the one-sided limits, from the left and from the right; the number $e$, as `math.e` |
| What is promised? | a limit promises that values get as close as we like, and stay close; `approach` promises a table from both sides, with the step halving |
| What happens when? | each row comes after a halving of the step; the walk, and the bank's payments, are sequences whose values settle |
| What does this space let us do? | in the real numbers, a step can shrink for ever; floats have a smallest gap, and past it the step is lost |

## What we have now

| Term or tool | What it means |
|---|---|
| limit of a sequence | the number the values get as close to as we like, and stay close to |
| $\infty$, "goes to infinity" | grows past any number; not a number we reach |
| a hole in a graph | a single $x$ where a rule has no value, drawn as an open circle |
| limit of a function, $\lim_{x \to a} f(x)$ | the number $f(x)$ heads for as $x$ gets close to $a$, from both sides |
| one-sided limit, $x \to a^-$ and $x \to a^+$ | the number a rule heads for from the left, or from the right |
| a limit and a value | two questions: a rule can have a limit and no value, or a value and no limit |
| limit at infinity, $\lim_{x \to \infty}$ | where a rule heads as $x$ grows past any number |
| $e \approx 2.71828$, `math.e` | the limit of $(1 + \frac{1}{n})^n$: growth paid all the time |
| floats and limits | a step smaller than the float gaps is lost, so a table works only while the step is well above them |

The practice page is next. Then
[How fast, right now?](tutorial:how-fast-right-now) uses a limit to
find a falling hailstone's speed at a single moment.

## Where to read more

The dewlab page
[Limits: getting closer without arriving](tutorial:approaching-a-limit),
from another course, meets the same holes and uses a limit to find the
speed of a falling ball.

Up and Atom (2020). *3 Paradoxes That Gave Us Calculus.*
<https://www.youtube.com/watch?v=EbHqtENNnSY>. Jade Tan-Holmes starts
where this page starts, going halfway and then halfway again, and follows
two more old puzzles to the limit. About fourteen minutes.
