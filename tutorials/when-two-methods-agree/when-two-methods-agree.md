---
title: "Checking: a closer look at two methods that agree"
year: "2026-2027"
version: 2026.09.26.1
---

# Checking: a closer look at two methods that agree

In [The Monty Hall problem](tutorial:three-doors#three-cases-you-can-count),
a simulation said two thirds, and counting the cases said two thirds. When
two different methods give the same answer, it feels like proof. Here are
two ideas about what that agreement shows. Both are reasonable, and they
cannot both be true.

**Idea A.** Two methods that agree are both right. If one had a mistake,
they would disagree.

**Idea B.** Two methods can agree because they share the same mistake.
Agreement shows that they calculate the same thing. It does not show that
the thing is what we wanted.

## An experiment

Somebody wants the average score of one roll of a die. They find it two
ways. First they count: add up the faces and divide by how many there are.
Then they check with a simulation of 10,000 rolls. Both methods use the
same description of a die.

```python exec
id: an-experiment-1
import random

faces = [0, 1, 2, 3, 4, 5]
counted = sum(faces) / len(faces)

rolls = [random.randint(0, 5) for roll in range(10000)]
simulated = sum(rolls) / len(rolls)

print("counted:  ", counted)
print("simulated:", round(simulated, 2))
```

The two methods agree: 2.5, and about 2.5. Idea A says the average roll of
a die is 2.5. Idea B says the agreement cannot tell us that. Both methods
could share a mistake.

The next cell finds the average of the faces of a real die, 1 to 6.

```python exec
id: an-experiment-2
real_faces = [1, 2, 3, 4, 5, 6]
print(sum(real_faces) / len(real_faces))
```

```predict
type: choice

Before you run it: will a real die also average 2.5?

- Yes
  - This is what idea A predicts: two methods agree, so 2.5 is right.
- No
  - This is what idea B allows: both methods could share a mistake.
```

It prints 3.5. A real die has faces 1 to 6, not 0 to 5. Both methods were
built from the same wrong picture of a die, so both gave the same wrong
answer. Idea B matches what happened.

Can you fix both methods, and check that they now agree on 3.5?

<details class="dl-answer"><summary>the two changes</summary>

`faces = [1, 2, 3, 4, 5, 6]`, and `random.randint(1, 6)`. The counted
average is 3.5, and the simulated one is about 3.5. They agree again, and
this time the picture of the die matches a real one.

</details>

## Why idea A feels right

Checking a calculation with a second method is a good habit. It catches
many mistakes: a mistake in the arithmetic, a loop that stops one step early,
a wrong sign. Those mistakes belong to one method, so the other method
does not make them, and the answers disagree.

But some mistakes come before either method starts. They are in how we
describe the problem: the faces of the die, the rules of the game, the
question we ask. Every method we build on that description has the same
mistake. Two methods that agree have checked each other's working. Nothing
has checked the description.

So a second method helps most when it starts from somewhere different. For
a die, that might be a real die, rolled by hand 60 times.

## Where else it happens

On the Monty Hall page, the careless host made "one in two" true. Here is
a count of the careless host's game, the way the page counted the three
cases.

```python exec
id: where-else-it-happens-1
import itertools

doors = ["door 1", "door 2", "door 3"]
finished = 0
switching_wins = 0
for car, first_pick, opened in itertools.product(doors, repeat=3):
    # The host cannot open your door, and opening the car spoils the game.
    if opened != first_pick and opened != car:
        finished = finished + 1
        if first_pick != car:
            switching_wins = switching_wins + 1
print(switching_wins, "of", finished)
```

It prints `6 of 12`, one in two, and the careless-host simulation on that
page also gave about one in two. The two methods agree. What would you
need to check, to know whether one in two is the answer for the TV show?

## Where to read more

Richard Feynman's lecture *Cargo Cult Science* (Caltech, 1974) is about
fooling yourself, and about the checks that stop it. The text is widely
reprinted, including in *Surely You're Joking, Mr. Feynman!*
