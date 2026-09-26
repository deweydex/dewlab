---
title: "Testing a class: hunting for the bug"
year: "2026-2027"
version: 2026.09.26.1
worlds:
  game: A game world, with characters, the things they carry, and rooms.
  ocean: An ocean expedition, with a submarine, its crew, and what they find.
  solar-system: A solar system, with planets, moons and the probes sent to them.
  your-own: A world of your own, with a class you design and grow page by page.
covers:
  five-suspects:
    covers: [FOOP-LO10]
  ten-lines-that-run-every-test:
    covers: [FOOP-LO10]
  a-test-before-the-fix:
    covers: [FOOP-LO10]
  close-enough:
    covers: [FOOP-LO10]
---

# Testing a class: hunting for the bug

Here are five versions of the submarine from
[Inheritance](tutorial:one-parent-many-children). Four of them have one
bug each. One is right. Run the cell. It makes the five classes, and
prints nothing.

```python exec
id: five-suspects-1
{{include: setup/oop/five-submarines.py}}
```

You could read all five closely, line by line, and spot the differences.
But a real class changes every week, and nobody reads it closely every
week. A test reads it for you, every time. On this page we hunt for the
bugs with tests: the suspects are the classes, and nothing about you is
being checked.

## Five suspects

Here is a first test. `check` builds a submarine from whichever class it
is given, dives 100 m, and uses `assert` to check the depth. The loop
gives it each suspect in turn. How many of the five do you think will
pass?

```python exec
id: five-suspects-2
def check(Sub):
    sub = Sub("Nautilus")
    sub.dive(100)
    assert sub.get_depth() == 100, "a dive of 100 m goes to 100 m"

suspects = {"A": SubmarineA, "B": SubmarineB, "C": SubmarineC,
            "D": SubmarineD, "E": SubmarineE}
for name in suspects:
    try:
        check(suspects[name])
        print(name, "passed")
    except AssertionError as error:
        print(name, "failed:", error)
```

All five pass. A class is a value like any other, so it can sit in a
dictionary, and `Sub("Nautilus")` builds a submarine from whichever class
`Sub` names. `try` and `except` let the loop carry on after a failed
`assert`, and print its message.

A *test* is code that uses a class and checks what it did. One test that
every suspect passes tells us very little. The bugs are somewhere a dive
of 100 m never goes.

Can you add asserts to `check`, so that four suspects fail and one is
left standing? Think about the edges of what a submarine does: a dive to
exactly the limit, a dive just past it, a rise past the surface.

```python exec
id: five-suspects-3
def check(Sub):
    sub = Sub("Nautilus")
    sub.dive(100)
    assert sub.get_depth() == 100, "a dive of 100 m goes to 100 m"
    # More checks here

for name in suspects:
    try:
        check(suspects[name])
        print(name, "passed")
    except AssertionError as error:
        print(name, "failed:", error)
```

```inputs
check(SubmarineA)
check(SubmarineB)
check(SubmarineC)
check(SubmarineD)
check(SubmarineE)
```

```hint
The hull limit is 400 m. After the dive of 100 m, what should a dive of
300 m more give? And a dive of 1 m after that? What should the depth be
after rising 500 m from there?
```

```solution
def check(Sub):
    sub = Sub("Nautilus")
    sub.dive(100)
    assert sub.get_depth() == 100, "a dive of 100 m goes to 100 m"
    sub.dive(300)
    assert sub.get_depth() == 400, "a dive to exactly the limit is allowed"
    sub.dive(1)
    assert sub.get_depth() == 400, "a dive past the limit changes nothing"
    sub.rise(500)
    assert sub.get_depth() == 0, "rising past the surface stops at 0"

for name in suspects:
    try:
        check(suspects[name])
        print(name, "passed")
    except AssertionError as error:
        print(name, "failed:", error)
---
C is the one left standing. A refuses a dive to exactly 400 m. B dives
even when it refuses. D checks each dive alone, so two dives can add up
past the limit. E rises above the surface. Three of the four bugs sit at
an edge: exactly 400, just past 400, just past 0.
```

That is where bugs like to live. A *boundary* is the edge of what a
method allows: exactly at the limit, one step past it, zero, empty. A
test at a boundary finds more bugs than ten tests in the middle.

## Ten lines that run every test

One `check` that does everything stops at its first failure, and says
nothing about the rest. Programmers usually write many small tests
instead, one for each promise, each building its own object, and each
named `test_` and what it checks. Then something runs them all.

