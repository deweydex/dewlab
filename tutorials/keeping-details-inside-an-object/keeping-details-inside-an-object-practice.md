---
title: "Encapsulation: keeping an object's data behind its methods — Practice"
practice_for: keeping-details-inside-an-object
year: "2026-2027"
version: 2026.09.26.1
---

# Encapsulation: keeping an object's data behind its methods — Practice

Problems on keeping rules inside a class, and three from earlier pages.
Try each problem before you open anything under it, and run the cells to
test your guesses.

## 1. Around the rule

```python exec
id: around-the-rule-1
class Probe:
    def __init__(self, name, fuel):
        self.name = name
        self._fuel = fuel

    def get_fuel(self):
        return self._fuel

    def burn(self, kg):
        if kg > self._fuel:
            print("Refused: not enough fuel for that burn.")
            return
        self._fuel = self._fuel - kg

voyager = Probe("Voyager", 70)
voyager.burn(80)
voyager._fuel = voyager._fuel - 80
print(voyager.get_fuel())
```

```predict
What will the last line print?

- -10
  - The line that reaches in to `_fuel` goes around the rule.
- 70
  - The rule in `burn` keeps the fuel safe.
- 0
  - Fuel cannot go below empty.
```

<details class="dl-answer"><summary>why</summary>

The refusal, then `-10`. `burn` refused the first burn. The next line
reached in to `_fuel` and took 80 away directly, and nothing checked it.
The underscore asked it not to. It could not stop it.

</details>

## 2. Room for four

The Nautilus has room for 4 crew. Can you make `board` refuse anyone
once there are already 4 on board?

```python exec
id: room-for-four-1
class Submarine:
    def __init__(self, name):
        self.name = name
        self._crew = []

    def get_crew(self):
        return self._crew

    def board(self, person):
        self._crew.append(person)

nautilus = Submarine("Nautilus")
for person in ["Ada", "Grace", "Alan", "Katherine", "Mary"]:
    nautilus.board(person)
print(nautilus.get_crew())
```

```inputs
nautilus.get_crew()
```

```hint
`len()` gives the number of items in a list. How many are on board when
`board` should say no?
```

```solution
class Submarine:
    def __init__(self, name):
        self.name = name
        self._crew = []

    def get_crew(self):
        return self._crew

    def board(self, person):
        if len(self._crew) >= 4:
            print("Refused: the Nautilus has room for 4.")
            return
        self._crew.append(person)

nautilus = Submarine("Nautilus")
for person in ["Ada", "Grace", "Alan", "Katherine", "Mary"]:
    nautilus.board(person)
print(nautilus.get_crew())
---
One refusal, for Mary, then `['Ada', 'Grace', 'Alan', 'Katherine']`.
`>= 4` refuses the fifth: with 4 on board, there is no room left.
```

## 3. The heating

```python exec
id: the-heating-1
class Thermostat:
    def __init__(self, temperature):
        self._temperature = temperature

    def get_temperature(self):
        return self._temperature

    def set_temperature(self, new_temperature):
        if new_temperature < 5 or new_temperature > 30:
            print("Refused: choose 5 to 30 degrees.")
            return
        self._temperature = new_temperature

heating = Thermostat(20)
heating.set_temperature(35)
heating.set_temperature(22)
print(heating.get_temperature())
heating._temperature = 50
print(heating.get_temperature())
```

Before you run it: what are the three lines of output? And why write
`heating.set_temperature(22)` rather than `heating._temperature = 22`,
when both give the same result here?

<details class="dl-answer"><summary>answer</summary>

`Refused: choose 5 to 30 degrees.`, then `22`, then `50`. The underscore
did not stop `heating._temperature = 50`.

`22` is a safe value, so today both lines give the same result. But the
next value might not be safe, and only the method checks it. Calling the
method means the check always runs.

</details>

## 4. Which are private?

Which of these names, written inside a class, does the class's writer
mean to be private?

- `self.name`
- `self._oxygen`
- `self.get_oxygen`
- `self._alarms`

<details class="dl-answer"><summary>answer</summary>

`self._oxygen` and `self._alarms`: both start with one underscore.
`self.name` has none, so other code may use it. `get_oxygen` has none
either. If it exists, it is a method the writer means other code to call.

</details>

## 5. Enough for the trip

```python exec
id: enough-for-the-trip-1
class OxygenTank:
    def __init__(self, litres):
        self._millilitres = round(litres * 1000)

    def has_enough(self, litres):
        return round(litres * 1000) <= self._millilitres

spare = OxygenTank(1.0)
print(spare.has_enough(0.999))
print(spare.has_enough(1.001))
print(spare.has_enough(1.0))
```

