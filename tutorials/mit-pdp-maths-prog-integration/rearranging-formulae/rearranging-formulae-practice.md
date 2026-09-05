---
title: "Rearranging Formulae — Practice"
slug: rearranging-formulae-practice
practice_for: rearranging-formulae
module: mit-pdp-maths-prog-integration
module_title: "Programming and Maths, Integrated"
year: "2026-2027"
series: algebra-and-functions
version: 2026.08.23.1
---

# Rearranging Formulae — Practice

Answers are folded. Rearrange by hand first — the checking cell will tell you whether you got it right, but only after you have committed to something.

## Tools

```python exec
id: tools-1
import random

def check(original, rearranged, ranges, tries=200):
    """Feed random values to both and see whether they ever disagree.

    `original` takes the named values and returns the subject; `rearranged`
    takes the subject plus the others and should give back the missing one.
    """
    for _ in range(tries):
        values = {name: random.uniform(low, high) for name, (low, high) in ranges.items()}
        subject = original(**values)
        wanted = list(ranges)[-1]
        recovered = rearranged(subject, **{k: v for k, v in values.items() if k != wanted})
        if abs(recovered - values[wanted]) > 1e-9:
            return f"Disagree: expected {values[wanted]}, got {recovered}"
    return f"Agreed on all {tries} tries."


print(check(lambda u, a, t: u + a * t,
            lambda v, u, a: (v - u) / a,
            {"u": (1, 100), "a": (1, 100), "t": (1, 100)}))
```

## The Moves

**1.** Make `P` the subject of `I = PRT/100`.

<details class="dl-answer"><summary>answer</summary>

`P = 100I/(RT)`.

Multiply both sides by 100, then divide by R and by T.

</details>

**2.** Make `C` the subject of `F = 9C/5 + 32`.

<details class="dl-answer"><summary>answer</summary>

`C = 5(F − 32)/9`.

Subtract 32 first, because it is the outermost operation, then undo the multiplication.

</details>

**3.** Make `h` the subject of `A = (a + b)h/2`.

<details class="dl-answer"><summary>answer</summary>

`h = 2A/(a + b)`.

</details>

**4.** Make `r` the subject of `A = πr²`.

<details class="dl-answer"><summary>answer</summary>

`r = √(A/π)`.

Divide by π, then take the square root. Strictly there is a ± — but a radius is a length, so the negative answer is discarded. That is a decision about the situation, not about the algebra.

</details>

**5.** Make `t` the subject of `s = ut + ½at²`, given that `u = 0`.

<details class="dl-answer"><summary>answer</summary>

With u = 0 it is `s = ½at²`, so `t = √(2s/a)`.

With u not zero it is a quadratic in t and needs the formula — which is worth noticing, because whether a rearrangement is easy often depends on what else you know.

</details>

**6.** Why does unwrapping go outside in, when evaluating goes inside out?

<details class="dl-answer"><summary>answer</summary>

To evaluate `u + at` you multiply first and add last. To undo it you have to remove the last thing that was done first — so subtract, then divide.

It is the same order you would take off a coat and a jumper: last on, first off.

</details>

## Unknowns Underneath

**7.** Make `R` the subject of `1/R = 1/a + 1/b`.

<details class="dl-answer"><summary>answer</summary>

`R = 1/(1/a + 1/b)`, or equivalently `R = ab/(a + b)`.

Find `1/R` first, then flip. The second form comes from putting the right-hand side over a common denominator.

</details>

**8.** Two resistors of 10 Ω in parallel — what is the combined resistance? And 100 Ω beside 1 Ω?

<details class="dl-answer"><summary>answer</summary>

5 Ω, and about 0.99 Ω.

Two equal resistors give exactly half of one. A large one beside a small one gives slightly *less* than the small one — the 100 barely matters, because current goes the easy way.

Both of those are readable off `R = ab/(a+b)` and neither is obvious from `1/R = 1/a + 1/b`. That is what rearranging is for.

</details>

**9.** Make `u` the subject of the lens formula `1/f = 1/u + 1/v`.

<details class="dl-answer"><summary>answer</summary>

`1/u = 1/f − 1/v`, so `u = 1/(1/f − 1/v)`, or `u = fv/(v − f)`.

Get the reciprocal of what you want on its own, then flip. The second form makes something visible: when `v = f` the bottom is zero and there is no answer, which physically means the object is infinitely far away.

