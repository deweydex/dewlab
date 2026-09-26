---
title: "Running a formula backwards: rearranging and inverses"
year: "2026-2027"
version: 2026.09.25.2
covers:
  one-formula-three-questions:
    covers: [MIT-1.7]
  the-same-move-on-both-sides:
    covers: [MIT-1.7]
  tools-for-any-trip:
    touches: [MIT-1.7, PDP-LO8]
  undoing-in-reverse-order:
    covers: [MIT-1.7, MIT-3.1]
  the-promise-run-backwards:
    covers: [MIT-3.1]
    touches: [PDP-LO8]
  when-the-way-back-needs-care:
    covers: [MIT-1.7, MIT-3.1]
  fractions-with-letters-in-them:
    covers: [MIT-1.7]
---

# Running a formula backwards: rearranging and inverses

The sunlight on your hand left the Sun 8 minutes and 19 seconds ago. How far has it come? The International Space Station goes once
round the Earth, about 42,700 km, in 92.9 minutes. How fast is it
going? And a radio message to a rover on Mars, 225 million km away,
travels as fast as light. How long does the rover wait for it?

Three questions about space, and one short formula answers all of
them, if we know how to run it backwards. That is what this page is
about.

On this page we:

- see one formula answer three different questions
- rearrange a formula by doing the same move to both sides
- undo a temperature formula, step by step, in reverse order
- write functions that undo each other, and test them both ways
- find where a rearranged formula needs a smaller space
- add and simplify fractions that have letters in them

> **The space we're in.** Numbers that measure things: kilometres,
> seconds, degrees. A formula here is a rule that stays true, and we may
> do any move to it, as long as we do the same move to both sides. One
> thing usually goes unsaid: a formula with a division in it has no
> answer when the bottom of the fraction is 0. Your toolkit is loaded,
> with every function from the earlier pages.

## Warm-up

Two questions from earlier pages. The first is from
[Numbers a computer can hold](tutorial:numbers-a-computer-can-hold), and
the second from
[Measuring rooms and tins](tutorial:measuring-rooms-and-tins).

```question
id: running-a-warm-up-1
type: fill-in-the-blank

Python works out `2 + 3 * 4` as {14}, because it multiplies before it adds.
```

```question
id: running-a-warm-up-2
type: fill-in-the-blank

A floor is 5 m long and 4 m wide. Its area is {20} square metres.
```

Keep that floor in mind. If a floor has an area of 20 square metres and
is 5 m long, how wide is it? If you said 4 m, you ran a formula
backwards.

## One formula, three questions

Speed, distance and time are tied together by one rule. In words: the
average speed is the distance travelled, divided by the time it took.
With letters, $s$ for speed, $d$ for distance and $t$ for time:

$$s = \frac{d}{t}$$

Let's check it on the space station. It goes 42,700 km in 92.9
minutes, which is $92.9 \times 60$ seconds. Before you run the cell,
guess: is its speed nearer 1 km a second, or 10?

```python exec
id: running-a-three-questions-1
distance_km = 42700
time_seconds = 92.9 * 60
print(distance_km / time_seconds)
```

About 7.66 km every second, which is about 27,600 km/h. At that speed
you would get from Dublin to Galway in under half a minute. The formula answers "how fast?"
straight away, because $s$ is alone on the left. The letter on its own
on one side of a formula is called the *subject* of the formula. Here
the subject is $s$.

The Sun asks a different question. Light travels 299,792 km every
second, so we know $s = 299{,}792$, and $t = 499$ seconds, and we want
$d$. The formula still holds, but $d$ is not on its own. We could
guess numbers until $\frac{d}{499}$ comes out as 299,792, but that is
slow. A better way is to change the formula so that $d$ is the subject.

<aside class="dl-note" id="running-note-metre">

**A metre made of light.** Since 1983, the metre has been defined by
light. It is the distance light travels in empty space in exactly
$\frac{1}{299{,}792{,}458}$ of a second. So the speed of light is exactly
299,792,458 metres a second, by definition.

</aside>

## The same move on both sides