```predict
What will the last line print?

- True
  - Exactly 1 litre is 1000 ml, and `<=` allows equal.
- False
  - Using all of the oxygen leaves nothing, so it is not enough.
```

<details class="dl-answer"><summary>why</summary>

`True`, `False`, `True`. The tank holds 1000 ml. 0.999 litres is 999 ml,
so `True`. 1.001 litres is 1001 ml, so `False`. 1.0 litres is exactly
1000 ml, and `<=` allows equal, so `True`.

</details>

## 6. A change the callers never see

A caller writes `print(spare.get_litres())` for the tank on the tutorial
page. Later, the class goes back to storing litres, in `_litres`. Does the
caller's line need to change? What if the caller had written
`print(spare._millilitres / 1000)` instead?

<details class="dl-answer"><summary>answer</summary>

`print(spare.get_litres())` does not need to change. The class's writer
changes `get_litres()` to return `self._litres`, and every caller gets
the new version.

`print(spare._millilitres / 1000)` stops with an `AttributeError`,
because the object has no `_millilitres` field any more. Callers that
used only the methods are safe. Callers that reached in are not.

</details>

## 7. Two ideas, one class

Encapsulation and abstraction usually come together. Are they two names
for one idea, or two ideas?

<details class="dl-answer"><summary>one answer</summary>

Two ideas, seen from two sides. Encapsulation is about where the data and
its rules live: behind the class's own methods. Abstraction is about what
a caller has to know: what `dive(250)` does, not the `if` inside it.
Keeping the data behind methods is what lets a caller see only the
methods.

</details>

## 8. From earlier: a rule that forgot self

From *Your development environment: finding a bug inside a class*.

```python exec
id: from-earlier-a-rule-that-forgot-self-1
class Character:
    def __init__(self, name, health):
        self.name = name
        self._health = health

    def heal(self, amount):
        if _health + amount > 10:
            print("Refused: health cannot go above 10.")
            return
        self._health = self._health + amount

ada = Character("Ada", 4)
ada.heal(3)
```

Run it, and read the traceback from the bottom. Which line do you change,
and to what?

<details class="dl-answer"><summary>answer</summary>

Line 7, the check: `_health` should be `self._health`. The last line of
the error says so, and suggests it: `name '_health' is not defined. Did
you mean: 'self._health'?` A field is always reached through `self`, even
a private one.

</details>

## 9. From earlier: printed, not returned

From *Classes and objects*.

```python exec
id: from-earlier-printed-not-returned-2
class Character:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        print(self.name)

ada = Character("Ada")
print(ada)
```

```question
id: from-earlier-printed-not-returned-q2
type: multiple-choice
answer: 3

What happens when it runs?

- It prints `Ada`.
  - `__str__` shows the name.
- It prints `Ada` twice.
  - `__str__` prints once, and `print()` prints again.
- It prints `Ada`, then stops with an error.
  - `__str__` has to return text, and this one returns nothing.
```

<details class="dl-answer"><summary>why</summary>

`Ada`, from the `print()` inside `__str__`, then a `TypeError`:
`__str__ returned non-string (type NoneType)`. `print(ada)` asks
`__str__` for text to show. This one prints the name itself and returns
nothing. Write `return self.name`, and let `print()` do the printing.

</details>

## 10. From earlier: storing on self

From *Sequence, selection and iteration inside a class*. This submarine
should count the refusals from its hull limit. What will the last line
print?

```python exec
id: from-earlier-storing-on-self-1
class Submarine:
    def __init__(self, name):
        self.name = name
        self._depth = 0
        self._refusals = 0

    def dive(self, metres):
        if self._depth + metres > 400:
            refusals = self._refusals + 1
            return
        self._depth = self._depth + metres

nautilus = Submarine("Nautilus")
nautilus.dive(500)
nautilus.dive(600)
print(nautilus._refusals)
```

```predict
What will the last line print?

- 0
  - `refusals` is a plain name, so `self._refusals` never changes.
- 2
  - Both dives were refused, and each one counted.
```

<details class="dl-answer"><summary>why</summary>

`0`. The count was stored in a plain name, which vanished when `dive`
ended. It should be `self._refusals = self._refusals + 1`. (And the last
line reaches in to a private field. A getter, `get_refusals()`, would be
the polite way to ask.)

</details>
