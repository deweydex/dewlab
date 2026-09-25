---
title: "Rearranging formulae: changing the subject — Practice"
practice_for: rearranging-formulae
year: "2026-2027"
version: 2026.09.25.1
---

# Rearranging formulae: changing the subject — Practice

The answers are hidden in folds under each problem. Try each
rearrangement by hand first, and write your answer down. The checking
cell below can then tell you whether it is right.

## Tools

This cell holds a function called `do_they_agree`. It feeds random
numbers to the original formula and to your rearrangement, and tells
you whether they ever disagree. The example at the bottom checks $t = \frac{v - u}{a}$.

```python exec
id: tools-1
import random

def do_they_agree(original, rearranged, ranges, tries=200):
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


print(do_they_agree(lambda u, a, t: u + a * t,
            lambda v, u, a: (v - u) / a,
            {"u": (1, 100), "a": (1, 100), "t": (1, 100)}))
```

## The moves

**1.** Make $P$ the subject of $I = \frac{PRT}{100}$.

<details class="dl-answer"><summary>answer</summary>

$P = \frac{100I}{RT}$.

Multiply both sides by 100. Then divide both sides by $R$ and by $T$.

</details>

**2.** Make $C$ the subject of $F = \frac{9C}{5} + 32$.

<details class="dl-answer"><summary>answer</summary>

$C = \frac{5(F - 32)}{9}$.

Subtract 32 first, because adding 32 was the last operation done (the
outermost one). Then undo the multiplication by $\frac{9}{5}$: multiply
by 5 and divide by 9.

</details>

**3.** Make $h$ the subject of $A = \frac{(a + b)h}{2}$.

<details class="dl-answer"><summary>answer</summary>

$h = \frac{2A}{a + b}$.

Multiply both sides by 2, then divide both sides by $(a + b)$.

</details>

**4.** Make $r$ the subject of $A = \pi r^2$.

<details class="dl-answer"><summary>answer</summary>

$r = \sqrt{\frac{A}{\pi}}$.

Divide by $\pi$, then take the square root. Strictly, the square root
gives $\pm$, a positive and a negative answer. But a radius is a length,
so we drop the negative answer. That is a decision about the situation,
not about the algebra.

</details>

**5.** Make $t$ the subject of $s = ut + \frac{1}{2}at^2$, when $u = 0$.

<details class="dl-answer"><summary>answer</summary>

With $u = 0$ the formula is $s = \frac{1}{2}at^2$, so $t = \sqrt{\frac{2s}{a}}$.

When $u$ is not zero, the formula is a quadratic in $t$, and you need
the quadratic formula from
[Solving equations: linear, quadratic and simultaneous](tutorial:cracking-equations).
This is worth noticing: whether a rearrangement is easy often depends on
what else you know.

</details>

**6.** Why does undoing go from the outside in, when evaluating goes
from the inside out?

<details class="dl-answer"><summary>answer</summary>

To evaluate $u + at$, you multiply first and add last. To undo it, you
must first remove the last thing that was done. So you subtract first,
then divide.

It is the same order as taking off a coat and a jumper: the last thing
you put on is the first thing you take off.

</details>

## Unknowns underneath

**7.** Make $R$ the subject of $\frac{1}{R} = \frac{1}{a} + \frac{1}{b}$.

<details class="dl-answer"><summary>answer</summary>

$R = \frac{1}{\frac{1}{a} + \frac{1}{b}}$. Another way to write the same
thing is $R = \frac{ab}{a + b}$.

Find $\frac{1}{R}$ first, then flip it. The second form comes from
putting the right-hand side over a common denominator:
$\frac{1}{a} + \frac{1}{b} = \frac{b + a}{ab}$.

</details>

**8.** What is the combined resistance of two 10 Ω resistors in
parallel? And of 100 Ω beside 1 Ω?

<details class="dl-answer"><summary>answer</summary>

5 Ω, and about 0.99 Ω.

Two equal resistors give exactly half the resistance of one. A large one
beside a small one gives a little *less* than the small one. The 100
hardly matters, because the current takes the easy path.

Both facts are easy to read from $R = \frac{ab}{a + b}$, and neither is
easy to see in $\frac{1}{R} = \frac{1}{a} + \frac{1}{b}$. That is what
rearranging is for.

</details>

**9.** Make $u$ the subject of the lens formula
$\frac{1}{f} = \frac{1}{u} + \frac{1}{v}$.

<details class="dl-answer"><summary>answer</summary>

$\frac{1}{u} = \frac{1}{f} - \frac{1}{v}$, so
$u = \frac{1}{\frac{1}{f} - \frac{1}{v}}$, which is the same as
$u = \frac{fv}{v - f}$.

Get the reciprocal of the letter you want on its own, then flip it. The
second form shows something new. When $v = f$, the bottom is zero and
there is no answer. In physics, this means the object is infinitely far
away.

</details>

**10.** In $R = \frac{ab}{a + b}$, what happens when $b = 0$? What does
that mean?

