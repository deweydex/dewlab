---
title: "Code other people can read: reviewing your toolkit — Practice"
practice_for: code-other-people-can-read
year: "2026-2027"
version: 2026.09.24.1
---

# Code other people can read: reviewing your toolkit — Practice

Each problem says what kind it is. **Predict** means guess first, then
run. **Make** means write something new. **Fix** means find one mistake
in code that looks fine. **Explain** means answer in words. **Another
way** means reach the same place by a second route. The answers are
folded away until you open them.

Your toolkit is loaded on this page. The tutorial's `quick_review` and
`check_median_tool` are not: they were page cells, so a problem that
needs one gives it again.

## Warm-up

Use this cell for any of the warm-up problems.

```python exec
id: code-other-practice-warm-up
# Try things here
```

**1. Predict.** A music app has this function. What do the last two
lines print? Is there a side effect, and would a stranger expect it
from the name?

```python
def add_track(playlist, track):
    playlist.append(track)
    return len(playlist)

morning = ["Dreams", "Zombie"]
count = add_track(morning, "Linger")
print(count)
print(morning)
```

<details class="dl-answer"><summary>answer</summary>

It prints `3`, then `['Dreams', 'Zombie', 'Linger']`.

`append` changes the list that `morning` points at, so the function has
a side effect. Here the name says "add", so a stranger would probably
expect the playlist to change. The function also gives back the new
length, which the name does not say. A docstring should say both:

```python
def add_track(playlist, track):
    """Put track at the end of playlist, and return how many tracks it now has.

    playlist is changed.
    """
    playlist.append(track)
    return len(playlist)
```

</details>

**2. Make.** A café works out a week's pay like this. The numbers are
made up. Rewrite it with a name that says what it gives, a docstring,
and a named constant for each magic number. Then check with `assert`
that your version agrees with this one for 0, 8, 22.5 and 39 hours.

```python
def pay(hours):
    return hours * 13.5 + 20
```

(The €20 is a weekly travel allowance.)

<details class="dl-answer"><summary>answer</summary>

```python
HOURLY_RATE = 13.50
TRAVEL_ALLOWANCE = 20


def weekly_pay(hours):
    """Return a week's pay in euro for hours worked, with the travel allowance added."""
    return hours * HOURLY_RATE + TRAVEL_ALLOWANCE


def pay(hours):
    return hours * 13.5 + 20


for hours in [0, 8, 22.5, 39]:
    assert weekly_pay(hours) == pay(hours), hours
print(weekly_pay(22.5))
```

It prints `323.75`. When the rate goes up, one line at the top changes,
and a stranger can find it.

</details>

**3. Explain.** A reviewer leaves this comment on a classmate's code:
"This is a mess. Who names a variable `x2`?" Rewrite it as a useful
review comment. What makes yours more useful?

<details class="dl-answer"><summary>answer</summary>

One possible comment: "In `score_round`, `x2` holds the player's second
throw. Could it be `second_throw`? I had to read the whole loop to find
out what it was."

It is more useful because it says what the reviewer saw, why it
mattered (they had to read the whole loop), and what they suggest. It
is about the code, not the person, so the writer can act on it without
feeling judged.

</details>

**4. Predict.** What does this cell show? Which part comes from the
docstring?

```python
def bus_fare(age):
    """Return the fare in euro for one bus trip, given the rider's age in years.

    Children under 5 travel free.
    """
    if age < 5:
        return 0
    return 2

help(bus_fare)
```

<details class="dl-answer"><summary>answer</summary>

`help()` shows the line `bus_fare(age)`, then the two lines of the
docstring under it. Everything after the first line is the docstring.
The fares are made up. The docstring tells a stranger the unit (euro),
what `age` is measured in (years), and the edge (under 5 is free), all
without reading the code.

</details>

## Core

A cell for the core problems.

```python exec
id: code-other-practice-core
import doctest
# Your working for problems 5 to 12
```

**5. Fix.** A weather app counts rainy days. The test fails. Is the
mistake in the code, the docstring, or the test? Fix it.

