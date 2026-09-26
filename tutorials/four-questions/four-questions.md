---
title: "Four questions for any puzzle"
year: "2026-2027"
version: 2026.09.25.1
covers:
  a-game-of-snakes-and-ladders:
    covers: [PDP-LO5]
  the-same-move-in-a-different-space:
    touches: [MIT-1.1]
  a-recipe:
    covers: [MIT-6.1, PDP-LO5]
  your-first-cell:
    touches: [PDP-LO4]
  the-same-move-in-python:
    touches: [PDP-LO4]
---

# Four questions for any puzzle

Have you ever sat down to a game that everyone else at the table
already knew? The rules fly past, people laugh at moves you do not
understand, and you feel a step behind. Many people who start maths or
programming again as adults know that feeling well.

Here is what a new player does, if they are brave. Before the first
roll, they ask: which piece is mine? What can I do on my turn? Who goes
first? And what are the rules here?

Those four questions are not only about games. We can ask them of a
recipe, a sum in maths, or a line of computer code. This page is about
those four questions, because they work on every page that comes after
it. You are allowed to ask them at any moment, and nobody will think
less of you for it.

On this page we:

- ask four questions of a board game
- see that the same move can mean different things in different places
- ask the same four questions of a recipe
- run our first line of Python, change it, and run it again

> **The space we're in.** This page assumes nothing: no maths, no
> computers, no memory of school. Every move is allowed here, including
> a guess that misses, and a guess that misses is often the fastest way
> to learn something. One thing usually goes unsaid, so we will say it: the Python
> on this page runs inside your own browser, and nothing you type is sent
> anywhere.

## A game of Snakes and Ladders

You may know this game already. If not, here it is. The board has 100
squares, numbered from 1 to 100. Each player has a piece that starts off
the board. On your turn, you roll a die and move your piece forward that
many squares. If you land at the bottom of a ladder, you climb to the top
of it. If you land on the head of a snake, you slide down to its tail.
The first player to reach square 100 wins.

Now let's ask our friend's four questions about it.

**Which piece is mine?** The game gives names to things. There is "the
red piece" and "the blue piece". Every square has a number, and the
number is its name: "square 38" points at one place on the board, and
only one. When you say "I'm on 38", everyone at the table knows where to
look.

**What can I do on my turn?** You roll the die, and the die promises you
a number from 1 to 6. You move that many squares. A ladder makes a
promise too. The ladder from square 4 to square 14 promises: land on 4,
and you end on 14. Something goes in (the square you landed on) and
something comes out (the square you finish on).

**Who goes first, and what happens next?** Players take turns, in order
around the table. Inside one turn there is an order too: first roll, then
move, then check for a snake or a ladder. If you checked for a ladder
before you moved, the check would be about the wrong square.

**What are the rules here?** The board has squares 1 to 100 and no
others. Pieces move forward, except when a snake sends them back. There
is one die, not two. Most of these rules are never written down. Everyone
at the table assumes them.

```question
id: four-q-square-97
type: multiple-choice
answer: 4

You are on square 97 and you roll a 6. There is no square 103. What
happens?

- You move to square 103.
  - Some families play this way, where you only need to reach 100 or beyond.
- You stay on square 97.
  - Some families play this way: you need the exact number to finish.
- You move to 100, then back 3 squares, to 97.
  - Some families play this way: bounce back off 100.
- It depends on the rules your family plays by.
  - The board does not say; the rules you agree on decide.
```

People play this in different ways. In some homes you need the exact
number to land on 100, so you stay where you are. In others you go up to
100 and then bounce back. Neither is wrong. They are two different sets
of rules, and the roll of 6 means something different in each one.

<aside class="dl-note" id="four-q-note-snakes">

**An old game.** Snakes and Ladders began in India, where it was called
Moksha Patam. The ladders stood for good deeds and the snakes for bad
ones. It reached England in the 1800s, and the rules have kept changing
from home to home ever since.

</aside>

## Four questions

The four questions we asked of the game are the four questions of this
whole course. Here they are with the short names programmers and
mathematicians give them.

| The question | Its name | In the game |
|---|---|---|
| What is named here? | naming | pieces, and numbered squares |
| What is promised? | functions | a roll gives 1 to 6; a ladder takes 4 to 14 |
| What happens when? | sequence | turns in order; roll, then move, then check |
| What does this space let us do? | environment | squares 1 to 100, one die, forward moves |

A *name* is a word or number that points at one thing, so that we can
talk about it. A *function* is a promise: give it something, and it gives
you something back. A *sequence* is the order things happen in. The
*environment* is the space we are working in: what is there, and which
moves are allowed.

You do not need to learn these four words by heart. The questions are
what matter, and they are allowed on every page, at any moment. When
something on a later page confuses you, one of these four questions is
usually a good place to start.

