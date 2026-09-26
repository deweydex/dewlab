---
title: "Sequence, selection and iteration inside a class — Practice"
practice_for: the-moves-you-already-know
year: "2026-2027"
version: 2026.09.26.1
---

# Sequence, selection and iteration inside a class — Practice

This page has problems on the four moves inside a class, and three from
earlier pages.
Try each problem before you open anything under it, and run the cells to
test your guesses.

## 1. A loop that chooses when to stop

This method burns a probe's fuel in steps of 10 kg:

```python
def burn_all(self):
    burns = 0
    while self.fuel >= 10:
        self.fuel = self.fuel - 10
        burns = burns + 1
    return burns
```

```question
id: a-loop-that-chooses-1
type: fill-in-the-blank

- `burns = 0` is {storing|sequence|selection|iteration}.
- `while self.fuel >= 10:` is {iteration|storing|sequence|selection}.
- `self.fuel = self.fuel - 10` is {storing|sequence|selection|iteration}.
```

<details class="dl-answer"><summary>why</summary>

A `while` line has a condition in it, like an `if`, so it can look like
selection. But its job is to repeat. It runs its lines again and again,
and the condition only decides when to stop. That makes it iteration.
`self.fuel = self.fuel - 10` stores on the object, so the fuel stays
burnt after the method ends.

</details>

## 2. Two names that look alike

```python exec
id: two-names-that-look-alike-1
class Room:
    def __init__(self, name):
        self.name = name
        self.visits = 0

    def enter(self):
        self.visits = self.visits + 1
        visits = 100

hall = Room("Hall")
hall.enter()
hall.enter()
print(hall.visits)
```

```predict
What will it print?

- 2
  - `visits = 100` stores in a plain name, which vanishes when `enter` ends.
- 100
  - The last line of `enter` sets the visits to 100.
- 102
  - The two visits are added to 100.
```

<details class="dl-answer"><summary>why</summary>

`2`. `visits` and `self.visits` are two different names. `visits = 100`
stores 100 in a plain name, inside one call of `enter`, and it is gone
when the call ends. Only `self.visits` stays with the room.

</details>

## 3. The same question twice

```python exec
id: the-same-question-twice-1
class Planet:
    def __init__(self, name, moons):
        self.name = name
        self.moons = moons

    def moons_wider_than(self, km):
        count = 0
        for width in self.moons:
            if width > km:
                count = count + 1
        return count

jupiter = Planet("Jupiter", [3643, 3122, 5268, 4821])
print(jupiter.moons_wider_than(3000))
print(jupiter.moons_wider_than(3000))
```

```predict
What will the second line print?

- 4
  - Each call starts `count` from 0 again.
- 8
  - The second call adds to the first call's count.
```

<details class="dl-answer"><summary>why</summary>

`4`, both times. `count = 0` is the first line of the method, so every
call starts from 0. That is why `count` is a plain name and not
`self.count`. If it lived on the object, what would the second call
print?

</details>

## 4. The narrowest moon

Can you give `Planet` a `narrowest_moon()` method?

```python exec
id: the-narrowest-moon-1
class Planet:
    def __init__(self, name, moons):
        self.name = name
        self.moons = moons

jupiter = Planet("Jupiter", [3643, 3122, 5268, 4821])
print(jupiter.narrowest_moon())
```

```inputs
Planet("Jupiter", [3643, 3122, 5268, 4821]).narrowest_moon()
Planet("Mars", [22, 12]).narrowest_moon()
Planet("Earth", [3475]).narrowest_moon()
```

```solution
title: with what you've met so far
class Planet:
    def __init__(self, name, moons):
        self.name = name
        self.moons = moons

    def narrowest_moon(self):
        best = self.moons[0]
        for width in self.moons:
            if width < best:
                best = width
        return best

jupiter = Planet("Jupiter", [3643, 3122, 5268, 4821])
print(jupiter.narrowest_moon())
---
3122: Europa. The same shape as `widest_moon()`, with `<` in place of `>`.
```

```solution
title: a shorter way
class Planet:
    def __init__(self, name, moons):
        self.name = name
        self.moons = moons

    def narrowest_moon(self):
        return min(self.moons)

jupiter = Planet("Jupiter", [3643, 3122, 5268, 4821])
print(jupiter.narrowest_moon())
---
`min()` runs the loop for you.
```

## 5. Deepest, too soon

