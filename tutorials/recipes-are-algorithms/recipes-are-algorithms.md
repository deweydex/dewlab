---
title: "Recipes are algorithms"
year: "2026-2027"
version: 2026.09.24.1
covers:
  teaching-a-robot-to-make-tea:
    covers: [MIT-6.1, PDP-LO5]
  steps-that-repeat-and-steps-that-choose:
    covers: [PDP-LO6, PDP-LO5]
  writing-a-plan-in-pseudocode:
    covers: [PDP-LO6]
  names-that-hold-values:
    covers: [PDP-LO6]
    touches: [PDP-LO4]
  a-name-for-a-whole-recipe:
    covers: [PDP-LO5]
    touches: [PDP-LO8]
  algorithms-outside-the-kitchen:
    covers: [PDP-LO2, MIT-6.1]
---

# Recipes are algorithms

Imagine you have a robot in your kitchen. It is strong, it is careful,
and it will do anything you tell it. You ask it to make you a cup of tea,
and it stands there, doing nothing. It does not know what "make" means.

How would you teach a robot to make tea? It sounds like a silly question,
but it is the question every programmer answers, every day. A computer is
that robot.

On this page we:

- write steps that a robot could follow exactly
- find the steps that repeat, and the steps that choose
- write a plan in pseudocode, a halfway point between English and Python
- give names to values in Python, and a name to a whole list of steps
- look for algorithms outside the kitchen

> **The space we're in.** A kitchen, but a strange one. The robot knows
> only the words we give it. It does exactly what we write, in the order
> we write it, and it never guesses what we meant. Python works the same
> way. That makes the robot trustworthy: it will never surprise you by
> guessing. It is also the thing that usually goes unsaid when people
> call computers "smart".

## Warm-up

Two questions from [Four questions for any puzzle](tutorial:four-questions).

```question
id: recipes-warm-up-1
type: multiple-choice
correct: 2

What does `print(2 * "tea ")` show?

- `2tea`
- `tea tea `
- An error, because you cannot multiply text.
```

```question
id: recipes-warm-up-2
type: multiple-choice
correct: 4

A film starts at 11 o'clock and lasts 3 hours. One friend says it ends at
14, and another says it ends at 2. Which question settles it?

- What is named here?
- What is promised?
- What happens when?
- What does this space let us do?
```

## Teaching a robot to make tea

Here is a first try at instructions for the robot. Most people would
write something like this.

1. Boil the kettle.
2. Put a tea bag in a cup.
3. Pour the water in.
4. Add milk.

A person could follow these steps without any trouble. A person fills
the gaps without noticing. Let's see what happens when nobody fills them.

```question
id: recipes-empty-kettle
type: multiple-choice
correct: 2

When the robot starts, the kettle is empty. What happens at step 1?

- The robot fills the kettle, then boils it.
- The robot switches on the empty kettle.
- The robot stops and asks what to do.
```

The robot does exactly what step 1 says: it boils the kettle. Nothing
says "fill it first", so it does not. And there is more trouble after
that. At step 3, pour the water in where: the cup, or the sink? How much
water: a splash, or the whole kettle? Step 4 adds milk, but the whole
carton? And the tea bag is never taken out.

Here is a second try.

1. Fill the kettle with water up to the 1-cup line.
2. Switch the kettle on, and wait until it switches itself off.
3. Put one tea bag in the cup.
4. Pour water from the kettle into the cup until it is 1 cm from the top.
5. Wait 3 minutes.
6. Take the tea bag out of the cup, and put it in the bin.
7. Pour milk into the cup for 1 second.

This version is longer, and that is the point. Every step now has one
meaning. It says how much, and where. The steps come in a fixed order,
and step 6 depends on step 3 having happened first. And the list ends:
after step 7, the robot is finished.

On the last page, an algorithm was a list of clear steps that completes
a task. Now we can say what "clear" asks for. A good algorithm has:

- **one meaning for every step**, so that two robots following it would
  do the same thing;
- **a fixed order**, so that every step happens after the steps it needs;
- **an end**, so that it finishes, and does not go on for ever.

Notice the thing we changed most from the first try to the second. It
was the environment. The first try assumed a person's knowledge: that
kettles need water, that tea bags come out. The second try says those
things out loud.

## Steps that repeat and steps that choose

Now three friends call round. Two of them take milk, and one does not.
We could write the whole list out three times, once for each cup. But
nobody writes a recipe like that. Instead we write "for each cup, do
this", and "if they take milk, add milk".

So there are three shapes a step can have.

- **One after another.** Do this, then this, then this. This is
  sequence, which we met on the last page.
- **Choosing.** Do this only if something is true: "if they take milk,
  add milk". This is called *selection*, because the robot selects one
  path or another.
