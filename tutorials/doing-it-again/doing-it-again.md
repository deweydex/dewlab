---
title: "Doing it again: loops, sums and products"
year: "2026-2027"
version: 2026.09.25.1
covers:
  a-ball-that-bounces:
    touches: [PDP-LO6]
  doing-it-for-each:
    covers: [PDP-LO6]
  a-running-total:
    covers: [PDP-LO6]
  counting-with-range:
    covers: [PDP-LO6]
  sigma-a-loop-written-by-mathematicians:
    covers: [MIT-6.4]
  pi-multiplying-instead-of-adding:
    covers: [MIT-6.4]
  until-something-is-true-while:
    covers: [PDP-LO6]
  two-tools-for-your-toolkit:
    touches: [MIT-6.4, PDP-LO6]
---

# Doing it again: loops, sums and products

Drop a ball on a hard floor. It bounces back up, not quite as high, then
again, a little lower, and again. So when does it stop? And how far has
it travelled by then?

Here is something odd to keep in mind. In the maths on this page, the
ball never stops bouncing, and it still travels less than 10 metres.
That sounds impossible. By the end of the page you will see it happen.

On this page we:

- repeat lines for each value in a list, with `for`
- keep a running total, and count with `range()`
- read sigma, $\sum$, and pi, $\prod$: loops written by mathematicians
- repeat until something is true, with `while`
- add `total` and `product` to your toolkit

> **The space we're in.** Numbers, and lines of Python that run from the
> top down. New on this page: a few lines can run again and again. Our
> ball is a *model*: a simple version of the real thing. It keeps exactly
> the same fraction of its height at every bounce, which a real ball does
> only roughly.

## Warm-up

Two questions from earlier pages. The first is from
[Numbers a computer can hold](tutorial:numbers-a-computer-can-hold), and
the second from
[True, false and every case](tutorial:true-false-and-every-case).

```question
id: doing-it-warm-up-1
type: fill-in-the-blank

A year starts on a Monday, day 1. Day 15 is also a Monday. `15 % 7`, the
remainder after taking out whole weeks, is {1}.
```

```question
id: doing-it-warm-up-2
type: multiple-choice
answer: 3

A loop over `[False, True]` sits inside another loop over
`[False, True]`. The inner loop prints one line each time round. How
many lines are printed in all?

- 2
  - This counts the outer loop only.
- 3
  - This adds the loops, 2 + 1, rather than multiplying.
- 4
  - The inner loop runs twice for each of the outer loop's two turns: 2 × 2.
- 8
  - This is 2 × 2 × 2, as if there were three loops.
```

## A ball that bounces

We drop the ball from 100 cm, which is 1 metre. It keeps 80% of its
height at each bounce, so the first bounce goes up to 80 cm, and the
second to 80% of that, 64 cm. How high is the tenth bounce? Guess
before you run the cell.

```python exec
id: doing-it-ball-1
keep = 0.8
print(100 * keep)
print(100 * keep * keep)
print(100 * keep ** 10)
```

