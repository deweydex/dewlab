---
title: "A class with many methods: giving one class more to do"
year: "2026-2027"
version: 2026.09.26.1
worlds:
  game: A game world, with characters, the things they carry, and rooms.
  ocean: An ocean expedition, with a submarine, its crew, and what they find.
  solar-system: A solar system, with planets, moons and the probes sent to them.
  your-own: A world of your own, with a class you design and grow page by page.
covers:
  giving-it-more-to-do:
    covers: [FOOP-LO4]
  data-that-belongs-together:
    covers: [FOOP-LO8]
  class-attributes-and-instance-attributes:
    covers: [FOOP-LO3]
    touches: [FOOP-LO8]
---

# A class with many methods: giving one class more to do

Light from the Sun takes time to reach a planet. Here is a class for a
planet, with one method, which finds how many minutes the light takes.
The distances are averages, in millions of kilometres. To Earth, it is
8.3 minutes. How long do you think it takes to reach Neptune?

```python exec
id: sunlight-1
class Planet:
    def __init__(self, name, distance):
        self.name = name
        self.distance = distance    # millions of km from the Sun

    def light_minutes(self):
        seconds = self.distance * 1000000 / 299792    # light: 299,792 km a second
        return round(seconds / 60, 1)

earth = Planet("Earth", 149.6)
neptune = Planet("Neptune", 4515.0)
print(earth.light_minutes())
print(neptune.light_minutes())
```

```predict
type: number
tolerance: 10

How many minutes for Neptune?
```

It prints `8.3`, then `251.0`: more than four hours. When you look at
Neptune through a telescope, you see it as it was four hours ago.

## Giving it more to do

A planet can answer more than one question. Below, the class grows two
more methods. `is_farther_than(other)` compares this planet with another
one. `describe()` makes a sentence, and asks `self.light_minutes()` for
its number. What will the two lines print?

```python exec
id: giving-it-more-to-do-1
class Planet:
    def __init__(self, name, distance):
        self.name = name
        self.distance = distance    # millions of km from the Sun

    def light_minutes(self):
        seconds = self.distance * 1000000 / 299792
        return round(seconds / 60, 1)

    def is_farther_than(self, other):    # new
        return self.distance > other.distance

    def describe(self):    # new
        return f"{self.name}: sunlight takes {self.light_minutes()} minutes"

earth = Planet("Earth", 149.6)
mars = Planet("Mars", 228.0)
print(mars.is_farther_than(earth))
print(mars.describe())
```

It prints `True`, then `Mars: sunlight takes 12.7 minutes`.

Look at what the new methods did not need. Neither one was given the
distance: both found it on `self`. `is_farther_than` also reads another
planet's distance, as `other.distance`, because `other` is a planet too.
And `describe` does not find the minutes again. It calls
`self.light_minutes()`: one method can use another, through `self`.

This is what *reusable* code means for a class. Each new job is a method
that can use everything the object already carries. It is written once,
and it works for every planet you make.

A stand-alone function can be reused just as well:
`light_minutes(distance)` would work on any distance. The difference is
where the data lives. The function needs the distance handed to it on
every call. The method finds it on the object, so a call only has to say
what is new.

Can you add a `light_hours()` method, which gives the time in hours,
rounded to one decimal place? Can it use `light_minutes()`?

```python exec
id: giving-it-more-to-do-2
class Planet:
    def __init__(self, name, distance):
        self.name = name
        self.distance = distance    # millions of km from the Sun

    def light_minutes(self):
        seconds = self.distance * 1000000 / 299792
        return round(seconds / 60, 1)

neptune = Planet("Neptune", 4515.0)
print(neptune.light_hours())
```

```inputs
Planet("Neptune", 4515.0).light_hours()
Planet("Jupiter", 778.5).light_hours()
```

```hint
There are 60 minutes in an hour. Which method already knows the minutes,
and how does a method ask another method on the same object?
```

```solution
class Planet:
    def __init__(self, name, distance):
        self.name = name
        self.distance = distance    # millions of km from the Sun

    def light_minutes(self):
        seconds = self.distance * 1000000 / 299792
        return round(seconds / 60, 1)

    def light_hours(self):    # new
        return round(self.light_minutes() / 60, 1)

neptune = Planet("Neptune", 4515.0)
print(neptune.light_hours())
---
4.2 hours. `light_hours` asks `light_minutes` and divides by 60, so the
sum is written in one place only. If the speed of light in
`light_minutes` were mistyped, fixing it there would fix both.
```

## Data that belongs together

An object can carry as many fields as it needs. A planet's moons belong
to it, so they can live on the planet too. This version leaves out the
methods from above, to keep the cell short. What will the last line print?

