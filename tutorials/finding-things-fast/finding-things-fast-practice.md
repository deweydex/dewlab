---
title: "Finding things fast: linear and binary search — Practice"
practice_for: finding-things-fast
year: "2026-2027"
version: 2026.09.25.1
datasets: [exoplanets, life-expectancy]
---

# Finding things fast: linear and binary search — Practice

Each problem says what kind it is. **Predict** means guess first, then
run. **Make** means write something new. **Fix** means find the one
line in some code that does not do what its writer meant, and change
it. **Explain** means answer in words. **Another way** means reach the
same place by a second route. The answers are folded away until you
open them, and each one is one way through: yours may go another way.

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

**3. Make.** Here are the files in a folder, in the order they were
saved. Use `linear_search` to find where `"report.pdf"` is, and print
it with a sentence. Then search for `"backup.zip"`, which nobody made.

```python
folder = ["notes.txt", "photo.png", "song.mp3", "report.pdf", "data.csv", "map.svg"]
```

<details class="dl-answer"><summary>answer</summary>

```python
folder = ["notes.txt", "photo.png", "song.mp3", "report.pdf", "data.csv", "map.svg"]
print("report.pdf is at index", linear_search(folder, "report.pdf"))
print("backup.zip is at index", linear_search(folder, "backup.zip"))
```

The report is at index 3, the fourth file. The backup gives −1, after
the search has looked at all six files.

</details>

**4. Explain.** Schlomo, who is learning Python too, writes his own
search. It gives back 0 when the target is not there. His reason is a
fair one: 0 is the usual number for "nothing". What happens when he
uses his search?

<details class="dl-answer"><summary>answer</summary>

0 is a real index: it means "found, at the front". So Schlomo's search
says the same thing about two different results. A program cannot tell "the first contact is Aoife" from "there
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

**6. Fix.** A laptop keeps a list of the Wi-Fi networks it has joined.
This search finds the first network, but says −1 for every other one,
even ones on the list. Run it, then find the line that stops it.

```python exec
id: finding-fast-practice-fix-wifi
def find_network(networks, name):
    """Return the index of name in networks, or -1 if name is not there."""
    for i in range(len(networks)):
        if networks[i] == name:
            return i
        else:
            return -1


networks = ["eduroam", "HomeNet", "Library-Guest", "Station-WiFi", "Phone-Hotspot"]
print(find_network(networks, "eduroam"))
print(find_network(networks, "Station-WiFi"))
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Follow the loop by hand for "Station-WiFi". What happens at `i = 0`?
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
def find_network(networks, name):
    """Return the index of name in networks, or -1 if name is not there."""
    for i in range(len(networks)):
        if networks[i] == name:
            return i
    return -1


print(find_network(networks, "eduroam"))
print(find_network(networks, "Station-WiFi"))
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

**8. Another way.** Load the planets from the tutorial, and find
Proxima Cen b three ways: with `binary_search` on the sorted names,
with `linear_search`, and with Python's own `.index()`. Then ask each
one for `"Vulcan"`, a planet astronomers once looked for inside the
orbit of Mercury, and never found.

```python exec
id: finding-fast-practice-planets
df = await load_csv("exoplanets.csv")
planets = df["name"].tolist()
planets_in_order = sorted(planets)
print(len(planets), "planets, on 25 September 2026")
```

<details class="dl-answer"><summary>answer</summary>

```python
print(binary_search(planets_in_order, "Proxima Cen b"))
print(linear_search(planets, "Proxima Cen b"))
print(planets.index("Proxima Cen b"))
print(binary_search(planets_in_order, "Vulcan"))
print(linear_search(planets, "Vulcan"))
```

The binary search gives 5185, an index in the sorted list. The other
two give 4914, an index in the list as the file gave it. Those are two
different lists, so two different indexes both point at Proxima Cen b.
For Vulcan, both of your tools give −1. `planets.index("Vulcan")` does
not: it stops with `ValueError: 'Vulcan' is not in list`. That is the
same search, with a different promise about a missing target. An error
is harder to miss than a −1, which is one reason Python chose it.

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
to 2023. It rises from 65.6 to 82.4. Schlomi, who is learning Python
too, has a quick idea: the numbers go up, so a binary search can find
the first year it reached 70. Can we trust a binary search on this
list, when the numbers only mostly go up?

<details class="dl-answer"><summary>answer</summary>

Not on this list. Schlomi's idea works on a list that is in order all the way
along, and this list is not: that page found fifteen years where life
expectancy fell. It
passed 70 in 1960, at 70.17, and fell back to 69.64 in 1961. A binary
search that looks at one year and sees 69.64 decides that every
earlier year is lower, which is false. Mostly sorted is not sorted. For
a list like this, a linear search from the front is the move that
keeps its promise.

</details>

**11. Fix.** A server keeps a sorted list of the network *ports* it
listens on: numbered doors for different kinds of traffic, such as 443
for secure web pages. Schlomo, who is learning Python too, wrote this
binary search. His idea: when `low` and `high` meet, only one port is
left, so the search can stop there. It finds some ports, but not 9000,
which is on the list. Run it. Which other ports does it miss? Change
the one line that makes it miss them.

```python exec
id: finding-fast-practice-fix-ports
def find_port(sorted_ports, target):
    """Return an index where target is in sorted_ports, or -1."""
    low = 0
    high = len(sorted_ports) - 1
    while low < high:
        middle = (low + high) // 2
        if sorted_ports[middle] == target:
            return middle
        if sorted_ports[middle] < target:
            low = middle + 1
        else:
            high = middle - 1
    return -1