</details>

**10.** In `R = ab/(a + b)`, what happens when `b = 0`, and what does that mean?

<details class="dl-answer"><summary>answer</summary>

`R = 0`. A resistance of zero is a plain wire, and a wire beside a resistor carries all the current — so the pair has no resistance worth speaking of.

Notice the original form `1/R = 1/a + 1/b` fails outright at b = 0, because `1/0` is undefined. The rearranged form gives a sensible answer. **The two forms are equivalent everywhere they are both defined, and one of them is defined in more places.**

</details>

**11.** Make `x` the subject of `y = (x + 1)/(x − 1)`.

<details class="dl-answer"><summary>answer</summary>

Multiply out: `y(x − 1) = x + 1`, so `yx − y = x + 1`.

Collect the x terms: `yx − x = y + 1`, so `x(y − 1) = y + 1`, so `x = (y + 1)/(y − 1)`.

The rearrangement is its own inverse, which is a pleasant surprise and worth checking.

</details>

## Checking

**12.** Write a check for your answer to question 2, and then deliberately break it to make sure the check catches the break.

<details class="dl-answer"><summary>answer</summary>

```python
def to_fahrenheit(c):
    return 9 * c / 5 + 32

def to_celsius(f):
    return 5 * (f - 32) / 9

print(all(abs(to_celsius(to_fahrenheit(c)) - c) < 1e-9
          for c in [-40, 0, 20, 37, 100]))

# Now break it:
def broken(f):
    return 5 * (f + 32) / 9
print(all(abs(broken(to_fahrenheit(c)) - c) < 1e-9 for c in [-40, 0, 20, 37, 100]))
```

The first prints True and the second False. **A test that has never failed has not been tested.**

</details>

**13.** Why is `abs(a - b) < 1e-9` better than `a == b` when checking a rearrangement?

<details class="dl-answer"><summary>answer</summary>

Because these are floating-point numbers, and two calculations that should agree exactly can differ in the last decimal place.

`0.1 + 0.2 == 0.3` is False in Python, and that is not a bug. Asking "are these equal?" of two floats is nearly always the wrong question; "are these closer than I care about?" is the right one.

</details>

**14.** Does agreeing on 200 random values prove a rearrangement is correct?

<details class="dl-answer"><summary>answer</summary>

No. It is strong evidence and not a proof — the same distinction as in *Logic and Truth*, where four rows *were* a proof because there were only four cases.

Here the space of inputs is infinite, so a check can only fail to find a problem. In practice it finds every mistake you are likely to make, which is worth a great deal even though it is not certainty.

</details>

## In Use

**15.** The formula for compound interest is `A = P(1 + r)ⁿ`. Make `P` the subject, and then make `r` the subject.

<details class="dl-answer"><summary>answer</summary>

`P = A/(1 + r)ⁿ`.

For r: `(1 + r)ⁿ = A/P`, so `1 + r = (A/P)^(1/n)`, so `r = (A/P)^(1/n) − 1`.

The second one needs an nth root, which is a fractional power — the same move as taking a square root, generalised.

</details>

**16.** You want €10,000 in 8 years and the rate is 3%. How much do you need to invest now?

<details class="dl-answer"><summary>answer</summary>

`P = 10000/(1.03)⁸ ≈ €7,894.09`.

</details>

**17.** Bandwidth, file size and time are related by `time = size/rate`. Make `rate` the subject, and work out what rate you need to move 4 GB in 90 seconds.

<details class="dl-answer"><summary>answer</summary>

`rate = size/time`, so `4 GB / 90 s ≈ 0.0444 GB/s`, which is about 45.5 MB/s or roughly 364 Mbit/s.

Watching the units is most of the work in this kind of question — bytes and bits differ by a factor of eight and the mistake is very common.

</details>

**18.** The formula for the period of a pendulum is `T = 2π√(L/g)`. Make `L` the subject, then find the length that gives a period of exactly one second, with g = 9.81.

<details class="dl-answer"><summary>answer</summary>

`T/(2π) = √(L/g)`, so `T²/(4π²) = L/g`, so `L = gT²/(4π²)`.

With T = 1 and g = 9.81: `L ≈ 0.2485 m`, about 25 cm.

A pendulum with a two-second period — one second each way — is about a metre, which is why grandfather clocks are the height they are.

</details>