Think of a formula as a balance, with the same weight on each side. If
we double one side, it tips, unless we double the other side too. So
here is the one rule for moving things around in a formula: any move is
allowed, as long as we do the same move to both sides.

Rearranging a formula to make a different letter its subject is called
*transposing* the formula, or *changing the subject*.

Start from $s = \frac{d}{t}$. On the right, $d$ is divided by $t$. The
move that undoes "divide by $t$" is "multiply by $t$". So we multiply
both sides by $t$:

$$s \times t = \frac{d}{t} \times t$$

On the right, dividing by $t$ and then multiplying by $t$ cancel out,
and $d$ is left. So:

$$d = s \times t$$

In words: the distance is the speed times the time. For the Sun, that
is $299{,}792 \times 499$, about 149.6 million km.

Now the message to Mars. We want $t$, and $t$ is at the bottom of the fraction.
Take $d = s \times t$, which we found above. Here $t$ is multiplied by
$s$, so we undo that by dividing both sides by $s$:

$$\frac{d}{s} = t$$

In words: the time is the distance divided by the speed. For Mars,
$\frac{225{,}000{,}000}{299{,}792}$ is about 751 seconds: the rover waits
about 12 and a half minutes.

That is one formula written three ways:

| Question | Subject | Formula |
|---|---|---|
| How fast? | $s$ | $s = \frac{d}{t}$ |
| How far? | $d$ | $d = s \times t$ |
| How long? | $t$ | $t = \frac{d}{s}$ |

How do we know we rearranged correctly? We can put the answers back into
the first formula and see if it still holds. Before you run the cell,
which lines do you expect to print `True`?

```python exec
id: running-a-both-sides-1
sun_distance = 299792 * 499
mars_wait = 225_000_000 / 299792

print(sun_distance, mars_wait)
print(sun_distance / 499 == 299792)
print(225_000_000 / mars_wait == 299792)
```

Both checks print `True`. (The `_` in `225_000_000` is only there to
make the number easier to read. Python ignores it.) Putting an answer back into the formula it
came from is called *substituting* it back, and it is the best habit on
this page. It turns "I think I rearranged it right" into "I checked".

### Your turn

The Moon is about 384,400 km away. The crew of Apollo 11 took about 76
hours to get there in 1969.

1. Before you run anything, which of the three formulas gives their
   average speed in km/h?
2. In the cell below, work it out. (Their real path curved, so this is
   the average over a straight line.)
3. Substitute it back: does the speed times the time give 384,400 km?

```python exec
id: running-a-both-sides-your-turn
time_hours = 76
# their average speed, then a check
```

## Tools for any trip

We will need these three formulas again, on this page and later. So
let's put them in the toolkit. The first one is written for you. Can you
write the other two? Each is one line.

```python exec
id: running-a-toolkit-travel
toolkit: yes
def speed(distance, time):
    """Return the average speed for a distance covered in a time.

    Use matching units: km and seconds give km/s, km and hours km/h.
    time must not be 0.
    """
    return distance / time


def travel_time(distance, speed):
    """Return how long it takes to cover distance at an average speed.

    Use matching units: km and km/s give seconds, km and km/h hours.
    speed must not be 0.
    """
    ...


def distance_travelled(speed, time):
    """Return the distance covered at an average speed for a time.

    Use matching units: km/s and seconds give km, km/h and hours km.
    """
    ...
```

```python toolkit-reference
for: running-a-toolkit-travel
def speed(distance, time):
    """Return the average speed for a distance covered in a time.

    Use matching units: km and seconds give km/s, km and hours km/h.
    time must not be 0.
    """
    return distance / time


def travel_time(distance, speed):
    """Return how long it takes to cover distance at an average speed.

    Use matching units: km and km/s give seconds, km and km/h hours.
    speed must not be 0.
    """
    return distance / speed


def distance_travelled(speed, time):
    """Return the distance covered at an average speed for a time.

    Use matching units: km/s and seconds give km, km/h and hours km.
    """
    return speed * time
```

Inside `travel_time`, the name `speed` means the number it was given,
not the function above it. A later page,
[What a function can see](tutorial:what-a-function-can-see), is about
exactly that.

