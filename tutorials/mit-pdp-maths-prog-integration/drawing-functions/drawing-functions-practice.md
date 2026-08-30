---
title: "Drawing Functions — Practice"
slug: drawing-functions-practice
practice_for: drawing-functions
module: mit-pdp-maths-prog-integration
module_title: "Programming and Maths, Integrated"
year: "2026-2027"
series: maths-and-programming
version: 2026.08.23.1
---

# Drawing Functions — Practice

Answers are folded. Several of these ask you to predict before plotting — the prediction is the exercise, and the plot is the marking.

## Tools

```python exec
id: tools-1
import matplotlib.pyplot as plt

def draw(f, low=-5, high=5, steps=300, label=None, ax=None):
    xs = [low + (high - low) * i / steps for i in range(steps + 1)]
    if ax is None:
        fig, ax = plt.subplots(figsize=(7, 4.5))
        ax.axhline(0, color="black", linewidth=0.8)
        ax.axvline(0, color="black", linewidth=0.8)
        ax.grid(alpha=0.3)
    ax.plot(xs, [f(x) for x in xs], label=label)
    if label:
        ax.legend(fontsize=8)
    return ax


draw(lambda x: x ** 2, label="x^2")
```

## Is It a Function?

**1.** Which of these are functions in the mathematical sense?

- (a) `def f(x): return x * 3 + 1`
- (b) `def g(x): return random.randint(1, 6)`
- (c) A rule that takes a person and gives their date of birth
- (d) A rule that takes a date and gives the people born on it

<details class="dl-answer"><summary>answer</summary>

(a) and (c) are functions. Each input gives exactly one output, every time.

(b) is not — the same input gives different answers.

(d) is not a function to a *person*, because a date has many people. It is a perfectly good function to a *set* of people, which is the usual fix: change what the output is allowed to be.

</details>

**2.** What is the domain of each?

- (a) `f(x) = 1/(x - 3)`
- (b) `g(x) = sqrt(x + 4)`
- (c) `h(x) = x**2`
- (d) `k(x) = 1/sqrt(x)`

<details class="dl-answer"><summary>answer</summary>

(a) Everything except 3. (b) Everything from −4 upwards. (c) Everything. (d) Everything strictly above 0 — zero is excluded because you cannot divide by the square root of zero.

</details>

**3.** A function has domain "all real numbers" and range "everything from 2 upwards". Sketch something it could be.

<details class="dl-answer"><summary>answer</summary>

Anything with a minimum of 2 and no maximum. `x² + 2` is the obvious one. So is `|x| + 2`.

</details>

## Lines

**4.** For each, say the slope and where it crosses the vertical axis, then predict which is steepest.

- (a) `y = 3x - 2`
- (b) `y = -5x + 1`
- (c) `y = 0.5x + 4`

<details class="dl-answer"><summary>answer</summary>

(a) slope 3, crosses at −2. (b) slope −5, crosses at 1. (c) slope 0.5, crosses at 4.

(b) is steepest. Steepness is about the size of the slope, not its sign — a slope of −5 is steeper than one of 3, it just goes the other way.

</details>

**5.** Which of these pass through the origin?

`y = 2x`, `y = 2x + 1`, `y = -7x`, `y = 4`

<details class="dl-answer"><summary>answer</summary>

The first and third. A line passes through the origin exactly when its intercept is zero.

`y = 4` is horizontal at height 4 and never comes near it.

</details>

**6.** Plot `y = 2x + 1` and `y = -x + 7` on one pair of axes and read off where they cross. Then check by solving.

<details class="dl-answer"><summary>answer</summary>

They cross at `(2, 5)`.

By algebra: `2x + 1 = −x + 7`, so `3x = 6` and `x = 2`, and then `y = 5`.

The two methods agreeing is the point — the picture is trustworthy, so it can be used where the algebra is harder.

</details>

## Curves

**7.** Before plotting: how many times does each cross the horizontal axis?

- (a) `y = x**2 - 4`
- (b) `y = x**2 + 4`
- (c) `y = x**3 - x`
- (d) `y = x**3`

<details class="dl-answer"><summary>answer</summary>

(a) Twice, at −2 and 2. (b) Never — it sits entirely above the axis. (c) Three times, at −1, 0 and 1. (d) Once, at 0.

</details>

**8.** What is the most times a cubic can cross the axis? And a quartic (`x⁴`)?

<details class="dl-answer"><summary>answer</summary>

Three and four. In general, a polynomial of degree n crosses at most n times, because it has at most n roots.

It can cross fewer times — `x³` crosses once and `x² + 4` not at all — but never more.

</details>

**9.** Plot `y = x**2`, `y = 3*x**2` and `y = 0.2*x**2` together. What does the coefficient do, and what does it not do?

<details class="dl-answer"><summary>answer</summary>

