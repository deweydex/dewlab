---
title: "Sorting a hand of cards: selection and insertion sort"
year: "2026-2027"
version: 2026.09.26.1
covers:
  two-ways-to-sort-a-hand:
    covers: [MIT-6.8]
    touches: [PDP-LO2]
  swapping-two-cards:
    touches: [MIT-6.8]
  selection-sort-find-the-smallest-again-and-again:
    covers: [MIT-6.8]
    touches: [MIT-6.7]
  insertion-sort-slide-each-card-into-place:
    covers: [MIT-6.8]
    touches: [MIT-6.7]
  counting-the-comparisons:
    covers: [MIT-6.8]
    touches: [MIT-6.4]
  a-new-list-and-the-old-one-left-alone:
    touches: [PDP-LO8, MIT-6.8]
  two-tools-for-your-toolkit:
    covers: [MIT-6.8]
    touches: [PDP-LO8, PDP-LO10]
---

# Sorting a hand of cards: selection and insertion sort

Someone deals you seven cards. Before you play, you put them in order,
lowest on the left. You do it without thinking, in a few seconds. But
what exactly did your hands do? And how many moves did it take?

Your hands already know at least one algorithm, and this page writes
it down. One of the two ways people
sort cards does almost no work on a hand that is already in order. The
other does exactly as much work on that hand as on any other.

On the last page, binary search needed a sorted list, and Python's
`sorted()` made one for us. This page shows how sorting works inside.

On this page we:

- write down, step by step, two ways people sort a hand of cards
- swap two values in a list, and see why the order of the steps matters
- turn each way into code: selection sort and insertion sort
- count the comparisons each one makes, and find that the starting
  order matters to one of them
- promise a new sorted list and leave the old one alone
- add `selection_sort` and `insertion_sort` to the toolkit

> **The space we're in.** We work with a list of values that can be compared with
> `<`: numbers, or words, which compare the way a dictionary orders
> them. To keep things plain, a card is its number: Ace is 1, Jack is
> 11, Queen is 12 and King is 13, and we leave the suits out. We usually
> do not say it, but a sort only ever compares two values at a time.
> It never sees the whole hand at once, the way your eye does.

## Warm-up

