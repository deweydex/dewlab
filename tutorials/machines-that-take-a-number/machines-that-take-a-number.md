---
title: "Machines that take a number: functions in maths and code"
year: "2026-2027"
version: 2026.09.24.1
covers:
  a-machine-with-one-slot:
    covers: [MIT-3.1]
    touches: [PDP-LO8]
  what-goes-in-and-what-comes-out:
    covers: [MIT-3.1]
    touches: [PDP-LO9]
  an-algorithm-is-a-function-too:
    covers: [MIT-6.2]
    touches: [PDP-LO6]
  functions-that-give-back-and-procedures-that-do:
    covers: [PDP-LO8]
  running-it-backwards-the-inverse:
    covers: [MIT-3.1]
  machines-in-a-row-composition:
    covers: [MIT-3.1, PDP-LO8]
---

# Machines that take a number: functions in maths and code

At the end of a taxi ride, the meter shows a price. It was given one
number, the distance, and it gave back one number, the fare. Nobody at
the taxi rank calls the meter a function, but that is what it is.

What does it mean for something to take an input and give an output?
And what happens when you give it an input it was never built for?

On this page we:

- write one rule as a function in maths and in Python, and see that the
  two are the same idea
- ask which inputs a function accepts, and which outputs it can give
- see an algorithm as a function on a set of inputs
- tell a function that gives back a value from one that only does
  something
- run a function backwards, with its inverse
- join two functions into one, and add `compose` to the toolkit

> **The space we're in.** Most functions on this page take one number
> and give one number back. We work in the real numbers, $\mathbb{R}$,
> where no number squares to make a negative one. Python gives us `def`
> and `return`, which we met on
> [Numbers a computer can hold](tutorial:numbers-a-computer-can-hold).
> One thing usually goes unsaid: Python never checks that a function
> keeps its promise. The docstring says the promise, and tests check it.

## Warm-up

Two questions from earlier pages. The first is from
[Doing it again](tutorial:doing-it-again), and the second from
[Orders and choices](tutorial:orders-and-choices).

```question
id: machines-warm-up-1
type: fill-in-the-blank

We start with `total = 0`. Then the loop `for day in range(7):` adds 3
to `total` each time round. When the loop ends, `total` is {21}.
```

```question
id: machines-warm-up-2
type: multiple-choice
correct: 3

Your toolkit's `factorial` promises the number of orders of `n`
different things. What does `factorial(4)` give back?

- 4
- 10
- 24
- 16
```

## A machine with one slot

Picture a machine with a slot on one side and a tray on the other. You
put a number in the slot. The machine follows its rule, and a number
drops into the tray. The same number in always gives the same number
out.

Here is a taxi meter's rule, in words. The numbers are made up, but they
are close to a real Irish fare: "start at €4, then add €1.50 for every
kilometre."

Maths writes that rule like this:

$$f(x) = 4 + 1.5x$$

We read $f(x)$ as "f of x". The letter $f$ is the function's name, $x$
stands for the input, and the right-hand side is the rule. So $f(10)$
means "put 10 in the slot":
$f(10) = 4 + 1.5 \times 10 = 19$. Writing a function this way is called
*function notation*.

Python writes the same rule with `def`. Before you run the cell, what
will each line show?

```python exec
id: machines-slot-1
def fare(km):
    """Return the taxi fare in euro for a trip of km kilometres."""
    return 4 + 1.5 * km

print(fare(10))
print(fare(2))
```

The cell shows `19.0` and `7.0`. Put the two versions side by side, and
every part of one has a partner in the other:

| | Maths | Python |
|---|---|---|
| the function's name | $f$ | `fare` |
| the input's name | $x$ | `km` |
| the rule | $4 + 1.5x$ | `4 + 1.5 * km` |
| using it on 10 | $f(10)$ | `fare(10)` |

These are not two ideas that happen to look alike. They are one idea,
written two ways. In maths, a function is a rule that gives exactly
one output for each input. A Python function that takes a number and
returns a number keeps the same promise.