```python exec
id: code-other-practice-fix-rain
def rainy_days(readings):
    """Return how many days had more than 1 mm of rain.

    readings is a list of daily rainfall in millimetres. It is not changed.
    """
    count = 0
    for millimetres in readings:
        if millimetres > 0:
            count = count + 1
    return count

assert rainy_days([0, 0.2, 1.5, 3, 0]) == 2, "only 1.5 and 3 are more than 1 mm"
print("rainy_days keeps its promise.")
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Work out by hand how many of the five readings are more than 1 mm.
2. Run the function on the same list with `print`. What does it give?
3. The docstring and the test agree with each other. Which line of the
   code disagrees with them?

**Think about:** when code and its docstring disagree, how do you
decide which one is the promise?

</details>

<details class="dl-answer"><summary>answer</summary>

The code is wrong. It counts every day with any rain at all, so it
gives 3: 0.2, 1.5 and 3. The docstring and the test both say "more than
1 mm". The fix is one line:

```python
        if millimetres > 1:
```

Now it gives 2, and the test passes. The docstring was written as the
promise, and the test agrees with it, so the code is the part to change.

</details>

**6. Predict.** A fitness app turns steps into kilometres. Which of the
three examples in the docstring will `doctest` report, if any? Run it
to check.

```python
import doctest

def steps_to_km(steps, stride_cm=75):
    """Return the distance walked in kilometres.

    >>> steps_to_km(10000)
    7.5
    >>> steps_to_km(4000, stride_cm=60)
    2.4
    >>> steps_to_km(0)
    0
    """
    return steps * stride_cm / 100000

doctest.run_docstring_examples(steps_to_km, globals(), name="steps_to_km")
```

<details class="dl-answer"><summary>answer</summary>

Only the third. The report says it expected `0` and got `0.0`. The `/`
always gives a float, and `doctest` compares the text Python prints,
not the number. The number is right; the example is written wrong. The
fix is to write `0.0` in the docstring.

</details>

**7. Make.** A restaurant's till has this function. It adds VAT at 23%
and, when asked, a 10% service charge. Review it with the checklist,
then rewrite it. Test that your version gives the same answers as this
one for several prices, with and without the service charge.

```python
def t(a,b):
    x=a*1.23
    if b==True:
        x=x+x*0.1
    return round(x,2)
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Say in one sentence what `t` gives back. That sentence is the start
   of your docstring and a clue to the name.
2. Give 1.23 and 0.1 names at the top, in capitals.
3. Keep each step in the same order as the original, so the floats
   round the same way.
4. Loop over a list of prices and over `[False, True]`, and `assert`
   that both versions agree.

**Think about:** why `b==True` can be written as just `b`.

</details>

<details class="dl-answer"><summary>answer</summary>

Review findings: the names `t`, `a`, `b` and `x` say nothing; there is
no docstring; 1.23 and 0.1 are magic numbers; `b==True` can be `b`; and
there are no spaces round `=` and `*`.

```python
VAT_MULTIPLIER = 1.23      # adds VAT at 23%
SERVICE_CHARGE = 0.10


def price_to_pay(price_before_vat, add_service=False):
    """Return the price in euro with VAT added, rounded to the cent.

    With add_service True, a service charge is added after the VAT.
    """
    price = price_before_vat * VAT_MULTIPLIER
    if add_service:
        price = price + price * SERVICE_CHARGE
    return round(price, 2)


def t(a,b):
    x=a*1.23
    if b==True:
        x=x+x*0.1
    return round(x,2)


for price in [0, 10, 18.5, 42, 99.99]:
    for add_service in [False, True]:
        assert price_to_pay(price, add_service) == t(price, add_service), price
print(price_to_pay(42, True))
```

It prints `56.83`. The steps are in the same order as the original, so
the answers match to the cent.

</details>

**8. Explain.** `quick_review` flags the names `gf` and `ga` in this
function. In the tutorial, we kept `p` and `q` in `slope`. Should `gf`
and `ga` be kept too? Why or why not?

```python
def goal_difference(gf, ga):
    """Return goals scored minus goals let in."""
    return gf - ga
```

<details class="dl-answer"><summary>answer</summary>

They should change, to `goals_for` and `goals_against`. `p` and `q`
match the maths written above `slope`, where two points are called $p$
and $q$. `gf` and `ga` come from no formula. They are short forms a
stranger has to decode, and the docstring does not say what they stand
for. The linter's note is the same in both cases; the reason behind the
name is what differs, and only a person can judge that.

</details>

**9. Fix.** Someone refactored a game's `best_score`. The tests were
written before the change, and one now fails. Find the mistake and fix
it.

```python exec
id: code-other-practice-fix-score
def best_score(scores):
    """Return the highest score in scores, a list of at least one number.

    The list is not changed.
    """
    in_order = sorted(scores)
    return in_order[0]

assert best_score([40, 95, 70]) == 95
assert best_score([7]) == 7
assert best_score([-3, -8]) == -3
print("best_score keeps its promise.")
```