This `deepest()` method has one line in the wrong place.

```python exec
id: deepest-too-soon-1
class Logbook:
    def __init__(self, submarine, depths):
        self.submarine = submarine
        self.depths = depths

    def deepest(self):
        best = self.depths[0]
        for depth in self.depths:
            if depth > best:
                best = depth
            return best

log = Logbook("Nautilus", [120, 340, 85])
print(log.deepest())
```

```predict
What will it print?

- 120
  - `return` is inside the loop, so the method stops on the first depth.
- 340
  - The loop looks at every depth before it returns.
- 85
  - `best` ends as the last depth in the list.
```

<details class="dl-answer"><summary>why</summary>

`120`. `return best` is indented under the `for`, so it is one of the
lines that repeat. It runs with the first depth, and a `return` ends the
method there. Take four spaces away from the front of it, so it starts in
the same column as `for`, and it runs once, after the loop: 340. No line
moved. The indent changed which lines repeat.

</details>

## 6. How heavy is the backpack?

Can you give `Backpack` a `total_weight()` method that adds every weight
in it?

```python exec
id: how-heavy-1
class Backpack:
    def __init__(self, owner, weights):
        self.owner = owner
        self.weights = weights

ada = Backpack("Ada", [2, 5, 1, 3])
print(ada.total_weight())
```

```inputs
Backpack("Ada", [2, 5, 1, 3]).total_weight()
Backpack("Grace", []).total_weight()
Backpack("Alan", [4]).total_weight()
```

```solution
title: with what you've met so far
class Backpack:
    def __init__(self, owner, weights):
        self.owner = owner
        self.weights = weights

    def total_weight(self):
        total = 0
        for weight in self.weights:
            total = total + weight
        return total

ada = Backpack("Ada", [2, 5, 1, 3])
print(ada.total_weight())
---
11 kg. An empty backpack gives 0, because the loop never runs and `total`
stays as it started. There is no selection here: every weight counts.
```

```solution
title: a shorter way
class Backpack:
    def __init__(self, owner, weights):
        self.owner = owner
        self.weights = weights

    def total_weight(self):
        return sum(self.weights)

ada = Backpack("Ada", [2, 5, 1, 3])
print(ada.total_weight())
```

## 7. A fifth move?

A class gives a program `self`, `__init__` and methods. Does it give it a
fifth move, beside storing, sequence, selection and iteration?

<details class="dl-answer"><summary>one answer</summary>

No, it does not add a fifth move. A class adds a second place to store
values: on the object, through `self`, where a value lasts from one method call to the
next and every method can reach it. The code inside each method is still
built from the same four moves.

</details>

## 8. From earlier: a slip in a name

From *Classes and objects*.

```python exec
id: from-earlier-a-slip-in-a-name-1
class Character:
    def __init__(self, name, health):
        self.name = name
        self.health = health

grace = Character("Grace", 8)
grace.heath = 3
print(grace.health)
```

```predict
What will it print?

- 8
  - `heath` is a new field, so `health` is unchanged.
- 3
  - The line sets Grace's health to 3.
- An error
  - A `Character` has no field called `heath`.
```

<details class="dl-answer"><summary>why</summary>

`8`. If you store on an object under a new name, you make a new field,
quietly, the way a misspelt key made a new entry in a dictionary. A slip in a
method's name, such as `grace.take_damge(5)`, stops with an error
instead.

</details>

## 9. From earlier: printed, not returned

From *Writing your own functions*.

```python exec
id: from-earlier-printed-not-returned-1
def double(n):
    print(n * 2)

result = double(4)
print(result)
```

```predict
What will the last line print?

- None
  - `double` prints its answer, but returns nothing.
- 8
  - `double(4)` is 8.
```

<details class="dl-answer"><summary>why</summary>

The cell shows `8`, then `None`. The `8` comes from the `print()` inside
`double`. The function has no `return`, so `result` is `None`. A method is
the same. `heaviest()` has to `return` its answer for a caller to use it.

</details>

## 10. From earlier: a loop that counts

From *Repeating steps with loops*. How many lines does this print, and
what is the last one?

```python
for step in range(2, 11, 3):
    print(step)
```

<details class="dl-answer"><summary>answer</summary>

Three lines: 2, 5 and 8. `range(2, 11, 3)` starts at 2, adds 3 each time,
and stops before it reaches 11.

</details>
