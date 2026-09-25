---
title: "Four questions for any puzzle — Practice"
practice_for: four-questions
year: "2026-2027"
version: 2026.09.25.1
---

# Four questions for any puzzle — Practice

Each problem says what kind it is. **Predict** asks you to guess what a
cell will show, then run it. **Make** asks you to write something small.
**Fix** gives you a cell with one mistake in it. **Explain** asks for an
answer in words. **Another way** asks you to reach an answer by a second
route, or to find the space where a "wrong" answer is right.

Many of these have more than one good answer. The answer folds show one
of them, with the thinking behind it. If yours is different, it may be
right too, and it may be more interesting: check it against the four
questions. Try each one before you open its fold. A guess that turns
out wrong is not wasted; it shows you exactly where to look.

## Warm-up

**1. Predict.** What will each line of this cell show? Write down your
three guesses, then run it.

```python exec
id: four-q-practice-predict-1
print(12 * 3)
print(2 * "la ")
print(3 * "2")
```

<details class="dl-answer"><summary>answer</summary>

```text
36
la la
222
```

The first line multiplies two numbers. The second repeats the string
`"la "` twice.

The third line is the surprise. `"2"` is in quote marks, so it is a
string, not a number. Python repeats the text "2" three times and gets
`222`. The same `*`, a different space: with a number it multiplies, and
with a string it repeats.

</details>

**2. Explain.** In a game of football, what is named? Give at least three
names, and say what each one points at.

<details class="dl-answer"><summary>answer</summary>

There are many. Here are some:

- "the ball" points at one ball;
- each team has a name, and each player has a name and a number on their
  shirt;
- "the penalty area" names one part of the pitch;
- "the score" names two numbers, one for each team, that change during
  the game.

Notice that a player's number does the same job as a square's number in
Snakes and Ladders. It points at one player, so the referee can say "number
7" and everyone knows who is meant.

</details>

**3. Explain.** Ask the four questions of noughts and crosses (some people
call it tic-tac-toe). Give one short answer to each.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Picture the game: a grid of three by three squares, two players, one
   uses X and one uses O.
2. **Named:** what do the players call each other, and how could you
   point at one square?
3. **Promised:** what does one move do to the grid?
4. **When:** who goes, and what is checked after each move?
5. **Space:** how many squares are there, and what can you not do?

**Think about:** which of these answers are written in the rules, and
which does everyone assume without saying?

</details>

<details class="dl-answer"><summary>answer</summary>

- **What is named here?** The two players are "X" and "O". Squares can
  be named too, for example "top left" or "the middle".
- **What is promised?** A move takes an empty square and puts your mark
  in it. The grid after your move has one more mark than before.
- **What happens when?** X usually goes first, then the players take
  turns. After every move, someone checks for three in a row.
- **What does this space let us do?** There are nine squares. You may
  only mark an empty one, and you may not rub a mark out. The game ends
  after at most nine moves.

</details>

**4. Make.** A photo on a phone takes up about 3 MB (megabytes) of
space. Write one line of Python that shows the space taken by 4 photos.

```python exec
id: four-q-practice-make-1
# Your line here
```

<details class="dl-answer"><summary>answer</summary>

```python
print(4 * 3)
```

It shows `12`, so four photos take about 12 MB. `print(3 * 4)` works
too: multiplying in either order gives the same answer.

</details>

## Core

**5. Fix.** Schlomo, who is learning Python too, wants the space taken
by 3 videos of 250 MB each. He writes this cell, and it stops with an
error. Run it, then find and fix his mistake.

```python exec
id: four-q-practice-fix-1
print(3 x 250)
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Run the cell and look at the last line of the message. It says
   `SyntaxError`, which is Python's way of saying "I cannot read this
   line". It may also ask "Perhaps you forgot a comma?". That is Python
   guessing, and here the guess is wrong.
2. Look at the symbol between `3` and `250`. Is that the symbol Python
   uses for multiply?
3. What did the first cell on the tutorial page use?

**Think about:** on paper, you write × or sometimes x. What does Python
use, and why might that be?

</details>

<details class="dl-answer"><summary>answer</summary>

```python
print(3 * 250)
```

It shows `750`: 750 MB. In Python, multiply is `*`, not `x`. To Python,
`x` is a letter, and `3 x 250` is a number, a letter and a number side
by side, with nothing to say what to do with them. So Python cannot
read the line.

Schlomo's mistake is a very common one, and a sensible one: on paper,
`x` is how most of us write multiply. It is a move from a different
space.

</details>

**6. Fix.** A digital alarm clock should show the word `beep` three
times. The cell stops with an error. Run it, read the last line of the
message, and fix it.

```python exec
id: four-q-practice-fix-2
print(3 * beep)
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The last line of the error says `NameError`. That means Python met a
   name it does not know.