```python exec
id: data-that-belongs-together-1
class Planet:
    def __init__(self, name, distance):
        self.name = name
        self.distance = distance
        self._moons = []

    def add_moon(self, moon):
        if moon in self._moons:
            print(f"Refused: {moon} is already a moon of {self.name}.")
            return
        self._moons.append(moon)

    def moon_count(self):
        return len(self._moons)

earth = Planet("Earth", 149.6)
earth.add_moon("the Moon")
mars = Planet("Mars", 228.0)
mars.add_moon("Phobos")
mars.add_moon("Deimos")
mars.add_moon("Phobos")
for planet in [earth, mars]:
    print(planet.name, planet.moon_count())
```

```predict
What will the last line print?

- Mars 2
  - The second Phobos is refused.
- Mars 3
  - Every call to `add_moon` adds a moon.
```

The second Phobos is refused, and the last line is `Mars 2`.

Look at what the loop does not need. There is no second list of moon
counts to keep in step with a list of planets. Each planet carries its
own name, distance and moons. To get one planet's name and moons
together, we ask that one planet.

Why is `_moons` private, when `name` and `distance` are not? The moons
have a rule to keep: no moon is added twice. The name and the distance
never change after a planet is made, and no rule guards them. A field is
made private when there is a rule to keep.

## Class attributes and instance attributes

An *attribute* is any name we reach with a dot after an object, such as
`mars.name` or `mars.describe`. An *instance* is another word for an
object: `mars` is an instance of `Planet`.

The fields we set on `self` in `__init__` are *instance attributes*. An
instance attribute belongs to one object. Earth's distance and Mars's
distance are two separate values.

Sometimes a value is the same for every object of a class. Every planet
here orbits the same star. A *class attribute* is a value that belongs to
the class itself, and every object of that class shares it. We write it
inside the class, but outside any method.

In the cell below, `star` is a class attribute. Near the end, we change it
once, through the class. What will the last two lines print?

```python exec
id: class-attributes-and-instance-attributes-1
class Planet:
    star = "the Sun"

    def __init__(self, name, distance):
        self.name = name
        self.distance = distance

earth = Planet("Earth", 149.6)
mars = Planet("Mars", 228.0)
print(earth.name, "orbits", earth.star)
print(mars.name, "orbits", mars.star)

Planet.star = "Sol"    # the Sun's Latin name
print(earth.star)
print(mars.star)
```

Both planets show `Sol`. There is only one `star`, stored on the class,
and `earth.star` and `mars.star` both reach that one value. Their
distances stay separate, because each distance is an instance attribute.

A class attribute can also keep a count across every object. Here, the
constructor adds one to `planets_made` each time a planet is built. How
many does the last line report?

```python exec
id: class-attributes-and-instance-attributes-2
class Planet:
    planets_made = 0

    def __init__(self, name, distance):
        self.name = name
        self.distance = distance
        Planet.planets_made = Planet.planets_made + 1

mercury = Planet("Mercury", 57.9)
venus = Planet("Venus", 108.2)
earth = Planet("Earth", 149.6)
print(Planet.planets_made)
```

It prints `3`. The constructor writes `Planet.planets_made`, not
`self.planets_made`. The count belongs to the class, so we change it
through the class.

Most people make this mistake at least once. Storing a value under that name
through an object never changes the class attribute. It makes a new
instance attribute, on that one object:

```python
earth.star = "Proxima"
print(earth.star)     # Proxima
print(mars.star)      # Sol
print(Planet.star)    # Sol
```

So read a class attribute through any object, but change it through the
class.

| | Instance attribute | Class attribute |
|---|---|---|
| Where it is written | On `self`, usually in `__init__` | In the class, outside any method |
| Who has it | Each object has its own value | One value, shared by every object |
| Example | `self.distance = distance` | `star = "the Sun"` |
| How to change it | `mars.distance = 230.0` changes Mars's only | `Planet.star = "Sol"` changes it for every planet |

### Your turn: your class, third version

This is the third version of your class, from
[Encapsulation](tutorial:keeping-details-inside-an-object). It gets a
method that answers a question, used inside another method, and a class
attribute that every object shares.

<div class="dl-world" data-world="game">

Ada heals to 13, above the 10 a character can have, and Grace heals after
she is down. Can you give `Character` a class attribute
`max_health = 10`, and a method `is_down()`? Then can you make `heal`
refuse to heal a character who is down, using `is_down()`, and never go
above `max_health`?

```python exec
id: your-class-3--game
{{include: setup/oop/game-2.py}}

ada = Character("Ada", 8)
ada.heal(5)
print(ada)
grace = Character("Grace", 3)
grace.take_damage(5)
grace.heal(4)
print(grace)
```

```inputs
str(ada)
str(grace)
ada.is_down()
grace.is_down()
```

```hint
`is_down()` answers a question, so it returns `True` or `False`. Inside
`heal`, how do you ask it about this character? And `min()` gives the
smaller of two values, the way `max()` gives the larger.
```

```solution
{{include: setup/oop/game-3.py}}

ada = Character("Ada", 8)
ada.heal(5)
print(ada)
grace = Character("Grace", 3)
grace.take_damage(5)
grace.heal(4)
print(grace)
---
`Ada (health 10)`, then a refusal, and `Grace (health 0)`. `heal` asks
`self.is_down()`, and reads the limit as `Character.max_health`, so
changing that one line changes it for every character. What does
`ada.heal(-50)` do to this version?
```

