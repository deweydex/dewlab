---
title: "Running a formula backwards: rearranging and inverses — Practice"
practice_for: running-a-formula-backwards
year: "2026-2027"
version: 2026.09.24.1
---

# Running a formula backwards: rearranging and inverses — Practice

Each problem says what kind it is. **Predict** means guess first, then
run. **Make** means write something new. **Fix** means find one mistake
in code that looks fine. **Explain** means answer in words. **Another
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

**1. Predict.** A coach travels at 100 km/h for 2.5 hours. A car covers
150 km at 60 km/h. A runner finishes a half marathon, 21.1 km, in 2
hours. What does each line print?

```python
print(distance_travelled(100, 2.5))
print(travel_time(150, 60))
print(speed(21.1, 2))
```

<details class="dl-answer"><summary>answer</summary>

`250.0`, `2.5` and `10.55`.

The coach goes $100 \times 2.5 = 250$ km. The car takes
$\frac{150}{60} = 2.5$ hours. The runner's average speed is
$\frac{21.1}{2} = 10.55$ km/h. Each line uses a different form of the
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

Going forwards, the last step is "add 32". Undoing works from the last
step back to the first, the way you take off your shoes before your
socks. So the first step back is "subtract 32", and the step after it
undoes the multiplying. If we multiplied first, the 32 would still be
mixed in with the number we multiply, and we would get the wrong answer.

</details>

**4. Predict.** In the novel *Fahrenheit 451*, 451 °F is the
temperature at which paper burns. What do these two lines print? Will
the second one give back exactly 451?

```python
print(fahrenheit_to_celsius(451))
print(celsius_to_fahrenheit(fahrenheit_to_celsius(451)))
```

<details class="dl-answer"><summary>answer</summary>

`232.77777777777777`, then `451.0`.

The round trip gives back exactly 451 this time. Sometimes a float round
trip lands exactly, and sometimes it lands very close, like the
`0.9999999999999984` for 1 °C in the tutorial. That is why a good test
of a round trip rounds first, or asks "close enough?".

</details>

## Core

A cell for the core problems.

```python exec
id: running-a-practice-core
# Your working for problems 5 to 12
```

**5. Make.** On a trip to New York, one euro buys 1.08 US dollars.
Write `euro_to_dollars(euro)` and its inverse, `dollars_to_euro(dollars)`.
Test each with a known value, then test the round trip for €50, €200 and
€1,234.56.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Going forwards, dollars $=$ euro $\times 1.08$.
2. Rearrange for euro: which move undoes "multiply by 1.08"?
3. For the round trip, round to 9 places before comparing, as the
   tutorial did.

**Think about:** why a known value like €50 $=$ \$54 is a better first
test than a round trip.

**Try this next:** a bureau de change adds a €3 fee before converting.
Which step does the inverse undo first?

</details>

<details class="dl-answer"><summary>answer</summary>

```python
def euro_to_dollars(euro):
    """Return the US dollars bought with euro, at 1.08 dollars per euro."""
    return euro * 1.08


def dollars_to_euro(dollars):
    """Return the euro that buy dollars, at 1.08 dollars per euro. Undoes euro_to_dollars."""
    return dollars / 1.08


assert round(euro_to_dollars(50), 9) == 54
assert round(dollars_to_euro(54), 9) == 50
for euro in [50, 200, 1234.56]:
    assert round(dollars_to_euro(euro_to_dollars(euro)), 9) == euro
print("The converter works both ways.")
```

It prints `The converter works both ways.` A known value checks the
rate. A round trip checks that the two functions undo each other, and
it would still pass if both used the wrong rate. The two kinds of test
catch different mistakes.

</details>

**6. Fix.** A health app turns a temperature taken in Fahrenheit into
Celsius. A fever of 100.4 °F should be 38 °C, but the app says about
82.6. Run the tests, find the mistake, and fix it.

```python exec
id: running-a-practice-fix-fever
def to_celsius(fahrenheit):
    """Return a temperature in degrees Celsius, given it in degrees Fahrenheit."""
    return fahrenheit - 32 * 5 / 9

assert round(to_celsius(32), 9) == 0
assert round(to_celsius(100.4), 9) == 38
print("All tests pass.")
```

<details class="dl-answer"><summary>answer</summary>

The first test fails with an `AssertionError`. Python multiplies before
it subtracts, so `fahrenheit - 32 * 5 / 9` takes away $\frac{160}{9}$,
about 17.8, and never subtracts 32 at all. Brackets make the subtraction
happen first:

```python
def to_celsius(fahrenheit):
    """Return a temperature in degrees Celsius, given it in degrees Fahrenheit."""
    return (fahrenheit - 32) * 5 / 9
```

Now both tests pass. The formula $C = \frac{5}{9}(F - 32)$ has the
brackets too, for the same reason.

</details>

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

**8. Make.** One cookbook's rule for roasting a turkey is 40 minutes for
each kilogram, plus 20 minutes. The oven is free for 4 hours. What is
the heaviest turkey that will be ready in time? Write the rule, run it
backwards, and check.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Forwards: minutes $= 40 \times$ kg $+ 20$. Two steps: multiply, then
   add.
2. Backwards, undo the last step first.
3. Four hours is how many minutes?

**Think about:** which step did the temperature formula undo first, and
why is this the same?

</details>

<details class="dl-answer"><summary>answer</summary>

$m = 40k + 20$. Subtract 20 from both sides, then divide both sides by
40:

$$k = \frac{m - 20}{40}$$

