---
title: "Running a formula backwards: rearranging and inverses — Practice"
practice_for: running-a-formula-backwards
year: "2026-2027"
version: 2026.09.26.1
---

# Running a formula backwards: rearranging and inverses — Practice

Each problem says what kind it is. **Predict** means guess first, then
run. **Make** means write something new. **Fix** means find why code
that looks fine does something else, and change it. **Explain** means
answer in words. **Another
way** means reach the same place by a second route. The answers are
folded away until you open them.

Your toolkit is loaded on this page, including the travel and
temperature tools from the tutorial.

## Warm-up

Use this cell for any of the warm-up problems.

```python exec
id: running-a-practice-warm-up
# Try things here
```

**1. Predict.** Light from the Moon takes 1.28 seconds to reach you,
at 299,792 km a second. The space station goes 42,700 km at 7.66 km a
second. The sound of thunder travels 1 km in 2.9 seconds. What does each
line print, roughly?

```python
print(distance_travelled(299792, 1.28))
print(travel_time(42700, 7.66))
print(speed(1, 2.9))
```

<details class="dl-answer"><summary>answer</summary>

It prints about `383733.76`, `5574.4` and `0.3448`.

The Moon is about 384,000 km away. The station takes about 5,574
seconds for one lap, which is 92.9 minutes. Sound travels about 0.345 km
a second, which is 345 metres. Each line uses a different form of the
same formula, $s = \frac{d}{t}$.

</details>

**2. Make.** A weather forecast gives wind speeds in km/h, and a sailing
app wants metres per second. The rule is: km/h $= 3.6 \times$ m/s.
Rearrange it to give m/s, and use it to turn a storm gust of 130 km/h
into metres per second, to one decimal place.

<details class="dl-answer"><summary>answer</summary>

Start from $k = 3.6 \times m$, with $k$ for km/h and $m$ for m/s. Here
$m$ is multiplied by 3.6, so divide both sides by 3.6:

$$m = \frac{k}{3.6}$$

```python
gust_kmh = 130
gust_ms = gust_kmh / 3.6
print(round(gust_ms, 1))
print(round(gust_ms * 3.6, 9) == gust_kmh)
```

This prints `36.1`, then `True`. The second line substitutes the answer
back into the first formula.

</details>

**3. Explain.** To turn Fahrenheit into Celsius, we subtract 32 first,
and multiply by $\frac{5}{9}$ second. Going the other way,
`celsius_to_fahrenheit` multiplies first and adds 32 second. Why are the
two orders opposite?

<details class="dl-answer"><summary>answer</summary>

Going forwards, the last step is "add 32". We undo the steps from the last
one back to the first, the way you take off your shoes before your
socks. So the first step back is "subtract 32", and the step after it
undoes the multiplying. If we multiplied first, the 32 would still be
mixed in with the number we multiply, and we would get a different
temperature.

</details>

**4. Predict.** The novel *Fahrenheit 451* takes 451 °F as the
temperature at which book paper catches fire. What do these two lines print? Will
the second one print exactly 451?

```python
print(fahrenheit_to_celsius(451))
print(celsius_to_fahrenheit(fahrenheit_to_celsius(451)))
```

<details class="dl-answer"><summary>answer</summary>

This prints `232.77777777777777`, then `451.0`.

The round trip returns exactly 451 this time. Sometimes a float round
trip lands exactly, and sometimes it lands very close, like the
`0.9999999999999984` for 1 °C in the tutorial. That is why a test
of a round trip rounds first, or asks "close enough?".

</details>

## Core

A cell for the core problems.

```python exec
id: running-a-practice-core
# Your working for problems 5 to 12
```

**5. Make.** Download speeds are given in megabits per second (Mb/s),
but file sizes are in megabytes (MB). A byte is 8 bits, so a megabyte is
8 megabits. Write `megabits_to_megabytes(megabits)` and its inverse,
`megabytes_to_megabits(megabytes)`. Test each with a known value, then
test the round trip for 50, 200 and 1,234.56. How many megabytes a
second does a 100 Mb/s connection download?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Going forwards, megabytes $=$ megabits $\div 8$.
2. Rearrange for megabits: which move undoes "divide by 8"?
3. For the round trip, round to 9 places before comparing, as the
   tutorial did.