2. Which word in the line is Python treating as a name?
3. How did the tutorial page tell Python that `"ha "` was text, and not
   a name?

**Think about:** which of the four questions is this error about?

</details>

<details class="dl-answer"><summary>answer</summary>

```python
print(3 * "beep ")
```

Without quote marks, Python reads `beep` as a name, and goes looking
for what that name points at. Nothing has that name yet, so Python says
`NameError: name 'beep' is not defined`.

With quote marks, `"beep "` is a string: the text itself, not a name
for something else. This error is about the first question, *what is
named here?* Python was asked to follow a name that pointed at nothing.

</details>

**7. Explain.** Here are the steps for sending a photo from a phone, out
of order. Put them in an order that works, and say which two steps
could swap without causing a problem.

- A. Tap Send.
- B. Open the messages app.
- C. Choose the photo.
- D. Choose who gets it.
- E. Unlock the phone.
- F. Wait for the tick that says it was sent.

<details class="dl-answer"><summary>answer</summary>

One order that works is E, B, D, C, A, F: unlock the phone, open the
app, choose the person, choose the photo, tap Send, and wait for the
tick.

C and D could swap. Some apps ask for the person first, and some for
the photo first, and either way the photo arrives.

A and F cannot swap. The tick only comes after something has been sent.
And E must come first, because a locked phone does nothing else.

</details>

**8. Another way.** Two videos last 45 minutes and 30 minutes. Schlomi,
who is also learning Python, says together they make `1:15`. Schlomo
says they make `75`. Who is right?

<details class="dl-answer"><summary>answer</summary>

Both of them. They are answering in two different spaces.

In ordinary numbers, 45 + 30 = 75, so there are 75 minutes. In hours and
minutes, every 60 minutes becomes one hour, so 75 minutes is 1 hour and
15 minutes, written `1:15`. These are two ways of writing the same
amount of time.

The question to ask was *what space are we in?* Once we know the space,
we can check each answer.

</details>

**9. Explain.** A help page says "Restart your phone if it is slow."
What does this step assume that it does not say? Give two things.

<details class="dl-answer"><summary>answer</summary>

There are many. Some of them:

- It assumes you know how to restart this phone: which button, held for
  how long.
- It assumes you know what "slow" means: slower than yesterday, or
  slower than a friend's phone?
- It assumes you have saved anything you were working on, since a
  restart closes every app.

A person who has used phones for years fills these gaps without
noticing. A machine, or someone who has never used one, cannot. Filling
those gaps is what the next page is about.

</details>

**10. Predict.** What will this cell show? Think about what happens
first.

```python exec
id: four-q-practice-predict-2
print(2 * "Olé! " + "Olé! Olé!")
print(10 * 10 * 10)
```

<details class="dl-answer"><summary>answer</summary>

```text
Olé! Olé! Olé! Olé!
1000
```

In the first line, `2 * "Olé! "` happens first, and gives
`Olé! Olé! `. Then `+` joins the string `"Olé! Olé!"` on the end. With
strings, `+` does not add: it joins one piece of text to another. That
is one more move that means something different in a different space.

The second line multiplies 10 by 10, and then that answer by 10 again.

</details>

**11. Explain.** A vending machine makes a promise. What goes in, and
what comes out? What must be true before it keeps its promise?

<details class="dl-answer"><summary>answer</summary>

You put in the number of your choice and enough money, or a card
payment. Out come a snack or a drink, and maybe some change.

Before it keeps the promise, some things must be true. You must pay at
least the price. The machine must be switched on, and the thing you
chose must be in stock. The number you typed must be one the machine
knows.

This is a function in the sense of this course: something in, something
out, and a promise about how the two are connected.

</details>

**12. Make.** Write one line that draws a line of 30 stars, `*`, across
the screen.

```python exec
id: four-q-practice-make-2
# Your line here
```