The tenth bounce reaches about 10.7 cm. (The tiny 6 at the end of
`10.737418240000006` is float rounding, as on
[Everything is ones and zeros](tutorial:everything-is-ones-and-zeros#why-01-02-is-not-03).)

<aside class="dl-note" id="doing-it-note-tennis">

**How bouncy is a real ball?** Tennis balls are tested with this very
question. The rules of the International Tennis Federation say a ball
dropped from 254 cm onto concrete must bounce back to between 135 and
147 cm. So a tennis ball keeps a little over half its height. Our ball,
at 80%, is bouncier.

</aside>

But the question at the top needs every bounce, added up: "do this
again, once for each bounce". On
[Recipes are algorithms](tutorial:recipes-are-algorithms#steps-that-repeat-and-steps-that-choose)
that was repetition.

## Doing it for each

Here are the first five bounce heights, to the nearest centimetre, and
a plan in pseudocode:

```text
SET bounces TO the five heights, first to fifth
REPEAT for each height in bounces:
    SHOW the height
SAY the ball is still bouncing
```

In Python, the square brackets make a *list*: a row of values, kept in
order, under one name. Unit 5 looks at lists properly. How many lines
will the cell print? Count before you run it.

```python exec
id: doing-it-for-1
bounces = [80, 64, 51, 41, 33]

for height in bounces:
    print(height)
print("The ball is still bouncing.")
```

Six lines: one for each of the five heights, then one more. Here is what
happened, in order.

1. The `for` line pointed the name `height` at 80, and Python ran the
   pushed-in line. Then it pointed `height` at 64, and ran it again, and
   so on to the end of the list.
2. When the list ran out, Python went on to the first line that is not
   pushed in.

A `for` loop runs some lines once for each value in a row of values. You
met one on [True, false and every case](tutorial:true-false-and-every-case),
going through `[False, True]`. The pushed-in lines are the *loop body*.
The name on the `for` line, here `height`, is the *loop variable*: each
time round, it points at the next value.

### Your turn

1. Put a sixth height, 26, on the end of `bounces`, and run the cell.
2. Put four spaces in front of the last line, so that it is pushed in
   like `print(height)`. Before you run it, how many times will that
   line print? Then take the spaces out again.

## A running total

Now the distance. The ball falls 100 cm. Then each bounce goes up and
comes down, so it adds its height twice. On paper:

| Bounce | Height | Travelled so far |
|---|---|---|
| (the drop) | | 100 |
| 1 | 80 | 260 |
| 2 | 64 | 388 |

Each row takes the distance so far, and adds twice the new height. A
*running total* is a name that holds the total so far, and grows each
time round the loop. What will the last line print?

```python exec
id: doing-it-running-1
bounces = [80, 64, 51, 41, 33]

travelled = 100
for height in bounces:
    travelled = travelled + 2 * height
    print("so far:", travelled)
print("After five bounces:", travelled, "cm")
```

After five bounces the ball has travelled 638 cm. In maths, "travelled
equals travelled plus something" would be false. In Python, `=` is an
instruction, in two steps. First, Python works out the right-hand side,
using the old value of `travelled`. Then it points the name `travelled`
at the answer. `travelled += 2 * height` is short for the same line.

Where each line sits matters too.

```question
id: doing-it-running-2
type: multiple-choice
answer: 2

Someone moves `travelled = 100` inside the loop, just above the line
that adds. What does the last line print now?

- After five bounces: 638 cm
  - This is the old total, when `travelled = 100` ran once, before the loop.
- After five bounces: 166 cm
  - Each time round, `travelled` starts again at 100, so only the last bounce is added: 100 + 2 × 33.
- After five bounces: 100 cm
  - The addition still runs after the reset each time round.
- An error, because `travelled` is made twice
  - Python lets a name be given a new value as often as you like.
```

Each time round, the loop would set `travelled` back to 100, so at the
end it holds only the drop and the last bounce: $100 + 2 \times 33 =
166$. A running total must start before the loop.

## Counting with range()

When the loop should count, `range()` gives the numbers, as on
[Untangling a condition](tutorial:untangling-a-condition#not-between).
`range(1, 8)` gives the whole numbers from 1 up to 7. The last number,
8, is left out.

```python exec
id: doing-it-range-1
for bounce in range(1, 8):
    print("bounce", bounce)
```

Now 20 bounces, with Python working out each height from the last one.
Guess how far the ball travels. Then change `keep` to 0.5, and to 0.9,
and guess again each time.

```python exec
id: doing-it-range-2
keep = 0.8

height = 100
travelled = 100
for bounce in range(1, 21):
    height = height * keep
    travelled = travelled + 2 * height
print("the 20th bounce:", round(height, 2), "cm")
print("travelled:", round(travelled, 1), "cm")
```

With `keep = 0.8`, the 20th bounce is just over 1 cm high, and the ball
has travelled about 890.8 cm. The order of the two lines in the body
matters: first the new height, then the distance.

### Choosing inside a loop

How many bounces come up between ankle height, about 10 cm, and knee
height, about 50 cm? Your toolkit has the tool for "from 10 to 50":
[`between`](tutorial:choosing-a-path#a-tool-of-your-own-between). Guess
first.

```python exec
id: doing-it-range-3
height = 100
middle = 0
for bounce in range(1, 21):
    height = height * 0.8
    if between(height, 10, 50):
        middle = middle + 1
        print("bounce", bounce, "reaches", round(height, 1), "cm")
print(middle, "bounces")
```

Seven, from the 4th to the 10th. This small program keeps values under
names: that is *storage*. It chooses with `if`, which is selection, and
repeats with `for`, which is iteration. Those are the three shapes of
step from [Recipes are algorithms](tutorial:recipes-are-algorithms), and
they can build any program. Planning a program from them is called
*structured design*.

Your turn: change 0.8 to 0.9. Do more bounces land between 10 and
50 cm, or fewer? Guess first.

## Sigma: a loop written by mathematicians

Maths writes a row of numbers like our heights as
$h_1, h_2, h_3$ and so on. The small number is the *index*: it says
which one we mean. So $h_3$ is the height of bounce 3, and $h_k$ is the
height of bounce $k$. For our ball, $h_k = 100 \times 0.8^k$.

Adding up all of them is written with a Greek capital S, called sigma:

$$\sum_{k=1}^{20} h_k$$

This is *sigma notation*: "add up every value, for each index from here
to there". It is a loop, written by mathematicians:

| In the sigma | What it says | In Python |
|---|---|---|
| $k = 1$, underneath | start the index at 1 | `for k in range(1, ...)` |
| $20$, on top | stop after 20, and include it | `range(..., 21)`, one past the end |
| $h_k$, after the sigma | what to add each time | `added = added + 100 * 0.8 ** k` |
| $\sum$ itself | add them all up | a running total that starts at 0 |

The whole distance is the drop plus every height twice:
$100 + 2\sum_{k=1}^{20} h_k$. Will this agree with the 890.8 cm from the
last section?

```python exec
id: doing-it-sigma-1
added = 0
for k in range(1, 21):
    added = added + 100 * 0.8 ** k
print(round(added, 1))
print(round(100 + 2 * added, 1))
```

### The most famous sigma

The most famous sigma is $1 + 2 + 3 + \dots + n$. A story says that a
young Carl Friedrich Gauss was asked to add 1 to 100 at school, and
found the answer in a moment. Write the numbers forwards, and under them
write them backwards:

| forwards | 1 | 2 | 3 | … | 99 | 100 |
|---|---|---|---|---|---|---|
| backwards | 100 | 99 | 98 | … | 2 | 1 |
| added | 101 | 101 | 101 | … | 101 | 101 |

Every column adds to 101, and there are 100 columns. So the two rows
make $100 \times 101$, which is the sum twice, and the sum is 5,050. In
words: the sum of 1 to $n$ is $n$ times $n + 1$, halved.

$$\sum_{i=1}^{n} i = \frac{n(n+1)}{2}$$

A formula like this is a promise, so let's check it. Python's built-in
`sum()` adds up a row of values. Will the two columns agree?

```python exec
id: doing-it-sigma-2
for n in [1, 2, 3, 10, 100, 365]:
    print(n, sum(range(1, n + 1)), n * (n + 1) // 2)
```

They agree every time. The formula is faster; the loop is the one we
can follow step by step.

### The ball that never stops

The ball's sum has a formula too. A sum where each value is the last
one times the same number $r$ is a *geometric series*:

$$\sum_{k=1}^{n} r^k = r \times \frac{1 - r^n}{1 - r}$$

For our ball, $r = 0.8$. As $n$ grows, $r^n$ gets closer and closer to
0: $0.8^{100}$ is about 0.0000000002. So the sum gets closer and closer
to $0.8 \times \frac{1}{0.2} = 4$, and never goes past it. What do you
think the distance will settle at?

```python exec
id: doing-it-sigma-3
r = 0.8
for n in [1, 5, 20, 50, 100]:
    by_loop = 0
    for k in range(1, n + 1):
        by_loop = by_loop + r ** k
    by_formula = r * (1 - r ** n) / (1 - r)
    print(n, round(by_loop, 6), round(by_formula, 6), round(100 + 200 * by_loop, 2))
```

The loop and the formula agree, and the distance settles at 900 cm. The
ball has no last bounce, and the whole journey is 9 metres. I
think this is the strangest result on the page. Unit 9's
[Getting closer](tutorial:getting-closer) names this settling: a limit.

<aside class="dl-note" id="doing-it-note-buzz">

**You can hear it.** A lower bounce is also a quicker one. In the model
the times shrink fast enough to add up to a few seconds. Drop a table tennis ball on a table and
listen: the taps come faster and faster, blur into a buzz, and stop.

</aside>

### Your turn

1. What is $\sum_{i=1}^{5} i^2$, which is $1^2 + 2^2 + 3^2 + 4^2 + 5^2$?
   Work it out on paper first.
2. Change the loop below so that it adds `i ** 2` each time, and check.
3. Try $\sum_{i=1}^{10} 2i$. What do you notice about the answer?

```python exec
id: doing-it-sigma-your-turn
result = 0
for i in range(1, 6):
    result = result + i
print(result)
```

## Pi: multiplying instead of adding

Schlomo, who is learning Python too, has a quicker idea. "Each bounce
loses 20% of the height. So after five bounces the ball has lost 100%,
and it stops." Is he right? Decide before you read on.

After five bounces the height has been multiplied by 0.8 five times. We
need a running product: a number that is multiplied, not added, each
time round.

```question
id: doing-it-pi-1
type: multiple-choice
answer: 2

A running total starts at 0. What should a running product start at?

- 0
  - Anything times 0 is 0, so the product would stay 0.
- 1
  - 1 is the number that changes nothing when you multiply by it.
- The first value in the list
  - This works too, if the loop then starts from the second value.
```

It starts at 1. Adding 0 changes nothing, so a total starts at 0.
Multiplying by 1 changes nothing, so a product starts at 1.

What fraction of its height does the ball keep after five bounces?

```python exec
id: doing-it-pi-2
keeps = [0.8, 0.8, 0.8, 0.8, 0.8]

kept = 1
for keep_now in keeps:
    kept = kept * keep_now
print(round(kept, 4))
print(round(100 * kept, 1), "cm")
```

The ball still keeps about 33% of its height, and reaches 32.8 cm.
Schlomo's idea was reasonable: for one or two small changes, adding the
percentages comes close. But each bounce loses 20% of a height that has
already shrunk. The losses multiply, and multiplying is the space they
live in.

Maths writes a product of many values with a Greek capital P, called pi:

$$\prod_{k=1}^{5} r_k = r_1 \times r_2 \times r_3 \times r_4 \times r_5$$

where $r_k$ is the fraction kept at bounce $k$. This is *pi notation*:
sigma, with multiplying in place of adding. Every $r_k$ is 0.8 here, so
the product is $0.8^5$. A power is a product of one number: $2^{10}$ on
[Numbers a computer can hold](tutorial:numbers-a-computer-can-hold#powers-and-how-many-times)
is $\prod_{i=1}^{10} 2$.

## Until something is true: while

When does a bounce first come up less than 1 cm? This time we do not
know how many times to go round. We know when to stop.

A *while loop* runs its body for as long as a condition is True. It
checks the condition before each round, and ends as soon as the
condition is False. Guess the bounce first.

```python exec
id: doing-it-while-1
keep = 0.8
height = 100
bounces_so_far = 0
while height >= 1:
    height = height * keep
    bounces_so_far = bounces_so_far + 1
print("Bounce", bounces_so_far, "reaches", round(height, 2), "cm.")
```

Bounce 21 is the first under 1 cm, at 0.92 cm. On Recipes are
algorithms we asked of every repeat: what makes it end? This loop ends
because `height` shrinks every round. Here is one that never would:

```python
height = 100
while height >= 1:
    height = height * 1.2    # a ball that bounces higher every time
```

No real ball can do that, but Python does not know about balls. If a
loop like this runs in a cell, the **Run** button turns into **Stop**.
Press it, and Python stops.

### Watching it bounce

The next cell builds the heights for a short film, with a `for` loop
inside a `while` loop, and matplotlib plays it. You do not need to
follow the drawing part yet.

Guess first: with `keep = 0.8`, will you see all 21 bounces? Then try
`keep = 0.5` and `keep = 0.95`, and guess each time.

```python exec
id: doing-it-while-watch
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

keep = 0.8                 # change this, and guess first

# The ball's height in every frame, built one bounce at a time.
path = []
height = 100
start = 8                  # the drop starts at the top of an arc
while height >= 1:
    frames_in_arc = max(2, round(16 * (height / 100) ** 0.5))   # lower is quicker
    for step in range(start, frames_in_arc + 1):
        u = step / frames_in_arc                   # 0 at the floor, 1 back at the floor
        path.append(4 * height * u * (1 - u))      # the top of the arc is at height
    start = 1
    height = height * keep

# Drawing: a grey trail, and the ball at the end of it.
figure, stage = plt.subplots(figsize=(3.2, 2.0))
stage.set_xlim(0, len(path))
stage.set_ylim(-4, 105)
stage.set_xlabel("time")
stage.set_ylabel("height (cm)")
figure.tight_layout()
trail, = stage.plot([], [], color="grey", linewidth=1)
ball, = stage.plot([], [], "o", markersize=9)

def draw_step(frame):
    trail.set_data(range(frame + 1), path[:frame + 1])
    ball.set_data([frame], [path[frame]])

skip = len(path) // 22 + 1          # at most 22 frames, so the film stays small
FuncAnimation(figure, draw_step, frames=range(0, len(path), skip), interval=140)
```

The grey trail draws each bounce as an arch. The arches get lower and
narrower, because a low bounce is also a quick one.

So which loop do you reach for? `for`, when you know the values, or how
many times: the first 20 bounces. `while`, when you know when to stop,
but not how many times: until a bounce is under 1 cm.

### Your turn

On which bounce has the ball first travelled more than 850 cm? Guess
first. Then write a `while` loop in the cell below that goes round while
`travelled` is 850 or less. Each round works out the new height, adds
it twice to `travelled`, and adds 1 to `bounces_so_far`.

```python exec
id: doing-it-while-your-turn
height = 100
travelled = 100
bounces_so_far = 0
# Your while loop here
print("Bounce", bounces_so_far, "and", round(travelled, 1), "cm so far")
```

## Two tools for your toolkit

Let's make adding up and multiplying into tools for later pages. In
`total`, the line inside the loop adds `0` where it should add each
value: change that `0`. `product` is a stub with only its promise
written. Write its body in the same shape as `total`, and remember
where a product starts.

```python exec
id: doing-it-toolkit
toolkit: yes
def total(values):
    """Add up every number in values, and return the sum.

    values can be a list, or a range. total([80, 64, 51]) is 195.
    With no values at all, the sum is 0.
    """
    running = 0
    for value in values:
        running = running + 0    # change this 0 so the line adds each value
    return running


def product(values):
    """Multiply every number in values together, and return the result.

    values can be a list, or a range. product([2, 3, 4]) is 24.
    With no values at all, the product is 1.
    """
    ...
```

```python toolkit-reference
for: doing-it-toolkit
def total(values):
    """Add up every number in values, and return the sum.

    values can be a list, or a range. total([80, 64, 51]) is 195.
    With no values at all, the sum is 0.
    """
    running = 0
    for value in values:
        running = running + value
    return running


def product(values):
    """Multiply every number in values together, and return the result.

    values can be a list, or a range. product([2, 3, 4]) is 24.
    With no values at all, the product is 1.
    """
    running = 1
    for value in values:
        running = running * value
    return running
```

Run the toolkit cell, then the tests. Until both tools are written,
a test stops with an `AssertionError`, telling you which promise is not
kept yet.

```python exec
id: doing-it-toolkit-tests
assert total([80, 64, 51]) == 195
assert total(range(1, 101)) == 5050           # Gauss's sum
assert total([]) == 0
assert product([2, 3, 4]) == 24
assert round(product([0.8, 0.8, 0.8, 0.8, 0.8]), 4) == 0.3277
assert product([]) == 1                       # nothing multiplied changes nothing
print("total and product keep their promises.")
```

```hint
Which test does the error point at? Print `total([80, 64, 51])` or
`product([2, 3, 4])` on its own, and compare it with what the test
expects.
```

```hint
after: 12 errors
title: some steps
1. In `total`, the loop points `value` at each number in turn. The line
   inside should add `value`, not `0`.
2. `product` has the same shape as `total`: a starting number, a loop,
   and a `return` after the loop.
3. A product starts at 1, and multiplies with `*`.

**Think about:** why must `return running` sit outside the loop, and
not inside it?
```

One thing about names. `total` is now a function. If a later cell says
`total = 0`, the name points at 0 instead, and the tool is gone from that
page. That is why this page used names like `travelled` and `kept`.

<details class="dl-why"><summary>Why this way?</summary>

Python already has `sum()`, and `math.prod()` in its `math` module.
Most programmers use them, for good reasons: they are tested, fast and
well known.

We wrote our own because a running total is the idea this page teaches,
and `sum()` hides it. Writing `total` shows the starting value, the loop,
and the line that runs again and again, and why a product starts at 1.
After that, `sum()` is not a mystery.

</details>

## Four questions, looking back

| The question | On this page |
|---|---|
| What is named here? | a list, `bounces`; a loop variable, `height`; running totals like `travelled`; the index $k$ in $h_k$ |
| What is promised? | one round of a `for` loop for each value; a sum and a product, from `total` and `product`; the same answer from each formula as from its loop |
| What happens when? | a running total starts before the loop; a `while` loop checks its condition before every round |
| What does this space let us do? | a total starts at 0 and a product at 1; losses multiply, they do not add; in the model, endless bounces add up to 9 metres |

## What we have now

| Term or tool | What it means |
|---|---|
| list | a row of values in square brackets, kept in order |
| `for x in values:` | run the pushed-in lines once for each value |
| loop body, loop variable | the pushed-in lines; the name that points at each value in turn |
| running total | the total so far: start it before the loop |
| `range(start, stop)` | whole numbers from `start` up to `stop`, leaving out `stop` |
| storage, selection, iteration | names, `if` and loops: the shapes of structured design |
| $\sum_{i=1}^{n} x_i$, $\prod_{i=1}^{n} x_i$ | sigma adds up $x_i$ for every $i$ from 1 to $n$; pi multiplies them |
| $\sum_{i=1}^{n} i = \frac{n(n+1)}{2}$ | the sum of 1 to $n$, found by pairing the ends |
| $\sum_{k=1}^{n} r^k = r \times \frac{1 - r^n}{1 - r}$ | a geometric series: each value is the last one times $r$ |
| `while condition:` | a loop that runs while the condition is True |
| `total(values)`, `product(values)` | your new toolkit tools |

The practice page is next. After it,
[Counting every outfit](tutorial:counting-every-outfit) puts one loop
inside another, and uses them to count.

For more on loops, the integrated course has
[Repeating steps with loops](tutorial:repeating-yourself).
