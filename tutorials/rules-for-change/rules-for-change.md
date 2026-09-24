---
title: "Rules for change: the sum, product, quotient and chain rules"
year: "2026-2027"
version: 2026.09.24.1
covers:
  a-pattern-in-the-slopes-the-power-rule:
    covers: [MIT-3.7]
    touches: [MIT-3.6]
  adding-rules-the-sum-rule:
    covers: [MIT-3.7]
    touches: [MIT-1.8, MIT-6.4]
  multiplying-rules-the-product-rule:
    covers: [MIT-3.7]
    touches: [MIT-1.3]
  dividing-rules-the-quotient-rule:
    covers: [MIT-3.7]
  a-rule-inside-a-rule-the-chain-rule:
    covers: [MIT-3.7]
    touches: [MIT-6.2, PDP-LO8]
  back-to-the-top-of-the-curve:
    covers: [MIT-3.7]
    touches: [MIT-3.4, MIT-1.9]
---

# Rules for change: the sum, product, quotient and chain rules

Your toolkit's `derivative_at` can find the slope of any curve, at any
point. Ask it about $x^2$ at 3, and it says about 6. At 5, it says about
10. Each answer is one number, a tiny bit off, and it comes with no
reason. Is there a shortcut: one rule that gives the slope everywhere
at once, exactly, and says why?

On this page we:

- find the power rule in a table of slopes, before we write it down
- build the slopes of bigger rules from smaller ones, with the sum,
  product, quotient and chain rules
- say each rule in words, then in symbols, and check it against
  `derivative_at` at many points
- come back to the top of Aoife's profit curve, and find it a second
  way