ports = [22, 80, 443, 8080, 9000]
for port in ports:
    print(port, find_port(ports, port))
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Follow the search for 9000 on paper, with columns for `low`, `high`
   and `middle`.
2. What are `low` and `high` when the loop stops?
3. Was the port at that index ever looked at?

**Think about:** Schlomo has a point: one port is left when `low` and
`high` meet. Which step did his loop leave out for that last port?

</details>

<details class="dl-answer"><summary>answer</summary>

The loop runs `while low < high`. When `low` and `high` are equal, one
port is still left, as Schlomo said, but the loop stops without looking
at it. For 9000, `low` and `high` both reach 4, and the search gives
up. It misses 80 the same way, when `low` and `high` both reach 1. The
change is one character: `while low <= high`.

```python
def find_port(sorted_ports, target):
    """Return an index where target is in sorted_ports, or -1."""
    low = 0
    high = len(sorted_ports) - 1
    while low <= high:
        middle = (low + high) // 2
        if sorted_ports[middle] == target:
            return middle
        if sorted_ports[middle] < target:
            low = middle + 1
        else:
            high = middle - 1
    return -1


for port in ports:
    print(port, find_port(ports, port))
```

Now every port is found. A test that searches for every item, as the
tutorial's toolkit tests do, finds a line like this one.

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
`5_100_000` with underscores, so that a long number reads in groups of three.)

</details>

## Stretch

Use this cell for any of the stretch problems.

```python exec
id: finding-fast-practice-stretch
scores = [120, 250, 310, 480, 520, 700]
print(binary_search(scores, 480))

life = await load_csv("life-expectancy.csv")
countries = life[life.year == 2016]["country"].tolist()
print(len(countries), "names, in alphabetical order")
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
at index 2, and $6 - 1 - 2 = 3$. The move "throw away half" still
works. It needed a space where "after the middle" and "bigger" mean the same
thing, or a search that knows they mean the opposite.

</details>

**15. Make.** The cell at the top of this section also loads
`countries`: the 261 names from the life expectancy file of
[A row of numbers](tutorial:a-row-of-numbers#a-real-list-ireland-since-1950),
in alphabetical order, with some regions and groups such as "World"
among the countries. Over all 261 names, how many looks does each
search need on average? Write two small counting functions, or copy `linear_looks`
and `binary_looks` from the tutorial. Search for every name in turn,
keep the counts in two lists, and use `mean` from your toolkit.

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

The linear search needs 131 looks on average, and 261 at most. Each
name is searched for once, so on average the search goes about
halfway along. The binary search needs about 7.1 looks on
average, and 9 at most: most names are found on the last two or
three looks, because each halving has twice as many places to end as
the one before.

</details>
