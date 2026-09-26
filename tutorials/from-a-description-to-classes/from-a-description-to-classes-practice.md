---
title: "Designing classes: from a description to classes — Practice"
practice_for: from-a-description-to-classes
year: "2026-2027"
version: 2026.09.26.1
---

# Designing classes: from a description to classes — Practice

This page has problems on turning a description into classes, and three
from earlier pages. Most have more than one good answer. The answers under them say
what was chosen, and why.

## 1. Class or field?

A library's description says: "Each book has a title, an author and a due
date. Members borrow books, and a member may have at most five at once."

```question
id: class-or-field-1
type: fill-in-the-blank

- A book's title is best as a {field|class of its own}.
- A member is best as a {class of its own|field of Book}: it keeps a rule about five books.
- A due date is best as a {field|class of its own}, at least until it needs rules of its own.
```

<details class="dl-answer"><summary>why</summary>

A title is one value, so it is a field. A member knows things (a name,
the books borrowed) and keeps a rule (at most five), so it needs a
class. A due date is one value today. If the library later charged fines
by the day, a date with its own questions might become a class.

</details>

## 2. Nouns on a bus

> A bus company runs buses on routes. Each route has a number and a list
> of stops. Each bus has a driver and seats for 50. A passenger taps a
> card to get on, and the card's balance pays the fare.

Which nouns would you make classes? Write your cards before you open the
answer.

<details class="dl-answer"><summary>one answer</summary>

`Route` (a number and its stops; could answer "does this route stop
here?"), `Bus` (a route, a driver, and the rule of 50 seats), and `Card`
(a balance, and the rule that a fare needs enough of it). The driver and
the stop are names, as fields, until they need to do something. The
passenger is interesting. In this description, the card does everything
a passenger does. Another good answer makes `Passenger` the class that
has a card.

</details>

## 3. Whose rule is it?

```question
id: whose-rule-is-it-1
type: multiple-choice
answer: 2

"A book can be borrowed by one member at a time." Which class is the most
natural home for that rule?

- `Member`
  - The member does the borrowing.
- `Book`
  - The book knows whether it is out, so it can refuse a second loan.
- `Library`
  - The library sees every book and every member.
```

<details class="dl-answer"><summary>why</summary>

`Book` is one good home: a `borrow(member)` method on the book can refuse
when the book is already out, and every loan passes through it. `Library`
is another good answer, if every loan goes through the library. `Member`
would need to ask every other member, which is a sign the rule lives
somewhere else.

</details>

## 4. A card with nothing to do

A design has a `Colour` class that knows a red, a green and a blue value,
and does nothing. Would you keep it as a class?

<details class="dl-answer"><summary>one answer</summary>

Perhaps not, today: three numbers could be a list or a dictionary. It
needs a class when it keeps a rule (each value from 0 to 255) or answers
a question (how bright is it? what is its opposite?). A design can keep
it. It just carries code that does nothing yet.

</details>

## 5. A skeleton that does not fit

This skeleton was written from cards. Run it. Which card was missing a
responsibility?

```python exec
id: a-skeleton-that-does-not-fit-1
class Route:
    def __init__(self, number, stops):
        self.number = number
        self.stops = stops


class Bus:
    def __init__(self, route):
        self.route = route
        self._passengers = 0

    def board(self):
        pass


bus = Bus(Route(46, ["Library", "Station", "Harbour"]))
print(bus.route.stops_at("Station"))
```

```inputs
Route(46, ["Library", "Station"]).stops_at("Station")
Route(46, ["Library", "Station"]).stops_at("Harbour")
```

```solution
class Route:
    def __init__(self, number, stops):
        self.number = number
        self.stops = stops

    def stops_at(self, stop):
        return stop in self.stops


class Bus:
    def __init__(self, route):
        self.route = route
        self._passengers = 0

    def board(self):
        pass


bus = Bus(Route(46, ["Library", "Station", "Harbour"]))
print(bus.route.stops_at("Station"))
---
`True`. The code asks a route "do you stop here?", and the `Route` card
did not say it could answer. That is what a skeleton is for: the mismatch
shows up as an `AttributeError` before any real code is written.
```

## 6. From earlier: two names for one list

From *A polynomial class*.

```python exec
id: from-earlier-two-names-for-one-list-1
class Route:
    def __init__(self, stops):
        self._stops = stops

    def count(self):
        return len(self._stops)

stops = ["Library", "Station"]
route = Route(stops)
stops.append("Harbour")
print(route.count())
```

```predict
type: number

What will it print?
```

<details class="dl-answer"><summary>why</summary>

`3`. `stops` and `self._stops` are two names for one list, so the caller
changed the route without touching it. `self._stops = list(stops)` would
give the route a copy of its own.

</details>

## 7. From earlier: one star for all

From *A class with many methods*.

```python exec
id: from-earlier-one-star-for-all-1
class Bus:
    fare = 2

    def __init__(self, number):
        self.number = number

bus_46 = Bus(46)
bus_10 = Bus(10)
Bus.fare = 3
bus_46.fare = 1
print(bus_10.fare, bus_46.fare)
```

```predict
What will it print?

- 3 1
  - `Bus.fare = 3` changed the class; `bus_46.fare = 1` made a new attribute on one bus.
- 1 1
  - The last change applies to every bus.
- 3 3
  - A class attribute cannot be changed through an object.
```

<details class="dl-answer"><summary>why</summary>

`3 1`. The change through the class reaches every bus that has no fare
of its own. The change through `bus_46` made an instance attribute on that
bus alone.

</details>

## 8. From earlier: a rule with a way around it

From *Encapsulation*. This `Card` refuses a fare it cannot pay. Can you
find a line, outside the class, that makes the balance negative anyway?
Is there a method call that puts money on the card, when it should only
take money off?

```python
class Card:
    def __init__(self, balance):
        self._balance = balance

    def pay(self, fare):
        if fare > self._balance:
            print("Refused: not enough on the card.")
            return
        self._balance = self._balance - fare
```

<details class="dl-answer"><summary>answer</summary>

`card._balance = -5` changes the field directly, and nothing checks it.
The method call is sneakier: `card.pay(-5)` passes the check, since −5 is
not more than the balance, and adds 5 to the card. A rule in a method
only checks the cases its writer thought of.

</details>
