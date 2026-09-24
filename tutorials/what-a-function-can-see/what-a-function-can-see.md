---
title: "What a function can see: scope and parameters"
year: "2026-2027"
version: 2026.09.24.1
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

You write a function that works out a runner's pace, and inside it you
give the pace a name. On the next line, outside the function, you ask
Python to print that name. Python says it has never heard of it. The
name was there a moment ago. Where did it go, and what can a function
see?

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

Here is the runner's function. A run of 5 km took 30 minutes. The last
line asks for the name made inside the function, and it is meant to
fail. Before you run it, which line do you think Python will stop at?

```python exec
id: what-function-inside-1
def pace(minutes, km):
    """Give back the minutes taken for each kilometre of a run."""
    minutes_per_km = minutes / km
    return minutes_per_km

print(pace(30, 5))
print(minutes_per_km)
```

The first line shows `6.0`, six minutes for each kilometre. Then Python
stops:

```text
NameError: name 'minutes_per_km' is not defined
```

That is the error from
[When Python says no](tutorial:when-python-says-no#the-last-line-first):
a name that points at nothing. But this time there is no typing mistake.
The name was made, inside the function, and it is gone.

Here is what happened, in order.

1. The call `pace(30, 5)` starts. Python makes a new, empty space of
   names for this one call.
2. In that space, `minutes` points at 30 and `km` points at 5.
3. `minutes_per_km = minutes / km` makes a third name, in the same space.
4. `return` hands the value 6.0 out to the line that called.
5. The call ends, and Python throws the space away, with every name in it.

A *local name* is a name made inside a function. It exists only inside
that function, and only while one call is running. The *scope* of a name
is the part of a program where the name can be seen. So the scope of
`minutes_per_km` is the inside of `pace`, and the last line of the cell
is outside it.

You can picture each call as a small room, built when the call starts
and taken down when it ends. The only thing carried out of the room is
the value in the `return` line.

If you want that value outside, keep it under a name of your own:

```python exec
id: what-function-inside-2
my_pace = pace(30, 5)
print(my_pace)
```

`my_pace` is made on the page, outside every function, so it stays
after the call ends.

### Your turn

1. A 10 km race took 55 minutes. In the cell above, keep the pace under
   the name `race_pace`, and print it.
2. After the call, add `print(km)`. Before you run it, which error do you
   expect, and why?

## A fresh space for every call

A café gives a stamp with every coffee. Here is a first try at a stamp
counter. It is called three times. Will it print 1, 2 and 3, or
something else? Decide, then run it to check.

```python exec
id: what-function-fresh-1
def add_stamp():
    """Add one stamp to a loyalty card."""
    stamps = 0
    stamps = stamps + 1
    return stamps

print(add_stamp())
print(add_stamp())
print(add_stamp())
```

It prints `1` three times. Each call gets a new space, so each call
starts again with `stamps = 0`. Nothing is kept from one call to the
next.

For a loyalty card, that is a problem: a card has to remember. But it
is also what makes a function a promise we can test. The tests on
[Does it work?](tutorial:does-it-work) are only worth running because
the same inputs give the same result every time. A later section on this
page fixes the café card.

Fresh spaces have a second good side. Two functions can use the same
name for different things, and they never get in each other's way. What
do you think this cell prints?

```python exec
id: what-function-fresh-2
def bus_fares(journeys):
    cost = journeys * 2.00
    return cost

def parking(hours):
    cost = hours * 3.50
    return cost

print(bus_fares(10) + parking(2))
```

It prints `27.0`: €20 of bus fares and €7 of parking. Each `cost` lives
in its own function's space. It is like two recipes in one cookbook that
both say "the batter": nobody pours the pancake batter into the cake
tin, because each recipe's names belong to that recipe.

## What a function can see from outside

So names made inside stay inside. Can a function see names made
outside? Here, the VAT rate is made on the page, and the function uses
it without being handed it. Will it work?

```python exec
id: what-function-outside-1
vat_percent = 23

def with_vat(price):
    """Give back the price with VAT added, rounded to the cent."""
    return round(price * (1 + vat_percent / 100), 2)

print(with_vat(100))
```

It works, and shows `123.0`. A *global name* is a name made on the page
itself, outside every function. Every function on the page can read it.

When a function meets a name, Python looks for it in three spaces, in
this order:

1. the function's own space, for this call;
2. the page's space, where the global names are;
3. Python's own space, where `print`, `round` and `len` live.

The first place that has the name wins. Your toolkit functions, like
`split_bill`, are in the page's space too. They were loaded there before
the first cell ran.

Now a question about sequence. The rate changes to 13.5%, Ireland's
lower rate for some services. The function was written when the rate was
23. What will it give now?

```python exec
id: what-function-outside-2
vat_percent = 13.5
print(with_vat(100))
```

It gives `113.5`. The function looks the name up each time it runs, not
when it was written. Compare that with `water_ml` on
[Recipes are algorithms](tutorial:recipes-are-algorithms#names-that-hold-values):
there, a line worked out a value once, and changing `cups` later made no
difference. A function's lines run again at every call, so they see the
page as it is at that moment.

Is that good? The same call, `with_vat(100)`, gave two different answers,
and nothing in the call or the docstring says why. The rate is a
*hidden input*: something the function needs that is not among its
parameters. The fix is to make it a parameter, with a default value, as
`split_bill` does with its tip:

```python exec
id: what-function-outside-3
def with_vat(price, vat_percent=23):
    """Give back the price with VAT added, rounded to the cent.

    vat_percent is the VAT rate as a percentage, 23 unless given.
    """
    return round(price * (1 + vat_percent / 100), 2)

assert with_vat(100) == 123.0
assert with_vat(100, 13.5) == 113.5
print(with_vat(100))
```

It prints `123.0`, even though the page's `vat_percent` is still 13.5.
The parameter `vat_percent` is a local name, and the function's own space
is searched first. Now everything the function needs is on its `def`
line, where a reader can see it.

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

1. Rewrite `add_stamp` from the café so that it takes the number of
   stamps in, and gives back one more.
2. Test it with two `assert` lines.
3. Start a card at 0, and use a loop from
   [Doing it again](tutorial:doing-it-again) to add ten stamps. Print the
   card at the end. It should say `10`.

```python exec
id: what-function-change-your-turn
# Your add_stamp(stamps), its tests, and a loop of ten coffees
```

## Values in, by position and by name

On [Machines that take a number](tutorial:machines-that-take-a-number#a-machine-with-one-slot),
the value in the brackets of a call was the argument, and the name in
the `def` line was the parameter, the slot it goes into. Now we can say
what "goes into" means. When a call starts, Python makes each parameter,
in the call's new space, point at its argument: the first parameter at
the first argument, the second at the second, and so on. This is
*parameter passing*.

Here is `split_bill` from your toolkit, called twice with the same two
names. What will the second line give?

```python exec
id: what-function-args-1
bill = 84
friends = 4
print(split_bill(bill, friends, 10))
print(split_bill(friends, bill, 10))
```

The first line gives `23.1`. The second gives `0.05`: a bill of €4,
shared between 84 people. `split_bill` never saw the names `bill` and
`friends`. It saw the values 84 and 4, in the order they came.

This answers the question from the top of the page, from the other side.
A function cannot see your variable's name. It sees only the value you
hand it. That is also why your toolkit works on every page:
`split_bill` was written on another page, knows nothing about this one,
and needs nothing from it.

The keyword arguments from
[Machines that take a number](tutorial:machines-that-take-a-number#functions-that-give-back-and-procedures-that-do)
match each value to a parameter by its name, not its place. So they can
come in any order, as long as they come after the plain ones.

```python exec
id: what-function-args-2
print(split_bill(people=4, total=84, tip_percent=10))
print(split_bill(84, 4, tip_percent=15))
```

These give `23.1` and `24.15`.

One more question. Inside this function, the parameter is given a new
value. Does `bill` on the page change too? Decide before you run it.

```python exec
id: what-function-args-3
def add_tip(total):
    total = total * 1.10
    return round(total, 2)

bill = 84
print(add_tip(bill))
print(bill)
```

The first line shows `92.4`, the bill with the tip added. The second
shows `84`: `bill` did not change. A walkthrough table, like the ones on
[Does it work?](tutorial:does-it-work), shows why. This one has a column
for each space.

| Step | The page's space | `add_tip`'s space |
|---|---|---|
| `bill = 84` | `bill` → 84 | (no call yet) |
| the call `add_tip(bill)` starts | `bill` → 84 | `total` → 84 |
| `total = total * 1.10` | `bill` → 84 | `total` → 92.4 |
| `return` hands 92.4 out | `bill` → 84 | (thrown away) |

The `=` inside made `total` point at a new value, in the call's own
space. It did nothing to `bill`, which lives in another space.

## Handing over a list

A list is a row of values, as on [Doing it again](tutorial:doing-it-again).
Unit 5 teaches lists properly. For now we need one thing about them:
`append` adds a value to the end of a list, as it did on
[True, false and every case](tutorial:true-false-and-every-case#a-tool-for-any-rule).

Here is a function that adds a song to a playlist. After the call, will
`road_trip` have two songs or three?

```python exec
id: what-function-list-1
def add_song(playlist, song):
    """Put song at the end of playlist. Gives nothing back."""
    playlist.append(song)

road_trip = ["Zombie", "Linger"]
add_song(road_trip, "Galway Girl")
print(road_trip)
```

Three. This time the function changed something on the page. Why is
this different from `add_tip`?

When the call starts, `playlist` is made to point at the same list that
`road_trip` points at. There is one list, with two names. `append` does
not make a name point at something new. It changes the list itself, and
every name that points at that list sees the change.

So there are two different moves, and it helps to keep them apart:

- `=` makes one name point at a new value. It happens in one space only.
- `append` changes the value itself. Every name pointing at it, in any
  space, sees the new value.

A number cannot be changed in place, so for numbers only the first move
exists. That is why `bill` was safe. A list can be changed in place, so a
function that is handed a list can change it. `add_song` says so in its
docstring, which is the honest thing to do.

`add_song` is a procedure, in the words of
[Machines that take a number](tutorial:machines-that-take-a-number#functions-that-give-back-and-procedures-that-do):
it does a job, and gives back `None`. Its job is a change that reaches
outside its own space, through the list it was handed.

```question
id: what-function-procedure-2
type: multiple-choice
correct: 3

After `road_trip = add_song(road_trip, "Sultans of Swing")`, what does
`road_trip` point at?

- The playlist, with the new song at the end
- The playlist, without the new song
- `None`, because `add_song` gives back nothing
```

## A function made inside a function

On [Machines that take a number](tutorial:machines-that-take-a-number#machines-in-a-row-composition),
`compose` made a function called `both` inside itself, and gave it back.
That page left a puzzle. When `both` runs, the call to `compose` has
already ended. So how does `both` still know `outer` and `inner`?

Here is a smaller machine of the same shape. `rate_converter` is given
an exchange rate, and gives back a function that changes euro at that
rate. The rates are made up. What will the last line show?

```python exec
id: what-function-made-inside-1
def rate_converter(rate):
    """Give back a function that changes euro into another money at rate."""
    def convert(euro):
        return round(euro * rate, 2)
    return convert

to_sterling = rate_converter(0.85)
to_dollars = rate_converter(1.10)
print(to_sterling(100), to_dollars(100))
```

It shows `85.0 110.0`. Each call to `rate_converter` made its own space,
with its own `rate` in it. Each `convert` was made inside one of those
spaces, and it keeps hold of that space. So Python does not throw the
space away when the call ends, because something still needs it.

A *closure* is a function that keeps the space it was made in. So a
function looks for a name in up to four spaces, in this order:

1. its own space, for this call;
2. the space of the function it was made inside, if there is one;
3. the page's space;
4. Python's own space.

That is how `both` finds `outer` and `inner`: in step 2. The mixed
problems at the end of this unit use this idea to build a unit converter.

## What does a function need?

Here is a delivery app's function, as someone first wrote it. It runs,
and it prints the right cost. Let's ask three questions of it: what
does it need, where does it get it, and what does it give back?

```python exec
id: what-function-need-1
rate_per_km = 0.19

def delivery_cost(distance_km):
    cost = 3 + distance_km * rate_per_km
    print("Delivery costs", round(cost, 2))

delivery_cost(12)
```

It needs two things, the distance and the rate. It gets the distance
from its parameter, and the rate from the page: a hidden input. It gives
back nothing, so no `assert` can check it, and no other function can use
its answer. Its local name `cost` is thrown away at the end of the call.

Three habits keep a function's promise in plain sight:

1. Everything it needs comes in through its parameters.
2. Everything it gives comes out through `return`.
3. It changes nothing outside itself, unless its docstring says so.

Every function in your toolkit keeps these three habits, and that is
the reason it can travel from page to page.

### Your turn

1. Rewrite `delivery_cost` in the cell below so that it keeps all three
   habits. Give the rate a default value of 0.19, and round to the cent.
2. Run the cell. The tests at the bottom check your promise. Until your
   rewrite is done, they stop with an `AssertionError`. That is the tests
   doing their job.
3. Print the cost of a 40 km delivery at a rate of €0.25 per km.

```python exec
id: what-function-need-your-turn
def delivery_cost(distance_km):
    cost = 3 + distance_km * rate_per_km
    print("Delivery costs", round(cost, 2))

assert delivery_cost(12) == 5.28
assert delivery_cost(12, rate_per_km=0.25) == 6.0
print("delivery_cost keeps its promise.")
```

```hint
What does the version above give back to the `assert`? Try
`print(delivery_cost(12))` on its own and look at the last line it
shows.
```

```hint
after: 10 errors
title: some steps
1. Add `rate_per_km=0.19` to the `def` line, after `distance_km`.
2. Swap the `print` line for a `return` line that gives back
   `round(cost, 2)`.
3. Nothing on the page needs to change: the tests only use the function.

**Think about:** which line of the old version made the tests fail, and
why did it not raise an error on its own?
```

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