A signal's trip counts as a trip. Now the tests. The first three check
the three questions from the top of this page. The last two are different: each one runs a formula forwards,
then backwards, and expects to arrive where it started. Until your two
functions are written, this cell stops with an error.

```python exec
id: running-a-toolkit-travel-tests
assert distance_travelled(299792, 499) == 149596208
assert round(speed(42700, 92.9 * 60), 2) == 7.66
assert round(travel_time(225_000_000, 299792)) == 751

assert travel_time(distance_travelled(80, 3), 80) == 3
assert speed(distance_travelled(80, 3), 3) == 80
print("The travel tools keep their promises.")
```

```hint
What did you expect the failing line to give? Try printing
`travel_time(60, 20)` on its own. It should be 3. What does your version
give now?
```

<details class="dl-answer"><summary>answer</summary>

Here is one good way. In `travel_time`, the `...` becomes
`return distance / speed`. In `distance_travelled`, it becomes
`return speed * time`. If you have not written them yet, put these in
the stub now, so that later cells on this page can use them.

</details>

## Undoing, in reverse order

The average temperature on Mars is about −60 °C. American pages often
give it as −76 degrees: degrees Fahrenheit, the scale used in the
United States. To turn degrees Celsius into Fahrenheit, there are two
steps:

1. multiply by $\frac{9}{5}$;
2. then add 32.

As a formula, with $C$ for Celsius and $F$ for Fahrenheit:

$$F = \frac{9}{5}C + 32$$

Water freezes at 0 °C, which is 32 °F, and boils at 100 °C, which is
212 °F. Let's check the formula gives both.

```python exec
id: running-a-reverse-1
print(0 * 9 / 5 + 32)
print(100 * 9 / 5 + 32)
```

Both come out as they should. Now the other way: is −76 °F really
−60 °C? We need $C$ as the subject.