<details class="dl-answer"><summary>answer</summary>

$R = 0$. A resistance of zero is a perfect wire. Put a perfect wire
beside a resistor, and all the current takes the wire, so the pair has
no resistance at all. (A real wire has a tiny resistance, so a real
pair has almost none.)

Notice that the original form, $\frac{1}{R} = \frac{1}{a} + \frac{1}{b}$,
fails completely at $b = 0$, because $\frac{1}{0}$ is undefined. The
rearranged form gives a sensible answer. **The two forms agree
everywhere they both work, and one of them works in more places.**

</details>

**11.** Make $x$ the subject of $y = \frac{x + 1}{x - 1}$.

<details class="dl-answer"><summary>answer</summary>

1. Multiply both sides by $(x - 1)$: $y(x - 1) = x + 1$, so
   $yx - y = x + 1$.
2. Collect the $x$ terms on one side: $yx - x = y + 1$.
3. Take out $x$ as a common factor: $x(y - 1) = y + 1$.
4. Divide by $(y - 1)$: $x = \frac{y + 1}{y - 1}$.

The answer has the same shape as the question, with $x$ and $y$ swapped.
That is a nice surprise, and worth checking with a number: $x = 3$ gives
$y = \frac{4}{2} = 2$, and $y = 2$ gives $x = \frac{3}{1} = 3$.

</details>

## Checking

**12.** Can you write a check for your answer to question 2? Then break
your answer on purpose, to make sure the check catches the mistake.

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

The first prints True and the second prints False. **A test that has
never failed has not really been tested.**

</details>

**13.** Why is `abs(a - b) < 1e-9` better than `a == b` when you check
a rearrangement?

<details class="dl-answer"><summary>answer</summary>

Because these are floats. Two calculations that should agree exactly can
differ in the last decimal place.

In Python, `0.1 + 0.2 == 0.3` is False, and that is not a bug. With
floats, "are these equal?" is nearly always the wrong question. The
right one is "are these closer together than I care about?"

</details>

**14.** If a rearrangement agrees with the original on 200 random
values, does that prove it is correct?

<details class="dl-answer"><summary>answer</summary>

No. It is strong evidence, but it is not a proof. Compare
[Logic: truth tables, XOR and De Morgan's laws](tutorial:logic-and-truth).
There, checking four rows *was* a proof, because there were only four
cases.

Here there are infinitely many possible inputs. So a check can only fail
to find a problem. In practice, it finds every mistake you are likely to
make. That is very useful, even though it is not certainty.

</details>

## In use

**15.** The formula for compound interest is $A = P(1 + r)^n$. Make $P$
the subject. Then make $r$ the subject.

<details class="dl-answer"><summary>answer</summary>

$P = \frac{A}{(1 + r)^n}$.

For $r$: $(1 + r)^n = \frac{A}{P}$, so $1 + r = \left(\frac{A}{P}\right)^{1/n}$,
so $r = \left(\frac{A}{P}\right)^{1/n} - 1$.

The second one needs an $n$th root, which is a fractional power. It is
the same move as taking a square root, for any $n$.

</details>

**16.** You want €10,000 in 8 years, and the interest rate is 3% a year.
How much do you need to invest now?

<details class="dl-answer"><summary>answer</summary>

$P = \frac{10000}{1.03^8} \approx$ €7,894.09.

</details>

**17.** Download time, file size and rate are related by
$\text{time} = \frac{\text{size}}{\text{rate}}$. Make rate the subject.
What rate do you need to move 4 GB in 90 seconds?

<details class="dl-answer"><summary>answer</summary>

$\text{rate} = \frac{\text{size}}{\text{time}}$. So the rate is
$\frac{4 \text{ GB}}{90 \text{ s}} \approx 0.0444$ GB/s. That is about
44.4 MB/s, or about 356 Mbit/s, since there are 8 bits in a byte. (If
you count a GB as 1024 MB, the answer is about 45.5 MB/s, or 364
Mbit/s.)

Watching the units is most of the work in a question like this. Bytes
and bits differ by a factor of eight, and mixing them up is a very
common mistake.

</details>

**18.** The period of a pendulum (the time for one full swing, there and
back) is $T = 2\pi\sqrt{\frac{L}{g}}$. Make $L$ the subject. Then find
the length that gives a period of exactly one second, with $g = 9.81$.

<details class="dl-answer"><summary>answer</summary>

1. Divide by $2\pi$: $\frac{T}{2\pi} = \sqrt{\frac{L}{g}}$.
2. Square both sides: $\frac{T^2}{4\pi^2} = \frac{L}{g}$.
3. Multiply by $g$: $L = \frac{gT^2}{4\pi^2}$.

With $T = 1$ and $g = 9.81$: $L \approx 0.2485$ m, about 25 cm.

A pendulum with a period of two seconds (one second each way) is about
a metre long. That is why grandfather clocks are as tall as they are.

</details>