**Think about:** why a known value like 8 megabits $=$ 1 megabyte is a
better first test than a round trip.

**Try this next:** a gigabit is 1,000 megabits. Use `compose` to make
`gigabits_to_megabytes`.

</details>

<details class="dl-answer"><summary>answer</summary>

Here is one answer. Yours may be different and work too.

```python
def megabits_to_megabytes(megabits):
    """Return a size in megabytes, given it in megabits."""
    return megabits / 8


def megabytes_to_megabits(megabytes):
    """Return a size in megabits, given it in megabytes. Undoes megabits_to_megabytes."""
    return megabytes * 8


assert megabits_to_megabytes(8) == 1
assert megabytes_to_megabits(1) == 8
for megabits in [50, 200, 1234.56]:
    assert round(megabytes_to_megabits(megabits_to_megabytes(megabits)), 9) == megabits
print(megabits_to_megabytes(100))
```

An assert prints nothing when it holds, so the only line is `12.5`. A 100 Mb/s
connection downloads 12.5 MB a second. A known value checks the factor.
A round trip checks that the two functions undo each other, and it
would still pass if both used a factor other than 8. The two kinds of
test find different problems.

</details>

**6. Fix.** Schlomi, who is learning Python too, writes a health app
that turns a temperature taken in Fahrenheit into Celsius. A fever of
100.4 °F is 38 °C, but the app says about 82.6. Can you find the line
that does not do what Schlomi meant?

```python exec
id: running-a-practice-fix-fever
def to_celsius(fahrenheit):
    """Return a temperature in degrees Celsius, given it in degrees Fahrenheit."""
    return fahrenheit - 32 * 5 / 9
```

```inputs
round(to_celsius(32), 9)       # freezing
round(to_celsius(100.4), 9)    # a fever
```

```solution
def to_celsius(fahrenheit):
    """Return a temperature in degrees Celsius, given it in degrees Fahrenheit."""
    return (fahrenheit - 32) * 5 / 9
---
Python multiplies before it subtracts, so `fahrenheit - 32 * 5 / 9`
takes away $\frac{160}{9}$, about 17.8, and never subtracts 32 at all.
Brackets make the subtraction happen first.

The formula $C = \frac{5}{9}(F - 32)$ has the brackets too, for the
same reason.
```

**7. Make.** A music producer knows that a track's length in seconds is
$\text{seconds} = \frac{\text{beats} \times 60}{\text{bpm}}$, where bpm
is the tempo in beats per minute. Rearrange it to make bpm the subject.
A 3-minute track has 384 beats. What is its tempo? Substitute your answer
back to check it.

<details class="dl-answer"><summary>answer</summary>

Multiply both sides by bpm:
$\text{seconds} \times \text{bpm} = \text{beats} \times 60$.
Then divide both sides by seconds:

$$\text{bpm} = \frac{\text{beats} \times 60}{\text{seconds}}$$

```python
def tempo(beats, seconds):
    """Return the tempo in beats per minute of a track with beats in seconds."""
    return beats * 60 / seconds

track_bpm = tempo(384, 180)
print(track_bpm)
print(384 * 60 / track_bpm)
```

This prints `128.0`, then `180.0`. Three minutes is 180 seconds, and
putting 128 bpm back into the first formula gives 180 seconds again.

</details>

**8. Make.** A 3D printer's software estimates how long a print takes.
Say that for one printer the rule is 3 minutes for each gram of
plastic, plus 12 minutes to warm up. (Real estimates depend on the
shape. This is a simple model.) The printer is free for 2 hours. What
is the heaviest print that will finish in time? Write the rule, run it
backwards, and check.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Forwards: minutes $= 3 \times$ grams $+ 12$. Two steps: multiply,
   then add.
2. Backwards, undo the last step first.
3. Two hours is how many minutes?

**Think about:** which step did the temperature formula undo first, and
why is this the same?

</details>

<details class="dl-answer"><summary>answer</summary>

$m = 3g + 12$. Subtract 12 from both sides, then divide both sides by
3:

