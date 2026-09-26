---
title: "Collections without repeats: sets"
year: "2026-2027"
version: 2026.09.25.1
datasets: [the-lost-world, the-war-of-the-worlds]
covers:
  two-playlists:
    covers: [MIT-2.1]
  is-it-in-the-set:
    covers: [MIT-2.1]
  on-both-lists-intersection:
    covers: [MIT-2.2]
  on-either-list-union:
    covers: [MIT-2.2]
  on-one-list-only-difference:
    covers: [MIT-2.2]
    touches: [MIT-2.4]
  everything-else-the-complement:
    covers: [MIT-2.2]
  two-books-thousands-of-words:
    covers: [MIT-2.2]
    touches: [MIT-2.1]
  sets-too-big-to-list:
    covers: [MIT-2.1]
  every-pair-and-every-smaller-set:
    covers: [MIT-2.2]
    touches: [MIT-5.2]
  from-sets-to-databases:
    touches: [MIT-2.2]
---

# Collections without repeats: sets

You and a friend each make a playlist in a music app. Some songs are on
both, and one of you has put a favourite in twice. Which songs are on
both playlists? And how many different songs are there between you?

A music app answers questions like these in a blink, for playlists of
thousands of songs. It uses a kind of collection that forgets repeats
and ignores order. By the end of this page you will use the same few
moves on two whole novels, one full of dinosaurs and one full of
Martians, and find out how many words they share.

On this page we:

- turn a list into a set, and see what a set keeps and what it drops
- ask whether a value is in a set, with `in`, written $\in$ in maths
- find what two sets share, what either one has, and what one has that
  the other does not, first for playlists and then for two real books
- take the complement of a set, and see why it needs a bigger set
  around it
- meet the empty set, and sets too big to list, such as $\mathbb{N}$
- make every pair from two sets, and every smaller set from one, and
  see eight screen colours appear
- see the same moves at work in a database

> **The space we're in.** Collections where only one thing matters:
> whether a value is in them or not. Their order does not matter, and
> neither does how many times a value was written down. Python gives us
> `set` with no import. One thing usually goes unsaid: a set in Python
> always holds a limited number of values, because it has to fit in the
> computer. A set in maths can go on for ever.

## Warm-up

The first question is from
[Kinds of data, and honest charts](tutorial:kinds-of-data-and-honest-charts),
and the second from
[Counting every outfit](tutorial:counting-every-outfit).

```question
id: collections-warm-up-1
type: fill-in-the-blank

`frequency_table(["tea", "coffee", "tea", "tea"])` has {2} keys, and
the frequency of `"tea"` is {3}.
```

```question
id: collections-warm-up-2
type: multiple-choice
answer: 3

A game offers 3 characters, each in 2 colours. How many pairs does
`all_pairs(characters, colours)` give?

- 2
  - This counts the colours only.
- 5
  - This adds the characters and the colours, rather than pairing them.
- 6
  - Each of 3 characters comes in each of 2 colours: 3 × 2.
- 9
  - This is 3 × 3, as if there were three colours.
```

## Two playlists

Here are the two playlists, as lists. Look for the song that appears
twice on each.

A *set* is a collection of different values, where the order does not
matter and each value counts once. `set(...)` makes a set from a list.
How many songs do you think each set will have?

```python exec
id: collections-playlists-1
mine = ["Zombie", "Linger", "Galway Girl", "One", "Linger", "Chasing Cars", "Dreams"]
yours = ["Take Me to Church", "Zombie", "Outnumbered", "Dreams", "Breakeven",
         "Zombie", "All I Want"]

my_songs = set(mine)
your_songs = set(yours)
print(len(mine), len(my_songs))
print(len(yours), len(your_songs))
print(my_songs)
```

Each list has 7 songs, and each set has 6. The set kept "Linger" once
and "Zombie" once, because a set only records whether a value is in it.

Look at the order of the last line. It is not the order of the list,
and it may change if you run the cell again: a set makes no promise
about order. When the order matters to us, `sorted(my_songs)` gives the
songs as a list, in alphabetical order.

