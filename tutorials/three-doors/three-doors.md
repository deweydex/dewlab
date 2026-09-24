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

You choose a door. Say you choose door 1. It stays shut for now.

The host knows what is behind every door. He opens one of the two doors
you did not choose, and he always opens one with a goat behind it. Say
he opens door 3, and there is the goat.

Then he offers you a choice. You can keep door 1, or you can switch to
door 2.

Does it matter which you do? Before you read on, make your own guess.

This puzzle is called the Monty Hall problem, after the host of an old
American game show. On this page we:

- look at the answer most people give first
- play the game thousands of times in Python, and count the wins
- count the three possible cases by hand, to see why the result is true
- change the host, and see what happens to the answer

We use the probability and simulation from
[Probability: simple, compound and conditional](tutorial:what-are-the-chances).

## Why staying feels fine

Here is the reasoning most people reach first. It deserves to be set
out properly, step by step.

Two doors are still shut. One of them has the car. Nothing you have been
told makes one door different from the other. So the chance is one in
two for either door, and switching gains you nothing.

That argument is careful. It is also wrong. This page is about finding
the one step in it that fails.

If you are still not convinced at the end, many clever people agree with
you. This problem caused a public argument among people who do
mathematics for a living.

So we will not settle it by arguing. Instead, we will play the game a few
thousand times and count.

## Playing one game

First, here is one game, written out step by step so we can watch it
happen. What do you think each line of output will show?

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

Run that cell a few times. Sometimes staying wins, and sometimes
switching wins. One game tells us nothing about which is better. That is
why we need a lot of games.

## Playing it ten thousand times

Next, we put one game inside a function, `play_once()`. Then we play it
10,000 times and count how often each choice wins.

Before you run the cell, what do you expect? If staying and switching
are equally good, each should win about half the time. Run it to check.

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

Were you surprised? Staying wins about a third of the time. Switching
wins about two thirds of the time. Neither is one in two.

Run the cell again. The two numbers change a little, but they stay close
to the same two values. That is worth noticing. The small changes come
from the randomness. The values they stay close to are not random at all.

### Your turn

1. Copy the lines from `num_games = 10000` to the end of the cell above
   into the cell below. You have already run the cell above, so
   `play_once()` is defined, and you do not need to copy it.
2. Change `num_games` to 100, and run the cell a few times.
3. Then try 1,000,000, and run it a few times again.

How much do the numbers change from run to run at each size? Does the
change get smaller as the number of games grows, as the law of large
numbers says it should?

```python exec
id: your-turn-1
# Try a different number of games
```

## Where the two thirds comes from

The simulation says switching is better. It does not say why, and a
number we cannot explain is not much use. So let's look again at the
lines that decide which door the host opens.

```python
choices_for_host = []
for door in doors:
    if door != first_pick and door != car:
        choices_for_host.append(door)
opened = random.choice(choices_for_host)
```

The `if` line has two conditions. The second one, `door != car`, is
the key to the whole problem. It means the host never opens the door
with the car. He is not guessing. He knows where the car is, and he
opens a door he knows has a goat behind it.

That is the step the first argument misses. It treats the two shut doors
as if nothing had happened to make them different. But something did
happen. The host chose a door, and the doors he was allowed to choose
depended on where the car was.

## Three cases you can count

There are only three places the car can be, and they are equally
likely. Say you picked door 1. The picture shows what happens in each
case.

![The three equally likely places the car can be, given you picked door 1. If the car is behind door 1, the host may open door 2 or door 3, and switching loses. If the car is behind door 2, the host must open door 3, and switching wins. If the car is behind door 3, the host must open door 2, and switching wins. Switching wins in two of the three cases.](monty-hall-cases.svg)

Look at the middle row. In two of the three cases, the host has no
choice at all. One door is yours, and another hides the car, so only one
door is left for him to open. When the host has only one door he can
open, the door he opens tells us where the car is.

Now count the bottom row. Switching wins in two of the three cases. That
is two out of three, the same as the simulation kept telling us.

Here is another way to say it. Switching wins exactly when your first
pick was wrong. Your first pick was a one-in-three guess, so it is wrong
two times in three. Switching turns every wrong first guess into a win.

## A host who is not paying attention

Is the host's knowledge really what makes switching better? If it is,
then a host who knows nothing should make the advantage disappear. We
can test that with a simulation.

So here is a careless host. He opens one of the other two doors at
random, without knowing what is behind it. Sometimes he opens the door
with the car himself, and the game is spoiled: there is nothing left to
decide.

Before you run the cell, what do you think will happen to the two
thirds?

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

About a third of the games are spoiled. In the games that finish,
staying and switching each win about half the time.

So the first argument, "one in two", is right about this game with a
careless host. It is wrong about the original game. Against a careless
host, the two shut doors are equally good. The two thirds never came
from the number of doors that were still shut. It came from the host
knowing where the car was, and from the fact that in two cases out of
three he had no choice.

### Your turn

What happens to the original game with a hundred doors instead of
three? You pick one door. The host, who knows where the car is, opens
ninety-eight doors with goats behind them. One other door is still shut.
How often does switching win now?

1. Before you write any code, guess the answer.
2. Write a simulation of the hundred-door game.
3. Run it, and see whether your guess was close.

**Hint:** the host's job is easier to write than it sounds. If your pick
is the car, the other shut door can be any of the other doors. If your
pick is not the car, the other shut door has to be the car.

```python exec
id: your-turn-2
# A hundred doors
```

## What you have now

You now know a problem where the answer that looks right is wrong. You
also have a way to settle that kind of question, and it does not depend
on who argues best.

Switching wins two times in three. It wins exactly when your first pick
was wrong, and a one-in-three guess is wrong two times in three.

The simulation convinced us, and the three cases explained why. Each one
needs the other. A number with no argument behind it is a fact you have
to trust without knowing why. An argument with nothing to check it
against is how the fifty-fifty answer lasted so long.

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
