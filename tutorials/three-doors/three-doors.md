---
title: "The Monty Hall problem: three doors and a simulation"
year: "2026-2027"
version: 2026.09.20.1
covers:
  why-staying-feels-fine:
    touches: [MIT-5.6]
  playing-it-ten-thousand-times:
    touches: [MIT-5.6, MIT-5.7]
  three-cases-you-can-count:
    covers: [MIT-5.7]
  a-host-who-is-not-paying-attention:
    touches: [MIT-5.7]
---

# The Monty Hall problem: three doors and a simulation

On a game show there are three doors. Behind one of them is a car.
Behind each of the other two is a goat.

You choose a door — let's say door 1 — and it stays shut for now.

The host knows what is behind every door. He opens one of the two doors
you did not choose, and he always opens one with a goat behind it. Say
he opens door 3, and there is the goat.

Then he offers you a choice. Keep door 1, or switch to door 2.

Does it matter which you do?

## Why staying feels fine

Here is the reasoning most people reach first, and it is worth setting
out properly rather than waving away.

Two doors are still shut. One of them has the car. Nothing you have been
told distinguishes them. So the chance is one in two whichever door you
end up with, and switching gains you nothing.

That argument is careful. It is also wrong, and this page is really
about finding the one step in it that fails. If you are not convinced
by the end, you are in good company — this problem caused a public
argument among people who do mathematics for a living.

Let's not settle it by arguing. Let's play the game a few thousand times
and count.

## Playing one game

First, one game, written out so we can watch it happen.

```python exec
id: playing-one-game-1
import random

doors = ["door 1", "door 2", "door 3"]

car = random.choice(doors)         # where the car actually is
first_pick = random.choice(doors)  # the door you point at

# The host opens a door that is neither your pick nor the car. When your
# pick happens to be the car, both remaining doors have goats and he can
# take either one.
choices_for_host = []
for door in doors:
    if door != first_pick and door != car:
        choices_for_host.append(door)
opened = random.choice(choices_for_host)

# One door is left once yours and the opened one are set aside. That is
# the door switching would take you to.
for door in doors:
    if door != first_pick and door != opened:
        other_door = door

print("The car is behind: ", car)
print("You picked:        ", first_pick)
print("The host opens:    ", opened)
print("Switching goes to: ", other_door)
print("Staying wins?      ", first_pick == car)
print("Switching wins?    ", other_door == car)
```

Run that a few times. Sometimes staying wins, sometimes switching does.
One game tells us nothing, which is exactly why we need a lot of them.

## Playing it ten thousand times

Let's wrap one game in a function, then play it over and over and keep
score.

```python exec
id: playing-it-ten-thousand-times-1
import random


def play_once():
    """Play one game. Returns whether staying won and whether switching won."""
    doors = ["door 1", "door 2", "door 3"]
    car = random.choice(doors)
    first_pick = random.choice(doors)

    choices_for_host = []
    for door in doors:
        if door != first_pick and door != car:
            choices_for_host.append(door)
    opened = random.choice(choices_for_host)

    for door in doors:
        if door != first_pick and door != opened:
            other_door = door

    return first_pick == car, other_door == car


num_games = 10000
staying_wins = 0
switching_wins = 0

for i in range(num_games):
    stayed_won, switched_won = play_once()
    if stayed_won:
        staying_wins = staying_wins + 1
    if switched_won:
        switching_wins = switching_wins + 1

print("Games played: ", num_games)
print("Staying won:  ", staying_wins, "->", round(staying_wins / num_games, 3))
print("Switching won:", switching_wins, "->", round(switching_wins / num_games, 3))
```

Staying wins about a third of the time. Switching wins about two thirds.
Not one in two.

Run the cell again. The two numbers move a little, and they land in the
same two places. That is worth noticing: the wobble is the randomness,
and the place they land is not random at all.

### Your turn

What happens with 100 games instead of 10,000? With 1,000,000? Try
changing `num_games` and running it again a few times at each size. How
much do the numbers wobble, and does the wobble shrink in the way you
would expect?

```python exec
id: your-turn-1
# Try a different number of games
```

## Where the two thirds comes from

The simulation says switching is better. It does not say why, and a
number you cannot explain is not much use. So look again at the line
that decides which door the host opens.

```python
choices_for_host = []
for door in doors:
    if door != first_pick and door != car:
        choices_for_host.append(door)
opened = random.choice(choices_for_host)
```

Two conditions, and the second one is the whole problem. `door != car`
means the host never opens the car. He is not guessing. He looks, and
then he opens a door he knows has a goat behind it.