Two words help us talk about the slot. On
[Recipes are algorithms](tutorial:recipes-are-algorithms) we met the
parameter: the name in the brackets of the `def` line, here `km`. The
value we put in when we call the function, here `10`, is the
*argument*. The parameter is the slot, and the argument is what goes
into it.

### Your turn

At night the fare is higher: €5 to start, then €1.80 for every
kilometre.

1. Change the rule in the cell below to the night rate.
2. Before you run it, work out what a 10 km trip costs at night.
3. Add a line that prints `night_fare(0)`. What does a trip of 0 km
   cost, and why?

```python exec
id: machines-slot-your-turn
def night_fare(km):
    """Return the night fare in euro for a trip of km kilometres."""
    return 4 + 1.5 * km   # change this to the night rate

print(night_fare(10))
```

## What goes in and what comes out

Can we put any number in the taxi slot? Python will run `fare(-3)`
without a word of complaint, and give back `-0.5`. A trip of −3 km
means nothing, and nobody is paid 50 cent to ride in a taxi. Python
followed the rule. The rule did not know which numbers it was meant
for.

The *domain* of a function is the set of inputs it accepts. The *range*
is the set of outputs it can give. For the taxi meter:

- the domain is every distance from 0 up: $x \ge 0$;
- the range is every fare from €4 up: $f(x) \ge 4$.

Some functions in Python do check their domain. Here is one. The
*square root* of a number is the number that, multiplied by itself,
makes it. The square root of 16 is 4, because $4 \times 4 = 16$. We
write it $\sqrt{16}$, and Python keeps it in the `math` module as
`math.sqrt`.

What do you think each line will do? The last line is meant to stop
with an error.

```python exec
id: machines-domain-1
import math

print(math.sqrt(16))
print(math.sqrt(2))
print(math.sqrt(-4))
```

The first two lines show `4.0` and `1.4142135623730951`. Now read the
last line of the error, as we did on
[When Python says no](tutorial:when-python-says-no):

`ValueError: math domain error`

Python uses the mathematician's own word. A *ValueError* means the value
was the right kind of thing, a number, but outside what the function
accepts. That is different from a `TypeError`, which means the wrong
kind of thing altogether.

So is asking for $\sqrt{-4}$ a foolish move? No. It has no answer in
$\mathbb{R}$, because every real number, multiplied by itself, gives 0
or more. Unit 7 builds a bigger space where $-4$ does have a square
root. The move is fine; it needs a different space.

Our own `fare` can say its domain too. The docstring says it in words,
and an `assert` at the top checks it. After the comma, an `assert` can
carry a message, which Python shows if the check fails. The last line
of this cell is meant to stop with an error.

```python exec
id: machines-domain-2
def fare(km):
    """Return the taxi fare in euro for a trip of km kilometres.

    km must be 0 or more.
    """
    assert km >= 0, "a trip cannot be shorter than 0 km"
    return 4 + 1.5 * km

print(fare(3))
print(fare(-3))
```

This time the last line of the error is
`AssertionError: a trip cannot be shorter than 0 km`. An error with a
message like that is a kindness to whoever calls the function next,
and that person is often you, a few weeks later.

```question
id: machines-range-round
type: multiple-choice
correct: 2

`round(x)` accepts any real number $x$ and rounds it to the nearest
whole number. What is its range?

- every real number
- the whole numbers, the integers
- the numbers from 0 to 9
```

## An algorithm is a function too

On [Doing it again](tutorial:doing-it-again) we added up
$1 + 2 + \dots + n$ in two ways. A loop added the numbers one at a time.
Gauss's trick paired the ends, and gave

$$1 + 2 + \dots + n = \frac{n(n + 1)}{2}$$

Let's write both ways as functions, and look at them as machines. Will
they agree for 100?

