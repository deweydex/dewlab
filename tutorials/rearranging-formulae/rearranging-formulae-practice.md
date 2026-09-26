---
title: "Rearranging formulae: changing the subject — Practice"
practice_for: rearranging-formulae
year: "2026-2027"
version: 2026.09.26.1
worlds:
  rockets: Rockets, probes and the orbits they reach.
  electronics: Batteries, resistors and the voltages between them.
  music: Notes, strings and the sound waves between them.
  fantasy-maps: A made-up kingdom, and the maps drawn of it.
---

# Rearranging formulae: changing the subject — Practice

The answers are hidden in folds under each problem. Try each
rearrangement by hand first, and write your answer down. The checking
cell below then shows whether your answer agrees with the original.

## Tools

This cell holds a function called `do_they_agree`. It feeds random
numbers to the original formula and to your rearrangement, and tells
you whether they ever disagree. The example at the bottom checks $t = \frac{v - u}{a}$.

```python exec
id: tools-1
import random

def do_they_agree(original, rearranged, ranges, tries=200):
    """Feed random values to both and see whether they ever disagree.

    `original` takes the named values and returns the subject. `rearranged`
    takes the subject and the others, and should return the missing one.
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

Subtract 32 first, because the formula added 32 last (the
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
This is worth noticing. A rearrangement is often easy or hard because of
what else you know.

</details>

**6.** Why do we undo from the outside in, when we evaluate from the
inside out?

<details class="dl-answer"><summary>answer</summary>

To evaluate $u + at$, you multiply first and add last. To undo it, you
must first remove the last thing that was done. So you subtract first,
then divide.

Think of a coat over a jumper. You take off the coat before the jumper.

</details>

## Unknowns underneath

**7.** Make $R$ the subject of $\frac{1}{R} = \frac{1}{a} + \frac{1}{b}$.

<details class="dl-answer"><summary>answer</summary>

$R = \frac{1}{\frac{1}{a} + \frac{1}{b}}$. Another way to write the same
thing is $R = \frac{ab}{a + b}$.

Find $\frac{1}{R}$ first, then flip it. To get the second form, put the
right-hand side over a common denominator:
$\frac{1}{a} + \frac{1}{b} = \frac{b + a}{ab}$.

</details>

**8.** What is the combined resistance of three resistors in parallel,
of 2, 3 and 6 Ω? The rule for three is
$\frac{1}{R} = \frac{1}{a} + \frac{1}{b} + \frac{1}{c}$.

<details class="dl-answer"><summary>answer</summary>

It is 1 Ω.

$\frac{1}{2} + \frac{1}{3} + \frac{1}{6} = \frac{3}{6} + \frac{2}{6} +
\frac{1}{6} = 1$, so $\frac{1}{R} = 1$ and $R = 1$. Python gives
`1.0000000000000002` for `1 / (1/2 + 1/3 + 1/6)`, which is 1 with a
rounding error. The combined resistance is less than the smallest one,
as it was for two.

</details>

**9.** Make $x$ the subject of $y = 7 - 2x$. Then make $b$ the subject
of $a = c - \frac{b}{4}$.

<details class="dl-answer"><summary>answer</summary>

$x = \frac{7 - y}{2}$, and $b = 4(c - a)$.

In each, the letter you want is behind a minus sign. Add that term to
both sides first: $y + 2x = 7$, then $2x = 7 - y$. And
$a + \frac{b}{4} = c$, then $\frac{b}{4} = c - a$. Check the first with
$x = 2$: $y = 3$, and $\frac{7 - 3}{2} = 2$.

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

**12.** Which of these Python lines calculates $\dfrac{a + b}{2}$, the
average of $a$ and $b$?

```python exec
id: which-line-is-the-average
a, b = 6, 10
print(a + b / 2)
print((a + b) / 2)
print(a + (b / 2))
print(a / 2 + b / 2)
```

<details class="dl-answer"><summary>answer</summary>

The second and the fourth. They print 8.0, the average. The first and
the third print 11.0, because Python divides only $b$ by 2.

On paper, the fraction bar groups $a + b$ as if it had brackets. On one
line, you write the brackets yourself. The fourth line divides each
part by 2, which gives the same answer, because
$\frac{a + b}{2} = \frac{a}{2} + \frac{b}{2}$.

</details>

## Checking

**13.** Can you write a check for your answer to question 2? Then break
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

The first prints True and the second prints False. **If you never see a
check fail, you cannot know that it works.**

</details>

**14.** Why is `abs(a - b) < 1e-9` better than `a == b` when you check
a rearrangement?

<details class="dl-answer"><summary>answer</summary>

These are floats. Two calculations that should agree exactly can
differ in the last decimal place.

In Python, `0.1 + 0.2 == 0.3` is False, and that is not a bug. With
floats, "are these equal?" is nearly always the wrong question. The
right one is "are these closer together than I care about?"

</details>

**15.** If a rearrangement agrees with the original on 200 random
values, does that prove it is correct?

<details class="dl-answer"><summary>answer</summary>

No. It is strong evidence, but it is not a proof. Compare
[Logic: truth tables, XOR and De Morgan's laws](tutorial:logic-and-truth).
There, we checked all four rows, and that *was* a proof, because there were only four
cases.

Here there are infinitely many possible inputs. So a check can only fail
to find a problem. In practice, it finds every mistake you are likely to
make. That is very useful, even though it is not certainty.

</details>

## In use

**16.** The formula for compound interest is $A = P(1 + r)^n$. Make $P$
the subject. Then make $r$ the subject.

<details class="dl-answer"><summary>answer</summary>

$P = \frac{A}{(1 + r)^n}$.

For $r$: $(1 + r)^n = \frac{A}{P}$, so $1 + r = \left(\frac{A}{P}\right)^{1/n}$,
so $r = \left(\frac{A}{P}\right)^{1/n} - 1$.

The second one needs an $n$th root, which is a fractional power. It is
the same move as taking a square root, for any $n$.

</details>

**17.** You want €10,000 in 8 years, and the interest rate is 3% a year.
How much do you need to invest now?

<details class="dl-answer"><summary>answer</summary>

$P = \frac{10000}{1.03^8} \approx$ €7,894.09.

</details>

**18.** Download time, file size and rate are related by
$\text{time} = \frac{\text{size}}{\text{rate}}$. Make rate the subject.
What rate do you need to move 4 GB in 90 seconds?

<details class="dl-answer"><summary>answer</summary>

$\text{rate} = \frac{\text{size}}{\text{time}}$. So the rate is
$\frac{4 \text{ GB}}{90 \text{ s}} \approx 0.0444$ GB/s. That is about
44.4 MB/s, or about 356 Mbit/s, since there are 8 bits in a byte. (If
you count a GB as 1024 MB, the answer is about 45.5 MB/s, or 364
Mbit/s.)

In a question like this, most of the work is to watch the units. Bytes
and bits differ by a factor of eight, and people often mix them up.

</details>

**19.** The period of a pendulum (the time for one full swing, there and
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

## Your world

**20.** A problem from the world you chose.

<div class="dl-world" data-world="rockets">

A satellite in a circular orbit moves at $v = \sqrt{\frac{GM}{r}}$ m/s,
where $r$ is its distance from the Earth's centre in metres and
$GM = 3.986 \times 10^{14}$ for the Earth. Make $r$ the subject. How far
above the ground is a satellite moving at 7,700 m/s? The Earth's radius
is 6,371 km.

```python exec
id: your-world--rockets
GM = 3.986e14
earth_radius = 6_371_000
```

<details class="dl-answer"><summary>answer</summary>

$r = \frac{GM}{v^2}$, and the satellite is about 352 km up.

Square both sides: $v^2 = \frac{GM}{r}$. Multiply by $r$ and divide by
$v^2$. Then subtract the Earth's radius:

```python
r = GM / 7700 ** 2
print(r, (r - earth_radius) / 1000)
```

$r$ is about 6,723 km from the centre, so about 352 km above the
ground. The International Space Station orbits at about 400 km, a
little slower.

</details>

</div>

<div class="dl-world" data-world="electronics">

The power a resistor turns into heat is $P = \frac{V^2}{R}$. Make $R$
the subject. What is the resistance of a 60 W heater made for 230 V?
Then make $V$ the subject.

```python exec
id: your-world--electronics
power = 60
volts = 230
```

<details class="dl-answer"><summary>answer</summary>

$R = \frac{V^2}{P}$, which is about 882 Ω. And $V = \sqrt{PR}$.

```python
resistance = volts ** 2 / power
print(resistance, (power * resistance) ** 0.5)
```

Multiply both sides by $R$, then divide by $P$. For $V$, multiply by
$R$ and take the square root. The round trip returns 230, apart from
rounding.

</details>

</div>

<div class="dl-world" data-world="music">

The wavelength of a sound is $\lambda = \frac{v}{f}$, where $v$ is the
speed of sound, about 343 m/s in air, and $f$ is the frequency. Make $f$
the subject. What frequency has a wavelength of exactly 1 m? What is the
wavelength of the orchestra's A, 440 Hz?

```python exec
id: your-world--music
speed = 343
```

<details class="dl-answer"><summary>answer</summary>

$f = \frac{v}{\lambda}$, so a 1 m wavelength is 343 Hz. The A at
440 Hz has a wavelength of about 0.78 m.

```python
print(speed / 1, speed / 440)
```

Multiply both sides by $f$, then divide by $\lambda$. Higher notes have
shorter waves, which is why a small speaker can play high notes but
struggles with low ones.

</details>

</div>

<div class="dl-world" data-world="fantasy-maps">

On a map drawn at 1 : $s$, a real distance in km is
$\text{ground} = \frac{\text{map} \times s}{100\,000}$, with the map
distance in cm. A mapmaker measures a road that is 12 km long as 24 cm
on an old map. Make $s$ the subject. What scale was the old map?

```python exec
id: your-world--fantasy-maps
ground_km = 12
map_cm = 24
```

<details class="dl-answer"><summary>answer</summary>

$s = \frac{100\,000 \times \text{ground}}{\text{map}}$, so the map is
1 : 50,000.

```python
print(100_000 * ground_km / map_cm)
```

Multiply both sides by 100,000, then divide by the map distance. A
kilometre is 100,000 cm, which is where the 100,000 comes from.

</details>

</div>

## From earlier

**21.** In [Polynomials: representing and combining them in
Python](tutorial:expressions-come-alive) we expanded brackets. Make $x$
the subject of $y = (x + 2)^2 - 4$, for $x$ of $-2$ or more. Is it
easier to expand first, or not?

<details class="dl-answer"><summary>answer</summary>

$x = \sqrt{y + 4} - 2$.

It is easier not to expand. $x$ appears once, inside the bracket, so
undo from the outside in: add 4, take the square root, then subtract 2.
Expanded, $y = x^2 + 4x$, and $x$ appears twice, which is much harder.
We keep the positive root because $x + 2$ is 0 or more. Check with
$y = 12$: $\sqrt{16} - 2 = 2$, and $(2 + 2)^2 - 4 = 12$.

</details>

**22.** In [Probability: simple, compound and
conditional](tutorial:what-are-the-chances), the chance of at least one
six in $n$ rolls of a die is $p = 1 - \left(\frac{5}{6}\right)^n$. Make
$n$ the subject. How many rolls give an even chance, $p = 0.5$? The
rules for logarithms from
[Number types, powers and logarithms](tutorial:numbers-and-their-families)
bring $n$ down.

<details class="dl-answer"><summary>answer</summary>

$n = \dfrac{\log(1 - p)}{\log(5/6)}$, which is about 3.8 for
$p = 0.5$. So four rolls give a better than even chance.

$\left(\frac{5}{6}\right)^n = 1 - p$. Take the logarithm of both sides:
$n \log\frac{5}{6} = \log(1 - p)$, and divide. With three rolls the
chance is about 0.42, and with four about 0.52.

</details>
