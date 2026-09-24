---
title: "Finding things fast: linear and binary search — Practice"
practice_for: finding-things-fast
year: "2026-2027"
version: 2026.09.24.1
datasets: [life-expectancy]
---

# Finding things fast: linear and binary search — Practice

Each problem says what kind it is. **Predict** means guess first, then
run. **Make** means write something new. **Fix** means find one mistake
in code that looks fine. **Explain** means answer in words. **Another
way** means reach the same place by a second route. The answers are
folded away until you open them.

Your toolkit is loaded on this page: `linear_search` and
`binary_search` from the tutorial, and `largest`, `mean`, `total` and
the rest from earlier pages.

## Warm-up

Use this cell for any of the warm-up problems.

```python exec
id: finding-fast-practice-warm-up
import math

towns = ["Dublin", "Cork", "Galway", "Limerick"]
print(linear_search(towns, "Cork"))
```

**1. Predict.** What do `linear_search(towns, "Galway")` and
`linear_search(towns, "Sligo")` give? Say each answer before you run it
in the cell above.

<details class="dl-answer"><summary>answer</summary>

`linear_search(towns, "Galway")` gives 2: Galway is the third town, and
indexes start at 0. `linear_search(towns, "Sligo")` gives −1, because
Sligo is not in the list. The search looked at all four towns first.

</details>

**2. Predict.** A sorted list holds the 16 teams in a cup draw. At
most, how many looks does a binary search need to find one team? Work
it out by halving on paper, then check it with a loop.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Halve 16, rounding down, until 1 is left. Count the halvings.
2. A binary search makes one look for each halving, and one more look
   at the last team left.

**Think about:** what $\log_2 16$ is, and why.

</details>

<details class="dl-answer"><summary>answer</summary>

$16 \to 8 \to 4 \to 2 \to 1$ is 4 halvings, so the worst case is
$4 + 1 = 5$ looks. $\log_2 16 = 4$, because $2^4 = 16$.

```python
teams_left = 16
halving_count = 0
while teams_left > 1:
    teams_left = teams_left // 2
    halving_count = halving_count + 1
print(halving_count, "halvings, so", halving_count + 1, "looks at most")
print(math.log2(16))
```

</details>

**3. Make.** Here is a shopping list for a curry. Use `linear_search`
to find where `"coconut milk"` is, and print it with a sentence. Then
search for `"rice"`, which someone forgot to write down.

```python
shopping = ["onions", "garlic", "ginger", "coconut milk", "spinach", "chickpeas"]
```

<details class="dl-answer"><summary>answer</summary>

```python
shopping = ["onions", "garlic", "ginger", "coconut milk", "spinach", "chickpeas"]
print("coconut milk is at index", linear_search(shopping, "coconut milk"))
print("rice is at index", linear_search(shopping, "rice"))
```

Coconut milk is at index 3, the fourth item. Rice gives −1: time to add
it to the list.

</details>

**4. Explain.** A friend writes their own search. It gives back 0 when
the target is not there. What goes wrong when they use it?

<details class="dl-answer"><summary>answer</summary>

0 is a real index: it means "found, at the front". So a search that
also gives 0 for "not there" says the same thing about two different
answers. A program cannot tell "the first contact is Aoife" from "there
is no Aoife", and it would dial the first contact's number either way.
A "not found" answer has to be a value that can never be a real
answer. −1 works in many languages, as long as the caller checks for
it, because in Python `values[-1]` is also a real item: the last one.

</details>

## Core

**5. Make.** A playlist is playing "Linger". Use `linear_search` to
find the song that comes next, and print it. Then try it with the last
song, "Dreams", and then with a song that is not on the playlist.
What happens in each case?

```python exec
id: finding-fast-practice-playlist
playlist = ["Zombie", "Linger", "Galway Girl", "Sultans of Swing", "Dreams"]
# Find the song after "Linger"
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. `linear_search(playlist, "Linger")` gives the index of "Linger".
2. The next song is one index further on.
3. Try the same two lines with "Dreams", and with "Imagine".

**Think about:** what index `-1 + 1` is.

</details>

<details class="dl-answer"><summary>answer</summary>

```python
position = linear_search(playlist, "Linger")
print(playlist[position + 1])
```

This prints `Galway Girl`. With "Dreams", `position` is 4, and
`playlist[5]` stops with an `IndexError`, because there is no song
after the last one. With "Imagine", `position` is −1, and
`playlist[0]` is "Zombie". There was no error at all: the code played
the first song for a song that is not there. That is the quiet trap
from the tutorial, and the fix is to check first:

```python
position = linear_search(playlist, "Imagine")
if position == -1:
    print("That song is not on the playlist.")
