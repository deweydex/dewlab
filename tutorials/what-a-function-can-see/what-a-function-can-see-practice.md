---
title: "What a function can see: scope and parameters — Practice"
practice_for: what-a-function-can-see
year: "2026-2027"
version: 2026.09.25.2
---

# What a function can see: scope and parameters — Practice

Each problem says what kind it is: **Predict**, **Make**, **Fix**,
**Explain** or **Another way**. Many problems here ask "which space is
this name in?". It helps to point at each name and say its space out
loud: this call's own, the page's, or Python's. Your toolkit is loaded
on this page, from every earlier page.

## Warm-up

Use this cell for any warm-up problem. Paste in the code, and run it.

```python exec
id: what-function-practice-scratch-1
# Try things here
```

**1. Predict.** A weather app works out how cold the wind makes 8 °C
feel. What does each line show? One of them is an error: which one, and
which kind?

```python
def feels_like(temperature, wind_kmh):
    chill = temperature - wind_kmh / 10
    return chill

print(feels_like(8, 30))
print(chill)
```

<details class="dl-answer"><summary>answer</summary>

The first line shows `5.0`. The second stops with
`NameError: name 'chill' is not defined`.

`chill` is a local name. It was made in the space of one call to
`feels_like`, and that space was thrown away when the call ended. Only
the value 5.0 came out, through `return`. To keep it, give it a name on
the page: `chill = feels_like(8, 30)`.

(The rule here is made up to keep the numbers small. Weather services
use a longer formula for wind chill.)

</details>

**2. Predict.** A phone has a screen brightness from 0 to 10. What do
the two lines show?

```python
brightness = 5

def brighter(brightness):
    brightness = brightness + 1
    return brightness

print(brighter(brightness))
print(brightness)
```

<details class="dl-answer"><summary>answer</summary>

`6`, then `5`.

There are two names called `brightness`, in two spaces. The parameter
`brightness` lives in the call's space. It starts by pointing at 5, and
then `=` points it at 6. The page's `brightness` is a different name,
and nothing points it anywhere new. To make the page's brightness go
up, the page has to do it: `brightness = brighter(brightness)`.

</details>

**3. Predict.** A game takes away a life. What does the last line show?

```python
def lose_life(lives):
    lives = lives - 1

print(lose_life(3))
```

<details class="dl-answer"><summary>answer</summary>

`None`.

`lose_life` has no `return` line, so it gives back `None`, Python's
value for "nothing here". The 2 it worked out was in a local name, and
it was thrown away with the call's space. Adding `return lives` at the
end makes it print `2`.

</details>

**4. Make.** In a game, each enemy you stop is worth 3 points, and each
coin you pick up is worth 1. This function reads the points for an enemy
from the page. Change it so that `points_per_enemy` is a parameter with
a default value of 3. Then check that `game_score(10, 4)` is 34 and that
`game_score(10, 4, points_per_enemy=2)` is 24.

```python exec
id: what-function-practice-game-score
points_per_enemy = 3

def game_score(enemies, coins):
    """Give back a player's score for the enemies stopped and coins picked up."""
    return enemies * points_per_enemy + coins

print(game_score(10, 4))
```

<details class="dl-answer"><summary>answer</summary>

Here is one answer. Yours may be different and work too.

```python
def game_score(enemies, coins, points_per_enemy=3):
    """Give back a player's score. An enemy is worth points_per_enemy, 3 unless given."""
    return enemies * points_per_enemy + coins

assert game_score(10, 4) == 34
assert game_score(10, 4, points_per_enemy=2) == 24
print("game_score keeps its promise.")
```

A harder level of the game could give a different number of points for
an enemy. With the points as a parameter, the function can answer for
any level, and the page's `points_per_enemy` no longer matters to it.

</details>

## Core

A scratch cell for the core problems.

```python exec
id: what-function-practice-scratch-2
# Try things here
```

**5. Fix.** Schlomo, who is learning Python too, keeps his phone's
battery level on the page, and writes a function that uses some of it.
This cell should print the battery after using 2%, which is 98. As it
is, it stops with an error. Read the last line of the error, and fix the
function.