Here are three tests for suspect C, and ten lines that find every
function whose name starts with `test_` and run it. `globals()` gives a
dictionary of every name the page has made, so the runner does not need a
list of the tests. What will the last line print?

```python exec
id: ten-lines-that-run-every-test-1
def test_a_dive_goes_down():
    sub = SubmarineC("Nautilus")
    sub.dive(100)
    assert sub.get_depth() == 100, "a dive of 100 m goes to 100 m"

def test_a_dive_to_the_limit_is_allowed():
    sub = SubmarineC("Nautilus")
    sub.dive(400)
    assert sub.get_depth() == 400, "a dive to exactly 400 m is allowed"

def test_rising_stops_at_the_surface():
    sub = SubmarineC("Nautilus")
    sub.rise(10)
    assert sub.get_depth() == 0, "rising at the surface stays at 0"

def run_tests():
    passed = 0
    failed = 0
    for name in list(globals()):
        if name.startswith("test_"):
            try:
                globals()[name]()
                passed = passed + 1
            except AssertionError as error:
                print("FAILED", name, error)
                failed = failed + 1
    print(passed, "passed,", failed, "failed")

run_tests()
```

```predict
What will the last line print?

- 3 passed, 0 failed
  - Suspect C was the one left standing.
- 1 passed, 2 failed
  - Two of the tests are at a boundary.
```

It prints `3 passed, 0 failed`. Change `SubmarineC` to `SubmarineA` in
all three tests, and run it again: now one test fails, and the other two
still run, and still say so.

Nearly every Python project runs its tests this way, with a tool called
*pytest*. It finds every function whose name starts with `test_`, in
every file whose name starts with `test_`, runs each one, and reports
what failed and why. These ten lines are the same idea, small enough to
read.

## A test before the fix

Here is the ocean world's submarine as it stood at the end of
[Composition](tutorial:objects-inside-objects). On
[Encapsulation](tutorial:keeping-details-inside-an-object) we asked what
`rise(-500)` does to it. A test is a good way to ask a question you
suspect the answer to. Write the test first, and run it before you fix
anything:

```python exec
id: a-test-before-the-fix-1
{{include: setup/oop/ocean-5.py}}


def test_rise_refuses_a_negative_number():
    sub = Submarine("Nautilus")
    sub.rise(-500)
    assert sub.get_depth() == 0, "rising by -500 m changes nothing"

run_tests()
```

The new test fails: rising by −500 m took the Nautilus 500 m down, past
its hull limit, and nothing refused. The three tests from before still
pass, since they build `SubmarineC`, which is still there: the runner
runs every test it can find. Now the fix, in `rise`:

```python
    def rise(self, metres):
        if metres < 0:
            print("Refused: rise needs a positive number of metres.")
            return
        self._depth = max(0, self._depth - metres)
```

Make that change in the cell above, and run it again: the new test
passes. Writing the failing test first does two things. It shows the bug
is real, and it shows the fix is what made it pass, not a lucky run. The
test then stays, so the bug cannot quietly come back.

## Close enough

A test can be wrong, too. The oxygen tank from
[Encapsulation](tutorial:keeping-details-inside-an-object), in its first
version, kept litres as decimals. Three uses of 0.1 litres from a full
litre leave 0.7. What will the test say?

```python exec
id: close-enough-1
class OxygenTank:
    def __init__(self, litres):
        self._litres = litres

    def get_litres(self):
        return self._litres

    def use(self, litres):
        self._litres = self._litres - litres

def test_three_uses():
    tank = OxygenTank(1.0)
    tank.use(0.1)
    tank.use(0.1)
    tank.use(0.1)
    assert tank.get_litres() == 0.7, "three uses of 0.1 leave 0.7"

test_three_uses()
```

It fails, and the tank is not to blame: `tank.get_litres()` is
`0.7000000000000001`. A decimal like 0.1 is stored very nearly, not
exactly, so decimals that should be equal can differ in the sixteenth
place. For decimals, a test asks "close enough?":

```python
    assert abs(tank.get_litres() - 0.7) < 0.000001, "three uses of 0.1 leave 0.7"
```

`abs()` gives the size of a difference without its sign. When a test
fails, the first question is which one is wrong: the code, or the test.

### Your turn: your class, sixth version

This is the sixth version of your class: five tests for it, at least one
of them at a boundary. On [Encapsulation](tutorial:keeping-details-inside-an-object)
each world's class left one door open. Write the test for that door
first, watch it fail, then close the door in the class cell. Your tests
go in the second cell: call each one at the bottom, as the first one is.
The cell runs them against your class, and against one good answer when
you compare.

