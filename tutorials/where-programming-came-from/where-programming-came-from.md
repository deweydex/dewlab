---
title: "Where programming came from: from Lovelace to Python"
year: "2026-2027"
version: 2026.09.24.1
covers:
  a-machine-that-was-never-built:
    covers: [PDP-LO1]
  ada-lovelaces-notes:
    covers: [PDP-LO1]
  note-g-retold-in-python:
    covers: [PDP-LO1]
    touches: [MIT-6.4, PDP-LO8]
  six-programmers-and-a-wall-of-cables:
    covers: [PDP-LO1]
  a-program-that-writes-programs:
    covers: [PDP-LO1, PDP-LO3]
  basic-a-language-for-beginners:
    covers: [PDP-LO1, PDP-LO3]
  the-web-javascript-and-python:
    covers: [PDP-LO1, PDP-LO3]
  a-timeline-you-can-run:
    covers: [PDP-LO1]
    touches: [MIT-6.8]
---

# Where programming came from: from Lovelace to Python

In 1843, a woman in London published a program for a machine that did
not exist. The machine was never finished, and nobody ran her program for
more than a hundred years. What did it do? And what would it look like
if we wrote it today, in the Python you have been writing all along?

On this page we:

- meet the Analytical Engine, a computer made of gears
- read Ada Lovelace's notes, and retell her program in Python
- meet the people who programmed the first electronic computers
- see why Grace Hopper wanted a program that writes programs
- follow BASIC into schools and homes, and JavaScript onto the web
- arrive at Python, and put every date on a timeline you can run

> **The space we're in.** This page is history, and history has rules of
> its own. Every date and name here was checked against at least one
> careful source, and where historians still argue, we say so. The Python
> on this page is a modern retelling: it does what the old programs did,
> in today's words. One thing usually goes unsaid: every tool you use was
> made by people, for reasons, and those reasons explain a lot of what
> seems strange about programming.

## Warm-up

