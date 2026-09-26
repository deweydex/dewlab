---
title: "The Monty Hall problem: three doors and a simulation — Practice"
practice_for: three-doors
year: "2026-2027"
version: 2026.09.26.1
---

# The Monty Hall problem: three doors and a simulation — Practice

The tutorial changed the host once, and the answer moved from two thirds
to a half. These problems change him three more ways, and add a door.
For each one, guess first, then play it thousands of times, then count
the cases. The simulation says what happens; the count says why.

## A host with a favourite door

**1.** You always pick door 1. When the host has a choice between door 2
and door 3, which happens when the car is behind door 1, he always opens
door 3. He still never opens the car. Suppose he opens door 3: should
you switch? And if he opens door 2?

Can you finish the game in this cell, and count separately how often
switching wins after each door he opens?

```python exec
id: doors-favourite-door
import random

opened_3 = 0
switching_won_3 = 0
opened_2 = 0
switching_won_2 = 0

for game in range(30000):
    car = random.choice([1, 2, 3])
    first_pick = 1
    # Which door does this host open? Which door would switching take you to?

print("He opened door 3:", opened_3, "times")
print("He opened door 2:", opened_2, "times")
```

```hint
When the car is behind door 1, he opens door 3, his favourite. When it
is behind door 2 or door 3, he has only one door he can open. The doors
are numbered 1, 2 and 3, which add up to 6, so the door switching takes
you to is `6 - first_pick - opened`.
```

```solution
import random

opened_3 = 0
switching_won_3 = 0
opened_2 = 0
switching_won_2 = 0

for game in range(30000):
    car = random.choice([1, 2, 3])
    first_pick = 1
    if car == 1:
        opened = 3
    elif car == 2:
        opened = 3
    else:
        opened = 2
    other_door = 6 - first_pick - opened
    if opened == 3:
        opened_3 = opened_3 + 1
        if other_door == car:
            switching_won_3 = switching_won_3 + 1
    else:
        opened_2 = opened_2 + 1
        if other_door == car:
            switching_won_2 = switching_won_2 + 1

print("He opened door 3:", opened_3, "times")
print("He opened door 2:", opened_2, "times")
print("Switching won after door 3:", round(switching_won_3 / opened_3, 3))
print("Switching won after door 2:", round(switching_won_2 / opened_2, 3))
---
After door 3, switching wins about half the time; after door 2, every
time. He opens door 3 when the car is behind door 1 and when it is behind
door 2: two equally likely cases, one each way. He opens door 2 only
when he has to, when the car is behind door 3. Over all the games,
switching still wins two thirds of the time: the host's habit changes
what each door tells you, not how often switching wins.
```

**2.** Can you get the answer "a half, after door 3" from the formula for
a conditional probability, $P(B \mid A) = \frac{P(A \text{ and } B)}{P(A)}$?

<details class="dl-answer"><summary>answer</summary>

Let A be "he opens door 3" and B be "switching wins", which here means
the car is behind door 2. He opens door 3 when the car is behind door 1
or door 2, so $P(A) = \frac{1}{3} + \frac{1}{3} = \frac{2}{3}$. Both
happen only when the car is behind door 2: $P(A \text{ and } B) =
\frac{1}{3}$. So $P(B \mid A) = \frac{1/3}{2/3} = \frac{1}{2}$.

</details>

## A host who does not always offer

**3.** A different host. If your first pick is the car, he always opens
a goat door and offers you the switch. If your first pick is a goat, he
offers the switch only half the time; the other half, he opens your door
and the game ends. He has offered you the switch. Should you take it?

```python exec
id: doors-sometimes-offers
import random

offered = 0
switching_won = 0

for game in range(30000):
    car = random.choice([1, 2, 3])
    first_pick = random.choice([1, 2, 3])
    if first_pick == car:
        offers = True
    else:
        offers = random.random() < 0.5
    # When he offers, does switching win?

print("He offered the switch in", offered, "games")
```

```hint
When he offers and your first pick was not the car, the other shut door
has to be the car, since he opens a goat. So switching wins exactly when
`first_pick != car`, as in the original game.
```

