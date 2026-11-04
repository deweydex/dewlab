---
title: "Inheritance: a closer look at \"is a\""
year: "2026-2027"
version: 2026.11.04.3
---

# Inheritance: a closer look at "is a"

In [Inheritance: one class built on another](tutorial:one-parent-many-children),
`class Troll(Character):` said "a troll is a character, plus something
different". The words "is a" are a good guide to when a child class fits.
But are they always enough? Here are two ideas. Both are reasonable, and
they cannot both be true.

**Idea A.** If every X is a Y in real life, or in maths, then `X(Y)` is a
safe child class. A square is a rectangle, so `Square(Rectangle)` is safe.

**Idea B.** A child class promises to do everything its parent can do,
and to stay what it is. If one of the parent's methods would break the
child's own rule, the child class does not fit, whatever real life says.

## An experiment

Here is a rectangle that can be stretched sideways, and a square built on
it. A square's rule is that its width and its height are the same.

```python exec
id: an-experiment-1
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def stretch(self, factor):
        self.width = self.width * factor

class Square(Rectangle):
    def __init__(self, side):
        super().__init__(side, side)

tile = Square(3)
tile.stretch(2)
print("width", tile.width, "height", tile.height, "area", tile.area())
```

Idea A says the square stays a square: a square is a rectangle, so it can
do whatever a rectangle does. Idea B says `stretch` changes one side only,
so the square will break its own rule.

```predict
type: choice

What will it print?

- width 6 height 6 area 36
  - This is what idea A predicts: a square stays a square, because it belongs to the group of rectangles.
- width 6 height 3 area 18
  - This is what idea B predicts: `stretch` changes one side only.
- An error
  - This reads `stretch` as a method a square refuses to run.
```

Run it. It prints `width 6 height 3 area 18`. Python raised no error, and
`tile` is still a `Square` object. But its sides are 6 and 3, so it is not
a square any more. The class did not keep its own rule, as idea B
predicted.

Can you change `Square` so that stretching keeps it square? Is the result
still something a program using rectangles would expect?

<details class="dl-answer"><summary>one change, and what it costs</summary>

`Square` can have its own `stretch`, which changes both sides:

    def stretch(self, factor):
        self.width = self.width * factor
        self.height = self.height * factor

Now a square stays square. But a program that stretched every rectangle
sideways, to make a row of them twice as wide, now gets squares that are
also twice as tall. The child keeps its rule by breaking the parent's
promise. One answer is to give the two classes a parent they can both
keep the promises of, such as a `Shape` with `area`, and no `stretch`.

</details>

## What each idea checks

The two ideas ask different questions about `Square(Rectangle)`.

Idea A asks whether every square belongs to the group of rectangles. In
maths it does: four right angles, with opposite sides equal. A square adds
one rule, that its sides are equal. A maths square never changes, so the
group is all there is to check.

Idea B asks what a program can do to the object. A square in a program has
methods, and each method can change it. So idea B looks at every method the
parent hands down. After the method runs, does the child still keep its own
rule?

The two ideas differ at `stretch`. Idea A checks only the group, so it never
runs `stretch`. Idea B runs `stretch(2)` and finds sides of 6 and 3. "Is a"
in a program means "can be used anywhere the parent is used, and nothing
breaks". Computer scientists call this the *Liskov substitution principle*,
after Barbara Liskov, who described it in 1987.

Let's move the stretch factor ourselves. The slider sets the number we pass
to `stretch`.

```python exec
id: what-each-idea-checks-1
factor = slider("factor", 1, 6, step=1, value=2, id="stretch-factor").value

tile = Square(3)
tile.stretch(factor)
print("stretch by", factor)
print("width", tile.width, "height", tile.height, "area", tile.area())
print("sides equal:", tile.width == tile.height)
```

Can you find a factor that leaves the square a square? What does that factor
do to a rectangle?

## Where else it happens

A penguin is a bird. Here is a `Bird` class with a method every bird in
this program is meant to have. What will the last line do?

```python exec
id: where-else-it-happens-1
class Bird:
    def fly(self):
        return "flies away"

class Penguin(Bird):
    def fly(self):
        return "cannot fly"

for bird in [Bird(), Penguin()]:
    print(bird.fly())
```

A program that tells every bird to fly when a cat comes cannot move the
penguin. Is `Penguin(Bird)` a good child class here? What would you
change about `Bird`?

## Where to read more

Barbara Liskov won the Turing Award in 2008. Her 1987 talk, *Data
Abstraction and Hierarchy*, is where the principle comes from.
