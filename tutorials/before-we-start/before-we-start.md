---
title: "Before we start: how this module works"
year: "2026-2027"
version: 2026.09.26.1
---

# Before we start: how this module works

Take a normal sheet of paper. Fold it in half. Fold it in half again,
and again. How many times can you do this before the paper will not
bend any more? Make a guess before you look at the choices.

```question
id: paper-folds-1
type: multiple-choice
answer: 2

How many times can one normal sheet of paper be folded in half?

- About 3 times
  - The paper gets thick quickly. But you can fold it a few more times
    than this.
- About 7 times
  - After 7 folds, the paper is 128 layers thick, like a small
    notebook. It is too stiff to bend.
- About 12 times
  - A student in California folded paper 12 times, in 2002. The paper
    was a very long strip, more than a kilometre long.
- About 50 times
  - Each fold doubles the thickness. After 50 folds, a thin sheet of
    paper would reach three quarters of the way to the Sun.
```

You have already done the most useful thing on this page. You made a
guess before you knew the answer. Every page in this module starts like
this.

There is a surprise in the paper question. Each fold only doubles the
paper. But after 50 folds, the paper would reach most of the way to the
Sun. Doubling again and again is called a *power*. Later pages in this
module are about powers. For now, just notice the surprise.

## What this module is for

This module is about the maths that schools teach everyone: fractions,
powers, roots and logarithms. Many people leave school and think "I am
not a maths person". If you think that, this module is for you.

The name, *The Zen of Slashes and Surds*, comes from two things you will
meet. A slash is the line in a fraction, like the line in 1/2. A surd is
a number like the square root of 2. Its digits never end. Many people
find slashes and surds scary. At the end of the module, we hope they
feel normal. (*Zen* is a word for a calm mind.)

## Nothing to memorise

We will not memorise anything here. We practise an idea until it feels
normal and easy to use. That is called *fluency*.

Think of the way to a shop you visit every week. You did not learn the
way from a list. You walked it many times, and now you do not need to
think about it. Fluency in maths is like that. It comes from doing many
small problems, not from remembering rules.

Every rule in this module comes from a picture: a pizza cut into
slices, a sheet of folded paper, a square of beads. If you forget a
rule, you can make it again from its picture. The picture is always
there.

## A guess comes first

Each step asks a question first, and explains after. Make a guess, even
when you are not sure. Sometimes your guess and the answer are
different. That is the most useful kind of guess, because it shows you
exactly where to look.

Some questions ask how sure you are. One choice is always "I'm not sure
yet". Choose it, and a hint opens. Nothing on these pages keeps a score,
and nothing is sent anywhere.

## Calm is the goal

When learning goes well, you feel curious: you want to know what
happens next. Sometimes that feeling slowly changes. You start to feel
frustrated: annoyed, tired or stuck. It is useful to notice this change.
It usually means that a step was too big. A smaller step helps more
than trying harder.

So calm is a goal of this module, as well as the maths. You will see
this box twice on every page. It says the same thing every time.

{{include: setup/zen-calm-check.md}}

You can try it now, while nothing here is hard. How do you feel at
the moment? You do not need to write anything. Noticing is enough.

## Small steps up a mountain

Think of understanding as the top of a mountain. Nobody has to jump to
the top. Each page is a path of small steps. Most steps are one picture
and one question.

When a step feels too big, look under its question for a line that says
"stuck? here are some steps". Click it, and it opens. Inside, the step
is cut into smaller steps. Here is one to try.

A sheet of paper is folded in half 3 times. How many layers thick is it
now?

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Before any folds, there is 1 layer.
2. One fold puts the paper on top of itself, so 1 layer becomes 2.
3. The next fold does the same to those 2 layers.

**Think about:** what one fold does to any number of layers.

**Try this next:** how many layers after 4 folds?

</details>

<details class="dl-answer"><summary>answer</summary>

8 layers. Each fold doubles the layers: 1, then 2, then 4, then 8.

</details>

The steps come first. The answer waits in its own fold, after the
steps. Open the steps at any time. Open the answer when you have
tried.

## Hearts, letters or numbers

On many pages you can choose how the maths is written. We can write
the same pattern with shapes, with letters, or with numbers:

$$\heartsuit \times \heartsuit \times \heartsuit \qquad a \times a \times a \qquad 5 \times 5 \times 5$$

A shape means: *any number can be here. Look at the pattern.* A letter
in algebra means the same thing. Numbers let you check a pattern with a
calculator.

On these pages, a box under the title shows the three ways. Choose the
one that feels calmest. You can change it at any step, and the page
remembers your choice.

## Pictures, questions and a little Python

Most steps in this module are a picture and a question. Some pages also
have a box of Python. Python is a language for computers. The box holds
a small program that draws a picture or checks a sum. You do not need
to know any programming. Press **Run** under the box to see what it
does. Then change a number and run it again.

<details class="dl-why"><summary>Why this way?</summary>

At school, many people learned maths as rules to memorise and use
quickly. For many of them, the fear of maths started there, with speed
and memory.

This module does the opposite. A rule comes last, after a picture that
shows why it works. You write the rule in your own words before you see
ours. Nothing is timed. This way is slower. But you get a rule you can
make again when you forget it. And you get a way of working that stays
calm when the maths gets harder.

</details>

## Looking back

A step will feel too big one day. Which idea from this page would help
you then?

A challenge, if you want one. The paper question said that 50 folds
would reach most of the way to the Sun. Can you check it? The program
below doubles the paper 7 times. How can you make it fold 50 times? The
Sun is about 150,000,000 km away.

```python challenge
# How thick is a sheet of paper, folded again and again?
thickness_mm = 0.1
for fold in range(1, 8):
    thickness_mm = thickness_mm * 2
    print(fold, "folds:", thickness_mm, "mm")
```

## Read more

The pictures in this module come from the classrooms of Maria
Montessori. In a Montessori classroom, children hold fraction pieces and
beads in their hands before they write any maths down. Montessori's
first book in English,
[*The Montessori Method*](https://www.gutenberg.org/ebooks/39863)
(1912), is free to read.

The student who folded paper 12 times was Britney Gallivan. The story,
with the formula Gallivan found for how much paper each fold needs, is
on [Wikipedia](https://en.wikipedia.org/wiki/Britney_Gallivan).