```python exec
id: what-function-practice-fix-battery
battery = 100

def use_battery(percent_used):
    battery = battery - percent_used
    return battery

print(use_battery(2))
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The error is an `UnboundLocalError`. Which name does it say is local?
2. Why is it local? Look for a line inside the function that gives it a
   value with `=`.
3. A function should get what it needs through its parameters.

**Think about:** would `global battery` fix it too? Why do most
programmers choose the other way?

**Try this next:** use your fixed function and a loop to find the
battery after five hours, using 2% an hour.

</details>

<details class="dl-answer"><summary>answer</summary>

The line `battery = battery - percent_used` gives `battery` a value
inside the function, so Python makes `battery` a local name for the
whole function. The right side then asks for the local `battery` before
it has a value. Schlomo's idea, to read the page's level, was
reasonable: a function can read a page's name. It cannot also give that
name a new value with `=`.

Take the level in as a parameter, and give the new level back:

```python
def use_battery(battery, percent_used):
    """Give back the battery level after using percent_used of it."""
    return battery - percent_used

battery = 100
battery = use_battery(battery, 2)
print(battery)
```

It prints `98`. The page's `battery` changes on a line on the page,
where a reader can see it.

</details>

**6. Explain.** Your toolkit's `travel_time(distance, speed)`, from
[Running a formula backwards](tutorial:running-a-formula-backwards),
has a parameter called `speed`. Your toolkit also has a function called
`speed`. Why do they not get in each other's way? What would happen if,
inside `travel_time`, you wrote `speed(100, 2)`?

<details class="dl-answer"><summary>answer</summary>

Inside `travel_time`, Python looks for `speed` in the call's own space
first, and finds the parameter there. So inside, `speed` means the
number that was handed in. Outside, on the page, `speed` still means the
toolkit function. Each space has its own `speed`.

Inside `travel_time`, `speed(100, 2)` would try to call a number. You
can see what that gives with a function of the same shape:

```python
def travel_time_with_a_call(distance, speed):
    return speed(100, 2)

travel_time_with_a_call(208, 80)
```

It stops with `TypeError: 'int' object is not callable`. The number 80
is not a function, and cannot be called. A local name hides a page's
name with the same spelling, for the whole function.

</details>

**7. Predict.** A pixel font is drawn on a grid of pixels. What do the
two print lines show?

```python
width = 4

def pixels_needed(rows):
    return rows * width

print(pixels_needed(7))
width = 5
print(pixels_needed(7))
```

<details class="dl-answer"><summary>answer</summary>

`28`, then `35`.

`width` is a global name, and the function reads it every time it runs,
not once when it was written. By the second call, the page's `width`
points at 5. That makes `width` a hidden input: the same call,
`pixels_needed(7)`, gave two answers. Giving the function a `width`
parameter would put everything it needs on its `def` line.

</details>

**8. Make.** Sound travels faster in warm air. A common rule says its
speed, in metres a second, is about $331 + 0.6T$, where $T$ is the air
temperature in °C. So at 20 °C it is about 343. Write
`thunder_km(seconds, celsius=20)`, which gives back how far away a
storm is, in km, from the seconds between the flash and the thunder,
rounded to two decimal places. It should need nothing from the page.
Test it with at least two `assert` lines.

```python exec
id: what-function-practice-thunder
# Your thunder_km, and its tests
```

<details class="dl-answer"><summary>answer</summary>

Here is one answer. Yours may be different and work too.

```python
def thunder_km(seconds, celsius=20):
    """Give back how far away a storm is, in km, rounded to two places.

    seconds is the time from the flash to the thunder. celsius is the air
    temperature, 20 unless given, since sound is faster in warm air.
    """
    sound_speed = 331 + 0.6 * celsius
    return round(seconds * sound_speed / 1000, 2)

assert thunder_km(3) == 1.03
assert thunder_km(3, celsius=0) == 0.99
print("thunder_km keeps its promise.")
```

At 20 °C, 3 seconds means about 1.03 km. On a freezing day the same 3
seconds mean about 0.99 km. The local name `sound_speed` is gone after
each call, and it is not needed outside.

</details>

**9. Predict.** A small robot keeps its route as a list of moves. What
does the last line show?

```python
def add_step(route):
    route.append("forward")

