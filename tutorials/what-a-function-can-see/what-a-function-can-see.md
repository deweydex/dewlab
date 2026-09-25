---
title: "What a function can see: scope and parameters"
year: "2026-2027"
version: 2026.09.25.2
covers:
  names-made-inside-a-function:
    covers: [PDP-LO8]
    touches: [PDP-LO9]
  a-fresh-space-for-every-call:
    covers: [PDP-LO8]
  what-a-function-can-see-from-outside:
    covers: [PDP-LO8]
  changing-a-name-from-inside:
    covers: [PDP-LO8]
    touches: [PDP-LO9]
  values-in-by-position-and-by-name:
    covers: [PDP-LO8]
  handing-over-a-list:
    covers: [PDP-LO8]
  a-function-made-inside-a-function:
    covers: [PDP-LO8]
    touches: [MIT-3.1]
  what-does-a-function-need:
    covers: [PDP-LO8]
    touches: [PDP-LO10]
---

# What a function can see: scope and parameters

You write a function that works out how fast a file downloaded, and
inside it you give the speed a name. On the next line, outside the
function, you ask Python to print that name. Python says it has never
heard of it. The name was there a moment ago. Where did it go, and what
can a function see?

On this page we:

- see where a name made inside a function goes when the function ends
- see which names a function can read from the page around it
- find out why a function cannot change a page's name with `=`
- hand values to a function by position and by name
- hand a function a list, and see why that is different
- find out how a function made inside another one keeps what it needs
- ask of any function: what does it need, and where does it get it?

> **The space we're in.** Every call to a function gets a small space
> of names of its own. Python makes it when the call starts, and
> usually throws it away when the call ends. From inside that space, a
> function can read the names on the page around it, but a new name made
> with `=` stays inside. Those rules are almost never written down, and
> they are what this page is about. Your toolkit from every earlier page
> is loaded here, as usual.

## Warm-up

Two questions from this unit. The first is from
[Machines that take a number](tutorial:machines-that-take-a-number), and
the second from [Does it work?](tutorial:does-it-work)

```question
id: what-function-warm-up-1
type: fill-in-the-blank

`double(x)` gives `2 * x`, and `add_one(x)` gives `x + 1`. The function
`compose(double, add_one)` does `add_one` first, then `double`. So
`compose(double, add_one)(5)` gives {12}.
```

```question
id: what-function-warm-up-2
type: multiple-choice
correct: 1

`0.1 + 0.2 == 0.3` is `False` in Python. What does
`close_enough(0.1 + 0.2, 0.3)` give?

- `True`, because the two differ by far less than the tolerance
- `False`, because the two are not exactly equal
- An error, because floats cannot be compared
```

## Names made inside a function

Here is the download function. A 700 MB file took 56 seconds. The last
line asks for the name made inside the function, and it is meant to
fail. Before you run it, which line do you think Python will stop at?

```python exec
id: what-function-inside-1
def download_speed(megabytes, seconds):
    """Give back the megabytes downloaded each second."""
    megabytes_per_second = megabytes / seconds
    return megabytes_per_second

print(download_speed(700, 56))
print(megabytes_per_second)
```

The first line shows `12.5`, twelve and a half megabytes each second.
Then Python stops:

```text
NameError: name 'megabytes_per_second' is not defined
```