$$g = \frac{m - 12}{3}$$

```python
def print_minutes(grams):
    """Return the minutes a print of grams takes, warm-up included."""
    return 3 * grams + 12


def heaviest_print(minutes):
    """Return the heaviest print, in grams, that finishes in minutes. Undoes print_minutes."""
    return (minutes - 12) / 3


print(heaviest_print(2 * 60))
print(print_minutes(heaviest_print(120)))
```

This prints `36.0`, then `120.0`. A print of 36 g takes exactly 2
hours.

</details>

**9. Explain.** A disk stores files in blocks of 4,096 bytes each. A
file of 1 byte still takes a whole block, and a file of 4,097 bytes
takes two. Your file takes 3 blocks. Can you find exactly how
big it is? What does this say about running the rule backwards?

<details class="dl-answer"><summary>answer</summary>

No. Every file from 8,193 bytes up to 12,288 bytes takes 3 blocks, so
"3 blocks" only tells you the size was somewhere in that range. Many
inputs give the same output, so the rule is not one-to-one, and it has
no inverse. The best a way back can do is give a range of sizes. Like
`round()`, the rule loses information, and nothing can get it
back.

</details>

**10. Another way.** Is there a temperature that is the same number in
Celsius and in Fahrenheit? Find it two ways: with algebra, and with a
loop that tries every whole number of degrees from −100 to 100.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. "The same number" means $F = C$. Put $C$ in place of $F$ in
   $F = \frac{9}{5}C + 32$.
2. Take $\frac{9}{5}C$ from both sides, and see what is left.
3. For the loop, `range(-100, 101)` gives every whole number from −100
   to 100.

**Try this next:** at what temperature is the Fahrenheit number exactly
double the Celsius number?

</details>

<details class="dl-answer"><summary>answer</summary>

With algebra, set $F = C$:

$$C = \frac{9}{5}C + 32$$

Take $\frac{9}{5}C$ from both sides: $-\frac{4}{5}C = 32$. Multiply both
sides by $-\frac{5}{4}$: $C = -40$.

With a loop:

```python
for celsius in range(-100, 101):
    if celsius_to_fahrenheit(celsius) == celsius:
        print(celsius)
```

This prints `-40`. The loop only finds whole numbers, but it needs no
algebra. The algebra finds the answer even if it had not been a whole
number. For "double", $2C = \frac{9}{5}C + 32$ gives $C = 160$.

</details>

**11. Fix.** Schlomo, who is learning Python too, times a drone that
flies $d$ km up a valley at 40 km/h, taking $\frac{d}{40}$ hours, and
back at 60 km/h, taking $\frac{d}{60}$ hours. He writes the total as
one fraction by adding the tops and adding the bottoms. Is his short
form the same as the long form, $\frac{d}{40} + \frac{d}{60}$? Can you
find the line that does not do what Schlomo meant?

```python exec
id: running-a-practice-fix-valley
def valley_flight_hours(distance):
    """Return the hours to fly distance km up the valley at 40 km/h and back at 60 km/h."""
    return 2 * distance / 100
```

```inputs
round(valley_flight_hours(3), 9)     # the short form...
round(3 / 40 + 3 / 60, 9)            # ...and the long form
round(valley_flight_hours(6), 9)
round(6 / 40 + 6 / 60, 9)
round(valley_flight_hours(12), 9)
round(12 / 40 + 12 / 60, 9)
```

```solution
def valley_flight_hours(distance):
    """Return the hours to fly distance km up the valley at 40 km/h and back at 60 km/h."""
    return distance / 24
---
Adding the tops and the bottoms, $\frac{d + d}{40 + 60}$, is not how
fractions add. It is a reasonable guess, since it is how we might add
two scores out of 40 and 60, but fractions of an hour add differently.
Give them a common denominator, 120, first:

$$\frac{d}{40} + \frac{d}{60} = \frac{3d}{120} + \frac{2d}{120} = \frac{5d}{120} = \frac{d}{24}$$

For a 12 km valley, Schlomo's version gave 0.24 hours, and the long
form gives half an hour. The table compares the short form with the
long form at three distances, which is a quick way to check any
simplifying.
```