## The same move in a different space

Here is a small puzzle. It is 10 o'clock in the morning, and a train
journey takes 4 hours. When does the train arrive?

```question
id: four-q-clock
type: fill-in-the-blank

It is 10 o'clock. After 4 more hours, a clock with 12 hours on its face shows {2} o'clock.
```

So on a clock, 10 + 4 is 2. At school, that would be marked wrong. But
nobody at the train station thinks it is wrong. It is the right answer in
a different space. On a clock face, the numbers go round from 12 back to
1, so adding can bring you back to a smaller number.

<aside class="dl-note" id="four-q-note-clock">

**Clock arithmetic.** Mathematicians call this *modular arithmetic*.
Carl Friedrich Gauss set out its rules, and the way it is still written
today, in a book in 1801. Computers use it all the time, and Python has a sign for it, `%`, which
we meet two pages from now.

</aside>

The same happens with the roll of 6 on square 97. The move is the same;
the rules of the space decide what it means.

This is the most useful idea on this page. When a move "doesn't work",
the move is not foolish. It belongs to some space, and the question is
which one. So the fourth question, "what space are we in?", is always
allowed. You will meet it again and again in this course: in the
counting numbers 0, 1, 2, 3 and so on, where 3 − 5 has no answer; in Python, where some moves are
allowed and some are not; and even on the surface of a ball, where a
triangle's angles do not add up to 180°.

```question
id: four-q-lift
type: multiple-choice
answer: 2

You are on floor 3 of a building and you go down 5 floors. In which
building is that possible?

- A building whose lowest floor is the ground floor, floor 0.
  - With floor 0 at the bottom, 3 − 5 floors is below the lowest floor.
- A building with two floors of car park under the ground, floors −1 and −2.
  - Floors −1 and −2 give the building room to go 5 floors down from 3.
- Neither: 3 − 5 has no answer.
  - 3 − 5 is −2 with negative numbers; whether the building has a floor −2 is the question.
```

## A recipe

Now let's try the four questions on something from a kitchen. Here is a
recipe for about eight small pancakes.

1. Put 150 g of flour in a bowl.
2. Add 1 egg and 250 ml of milk.
3. Whisk until smooth. This mixture is now called the batter.
4. Heat a frying pan on the hob.
5. Melt a little butter in the pan, and pour in a small ladle of batter.
6. Cook until bubbles appear, then turn it over.
7. Repeat steps 5 and 6 until the batter is gone.

**What is named here?** The flour, the egg, the milk, the bowl and the
pan all have names. Step 3 does something interesting: it gives a new
name, "the batter", to a mixture of three things. After step 3 the recipe
never says "flour, egg and milk" again. It says "batter". A new name for
something made from other things saves a lot of words.

**What is promised?** "Whisk" is a promise: put in lumpy flour, egg and
milk, and you get smooth batter out. The whole recipe is a bigger
promise. Ingredients go in, and pancakes come out.

**What happens when?** The steps are numbered, and the numbers matter.
You cannot pour batter before you have made it. Step 7 sends you back to
step 5, again and again, until something is true: the batter is gone.

**What does this space let us do?** The recipe assumes a lot that it
never says. It assumes you have a hob, a pan and a ladle. It assumes you
know what "whisk" means. It assumes "a little butter" means about the
same thing to you as it did to the writer.

```question
id: four-q-swap-steps
type: multiple-choice
answer: 1

Which step could move to the very start of the recipe, and still give
the same pancakes?

- Step 4, heat the pan.
  - Heating the pan does not touch the batter, so it can happen first.
- Step 3, whisk until smooth.
  - Whisking needs the ingredients already in the bowl.
- Step 5, pour in the batter.
  - Pouring needs a hot pan and a smooth batter.
```

A list of steps like this one, clear enough to follow exactly and in
order, and one that finishes, has a name. An *algorithm* is a list of
clear steps that completes a task. Every recipe is trying to be one. The
next page, [Recipes are algorithms](tutorial:recipes-are-algorithms), is
about what it takes to write one so well that even a machine could
follow it.

## Your first cell

A computer needs the same four answers that a new player needs. So let's
meet one.

Below is a *cell*. A cell is a small box of Python code inside this page.
You can run it, and the result appears underneath. You can change it and
run it again. Nothing you do in a cell can break the page or your
computer, and every cell has a **reset** button that brings back the code
it started with.

To run a cell, press its **Run** button, or hold Ctrl and press Enter.
The first run can take a few seconds, because Python has to load in your
browser.

The screen you are reading this on is made of tiny squares of light. A
common kind of screen, called Full HD, has 1920 of them across and 1080
down. How many is that altogether? Make a guess before you press Run:
a thousand? A million? Then run it to check.