<details class="dl-answer"><summary>answer</summary>

`sorted()` puts the smallest first, so `in_order[0]` is the lowest
score. The highest is the last one:

```python
    return in_order[-1]
```

Then all three tests pass. The one-value test passed even with the
mistake, because the smallest and largest of `[7]` are the same. That
is why a test suite needs more than one test case.

</details>

**10. Another way.** Here is a function for a playlist's length. Write
a second version, `playlist_minutes_again`, using `total` from your
toolkit. Test that the two agree on three playlists, including an empty
one. Which would a reviewer rather read?

```python
def playlist_minutes(track_seconds):
    """Return the length of a playlist in minutes, given each track's length in seconds."""
    seconds = 0
    for length in track_seconds:
        seconds = seconds + length
    return seconds / 60
```

<details class="dl-answer"><summary>answer</summary>

```python
def playlist_minutes_again(track_seconds):
    """Return the length of a playlist in minutes, given each track's length in seconds."""
    return total(track_seconds) / 60


for tracks in [[210, 185, 240], [], [3600]]:
    assert playlist_minutes(tracks) == playlist_minutes_again(tracks), tracks
print(playlist_minutes_again([210, 185, 240]))
```

It prints `10.583333333333334`. Most reviewers would pick the second:
it is one line, and `total` is a tool the team has already tested. The
first shows every step, which is useful while you are learning, and
repeats work the toolkit already does.

</details>

**11. Make.** Write a docstring for this function that says all four
things: what comes out, what must go in, the edges, and an example.
Make the example one that `doctest` can run: 210 km in a car that uses
6 litres per 100 km, with fuel at €1.75 a litre. Run `doctest` to check
it.

```python
def travel_cost(km, litres_per_100km, price_per_litre):
    return round(km * litres_per_100km / 100 * price_per_litre, 2)
```

<details class="dl-answer"><summary>answer</summary>

One possible docstring:

```python
def travel_cost(km, litres_per_100km, price_per_litre):
    """Return the fuel cost in euro of a car trip, rounded to the cent.

    km is the length of the trip in kilometres, litres_per_100km is
    the car's fuel use, and price_per_litre is in euro. All are 0 or
    more. Nothing outside the function is changed.

    >>> travel_cost(210, 6, 1.75)
    22.05
    """
    return round(km * litres_per_100km / 100 * price_per_litre, 2)


doctest.run_docstring_examples(travel_cost, globals(), name="travel_cost")
```

`doctest` shows nothing, which means the example passed. The trip uses
12.6 litres, and 12.6 × 1.75 is €22.05.

</details>

**12. Explain.** This currency converter works when the page first
runs. Which question from the review checklist does it fail, and what
could go wrong later? Write the review comment you would leave.

```python
rate = 0.85

def to_sterling(euro):
    """Return an amount in pounds sterling, given it in euro."""
    return round(euro * rate, 2)
```

<details class="dl-answer"><summary>answer</summary>

It fails the fourth question, "what does this space let us do?". The
function needs `rate`, and it takes it from outside, a hidden input. If
any other cell later sets `rate` to something else, for example a
dollar rate, `to_sterling` quietly gives wrong answers, and its own
code looks fine.

A review comment: "`to_sterling` reads `rate` from the page. Could the
rate come in as a parameter, `rate=0.85`, so the function says what it
needs and a test can check it?" The 0.85 is an example rate, not
today's.

</details>

## Stretch

A cell for the stretch problems. It holds `quick_review` from the
tutorial, so you can change it.

```python exec
id: code-other-practice-stretch
def quick_review(function):
    """Return a list of notes on function, the way a small linter would."""
    notes = []
    if not function.__doc__:
        notes.append("no docstring")
    code = function.__code__
    for name in code.co_varnames:    # every input and every name made inside
        if len(name) < 3:
            notes.append("short name " + name)
    if "print" in code.co_names:
        notes.append("uses print")
    return notes
```

**13. Make.** `function.__code__.co_consts` holds the fixed values a
function uses: its numbers, its strings, `True` and `None`. Add a check
to `quick_review` that notes every number in it except 0, 1 and −1, as
a possible magic number. Try it on `t` from problem 7. Is every number
it finds really a magic number?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Print `t.__code__.co_consts` first, to see what is in it.
2. Loop over it. `type(value) in (int, float)` is True only for
   numbers, and False for `True`, `None` and strings.
3. Skip 0, 1 and −1, and add a note for the rest.