> **The space we're in.** Rules made from powers of $x$, added,
> multiplied, divided and put inside each other, over the real numbers.
> Every rule on this page is checked against `derivative_at` from
> [How fast, right now?](tutorial:how-fast-right-now), which is an
> estimate. So "agrees" means "agrees to within 0.00001", with
> `close_enough` from
> [Does it work?](tutorial:does-it-work#close-enough). One thing
> usually goes unsaid: a rule for slopes is a promise about every $x$,
> and checking 40 points does not prove it. It does catch almost every
> mistake.

## Warm-up

The first question is from
[Machines that take a number](tutorial:machines-that-take-a-number#machines-in-a-row-composition),
and the second from
[How fast, right now?](tutorial:how-fast-right-now#a-tool-for-the-slope-at-a-point).

```question
id: rules-for-warm-up-1
type: fill-in-the-blank

`double` doubles a number and `add_one` adds 1. Then
`compose(double, add_one)(5)` is {12}.
```

```question
id: rules-for-warm-up-2
type: multiple-choice
correct: 3

What does `derivative_at(rule, 2)` work out?

- the height of the graph of `rule` at 2
- the average of `rule` from 0 to 2
- the slope of a very short chord of `rule`, centred on 2
- the root of `rule` nearest to 2
```

## A pattern in the slopes: the power rule

Let's start with a table. The cell asks `derivative_at` for the slopes
of $x^2$, $x^3$ and $x^4$ at the whole numbers from 1 to 5, and rounds
them to 4 places. Before you run it, guess the slope of $x^2$ at 4.

```python exec
id: rules-for-power-1
def squared(x):
    return x ** 2

def cubed(x):
    return x ** 3

def fourth_power(x):
    return x ** 4

print("x", "x²", "x³", "x⁴")
for x in range(1, 6):
    print(x, round(derivative_at(squared, x), 4),
          round(derivative_at(cubed, x), 4),
          round(derivative_at(fourth_power, x), 4))
```

Look down each column. For $x^2$ the slopes are 2, 4, 6, 8, 10: always
twice $x$. For $x^3$ they are 3, 12, 27, 48, 75: three times $x^2$. Can
you see the pattern in the $x^4$ column before reading on?

It is 4, 32, 108, 256, 500: four times $x^3$. In each column, the power
comes down in front, and the new power is one less. In words: to find
the slope of $x$ to a power, multiply by the power, and take one off
the power. This is the *power rule*:

$$\text{the slope of } x^n \text{ is } n x^{n-1}$$

On
[How fast, right now?](tutorial:how-fast-right-now#the-derivative-is-a-limit),
the derivative $f'(a)$ was one number: the slope at one point $a$. The
power rule gives it at every point at once, so the derivative is itself
a rule. Put in an $x$, and a slope comes out. If $f(x) = x^4$, then
$f'(x) = 4x^3$. Finding the derivative of a rule is called
*differentiating*.

Two small cases come with it. A number in front stays in front: the
slope of $5x^3$ is $5 \times 3x^2 = 15x^2$, because making a curve 5
times as tall makes it 5 times as steep. And a number on its own, such
as 7, has slope 0: its graph is a flat line.

A table of five rows is a pattern, not a check. Here is a helper that
checks a slope rule against `derivative_at` at every point in a list.

```python exec
id: rules-for-power-2
def slopes_agree(rule, slope_rule, points):
    """Return True when slope_rule(x) and derivative_at(rule, x) agree at every x in points.

    derivative_at is an estimate, so agree means within 0.00001.
    Prints the first x where they disagree.
    """
    for x in points:
        if not close_enough(derivative_at(rule, x), slope_rule(x), tolerance=1e-5):
            print("they disagree at", x)
            return False
    return True

points = []
for step in range(-30, 31):
    points.append(step / 10)

def power_rule_for_fourth(x):
    return 4 * x ** 3

print(len(points), "points from", points[0], "to", points[-1])
print(slopes_agree(fourth_power, power_rule_for_fourth, points))
```

Sixty-one points, and the power rule agrees with the chord at every
one.

Does it work for powers that are not whole numbers? $\sqrt{x}$ is
$x^{1/2}$, and $\frac{1}{x}$ is $x^{-1}$, a negative power, as on
[Doubling and halving](tutorial:doubling-and-halving#halving-down-to-1).
The power rule would say their slopes are $\frac{1}{2}x^{-1/2}$ and
$-1 \times x^{-2}$. Both rules have trouble at 0 and below, so the
cell uses positive points only. Predict: will both agree?

```python exec
id: rules-for-power-3
import math

positive_points = []
for step in range(1, 51):
    positive_points.append(step / 10)

def one_over(x):
    return 1 / x

def root_slope(x):
    return 0.5 * x ** -0.5

def one_over_slope(x):
    return -1 * x ** -2

print(slopes_agree(math.sqrt, root_slope, positive_points))
print(slopes_agree(one_over, one_over_slope, positive_points))
```

Both agree. The power rule holds for any power $n$, not only whole
numbers. The minus sign in the slope of $\frac{1}{x}$ says it goes
downhill: the more friends share a prize, the less each gets.

## Adding rules: the sum rule

A car's stopping distance has two parts. While the driver sees the
danger and moves a foot to the brake, the car keeps going: the
thinking distance. Then the brakes slow it: the braking distance.
Here is a model with the shape of the Road Safety Authority's chart, in
metres, at a speed of $v$ km/h. The numbers are rounded and made up.

$$\text{stopping}(v) = 0.2v + 0.006v^2$$

At 50 km/h that is $10 + 15 = 25$ m. How much further does the car need
for each extra km/h? That is the slope of the stopping distance.

The *sum rule* says, in words: the slope of a sum is the sum of the
slopes. In symbols, if $h(x) = f(x) + g(x)$, then

$$h'(x) = f'(x) + g'(x)$$

So the slope is $0.2 + 0.012v$. Predict the slope at 100 km/h, then
run the check.

```python exec
id: rules-for-sum-1
def stopping(speed):
    """Return the stopping distance in metres at speed km/h: thinking plus braking."""
    return 0.2 * speed + 0.006 * speed ** 2

def stopping_slope(speed):
    return 0.2 + 0.012 * speed

speeds = list(range(0, 131, 5))
print(slopes_agree(stopping, stopping_slope, speeds))
print(stopping_slope(50), stopping_slope(100))
```

At 50 km/h, each extra km/h adds 0.8 m. At 100 km/h, it adds 1.4 m.
The faster you go, the more each extra km/h costs, because the braking
part grows with the square of the speed.

A polynomial is a sum of powers, and on
[Rules with letters in them](tutorial:rules-with-letters-in-them#terms-coefficients-and-a-list)
a polynomial was a list of coefficients, lowest power first. So the
power rule and the sum rule together are a loop over that list. The
coefficient of $x^k$ is multiplied by $k$, and moves down one place.
What list do you expect for $5 + 3x - 2x^2 + x^3$?

```python exec
id: rules-for-sum-2
def derivative_coefficients(coefficients):
    """Return the coefficients of the derivative of a polynomial.

    Both lists are lowest power first: [5, 3, -2, 1] is 5 + 3x - 2x² + x³.
    """
    result = []
    for power in range(1, len(coefficients)):
        result.append(power * coefficients[power])
    return result

cubic_rule = [5, 3, -2, 1]
cubic_slope = derivative_coefficients(cubic_rule)
print(cubic_slope)

def cubic(x):
    return evaluate(cubic_rule, x)

def cubic_slope_rule(x):
    return evaluate(cubic_slope, x)

print(slopes_agree(cubic, cubic_slope_rule, points))
```

The list is `[3, -4, 3]`, which is $3 - 4x + 3x^2$. The number 5 has
gone: a number on its own has slope 0. The check agrees at all 61
points.

## Multiplying rules: the product rule

A coffee cart sells 200 cups a week at €2.50 a cup. Each week the
owner raises the price by 10 cent, and sells 5 fewer cups. After $t$
weeks the price is $2.5 + 0.1t$, the number sold is $200 - 5t$, and the
takings are the price times the number. Are the takings going up or
down, and how fast?

The takings are the area of a rectangle, with the price along one side
and the number sold along the other. When both sides change a little,
the area changes in three pieces: a strip along one side, a strip
along the other, and a tiny corner where both changes meet. For a very
small change, the corner is so small that it disappears. What is left
is the two strips.

That gives the *product rule*. In words: the first times the slope of the
second, plus the second times the slope of the first. In symbols, if
$h(x) = f(x) \times g(x)$, then

$$h'(x) = f(x)\,g'(x) + g(x)\,f'(x)$$

Many people's first guess is "the slope of a product is the product of
the slopes". The cell tries both. Which do you think will agree with
`derivative_at`?

```python exec
id: rules-for-product-1
def price(week):
    return 2.5 + 0.1 * week

def cups(week):
    return 200 - 5 * week

def takings(week):
    return price(week) * cups(week)

def product_rule_slope(week):
    return price(week) * -5 + cups(week) * 0.1

def slopes_multiplied(week):
    return 0.1 * -5

weeks = list(range(0, 21))
print("product rule:", slopes_agree(takings, product_rule_slope, weeks))
print("slopes multiplied:", slopes_agree(takings, slopes_multiplied, weeks))
print(product_rule_slope(0), product_rule_slope(10))
```

The product rule agrees in every week. Multiplying the slopes gives
$-0.5$ every week, and disagrees at week 0. At the start, the takings
grow by €7.50 a week. By week 10 they fall by €2.50 a week: the lost
cups now cost more than the higher price brings in.

Is multiplying slopes a foolish move, then? Do not throw it away yet. It is
the right move in a different space, two sections from here.

## Dividing rules: the quotient rule

A café buys a coffee machine for €600, and each cup costs €0.30 in
beans and milk. After $n$ cups, the average cost of a cup is the total
cost divided by the number of cups:

$$\text{average}(n) = \frac{600 + 0.3n}{n}$$

The average falls as more cups are made. How fast?

The *quotient rule* gives the slope of one rule divided by another. In
words: the bottom times the slope of the top, minus the top times the
slope of the bottom, all over the bottom squared. In symbols, if
$h(x) = \frac{f(x)}{g(x)}$, then

$$h'(x) = \frac{g(x)\,f'(x) - f(x)\,g'(x)}{g(x)^2}$$

The order matters, because of the minus sign. The bottom can never be
0, since a division by 0 has no value.

For the café, the top is $600 + 0.3n$, with slope 0.3, and the bottom
is $n$, with slope 1. So the slope of the average is

$$\frac{n \times 0.3 - (600 + 0.3n) \times 1}{n^2} = \frac{-600}{n^2}$$

Predict the sign of the slope before you run it.

```python exec
id: rules-for-quotient-1
def average_cost(cups_made):
    """Return the average cost of a cup, in euro, after cups_made cups."""
    return (600 + 0.3 * cups_made) / cups_made

def quotient_rule_slope(cups_made):
    top = 600 + 0.3 * cups_made
    bottom = cups_made
    return (bottom * 0.3 - top * 1) / bottom ** 2

cup_counts = list(range(100, 5001, 100))
print(slopes_agree(average_cost, quotient_rule_slope, cup_counts))
print(average_cost(1000), quotient_rule_slope(1000))
```

After 1,000 cups the average cost is €0.90, and it is falling by
0.0006 of a euro with each extra cup. The slope is negative, and it
gets closer to 0 as $n$ grows: the machine's €600 is shared among more
and more cups, and each extra cup changes the share less.

There is another way. The average is $600 \times n^{-1} + 0.3$, and the
power rule and the sum rule give $-600n^{-2}$ in one step. Two routes,
one answer. The quotient rule is the one that works when the bottom is
not a single power, as in $\frac{x}{x^2 + 1}$.

## A rule inside a rule: the chain rule

A stone drops into a still pond. The ripple's radius grows by 0.5
metres every second. After $t$ seconds, the radius is $0.5t$, and the
area inside the ripple is $\pi r^2$, which is `circle_area` from
[Measuring rooms and tins](tutorial:measuring-rooms-and-tins#tools-for-flat-shapes).
So the area after $t$ seconds is one rule inside another:
`compose(circle_area, ripple_radius)`.

How fast is the area growing? Think of the rates, with their units:

- the area grows by $2\pi r$ square metres for each metre of radius
  (the power rule on $\pi r^2$)
- the radius grows by 0.5 metres for each second

Metres cancel, and square metres per second are left: $2\pi r \times
0.5$. The rates multiply.

That is the *chain rule*. In words: the slope of the outside rule,
worked out at the inside value, times the slope of the inside rule. In
symbols, if $h(x) = f(g(x))$, then

$$h'(x) = f'(g(x)) \times g'(x)$$

After 6 seconds, the radius is 3 m. Predict the growth of the area, in
square metres per second, then run it.

```python exec
id: rules-for-chain-1
def ripple_radius(seconds):
    return 0.5 * seconds

ripple_area = compose(circle_area, ripple_radius)

def chain_rule_slope(seconds):
    radius = ripple_radius(seconds)
    return 2 * math.pi * radius * 0.5

times = list(range(0, 21))
print(slopes_agree(ripple_area, chain_rule_slope, times))
print(chain_rule_slope(6), 3 * math.pi)
```

About 9.42 square metres a second, which is $3\pi$. The chain rule
agrees at every second.

Here is the space where multiplying slopes is right. For a product,
two rules sit side by side, and multiplying their slopes fails. For a
rule inside a rule, one rule's output is the other's input, and the
slopes multiply.

One more check, on a rule with no story: $(2x + 1)^3$. The outside rule
is "cube it", with slope $3u^2$, and the inside is $2x + 1$, with slope
2. What does the chain rule give?

```python exec
id: rules-for-chain-2
def inside(x):
    return 2 * x + 1

def bracket_cubed(x):
    return inside(x) ** 3

def bracket_cubed_slope(x):
    return 3 * inside(x) ** 2 * 2

print(slopes_agree(bracket_cubed, bracket_cubed_slope, points))
```

It agrees: the slope of $(2x + 1)^3$ is $6(2x + 1)^2$.

### Your turn

1. Say in words what the chain rule gives for $(5x - 3)^4$, then write
   its slope rule.
2. Check it with `slopes_agree` over `points`.
3. Find the slope of $x^2(2x + 1)^3$. You need the product rule and
   the chain rule together. Check it too.

```python exec
id: rules-for-chain-your-turn
# Your slope rules, and the checks
```

## Back to the top of the curve

On [The top of the curve](tutorial:the-top-of-the-curve#a-price-too-low-a-price-too-high),
Aoife's profit at a price of $p$ euro was $-20p^2 + 140p - 120$, and its
top was at €3.50. That page found it by completing the square, and it
made a promise: Unit 9 would come back to this curve with the idea of a
slope at a point.

At the top of a curve, the curve is neither going up nor going down.
Its
[tangent line](tutorial:how-fast-right-now#the-tangent-line) is flat,
so the slope there is 0. By the power rule and the
sum rule, the slope of the profit is $-40p + 140$. Where is that 0?
That is a linear equation, and your toolkit's `solve_linear` from
[Solving for x](tutorial:solving-for-x#a-tool-for-any-straight-line-equation)
solves it. Predict the answer.

```python exec
id: rules-for-top-1
profit_rule = [-120, 140, -20]
profit_slope = derivative_coefficients(profit_rule)
print(profit_slope)

best_price = solve_linear(profit_slope[1], profit_slope[0])
print(best_price, evaluate(profit_rule, best_price))
print(vertex(-20, 140, -120))
```

The slope is $140 - 40p$, it is 0 at €3.50, and the profit there is
€125. It is the same answer as `vertex` gives, found by a new route.

This works for every quadratic. The slope of $ax^2 + bx + c$ is
$2ax + b$, and that is 0 when $x = -\frac{b}{2a}$: the formula from
Unit 7, found again. The difference is what comes next. Completing the
square only works on a quadratic. A slope of 0 finds the tops and
bottoms of any curve whose slope we can work out, and the four rules on
this page can work out a great many.

### Your turn

A box with no lid is made from a square of card 30 cm across, by
cutting a square of side $x$ from each corner and folding up the sides.
Its volume is $x(30 - 2x)^2$.

1. Use the product rule and the chain rule to find the slope of the
   volume.
2. Check your slope rule with `slopes_agree`, for $x$ from 0 to 15.
3. The slope works out to $(30 - 2x)(30 - 6x)$. Where is it 0? Which
   of those answers gives the biggest box?

```python exec
id: rules-for-top-your-turn
# The box with no lid
```

<details class="dl-why"><summary>Why this way?</summary>

This page found the power rule in a table, and checked every rule
against `derivative_at` at many points. It did not prove any of them.

Most calculus courses prove each rule from the definition of the
derivative, using limits and algebra. Proof is what makes a rule
certain, rather than very likely. A proof also shows why the corner of the
rectangle disappears, which this page said only in words.

We checked instead of proving because a check is something you can
run, change and break, and every rule came with a picture or a story
first. The cost is that 61 points agreeing is strong evidence, not
certainty. For proofs from limits, see the page linked at the end.

</details>

## Four questions, looking back

| The question | On this page |
|---|---|
| What is named here? | $f'(x)$, the derivative of $f(x)$; the inside and outside rules of a composition; a polynomial's slope as a new list |
| What is promised? | each rule promises a slope at every $x$; `slopes_agree` promises only that 61 points agree, which checks the promise but does not prove it |
| What happens when? | the chain rule works out the inside rule first, then the outside rule's slope at that value; a slope of 0 is found before the top |
| What does this space let us do? | the quotient rule needs a bottom that is not 0; multiplying slopes fails for a product and is right for a rule inside a rule |

## What we have now

| Term or tool | What it means |
|---|---|
| derivative, $f'(x)$ | the rule that gives the slope of $f$ at every $x$ |
| differentiating | finding a derivative |
| power rule | the slope of $x^n$ is $n x^{n-1}$, for any power $n$ |
| a number in front, a number alone | the slope of $5x^3$ is $15x^2$; the slope of 7 is 0 |
| sum rule | the slope of $f + g$ is $f' + g'$ |
| product rule | the slope of $f \times g$ is $f g' + g f'$ |
| quotient rule | the slope of $\frac{f}{g}$ is $\frac{g f' - f g'}{g^2}$ |
| chain rule | the slope of $f(g(x))$ is $f'(g(x)) \times g'(x)$ |
| slope 0 at a top or bottom | where the tangent is flat, a curve can turn |

The practice page is next. Then
[Solving by computing](tutorial:solving-by-computing) uses slopes to
find roots that no formula gives.

## Where to read more

The dewlab page
[Derivatives: the rate of change of a curve](tutorial:rates-of-change)
meets the same rules from another direction, with a first look at why
they hold.
