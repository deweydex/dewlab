---
title: "Recipes are algorithms — Practice"
practice_for: recipes-are-algorithms
year: "2026-2027"
version: 2026.09.25.1
---

# Recipes are algorithms — Practice

Each problem says what kind it is: **Predict**, **Make**, **Fix**,
**Explain** or **Another way**. For a Predict problem, write your guess
down before you run the cell. A guess that missed, once you see why,
teaches more than a lucky match you were not sure of.

A plan or pseudocode can be written in many different ways. Where an
answer fold shows a plan, it shows one answer, not the only one.
Yours may be clearer. Here is one test for any plan. Would a robot
that knows nothing follow it and finish the task?

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

`48`. The name `songs` points at 12. Then Python calculates `songs * 4`,
which is 48, and the name `minutes` points at that. A playlist of 12 songs, each
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

**4. Make.** A phone backs up your photos each night, and each photo
takes about 3 MB (megabytes) of space. Make a variable `photos` that holds 8, and show the
space that 8 photos take.

```python exec
id: recipes-practice-make-1
# Your code here
```

<details class="dl-answer"><summary>answer</summary>

```python
photos = 8
print(photos * 3)
```

It shows `24`, so 8 photos take about 24 MB. You could also give the
size its own name, `photo_mb = 3`, and write `print(photos * photo_mb)`.
Then, if the phone's camera changes, there is only one line to change,
and the name says what the number is.

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

Python calculates `bonus` on the second line, when `score` is 10, so
`bonus` points at 20. The third line makes `score` point at 50, but
the second line does not run again. In Python, `=` is a step
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

The `def` part shows nothing when it runs. It only writes the recipe
card. Each `chorus()` line calls the function, and its one step runs.
It is called three times, so the chorus appears three times.

</details>

**7. Fix.** Schlomo, who is learning Python too, wrote the steps a
phone follows when it starts. The first time his cell runs, it stops
with an error. Run it, read the last line of the error, and fix it.

```python exec
id: recipes-practice-fix-1
start_up()

def start_up():
    print("Check the battery.")
    print("Show the lock screen.")
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The error is a `NameError`: Python met a name it did not know.
2. Which line does the error point at?
3. At the moment that line runs, has the `def` happened yet?

**Think about:** which of the four questions is this about?

</details>

<details class="dl-answer"><summary>answer</summary>

```python
def start_up():
    print("Check the battery.")
    print("Show the lock screen.")

start_up()
```

Python runs a cell from the top. On the first line, the function has not
been defined yet, so the name `start_up` points at nothing. The fix is
to define it first, and call it after. Schlomo's order makes sense on
paper, where the most important line often comes first. In Python, the
order is about "what happens when?".

Watch for one thing. Once your fixed cell has run, move the call
back to the top and run it again. Now it works. The function was
defined by the earlier run, and the page remembers every name that any
cell has made. So whether a cell works can depend on what ran before it,
and in what order. On a fresh page, the broken version would stop with
the same error again.

</details>

**8. Fix.** This function should show the two steps of a backup. It
stops with an error. Run it, read the error, and fix it.

```python exec
id: recipes-practice-fix-2
def save_backup():
print("Copy every new photo.")
print("Check that the copies open.")

save_backup()
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
def save_backup():
    print("Copy every new photo.")
    print("Check that the copies open.")

save_backup()
```

The error is `IndentationError: expected an indented block after
function definition on line 1`. To
*indent* a line is to push it in to the right. Python uses indenting to
know which steps belong to the function. Without it, the function has no
steps at all, and Python will not accept an empty recipe card.

The last line, `save_backup()`, is not indented, because it is not
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

Other examples: a website that locks your account after five wrong
passwords; a phone that tries to connect to Wi-Fi a few times, then
stops and tells you; a recipe that says "stir until thick, or for at
most 10 minutes".

</details>

<aside class="dl-note" id="recipes-practice-note-pin">

**Why a PIN has four digits.** John Shepherd-Barron led the team that
built one of the first cash machines. It opened at a Barclays bank in
Enfield, in London, in 1967. He planned a code of six digits. His wife,
Caroline, told him she could remember only four, and four digits became
the usual length around the world.

</aside>

**11. Make.** A robot pen draws on paper. Write a function
`draw_letter_l()` that shows at least three steps for drawing a capital
L. Then call it.

```python exec
id: recipes-practice-make-3
# Your function here
```

<details class="dl-answer"><summary>answer</summary>

One answer:

```python
def draw_letter_l():
    print("Put the pen down at the top.")
    print("Draw a line 4 cm down.")
    print("Turn left.")
    print("Draw a line 2 cm long.")
    print("Lift the pen.")