**Think about:** why `True` is not caught, even though `True == 1`.

</details>

<details class="dl-answer"><summary>answer</summary>

Add this before `return notes`:

```python
    for value in code.co_consts:
        if type(value) in (int, float) and value not in (0, 1, -1):
            notes.append("number " + str(value))
```

For `t` it gives `['no docstring', 'short name a', 'short name b',
'short name x', 'number 1.23', 'number 0.1', 'number 2']`. The first
two numbers are magic numbers. The 2 is from `round(x, 2)`, "to the
cent", which a reader of money code understands without a name. The
tool finds places to look; a person decides. `True` is left out
because its type is `bool`, not `int`.

</details>

**14. Another way.** Problem 6 checked `steps_to_km` with `doctest`.
Check the same promise a second way: write its three examples as
`assert` lines, with `close_enough`. Which way would you rather find in a stranger's code,
and why?

<details class="dl-answer"><summary>answer</summary>

```python
def steps_to_km(steps, stride_cm=75):
    """Return the distance walked in kilometres."""
    return steps * stride_cm / 100000


assert close_enough(steps_to_km(10000), 7.5)
assert close_enough(steps_to_km(4000, stride_cm=60), 2.4)
assert close_enough(steps_to_km(0), 0)
print("steps_to_km keeps its promise.")
```

Both check the same three cases. The `assert` lines compare numbers,
so `0` and `0.0` agree, and `close_enough` forgives float rounding.
`doctest` compares printed text, which is stricter, but its examples
sit in the docstring, where a stranger reads them with `help()`. Many
teams keep a few examples in the docstring and the full tests
elsewhere.

</details>

**15. Explain.** The tutorial taught reviewing with a function written
badly on purpose, and gave the coding rules afterwards. Would you have
taught the rules first? Say which way you would choose, and why.

<details class="dl-answer"><summary>answer</summary>

A good answer weighs both sides. Rules first gives a reader the
standard before they write anything, so they build good habits from
the start, and it is how a standard arrives in most jobs. A bad
function first lets a reader feel the problem each rule solves, so the
rules make sense, but it asks them to read messy code before they know
what to look for. A good answer might also say who the reader is: a
person who has written code for a while may get more from the bad
function, and a person starting out may want the rules. Either choice
is fine if the reasons are there.

</details>

**16. Make.** This function turns amounts of red, green and blue into
a web colour code, using `to_hex` from
[Everything is ones and zeros](tutorial:everything-is-ones-and-zeros).
It works. Review it, then refactor it so that the repeated steps are
written once, in a helper function. Test that your version agrees with
this one on many colours.

```python
def c(r,g,b):
    x=to_hex(r)
    if len(x)==1: x="0"+x
    y=to_hex(g)
    if len(y)==1: y="0"+y
    z=to_hex(b)
    if len(z)==1: z="0"+z
    return "#"+x+y+z
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The same two lines appear three times. What do they do to one
   amount? That is the helper's job, and its name.
2. Write the helper with a docstring, then the main function, which
   calls it three times.
3. Test with three nested loops over a few values each. Include 0, 9,
   10 and 255: they sit at the edges of one and two hex digits.

**Think about:** what would you have to change in `c` if a colour
code ever needed lower-case letters? And in yours?

</details>

<details class="dl-answer"><summary>answer</summary>

```python
def two_hex_digits(amount):
    """Return amount, a whole number from 0 to 255, as two hex digits."""
    digits = to_hex(amount)
    if len(digits) == 1:
        digits = "0" + digits
    return digits


def colour_code(red, green, blue):
    """Return a web colour code like "#FF8800" for amounts of red, green and blue.

    Each amount is a whole number from 0 to 255.
    """
    return "#" + two_hex_digits(red) + two_hex_digits(green) + two_hex_digits(blue)


def c(r,g,b):
    x=to_hex(r)
    if len(x)==1: x="0"+x
    y=to_hex(g)
    if len(y)==1: y="0"+y
    z=to_hex(b)
    if len(z)==1: z="0"+z
    return "#"+x+y+z


checked = 0
for red in range(0, 256, 15):
    for green in range(0, 256, 17):
        for blue in [0, 9, 10, 128, 255]:
            assert colour_code(red, green, blue) == c(red, green, blue)
            checked = checked + 1
print(checked, "colours agree.", colour_code(255, 136, 0))
```

It prints `1440 colours agree. #FF8800`. A change to how one amount
becomes two digits now happens in one place, not three.

</details>