That is the error from
[When Python says no](tutorial:when-python-says-no#the-last-line-first):
a name that points at nothing. But this time there is no typing mistake.
The name was made, inside the function, and it is gone.

Here is what happened, in order.

1. The call `download_speed(700, 56)` starts. Python makes a new, empty
   space of names for this one call.
2. In that space, `megabytes` points at 700 and `seconds` points at 56.
3. `megabytes_per_second = megabytes / seconds` makes a third name, in
   the same space.
4. `return` hands the value 12.5 out to the line that called.
5. The call ends, and Python throws the space away, with every name in it.

A *local name* is a name made inside a function. It exists only inside
that function, and only while one call is running. The *scope* of a name
is the part of a program where the name can be seen. So the scope of
`megabytes_per_second` is the inside of `download_speed`, and the last
line of the cell is outside it.

You can picture each call as a small room, built when the call starts
and taken down when it ends. The only thing carried out of the room is
the value in the `return` line.

If you want that value outside, keep it under a name of your own:

```python exec
id: what-function-inside-2
my_speed = download_speed(700, 56)
print(my_speed)
```

`my_speed` is made on the page, outside every function, so it stays
after the call ends.

### Your turn

1. A 2,400 MB game took 80 seconds to download. In the cell above, keep
   its speed under the name `game_speed`, and print it.
2. After the call, add `print(seconds)`. Before you run it, which error
   do you expect, and why?

## A fresh space for every call

A network card counts the packets of data it receives: small pieces of
a file, sent one at a time. Here is a first try at a packet counter.
It is called three times. Will it print 1, 2 and 3, or something else?
Decide, then run it to check.

```python exec
id: what-function-fresh-1
def add_packet():
    """Add one to the count of packets received."""
    packets = 0
    packets = packets + 1
    return packets

print(add_packet())
print(add_packet())
print(add_packet())
```

It prints `1` three times. Each call gets a new space, so each call
starts again with `packets = 0`. Nothing is kept from one call to the
next.

For a counter, that is a problem: a counter has to remember. But it is
also what makes a function a promise we can test: the same inputs give
the same result every time. A later section on this page fixes the
counter.

Fresh spaces have a second good side. Two functions can use the same
name for different things, and they never get in each other's way. What
do you think this cell prints?

```python exec
id: what-function-fresh-2
def image_bytes(width, height):
    size = width * height * 3        # 3 bytes for each pixel
    return size

def sound_bytes(seconds):
    size = seconds * 44100 * 2 * 2   # CD sound: 44,100 samples a second, 2 bytes each, 2 speakers
    return size

print(image_bytes(1920, 1080) + sound_bytes(10))
```

It prints `7984800`: about 6.2 million bytes for one full-HD picture,
and 1.8 million for ten seconds of CD sound. Each `size` lives in its
own function's space, like two files called `notes.txt` in two
different folders.

## What a function can see from outside

So names made inside stay inside. Can a function see names made
outside? Drop a ball, and *gravity*, the pull of the Earth, makes it
fall faster and faster. On Earth, a falling thing gets 9.81 metres a
second faster every second. Physics gives a rule for how long a fall
takes, if we ignore the air: $t = \sqrt{\frac{2h}{g}}$, where $h$ is the
height and $g$ is that 9.81. You do not need to know where the rule
comes from. Here, `gravity` is made on the page, and the function uses
it without being handed it. Will it work?

```python exec
id: what-function-outside-1
import math

gravity = 9.81

def fall_time(height):
    """Give back the seconds a ball takes to fall height metres, ignoring the air."""
    return round(math.sqrt(2 * height / gravity), 2)

print(fall_time(20))
```

It works, and shows `2.02`: a ball dropped from 20 metres lands in
about 2 seconds. A *global
name* is a name made on the page itself, outside every function. Every
function on the page can read it.

When a function meets a name, Python looks for it in three spaces, in
this order:

1. the function's own space, for this call;
2. the page's space, where the global names are;
3. Python's own space, where `print`, `round` and `len` live.

The first place that has the name wins. Your toolkit functions, like
`digit_at`, are in the page's space too. They were loaded there before
the first cell ran.

Now a question about sequence. We take the ball to the Moon, where
gravity is much weaker: 1.62 metres a second, every second. The
function was written for Earth. What will it give now?

```python exec
id: what-function-outside-2
gravity = 1.62
print(fall_time(20))
```

It gives `4.97`: the same drop takes more than twice as long. The
function looks the name up each time it runs, not when it was written.
Compare that with `water_ml` on
[Recipes are algorithms](tutorial:recipes-are-algorithms#names-that-hold-values):
there, a line worked out a value once, and changing `cups` later made no
difference. A function's lines run again at every call, so they see the
page as it is at that moment.

<aside class="dl-note" id="what-function-note-moon">

**A hammer and a feather.** In 1971, on the Apollo 15 mission, the
astronaut David Scott dropped a hammer and a feather together on the
Moon. With no air to slow the feather, they landed at the same moment,
as the rule above says they should. NASA keeps a film of it online.

</aside>

Is that good? The same call, `fall_time(20)`, gave two different
answers, and nothing in the call or the docstring says why. The pull of
gravity is a *hidden input*: something the function needs that is not
among its parameters. The fix is to make it a parameter, with a default
value, as `digit_at` does with its base:

```python exec
id: what-function-outside-3
def fall_time(height, gravity=9.81):
    """Give back the seconds a ball takes to fall height metres, ignoring the air.

    gravity is how much faster, in metres a second, a falling thing gets
    every second: 9.81 on Earth unless given.
    """
    return round(math.sqrt(2 * height / gravity), 2)

assert fall_time(20) == 2.02
assert fall_time(20, 1.62) == 4.97
print(fall_time(20))
```

It prints `2.02`, even though the page's `gravity` is still 1.62. The
parameter `gravity` is a local name, and the function's own space is
searched first. Now everything the function needs is on its `def` line,
where a reader can see it, and the Moon is one argument away.

## Changing a name from inside

A quiz game keeps a score. The function below should add one point to
it. This cell is meant to fail. Before you run it, can you guess why?
Here is a clue: the problem is inside the function, not outside it.

```python exec
id: what-function-change-1
score = 0

def add_point():
    score = score + 1

add_point()
print(score)
```

The last line of the error says:

```text
UnboundLocalError: cannot access local variable 'score' where it is not associated with a value
```

"Local variable 'score'"? We made `score` on the page. Here is the
rule that explains it. When Python reads a `def`, it notes every name the
function gives a value to with `=`. Those names are local, for the whole
function, from its first line. So inside `add_point`, `score` means the
local `score`. The right side of `score = score + 1` asks for its value
before it has one. An *UnboundLocalError* is a NameError about a local
name that has no value yet.

Python decided this while reading the `def`, before the function ever
ran: reading first, running after, as on
[When Python says no](tutorial:when-python-says-no#mistakes-python-finds-before-it-starts).

Python does have a way to say "use the page's name". The keyword
`global`, on the first line of a function, does it:

```python
def add_point():
    global score
    score = score + 1
```

It works, and most programmers use it rarely. A function that changes a
page's names without saying so makes a promise it never writes down,
and a test can only check what a function gives back. The usual way is
to take the value in and give the new value back:

```python exec
id: what-function-change-2
def add_point(score):
    """Give back the score with one more point."""
    return score + 1

assert add_point(0) == 1
assert add_point(9) == 10

score = 0
score = add_point(score)
score = add_point(score)
print(score)
```

It prints `2`. The name `score` on the page changes, and the line that
changes it is on the page, where you can see it.

### Your turn

1. Rewrite `add_packet` so that it takes the count of packets in, and
   gives back one more.
2. Test it with two `assert` lines.
3. Start a count at 0, and use a loop from
   [Doing it again](tutorial:doing-it-again) to add ten packets. Print
   the count at the end. It should say `10`.

```python exec
id: what-function-change-your-turn
# Your add_packet(packets), its tests, and a loop of ten packets
```

## Values in, by position and by name

On [Machines that take a number](tutorial:machines-that-take-a-number#a-machine-with-one-slot),
the value in the brackets of a call was the argument, and the name in
the `def` line was the parameter, the slot it goes into. Now we can say
what "goes into" means. When a call starts, Python makes each parameter,
in the call's new space, point at its argument: the first parameter at
the first argument, the second at the second, and so on. This is
*parameter passing*.

Here is `digit_at` from your toolkit, called twice with the same two
names. What will the second line give?

```python exec
id: what-function-args-1
year = 2026
place = 3
print(digit_at(year, place))
print(digit_at(place, year))
```

The first line gives `2`, the thousands digit of 2026. The second gives
`0`: the digit in place 2026 of the number 3, far past its only digit.
`digit_at` never saw the names `year` and `place`. Even the page's
`place` went into the slot called `number`, because it came first. The
function saw the values 3 and 2026, in the order they came.

This answers the question from the top of the page, from the other side.
A function cannot see your variable's name. It sees only the value you
hand it. That is also why your toolkit works on every page:
`digit_at` was written on another page, knows nothing about this one,
and needs nothing from it.

Keyword arguments, from
[Machines that take a number](tutorial:machines-that-take-a-number#functions-that-give-back-and-procedures-that-do),
match each value to a parameter by its name instead, so
`digit_at(place=0, number=2026)` gives 6, the last digit.

One more question. In a game, a bonus doubles your points. Inside this
function, the parameter is given a new value. Does `score` on the page
change too? Decide before you run it.

```python exec
id: what-function-args-3
def add_bonus(points):
    points = points * 2
    return points

score = 84
print(add_bonus(score))
print(score)
```

The first line shows `168`, the score with its bonus. The second shows
`84`: `score` did not change. A trace table, like the ones on
[Does it work?](tutorial:does-it-work#a-walkthrough-by-hand), shows why. This one has a column
for each space.

| Step | The page's space | `add_bonus`'s space |
|---|---|---|
| `score = 84` | `score` → 84 | (no call yet) |
| the call `add_bonus(score)` starts | `score` → 84 | `points` → 84 |
| `points = points * 2` | `score` → 84 | `points` → 168 |
| `return` hands 168 out | `score` → 84 | (thrown away) |

The `=` inside made `points` point at a new value, in the call's own
space. It did nothing to `score`, which lives in another space.

## Handing over a list

A list is a row of values, as on [Doing it again](tutorial:doing-it-again),
and `append` adds a value to its end, as on
[True, false and every case](tutorial:true-false-and-every-case#a-tool-for-any-rule).

Here is a function that adds a reading to a sensor's log. After the
call, will `today` have two readings or three?

```python exec
id: what-function-list-1
def add_reading(readings, value):
    """Put value at the end of readings. Gives nothing back."""
    readings.append(value)

today = [14.2, 14.8]
add_reading(today, 15.1)
print(today)
```

Three. This time the function changed something on the page. Why is
this different from `add_bonus`?

When the call starts, `readings` is made to point at the same list that
`today` points at. There is one list, with two names. `append` does not
make a name point at something new. It changes the list itself, and
every name that points at that list sees the change.

So there are two different moves, and it helps to keep them apart:

- `=` makes one name point at a new value. It happens in one space only.
- `append` changes the value itself. Every name pointing at it, in any
  space, sees the new value.

A number cannot be changed in place, so for numbers only the first move
exists. That is why `score` was safe. A list can be changed in place, so a
function that is handed a list can change it. `add_reading` says so in
its docstring, which is the honest thing to do. It is a procedure, in
the words of
[Machines that take a number](tutorial:machines-that-take-a-number#functions-that-give-back-and-procedures-that-do):
it gives back `None`, and its job reaches outside its own space, through
the list it was handed.

```question
id: what-function-procedure-2
type: multiple-choice
correct: 3

After `today = add_reading(today, 15.6)`, what does `today` point at?

- The log, with the new reading at the end
- The log, without the new reading
- `None`, because `add_reading` gives back nothing
```

## A function made inside a function

On [Machines that take a number](tutorial:machines-that-take-a-number#machines-in-a-row-composition),
`compose` made a function called `both` inside itself, and gave it back.
That page left a puzzle. When `both` runs, the call to `compose` has
already ended. So how does `both` still know `outer` and `inner`?

Here is a smaller machine of the same shape. `converter` is given a
factor, and gives back a function that multiplies by that factor. There
are 8 bits in a byte, and exactly 2.54 centimetres in an inch. What will
the last line show?

```python exec
id: what-function-made-inside-1
def converter(factor):
    """Give back a function that multiplies its input by factor."""
    def convert(value):
        return value * factor
    return convert

bytes_to_bits = converter(8)
inches_to_cm = converter(2.54)
print(bytes_to_bits(100), inches_to_cm(6.1))
```

It shows `800 15.494`: 100 bytes are 800 bits, and a phone screen 6.1
inches from corner to corner is about 15.5 cm. Each call to `converter`
made its own space, with its own `factor` in it. Each `convert` was made
inside one of those spaces, and it keeps hold of that space. So Python
does not throw the space away when the call ends, because something
still needs it.

A *closure* is a function that keeps the space it was made in. So a
function looks for a name in up to four spaces, in this order:

1. its own space, for this call;
2. the space of the function it was made inside, if there is one;
3. the page's space;
4. Python's own space.

That is how `both` finds `outer` and `inner`: in step 2. The mixed
problems at the end of this unit use this idea to build a unit converter.

## What does a function need?

Here is a download timer, as someone first wrote it. It says a
download takes 2 seconds to start, then the time the data needs at the
connection's speed. (A byte is 8 bits, and speeds are given in megabits
a second.) It runs, and it prints the right time. Let's ask three
questions of it: what does it need, where does it get it, and what does
it give back?

```python exec
id: what-function-need-1
speed_mbps = 100

def download_seconds(size_mb):
    seconds = 2 + size_mb * 8 / speed_mbps
    print("The download takes", round(seconds, 1), "seconds")

download_seconds(700)
```

It needs two things, the size and the speed. It gets the size from its
parameter, and the speed from the page: a hidden input. It gives back
nothing, so no `assert` can check it, and no other function can use its
answer. Its local name `seconds` is thrown away at the end of the call.

Three habits keep a function's promise in plain sight:

1. Everything it needs comes in through its parameters.
2. Everything it gives comes out through `return`.
3. It changes nothing outside itself, unless its docstring says so.

Every function in your toolkit keeps these three habits, and that is
the reason it can travel from page to page.

### Your turn

1. Rewrite `download_seconds` in the cell below so that it keeps all
   three habits. Give the speed a default value of 100, and round to one
   decimal place.
2. Run the cell. The tests at the bottom check your promise. Until your
   rewrite is done, they stop with an `AssertionError`. That is the tests
   doing their job.
3. Print the time for a 4,000 MB file at 50 megabits a second.

```python exec
id: what-function-need-your-turn
def download_seconds(size_mb):
    seconds = 2 + size_mb * 8 / speed_mbps
    print("The download takes", round(seconds, 1), "seconds")

assert download_seconds(700) == 58.0
assert download_seconds(700, speed_mbps=25) == 226.0
print("download_seconds keeps its promise.")
```

```hint
What does the version above give back to the `assert`? Try
`print(download_seconds(700))` on its own and look at the last line it
shows.
```

```hint
after: 10 errors
title: some steps
1. Add `speed_mbps=100` to the `def` line, after `size_mb`.
2. Swap the `print` line for a `return` line that gives back
   `round(seconds, 1)`.
3. Nothing on the page needs to change: the tests only use the function.

**Think about:** which line of the old version made the tests fail, and
why did it not raise an error on its own?
```

<details class="dl-why"><summary>Why this way?</summary>

This page ended with closures: a function made inside another one, which
keeps the space it was made in. Many courses at this level leave
closures out. A programmer can go a long time without needing one.

Leaving them out is a reasonable choice. The page is long already, and
that section is the hardest on it.

We kept it because [Machines that take a number](tutorial:machines-that-take-a-number)
made a promise. Its `compose` gave back a function that still knew
`outer` and `inner`, and that page said a later page would explain how.
A course that asks you to check promises should keep its own. The
section is last on the page, so you can stop before it and come back to
it another day.

</details>

## Four questions, looking back

| Question | On this page |
|---|---|
| What is named here? | Parameters and local names, made fresh in each call's space. Global names, made on the page. A list can have two names, one in each space. |
| What is promised? | A function promises what it gives back. Its parameters and its docstring should say everything it needs, and anything it changes. |
| What happens when? | Each call's space is made when the call starts, and thrown away when it ends unless a closure still needs it. Python decides which names are local while reading the `def`, before it runs. |
| What does this space let us do? | Inside a function: read the page's names, but not give them new values with `=`. Outside: see only what the function hands back. |

## What we have now

| Term | What it means |
|---|---|
| local name | a name made inside a function; it exists only during one call |
| scope | the part of a program where a name can be seen |
| global name | a name made on the page, outside every function; every function can read it |
| hidden input | something a function needs that is not one of its parameters |
| `UnboundLocalError` | a local name was used before it had a value |
| `global` | a keyword that lets a function give a page's name a new value; used rarely |
| parameter passing | each parameter is made to point at its argument, in the call's new space |
| `=` and `append` | `=` points one name at a new value, in one space; `append` changes the list itself, for every name |
| closure | a function that keeps the space it was made in, like `compose`'s `both` |
| where Python looks | the call's own space, then the function it was made in, then the page, then Python's own names |

That is the last page of Unit 4. After its practice page come the
[mixed problems](tutorial:mixed-making-your-own-tools), where the unit's
tools come together into a unit converter.

## Where to read more

The integrated course's
[Writing your own functions](tutorial:writing-your-own-functions#scope-where-variables-live)
has a shorter section on scope, with other examples.