**12. Make.** On a disk of $x$ GB, one program uses a third of the
space, and another uses a sixth. Write $\frac{x}{3} + \frac{x}{6}$ as
one fraction, and simplify it. What part of the disk is still free?
Check your answer with code for a 512 GB disk and a 1,000 GB disk.

<details class="dl-answer"><summary>answer</summary>

The common denominator is 6:

$$\frac{x}{3} + \frac{x}{6} = \frac{2x}{6} + \frac{x}{6} = \frac{3x}{6} = \frac{x}{2}$$

So between them they use half the disk, and half is still free.

```python
for disk in [512, 1000]:
    print(disk, disk / 3 + disk / 6, disk / 2)
```

This prints `512 256.0 256.0` and `1000 500.0 500.0`. The long form and
the short form agree.

</details>

## Stretch

A cell for the stretch problems.

```python exec
id: running-a-practice-stretch
# Your working for problems 13 to 16
```

**13. Make.** In the tutorial, the drone's round trip at 20 km/h and
30 km/h had an average speed of 24 km/h. Show that, for any speeds $a$ there and $b$
back, the average speed is $\frac{2ab}{a + b}$. Then write
`round_trip_speed(there, back)` and test it against the travel tools for
20 and 30, and for 40 and 60.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The whole trip takes $\frac{d}{a} + \frac{d}{b}$ hours.
2. Use $ab$ as the common denominator.
3. The whole distance is $2d$. Divide it by the whole time, and watch
   the $d$ cancel.

**Think about:** what happens to the average if $b$ is very small, like
a flight back at 1 km/h against a gale?

</details>

<details class="dl-answer"><summary>answer</summary>

$$\frac{d}{a} + \frac{d}{b} = \frac{bd}{ab} + \frac{ad}{ab} = \frac{(a + b)d}{ab}$$

$$\text{average} = 2d \div \frac{(a + b)d}{ab} = 2d \times \frac{ab}{(a + b)d} = \frac{2ab}{a + b}$$

```python
def round_trip_speed(there, back):
    """Return the average speed of a trip out at there km/h and back at back km/h."""
    return 2 * there * back / (there + back)


for there, back in [(20, 30), (40, 60)]:
    distance = 10
    whole_time = travel_time(distance, there) + travel_time(distance, back)
    print(round_trip_speed(there, back), speed(2 * distance, whole_time))
```

This prints `24.0 24.000000000000004`, then
`48.0 48.00000000000001`. The formula and the travel tools agree, apart
from a tiny float difference in the last digits. With a flight back at
1 km/h, the average stays under 2 km/h however fast the trip out was, because the slow part takes up almost
all the time.

</details>

**14. Another way.** Scientists use the Kelvin scale:
$K = C + 273.15$. Write `celsius_to_kelvin` and `kelvin_to_celsius`.
Then use `compose` to make `fahrenheit_to_kelvin` from two functions you
already have. Finally, make its inverse, `kelvin_to_fahrenheit`, by
composing the two inverses. In which order do they go?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Fahrenheit to Kelvin takes two steps: first
   `fahrenheit_to_celsius`, then `celsius_to_kelvin`.
2. `compose(outer, inner)` runs `inner` first.
3. Going back, undo the last step first.

**Think about:** socks and shoes, one more time.

</details>

<details class="dl-answer"><summary>answer</summary>

Here is one answer. Yours may be different and work too.

```python
def celsius_to_kelvin(celsius):
    """Return a temperature in kelvin, given it in degrees Celsius."""
    return celsius + 273.15


def kelvin_to_celsius(kelvin):
    """Return a temperature in degrees Celsius, given it in kelvin. Undoes celsius_to_kelvin."""
    return kelvin - 273.15


fahrenheit_to_kelvin = compose(celsius_to_kelvin, fahrenheit_to_celsius)
kelvin_to_fahrenheit = compose(celsius_to_fahrenheit, kelvin_to_celsius)

print(fahrenheit_to_kelvin(32))
print(kelvin_to_fahrenheit(273.15))
print(round(kelvin_to_fahrenheit(fahrenheit_to_kelvin(98.6)), 9))
```