```solution
import random

offered = 0
switching_won = 0

for game in range(30000):
    car = random.choice([1, 2, 3])
    first_pick = random.choice([1, 2, 3])
    if first_pick == car:
        offers = True
    else:
        offers = random.random() < 0.5
    if offers:
        offered = offered + 1
        if first_pick != car:
            switching_won = switching_won + 1

print("He offered the switch in", offered, "games")
print("Switching won:", round(switching_won / offered, 3))
---
About a half. Count a hundred games of each kind of first pick, as the
medical test counted a million people: of 300 games, 100 start with the
car, and he offers in all 100; 200 start with a goat, and he offers in
100. So he offers in 200 games, and switching wins in the 100 of them
that started with a goat. The offer itself is information. A host who
offered *only* when you had picked the car would make switching lose
every time.
```

## Four doors

**4.** Four doors, one car. You pick a door. The host, who knows where
the car is, opens one of the other doors with a goat behind it. Two
doors besides yours are still shut. If you switch, you choose one of the
two at random. How often does switching win? How often does staying?

```python exec
id: doors-four-doors
import random

games = 30000
switching_won = 0
staying_won = 0

for game in range(games):
    car = random.randrange(4)
    first_pick = random.randrange(4)
    goats_he_can_open = [door for door in range(4) if door != first_pick and door != car]
    opened = random.choice(goats_he_can_open)
    # Which doors are still shut, besides yours? Switch to one of them at random.

print("Switching won:", round(switching_won / games, 3))
print("Staying won:  ", round(staying_won / games, 3))
```

```predict
type: number
tolerance: 0.03

What share of the games will switching win, once the cell is finished?
```

```hint
The doors still shut, besides yours, are the ones that are neither
`first_pick` nor `opened`. `random.choice` picks one of them.
```

```solution
import random

games = 30000
switching_won = 0
staying_won = 0

for game in range(games):
    car = random.randrange(4)
    first_pick = random.randrange(4)
    goats_he_can_open = [door for door in range(4) if door != first_pick and door != car]
    opened = random.choice(goats_he_can_open)
    still_shut = [door for door in range(4) if door != first_pick and door != opened]
    new_pick = random.choice(still_shut)
    if new_pick == car:
        switching_won = switching_won + 1
    if first_pick == car:
        staying_won = staying_won + 1

print("Switching won:", round(switching_won / games, 3))
print("Staying won:  ", round(staying_won / games, 3))
---
Switching wins about 0.375 and staying 0.25. Staying wins when your
first pick was right, 1 time in 4. Your first pick is wrong 3 times in
4, and then the car is behind one of the two doors you can switch to,
so a random switch finds it half the time: $\frac{3}{4} \times
\frac{1}{2} = \frac{3}{8}$. Switching is still better, though it wins
less than half the time.
```

**5.** Same four doors, but now the host opens *two* goat doors. How
often does switching win?

<details class="dl-answer"><summary>answer</summary>

$\frac{3}{4}$. Only one door besides yours is left shut, so switching
wins whenever your first pick was wrong. With $n$ doors and a host who
opens every goat door but one, switching wins $\frac{n-1}{n}$ of the
time: the hundred-door game from the tutorial is $\frac{99}{100}$.

</details>

## From earlier

**6.** From *Logic and truth*. In the original game, exactly one of
`stayed_won` and `switched_won` is `True`, every game. Which operator
from that page is `True` when exactly one of two things is?

<details class="dl-answer"><summary>answer</summary>

Exclusive or, XOR: `stayed_won ^ switched_won` is `True` in every game.
It fails for the careless host, whose spoiled games have neither winning,
and for four doors, where staying and switching can both lose.

</details>

**7.** From *Counting*. With $n$ doors, how many pairs of (where the car
is, which door you pick) are there, and in how many is your pick wrong?

<details class="dl-answer"><summary>answer</summary>

$n^2$ pairs, by the multiplication principle, and $n^2 - n = n(n-1)$
with the pick wrong, since exactly $n$ pairs have the pick right. So a
wrong first pick has probability $\frac{n(n-1)}{n^2} = \frac{n-1}{n}$:
$\frac{6}{9}$ for three doors, the tutorial's count.

</details>

**8.** From *Probability*. In the original game, is "your first pick is
the car" independent of "the host opens door 3"? Take your pick as door
1, and a host who chooses at random when he has a choice.

<details class="dl-answer"><summary>answer</summary>

Yes. He opens door 3 half the time: when the car is behind door 2
($\frac{1}{3}$), and half of the time it is behind door 1
($\frac{1}{6}$). Both happen $\frac{1}{6}$ of the time, and
$\frac{1}{3} \times \frac{1}{2} = \frac{1}{6}$. The door he opens tells
you nothing about your own door. It tells you a great deal about the
*other* one, which is where the two thirds lives. With the favourite-door
host of problem 1, they are no longer independent.

</details>