<details class="dl-answer"><summary>answer</summary>

```python
print(30 * "*")
```

The star is inside quote marks, so it is a string and `30 *` repeats it.
The `*` outside the quote marks is the multiply sign doing its string
job. The same symbol is doing two different things in one line, and
Python can tell which is which from the quote marks.

</details>

## Stretch

**13. Another way.** The tutorial worked out `print(4 * 7)`. Show the
same 28 in Python in a different way, without using `*`.

```python exec
id: four-q-practice-another-1
# Another way to get 28
```

<details class="dl-answer"><summary>answer</summary>

```python
print(7 + 7 + 7 + 7)
```

Multiplying by 4 is adding four times. Both lines keep the same
promise. The first is shorter, and it stays short for `1920 * 1080`,
when the second would need 1080 copies of 1920.

</details>

**14. Explain.** The weather forecast says it will be 30 degrees
tomorrow. Is that a hot day? What question do you need to ask first?

<details class="dl-answer"><summary>answer</summary>

It depends on the scale. The question is *what space are we in?*

In Celsius, the scale used in Ireland, 30 degrees is a very hot day. In
Fahrenheit, the scale used in the United States, 30 degrees is below
freezing, because water freezes at 32 degrees Fahrenheit.

The number 30 is the same in both. What it means depends on the space.

</details>

**15. Another way.** Your friend is sure this is a mistake:

$$11 + 3 = 2$$

Find a space where it is right. Then find a second, different space
where $5 + 3 = 1$ is right.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Think of the clock from the tutorial page. What time is it 3 hours
   after 11 o'clock?
2. For the second one, think of something else that goes round and round
   and starts again. How many of them are there?
3. Days of the week are one example. Number them, starting with Monday
   as day 1.

**Think about:** what do all these spaces have in common?

**Try this next:** in which space is $10 + 5 = 3$ right?

</details>

<details class="dl-answer"><summary>answer</summary>

On a 12-hour clock, 3 hours after 11 o'clock is 2 o'clock, so
$11 + 3 = 2$.

For $5 + 3 = 1$, try the days of the week, numbered from Monday as day 1
to Sunday as day 7. Three days after Friday (day 5) is Monday (day 1).

Both spaces go round in a circle and start again. On a clock the circle
has 12 steps, and in a week it has 7. For the "try this next": 5 months
after October (month 10) is March (month 3), so $10 + 5 = 3$ is right
when we count months.

</details>

**16. Explain.** Choose a game you like that is not on this page: a card
game, a video game, a sport, or anything else. Ask the four questions of
it, and find one rule that everyone assumes but that is not written
down.

<details class="dl-answer"><summary>answer</summary>

Here is one example, for the card game Snap.

- **What is named here?** The cards, each with a name like "the seven of
  hearts". The two piles, one for each player, and the pile in the middle.
- **What is promised?** Turning a card puts it face up on the middle
  pile. Saying "Snap!" first, when two cards match, wins you the middle
  pile.
- **What happens when?** Players turn cards one at a time, taking turns.
  After each card, everyone checks for a match.
- **What does this space let us do?** A normal pack of 52 cards. You may
  only turn your own top card.

One rule nobody writes down: you turn the card away from you, so that
you do not see it before the other player does. Your game will have its
own. Look for the rules that people only mention when somebody breaks
them.

</details>

**17. Explain.** The tutorial page started with a board game and a recipe,
and came to Python last. Picture a friend who has never written any code,
and who asks you to teach them. Would you start with a game, or with a line
of Python? Give one reason for your choice, and one thing the other way
would do better. There is no single right answer. The "Why this way?" box
on the tutorial page says what this course chose, and why.

<details class="dl-answer"><summary>answer</summary>

There is no one right answer. A good answer weighs a few things.

- **Who your friend is.** Someone who came to learn programming may want
  to see the computer do something in the first minute. Someone who is
  nervous about computers may be glad to start with something they
  already know.
- **What the first lesson is for.** If it is the four questions, a game
  shows that they work on anything, not only on code. If it is how to run
  a cell, starting with code gets there sooner.
- **What each way gives up.** Game first is slower to reach Python. Code
  first can make the four questions look like computer words, when they
  are questions for any situation.

A strong answer names the person it is for, and says what the other way
would have done better. Either choice can work.

</details>