draw_letter_l()
```

Check three things: every step is pushed in by the same amount, the call
at the end is not pushed in, and the call has brackets.

</details>

**12. Another way.** Schlomi, who is also learning Python, wants the
robot pen to draw a dashed line. Her plan has 20 lines, each one saying
"Draw 1 cm, then lift the pen and move 1 cm". It works. Write the same
plan a shorter way, in pseudocode. Which way is better if she wants 50
dashes next week?

<details class="dl-answer"><summary>answer</summary>

```text
REPEAT 20 times:
    DRAW 1 cm
    LIFT the pen and MOVE 1 cm
    PUT the pen down
```

Schlomi's 20-line plan and the short plan promise the same line, so
hers works. But for 50 dashes, the long version needs 30 more lines,
and she could lose count while writing them. The short version needs
one number changed. A repeat says "how many" in one place, where it is simple to
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

Your answer may name different parts. Check that each one really fits
its shape.

</details>

## Stretch

**14. Another way.** Read this cell, and predict what it shows.

```python exec
id: recipes-practice-another-1
goals = 2
goals = goals + 1
print(goals)
```

In a maths class, $g = g + 1$ has no answer. No number is equal to
itself plus one. So why does Python accept `goals = goals + 1`? In
which space does it make sense?

<details class="dl-answer"><summary>answer</summary>

It shows `3`.

In maths, `=` says that two things are equal, always. No number $g$ is
equal to $g + 1$, so the equation has no answer, and a maths teacher is
right to say so.

In Python, `=` is a step: "make this name point at this value". Python
first calculates the right-hand side, `goals + 1`, using the value
`goals` has now, which is 2. That gives 3. Only then does the name
`goals` move to point at 3. It is a step in time, like a scoreboard
going from 2 to 3 when a goal is scored.

Both make sense, each in its own space. The maths space asks "what is
true?", and Python's space asks "what happens next?".

</details>

**15. Make.** An image is stored with 3 bytes for each pixel, one each
for red, green and blue. Write a function `memory_for(width, height)`
that shows how many pixels an image has, and how many bytes it needs.
Call it for an image 4 pixels by 3, and for one 1920 by 1080.

```python exec
id: recipes-practice-make-4
# Your function here
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Start from `make_tea_for(cups)` on the tutorial page. It has the
   same shape, with two parameters instead of one.
2. The first line is `def memory_for(width, height):`.
3. Each step is a `print` line, pushed in, with the amount calculated
   from `width` and `height`.
4. After the function, not pushed in, write two calls.

**Think about:** what do `width` and `height` point at during the first
call, and during the second?

**Try this next:** some small screens use half a byte for each pixel.
Add a third line for that. What happens with an image 3 pixels by 3?

</details>

<details class="dl-answer"><summary>answer</summary>

```python
def memory_for(width, height):
    print("Pixels:", width * height)
    print("Bytes:", width * height * 3)

memory_for(4, 3)
memory_for(1920, 1080)
```

This shows:

```text
Pixels: 12
Bytes: 36
Pixels: 2073600
Bytes: 6220800
```

A full screen of pixels takes over 6 million bytes. For the "try this
next": `width * height / 2` for a 3 by 3 image is 4.5 bytes. Half a
byte cannot be stored on its own. The next page is about which numbers
a computer can hold, and what `/` returns.

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

This plan still misses one thing. What happens if a roll would take
a piece past 100? A robot would need to be told. Adding one more `IF`
for it, in your family's version of the rule, finishes the plan.

</details>
