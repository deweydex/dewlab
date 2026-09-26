---
title: "Documenting a class with docstrings — Practice"
practice_for: documenting-a-class
year: "2026-2027"
version: 2026.09.26.1
---

# Documenting a class with docstrings — Practice

Problems on docstrings and doctest, and three from earlier pages. Try
each problem before you open anything under it, and run the cells to test
your guesses.

## 1. Which docstring helps?

```question
id: which-docstring-helps-1
type: multiple-choice
answer: 3

A caller wants to know what `ada.heal(-50)` does. Which docstring tells
them?

- """Heals the character."""
  - It says what the method is for.
- """Add amount to health. Uses min() and max_health."""
  - It says how the method works inside.
- """Add amount to health, stopping at max_health. Refuses a negative amount, or a character who is down, and prints why."""
  - It says what the method promises, refusals included.
```

<details class="dl-answer"><summary>why</summary>

The third. The first repeats the method's name. The second tells the
caller about the inside, which they should not need, and which may change.
The third says what a caller can count on, including what happens with −50.

</details>

## 2. A promise for enter

Can you write a docstring for `Room.enter` that says the four things a
method promises: what it does, what its parameter should be, what comes
back, and what it refuses?

```python exec
id: a-promise-for-enter-1
class Room:
    def __init__(self, name):
        self.name = name
        self._characters = []

    def enter(self, character):
        if character in self._characters:
            print(f"Refused: {character} is already in {self.name}.")
            return
        self._characters.append(character)

help(Room.enter)
```

```solution
class Room:
    def __init__(self, name):
        self.name = name
        self._characters = []

    def enter(self, character):
        """Put character in the room.

        character: anyone who can be in a room.
        Refuses a character who is already inside, and prints why.
        Returns nothing.
        """
        if character in self._characters:
            print(f"Refused: {character} is already in {self.name}.")
            return
        self._characters.append(character)

help(Room.enter)
---
One good docstring. "Returns nothing" is worth saying: a caller who
writes `result = hall.enter(ada)` learns from it that `result` will be
`None`.
```

## 3. The same list, written differently

```python exec
id: the-same-list-written-differently-1
import doctest

class Room:
    def __init__(self, name):
        self.name = name
        self._names = []

    def enter(self, name):
        self._names.append(name)

    def standing(self):
        """Return the names inside.

        >>> hall = Room("Hall")
        >>> hall.enter("Ada")
        >>> hall.standing()
        ["Ada"]
        """
        return list(self._names)

doctest.run_docstring_examples(Room.standing, globals(), name="standing")
```

```question
id: the-same-list-written-differently-q1
type: multiple-choice
answer: 2

Does the example pass?

- Yes: `["Ada"]` and `['Ada']` are the same list.
  - Python treats both quotes alike.
- No: doctest compares the text Python would show, and Python shows `['Ada']`.
  - doctest checks what is printed, character by character.
```

<details class="dl-answer"><summary>why</summary>

It fails, with `Expected: ["Ada"]` and `Got: ['Ada']`. doctest does not
compare values: it compares the text Python shows, and Python shows a list
of strings with single quotes. Write the example the way Python would show
the answer.

</details>

## 4. A docstring that stopped telling the truth

This method's code and its docstring disagree. Run the cell. Which one
would you change?

```python exec
id: a-docstring-that-stopped-1
import doctest

class Submarine:
    hull_limit = 400

    def __init__(self, name):
        self.name = name
        self._depth = 0

    def can_dive(self, metres):
        """Return True if the submarine can dive metres deeper.

        >>> Submarine("Nautilus").can_dive(400)
        True
        """
        return self._depth + metres < self.hull_limit

doctest.run_docstring_examples(Submarine.can_dive, globals(), name="can_dive")
```

<details class="dl-answer"><summary>answer</summary>

The example expects a dive to exactly 400 m to be allowed, and the code
says no: it uses `<`. The hull is safe to 400 m, so the code is wrong
and the docstring is right. Change `<` to `<=`. Sometimes it is the other
way round, and the docstring is out of date. Either way, the example is
what found the disagreement.

</details>

## 5. Where does it go?

```question
id: where-does-it-go-1
type: fill-in-the-blank

- A class docstring goes on the {first line inside the class|line above the class|last line of __init__}.
- A method docstring goes on the {first line inside the method|line above the method|line after return}.
- An example in a docstring starts with {>>>|#|print}.
```

## 6. From earlier: a test at the edge

From *Testing a class*. `Probe.can_burn(kg)` says whether a probe can
burn `kg` now. A probe has 70 kg. Which two values of `kg` would you test
first, and why?

<details class="dl-answer"><summary>one answer</summary>

70 and 71: exactly all of the fuel, and one kilogram past it. That is the
boundary, where a `<` written for `<=` would show. 0 and −1 are the other
edge.

</details>

## 7. From earlier: what the container asks

From *Composition*. `Mission.total_fuel()` adds `probe.get_fuel()` for
each probe. Someone changes it to add `probe._fuel` instead. Both give the
same number today. What could make them differ later?

<details class="dl-answer"><summary>answer</summary>

A change inside `Probe`: say the fuel is stored in grams, or a child
class keeps a reserve that `get_fuel` leaves out. `get_fuel()` would keep
its promise, and `_fuel` would not. A docstring on `get_fuel` is where
that promise is written down.

</details>

## 8. From earlier: one sentence for a child class

From *Inheritance*. A class starts:

```python
class Bathyscaphe(Submarine):
    hull_limit = 11000
```

Can you write its class docstring in one sentence, the same sentence you
might have written as the reason for the child class?

<details class="dl-answer"><summary>one answer</summary>

`"""A submarine built for the deepest trenches: its hull is safe to
11,000 m."""` The reason a child class exists is the most useful thing
its docstring can say.

</details>