elif position == len(playlist) - 1:
    print("That was the last song.")
else:
    print(playlist[position + 1])
```

</details>

**6. Fix.** A coach wants to know where a player is in the team list.
This search finds the first player, but says −1 for every other player,
even ones on the team. Run it, then find the mistake.

```python exec
id: finding-fast-practice-fix-team
def find_player(team, name):
    """Return the index of name in team, or -1 if name is not there."""
    for i in range(len(team)):
        if team[i] == name:
            return i
        else:
            return -1


team = ["Katie", "Ciara", "Aimée", "Orlaith", "Sinéad"]
print(find_player(team, "Katie"))
print(find_player(team, "Orlaith"))
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Follow the loop by hand for "Orlaith". What happens at `i = 0`?
2. `return` ends the whole function at once. How many names does this
   function ever look at?
3. When do we really know that a name is not there?

**Think about:** which line should wait until every name has been
looked at.

</details>

<details class="dl-answer"><summary>answer</summary>

The `else: return -1` sits inside the loop. So when the first name is
not a match, the function gives back −1 at once, without looking at
the others. We only know that a name is missing after the loop has
looked at every name, so `return -1` belongs after the loop:

```python
def find_player(team, name):
    """Return the index of name in team, or -1 if name is not there."""
    for i in range(len(team)):
        if team[i] == name:
            return i
    return -1


print(find_player(team, "Katie"))
print(find_player(team, "Orlaith"))
```

Now it prints 0 and 3.

</details>

**7. Predict.** A fitness tracker kept a week of step counts, in the
order of the days. Someone searches it with `binary_search`. What does
each line print? Guess all three before you run it.

```python exec
id: finding-fast-practice-steps
steps = [8200, 10400, 6100, 12000, 9000, 7300, 11500]
print(binary_search(steps, 12000))
print(binary_search(steps, 9000))
print(binary_search(steps, 6100))
```

<details class="dl-answer"><summary>answer</summary>

It prints 3, then −1, then −1. The first look is always the middle,
index 3, and that is 12000, so the first search is lucky. For 9000, the
search sees 12000, which is bigger, and throws away the right half,
where 9000 really is. For 6100, the second look is 10400, which is
bigger, so it throws away 6100 at index 2 along with it.

The list is in the order of the days, not in order of size, so binary
search's promise does not hold. `linear_search(steps, 9000)` gives 4,
and so would a binary search on `sorted(steps)`, once you work out the
new index.

</details>

**8. Another way.** Load the countries from the tutorial, and find
Ireland three ways: with `binary_search`, with `linear_search`, and with
Python's own `.index()`. Do all three agree? Then ask each one for
`"Atlantis"`.

```python exec
id: finding-fast-practice-countries
df = await load_csv("life-expectancy.csv")
countries = df[df.year == 2016]["country"].tolist()
print(len(countries))
```

<details class="dl-answer"><summary>answer</summary>

```python
print(binary_search(countries, "Ireland"))
print(linear_search(countries, "Ireland"))
print(countries.index("Ireland"))
print(binary_search(countries, "Atlantis"))
print(linear_search(countries, "Atlantis"))
```

All three give 97 for Ireland. For Atlantis, both of your tools give
−1. `countries.index("Atlantis")` does not: it stops with
`ValueError: 'Atlantis' is not in list`. The same search, with a
different promise about what happens when the target is missing. An
error is harder to miss than a −1, which is one reason Python chose it.

</details>

**9. Make.** In the guessing game, a friend thinks of a number from 1
to 100. Write a function `guesses_needed(secret)` that plays the game
the halving way, and gives back how many guesses it took. Then try it
on every secret from 1 to 100, and find the most guesses any secret
needed.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Keep `low = 1` and `high = 100`, and a count of guesses.
2. Each round, guess the middle, `(low + high) // 2`, and add 1 to the
   count.
3. If the guess is the secret, give back the count. If the guess is too
   low, `low` becomes the guess plus 1. If it is too high, `high`
   becomes the guess minus 1.
4. Build a list of `guesses_needed(secret)` for every secret, and use
   `largest` from your toolkit.

**Think about:** how this is the tutorial's `binary_looks`, with a
range of numbers in place of a list.

</details>

<details class="dl-answer"><summary>answer</summary>