Two questions from earlier pages. The first is from
[Finding things fast](tutorial:finding-things-fast), and the second
from
[A row of numbers](tutorial:a-row-of-numbers#two-names-for-one-list).

```question
id: sorting-hand-warm-up-1
type: multiple-choice
answer: 2

Which of these lists can `binary_search` be trusted with?

- `[9, 4, 7, 1]`
  - `binary_search` throws away half the list at each look, which only works when the list is in order.
- `[1, 4, 7, 9]`
  - In order, so each look tells `binary_search` which half to throw away.
- both, since they hold the same numbers
  - The same numbers, but only one list is in order, and the order is what the search relies on.
```

```question
id: sorting-hand-warm-up-2
type: multiple-choice
answer: 1

`week = [11, 13, 9]`, then `forecast = week`, then
`forecast[0] = 20`. What is `week[0]` now?

- 20
  - `forecast = week` gives the same list a second name, so a change through one name shows through both.
- 11
  - This is what you would see if `forecast = week` made a copy.
- It stops with an error.
  - A list can be changed through any of its names, so the line runs.
```

## Two ways to sort a hand

Watch someone sort a hand of cards, and you will usually see one of two
ways.

**The first way.** Look through the whole hand for the lowest card, and
put it at the left end. Then look through the rest for the lowest one
left, and put it next. Keep going until every card has been chosen.

**The second way.** Hold the cards in a fan, and take them from left to
right. The first card is in order on its own. Take the second, and
slide it to the left of the first if it is lower. Take the third, and
slide it left past every card that is higher than it, until it meets a
lower one. Each new card goes into its place among the cards you have
already sorted.

To *sort* a list is to put its values in order. On this page, "in
order" means from smallest to largest, which is called *ascending*
order. A way of doing it, written as clear steps, is a *sorting
algorithm*: a recipe, like the tea-making robot's on
[Recipes are algorithms](tutorial:recipes-are-algorithms).

```question
id: sorting-hand-two-ways-1
type: multiple-choice
answer: 3

Someone is dealt cards one at a time, and puts each new card into its
place as it arrives. Which way is that?

- The first way: find the lowest each time.
  - Finding the lowest needs all the cards in front of you, and these arrive one at a time.
- Neither way.
  - It is one of the two: each card goes into its place among the cards already held.
- The second way: slide each card into its place.
  - Each new card slides into its place among the cards already held, as it arrives.
```

The second way works even while the cards are still arriving. The
first way needs the whole hand in front of it, because it cannot know
the lowest card until it has seen them all.

<aside class="dl-note" id="sorting-hand-note-bridge">

**The bridge player's method.** Donald Knuth's *The Art of Computer
Programming*, the best-known set of books on algorithms, begins its
section on insertion sort with card players. It calls insertion sort
the method a bridge player uses to put a hand in order. Programmers
have been learning sorting from a hand of cards for over fifty years.

</aside>

## Swapping two cards

Both ways move cards about, and the smallest move is a *swap*: two
values change places. Here is a hand as a list: 7, 3, Queen, Ace, 9.
We want to swap the 7 at index 0 and the Ace at index 3.

Here is a first try. Before you run it, read the two lines slowly.
What will the hand be afterwards?

```python exec
id: sorting-hand-swap-1
hand = [7, 3, 12, 1, 9]
hand[0] = hand[3]
hand[3] = hand[0]
print(hand)
```

It prints `[1, 3, 12, 1, 9]`. There are two Aces, and the 7 is gone.
The first line pointed `hand[0]` at the Ace. That was the only name
the 7 had, so it was lost. By the time the second line ran, `hand[0]`
was already 1.

With real cards you never have this problem, because you hold one card
in each hand. In code, the fix is the same idea. Keep the 7 under a
name of its own before it is replaced. Python can also do both at once:

```python exec
id: sorting-hand-swap-2
hand = [7, 3, 12, 1, 9]
hand[0], hand[3] = hand[3], hand[0]
print(hand)
```

This time it prints `[1, 3, 12, 7, 9]`. The order of events makes it
work. First, Python calculates everything on the right of the `=`, the
values 1 and 7. Only then does it point `hand[0]` at 1 and
`hand[3]` at 7. So nothing is lost.

## Selection sort: find the smallest, again and again

The first way has a name. A *selection sort* finds the smallest value
in the part of the list not yet sorted, and swaps it to the front of
that part. It does that again and again, until the whole list is
sorted. It "selects" one value each round.

Your toolkit's `smallest` from
[A row of numbers](tutorial:a-row-of-numbers#three-tools-for-your-toolkit)
gives the smallest value. For a swap we need its index as well, so the
inner loop keeps `smallest_at`, the index of the smallest card seen so
far. (A name like `smallest = ...` would hide the toolkit tool.)

The outer loop picks the `place` to fill: 0, then 1, then 2, and so on.
It stops one short of the end, because when every other card is in
place, the last one must be too. The function works on a copy made with
`.copy()`, so the hand it is given stays as it was.

Before you run it, write down on paper what the hand will look like
after the first round.

```python exec
id: sorting-hand-selection-1
def selection_steps(hand):
    """Selection sort a copy of hand, showing the cards after each round."""
    cards = hand.copy()
    for place in range(len(cards) - 1):
        smallest_at = place
        for i in range(place + 1, len(cards)):
            if cards[i] < cards[smallest_at]:
                smallest_at = i
        cards[place], cards[smallest_at] = cards[smallest_at], cards[place]
        print("place", place, ":", cards)
    return cards


hand = [7, 3, 12, 1, 9]
print(selection_steps(hand))
```

It takes four rounds. In round 1, the Ace was found at index 3 and swapped with
the 7 at index 0. In round 2, the smallest of the rest was the 3,
already at index 1, so it swapped with itself and nothing moved. In
round 3, the 7 swapped with the Queen. In round 4, the 9 swapped with
the Queen, and the hand was sorted.

Notice that the list is always in two parts: a sorted part on the left
that grows by one card each round, and the rest on the right.

<img src="selection-rounds.svg" alt="The hand 7, 3, 12, 1, 9, then the hand after each of the four rounds of selection sort, with the sorted part on the left shaded green. The Ace is 1 and the Queen is 12. Round 1: the smallest card, 1, swaps with the 7, giving 1, 3, 12, 7, 9. Round 2: the smallest left is 3, already in place, so nothing moves. Round 3: the 7 swaps with the 12, giving 1, 3, 7, 12, 9. Round 4: the 9 swaps with the 12, giving 1, 3, 7, 9, 12. The green part grows by one card each round.">

### Your turn

1. Sort a hand of your own, with six or seven cards. Before you run it,
   predict the first two rounds.
2. Try a hand that is already sorted, like `[1, 3, 7, 9, 12]`. Does
   selection sort notice that it has nothing to do?

```python exec
id: sorting-hand-selection-your-turn
print(selection_steps([13, 2, 8, 5, 11, 4]))
```

## Insertion sort: slide each card into place

The second way is an *insertion sort*. It takes each value in turn,
from the second one on, and inserts it into its place among the values
to its left, which are already sorted.

To slide a card left, the code moves each higher card one place to the
right, making a gap, until the card meets a lower one, or reaches the
left end. Then the card drops into the gap. This `while` loop has two
conditions joined by `and`, as on
[True, false and every case](tutorial:true-false-and-every-case):
"there is still a card to the left, and that card is higher".

The `while` line is the hardest line on this page to read. If it
feels tangled, read it aloud as "while there is a card to the left,
and that card is higher", or run the cell with a hand of three cards
first and watch what moves.

Before you run it, which card do you think moves the furthest?

```python exec
id: sorting-hand-insertion-1
def insertion_steps(hand):
    """Insertion sort a copy of hand, showing the cards after each card is placed."""
    cards = hand.copy()
    for place in range(1, len(cards)):
        card = cards[place]
        i = place
        while i > 0 and cards[i - 1] > card:
            cards[i] = cards[i - 1]    # move the higher card one place right
            i = i - 1
        cards[i] = card                # drop the card into the gap
        print("placed", card, ":", cards)
    return cards


print(insertion_steps(hand))
```

The 3 slid one place, past the 7. The Queen did not move, because the 7
to its left is lower. The Ace slid all the way to the front, past three
cards, so it moved the furthest. The 9 slid past the Queen and stopped at
the 7.

<img src="insertion-rounds.svg" alt="The hand 7, 3, 12, 1, 9, then the hand after each card is placed by insertion sort, with the sorted part on the left shaded green and the card just placed in amber. The 3 slides left past 1 card, to the front, giving 3, 7, 12, 1, 9. The 12 stays where it is, because the 7 to its left is lower. The 1 slides left past 3 cards, to the front, giving 1, 3, 7, 12, 9. The 9 slides left past 1 card and stops at the 7, giving 1, 3, 7, 9, 12.">

The list is in two parts here too, a sorted part on the left and the
rest. But the parts grow in a different way. Selection sort chooses
which card comes next, by looking at all the rest. Insertion sort takes
whichever card comes next, and does the work of finding its place.

```question
id: sorting-hand-insertion-2
type: multiple-choice
answer: 2

The line `card = cards[place]` keeps the card under its own name before
the loop. Why is that needed?

- It makes the code shorter.
  - It adds a line, so the code is longer.
- The first move, `cards[i] = cards[i - 1]`, puts another card at that index, and the card would be lost.
  - `cards[i] = cards[i - 1]` writes over the card at that index, so it has to be kept somewhere first.
- `cards[place]` cannot be used inside a `while` loop.
  - An index can be used inside a `while` loop; the trouble is that the card at it changes.
```

## Counting the comparisons

Which way takes fewer moves? For a computer, the step we count is the
*comparison*: looking at two values to see which is smaller. Each
comparison is one `<` or `>` between two cards.

We add a counter to each sort, as we did for the searches on
[Finding things fast](tutorial:finding-things-fast#counting-the-looks).
For insertion sort there is one detail. The `while` loop stops for one
of two reasons: the card reached the left end, or it met a lower card.
The second reason cost a comparison too, so the counter adds 1 for it
after the loop.

```python exec
id: sorting-hand-count-1
def selection_comparisons(hand):
    """Selection sort a copy of hand. Return how many comparisons it made."""
    cards = hand.copy()
    comparisons = 0
    for place in range(len(cards) - 1):
        smallest_at = place
        for i in range(place + 1, len(cards)):
            comparisons = comparisons + 1
            if cards[i] < cards[smallest_at]:
                smallest_at = i
        cards[place], cards[smallest_at] = cards[smallest_at], cards[place]
    return comparisons


def insertion_comparisons(hand):
    """Insertion sort a copy of hand. Return how many comparisons it made."""
    cards = hand.copy()
    comparisons = 0
    for place in range(1, len(cards)):
        card = cards[place]
        i = place
        while i > 0 and cards[i - 1] > card:
            comparisons = comparisons + 1
            cards[i] = cards[i - 1]
            i = i - 1
        if i > 0:
            comparisons = comparisons + 1    # the one that found a lower card
        cards[i] = card
    return comparisons
```

Now three hands of five cards: our hand, a hand already in order, and a
hand in reverse order. Guess each count before you run it.

```python exec
id: sorting-hand-count-2
hands = [[7, 3, 12, 1, 9], [1, 3, 7, 9, 12], [12, 9, 7, 3, 1]]
for five_cards in hands:
    print(five_cards, selection_comparisons(five_cards), insertion_comparisons(five_cards))
```

| Hand | Selection sort | Insertion sort |
|---|---|---|
| 7, 3, Q, A, 9 | 10 | 7 |
| already in order | 10 | 4 |
| in reverse order | 10 | 10 |

Selection sort makes 10 comparisons every time, even on the hand that
was already in order. I find that a strange result. It does all that
work to learn nothing new. It has to look at every card left to be sure
which is the smallest, whatever the order.
In the first round it compares 4 pairs, then 3, then 2, then 1:

$$4 + 3 + 2 + 1 = 10$$

That is the sum from
[Doing it again](tutorial:doing-it-again#sigma-a-loop-written-by-mathematicians),
$1 + 2 + \dots + (n - 1)$, for a hand of $n$ cards. Gauss's formula
gives it at once:

$$\sum_{i=1}^{n-1} i = \frac{(n-1)n}{2}$$

In words: for $n$ cards, selection sort makes $n$ times $n - 1$,
halved, comparisons. For 5 cards that is $\frac{4 \times 5}{2} = 10$.

Insertion sort is different. A hand already in order costs only 4
comparisons. Each card looks once to its left, finds a lower card, and
stays. A hand in reverse order costs 10, because every card slides all
the way to the front. For insertion sort, the order of the cards when
we start decides how much work there is. So order matters in the data,
as well as in the code.

### Your turn

1. Before you run anything, use the formula: how many comparisons does
   selection sort make on a full suit of 13 cards? And on a whole pack
   of 52?
2. Check the 13-card answer with `selection_comparisons(list(range(13, 0, -1)))`.
   (`range(13, 0, -1)` counts down from 13 to 1.)
3. Try `insertion_comparisons` on the same 13 cards in reverse order,
   and then in order. What do you notice?

```python exec
id: sorting-hand-count-your-turn
print(selection_comparisons(list(range(13, 0, -1))))
```

The next page,
[Racing the sorts](tutorial:racing-the-sorts), counts comparisons on
lists of 10, 100 and 1,000 values, and plots them.

## A new list, and the old one left alone

Python gives us two ways to sort, and they keep different promises.
What do you think each `print` shows?

```python exec
id: sorting-hand-new-list-1
hand = [7, 3, 12, 1, 9]
in_order = sorted(hand)
print(hand, in_order)

answer = hand.sort()
print(hand, answer)
```

`sorted(hand)` returns a new list, in order, and leaves `hand` as it
was. `hand.sort()` does something else. It sorts `hand` itself, in
place, and returns `None`. It is a procedure, in the words of
[Machines that take a number](tutorial:machines-that-take-a-number#functions-that-give-back-and-procedures-that-do).
So `answer` is `None`. A line like `hand = hand.sort()` looks
harmless, but it loses the whole hand.

Both are useful. Sorting in place needs no second list, which matters
when the list is huge. A new list keeps the original, which matters
when someone else is still using it. Think of a playlist in the order a
friend made it. You want to see it sorted by title, and your friend
wants their order back.

Our own sorts promise a new list, like `sorted()`. That is why each of
them starts with `cards = hand.copy()`. Without the copy, `cards` would
be a second name for the same list, as on
[A row of numbers](tutorial:a-row-of-numbers#two-names-for-one-list),
and every swap would change the caller's list too.

## Two tools for your toolkit

Here are the two sorts as toolkit tools, with their promises. Each
returns a new sorted list, and leaves `values` alone. They are
stubs. For each one, start from the `..._steps` version above: keep the
copy, delete the `print` line, and rename `hand` and `cards` so that
the names fit any list, not only cards.

```python exec
id: sorting-hand-toolkit
toolkit: yes
def selection_sort(values):
    """Return a new list with the items of values in ascending order,
    found by selection sort. values itself is not changed.

    The items must be comparable with <, like numbers or words.
    """
    ...


def insertion_sort(values):
    """Return a new list with the items of values in ascending order,
    found by insertion sort. values itself is not changed.

    The items must be comparable with <, like numbers or words.
    """
    ...
```

```python toolkit-reference
for: sorting-hand-toolkit
def selection_sort(values):
    """Return a new list with the items of values in ascending order,
    found by selection sort. values itself is not changed.

    The items must be comparable with <, like numbers or words.
    """
    items = values.copy()
    for place in range(len(items) - 1):
        smallest_at = place
        for i in range(place + 1, len(items)):
            if items[i] < items[smallest_at]:
                smallest_at = i
        items[place], items[smallest_at] = items[smallest_at], items[place]
    return items


def insertion_sort(values):
    """Return a new list with the items of values in ascending order,
    found by insertion sort. values itself is not changed.

    The items must be comparable with <, like numbers or words.
    """
    items = values.copy()
    for place in range(1, len(items)):
        item = items[place]
        i = place
        while i > 0 and items[i - 1] > item:
            items[i] = items[i - 1]
            i = i - 1
        items[i] = item
    return items
```

How do your two sorts compare with one way to write them? The table
below runs the same calls on your tools and on a solution, side by side.
The rows try each promise at its edges: an empty list, one item, items
that repeat, words, and negative numbers. Two rows show `hands[0]`, the
first hand from the counting cell, after a sort. The promise says that
its order does not change. Where a row is different, try that call on
its own.

```inputs
for: sorting-hand-toolkit
selection_sort(hands[0])
hands[0]                                         # after selection_sort
selection_sort([])
selection_sort([5])
selection_sort([4, 1, 4, 1])
selection_sort(["Oisín", "Aoife", "Kwame"])
selection_sort([12, -50, 7, 0, 7, -3, 44, -50])
insertion_sort(hands[0])
hands[0]                                         # after insertion_sort
insertion_sort([])
insertion_sort([5])
insertion_sort([4, 1, 4, 1])
insertion_sort(["Oisín", "Aoife", "Kwame"])
insertion_sort([12, -50, 7, 0, 7, -3, 44, -50])
```

```solution
for: sorting-hand-toolkit
def selection_sort(values):
    """Return a new list with the items of values in ascending order,
    found by selection sort. values itself is not changed.

    The items must be comparable with <, like numbers or words.
    """
    items = values.copy()
    for place in range(len(items) - 1):
        smallest_at = place
        for i in range(place + 1, len(items)):
            if items[i] < items[smallest_at]:
                smallest_at = i
        items[place], items[smallest_at] = items[smallest_at], items[place]
    return items


def insertion_sort(values):
    """Return a new list with the items of values in ascending order,
    found by insertion sort. values itself is not changed.

    The items must be comparable with <, like numbers or words.
    """
    items = values.copy()
    for place in range(1, len(items)):
        item = items[place]
        i = place
        while i > 0 and items[i - 1] > item:
            items[i] = items[i - 1]
            i = i - 1
        items[i] = item
    return items
```

```hint
for: sorting-hand-toolkit
after: 3 runs
Which row is different? Try `print(selection_sort([3, 1, 2]))` on its
own. If it shows `None`, the function has no `return` yet. If a
`hands[0]` row is different, check that the function sorts a copy.
```

```hint
for: sorting-hand-toolkit
after: 8 runs
title: some steps
1. Copy the body of `selection_steps`, from `cards = hand.copy()` down
   to `return cards`, into `selection_sort`.
2. Take out the `print` line.
3. Change `hand` to `values`, and `cards` to `items`, everywhere in the
   body. Do the same for `insertion_sort`, from `insertion_steps`.

**Think about:** which rows would stay the same if you left out
`.copy()`, and which one would be different?
```

### Your turn

If you have not written the two sorts yet, open the solution under the
table and copy it into the stubs.

Sorting and searching go together. Your contacts from the last page
were in the order they were added.

1. Sort them with `insertion_sort`.
2. Find Priya in the sorted list with `binary_search`.
3. What does `binary_search` give if you search the list before
   sorting it? Why?

```python exec
id: sorting-hand-toolkit-your-turn
contacts = ["Siobhán", "Tomasz", "Aoife", "Kwame", "Niamh", "Oisín", "Priya", "Liam"]
# Sort, then search
```

<details class="dl-why"><summary>Why this way?</summary>

This page taught selection sort and insertion sort, two ways people
already sort cards. Many courses start with a third, bubble sort, which
walks along the list swapping any two neighbours that are in the
wrong order, again and again.

Bubble sort has real strengths. Its code is short, it only ever
compares neighbours, and it is a favourite in exams. The practice page
has you write it.

We started from cards because your hands already know these two ways.
The code then describes something you have done, and each line has a
move to match. Hardly anyone sorts cards by bubble sort. Starting from what
you already do is slower in places, but it makes the question "which
steps, in which order?" one you can answer from your own hands.

</details>

## Four questions, looking back

| The question | On this page |
|---|---|
| What is named here? | `place`, the index being filled or the card being placed; `smallest_at`, an index kept as a name; a copy, `cards`, with a name of its own |
| What is promised? | `selection_sort` and `insertion_sort` promise a new list in ascending order, and the old one unchanged; `.sort()` promises to change the list itself, and returns `None` |
| What happens when? | a swap calculates both values before it moves either; selection sort always makes $\frac{n(n-1)}{2}$ comparisons; insertion sort makes fewer when the list starts nearly in order |
| What does this space let us do? | anything that can be compared with `<`; one comparison of two values at a time; changing a list in place, or making a new one |

## What we have now

| Term or tool | What it means |
|---|---|
| sort, ascending order | put values in order; from smallest to largest |
| sorting algorithm | a way of sorting, written as clear steps |
| swap, `a[i], a[j] = a[j], a[i]` | two values change places; Python calculates the right-hand side first |
| selection sort | find the smallest of the rest, and swap it to the front of the rest; repeat |
| insertion sort | take each value in turn, and slide it into its place among the sorted values to its left |
| comparison | one look at two values, to see which is smaller: the step we count |
| $\frac{n(n-1)}{2}$ | the comparisons selection sort makes on $n$ values, and insertion sort's worst case |
| `sorted(values)` | Python's sort that returns a new list |
| `values.sort()` | Python's sort that changes the list in place, and returns `None` |
| `range(13, 0, -1)` | counting down: a third number in `range` is the step |
| `selection_sort`, `insertion_sort` | your two new toolkit tools |

The practice page is next. After it,
[Racing the sorts](tutorial:racing-the-sorts) races these two sorts
against a third, on lists much longer than a hand of cards.

For another route through the same ideas, with bubble sort as well,
the integrated course has
[Sorting a list: bubble, insertion and selection sort](tutorial:putting-things-in-order).

## Where to read more

Polylog (2022). *The Simplest Sorting Algorithm (You've Never Heard Of).*
<https://www.youtube.com/watch?v=_W0yUJlscRA>. It uses two loops and one
swap. It looks wrong, but it sorts. Which of this page's two sorts is it closest
to? Four minutes.