```python exec
id: machines-algorithm-1
def sum_by_loop(n):
    """Return 1 + 2 + ... + n, adding one number at a time.

    n is a whole number, 0 or more.
    """
    running_total = 0
    for number in range(1, n + 1):
        running_total = running_total + number
    return running_total


def sum_by_formula(n):
    """Return 1 + 2 + ... + n, using n(n + 1) / 2.

    n is a whole number, 0 or more.
    """
    # n(n + 1) is always even, so // loses nothing and keeps an int.
    return n * (n + 1) // 2


print(sum_by_loop(100), sum_by_formula(100))
```

Both give 5050. Inside, the steps are completely different. One makes a
hundred additions, and the other makes one multiplication and one
division. But from the outside, as machines, the two cannot be told
apart: the same input always gives the same output.

This is how mathematicians think of an algorithm. An algorithm, the list
of clear steps we met on
[Four questions for any puzzle](tutorial:four-questions), is a function
on a domain of inputs: for each input it is built for, it gives one
output. The function says what comes out. The algorithm says how we get
there. Two algorithms can be one function.

Let's check that claim on a lot of the domain at once. How long do you
expect this to take?

```python exec
id: machines-algorithm-2
for n in range(0, 1001):
    assert sum_by_loop(n) == sum_by_formula(n)
print("They agree for every n from 0 to 1000.")
```

A thousand and one checks, and every one passed. Now let's try an input
from outside the domain. "Add up the whole numbers from 1 to −5" does
not mean anything. What will each function do with it?

```python exec
id: machines-algorithm-3
print(sum_by_loop(-5), sum_by_formula(-5))
```

The loop gives `0`, because `range(1, -4)` is empty, so it adds nothing.
The formula gives `10`. Outside the domain, the two machines disagree,
and neither answer is right, because the question has no answer. That is
why the domain belongs in the promise. Both functions promised the same
thing, for whole numbers from 0 up, and both kept that promise.

## Functions that give back, and procedures that do

Not every function hands back a value. Some do a job instead: they
print a receipt, draw a picture or save a file. Here is one. What will
the last line show?

```python exec
id: machines-procedure-1
def show_receipt(km):
    """Print a receipt for a taxi trip of km kilometres."""
    print("Distance in km:", km)
    print("Fare in euro:", fare(km))


result = show_receipt(8)
print("show_receipt gave back:", result)
```

The receipt appears, and then `show_receipt gave back: None`. *None* is
Python's value for "nothing here". A function with no `return` line
gives back `None` when it finishes.

A *procedure* is a function that does a job, such as printing, instead
of giving back a value. Python writes both with `def`. Some older
languages, such as Pascal, use two different words for them. The
difference matters when we build with them. `fare(8) + 2` is a number
we can use. `show_receipt(8) + 2` asks Python to add `None` and 2, and
stops with a `TypeError`.

Look at how `show_receipt` gets its fare. It does not work the fare out
again: it calls `fare`. Splitting a program into small functions, each
with one job, is called *modularisation*. When the taxi rate changes,
we change `fare`, and every receipt is right at once.

A call can also name its arguments. `fare(km=8)` puts 8 into the slot
called `km`. This is a *keyword argument*, and it helps most when a
function has several slots. Your toolkit's `split_bill` has three.
Before you run this, what will each person pay?

```python exec
id: machines-procedure-2
print(split_bill(fare(12), 3))
print(split_bill(fare(12), people=3, tip_percent=10))
```

Each person pays €7.33, or €8.07 with a 10% tip. Look at the order of
events. Python works out `fare(12)` first, and gets 22.0. Only then
does that number go into `split_bill`. The inside of the brackets
happens before the outside, as it did with `print(3 * 250)` on the
first page of this course.

## Running it backwards: the inverse

The receipt fell out of your pocket, but you remember paying €19. How
far did you go?

The meter's rule did two things, in order: multiply by 1.5, then add 4.
To go backwards, undo each step in the opposite order. First take away
4, then divide by 1.5:

$$f^{-1}(y) = \frac{y - 4}{1.5}$$

We read $f^{-1}$ as "f inverse". The *inverse* of a function is a
function that undoes it: if $f$ takes $x$ to $y$, then $f^{-1}$ takes
$y$ back to $x$. The −1 here is a name, not a power.

