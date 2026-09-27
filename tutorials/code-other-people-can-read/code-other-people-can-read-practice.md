---
title: "Code other people can read: reviewing your toolkit — Practice"
practice_for: code-other-people-can-read
year: "2026-2027"
version: 2026.09.26.1
---

# Code other people can read: reviewing your toolkit — Practice

Each problem says what kind it is. **Predict** means guess first, then
run. **Make** means write something new. **Fix** means find why code
that looks fine does something else, and change it. **Explain** means
answer in words. **Another way** means reach the same place by a second
route. The answers are folded away until you open them. Each is one
answer, and yours may be different and work too.

Your toolkit is loaded on this page. The tutorial's `quick_review` and
`check_median_tool` are not loaded. They were page cells, so a problem
that needs one gives it again. Schlomo and Schlomi, who are learning Python
too, wrote two of the functions below.

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
expect the playlist to change. The function also returns the new
length, which the name does not say. A docstring can say both:

```python
def add_track(playlist, track):
    """Put track at the end of playlist, and return how many tracks it now has.

    playlist is changed.
    """
    playlist.append(track)
    return len(playlist)
```

</details>

**2. Make.** A download manager calculates how long a file will take
like this. Rewrite it with names that say what goes in and what comes
out, a docstring, and a named constant for each magic number. Then
check with `assert` that your version agrees with this one for files
of 0, 5, 700 and 4,500 MB at 100 megabits a second.

```python
def dl_time(size, speed):
    return size * 8 / speed + 2
```

(A byte is 8 bits, and the 2 is the seconds it takes to connect before
anything arrives.)

<details class="dl-answer"><summary>answer</summary>

```python
BITS_PER_BYTE = 8
CONNECT_SECONDS = 2


def download_seconds(megabytes, megabits_per_second):
    """Return how many seconds a file of megabytes takes to download.

    megabits_per_second is the speed of the connection. The time
    includes the seconds it takes to connect.
    """
    return megabytes * BITS_PER_BYTE / megabits_per_second + CONNECT_SECONDS


def dl_time(size, speed):
    return size * 8 / speed + 2


for megabytes in [0, 5, 700, 4500]:
    assert download_seconds(megabytes, 100) == dl_time(megabytes, 100), megabytes
print(download_seconds(700, 100))
```

It prints `58.0`. That is about a minute for 700 MB. The name
`megabits_per_second` also answers a stranger's first question: bits or
bytes?

</details>

**3. Explain.** A reviewer leaves this comment on a classmate's game
code: "This is a mess. Who names a variable `x2`?" Rewrite it as a
review comment the writer can act on. What does yours give them that
the first did not?

<details class="dl-answer"><summary>answer</summary>

One possible comment: "In `score_round`, `x2` holds the player's second
throw. Could it be `second_throw`? I had to read the whole loop to find
what it was."

It says what the reviewer saw, why it mattered, and what they suggest.
It is about the code, not the person, so the writer can act on it
without feeling judged.

</details>

**4. Predict.** What does this cell show? Which part comes from the
docstring?

```python
def display_rows(pixels, width):
    """Return how many rows of a display pixels fill, given width pixels in each row.

    A part-filled last row counts as a row.
    """
    return (pixels + width - 1) // width

help(display_rows)
```

<details class="dl-answer"><summary>answer</summary>

