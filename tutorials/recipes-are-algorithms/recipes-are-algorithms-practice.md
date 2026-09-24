---
title: "Recipes are algorithms — Practice"
practice_for: recipes-are-algorithms
year: "2026-2027"
version: 2026.09.24.1
---

# Recipes are algorithms — Practice

Each problem says what kind it is: **Predict**, **Make**, **Fix**,
**Explain** or **Another way**. For a Predict problem, write your guess
down before you run the cell. A wrong guess that you then understand
teaches more than a right one you were not sure of.

Plans and pseudocode can be right in many different ways. Where an
answer fold shows a plan, it shows one good plan, not the only one.

## Warm-up

**1. Explain.** Each of these instructions is fine for a person and
hard for a robot. Say what the robot would not know, then rewrite each
one so that it has one meaning.

- (a) Add salt to taste.
- (b) Take the medicine with food.
- (c) Turn left after a while.

<details class="dl-answer"><summary>answer</summary>

(a) "To taste" means "until it tastes right to you", and the robot has
no idea what tastes right. A rewrite: "Add a quarter of a teaspoon of
salt."

(b) Does "with food" mean before, during or after eating? A rewrite:
"Take one tablet during a meal, or up to 30 minutes after it."

(c) "A while" could be a minute or an hour, and "left" could be any of
several roads. A rewrite: "Take the second turn on the left, after
about 500 metres."

In each case the rewrite says an amount, a time or a place that the
first version left to the reader.

</details>

**2. Predict.** What will this cell show?

```python exec
id: recipes-practice-predict-1
songs = 12
minutes = songs * 4
print(minutes)
```

<details class="dl-answer"><summary>answer</summary>

`48`. The name `songs` points at 12. Then `songs * 4` is worked out, 48,
and the name `minutes` points at that. A playlist of 12 songs, each
about 4 minutes long, lasts about 48 minutes.

</details>

**3. Explain.** Which shape of step is each of these: sequence,
selection or repetition?

- (a) Do 10 press-ups.
- (b) If it is raining, take an umbrella.
- (c) Warm up, then run, then stretch.
- (d) Keep stirring the porridge until it is thick.

<details class="dl-answer"><summary>answer</summary>

(a) Repetition: one press-up, done 10 times.

(b) Selection: take the umbrella only if something is true.

(c) Sequence: three steps, one after another.

(d) Repetition, which stops when something becomes true. There is a
choice hidden inside it too: after each stir, check "is it thick yet?".
Most repeats that end with "until" have a check like this inside.

</details>

**4. Make.** A bus journey on a Leap card costs €2. Make a variable
`journeys` that holds 8, and show the cost of 8 journeys.

```python exec
id: recipes-practice-make-1
# Your code here
```

<details class="dl-answer"><summary>answer</summary>

```python
journeys = 8
print(journeys * 2)
```

It shows `16`, so 8 journeys cost €16. You could also give the fare its
own name, `fare = 2`, and write `print(journeys * fare)`. Then, if the
fare changes, there is only one line to change, and the name says
what the number is.

</details>

## Core

**5. Predict.** What will this cell show? Think about what happens when.

```python exec
id: recipes-practice-predict-2
score = 10
bonus = score * 2
score = 50
print(bonus)
```

<details class="dl-answer"><summary>answer</summary>

`20`.

`bonus` is worked out on the second line, when `score` is 10, so
`bonus` points at 20. The third line makes `score` point at 50, but
that does not go back and redo the second line. In Python, `=` is a step
done once, at one moment.

</details>

**6. Predict.** How many lines will this cell show, and what are they?

```python exec
id: recipes-practice-predict-3
def chorus():
    print("Hey, hey, hey!")

print("Verse one")
chorus()
print("Verse two")
chorus()
chorus()
```

<details class="dl-answer"><summary>answer</summary>

Five lines:

```text
Verse one
Hey, hey, hey!
Verse two
Hey, hey, hey!
Hey, hey, hey!
```

The `def` part shows nothing when it runs: it only writes the recipe
card. Each `chorus()` line calls the function, and its one step runs.
It is called three times, so the chorus appears three times.

</details>

**7. Fix.** This cell should show a short stretching routine. The first
time it runs, it stops with an error. Run it, read the last line of the
error, and fix it.