today = ["left", "forward"]
add_step(today)
add_step(today)
print(today)
```

<details class="dl-answer"><summary>answer</summary>

`['left', 'forward', 'forward', 'forward']`.

`route` and `today` are two names for one list. `append` changes the
list itself, so the page sees each change. Two calls add two steps.

</details>

**10. Another way.** `add_reading` on the tutorial page changes the
list it is handed. Write a second version, `with_reading(readings,
value)`, that leaves the list it was handed as it was, and gives back a
new list with the value at the end. Show that the old log did not
change.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. `+` joins two lists into a new list, the way it joins two strings.
2. `[value]` is a list with one value in it.
3. Give the new list back with `return`.

**Think about:** which of the two moves from the tutorial does your
version use, `=` or `append`?

**Try this next:** when would you want the first version, and when the
second?

</details>

<details class="dl-answer"><summary>answer</summary>

Here is one answer. Yours may be different and work too.

```python
def with_reading(readings, value):
    """Give back a new list: readings with value at the end. readings does not change."""
    return readings + [value]

old = [14.2, 14.8]
new = with_reading(old, 15.1)
print(old)
print(new)
```

The first line shows `[14.2, 14.8]` and the second
`[14.2, 14.8, 15.1]`. `readings + [value]` makes a new list, and changes
nothing that already exists.

Both versions work. `add_reading` suits a log you are building
up and mean to change. `with_reading` suits a case where you want to
keep the old list too, and it is easier to test, because everything it
does comes out through `return`.

</details>

**11. Fix.** Schlomi, who is learning Python too, is writing an
adventure game, where a backpack is a list of items. Her cell stops
with an error on the second `pick_up` line. Find the line that does not
do what Schlomi meant, and change it.

```python exec
id: what-function-practice-fix-backpack
def pick_up(backpack, item):
    """Put item into backpack. Gives nothing back."""
    backpack.append(item)

my_backpack = ["torch"]
my_backpack = pick_up(my_backpack, "key")
my_backpack = pick_up(my_backpack, "map")
print(my_backpack)
```

<details class="dl-answer"><summary>answer</summary>

The error is
`AttributeError: 'NoneType' object has no attribute 'append'`.

`pick_up` is a procedure: it gives back `None`. So the first
`my_backpack = pick_up(...)` line makes `my_backpack` point at `None`,
and the key is lost with the list. On the next line, `pick_up` is handed
`None`, and `None` has no `append`.

`pick_up` already changes the list, so there is nothing to keep. Call
it on its own:

```python
my_backpack = ["torch"]
pick_up(my_backpack, "key")
pick_up(my_backpack, "map")
print(my_backpack)
```

It prints `['torch', 'key', 'map']`. The line that failed was the
second `pick_up`, but the line responsible was the first, as on
[When Python says no](tutorial:when-python-says-no#following-the-trail-back).

</details>

**12. Explain.** Rainfall is measured in millimetres. Fill in a
trace table for this cell, with one column for the page's space
and one for the call's space. What is `week` at the end?

```python
rain_mm = 3

def double_it(rain_mm):
    rain_mm = rain_mm * 2
    return rain_mm

week = double_it(rain_mm) + rain_mm
```

<details class="dl-answer"><summary>answer</summary>

| Step | The page's space | `double_it`'s space |
|---|---|---|
| `rain_mm = 3` | `rain_mm` → 3 | (no call yet) |
| the call `double_it(rain_mm)` starts | `rain_mm` → 3 | `rain_mm` → 3 |
| `rain_mm = rain_mm * 2` | `rain_mm` → 3 | `rain_mm` → 6 |
| `return` hands 6 out | `rain_mm` → 3 | (thrown away) |
| `week = 6 + rain_mm` | `rain_mm` → 3, `week` → 9 | |

`week` is 9. The `+ rain_mm` at the end reads the page's `rain_mm`,
which is still 3. Using the same spelling for two names in two spaces is
allowed, but in a walkthrough the two are hard to tell apart, which is
one reason to choose different names.

</details>

## Stretch

A scratch cell for the stretch problems.

```python exec
id: what-function-practice-scratch-3
# Try things here
```

**13. Make.** In a drawing app, a colour's red, green and blue parts
each go from 0 to 255, as on
[Everything is ones and zeros](tutorial:everything-is-ones-and-zeros).
Write `brightener(factor)`, which gives back a function. That function
takes one part of a colour, multiplies it by `factor`, rounds it, and
gives back the answer, but never more than 255. Then use it with
`to_hex` to brighten the red part 200 by 20%, and the red part 240 by
20%.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Follow the shape of `converter` on the tutorial page: a `def` inside
   a `def`, and `return` the inner function without brackets.
2. Inside the inner function, work out the new value, then use `if` to
   bring anything over 255 down to 255.
3. `to_hex(240)` gives the two hex digits for 240.

**Think about:** which space does the inner function find `factor` in?

**Try this next:** make a `darkener` the same way, and check that 0
stays 0.

</details>

<details class="dl-answer"><summary>answer</summary>

Here is one answer. Yours may be different and work too.

```python
def brightener(factor):
    """Give back a function that brightens one colour part by factor, up to 255."""
    def brighten(part):
        new_part = round(part * factor)
        if new_part > 255:
            new_part = 255
        return new_part
    return brighten