It stretches the curve vertically — bigger means narrower-looking.

What it does not do is move the curve. All three still have their lowest point at the origin, and all three still cross the axis exactly once, at zero.

</details>

**10.** Plot `y = x**3` and `y = -x**3`. Describe the difference in one sentence.

<details class="dl-answer"><summary>answer</summary>

The second is the first flipped upside down — a reflection in the horizontal axis.

`x³` climbs from bottom left to top right; `−x³` falls from top left to bottom right.

</details>

## Reading Answers Off the Picture

**11.** Plot `y = x**2 - 3*x - 4` and read off its roots. Then check with the quadratic formula.

<details class="dl-answer"><summary>answer</summary>

It crosses at −1 and 4.

By formula: discriminant is 9 + 16 = 25, so the roots are (3 ± 5)/2, which is 4 and −1.

</details>

**12.** Solve `x**3 - 2*x = 1` from a picture, to one decimal place.

<details class="dl-answer"><summary>answer</summary>

Plot `y = x³ − 2x` and the horizontal line `y = 1`, and read off the crossings: roughly −1.0, −0.6 and 1.6.

More precisely: −1, −0.618 and 1.618. The exact answers involve the golden ratio, and there is no straightforward algebraic route to them — which is the argument for the picture.

</details>

**13.** Where do `y = x**2` and `y = x + 2` cross? Read it off, then verify.

<details class="dl-answer"><summary>answer</summary>

At `(-1, 1)` and `(2, 4)`.

Setting them equal: `x² = x + 2`, so `x² − x − 2 = 0`, which factorises as `(x − 2)(x + 1)`.

</details>

**14.** A projectile's height in metres after `t` seconds is `h = 20t - 4.9t**2`. Plot it and answer: when does it land, and how high does it get?

<details class="dl-answer"><summary>answer</summary>

It lands when the height returns to zero, at about t = 4.08 seconds. (Setting `20t − 4.9t² = 0` gives `t(20 − 4.9t) = 0`, so t = 0 or t = 20/4.9.)

The highest point is halfway between the two roots, at t ≈ 2.04, where the height is about 20.4 m.

The curve is symmetric about its peak, which is why halfway between the roots is the right place to look.

</details>

## Inverses

**15.** What is the inverse of each?

- (a) `f(x) = x + 7`
- (b) `f(x) = 5x`
- (c) `f(x) = 3x - 2`
- (d) `f(x) = x**3`

<details class="dl-answer"><summary>answer</summary>

(a) `x − 7`. (b) `x/5`. (c) `(x + 2)/3`. (d) the cube root, `x**(1/3)`.

Each one undoes the operations in reverse order, which is the same unwrapping as in *Rearranging Formulae*.

</details>

**16.** Check one of your answers by round-tripping several values through both.

<details class="dl-answer"><summary>answer</summary>

```python
f = lambda x: 3 * x - 2
g = lambda x: (x + 2) / 3
print(all(abs(g(f(x)) - x) < 1e-9 for x in [-10, 0, 1.5, 7, 100]))
```

Both directions are worth checking: `f(g(x))` should also come back to x.

</details>

**17.** Why does `x**2` have no inverse over all the numbers, while `x**3` does?

<details class="dl-answer"><summary>answer</summary>

Because 3 and −3 both square to 9, so the inverse of 9 has two candidates and a function may only give one.

Cubing does not collide: no two different numbers have the same cube, because the sign survives. So the cube root is a function everywhere.

The usual fix for squaring is to restrict the domain to non-negative numbers, which is exactly what `math.sqrt` does by returning only the positive root.

</details>

**18.** Plot `y = 2x + 1`, its inverse, and `y = x` on one pair of axes. What do you notice?

<details class="dl-answer"><summary>answer</summary>

The inverse is `(x − 1)/2`, and the two curves are mirror images in the line `y = x`.

That is what inverting does geometrically: swapping the inputs and outputs swaps the axes, which reflects everything across the diagonal.

</details>

## One Longer One

**19.** A shop's profit on selling `n` items is `P(n) = -0.5*n**2 + 30*n - 200` euro.

- (a) Plot it for n from 0 to 60.
- (b) How many items must they sell to break even?
- (c) How many items gives the most profit, and how much is it?
- (d) What happens beyond about 52 items, and does that make sense?

<details class="dl-answer"><summary>answer</summary>

(b) Break-even is where the curve crosses zero: at about n = 7.6 and n = 52.4. Since items are whole, they need 8 to move into profit.

(c) The peak is halfway between the roots, at n = 30, where the profit is €250.

(d) Past 52 the model says profit goes negative and keeps falling. That is the model rather than the shop — a quadratic falls forever, and a real business would not keep making items at a loss. **A model is trustworthy over the range it was built for and not beyond it**, which is worth knowing before you extrapolate anything.

</details>
