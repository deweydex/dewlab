---
title: "Testing a class: hunting for the bug — Practice"
practice_for: testing-what-a-class-does
year: "2026-2027"
version: 2026.09.26.1
---

# Testing a class: hunting for the bug — Practice

This page has problems on tests, boundaries and runners, and three from
earlier pages.
Try each problem before you open anything under it, and run the cells to
test your guesses.

## 1. Where are the boundaries?

`take_damage` refuses a negative amount, and health stops at 0. A
character has 10 health.

```question
id: where-are-the-boundaries-1
type: fill-in-the-blank

- A hit of {10|5|3} is at a boundary: it leaves exactly 0.
- A hit of {0|5|3} is at a boundary too: the smallest amount that is not refused.
- A hit of {11|5|3} is one step past a boundary: it would leave −1.
```

<details class="dl-answer"><summary>why</summary>

10, 0 and 11. A hit of 5 is in the middle, where bugs are least likely.
A `>` written as `>=`, or a missing `max(0, ...)`, would show itself in
tests at 0, 10 and 11.

</details>

## 2. Which tests run?

```python exec
id: which-tests-run-1
def test_one():
    pass

def check_two():
    assert 1 + 1 == 3, "check_two"

def test_three():
    assert 1 + 1 == 3, "sums"

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

- 1 passed, 1 failed
  - Only names that start with `test_` are run.
- 1 passed, 2 failed
  - Every function with an `assert` in it is a test.
- 2 passed, 1 failed
  - `check_two` passes because it is never called.
```

<details class="dl-answer"><summary>why</summary>

`FAILED test_three sums`, then `1 passed, 1 failed`. `check_two` is never
run: its name does not start with `test_`. pytest works the same way, so
a test with the wrong name never runs, and nothing tells you.

</details>

## 3. Twice in the hall

This `Room` should refuse anyone already inside, and does not. Can you
write a test that fails on this version, then fix the class so the test
passes?

```python exec
id: twice-in-the-hall-1
class Room:
    def __init__(self, name):
        self.name = name
        self._characters = []

    def enter(self, character):
        self._characters.append(character)

    def count(self):
        return len(self._characters)
```

```python exec
id: twice-in-the-hall-tests
tests: twice-in-the-hall-1
def test_nobody_enters_twice():
    hall = Room("Hall")
    hall.enter("Ada")
    hall.enter("Ada")
    assert hall.count() == 1

test_nobody_enters_twice()
```

```solution
for: twice-in-the-hall-1
class Room:
    def __init__(self, name):
        self.name = name
        self._characters = []

    def enter(self, character):
        if character in self._characters:
            print(f"Refused: {character} is already in {self.name}.")
            return
        self._characters.append(character)

    def count(self):
        return len(self._characters)
---
The test builds a room, sends Ada in twice, and expects a count of 1.
It fails on the first version, with a count of 2, and passes on this one.
```

## 4. A test that is wrong

```python exec
id: a-test-that-is-wrong-1
def test_three_tenths():
    assert 0.1 * 3 == 0.3, "three tenths"

test_three_tenths()
```

Run it. Is the code wrong, or the test? Can you fix whichever it is?

<details class="dl-answer"><summary>answer</summary>

The test. `0.1 * 3` is `0.30000000000000004`, very nearly 0.3, because
0.1 is stored very nearly, not exactly. For decimals, a test asks "close
enough?": `assert abs(0.1 * 3 - 0.3) < 0.000001`.

</details>

## 5. What pytest adds

The ten-line runner on the tutorial page finds and runs every `test_`
function. What would you want a real test tool to do that those ten lines
do not?

<details class="dl-answer"><summary>one answer</summary>

Find tests in every file, not only on one page. Say which line of a test
failed, and what the values were. Run only the tests you name. Run each
test with a fresh start, so no test changes anything the next one uses.
pytest does all of these.

</details>

## 6. From earlier: the same object in two places

From *Composition*.

```python exec
id: from-earlier-the-same-object-1
class Mission:
    def __init__(self, name):
        self.name = name
        self._probes = []

    def launch(self, probe):
        self._probes.append(probe)

    def count(self):
        return len(self._probes)

outer = Mission("Outer")
inner = Mission("Inner")
outer.launch("Voyager")
inner.launch("Voyager")
print(outer.count() + inner.count())
```

```predict
type: number

What will it print?
```

<details class="dl-answer"><summary>why</summary>

`2`. Each mission keeps its own list, made in its own `__init__`, so
each counts one. The same name in both lists is two entries, not one
shared one.

</details>

## 7. From earlier: through the parent

From *Inheritance*. A `Knight(Character)` overrides `take_damage` to call
`super().take_damage(max(0, amount - 2))`. Which of these tests does the
knight pass, if `Character` is right?

- (a) A hit of 5 leaves a knight of 10 health at 7.
- (b) A hit of −3 leaves a knight at 10.
- (c) A hit of 20 leaves a knight at 0.

<details class="dl-answer"><summary>answer</summary>

All three. (a) 5 − 2 = 3. (b) `max(0, -5)` is 0, and a hit of 0 changes
nothing. (c) 18 is passed to the parent, whose `max(0, ...)` stops health
at 0. The knight passes (b) and (c) because it uses `super()`. The
parent's rules do that work.

</details>

## 8. From earlier: a skeleton's first test

From *Designing classes*. A skeleton's methods all say `pass`. What does
a test of a skeleton's method show, and why might you write one before
the method?

<details class="dl-answer"><summary>one answer</summary>

It fails, since `pass` returns `None`. Written before the method, the
test says exactly what the method must do, and the method is finished
when the test passes. This is test first, as on the tutorial page.

</details>