```python exec
id: recipes-practice-fix-1
stretch_routine()

def stretch_routine():
    print("Reach up high for 10 seconds.")
    print("Touch your toes for 10 seconds.")
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The error is a `NameError`: Python met a name it did not know.
2. Which line does the error point at?
3. At the moment that line runs, has the `def` happened yet?

**Think about:** which of the four questions is this about?

</details>

<details class="dl-answer"><summary>answer</summary>

```python
def stretch_routine():
    print("Reach up high for 10 seconds.")
    print("Touch your toes for 10 seconds.")

stretch_routine()
```

Python runs a cell from the top. On the first line, the function has not
been defined yet, so the name `stretch_routine` points at nothing. The
fix is to define it first, and call it after. This is a mistake about
"what happens when?".

One thing to watch for. Once your fixed cell has run, move the call
back to the top and run it again. Now it works. The function was
defined by the earlier run, and the page remembers every name that any
cell has made. So whether a cell works can depend on what ran before it,
and in what order. On a fresh page, the broken version would stop with
the same error again.

</details>

**8. Fix.** This function should show two things to pack on a rainy
day. It stops with an error. Run it, read the error, and fix it.

```python exec
id: recipes-practice-fix-2
def pack_for_rain():
print("Pack a raincoat.")
print("Pack an umbrella.")

pack_for_rain()
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The last line of the error names the problem. What does it say Python
   expected?
2. Look at `make_tea` on the tutorial page. How were its steps laid out
   under the `def` line?

**Think about:** how does Python know which lines belong to a function
and which do not?

</details>

<details class="dl-answer"><summary>answer</summary>

```python
def pack_for_rain():
    print("Pack a raincoat.")
    print("Pack an umbrella.")

pack_for_rain()
```

The error is `IndentationError: expected an indented block after
function definition on line 1`. To
*indent* a line is to push it in to the right. Python uses indenting to
know which steps belong to the function. Without it, the function has no
steps at all, and Python will not accept an empty recipe card.

The last line, `pack_for_rain()`, is not indented, because it is not
one of the function's steps. It is the line that uses the card.

</details>

**9. Make.** Write a plan in pseudocode for crossing a road at a
pedestrian crossing with lights. Use `REPEAT` or `WAIT until` at least
once, and `IF` at least once.

```python exec
id: recipes-practice-make-2
# Your plan here, one comment line at a time
```

<details class="dl-answer"><summary>answer</summary>

One plan:

```text
PRESS the button
REPEAT until the green man shows:
    WAIT one second
LOOK right, then left, then right again
IF a car is still moving towards the crossing:
    WAIT until it stops
CROSS the road
```

The repeat ends when the green man shows, so it cannot go on for ever,
as long as the lights are working. That "as long as" is an assumption
about the environment, and it is worth noticing.

</details>

**10. Explain.** A card machine in a shop lets you try your PIN three
times, and then it stops. Why is it a good idea for a repeat to have a
limit like this? Give one more example of a repeat that needs one.

<details class="dl-answer"><summary>answer</summary>

Without a limit, someone with a stolen card could try every possible PIN
until one worked. A four-digit PIN has 10,000 possibilities, and a
machine could try them all quickly. The limit makes that impossible.

A limit also guarantees that the repeat ends. An algorithm must finish,
and "repeat until the PIN is right" might never finish if the person
does not know it.

Other examples: a website that locks you out after five wrong
passwords; a phone that tries to connect to Wi-Fi a few times, then
stops and tells you; a recipe that says "stir until thick, or for at
most 10 minutes".

</details>

**11. Make.** Write a function `directions_to_college()` that shows at
least three steps for getting from a bus stop to a college door. Then
call it.

```python exec
id: recipes-practice-make-3
# Your function here
```

<details class="dl-answer"><summary>answer</summary>

One answer:

```python
def directions_to_college():
    print("Get off the bus at the stop after the bridge.")
    print("Walk up the hill for about 200 metres.")
    print("Turn right at the post office.")
    print("The college door is the red one on your left.")

directions_to_college()
```

Check three things: every step is pushed in by the same amount, the call
at the end is not pushed in, and the call has brackets.

</details>

**12. Another way.** A coach writes a warm-up on the whiteboard as 20
lines, each one saying "Do a star jump". Write the same warm-up a shorter
way, in pseudocode. Which way is better if the coach wants 50 star jumps
next week?