```python
def roasting_minutes(kilograms):
    """Return the roasting time in minutes for a turkey of kilograms."""
    return 40 * kilograms + 20


def heaviest_turkey(minutes):
    """Return the heaviest turkey, in kg, that roasts in minutes. Undoes roasting_minutes."""
    return (minutes - 20) / 40


print(heaviest_turkey(4 * 60))
print(roasting_minutes(heaviest_turkey(240)))
```

This prints `5.5`, then `240.0`. A turkey of 5.5 kg takes exactly 4
hours.

</details>

**9. Explain.** A car park charges €3 for every hour or part of an hour:
20 minutes costs €3, and 61 minutes costs €6. Your ticket says you paid
€6. Can you work out exactly how long you parked? What does this say
about running the charge backwards?

<details class="dl-answer"><summary>answer</summary>

No. Every stay from just over 60 minutes up to 120 minutes costs €6, so
€6 only tells you the stay was somewhere in that hour. Many inputs give
the same output, so the charge is not one-to-one, and it has no inverse.
The best a way back can do is give a range of times. Like `round()`, the
charge throws information away, and nothing can bring it back.

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

**11. Fix.** A hill-walking app times a walk of $d$ km as $\frac{d}{4}$
hours up at 4 km/h and $\frac{d}{6}$ hours down at 6 km/h. Someone wrote
the total as one fraction by adding the tops and adding the bottoms. Run
the test, then fix the function.

```python exec
id: running-a-practice-fix-hill
def hill_walk_hours(distance):
    """Return the hours to walk distance km up at 4 km/h and back down at 6 km/h."""
    return 2 * distance / 10

for distance in [3, 6, 12]:
    assert round(hill_walk_hours(distance), 9) == round(distance / 4 + distance / 6, 9)
print("The walk time is right.")
```

<details class="dl-answer"><summary>answer</summary>

Adding the tops and the bottoms, $\frac{d + d}{4 + 6}$, is not how
fractions add. Give them a common denominator, 12, first:

$$\frac{d}{4} + \frac{d}{6} = \frac{3d}{12} + \frac{2d}{12} = \frac{5d}{12}$$

```python
def hill_walk_hours(distance):
    """Return the hours to walk distance km up at 4 km/h and back down at 6 km/h."""
    return 5 * distance / 12
```

Now the test prints `The walk time is right.` For a 12 km walk, the
wrong version gave 2.4 hours, and the right one gives 5 hours. The test
compared the short form against the long form at three distances, which
is a quick way to check any simplifying.

</details>

**12. Make.** Two friends split a bill of $x$ euro. One pays a third of
it, and the other pays a sixth. Write $\frac{x}{3} + \frac{x}{6}$ as one
fraction, and simplify it. What part of the bill is still unpaid? Check
your answer with code for a bill of €84 and a bill of €150.

<details class="dl-answer"><summary>answer</summary>

The common denominator is 6:

$$\frac{x}{3} + \frac{x}{6} = \frac{2x}{6} + \frac{x}{6} = \frac{3x}{6} = \frac{x}{2}$$

So between them they pay half the bill, and half is still unpaid.

```python
for bill in [84, 150]:
    print(bill, bill / 3 + bill / 6, bill / 2)
```

This prints `84 42.0 42.0` and `150 75.0 75.0`. The long form and the
short form agree.

</details>

## Stretch

A cell for the stretch problems.

```python exec
id: running-a-practice-stretch
# Your working for problems 13 to 16
```

**13. Make.** In the tutorial, a round trip at 20 km/h and 30 km/h had
an average speed of 24 km/h. Show that, for any speeds $a$ there and $b$
back, the average speed is $\frac{2ab}{a + b}$. Then write
`round_trip_speed(there, back)` and test it against the travel tools for
20 and 30, and for 40 and 60.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The whole trip takes $\frac{d}{a} + \frac{d}{b}$ hours.
2. Use $ab$ as the common denominator.
3. The whole distance is $2d$. Divide it by the whole time, and watch
   the $d$ cancel.

**Think about:** what happens to the average if $b$ is very small, like
a walk back at 1 km/h?

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
from a tiny float difference in the last digits. With a walk back at 1 km/h, the average stays under 2 km/h
however fast the trip out was, because the slow part takes up almost
all the time.

</details>

**14. Another way.** Scientists use the Kelvin scale:
$K = C + 273.15$. Write `celsius_to_kelvin` and `kelvin_to_celsius`.
Then use `compose` to make `fahrenheit_to_kelvin` from two functions you
already have. Finally, make its inverse, `kelvin_to_fahrenheit`, by
composing the two inverses. In which order do they go?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Fahrenheit to Kelvin goes through Celsius: first
   `fahrenheit_to_celsius`, then `celsius_to_kelvin`.
2. `compose(outer, inner)` runs `inner` first.
3. Going back, undo the last step first.

**Think about:** socks and shoes, one more time.

</details>

<details class="dl-answer"><summary>answer</summary>

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

**15. Make.** A bus goes from Dublin to Athlone, 125 km, at an average
of 100 km/h, then from Athlone to Galway, 95 km, at 80 km/h. Use
`travel_time` and `total` to find the time for the whole trip, then
`speed` to find the average speed for the whole trip. Is it the average
of 100 and 80?

<details class="dl-answer"><summary>answer</summary>

```python
leg_times = [travel_time(125, 100), travel_time(95, 80)]
whole_time = total(leg_times)
print(whole_time)
print(speed(125 + 95, whole_time))
```

This prints `2.4375`, then about `90.26`. The trip takes 2.4375 hours,
which is 2 hours and about 26 minutes. The average speed is about
90.26 km/h, not 90. The two legs are different lengths and take
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