<div class="dl-world" data-world="game">

```python exec
id: your-class-6--game
{{include: setup/oop/game-5.py}}
```

```solution
{{include: setup/oop/game-6.py}}
---
The one change is in `heal`: a negative amount is refused, as it is in
`take_damage`. Your tests run against this version too, when you
compare.
```

```python exec
id: your-class-6-tests--game
tests: your-class-6--game
def test_a_hit_takes_health():
    ada = Character("Ada", 10)
    ada.take_damage(3)
    assert ada.get_health() == 7

# Four more: one for heal(-50), and one at a boundary

test_a_hit_takes_health()
```

```hint
What should `heal(-50)` do to a character with 5 health? Where is the
boundary for health: what should a hit that leaves exactly 0 do, and a
heal that reaches exactly `max_health`?
```

</div>

<div class="dl-world" data-world="ocean">

```python exec
id: your-class-6--ocean
{{include: setup/oop/ocean-5.py}}
```

```solution
{{include: setup/oop/ocean-6.py}}
---
The one change is in `rise`, as on this page. Your tests run against
this version too, when you compare.
```

```python exec
id: your-class-6-tests--ocean
tests: your-class-6--ocean
def test_rise_refuses_a_negative_number():
    sub = Submarine("Nautilus")
    sub.rise(-500)
    assert sub.get_depth() == 0

# Four more: one for the Bathyscaphe, and one at a boundary

test_rise_refuses_a_negative_number()
```

```hint
Where are a bathyscaphe's boundaries? What should `room_below()` give
at the surface, and at exactly 11,000 m? What should an expedition with
two submarines say is deepest when both are at the same depth?
```

</div>

<div class="dl-world" data-world="solar-system">

```python exec
id: your-class-6--solar-system
{{include: setup/oop/solar-system-5.py}}
```

```solution
{{include: setup/oop/solar-system-6.py}}
---
The one change is in `can_burn`: a negative burn is never possible.
Because `burn` asks `can_burn`, the fix closes the door in both. Your
tests run against this version too, when you compare.
```

```python exec
id: your-class-6-tests--solar-system
tests: your-class-6--solar-system
def test_a_burn_uses_fuel():
    voyager = Probe("Voyager", 100)
    voyager.burn(30)
    assert voyager.get_fuel() == 70

# Four more: one for burn(-50), and one at a boundary

test_a_burn_uses_fuel()
```

```hint
What should `burn(-50)` do to a probe with 70 kg? Where is the boundary
for fuel: can a probe burn exactly all it has? What should `refuel` do
when the tank is exactly full?
```

</div>

<div class="dl-world" data-world="your-own">

Copy your classes from [Composition](tutorial:objects-inside-objects)
into the first cell. Which door did your class leave open? Write its test
first, in the second cell, and watch it fail. Then write four more, with
at least one at a boundary, and call each one at the bottom of the cell.

```python exec
id: your-class-6--your-own
# My classes so far
```

```python exec
id: your-class-6-tests--your-own
tests: your-class-6--your-own
# My five tests
```

</div>

## Looking back

On this page, a test was wrong once, and four classes were. When a test
fails, how will you decide which one to change?

A challenge: suspect D checked each dive alone. Can you write the one
test that D fails and every other suspect passes?

```python challenge
# Paste the five suspects from the top of the page here, then:

suspects = {"A": SubmarineA, "B": SubmarineB, "C": SubmarineC,
            "D": SubmarineD, "E": SubmarineE}

def test_only_d_fails(Sub):
    sub = Sub("Nautilus")
    # One test here

for name in suspects:
    try:
        test_only_d_fails(suspects[name])
        print(name, "passed")
    except AssertionError as error:
        print(name, "failed:", error)
```

Next, [Documenting a class](tutorial:documenting-a-class) writes down
what each method promises, in a form Python can test too.

## Where to read more

Everything here is covered elsewhere too, often in a form that will suit you
better than this one.

pytest. *Get Started*.
<https://docs.pytest.org/en/stable/getting-started.html>. The tool this
page's ten lines imitate, from installing it to the first failing test.

Beck, K. (2002). *Test-Driven Development: By Example*. Addison-Wesley.
The book that made "write the failing test first" a habit, worked through
on real code.

Python Software Foundation. *The Python Language Reference*, section
7.3, "The assert statement".
<https://docs.python.org/3/reference/simple_stmts.html#the-assert-statement>.
What `assert` does, exactly, and the one case where Python skips it.