This prints `273.15`, `32.0` and `98.6`. Going forwards, the Celsius
step comes first and the Kelvin step second. Going back, the Kelvin step
is undone first, so `kelvin_to_celsius` is the inner function. The
inverse of a composition is the inverses, composed in reverse order.

</details>

<aside class="dl-note" id="running-practice-note-kelvin">

**A scale named after a river.** The Kelvin scale is named after
William Thomson, who was born in Belfast in 1824. He was a professor at
the University of Glasgow for 53 years. When he became a lord in 1892,
he took his title from the River Kelvin, which runs past the
university. So the kelvin, a unit of temperature, has the name of a
river in Scotland.

</aside>

**15. Make.** A bus goes from Dublin to Athlone, about 120 km, at an
average of 100 km/h, then from Athlone to Galway, about 88 km, at
80 km/h. Use
`travel_time` and `total` to find the time for the whole trip, then
`speed` to find the average speed for the whole trip. Is it the average
of 100 and 80?

<details class="dl-answer"><summary>answer</summary>

```python
leg_times = [travel_time(120, 100), travel_time(88, 80)]
whole_time = total(leg_times)
print(whole_time)
print(speed(120 + 88, whole_time))
```

This prints `2.3`, then about `90.43`. The trip takes 2.3 hours,
which is 2 hours and 18 minutes. The average speed is about
90.43 km/h, not 90. The two legs are different lengths and take
different times, so the speeds do not count equally.

</details>

**16. Make.** A person's body mass index is
$\text{BMI} = \frac{\text{mass}}{\text{height}^2}$, with mass in kg and
height in metres. What mass gives a BMI of 25 for someone 1.75 m tall?
Then rearrange the formula to make height the subject, and say which
space you need the square root in.

<details class="dl-answer"><summary>answer</summary>

Multiply both sides by $\text{height}^2$:
$\text{mass} = \text{BMI} \times \text{height}^2$. For a BMI of 25 at
1.75 m:

```python
import math

mass = 25 * 1.75 ** 2
print(mass)
print(math.sqrt(mass / 25))
```

This prints `76.5625`, then `1.75`. For height, divide both sides of
$\text{mass} = \text{BMI} \times \text{height}^2$ by BMI, then take the
square root:

$$\text{height} = \sqrt{\frac{\text{mass}}{\text{BMI}}}$$

Both $1.75$ and $-1.75$ square to $3.0625$, but a height is a length,
and lengths are never negative. In the space of numbers from 0 upwards,
the square root gives the one answer. And a BMI of 0 would divide by
zero, so the rearranged formula needs a BMI above 0.

</details>

**17. Explain.** Many people learned "change sides,
change signs" at school. The tutorial page used "the same move on both
sides" instead. Take $F = \frac{9}{5}C + 32$ and make $C$ the subject, once
each way. Then say which way you would teach to someone meeting
rearranging for the first time, and why.

<details class="dl-answer"><summary>answer</summary>

**The same move on both sides.** Subtract 32 from both sides:
$F - 32 = \frac{9}{5}C$. Then multiply both sides by $\frac{5}{9}$:
$C = \frac{5}{9}(F - 32)$.

**Change sides, change signs.** The $+32$ moves across and becomes
$-32$: $F - 32 = \frac{9}{5}C$. Then the "times $\frac{9}{5}$" moves
across and becomes "divide by $\frac{9}{5}$", which is the same as
multiplying by $\frac{5}{9}$: $C = \frac{5}{9}(F - 32)$.

Both give the same answer. Substitute it back to check:

```python
fahrenheit = 68
print((fahrenheit - 32) * 5 / 9)
```

It shows `20.0`.

There is more than one good answer to which one to teach. Here are some
things to weigh. The short rule is quick, and many people use it well. But it does
not say which part moves first. A common slip is to move the
$\frac{9}{5}$ first, and get $C = \frac{5}{9}F - 32$, which turns −76 °F into about −74.2 °C, not −60. The balance is slower, but
you can say each step out loud. One
answer might teach the balance first, and then show the short rule as the
balance with the middle steps left out.

</details>