The values in a set are its *elements*, or *members*. Maths writes a
set with curly brackets, as on
[Counting every outfit](tutorial:counting-every-outfit#outcomes-of-an-experiment),
and so does Python:

$$A = \{\text{Zombie}, \text{Linger}, \text{Dreams}\}$$

The number of elements in a set is its *cardinality*, written with
straight lines on each side: here $|A| = 3$. In Python, cardinality is
`len`.

Two sets are equal when they have the same elements, in any order. What
do you think each line will print?

```python exec
id: collections-playlists-2
print({1, 2, 3} == {3, 2, 1})
print([1, 2, 3] == [3, 2, 1])
print({1, 2, 2, 3} == {1, 2, 3})
print(len({"a", "b", "a", "a"}))
```

`True`, `False`, `True` and `2`. A list is a row, where the order is
part of what it is. A set is a bag, where only what is inside matters.

## Is it in the set?

On
[Chances that combine](tutorial:chances-that-combine), `in` asked
whether a value was one of the values in a list. It asks the same of a
set. Guess each answer, then run it.

```python exec
id: collections-in-1
print("Zombie" in my_songs)
print("Breakeven" in my_songs)
print("Breakeven" not in my_songs)
```

`True`, `False`, `True`. Maths has a symbol for "is an element of":
$\in$, a rounded letter E. With a line through it, $\notin$ means "is
not an element of". So

$$\text{Zombie} \in A \qquad \text{Breakeven} \notin A$$

reads "Zombie is an element of A, and Breakeven is not an element of
A".

For a long list, `in` looks at the values one by one. A set can answer
without looking through every value, using a short code made from each
value, called a hash, which
[Chances that combine](tutorial:chances-that-combine#the-birthday-problem)
mentioned. That is how the music app answers in a blink. Unit 6 counts
the steps.

## On both lists: intersection

Which songs are on both playlists? Before Python answers, let's answer
it with a loop, the long way, so that we can see what the short way
promises.

```python exec
id: collections-both-1
shared = []
for song in my_songs:
    if song in your_songs:
        shared.append(song)
print(sorted(shared))
```

Two songs: "Dreams" and "Zombie". The loop kept each of my songs that is
also one of yours.

The *intersection* of two sets is the set of elements that are in both.
Maths writes it $A \cap B$, and says "A intersect B" or "A and B". The
symbol looks like an upside-down U, and "and" is the word to remember:
in $A$ **and** in $B$. Python writes it `&`, the same sign as "and".

```python exec
id: collections-both-2
both = my_songs & your_songs
print(sorted(both))
print(both == set(shared))
```

The same two songs, and the two routes agree. The loop is the proof,
and `&` is the fast way.

## On either list: union

How many different songs are there between you? The *union* of two sets
is the set of elements that are in either one, or in both. Maths writes
it $A \cup B$, and says "A union B" or "A or B". The symbol is a U, for
union. Python writes it `|`, a straight line that is often on the key
beside the Z or above the Enter key.

Each of you has 6 songs. How many are in the union? Guess before you
run it.

```python exec
id: collections-either-1
either = my_songs | your_songs
print(len(either))
print(sorted(either))
```

Ten, not twelve. "Dreams" and "Zombie" are on both lists, and the union
holds each of them once. How to count a union without making it is the
subject of the next page.

### Your turn

1. Add a song of your own to both `mine` and `yours`, and run the first
   cell of this page again. Before you run the intersection and the
   union, say how their sizes will change.
2. What is `my_songs & my_songs`? And `my_songs | my_songs`? Guess, then
   check.

## On one list only: difference

Which songs are mine, and not yours? The *difference* $A \setminus B$,
said "A minus B" or "A without B", is the set of elements in $A$ that
are not in $B$. Python writes it with a minus sign, `-`.

Will `your_songs - my_songs` give the same songs as
`my_songs - your_songs`? Run it to check.

```python exec
id: collections-only-1
print(sorted(my_songs - your_songs))
print(sorted(your_songs - my_songs))
```

No: four songs each, and not the same four. Like $5 - 3$ and $3 - 5$,
the order of a difference matters.

One more: the songs on exactly one of the two lists, mine or yours but
not both. That is the *symmetric difference*, written $A \,\triangle\, B$.
Python writes it `^`. You met `^` on
[Bits that flip](tutorial:bits-that-flip#xor-on-single-bits), as
exclusive or: exactly one of two bits is 1. Here it means exactly one
of two sets holds the song.

```python exec
id: collections-only-2
print(sorted(my_songs ^ your_songs))
print((my_songs ^ your_songs) == (either - both))
```

Eight songs: the ten in the union, without the two in the
intersection.

## Two books, thousands of words

Now some real data. *The Lost World*, by Arthur Conan Doyle (1912),
sends four explorers to a plateau in South America where dinosaurs are
still alive. *The War of the Worlds*, by H. G. Wells (1898), lands
Martians near London. Both books are in dewlab's data folder. How many
different words do you think a whole novel uses? A thousand? Fifty
thousand? Pause here and guess. I'll wait.

The cell below loads both books, each as one long piece of text, and
makes a set of the words in each. You do not need to follow every line
of `words_in`. It keeps the novel between the header and the licence
that Project Gutenberg, a free online library, adds to each book. Then
`re.findall` finds every run of the letters a to z.

```python exec
id: collections-books-1
import re


def words_in(book):
    """Return the set of different words in a Project Gutenberg book."""
    start = book.find("\n", book.find("*** START"))    # after the library's header
    end = book.find("*** END")                         # before its licence
    return set(re.findall("[a-z]+", book[start:end].lower()))


lost_world = words_in(await load_text("the-lost-world.txt"))
war_of_the_worlds = words_in(await load_text("the-war-of-the-worlds.txt"))
print(len(lost_world), len(war_of_the_worlds))
print(len(lost_world & war_of_the_worlds), len(lost_world | war_of_the_worlds))
```

*The Lost World* uses 7,766 different words, and *The War of the
Worlds* 6,743. Did you guess more? *The Lost World* is about 77,000
words long, so about nine words in ten repeat a word it has already
used. The two books share 3,540 words, and between them they use
10,969.

Which words tell the two books apart? Guess each line before you run it.

```python exec
id: collections-books-2
for word in ["london", "dinosaur", "pterodactyl", "martian", "tripod"]:
    print(word, word in lost_world, word in war_of_the_worlds)
print(len(lost_world - war_of_the_worlds), len(war_of_the_worlds - lost_world))
```

Both books visit London. The dinosaurs and the flying pterodactyl are
only in *The Lost World*, and the Martians and their three-legged
fighting machines, the tripods, only in *The War of the Worlds*. 4,226
words are in the first book and not the second, and 3,203 the other
way round. A difference of two sets of words is a rough picture of
what makes each book its own.

## Everything else: the complement

Say the music library on your phone holds twelve songs. Which of them
are not on my playlist?

On
[Chances that combine](tutorial:chances-that-combine#not-and-at-least-once),
the complement of an event was everything that could happen except that
event. The complement of a set is the same idea: every element that is
not in the set. It is written $A'$, or sometimes $A^c$.

But "every element" of what? The complement only has an answer once we
say which elements there are to choose from. That bigger set is the
*universal set*, written $U$: everything we are talking about, here and
now. So $A' = U \setminus A$.

```python exec
id: collections-complement-1
library = either | {"Fairytale of New York", "Whiskey in the Jar"}
print(len(library))

not_mine = library - my_songs
print(len(not_mine))
print(sorted(not_mine))
```

Of the 12 songs in the library, 6 are not on my playlist. Change the
universal set to every song ever recorded, and the complement becomes
millions of songs. The set $A$ did not change; the space around it did.
The complement asks "what space are we in?" before it can answer at
all.

## Sets too big to list

Some sets are empty. The *empty set* is the set with no elements at
all. Maths writes it $\varnothing$, and its cardinality is 0. The songs
on both my playlist and an empty playlist make an empty set.

In Python, the empty set is `set()`. You might expect `{}`. What do
you think this cell prints?

```python exec
id: collections-empty-1
print(my_songs & set())
print(len(set()))
print(type({}))
```

The first line prints `set()`, which is how Python writes the empty
set. The last line says `dict`: `{}` makes an empty dictionary, from
[Kinds of data, and honest charts](tutorial:kinds-of-data-and-honest-charts#counting-a-frequency-table).
Dictionaries came to Python before sets did, so they got the curly
brackets first.

An empty set is often where a set begins. `.add(value)` puts one more
element into a set, and does nothing if it is already there.

```python exec
id: collections-empty-2
favourites = set()
favourites.add("Zombie")
favourites.add("Dreams")
favourites.add("Zombie")
print(sorted(favourites))
```

Two elements: the second "Zombie" changed nothing.

At the other end, some sets never stop. A *finite set* has a number of
elements we could count, even if it is large: the words in a novel,
the people in Ireland. An *infinite set* has no end, so no count. The number families from
[Numbers a computer can hold](tutorial:numbers-a-computer-can-hold#families-of-numbers)
are sets:

| Set | Its elements | Finite? |
|---|---|---|
| $\mathbb{N}$ | the natural numbers: 0, 1, 2, 3, … | infinite |
| $\mathbb{Z}$ | the integers: …, −2, −1, 0, 1, 2, … | infinite |
| $\mathbb{Q}$ | the rational numbers: every fraction of two integers | infinite |
| $\mathbb{R}$ | the real numbers: every point on the number line | infinite |
| $\mathbb{C}$ | the complex numbers, built in Unit 7, where −4 has a square root | infinite |

Each one sits inside the next. $A \subseteq B$, said "A is a *subset*
of B", means every element of $A$ is also in $B$. So
$\mathbb{N} \subseteq \mathbb{Z}$. In Python, `<=` asks the same
question of two sets.

A Python set cannot hold $\mathbb{N}$: it would never finish being
made. But we can still ask whether a number is in it, with a test that
describes the set by a rule. Maths writes a set by its rule like this,
said "the set of every x in Z such that x is 0 or more":

$$\mathbb{N} = \{x \in \mathbb{Z} : x \ge 0\}$$

```python exec
id: collections-infinite-1
def in_naturals(number):
    """True when number is a natural number: a whole number, 0 or more."""
    return number == int(number) and number >= 0


print(in_naturals(7), in_naturals(-2), in_naturals(3.5))
print({"Zombie", "Dreams"} <= my_songs)
print(both <= either)
```

`True False False`, then `True` and `True`. A finite set can be listed.
An infinite one needs a rule, and a function is a rule we can run.

```question
id: collections-infinite-2
type: multiple-choice
answer: 2

Which of these sets is infinite?

- the songs in every playlist on your phone
  - Huge, but a phone holds a finite number of songs.
- the even numbers
  - There is always a next even number: add 2.
- the people who have ever lived
  - An enormous number of people, but a finite one.
- the grains of sand on every beach in Ireland
  - More grains than anyone could count, but still a finite number.
```

## Every pair, and every smaller set

The *Cartesian product* $A \times B$, said "A cross B", is the set of
every pair $(a, b)$ with $a$ from $A$ and $b$ from $B$. You made it on
[Counting every outfit](tutorial:counting-every-outfit#a-tool-that-lists-every-pair):
it is `all_pairs`. And its size is the counting principle,
$|A \times B| = |A| \times |B|$. A web designer who wants to check a new
page on every device, in light mode and in dark mode, needs every pair:

```python exec
id: collections-pairs-1
devices = {"phone", "tablet", "laptop"}
modes = {"light", "dark"}
checks = set(all_pairs(devices, modes))
print(len(checks), len(devices) * len(modes))
print(("phone", "dark") in checks)
```

Six checks, as the counting principle promised.

The second way. A pixel on a screen has three small lights: red, green
and blue. Say each light can only be off or fully on. Which colours can
the pixel show? Guess how many before you read on.

Each colour is a subset of the lights. The *power set* of a set,
written $\mathcal{P}(A)$, is the set of all its subsets, including the
empty set and the whole set itself. Here is a way to build it. Start
with one colour, all lights off. Then, for each light, keep every colour
you have, and add a copy of each with the new light on.

```python exec
id: collections-power-1
lights = ["red", "green", "blue"]

colours = [set()]
for light in lights:
    with_light = []
    for colour in colours:
        with_light.append(colour | {light})
    colours = colours + with_light

for colour in colours:
    print(sorted(colour))
print(len(colours), "colours")
```

Eight colours, from no lights to all three. `colours` is a list of sets,
not a set of sets, because a Python set cannot hold a value that might
change, and a set can change. What do they look like? The next cell
draws one square for each, with each light at full strength (1) or off
(0).

```python exec
id: collections-power-2
import matplotlib.pyplot as plt

for position in range(len(colours)):
    strengths = []
    for light in lights:
        if light in colours[position]:
            strengths.append(1)
        else:
            strengths.append(0)
    plt.bar(position, 1, color=strengths, edgecolor="grey")
plt.axis("off")
```

Black, red, green, yellow, blue, magenta, cyan and white. Red and green
light make yellow. That surprises most people who learned to mix paint,
where red and green make brown: light adds, and paint takes away.

<aside class="dl-note" id="collections-note-teletext">

**Eight colours on television.** Teletext, the pages of news and
weather that televisions showed from the 1970s on, used exactly these
eight colours: each of red, green and blue was either fully on or off.

</aside>

Why eight? Each light is either on or off, so each new light doubles the
count: $2 \times 2 \times 2 = 2^3$. For a set of $n$ elements,

$$|\mathcal{P}(A)| = 2^n$$

It is the same count as the rows of a truth table on
[True, false and every case](tutorial:true-false-and-every-case#how-many-rows).
That is no accident: a row that says "red True, green True, blue False"
is the colour yellow.

### Your turn

1. Some early computers added a fourth element to each pixel, "bright",
   which made every colour stronger. Add it to `lights`, and run the
   first cell. Before you do, how many colours will there be?
2. With 10 elements, how many subsets? Work it out with `2 ** 10`
   first, then check it with the cell.
3. Use `combinations` from
   [Orders and choices](tutorial:orders-and-choices) to count the
   colours with exactly two of the three lights on. Which colours are
   they?

## From sets to databases

A database keeps its data in tables, and a table is close to a set of
rows: each row is there once, and the order of the rows is not part of
the table. So the moves on this page are database moves too. A SQL
`JOIN` matches the rows of two tables that share a value, such as a
customer's id, and keeps what they have in common, as an intersection
does. A `CROSS JOIN` makes every pair of rows from two tables, as
`all_pairs` does.

The Database Methods course builds real tables with SQL. Its page
[Joining two tables: foreign keys and JOIN](tutorial:a-second-table-and-a-join)
is where the JOIN is taught.

<details class="dl-why"><summary>Why this way?</summary>

This page used Python's own sets, and wrote only one loop, to show what
`&` promises. Another way is to build every set operation yourself,
from lists and loops, as the page
[Sets: building them from sorted lists](tutorial:sets-as-sorted-lists)
does.

Building them yourself shows exactly how a union is made, and is good
practice with loops and lists.

We chose the built-in sets because the subject here is the language:
$\cap$, $\cup$, $\setminus$ and $\in$, and what each one means. Each
symbol is a name for a move, and a reader who knows the names can read
a maths book, a SQL query and a Python program with the same ideas.
One loop checked one promise, and the rest of the page could be about
meaning.

</details>

## Four questions, looking back

| The question | On this page |
|---|---|
| What is named here? | a set, and its elements; the symbols $\in$, $\cap$, $\cup$, $\setminus$, $\triangle$ and $'$, each a name for a move; $\varnothing$, $U$, and the number families |
| What is promised? | a set holds each value once; `&` promises the same set as the loop that checks both; $\lvert A \times B \rvert = \lvert A \rvert \times \lvert B \rvert$, and $\lvert \mathcal{P}(A) \rvert = 2^n$ |
| What happens when? | a set keeps no order, so we sort it when order matters; the power set doubles once for each new element, as each light doubles the colours |
| What does this space let us do? | a Python set is finite, so an infinite set needs a rule; a complement needs a universal set before it has any answer |

## What we have now

| Term or tool | What it means |
|---|---|
| set, element | a collection of different values, with no order; a value in it |
| `set(values)`, `set()`, `.add()` | a set made from a list; the empty set; put one more element in |
| cardinality, $\lvert A \rvert$ | the number of elements; `len` in Python |
| $\in$, $\notin$ | is an element of; is not an element of: `in`, `not in` |
| intersection, $A \cap B$ | in both: `&` |
| union, $A \cup B$ | in either, or both: `|` |
| difference, $A \setminus B$ | in $A$ and not in $B$: `-` |
| symmetric difference, $A \triangle B$ | in exactly one: `^` |
| universal set $U$, complement $A'$ | everything we are talking about; everything in $U$ that is not in $A$ |
| empty set, $\varnothing$ | the set with no elements |
| finite, infinite | can be counted; never ends |
| subset, $A \subseteq B$ | every element of $A$ is in $B$: `<=` |
| $\mathbb{N}, \mathbb{Z}, \mathbb{Q}, \mathbb{R}, \mathbb{C}$ | the number families, as infinite sets |
| Cartesian product, $A \times B$ | every pair: `all_pairs` |
| power set, $\mathcal{P}(A)$ | every subset, $2^n$ of them |

The practice page is next. After it,
[Circles that overlap](tutorial:circles-that-overlap) draws two and
three sets as circles, and counts a union without making it.
