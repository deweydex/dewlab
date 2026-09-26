---
title: "A class with many methods: giving one class more to do — Practice"
practice_for: one-class-many-methods
year: "2026-2027"
version: 2026.09.26.1
---

# A class with many methods: giving one class more to do — Practice

Problems on classes with many methods and on class attributes, and three
from earlier pages. Try each problem before you open anything under it,
and run the cells to test your guesses.

## 1. Two questions for one planet

```python exec
id: two-questions-1
class Planet:
    def __init__(self, name, distance):
        self.name = name
        self.distance = distance    # millions of km from the Sun

    def light_minutes(self):
        seconds = self.distance * 1000000 / 299792
        return round(seconds / 60, 1)

    def is_farther_than(self, other):
        return self.distance > other.distance

    def describe(self):
        return f"{self.name}: sunlight takes {self.light_minutes()} minutes"

earth = Planet("Earth", 149.6)
mars = Planet("Mars", 228.0)
jupiter = Planet("Jupiter", 778.5)
print(earth.is_farther_than(mars))
print(jupiter.describe())
```

```predict
What will the last line print?

- Jupiter: sunlight takes 43.3 minutes
  - `describe` asks `light_minutes` for Jupiter's number.
- Jupiter: sunlight takes 8.3 minutes
  - `describe` gives Earth's number, the first planet made.
```

<details class="dl-answer"><summary>why</summary>

`False`, then `Jupiter: sunlight takes 43.3 minutes`. Earth is closer
than Mars, so it is not farther. Inside `describe`, `self` is `jupiter`,
so `self.light_minutes()` works on Jupiter's own distance.

</details>

## 2. The closer of two

Can you add a `closer_of(other)` method that returns whichever of the two
planets is closer to the Sun? Can it use `is_farther_than`?

```python exec
id: the-closer-of-two-1
class Planet:
    def __init__(self, name, distance):
        self.name = name
        self.distance = distance    # millions of km from the Sun

    def is_farther_than(self, other):
        return self.distance > other.distance

mars = Planet("Mars", 228.0)
earth = Planet("Earth", 149.6)
print(mars.closer_of(earth).name)
```

```inputs
Planet("Mars", 228.0).closer_of(Planet("Earth", 149.6)).name
Planet("Earth", 149.6).closer_of(Planet("Mars", 228.0)).name
```

```hint
The method returns a planet, not a name. If `self` is farther than
`other`, which one is closer?
```

```solution
class Planet:
    def __init__(self, name, distance):
        self.name = name
        self.distance = distance    # millions of km from the Sun

    def is_farther_than(self, other):
        return self.distance > other.distance

    def closer_of(self, other):
        if self.is_farther_than(other):
            return other
        return self

mars = Planet("Mars", 228.0)
earth = Planet("Earth", 149.6)
print(mars.closer_of(earth).name)
---
`Earth`, in both orders. The method returns a whole planet, so the
caller can ask it anything: its `.name`, or its `.distance`.
```

## 3. One star, renamed

```python exec
id: one-star-renamed-1
class Planet:
    star = "the Sun"

    def __init__(self, name):
        self.name = name

earth = Planet("Earth")
mars = Planet("Mars")
earth.star = "Proxima"
Planet.star = "Sol"
print(earth.star, mars.star)
```

```predict
What will it print?

- Proxima Sol
  - `earth.star = ...` made a new attribute on Earth alone.
- Sol Sol
  - Changing the class changes every planet.
- Proxima Proxima
  - `earth.star = ...` changed the class attribute.
```

<details class="dl-answer"><summary>why</summary>

`Proxima Sol`. `earth.star = "Proxima"` did not touch the class
attribute. It made a new instance attribute, on Earth alone, and from then
on `earth.star` finds that one first. Mars still reads the class's `star`,
which is now `Sol`.

</details>

## 4. A planet counter

```python exec
id: a-planet-counter-1
class Planet:
    planets_made = 0

    def __init__(self, name):
        self.name = name
        Planet.planets_made = Planet.planets_made + 1

for name in ["Mercury", "Venus", "Earth", "Mars"]:
    Planet(name)
print(Planet.planets_made)
```