On [Machines that take a number](tutorial:machines-that-take-a-number#running-it-backwards-the-inverse),
we undid the sensor's two steps in the opposite order. Think of
putting on socks, then shoes. To undo that, you take off the shoes
first, then the socks. The last thing done is the first thing undone.
Here, the last step going forwards was "add 32", so the first step
going backwards is "subtract 32". Then we undo "multiply by
$\frac{9}{5}$" by multiplying by $\frac{5}{9}$.

The rule from the last section does these moves for us, one at a time,
to both sides:

$$F - 32 = \frac{9}{5}C$$

$$\frac{5}{9}(F - 32) = C$$

So $C = \frac{5}{9}(F - 32)$. The brackets matter: they say "subtract
first", the way the undoing needs.

A common slip is to do the undoing steps in the forward order: multiply
by $\frac{5}{9}$ first, then subtract 32. Which of these two lines do you
think gives −60 °C for −76 °F? Run it to check.

```python exec
id: running-a-reverse-2
fahrenheit = -76
print((fahrenheit - 32) * 5 / 9)
print(fahrenheit * 5 / 9 - 32)
```

The first line gives −60.0. The second gives about −74.2. Look at how
believable that is: it is a cold Mars number too, and nothing about it
looks wrong. The steps were right, and the order was wrong. Undoing is
sequence, run in reverse.

```question
id: running-a-reverse-3
type: multiple-choice
answer: 3

An image editor scales a picture to 150% of its width, then crops 20
pixels off. The result is 1,180 pixels wide. How do we find the width
of the original?

- Multiply 1,180 by 1.5, then subtract 20.
  - This does the forward steps again, instead of undoing them.
- Divide 1,180 by 1.5, then add 20.
  - Each step is undone, but in the order they were done; the last step done is the first to undo.
- Add 20 to 1,180, then divide by 1.5.
  - Undo the last step first: put back the 20 pixels, then undo the scaling.
```

## The promise run backwards

A function makes a promise: give it a temperature in Celsius, and it
gives back the same temperature in Fahrenheit. Its inverse, $f^{-1}$,
keeps the same promise backwards: give it −76, and it gives back −60.

The first function below is written for you. The formula we have
rearranged is its inverse. Can you write it as a function?

```python exec
id: running-a-toolkit-temperature
toolkit: yes
def celsius_to_fahrenheit(celsius):
    """Return a temperature in degrees Fahrenheit, given it in degrees Celsius."""
    return celsius * 9 / 5 + 32


def fahrenheit_to_celsius(fahrenheit):
    """Return a temperature in degrees Celsius, given it in degrees Fahrenheit.

    This undoes celsius_to_fahrenheit.
    """
    ...
```

```python toolkit-reference
for: running-a-toolkit-temperature
def celsius_to_fahrenheit(celsius):
    """Return a temperature in degrees Fahrenheit, given it in degrees Celsius."""
    return celsius * 9 / 5 + 32


def fahrenheit_to_celsius(fahrenheit):
    """Return a temperature in degrees Celsius, given it in degrees Fahrenheit.

    This undoes celsius_to_fahrenheit.
    """
    return (fahrenheit - 32) * 5 / 9
```

How do we test an inverse? There are two kinds of test. The first kind
uses values we already know: 0 °C is 32 °F, and 100 °C is 212 °F. The
second kind needs no known values at all. We go there and back, and we
should arrive where we started. This cell and the next two need your
`fahrenheit_to_celsius`, so write it first. What do you expect the last
three lines to print?

```python exec
id: running-a-backwards-1
assert fahrenheit_to_celsius(32) == 0
assert fahrenheit_to_celsius(212) == 100
assert fahrenheit_to_celsius(-76) == -60

print(fahrenheit_to_celsius(celsius_to_fahrenheit(37)))
print(fahrenheit_to_celsius(celsius_to_fahrenheit(-40)))
print(fahrenheit_to_celsius(celsius_to_fahrenheit(1)))
```

<details class="dl-answer"><summary>answer</summary>

One good way: in `fahrenheit_to_celsius`, the `...` becomes
`return (fahrenheit - 32) * 5 / 9`. The brackets make the subtraction
happen first.

</details>

Body temperature, 37 °C, comes back as `37.0`. And −40 comes back as
−40: it is the one temperature where both scales agree.

But 1 °C comes back as `0.9999999999999984`. The two functions are
right. As on
[Everything is ones and zeros](tutorial:everything-is-ones-and-zeros),
a float is very close to the true value, and each step of the trip adds
a tiny error. So for a float, "we arrive where we started" means "we
arrive very, very close". For now we round before we compare. The next page,
[Does it work?](tutorial:does-it-work), builds a better tool for this.

```python exec
id: running-a-backwards-2
there_and_back = fahrenheit_to_celsius(celsius_to_fahrenheit(1))
print(there_and_back == 1)
print(round(there_and_back, 9) == 1)
```

On [Machines that take a number](tutorial:machines-that-take-a-number#machines-in-a-row-composition)
we joined two functions into one with `compose`, and saw that a function
composed with its inverse gives back whatever it is given. Here it is,
tested on a whole row of temperatures, with a loop. What will it print?

```python exec
id: running-a-backwards-3
there_and_back = compose(fahrenheit_to_celsius, celsius_to_fahrenheit)

for celsius in [-80, -60, -40, 0, 1, 18.5, 37, 100]:
    assert round(there_and_back(celsius), 9) == celsius
print("fahrenheit_to_celsius undoes celsius_to_fahrenheit.")
```

The loop checks eight temperatures in one go, from a lab freezer to
boiling water. A test like this does not need anyone to know the right answers.
It only needs the promise: going there and back changes nothing.

### Your turn

Biology labs keep samples in freezers at −80 °C. An American catalogue
lists the same freezer in Fahrenheit.

1. Before you run anything, guess: is −80 °C more or fewer than −80 °F?
2. In the cell below, use `celsius_to_fahrenheit` to find it.
3. Run it back the other way with `fahrenheit_to_celsius`. Do you get
   −80 again, or very close to it?

```python exec
id: running-a-backwards-your-turn
# The lab freezer, in Fahrenheit, and back again
```

## When the way back needs care

A formula that works for every number going forwards may not work for
every number going backwards. Here are two places to take care.

The first is zero. A Mars rover parked for 10 hours has a speed of 0,
and `distance_travelled(0, 10)` is 0 km. That makes sense. Now run the
same formula backwards: how long does the parked rover take to reach a
rock 1 km away? The next cell uses your two travel functions, and it is
meant to fail. Before you run it, which error do you think Python will
give?

```python exec
id: running-a-way-back-1
print(distance_travelled(0, 10))
print(travel_time(1, 0))
```

The first line prints `0`. The second stops with a `ZeroDivisionError`.
The question has no answer, because a parked rover never arrives. The
formula $d = s \times t$ accepts a speed of 0, and the rearranged
$t = \frac{d}{s}$ does not. So rearranging can make the domain smaller.
That is why the docstring of `travel_time` says "speed must not be 0":
the promise names its own space.

The second place is a square. On
[Measuring rooms and tins](tutorial:measuring-rooms-and-tins), the area
of a circle was $A = \pi r^2$. The James Webb Space Telescope collects
light over 25.4 square metres of mirror. If that were one round mirror,
what would its radius be?

We want $r$ as the subject. First, divide both sides by $\pi$:

$$\frac{A}{\pi} = r^2$$

Then undo the square with a square root:

$$r = \sqrt{\frac{A}{\pi}}$$

On [Machines that take a number](tutorial:machines-that-take-a-number#running-it-backwards-the-inverse)
we saw that squaring has no inverse on all of $\mathbb{R}$, because 3
and −3 both square to 9. So which space are we in? A radius is a
length, and a length is never negative. In the space of numbers from 0
upwards, the square root is the one answer. What do you expect the
radius to be, roughly? Run it to check, and to substitute it back.

```python exec
id: running-a-way-back-2
import math

mirror_area = 25.4
radius = math.sqrt(mirror_area / math.pi)
print(radius)
print(circle_area(radius))
```

The radius is about 2.84 m, so one round mirror would be about 5.7 m
across. Putting the radius back into `circle_area` gives 25.4 again.
The real mirror is 6.5 m across, because
it is 18 six-sided pieces with small gaps between them, not one
circle.

```question
id: running-a-way-back-3
type: multiple-choice
answer: 2

Which rearranged formula has a smaller domain than the formula it came
from?

- $d = s \times t$, rearranged from $t = \frac{d}{s}$
  - Rearranging this way removes a division, so s = 0 is allowed again: the domain grows.
- $t = \frac{d}{s}$, rearranged from $d = s \times t$
  - Dividing by s rules out s = 0, which d = s × t allowed.
- $F = \frac{9}{5}C + 32$, rearranged from $C = \frac{5}{9}(F - 32)$
  - Both formulas accept every temperature, so neither domain is smaller.
```

## Fractions with letters in them

A drone flies out to a weather station at 20 km/h, into the wind, and
comes back at 30 km/h, with the wind behind it. What was its average
speed for the whole trip?

Pause and guess before you read on. Many people say 25 km/h, halfway
between. Let's find out, without knowing how far the station is. Call
the distance $d$.

Going there takes $\frac{d}{20}$ hours, and coming back takes
$\frac{d}{30}$ hours. The whole trip takes

$$\frac{d}{20} + \frac{d}{30}$$

A fraction with a letter in it, like $\frac{d}{20}$, is called an
*algebraic fraction*. We add algebraic fractions the same way as number
fractions: first give them the same bottom number, then add the tops.
The bottom number of a fraction is its *denominator*. The smallest
number that both 20 and 30 divide into is 60, so 60 is a *common
denominator*:

$$\frac{d}{20} + \frac{d}{30} = \frac{3d}{60} + \frac{2d}{60} = \frac{5d}{60} = \frac{d}{12}$$

The last step divides the top and the bottom by 5, which leaves the
value the same. So the whole trip takes $\frac{d}{12}$ hours.

The whole trip covers $2d$ km. The average speed is distance over time:

$$\frac{2d}{\;\frac{d}{12}\;} = 2d \times \frac{12}{d} = 24$$

The $d$ on the top and the $d$ on the bottom cancel. The average speed
is 24 km/h, not 25, and it is 24 whatever the distance. Is that
believable? Let's check with the travel tools from your toolkit, for
three different stations. (This cell needs your `travel_time`.) Before you
run it, what do you expect each line to show?

```python exec
id: running-a-fractions-1
for distance in [6, 15, 42]:
    whole_time = travel_time(distance, 20) + travel_time(distance, 30)
    print(distance, whole_time, speed(2 * distance, whole_time))
```

Every line gives an average speed of 24.0. The algebra said the
distance would not matter, and the code agrees.

Why is it less than 25? The drone spends longer on the slow part of the
trip, so the slow speed counts for more of the time. I think this is the
most surprising result on the page, and it has a name: the harmonic
mean.

### Your turn

An underwater robot dives to the sea floor at 2 m/s, and climbs back at
3 m/s.

1. Write the time for the two trips, $\frac{d}{2} + \frac{d}{3}$, as one
   fraction. What is the common denominator?
2. Work out the average speed with algebra.
3. Check it with the toolkit in the cell below, for a sea floor 100 m
   down and one 3,000 m down.

```python exec
id: running-a-fractions-your-turn
# Check the robot's average speed here
```

<details class="dl-answer"><summary>answer</summary>

$\frac{d}{2} + \frac{d}{3} = \frac{3d}{6} + \frac{2d}{6} = \frac{5d}{6}$,
with a common denominator of 6. The average speed is
$2d \div \frac{5d}{6} = 2d \times \frac{6}{5d} = \frac{12}{5} = 2.4$ m/s.

```python
for depth in [100, 3000]:
    whole_time = travel_time(depth, 2) + travel_time(depth, 3)
    print(depth, speed(2 * depth, whole_time))
```

Both lines give 2.4. Yours may be written another way and be as
good.

</details>

<details class="dl-why"><summary>Why this way?</summary>

This page rearranged every formula with one rule: do the same move to
both sides. Many people learned a shorter rule at school: "change sides,
change signs". A number moves across the equals sign, and a plus becomes
a minus, a times becomes a divide.

The short rule is fast, and it gives the right answer when it is used
with care. Many people who are good at algebra use it every day.

We used the balance because the short rule hides why it works, and a
rule you cannot explain is hard to repair. "The same
move on both sides" is one promise that covers every case, including the
ones where the short rule often fails, like the brackets in the
temperature formula. The short rule is the balance, with the middle
steps left out.

</details>

## Four questions, looking back

| The question | On this page |
|---|---|
| What is named here? | letters in a formula, $s$, $d$ and $t$; the subject, the letter on its own; a denominator shared by two fractions |
| What is promised? | a formula stays true after the same move on both sides; `fahrenheit_to_celsius` promises to undo `celsius_to_fahrenheit` |
| What happens when? | undoing runs the steps in reverse order: the last step forwards is the first step back |
| What does this space let us do? | $d = s \times t$ allows a speed of 0, and $t = \frac{d}{s}$ does not; a radius lives in the numbers from 0 upwards, where the square root is the one answer; floats come back very close, not always equal |

## What we have now

| Term or move | What it means |
|---|---|
| subject | the letter on its own on one side of a formula |
| transposing, changing the subject | rearranging a formula so a different letter is the subject |
| the same move on both sides | the rule that keeps a formula true while we rearrange it |
| substituting back | putting an answer into the formula it came from, to check it |
| undoing in reverse order | the last step forwards is the first step back |
| a smaller domain | a rearranged formula can refuse inputs the first one accepted, like a speed of 0 |
| algebraic fraction | a fraction with a letter in it, like $\frac{d}{20}$ |
| denominator, common denominator | the bottom of a fraction; a bottom number several fractions can share |
| `speed`, `travel_time`, `distance_travelled` | your toolkit's three forms of $s = \frac{d}{t}$ |
| `celsius_to_fahrenheit`, `fahrenheit_to_celsius` | your toolkit's temperature converter, both ways |

For another route through rearranging, the integrated course has
[Rearranging formulae: changing the subject](tutorial:rearranging-formulae).