What will these three lines show? The second and third put one machine's
output into the other's slot.

```python exec
id: machines-inverse-1
def distance_for(euro):
    """Return how many km a taxi trip was, if it cost euro euro."""
    return (euro - 4) / 1.5

print(distance_for(19))
print(distance_for(fare(7)))
print(fare(distance_for(31)))
```

The answers are `10.0`, `7.0` and `31.0`. Going forward and then back
lands where we started, whichever way round we go. Notice that the
domain of `distance_for` is the range of `fare`. A fare of €2 is not in
that range, and `distance_for(2)` gives a negative distance, which means
nothing. A later page in this unit,
[Running a formula backwards](tutorial:running-a-formula-backwards),
undoes formulas in general, one step at a time.

Does every function have an inverse? Try squaring. What will each line
show?

```python exec
id: machines-inverse-2
import math

def square(x):
    """Return x multiplied by itself."""
    return x * x

print(square(3), square(-3))
print(math.sqrt(square(3)), math.sqrt(square(-3)))
```

Both 3 and −3 square to 9. So if the tray shows 9, which number went in?
There is no way to know, and an inverse must give one answer. The square
root chooses 3, which is right for 3 and wrong for −3.

A function has an inverse only when each output comes from exactly one
input. Such a function is called *one-to-one*. Squaring on all of
$\mathbb{R}$ is not one-to-one. But on a smaller space, the numbers from
0 up, it is, and there $\sqrt{x}$ is its inverse. A move that fails in
one space can work in another. This time the space that works is
smaller.

```question
id: machines-inverse-round
type: multiple-choice
correct: 3

Does `round` have an inverse?

- Yes: add 0.5 to the answer.
- Yes: `round` is its own inverse.
- No: `round(2.4)` and `round(1.6)` both give 2, so 2 cannot say which went in.
```

## Machines in a row: composition

Last section, `split_bill(fare(12), 3)` sent the output of one machine
straight into the slot of the next. Joining two functions this way is
called *composition*. Maths writes "g after f" as

$$(g \circ f)(x) = g(f(x))$$

The small circle is read "after", and it is a reminder that $f$ runs
first, even though it is written second.

Does the order matter? A shop adds €5 for delivery, and has a sale with
10% off. Here are both orders, on a €50 jacket. Predict both answers.

```python exec
id: machines-compose-1
def add_delivery(price):
    """Return the price with €5 delivery added."""
    return price + 5


def take_ten_percent_off(price):
    """Return the price with 10% taken off."""
    return price * 0.9


print(take_ten_percent_off(add_delivery(50)))
print(add_delivery(take_ten_percent_off(50)))
```

The first order gives €49.50, because the discount comes off the
delivery too. The second gives €50.00. The same two machines, in a
different order, give a different answer. That is sequence, the third of
our four questions: what happens when?

### Your turn: a tool that joins machines

Your toolkit already takes functions as inputs: `truth_table` was given
a rule. `compose` goes one step further. It takes two functions and
gives back a new function. Here is its promise:
`compose(outer, inner)` is a function that, given `x`, returns
`outer(inner(x))`.

Replace the `...` with three lines:

1. Inside `compose`, start a new function with `def both(x):`, pushed
   in one level.
2. Inside `both`, pushed in one more level, return `outer(inner(x))`.
3. Back at the level of `def both`, write `return both`, with no
   brackets after `both`. The brackets would call it; without them, we
   hand over the function itself.

```python exec
id: machines-toolkit
toolkit: yes
def compose(outer, inner):
    """Return a new function that runs inner on its input, then outer on the result.

    compose(outer, inner)(x) gives the same answer as outer(inner(x)).
    """
    ...
```

```python toolkit-reference
for: machines-toolkit
def compose(outer, inner):
    """Return a new function that runs inner on its input, then outer on the result.

    compose(outer, inner)(x) gives the same answer as outer(inner(x)).
    """
    def both(x):
        return outer(inner(x))
    return both
```