twenty_percent = brightener(1.2)
print(twenty_percent(200), to_hex(twenty_percent(200)))
print(twenty_percent(240), to_hex(twenty_percent(240)))
```

The first line shows `240 F0`. The second shows `255 FF`, because 288
is more than a colour part can hold.

`brighten` finds `factor` in the space of the call to `brightener` it
was made in. That space stays alive as long as `twenty_percent` needs
it: `twenty_percent` is a closure.

</details>

**14. Another way.** Here are two ways to time a fall on the Moon. The
first is `fall_time` from the tutorial, with a default for gravity. The
second is a closure, in the shape of `converter`. Write the closure,
`fall_timer(gravity)`, which gives back a function of the height alone.
Then check with `close_enough` that both ways agree on the Moon, where
gravity is 1.62, for every whole-metre height from 0 to 200.

```python exec
id: what-function-practice-two-falls
import math

def fall_time(height, gravity=9.81):
    """Give back the seconds a ball takes to fall height metres, ignoring the air."""
    return math.sqrt(2 * height / gravity)

# Your fall_timer, and a loop that checks the two ways agree
```

<details class="dl-answer"><summary>answer</summary>

Here is one answer. Yours may be different and work too.

```python
def fall_timer(gravity):
    """Give back a function that times a fall of any height, at this gravity."""
    def time_for(height):
        return math.sqrt(2 * height / gravity)
    return time_for

moon_fall = fall_timer(1.62)
for height in range(0, 201):
    assert close_enough(moon_fall(height), fall_time(height, 1.62))
print("The two ways agree from 0 to 200 metres.")
```

The two ways keep gravity in different places. `fall_time` is handed it
at every call. `moon_fall` was handed it once, and keeps it in the space
it was made in. The closure is handy when one value is used many times,
or when a tool like `compose` needs a function of one input.

</details>

**15. Explain.** `travel_time` was written on another page, and it
works here. Suppose it had read its speed from a name made in a
different cell of that page, like `average_speed = 80`, instead of from
a parameter. What would happen when you called it on this page, and why?

<details class="dl-answer"><summary>answer</summary>

It would stop with a `NameError: name 'average_speed' is not defined`.

Only the toolkit cell of that page is loaded here. The other cells of
that page never run on this one, so the page's space here has no
`average_speed`. The function would look in its own space, then in this
page's space, then in Python's, and find it in none of them.

A function that needs nothing but its parameters can go anywhere. That
is why every toolkit function takes everything it needs as a parameter.

</details>

**16. Make.** Your toolkit's `simulate(trial, times)`, from
[How likely is it?](tutorial:how-likely-is-it), runs `trial()` again
and again and gives back the fraction of runs where it gave `True`. A
trial has no parameters. So how can one tool simulate a day with a 30%
chance of rain, and another with a 70% chance? Write
`chance_of(probability)`, which gives back a trial that is True with
that probability. Then simulate 10,000 days at 30% and at 70%.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. `random.random()` gives a random float from 0 up to 1, so
   `random.random() < 0.3` is True about 30% of the time.
2. Make the trial inside `chance_of`, with no parameters. It can still
   see `probability`.
3. Give the trial back without brackets, and hand it to `simulate`.

**Think about:** why can't `simulate` just pass the probability to the
trial itself?

**Try this next:** write a trial for "at least one wet day in a week of
30% days", simulate it, and compare with `at_least_one(0.3, 7)`.

</details>

<details class="dl-answer"><summary>answer</summary>

Here is one answer. Yours may be different and work too.

```python
import random

def chance_of(probability):
    """Give back a trial with no parameters that is True with this probability."""
    def trial():
        return random.random() < probability
    return trial

print(simulate(chance_of(0.3), 10000))
print(simulate(chance_of(0.7), 10000))
```

The two lines show numbers close to 0.3 and 0.7, and different on every
run, since the days are random.

`simulate` was written to call `trial()` with nothing in the brackets,
so it has no way to pass a probability in. The closure solves that: the
probability goes in once, when `chance_of` is called, and each trial
finds it in the space it was made in.

</details>