<details class="dl-answer"><summary>answer</summary>

```text
REPEAT 20 times:
    DO a star jump
```

The 20-line version and the 2-line version promise the same warm-up.
For 50 star jumps, the long version needs 30 more lines, and you could
lose count while writing them. The short version needs one number
changed. A repeat says "how many" in one place, where it is simple to
read and simple to change.

</details>

**13. Explain.** Think about a dishwasher. Find one example of each of
the three shapes of step in what it does: sequence, selection and
repetition.

<details class="dl-answer"><summary>answer</summary>

- **Sequence:** fill with water, heat it, spray, drain, dry. Each part
  happens after the one before.
- **Selection:** if you chose the "eco" setting, it heats the water
  less; if the door is open, it will not start.
- **Repetition:** it sprays and drains more than once, and it keeps
  heating the water until it reaches the right temperature.

Your answer may name different parts. What matters is that each one
really does fit its shape.

</details>

## Stretch

**14. Another way.** Read this cell, and predict what it shows.

```python exec
id: recipes-practice-another-1
goals = 2
goals = goals + 1
print(goals)
```

In a maths class, $g = g + 1$ has no answer: no number is equal to
itself plus one. So why does Python accept `goals = goals + 1`? In
which space does it make sense?

<details class="dl-answer"><summary>answer</summary>

It shows `3`.

In maths, `=` says that two things are equal, always. No number $g$ is
equal to $g + 1$, so the equation has no answer, and a maths teacher is
right to say so.

In Python, `=` is a step: "make this name point at this value". Python
first works out the right-hand side, `goals + 1`, using the value
`goals` has now, which is 2. That gives 3. Only then does the name
`goals` move to point at 3. It is a step in time, like a scoreboard
going from 2 to 3 when a goal is scored.

Both are right, in their own space. The maths space asks "what is
true?", and Python's space asks "what happens next?".

</details>

**15. Make.** A pancake recipe needs 50 g of flour and 80 ml of milk for
each person. Write a function `pancakes_for(people)` that shows how
much flour and how much milk to use. Call it for 2 people and for 6
people.

```python exec
id: recipes-practice-make-4
# Your function here
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Start from `make_tea_for(cups)` on the tutorial page. It has the same
   shape.
2. The first line is `def pancakes_for(people):`.
3. Each step is a `print` line, pushed in, with the amount worked out
   from `people`.
4. After the function, not pushed in, write two calls.

**Think about:** what does `people` point at during the first call, and
during the second?

**Try this next:** add a third line for eggs, at one egg for every two
people. What happens with 3 people?

</details>

<details class="dl-answer"><summary>answer</summary>

```python
def pancakes_for(people):
    print("Use", people * 50, "g of flour.")
    print("Use", people * 80, "ml of milk.")

pancakes_for(2)
pancakes_for(6)
```

This shows:

```text
Use 100 g of flour.
Use 160 ml of milk.
Use 300 g of flour.
Use 480 ml of milk.
```

For the "try this next": `people / 2` eggs for 3 people is 1.5 eggs.
Half an egg is possible, but awkward. The next page is about which
numbers a computer can hold, and what `/` gives back.

</details>

**16. Make.** Write the whole of a game of Snakes and Ladders as a plan
in pseudocode, for two players. Use `REPEAT` for the turns and `IF` for
the snakes and ladders.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Start with the pieces: where are they before the game starts?
2. One turn is: roll, move, then check the square. Write that first.
3. Put one turn inside a `REPEAT`. When does the repeating stop?
4. Where does the check for a winner go: before the move, or after it?

**Think about:** what does the plan need to say about square 100 that
the family rules from the tutorial page did not agree on?

</details>

<details class="dl-answer"><summary>answer</summary>

One plan:

```text
SET red TO 0
SET blue TO 0
SET player TO red
REPEAT until a player is on square 100:
    ROLL the die
    MOVE player forward by the number rolled
    IF player is at the bottom of a ladder:
        MOVE player to the top of the ladder
    IF player is on the head of a snake:
        MOVE player to the tail of the snake
    IF player is on square 100:
        SAY player wins
    OTHERWISE:
        SET player TO the other player
```

This plan still leaves one thing out: what happens if a roll would take
a piece past 100? A robot would need to be told. Adding one more `IF`
for it, in your family's version of the rule, finishes the plan.

</details>