```python
def guesses_needed(secret):
    """Play higher-or-lower on 1 to 100 by always guessing the middle.

    Return how many guesses it took to reach secret.
    """
    low = 1
    high = 100
    guesses = 0
    while low <= high:
        guess = (low + high) // 2
        guesses = guesses + 1
        if guess == secret:
            return guesses
        if guess < secret:
            low = guess + 1
        else:
            high = guess - 1
    return guesses


all_games = []
for secret in range(1, 101):
    all_games.append(guesses_needed(secret))
print(guesses_needed(50), guesses_needed(1), guesses_needed(100))
print(largest(all_games))
```

Secret 50 takes 1 guess, 1 takes 6 and 100 takes 7. The most any
secret needs is 7, as the tutorial's halving chain said.

</details>

**10. Explain.** On
[A row of numbers](tutorial:a-row-of-numbers#a-real-list-ireland-since-1950)
we made the list `ireland`, of life expectancy in each year from 1950
to 2016. It rises from 65.6 to 81.1. Someone wants a binary search to
find the first year it reached 70. Why can we not trust a binary search
on this list, even though the numbers mostly go up?

<details class="dl-answer"><summary>answer</summary>

A binary search needs the list to be in order all the way along. This
list is not: that page found ten years where life expectancy fell. It
passed 70 in 1960, at 70.23, and fell back to 69.69 in 1961. A binary
search that looks at one year and sees 69.69 decides that every
earlier year is lower, which is false. Mostly sorted is not sorted. For
a list like this, a linear search from the front is the move that
keeps its promise.

</details>

**11. Fix.** A café's prices are sorted, cheapest first. This binary
search finds some prices, but not €21, even though it is on the menu.
Run it, then find the mistake. Which other prices does it miss?

```python exec
id: finding-fast-practice-fix-prices
def find_price(sorted_prices, target):
    """Return an index where target is in sorted_prices, or -1."""
    low = 0
    high = len(sorted_prices) - 1
    while low < high:
        middle = (low + high) // 2
        if sorted_prices[middle] == target:
            return middle
        if sorted_prices[middle] < target:
            low = middle + 1
        else:
            high = middle - 1
    return -1


prices = [2, 5, 8, 13, 21]
for price in prices:
    print(price, find_price(prices, price))
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Follow the search for 21 on paper, with columns for `low`, `high`
   and `middle`.
2. What are `low` and `high` when the loop stops?
3. Was the item at that index ever looked at?

**Think about:** what it means when `low` and `high` are equal. How
many items are left to look at?

</details>

<details class="dl-answer"><summary>answer</summary>

The loop runs `while low < high`. When `low` and `high` are equal, one
price is still left to look at, but the loop stops without looking at
it. For 21, `low` and `high` both reach 4, and the search gives up. It
misses 5 the same way, when `low` and `high` both reach 1. The fix is one character: `while low <= high`.

```python
def find_price(sorted_prices, target):
    """Return an index where target is in sorted_prices, or -1."""
    low = 0
    high = len(sorted_prices) - 1
    while low <= high:
        middle = (low + high) // 2
        if sorted_prices[middle] == target:
            return middle
        if sorted_prices[middle] < target:
            low = middle + 1
        else:
            high = middle - 1
    return -1


for price in prices:
    print(price, find_price(prices, price))
```

Now every price is found. A test that searches for every item, as the
tutorial's toolkit tests do, catches this kind of mistake.

</details>

**12. Make.** About 5.1 million people live in Ireland. If every name
were in one sorted list, how many looks would a binary search need at
most? Use `math.log2`, and `math.floor`, which rounds down.

<details class="dl-answer"><summary>answer</summary>

```python
people = 5_100_000
print(math.log2(people))
print(math.floor(math.log2(people)) + 1)
```

$\log_2 5{,}100{,}000$ is about 22.3. Rounded down that is 22
halvings, and one more look at the last name gives 23 looks at most. A
linear search could need 5.1 million. (Python lets us write
`5_100_000` with underscores, to make a long number easier to read.)

</details>

## Stretch

Use this cell for any of the stretch problems.

```python exec
id: finding-fast-practice-stretch
scores = [120, 250, 310, 480, 520, 700]
print(binary_search(scores, 480))
```

**13. Make.** A game keeps its high scores sorted, lowest first. A new
score comes in. Write `where_it_goes(sorted_values, new_value)`, which
gives back the index where the new value should go so that the list
stays sorted. Use the binary search idea: at the end of the loop,
`low` is that index. Test it with 400, 50 and 900 on `scores`.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Start from `binary_search`'s loop, with `low` and `high`.
2. You do not need the `==` check: keep going until `low` passes
   `high`.
3. Give back `low` after the loop.
4. To check, put the value in with `scores[:i] + [value] + scores[i:]`
   and compare with `sorted()`.

**Think about:** why `low` ends one place to the right of the last
score that is smaller than the new one.

</details>

<details class="dl-answer"><summary>answer</summary>

```python
def where_it_goes(sorted_values, new_value):
    """Return the index where new_value can go so sorted_values stays in order."""
    low = 0
    high = len(sorted_values) - 1
    while low <= high:
        middle = (low + high) // 2
        if sorted_values[middle] < new_value:
            low = middle + 1
        else:
            high = middle - 1
    return low


for new_score in [400, 50, 900]:
    i = where_it_goes(scores, new_score)
    longer = scores[:i] + [new_score] + scores[i:]
    print(new_score, "goes at index", i, longer, longer == sorted(longer))
```

400 goes at index 3, 50 at index 0 and 900 at index 6, the end. Every
new list is still sorted. The next page,
[Sorting a hand of cards](tutorial:sorting-a-hand-of-cards), sorts a
whole list by putting each value where it goes, one at a time.

</details>

**14. Another way.** A league table is sorted highest score first.
`binary_search` cannot find 310 in the list below, though it is
there. Find a space where it works: first by changing the list, then by
changing the search.

```python exec
id: finding-fast-practice-league
league = [700, 520, 480, 310, 250, 120]
print(binary_search(league, 310))
```

<details class="dl-answer"><summary>answer</summary>

`binary_search` promises to work on a list sorted smallest first. Its
first look is 480. 310 is smaller, so it keeps the left half, which in
this list holds the bigger scores, and 310 is thrown away.

One way is to change the list: `league[::-1]` is the list backwards,
smallest first, and there `binary_search` works. The index it gives is
counted from the other end, so `len(league) - 1 - i` turns it back.

Another way is to change the search: in a list sorted largest first,
"after the middle" means "smaller", so the two moves swap.

```python
def binary_search_largest_first(values, target):
    """Like binary_search, for a list sorted largest first."""
    low = 0
    high = len(values) - 1
    while low <= high:
        middle = (low + high) // 2
        if values[middle] == target:
            return middle
        if values[middle] > target:
            low = middle + 1
        else:
            high = middle - 1
    return -1


i = binary_search(league[::-1], 310)
print(i, len(league) - 1 - i)
print(binary_search_largest_first(league, 310))
```

Both routes find 310 at index 3 of `league`: the backwards list has it
at index 2, and $6 - 1 - 2 = 3$. The move "throw away half" was right.
It needed a space where "after the middle" and "bigger" mean the same
thing, or a search that knows they mean the opposite.

</details>

**15. Make.** Over all 226 names in `countries`, how many looks does each search
need on average? Write two small counting functions, or copy
`linear_looks` and `binary_looks` from the tutorial. Search for every
country in turn, keep the counts in two lists, and use `mean` from your
toolkit. Use the `countries` list from problem 8, which holds a few
regions as well as countries.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Copy `linear_looks` and `binary_looks` from the tutorial.
2. Start two empty lists. For each country in `countries`, append its
   linear count to one list and its binary count to the other.
3. Print `mean` of each list, and `largest` of each list.

**Think about:** why the linear average is about half the length of the
list.

</details>

<details class="dl-answer"><summary>answer</summary>

```python
def linear_looks(values, target):
    """Search values from the front for target. Return how many items were looked at."""
    looks = 0
    for i in range(len(values)):
        looks = looks + 1
        if values[i] == target:
            return looks
    return looks


def binary_looks(sorted_values, target):
    """Binary search sorted_values for target. Return how many items were looked at."""
    looks = 0
    low = 0
    high = len(sorted_values) - 1
    while low <= high:
        middle = (low + high) // 2
        looks = looks + 1
        if sorted_values[middle] == target:
            return looks
        if sorted_values[middle] < target:
            low = middle + 1
        else:
            high = middle - 1
    return looks


linear_counts = []
binary_counts = []
for country in countries:
    linear_counts.append(linear_looks(countries, country))
    binary_counts.append(binary_looks(countries, country))

print(mean(linear_counts), largest(linear_counts))
print(round(mean(binary_counts), 2), largest(binary_counts))
```

The linear search needs 113.5 looks on average, and 226 at most. Each
name is searched for once, so on average the search goes about
halfway along. The binary search needs about 6.9 looks on
average, and 8 at most: most names are found on the last two or
three looks, because each halving has twice as many places to end as
the one before.

</details>