</div>

<div class="dl-world" data-world="ocean">

The hull limit, 400, is written inside `dive`. Can you make it a class
attribute, `hull_limit = 400`? Then can you add a method `room_below()`,
which gives the metres left before the limit, and use it in `dive`'s
check?

```python exec
id: your-class-3--ocean
{{include: setup/oop/ocean-2.py}}

nautilus = Submarine("Nautilus")
nautilus.dive(300)
print(nautilus.room_below())
nautilus.dive(150)
print(nautilus)
```

```inputs
nautilus.room_below()
str(nautilus)
```

```hint
`room_below()` answers a question, so it returns a number: the limit take
away the depth. Inside `dive`, how do you ask it about this submarine?
And how does a method read a class attribute?
```

```solution
{{include: setup/oop/ocean-3.py}}

nautilus = Submarine("Nautilus")
nautilus.dive(300)
print(nautilus.room_below())
nautilus.dive(150)
print(nautilus)
---
`100`, a refusal, then `Nautilus at 300 m`. The limit is written once, as
`Submarine.hull_limit`, and `dive` asks `self.room_below()`. The real
Alvin is safe to 6,500 m. If your expedition had both, should the limit
still belong to the class?
```

</div>

<div class="dl-world" data-world="solar-system">

Voyager's tank holds 100 kg, but `refuel` will fill it past that. Can you
give `Probe` a class attribute `tank_size = 100`, and a method
`can_burn(kg)`? Then can you make `burn` use `can_burn` for its check, and
`refuel` never fill past `tank_size`?

```python exec
id: your-class-3--solar-system
{{include: setup/oop/solar-system-2.py}}

voyager = Probe("Voyager", 100)
voyager.burn(30)
print(voyager.can_burn(80))
voyager.refuel(50)
print(voyager)
```

```inputs
voyager.can_burn(80)
voyager.can_burn(100)
str(voyager)
```

```hint
`can_burn(kg)` answers a question, so it returns `True` or `False`.
Inside `burn`, how do you ask it about this probe? And `min()` gives the
smaller of two values, the way `max()` gives the larger.
```

```solution
{{include: setup/oop/solar-system-3.py}}

voyager = Probe("Voyager", 100)
voyager.burn(30)
print(voyager.can_burn(80))
voyager.refuel(50)
print(voyager)
---
`False`, then `Voyager (fuel 100 kg)`. `burn` asks `self.can_burn(kg)`,
and a caller can ask it too, before a burn. What does
`voyager.burn(-50)` do to this version?
```

</div>

<div class="dl-world" data-world="your-own">

Can you give your class a method that answers a question about one
object, and use it inside another method? And is there a value that every
object of your class shares, which could be a class attribute? Your class
from [Encapsulation](tutorial:keeping-details-inside-an-object) is saved
in that page's last cell: copy it here to start.

```python exec
id: your-class-3--your-own
# My class, third version: a question, used by another method.
```

</div>

## Looking back

Every method on this page found what it needed on `self`, with nothing
handed to it. So when does a method still need a parameter? Look at
`is_farther_than(other)` and `add_moon(moon)`: what do their parameters
bring that the object does not already have?

A challenge: Johannes Kepler found that a planet's year, in Earth years,
is its distance from the Sun, measured in Earth distances, to the power
1.5. Can you give `Planet` a `year_length()` method? How long is a year
on Neptune?

```python challenge
class Planet:
    def __init__(self, name, distance):
        self.name = name
        self.distance = distance    # millions of km from the Sun

    def year_length(self):
        # Earth is 149.6 million km from the Sun.
        return 0

print(Planet("Mars", 228.0).year_length())
print(Planet("Neptune", 4515.0).year_length())
```

Next, [A polynomial class: a project in many methods](tutorial:a-polynomial-class)
builds one class, a method at a time, from a ball thrown in the air. Or
go straight on to
[Inheritance: one class built on another](tutorial:one-parent-many-children),
which builds new classes out of the ones you have.

## Where to read more

Everything here is covered elsewhere too, often in a form that will suit you
better than this one.

Downey, A. B. (2015). *Think Python: How to Think Like a Computer
Scientist* (2nd ed.). Green Tea Press. Free at
<https://greenteapress.com/wp/think-python-2e/>. Chapter 17, "Classes and
methods", grows one class a method at a time, as this page did.

Python Software Foundation. *The Python Tutorial*, section 9.3.5, "Class
and Instance Variables".
<https://docs.python.org/3/tutorial/classes.html#class-and-instance-variables>.
The official reference on what belongs on the class, what belongs on
`self`, and the trap when a shared value is a list.

NASA. *Planetary Fact Sheet*.
<https://nssdc.gsfc.nasa.gov/planetary/factsheet/>. The distances on this
page, and much more about every planet, for your own `Planet` class.