The first question is from
[Untangling a condition](tutorial:untangling-a-condition#de-morgans-laws),
and the second from
[When Python says no](tutorial:when-python-says-no#compilers-linkers-and-python).

```question
id: where-prog-warm-up-1
type: multiple-choice
correct: 3

De Morgan's laws say that `not (a and b)` always gives the same answer
as which of these?

- `not a and not b`
- `a or b`
- `not a or not b`
- `not (a or b)`
```

```question
id: where-prog-warm-up-2
type: fill-in-the-blank

A {compiler|linker|traceback} reads the whole program first and
translates it into instructions the machine can follow.
```

## A machine that was never built

Charles Babbage was an English mathematician. In 1834 he began to
design a machine he called the *Analytical Engine*. It was a calculating
machine made of gears, with no electricity at all, and it was designed
to follow any list of instructions it was given.

The design had two main parts, and both are still inside every
computer. The *store* held numbers while the machine worked, like the
names in a Python program. The *mill* did the arithmetic, like the part
of a computer that adds and multiplies. The instructions came in on
punched cards: stiff cards with holes in them.

The cards were borrowed from weaving. Joseph Marie Jacquard's loom used
punched cards to weave complicated patterns into cloth, one card for each
row of the pattern. Babbage saw that a card could say "add" or "divide"
in the same way that it said "lift this thread".

Babbage worked on the design for the rest of his life, but the money to
build it never came. When he died in 1871, only a small trial piece of
the mill had been made. It is in the Science Museum in London today.

## Ada Lovelace's notes

In 1842, an Italian engineer, Luigi Menabrea, published a paper in
French about Babbage's engine. Ada Lovelace translated it into English.
She was 27, and she had spent 1840 and 1841 studying advanced maths by
letter with Augustus De Morgan, the De Morgan of the warm-up. (His page
promised that we would meet her later in the course. Here she is.)

Lovelace did not only translate. She added seven notes of her own,
lettered A to G, and together they were about three times as long as
the paper. The translation came out in August 1843, signed only with her
initials, A.A.L.

Her notes saw further than the paper did. The engine, she wrote, "weaves
algebraical patterns just as the Jacquard-loom weaves flowers and
leaves". She saw that it could work on things other than numbers, if
those things followed exact rules. If the rules of harmony could be
written down, she wrote, the engine "might compose elaborate and
scientific pieces of music of any degree of complexity or extent".

The last note, *Note G*, is the famous one. It sets out, step by step,
how the engine could work out a sequence of numbers called the Bernoulli
numbers. Babbage supplied the formulas, and Lovelace turned them into a
table of every operation the engine would do, in order. Her letters show
her checking it with great care, and finding a mistake of Babbage's on
the way. Many historians call Note G the first published computer
program. Some historians argue about how much of it was Babbage's
work.

## Note G, retold in Python

The *Bernoulli numbers* are a sequence of fractions that appear in
formulas for adding up powers, such as $1^2 + 2^2 + \dots + n^2$. They
are named after Jacob Bernoulli, a Swiss mathematician, who wrote about
them in a book published in 1713, after his death. Seki Takakazu found the
same numbers in Japan, and his work was published a year earlier.

Each Bernoulli number is found from the ones before it. That makes them
a good job for a machine: a loop, with a list that grows. The only
trouble is that they are fractions, and floats would round them, as on
[Everything is ones and zeros](tutorial:everything-is-ones-and-zeros#why-01-02-is-not-03).
Python has a module for exact fractions. What do you expect each line
to print?

```python exec
id: where-prog-fractions
from fractions import Fraction

print(1 / 3 + 1 / 6)
print(Fraction(1, 3) + Fraction(1, 6))
print(Fraction(1, 3) * 3)
```

A *Fraction* is Python's exact fraction: a whole number over a whole
number, kept that way. `Fraction(1, 3)` is one third, exactly, and
adding fractions gives an exact fraction back. The float version
prints `0.5` too, but floats keep only about 16 digits.

Here is the rule for the Bernoulli numbers in words. The first one,
$B_0$, is 1. After that, each new one is chosen so that a certain
weighted sum of all the numbers so far comes out to 0. The weights are
combinations, the "choose" numbers from
[Orders and choices](tutorial:orders-and-choices#when-order-does-not-matter).
In symbols, for each $m$ from 1 on:

$$\sum_{k=0}^{m} \binom{m+1}{k} B_k = 0$$

This is a modern way to write the rule, not the one Lovelace's table
used. It gives the same numbers. The cell uses `combinations` from your
toolkit. Before you run it, guess: will every Bernoulli number be a
different fraction?

```python exec
id: where-prog-bernoulli
def bernoulli_numbers(how_many):
    """Return the first how_many Bernoulli numbers, B0 onwards, as exact fractions."""
    numbers = [Fraction(1)]
    for m in range(1, how_many):
        weighted_sum = Fraction(0)
        for k in range(m):
            weighted_sum = weighted_sum + combinations(m + 1, k) * numbers[k]
        # choose the new number so that the whole weighted sum is 0
        numbers.append(-weighted_sum / (m + 1))
    return numbers

bernoulli = bernoulli_numbers(9)
for position in range(len(bernoulli)):
    print("B", position, "=", bernoulli[position])
```

No: $B_4$ and $B_8$ are both $-\frac{1}{30}$. And after $B_1$, every
Bernoulli number in an odd place is 0. That explains
Lovelace's numbering. She skipped the zeros, and she named the ones
that were left $B_1, B_3, B_5, B_7$. So her $B_7$, the number Note G
was built to find, is the one we now call $B_8$:

```python exec
id: where-prog-her-numbering
for hers, ours in [(1, 2), (3, 4), (5, 6), (7, 8)]:
    print("Lovelace's B", hers, "is our B", ours, "=", bernoulli[ours])
```

Her $B_7$ is $-\frac{1}{30}$. Much later, people who ran her table on
modern computers found one line where the two numbers of a division
were the wrong way round. That one swap makes the table give
$-\frac{25621}{630}$ where it should give $-\frac{1}{30}$. It may have
been the printer's mistake and not hers. Either way, it is often called
the oldest bug on record, and it tells us something reassuring: the
first program had a bug too.

Why did anyone want these numbers? Bernoulli wrote that, with his
table, he found the sum of the tenth powers of the numbers from 1 to
1,000 in "less than half of a quarter of an hour". He gave the answer as
91,409,924,241,424,243,424,241,924,242,500. How long will your loop
take?

```python exec
id: where-prog-tenth-powers
tenth_powers = []
for number in range(1, 1001):
    tenth_powers.append(number ** 10)
print(total(tenth_powers))
```

Your loop agrees with Bernoulli, digit for digit. He did it by hand.

### Your turn

1. Change `bernoulli_numbers(9)` to `bernoulli_numbers(15)`. Are the
   odd places after $B_1$ still 0?
2. Look at $B_{12}$. Is it still a small fraction?
3. Change `** 10` to `** 2` and `1001` to `11`. The sum of the squares
   from 1 to 10 is 385. Does your loop agree?

## Six programmers and a wall of cables

A hundred years later, the machines became electronic. ENIAC, built in
the United States, was shown to the public at the University of
Pennsylvania on 15 February 1946. It had no
programming language. To give it a new program, people moved cables and
set switches by hand.

The first people to program it were six women: Betty Snyder, Jean
Jennings, Kay McNulty, Marlyn Wescoff, Frances Bilas and Ruth
Lichterman. They learned the machine from its wiring diagrams. Kay
McNulty was born in 1921 in Creeslough, County Donegal. She spoke only
Irish when her family moved to Philadelphia in 1924, and she went on to
take a degree in mathematics. None of the six was named in the press
release when ENIAC was shown to the public.

## A program that writes programs

By the 1950s, computers held their programs in memory, but a program was
still a long list of numbers. Writing it was slow, and one wrong digit
could break it.

Grace Hopper, an American mathematician, had an idea that many people
at the time did not believe in: the
computer itself could do the translating. Between 1951 and 1952 she
wrote the A-0 system for the UNIVAC I. It took short names for pieces of
code that were kept in a library, and it put the machine's program
together from them. It is often called the first compiler, the kind of
tool you met on
[When Python says no](tutorial:when-python-says-no#compilers-linkers-and-python).
This was a program whose job was to write another program.

Hopper then asked a further question: why should business programs be
written in maths symbols at all? Her team's language FLOW-MATIC, from
1955 on, used English words for its instructions.

A *high-level language* is a way of writing a program in words and
symbols that people can read, which a compiler or an interpreter then
turns into the machine's own instructions. Two famous ones came next,
each made for a different kind of user:

| Year | Language | Made for |
|---|---|---|
| 1957 | FORTRAN, by John Backus's team at IBM | scientists and engineers: its name is short for FORmula TRANslating |
| 1959 | COBOL, by a committee that met at the Pentagon | business records: it drew on FLOW-MATIC, and Hopper advised the committee |

They were built for different people, so they look different. The next
page looks at more differences like this.

## BASIC: a language for beginners

At 4 o'clock in the morning on 1 May 1964, at Dartmouth College in the
United States, the mathematician John Kemeny and a student typed RUN on
two terminals at the same time. Both programs worked. The language was
*BASIC*, short for Beginner's All-purpose Symbolic Instruction Code.
Kemeny and Thomas Kurtz made it so that every student could program,
not only scientists. Here is a BASIC program that adds up the numbers
from 1 to 10. It is to read, not to run:

```basic
10 LET S = 0
20 FOR I = 1 TO 10
30 LET S = S + I
40 NEXT I
50 PRINT S
60 END
```

Every line has a number, and the numbers give the order. Do you
recognise the loop? It is the running total from
[Doing it again](tutorial:doing-it-again#a-running-total).

Then BASIC went home. Microsoft's first product, in 1975, was a BASIC
for the Altair, an early computer sold as a kit. In December 1981 the
BBC Micro was launched, with BBC BASIC written by Sophie Wilson, and it
went into many schools in Britain. The ZX Spectrum and the
Commodore 64 followed in 1982, both with BASIC built in. Switch on a
Commodore 64 and the screen said `READY.`, waiting for a line of BASIC.
For many people, that was where their first program was written.

## The web, JavaScript and Python

In March 1989, Tim Berners-Lee, working at CERN in Switzerland, wrote a
proposal for a system that linked documents together. It became the
World Wide Web, and the first website went online on 6 August 1991.

Early web pages could show text and links, but they could not run a
program of their own. In May 1995, Brendan Eich at Netscape wrote the first version of a
language for the browser in about ten days. It was called Mocha, then
LiveScript, and in December 1995 it was named *JavaScript*. It shipped
in Netscape Navigator 2.0 in 1996, and today every web browser runs it.

Meanwhile, in December 1989, a Dutch programmer, Guido van Rossum,
wanted a hobby project for the week around Christmas. He worked at CWI,
a research centre in Amsterdam, and he began a new language that grew
out of an earlier one called ABC. He named it after the comedy show
*Monty Python's Flying Circus*, not the snake. *Python* 0.9.0 was
published on 20 February 1991. Your cells on this page run a version of
the same language, grown up.

## A timeline you can run

Here is the story so far as a list of pairs: a year and an event. The
list is not in order, on purpose. What does `sorted` do to a list of
pairs? Predict, then run it.

```python exec
id: where-prog-timeline
import matplotlib.pyplot as plt

events = [
    (1991, "Python 0.9.0"),
    (1843, "Lovelace's notes and Note G"),
    (1964, "BASIC at Dartmouth"),
    (1834, "Babbage begins the Analytical Engine"),
    (1995, "JavaScript"),
    (1946, "ENIAC shown to the public"),
    (1957, "FORTRAN"),
    (1952, "Hopper's A-0 compiler"),
    (1981, "BBC Micro"),
    (1959, "COBOL"),
]

in_order = sorted(events)
for year, event in in_order:
    print(year, event)

years = []
for year, event in in_order:
    years.append(year)
print("From first to last:", years[-1] - years[0], "years")

plt.figure(figsize=(8, 4))
plt.plot(years, range(len(years)), "o")
for row in range(len(in_order)):
    plt.text(in_order[row][0] + 2, row, in_order[row][1], va="center")
plt.xlim(1820, 2060)
plt.yticks([])
plt.xlabel("year")
```

`sorted` puts pairs in order by their first item, the year, and it would
look at the second item only if two years were the same. The picture
shows something a list hides. For a hundred years after Note G, there is
nothing: the ideas waited for machines that could run them. After 1946,
the events come closer and closer together.

### Your turn

1. Add `(1989, "Berners-Lee's proposal for the web")` anywhere in the
   list, and run the cell again. Where does it land?
2. Add a pair for the year you ran your first line of Python.
3. Which gap between two events in the list is the longest? Write a
   loop that finds it.

<details class="dl-why"><summary>Why this way?</summary>

This page told the history as a story of people and machines, with a
few programs you could run. The usual way is a list of generations:
first-generation machine code, then assembly, then high-level languages,
and so on, with a table of dates to learn.

The generations list is short and tidy, it is what many exams ask for,
and it puts the big steps in order.

We chose people because each step was somebody's answer to a real
problem: a loom's cards, a mistake-prone list of numbers, students who
were not scientists. Knowing the problem makes the tool make sense. The
cost is that this page left out many languages and many people, and
does not give you a neat list of generations.

</details>

## Four questions, looking back

| The question | On this page |
|---|---|
| What is named here? | the store's numbered places; $B_0, B_1, \dots$, which Lovelace named differently; languages named after a formula, a beginner's code and a comedy show |
| What is promised? | Note G promised the Bernoulli numbers; a compiler promises to turn words into the machine's instructions; `bernoulli_numbers` promises exact fractions |
| What happens when? | each Bernoulli number after the ones before it; a century between Note G and ENIAC; `sorted` putting the years in order |
| What does this space let us do? | a machine of gears, then of cables, then of stored programs, each allowing more; `Fraction` keeps exact values where floats would round |

## What we have now

| Term or tool | What it means |
|---|---|
| Analytical Engine | Babbage's design for a computer made of gears, begun in 1834, with a store, a mill and punched cards |
| Note G | Ada Lovelace's 1843 step-by-step table for working out Bernoulli numbers, often called the first published program |
| Bernoulli numbers | a sequence of fractions that appear in formulas for sums of powers |
| `Fraction(a, b)` | Python's exact fraction, from the `fractions` module |
| high-level language | a language people can read, turned into machine instructions by a compiler or an interpreter |
| BASIC | a language made in 1964 for beginners, later built into home computers |
| JavaScript | the language of the web browser, first written in 1995 |
| Python | the language of this course, first published in 1991 |

## Where to read more

[How programming languages came to be](tutorial:how-we-got-here), in
the Programming and Design Principles course, tells a shorter version
of this story with a different focus: machine code, assembly, and why
hexadecimal exists. It has codes to crack along the way.

Stephen Wolfram (2015). *Untangling the Tale of Ada Lovelace.*
<https://writings.stephenwolfram.com/2015/12/untangling-the-tale-of-ada-lovelace/>.
A careful read of her letters.

The practice page is next. On the page after it, one small task is
written in four of the languages you met here.