- **Repeating.** Do the same steps again: "for each cup", or "stir until
  the sugar is gone". This is called *repetition*. Programmers also call
  it *iteration*.

Every algorithm ever written is built from these three shapes. The order
in which a program's steps run, with its choosing and repeating, is what
programmers call *control flow*. That is the only time this page will
use that phrase. "What happens when?" asks the same thing in plain
words.

```question
id: recipes-shapes
type: fill-in-the-blank

"Stir until the sugar is gone" is {repetition|selection|sequence}. "If the milk smells sour, open a new carton" is {selection|repetition|sequence}.
```

Look again at "stir until the sugar is gone". A repeat needs a way to
stop. Sugar does dissolve, so this one stops. But "stir until the sand
is gone" would never stop, and a robot would stir for ever. So when you
write a repeat, it is worth asking: what makes it end?

## Writing a plan in pseudocode

Before a programmer writes Python, they often write a plan. *Pseudocode*
is a plan for a program, written in plain words, but laid out like a
program. No computer runs it; it is for people. ("Pseudo" means "not
real", so pseudocode is code that is not quite code.)

Here is our tea for friends, in pseudocode.

```text
SET cups TO 3
FILL the kettle with water for cups
BOIL the kettle
REPEAT for each cup:
    PUT one tea bag in the cup
    POUR boiled water into the cup
    WAIT 3 minutes
    TAKE OUT the tea bag
    IF this friend takes milk:
        ADD milk
SERVE the cups
```

There are no fixed rules for pseudocode, but a few habits help.

- A word in capitals says what to do.
- The lines pushed in to the right belong to the line above them. The
  five steps under `REPEAT` happen once for each cup. `ADD milk` happens
  only when the `IF` is true.
- `SET cups TO 3` gives the number 3 a name, `cups`. After that, the
  plan says `cups` wherever it means "however many cups we are making".
  If a fourth friend arrives, we change one line.

That last line is about storage: keeping a value under a name, to use
later. It is the next idea on this page.

### Your turn

Write a plan, in pseudocode, for making toast for some friends. Some
want butter and some want jam. Use `SET`, `REPEAT` and `IF` at least once
each.

Write it in the cell below. Each line starts with `#`, which makes it a
*comment*: a note for people, which Python skips. So you can run the cell
and nothing will go wrong. There is one possible answer at the bottom of
this section.

```python exec
id: recipes-toast-plan
# SET slices TO 4
# ...your plan here
```

<details class="dl-answer"><summary>one possible plan</summary>

```text
SET slices TO 4
REPEAT for each slice:
    PUT the slice in the toaster
    WAIT until it pops up
    IF this friend wants butter:
        SPREAD butter
    IF this friend wants jam:
        SPREAD jam
    PUT the slice on a plate
SERVE the plates
```

Yours may be quite different and still be right. A good test: could
someone who has never made toast follow your plan?

</details>

## Names that hold values

Python can hold a value under a name too. Before you run this cell,
what do you think it will show?

```python exec
id: recipes-names-1
cups = 3
water_ml = cups * 250
print(water_ml)
```

It shows `750`: three cups of 250 ml each.

The first line, `cups = 3`, makes the name `cups` point at the number 3.
A name used like this is called a *variable*. A variable is a name that
points at a value. The `=` sign here is an instruction: it means "make
this name point at this value". It helps to read it as "becomes", so
that `cups = 3` says "cups becomes 3".

The second line works out `cups * 250`, and makes the name `water_ml`
point at the answer.

Now a friend leaves and another two arrive, so we have 5 cups to make.
This next cell changes `cups` to 5, then shows `water_ml` again. Will it
show 750 or 1250? Make your guess, then run it to check.

```python exec
id: recipes-names-2
cups = 5
print(water_ml)
```

It still shows 750. This surprises almost everyone, so let's ask "what
happens when?".

`water_ml` was worked out when its line ran, and at that moment `cups`
was 3. The line did its job once, and then it was finished. Changing
`cups` later does not go back and do it again.

In a maths book, $\text{water} = 250 \times \text{cups}$ would be a rule
that stays true, whatever cups becomes. In Python, `water_ml = cups * 250`
is a step, done once, at one moment. Neither is wrong. They are two
different spaces, and in Python's space the order of the lines is
everything.

### Your turn

1. In the cell below, work out `water_ml` again, now that `cups` is 5,
   and show it. (Copy the line from the first cell.)
2. A café uses 30 ml of milk for each cup. Make a variable `milk_ml` that
   holds the milk for `cups` cups, and show it.
3. Change `cups` to 12 at the top of the cell, and run it again. Did
   both answers change?

```python exec
id: recipes-names-your-turn
cups = 5
# work out water_ml and milk_ml here
```

```hint
Which line gave `water_ml` its value in the first cell? What would
happen if that line ran again, now?
```

## A name for a whole recipe

A variable is a name for one value. Could we have a name for a whole
list of steps? A recipe card does this: "Tea" at the top, and the steps
underneath.

Here is the second try at tea, as a recipe card in Python. Before you
run it, what do you think will appear under the cell?

```python exec
id: recipes-card-1
def make_tea():
    print("Fill the kettle to the 1-cup line.")
    print("Boil the kettle.")
    print("Put one tea bag in the cup.")
    print("Pour the boiled water into the cup.")
    print("Wait 3 minutes, then take out the tea bag.")
```

Nothing appears. That is correct, and it is worth a moment. The word
`def` is short for "define". This cell writes a recipe card called
`make_tea`, with five steps on it, and puts it away. Writing a recipe
card does not make any tea.

To use the card, we write its name with brackets after it. That is
called *calling* the function. Now the steps run, in order, from the top.
How many lines do you expect this time?

```python exec
id: recipes-card-2
make_tea()
print("One cup done. Now the second.")
make_tea()
```

Eleven lines: five steps, then our note, then the same five steps again.
We wrote the steps once and used them twice.

In Python, a function is a name for a list of steps. That fits the
meaning from the last page, a promise: `make_tea` promises that, when you
call it, these five steps happen, in this order. The lines pushed in
under `def` are the steps that belong to the function. Python uses that
push to the right in the same way our pseudocode did.

A function can also take a value. Here, `cups` in the brackets is a
*parameter*: a name that stands for whatever number we give when we call
the function. Which numbers will the first line of each recipe show?

```python exec
id: recipes-card-3
def make_tea_for(cups):
    print("Fill the kettle with", cups * 250, "ml of water.")
    print("Put", cups, "tea bags in the pot.")
    print("Wait 4 minutes, then pour.")

make_tea_for(2)
make_tea_for(6)
```

The first call gives `cups` the value 2, and the second gives it 6. The
same card, two different pots. (When `print` is given several things,
separated by commas, it shows them all on one line with a space between
each.)

### Your turn

1. In the cell below, write a function `make_toast()` with at least three
   steps, each one a `print` line pushed in to the right.
2. Call it twice.
3. If you would like more: write `make_toast_for(slices)`, and make one
   step say how many slices to put in the toaster.

```python exec
id: recipes-card-your-turn
def make_toast():
    print("Put a slice of bread in the toaster.")
    # more steps here
```

```hint
Is every step pushed in by the same amount as the first `print` line?
And did you call the function, with brackets, on a line that is not
pushed in?
```

## Algorithms outside the kitchen

Once you look for algorithms, you find them everywhere. A few of them:

- **A washing machine** runs a fixed sequence: fill, wash, drain, rinse,
  spin. It repeats the rinse two or three times. It chooses a
  temperature from the dial you set.
- **A card payment at a shop** asks for your PIN. If it is right, the
  payment goes through. If it is wrong, it lets you try again, but only
  three times.
- **A music app on shuffle** picks a song you have not heard yet, plays
  it, and repeats until the playlist is done.
- **A satnav** looks at many possible routes, works out how long each
  one takes, and chooses the fastest.

Each of these was once a plan written by a person, then turned into
code. None of them is "smart" in the way a person is. Each one follows
its steps exactly, very fast, and very many times.

```question
id: recipes-satnav
type: multiple-choice
correct: 3

A satnav works out the time for every possible route, then picks the
fastest one. Which shapes of step does it use?

- Sequence only.
- Selection only.
- Repetition (for every route) and selection (picking the fastest).
```

If you would like another view of the same ideas, the page
[Algorithms, pseudocode and your first Python](tutorial:first-steps)
covers them in a different way.

## Four questions, looking back

| The question | On this page |
|---|---|
| What is named here? | `cups` and `water_ml` in Python, `cups` in pseudocode, and a whole recipe called `make_tea` |
| What is promised? | `make_tea()` promises five steps, in order; `make_tea_for(cups)` promises the right amount for any number of cups |
| What happens when? | steps run from the top, one at a time; a value is worked out when its line runs, not later |
| What does this space let us do? | the robot, and Python, do exactly what is written and nothing more; everything a person would assume must be said |

## What we have now

| Term | What it means |
|---|---|
| sequence, selection, repetition | the three shapes of step: one after another, choosing, repeating |
| iteration | another word for repetition |
| pseudocode | a plan in plain words, laid out like a program |
| comment | a line starting with `#`, for people; Python skips it |
| variable | a name that points at a value, made with `=` |
| `def` | defines a function: a name for a list of steps |
| calling a function | writing its name with brackets, which runs its steps |
| parameter | a name in a function's brackets that stands for the value it is given |

The most useful thing on this page is a habit. Before you write any
steps, ask what a robot would get wrong. The answer is usually something
you assumed without saying.