`help()` shows the line `display_rows(pixels, width)`, then the two
lines of the docstring under it. Everything after the first line is the
docstring. It tells a stranger what the function counts, and the edge
that matters most: 13 pixels on a display 4 wide fill 4 rows, not 3,
because the last row is part-filled. The same row and column sums were
on [Numbers a computer can hold](tutorial:numbers-a-computer-can-hold#the-row-and-column-of-a-pixel).

</details>

## Core

A cell for the core problems.

```python exec
id: code-other-practice-core
import doctest
# Your working for problems 5 to 12
```

**5. Fix.** A weather station counts rainy days. The test stops the
cell. Which part does something different from the other two: the code,
the docstring, or the test? Change that part.

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
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Count by hand how many of the five readings are more than 1 mm.
2. Run the function on the same list with `print`. What does it give?
3. The docstring and the test agree with each other. Which line of the
   code says something else?

**Think about:** when code and its docstring disagree, how do you
decide which one is the promise?

</details>

<details class="dl-answer"><summary>answer</summary>

The code is the odd one out. It counts every day with any rain at all,
so it gives 3: 0.2, 1.5 and 3. The docstring and the test both say
"more than 1 mm". The change is one line:

```python
        if millimetres > 1:
```

Now it gives 2, the number the docstring and the test both describe.
The docstring was written as the promise, and the test agrees with it, so the code is the part to
change.

</details>

**6. Predict.** Here is `image_megabytes` from
[Does it work?](tutorial:does-it-work#names-and-comments-a-stranger-can-read),
with three examples in its docstring. Which of them will `doctest`
report, if any? Run it to check.

```python
import doctest

def image_megabytes(width, height):
    """Return the size in MB of a picture, width by height pixels, at 3 bytes a pixel.

    >>> image_megabytes(1000, 1000)
    3.0
    >>> image_megabytes(1920, 1080)
    6.2208
    >>> image_megabytes(0, 1080)
    0
    """
    return width * height * 3 / 1000000

doctest.run_docstring_examples(image_megabytes, globals(), name="image_megabytes")
```

<details class="dl-answer"><summary>answer</summary>

Only the third. The report says it expected `0` and got `0.0`. The `/`
always gives a float, and `doctest` compares the text Python prints,
not the number. The number is 0 either way. Only the example's text
differs. If you write `0.0` in the docstring, it matches.

</details>

<aside class="dl-note" id="code-other-practice-note-doctest">

**Who wrote doctest.** Tim Peters wrote `doctest`, and it became part
of Python in version 2.1, in 2001. He also wrote the Zen of Python, the
sayings from the tutorial page.

</aside>

**7. Make.** A weather station's code turns a board's 10-bit reading
from its TMP36 chip into °C. This chip reads 1.5 °C high, so when asked,
the function takes that away. Review it with the checklist, then
rewrite it. Test that your version gives the same answers as this one
for many readings, with and without the correction.

```python
def t(a,b):
    x=a*5/1024
    x=x*100-50
    if b==True:
        x=x-1.5
    return round(x,1)
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Say in one sentence what `t` returns. That sentence is the start
   of your docstring and a clue to the name.
2. The first two lines are two machines from
   [Machines that take a number](tutorial:machines-that-take-a-number#machines-in-a-row-composition):
   `reading_volts` and `sensor_celsius`.
3. Give 5, 1024 and 1.5 names at the top, in capitals.
4. Keep each step in the same order as the original, so the floats
   round the same way.
5. Loop over readings and over `[False, True]`, and `assert` that both
   versions agree.

**Think about:** why `b==True` can be written as `b`.

</details>

<details class="dl-answer"><summary>answer</summary>

Review findings: the names `t`, `a`, `b` and `x` say nothing; there is
no docstring; 5, 1024 and 1.5 are magic numbers; `b==True` can be `b`;
there are no spaces round `=` and `*`; and `x` holds a voltage on one
line and a temperature on the next.

```python
BOARD_VOLTS = 5          # the board measures 0 to 5 volts
READING_STEPS = 1024     # a 10-bit reading runs from 0 to 1023
SENSOR_ERROR_C = 1.5     # this chip reads 1.5 °C high


def reading_volts(reading):
    """Return the voltage for a board's reading, a whole number from 0 to 1023."""
    return reading * BOARD_VOLTS / READING_STEPS


def sensor_celsius(volts):
    """Return the temperature in °C that a TMP36 chip reads as volts."""
    return volts * 100 - 50


def reading_celsius(reading, correct_error=False):
    """Return the temperature in °C for a board's reading, to one decimal place.

    With correct_error True, the chip's known error is taken away.
    """
    celsius = sensor_celsius(reading_volts(reading))
    if correct_error:
        celsius = celsius - SENSOR_ERROR_C
    return round(celsius, 1)


def t(a,b):
    x=a*5/1024
    x=x*100-50
    if b==True:
        x=x-1.5
    return round(x,1)


for reading in range(20, 360):
    for correct_error in [False, True]:
        assert reading_celsius(reading, correct_error) == t(reading, correct_error), reading
print(reading_celsius(154), reading_celsius(154, correct_error=True))
```

It prints `25.2 23.7`. The steps are in the same order as the original,
so the answers match for every reading. The 100 and the 50 stay inside
`sensor_celsius`, whose docstring says where they come from.

</details>

**8. Explain.** `quick_review` flags the names `mb` and `s` in this
function. In the tutorial, we kept `p` and `q` in `slope`. Should `mb`
and `s` be kept too? Why or why not?

```python
def rate(mb, s):
    """Return a download speed in megabits a second."""
    return mb * 8 / s
```

<details class="dl-answer"><summary>answer</summary>

They could change, to `megabytes` and `seconds`. `p` and `q` match the
maths written above `slope`, where two points are called $p$ and $q$.
`mb` and `s` come from no formula. They are short forms a stranger has
to decode, and the docstring does not say what they stand for: is `mb`
megabytes or megabits? The linter's note is the same in both cases.
The reason behind the name differs, and only a person can judge
that.

</details>

**9. Fix.** Schlomi refactored a game's `best_score`. A leaderboard
shows the best score at the top, so she sorted the scores and took the
first one. Before her change, `best_score([40, 95, 70])` gave 95. Now
it gives 40. Can you find the line that does not do what Schlomi meant,
and change it?

```python exec
id: code-other-practice-fix-score
def best_score(scores):
    """Return the highest score in scores, a list of at least one number.

    The list is not changed.
    """
    in_order = sorted(scores)
    return in_order[0]
```

```inputs
best_score([40, 95, 70])
best_score([7])          # one score
best_score([-3, -8])     # negative scores
```

```solution
def best_score(scores):
    """Return the highest score in scores, a list of at least one number.

    The list is not changed.
    """
    in_order = sorted(scores)
    return in_order[-1]
---
A leaderboard puts the biggest score first, but `sorted()` puts the
smallest first, so `in_order[0]` is the lowest score. The highest is
the last one, `in_order[-1]`.

Schlomi's version gives 7 for `[7]` too, because the smallest and
largest of `[7]` are the same. So the inputs need more than one
case.
```

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

It prints `10.583333333333334`. Most reviewers would pick the second.
It is one line, and `total` is a tool the team has already tested. The
first shows every step, which helps while you are learning, and repeats
work the toolkit already does.

</details>

**11. Make.** Write a docstring for this function that says all four
things: what comes out, what must go in, the edges, and an example.
Make the example one that `doctest` can run. The Sun is 149,600,000 km
from the Earth, on average. Run `doctest` to check it.

```python
def light_minutes(km):
    return round(km / 299792.458 / 60, 2)
```

<details class="dl-answer"><summary>answer</summary>

One possible docstring:

```python
def light_minutes(km):
    """Return how many minutes light takes to travel km, to 2 decimal places.

    km is a distance in kilometres, 0 or more. Light travels
    299,792.458 km each second. Nothing outside the function changes.

    >>> light_minutes(149600000)
    8.32
    """
    return round(km / 299792.458 / 60, 2)


doctest.run_docstring_examples(light_minutes, globals(), name="light_minutes")
```

`doctest` shows nothing, which means the example passed. Sunlight takes
8.32 minutes, about 8 minutes 19 seconds, as on
[Running a formula backwards](tutorial:running-a-formula-backwards).

</details>

**12. Explain.** Schlomo wrote this for his weather station. His chip
reads a little high, so he put its error in a name at the top, where
he can find it and change it. The function
works when the page first runs. Which question from the review
checklist does it raise, and what could happen later? Write the review
comment you would leave.

```python
offset = 1.5

def corrected(celsius):
    """Return a reading in °C, corrected for the chip's known error."""
    return round(celsius - offset, 1)
```

<details class="dl-answer"><summary>answer</summary>

It raises the fourth question, "what does this space let us do?". The
function needs `offset`, and it takes it from outside, a hidden input.
If a later cell sets `offset` for a second chip, `corrected` quietly
gives different answers for the first one, and its own code looks the
same as before.

Schlomo's idea of a name at the top is the named-constant habit, and a
constant that truly never changes can live there. This one is
different for every chip. A review comment: "`corrected` reads
`offset` from the page. Could it come in as a parameter,
`offset=1.5`, so the function says what it needs and a test can check
it for each chip?"

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
it finds a magic number?

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
'short name x', 'number 5', 'number 1024', 'number 100', 'number 50',
'number 1.5']`. The 5, the 1024 and the 1.5 are magic numbers. A
stranger cannot tell what they mean. The 100 and the 50 are the TMP36's
own rule, and a docstring that names the chip explains them. The 1 in
`round(x, 1)`, one decimal place, is skipped. The tool finds places to
look. A person decides. `True` is left out because its type is `bool`,
not `int`.

</details>

**14. Another way.** Problem 6 checked `image_megabytes` with
`doctest`. Check the same promise a second way: write its three
examples as `assert` lines, with `close_enough`. Which way would you
rather find in a stranger's code, and why?

<details class="dl-answer"><summary>answer</summary>

```python
def image_megabytes(width, height):
    """Return the size in MB of a picture, width by height pixels, at 3 bytes a pixel."""
    return width * height * 3 / 1000000


assert close_enough(image_megabytes(1000, 1000), 3.0)
assert close_enough(image_megabytes(1920, 1080), 6.2208)
assert close_enough(image_megabytes(0, 1080), 0)
```

Both check the same three cases. The `assert` lines compare numbers,
so `0` and `0.0` agree, and `close_enough` ignores tiny float errors.
`doctest` compares printed text, which is stricter, but its examples
sit in the docstring, where a stranger reads them with `help()`. Many
teams keep a few examples in the docstring and the full tests
elsewhere. `close_enough` would also accept the tutorial's
`sensor_celsius(0.57)`, which `doctest` printed as `6.999999999999993`.

</details>

**15. Explain.** The tutorial taught reviewing with a function made
hard to read on purpose, and gave the coding rules afterwards. Would you
have taught the rules first? Say which way you would choose, and why.

<details class="dl-answer"><summary>answer</summary>

There is more than one answer worth giving. Rules first gives a reader
the standard before they write anything, so habits start early, and it
is how a standard arrives in most jobs. A hard-to-read function first
lets a reader meet the problem each rule solves, so the rules make
sense, but it asks them to read messy code before they know what to
look for. An answer might also say who the reader is: a person who has
written code for a while may get more from the function first, and a
person starting out may want the rules. Either choice works if you give
your reasons.

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