That is the step the first argument misses. It treats the two remaining
doors as though nothing had happened to tell them apart. Something did
happen: the host chose, and what he was allowed to choose depended on
where the car was.

## Three cases you can count

There are only three places the car can be, and they are equally likely.
Say you picked door 1.

![The three equally likely places the car can be, given you picked door 1. If the car is behind door 1, the host may open door 2 or door 3, and switching loses. If the car is behind door 2, the host must open door 3, and switching wins. If the car is behind door 3, the host must open door 2, and switching wins. Switching wins in two of the three cases.](monty-hall-cases.svg)

Read the middle row. In two of the three cases the host has no choice at
all — one door is yours and the other hides the car, so exactly one door
is available to him. His hand is forced, and a forced move carries
information.

Now count the bottom row. Switching wins in two of the three cases. Two
out of three, which is what the simulation kept telling us.

Another way to say the same thing: switching wins exactly when your
first pick was wrong. Your first pick was a one-in-three guess, so it is
wrong two times in three. Switching turns every wrong first guess into a
win.

## A host who is not paying attention

If the host's knowledge is really what does the work, then taking it
away should destroy the effect. That is a claim we can test rather than
assert.

So here is a careless host. He opens one of the other two doors at
random, without knowing what is behind it. Sometimes he opens the car
himself and the game falls apart.

```python exec
id: a-host-who-is-not-paying-attention-1
import random


def play_with_a_careless_host():
    """One game where the host opens a door at random.

    Returns None when he opens the car, because there is no choice left
    to make and the game is spoiled.
    """
    doors = ["door 1", "door 2", "door 3"]
    car = random.choice(doors)
    first_pick = random.choice(doors)

    # The only thing he avoids is your door. He does not avoid the car,
    # because he does not know where it is.
    choices_for_host = []
    for door in doors:
        if door != first_pick:
            choices_for_host.append(door)
    opened = random.choice(choices_for_host)

    if opened == car:
        return None

    for door in doors:
        if door != first_pick and door != opened:
            other_door = door

    return first_pick == car, other_door == car


num_games = 10000
spoiled = 0
games_finished = 0
staying_wins = 0
switching_wins = 0

for i in range(num_games):
    result = play_with_a_careless_host()
    if result is None:
        spoiled = spoiled + 1
        continue
    games_finished = games_finished + 1
    stayed_won, switched_won = result
    if stayed_won:
        staying_wins = staying_wins + 1
    if switched_won:
        switching_wins = switching_wins + 1

print("Spoiled — he opened the car:", spoiled, "of", num_games)
print("Games that finished:        ", games_finished)
print("Staying won:  ", round(staying_wins / games_finished, 3))
print("Switching won:", round(switching_wins / games_finished, 3))
```

About a third of the games are spoiled. Among the ones that finish,
staying and switching each win about half the time.

So the first argument was right about one game and wrong about this one.
Against a careless host, the two remaining doors really are as good as
each other. The two thirds was never about how many doors were left
standing. It came from the host knowing, and from the fact that in two
cases out of three he had no choice.

### Your turn

Try the original game with a hundred doors instead of three. You pick
one, the host opens ninety-eight doors with goats behind them, and one
other door is left. How often does switching win now?

Before you write it, guess the answer. Then write it, and see whether
your guess was close.

Hint: the host's job is easier to write than it sounds. If your pick is
the car, the door left standing can be any other; if it is not, the door
left standing has to be the car.

```python exec
id: your-turn-2
# A hundred doors
```

## What you have now

A problem where the obvious answer is wrong, and a way of settling that
kind of question that does not depend on who argues best.

Switching wins two times in three, because it wins exactly when your
first pick was wrong, and a one-in-three guess is wrong two times in
three.

The simulation is what convinced us, and the three cases are what
explained it. Neither is worth much on its own: a number with no
argument behind it is a fact you have to take on trust, and an argument
with nothing to check it against is how the fifty-fifty answer survived
so long.

## Where to Read More

vos Savant, M. (1990). *Ask Marilyn*. Parade Magazine. The column that
set off the argument. Thousands of readers wrote in to say the answer
was wrong, including people with doctorates, which is worth remembering
the next time an answer feels obvious.

Rosenhouse, J. (2009). *The Monty Hall Problem: The Remarkable Story of
Math's Most Contentious Brain Teaser*. Oxford University Press. A whole
book on this one question, including the variations where the answer
changes — a host with a preference between the two goat doors, or one
who only offers the switch sometimes.