```python exec
id: four-q-first-cell
print(1920 * 1080)
```

You should see `2073600` under the cell: more than two million tiny
lights, on a thing you look at every day. I find that number surprising
every time. In Python, `*` means multiply, because a keyboard has no ×
key.

Let's ask the four questions of that one line.

**What is named here?** `print` is a name. Python already knows it; we
did not have to explain it.

**What is promised?** `print` is a function, and its promise is: give me
something in brackets, and I will show it on the screen.

**What happens when?** Python works out `1920 * 1080` first, and gets
2073600. Only then does `print` show it. The inside of the brackets
happens before the outside.

**What does this space let us do?** Python gives us `print` and `*`
without being asked. It also runs one line after another, from the top of
the cell down.

### Your turn

Try these, one at a time.

1. A phone screen might be 1080 across and 2400 down. Change the
   numbers and run the cell again. Does the answer match what you
   expected?
2. Change one of them to a very big number, like `3000000`, and run it.
   Python does not get tired of big numbers.
3. Press the cell's **reset** button, and see the first numbers come
   back.

That is all there is to a cell: read it, guess, run, change, run again.

## The same move in Python

Earlier, 10 + 4 meant one thing in ordinary numbers and another on a
clock. Does anything like that happen in Python?

Here is a cell with two lines. The first multiplies a number. The second
multiplies some text, written in quote marks. Text in quote marks is
called a *string*, because it is a string of letters, one after another.

Before you run it, what do you think the second line will show? Is it
allowed at all? Make a guess, even a wild one, then run it to check.

```python exec
id: four-q-same-move
print(4 * 7)
print(4 * "#")
```

The second line shows `####`. The same `*` does a different job, because
it is working in a different space. With numbers, `4 *` means "multiply
by 4". With text, `4 *` means "write it out 4 times". If you squint,
`####` is a row of four lit squares on a tiny screen. This unit ends by
drawing numbers in exactly that way.

Neither meaning is the "real" one. Each is right in its own space, in the
same way that 10 + 4 is 14 on a calculator and 2 on a clock. Python decides which
job `*` does by looking at what it is given, a number or a string.

### Your turn

The cell below is yours to play with. Try these, one at a time.

1. Run it as it is.
2. Change `"ha "` to a word of your own, and run it again.
3. What happens if you take out the space before the closing quote mark,
   so it says `"ha"`? Make a guess first, then run it.
4. Try `print(20 * "-")`. People use this to draw a line across the
   screen.

```python exec
id: four-q-your-turn
print(3 * "ha ")
```

<details class="dl-why"><summary>Why this way?</summary>

This page started with a board game and a recipe, and came to Python
last. Many courses start the other way round: the first page shows a line
of code, and the words for it come later.

Starting with code is a good choice for someone who came to learn
programming. They see the computer do something in the first minute, and
that can be exciting.

We started with a game because the four questions are not about
computers. They work on anything that has names, promises, an order and
rules. Most people have played a board game long before they meet any
Python. If the questions work on something you know, you have a reason
to trust them on something new.

</details>

## Four questions, looking back

Here are the four questions again, asked of all three things on this
page.

| The question | Snakes and Ladders | Pancakes | `print(1920 * 1080)` |
|---|---|---|---|
| What is named here? | pieces and squares | ingredients, and "the batter" | `print` |
| What is promised? | a roll gives 1 to 6; a ladder lifts you | whisking gives smooth batter | `print` shows what is in its brackets |
| What happens when? | turns in order; roll, move, check | numbered steps; repeat until done | the brackets first, then `print` |
| What does this space let us do? | squares 1 to 100, house rules | a hob, a pan, knowing "whisk" | `print` and `*`, without asking |

Three very different things, and the same four questions opened up each
one. That is the plan for the whole course. Whenever you meet something
new, in maths or in code, you already have four ways in.

## What we have now

| Term | What it means |
|---|---|
| name | a word or number that points at one thing |
| function | a promise: give it something, and it gives something back |
| sequence | the order things happen in |
| environment | the space we are working in, and the moves it allows |
| algorithm | a list of clear steps that completes a task |
| cell | a box of Python on the page that you can run, change and reset |
| `print()` | shows whatever is in its brackets |
| `*` | multiplies numbers; with a string, repeats it |
| string | text in quote marks |

Most of all, we have a question that is always allowed: "what space are
we in?"

## Where to read more

Up and Atom (2018). *Can You Guess Who's Lying? 3 Logic Riddles to Train
Your Problem Solving Skills.*
<https://www.youtube.com/watch?v=xjSjxVAbhJ8>. Three puzzles about people
who always tell the truth and people who always lie. Try the four
questions from this page on each one before Jade Tan-Holmes gives her
answer. About twelve minutes.