```predict
type: number

What will it print?
```

<details class="dl-answer"><summary>why</summary>

`4`. Each `Planet(name)` runs `__init__`, which adds one to the count on
the class. None of the four planets was stored under a name, but each one
was made.

</details>

## 5. Moons for everyone

This class keeps its moons in a class attribute.

```python exec
id: moons-for-everyone-1
class Planet:
    moons = []

    def __init__(self, name):
        self.name = name

    def add_moon(self, moon):
        self.moons.append(moon)

mars = Planet("Mars")
earth = Planet("Earth")
mars.add_moon("Phobos")
print(earth.moons)
```

```predict
What will it print?

- ['Phobos']
  - There is one list, on the class, and every planet shares it.
- []
  - Earth has no moons added.
```

<details class="dl-answer"><summary>why</summary>

`['Phobos']`: Earth has Mars's moon. `moons = []` makes one list, on the
class. `self.moons.append(...)` does not store a new value under a name,
so it makes no instance attribute. It changes the one shared list. That is
why the tutorial's `Planet` makes `self._moons = []` inside `__init__`:
each planet gets a list of its own.

</details>

## 6. One limit or many

The Nautilus is safe to 400 m. Alvin, another real submarine, is safe to
6,500 m. Should `hull_limit` be a class attribute or an instance
attribute, if both are in your program?

<details class="dl-answer"><summary>one answer</summary>

An instance attribute: `self.hull_limit = hull_limit`, given to
`__init__` for each submarine. A class attribute says "every submarine is
the same here", and these two are not. If every submarine in your program
shares one limit, a class attribute is simpler.

</details>

## 7. From earlier: reaching in

From *Encapsulation*.

```python exec
id: from-earlier-reaching-in-1
class Planet:
    def __init__(self, name):
        self.name = name
        self._moons = []

    def add_moon(self, moon):
        if moon in self._moons:
            print("Refused: already a moon.")
            return
        self._moons.append(moon)

    def moon_count(self):
        return len(self._moons)

mars = Planet("Mars")
mars.add_moon("Phobos")
mars._moons.append("Phobos")
print(mars.moon_count())
```

```predict
type: number

What will it print?
```

<details class="dl-answer"><summary>why</summary>

`2`. The rule is in `add_moon`, and the last line but one went around it,
straight to the private list. The underscore asked it not to. Nothing
stopped it.

</details>

## 8. From earlier: one argument short

From *Your development environment: finding a bug inside a class*.

```python exec
id: from-earlier-one-argument-short-1
class Planet:
    def __init__(self, name, distance):
        self.name = name
        self.distance = distance

    def is_farther_than(self, other):
        return self.distance > other.distance

    def farther_of(self, other):
        if self.is_farther_than():
            return self
        return other

mars = Planet("Mars", 228.0)
earth = Planet("Earth", 149.6)
print(mars.farther_of(earth).name)
```

Run it, and read the traceback from the bottom. Which line do you change,
and to what?

<details class="dl-answer"><summary>answer</summary>

Line 10: `self.is_farther_than()` should be `self.is_farther_than(other)`.
The error, `missing 1 required positional argument: 'other'`, names the
method that is short of a value, and the line above it shows the call.
Fixed, it prints `Mars`.

</details>

## 9. From earlier: which move?

From *Sequence, selection and iteration inside a class*.

```python
def moon_count(self):
    count = 0
    for moon in self._moons:
        count = count + 1
    return count
```

```question
id: from-earlier-which-move-1
type: fill-in-the-blank

- `count = 0` is {storing|sequence|selection|iteration}.
- `for moon in self._moons:` is {iteration|storing|sequence|selection}.
- There is no {selection|storing|iteration} here: every moon counts.
```

<details class="dl-answer"><summary>why</summary>

The method stores a starting count, and repeats a step for each moon.
Nothing is chosen, because every moon is counted. `len(self._moons)`
gives the same answer in one line.

</details>