```hint
What does `compose(add_delivery, square)` give back at the moment? Try
`print(compose(add_delivery, square))` on its own. A function you can
call is shown as `<function ...>`.
```

```hint
after: 10 errors
title: some steps
1. The first line under the docstring is `def both(x):`, pushed in as
   far as the docstring.
2. The line under that is pushed in one level further, and starts with
   `return`.
3. The last line is back at the level of `def both(x):`, and gives
   back `both`.

**Think about:** why `return both` and not `return both(x)`? Which one
hands back a machine, and which one hands back a number?
```

Now the tests. Until `compose` is written, the first test stops with an
error. That is the test doing its job. What do you notice about the
third test?

```python exec
id: machines-toolkit-tests
sale_price = compose(take_ten_percent_off, add_delivery)
assert sale_price(50) == take_ten_percent_off(add_delivery(50))
assert compose(add_delivery, take_ten_percent_off)(50) == 50
assert compose(distance_for, fare)(10) == 10
assert compose(math.sqrt, square)(-3) == 3
print("compose keeps its promise.")
```

The third test joins `fare` to its own inverse, and 10 comes straight
back out. That is one way to say what an inverse is:
$f^{-1}(f(x)) = x$ for every $x$ in the domain. The last test is the
square root failing to undo squaring: −3 went in, and 3 came out.

One thing may seem strange. `both` is made inside `compose`, and still
knows `outer` and `inner` after `compose` has finished. A later page in
this unit, [What a function can see](tutorial:what-a-function-can-see),
explains how.

### Your turn

1. Write `add_vat(price)`, which adds 23% VAT to a price. (Multiply by
   1.23.)
2. Make `compose(add_vat, add_delivery)`, and try it on a €40 order.
3. Now compose them the other way round. Before you run it, which order
   do you think costs more, and why?

```python exec
id: machines-compose-your-turn
# Your add_vat, and both orders
```

<details class="dl-why"><summary>Why this way?</summary>

This page showed a function as a machine with a slot and a tray.
Mathematicians define a function another way: as a set of pairs, each
input paired with exactly one output, with no machine in sight.

The set of pairs is the definition a university course would use. It
covers functions no machine could ever run, and it makes proofs exact.

We used the machine because it answers "what is promised?" with a
picture you can keep in your head. It also fits Python, where `def` does
build something you put values into. The picture has a cost. It hides
the fact that a function is only its pairs, and that fact is why two
different machines, the loop and Gauss's formula, could be one
function.

</details>

## Four questions, looking back

| The question | On this page |
|---|---|
| What is named here? | a function ($f$, `fare`), its input ($x$, `km`), and the value put in, the argument |
| What is promised? | one output for each input in the domain; an inverse promises to undo; `compose` promises a new function |
| What happens when? | the inside of the brackets first; in $g(f(x))$, $f$ runs first; the order of two machines can change the answer |
| What does this space let us do? | the domain says which inputs are allowed; $\sqrt{-4}$ needs a bigger space; squaring has an inverse only on a smaller one |

## What we have now

| Term | What it means |
|---|---|
| $f(x)$ | function notation: the function $f$, used on the input $x$ |
| argument | the value put into a parameter when a function is called |
| domain, range | the inputs a function accepts; the outputs it can give |
| `math.sqrt(x)` | the square root of $x$: the number that, times itself, makes $x$ |
| `ValueError` | the right kind of value, but outside what the function accepts |
| `assert condition, "message"` | a check that shows a message when it fails |
| algorithm as a function | for each input in its domain, one output; two algorithms can be one function |
| procedure, `None` | a function that does a job and gives back nothing; Python's value for nothing |
| modularisation | splitting a program into small functions, each with one job |
| keyword argument | naming the slot in a call: `fare(km=8)` |
| inverse, $f^{-1}$ | the function that undoes $f$ |
| one-to-one | each output comes from exactly one input; only these have inverses |
| composition, $g \circ f$ | $g(f(x))$: the output of $f$ goes into $g$ |
| `compose(outer, inner)` | your toolkit function that joins two machines into one |
