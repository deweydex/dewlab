---
title: "Dictionaries: looking things up by name — Practice"
practice_for: looking-things-up-by-name
year: "2026-2027"
version: 2026.09.22.1
---

# Dictionaries: looking things up by name — Practice

On this page we practise dictionaries: making them, changing them,
looping over them, and counting with them. Each answer is folded away
under its problem. Try the problem first, then open the answer.

Many of the questions ask you to predict. Write your guess down before
you run anything. A wrong guess you can explain teaches more than a
right guess you cannot.

## Making and Changing a Dictionary

The cell below is a scratchpad for this section.

```python exec
id: making-and-changing-a-dictionary-1
ages = {"Aoife": 34, "Ben": 29, "Cara": 41}
print(ages)
print(ages["Ben"], len(ages))
```

**1.** Here `ages = {"Aoife": 34, "Ben": 29, "Cara": 41}`. What does each
of these give?

- (a) `ages["Ben"]`
- (b) `len(ages)`
- (c) `"Cara" in ages`
- (d) `41 in ages`
- (e) `ages["ben"]`

<details class="dl-answer"><summary>answer</summary>

(a) 29. (b) 3. (c) `True`. (d) `False`. (e) a `KeyError`.

(d) is `False` because `in` checks the keys, and 41 is a value.

(e) fails because capital letters matter. `"ben"` and `"Ben"` are two
different keys, and only `"Ben"` is in the dictionary.

</details>

**2.** What does this print? Why?

```python
ages = {"Aoife": 34, "Ben": 29, "Aoife": 35}
print(ages)
```

<details class="dl-answer"><summary>answer</summary>

`{'Aoife': 35, 'Ben': 29}`.

A key appears only once in a dictionary. When the same key is written
twice, the second value replaces the first, in the same way as
`ages["Aoife"] = 35` would. So there is no error, and one of the values
is lost without a warning. Watch for this when you type a long
dictionary by hand.

</details>

**3.** What does `ages[0]` give? Why is it not the first pair?

<details class="dl-answer"><summary>answer</summary>

A `KeyError`, with the key `0`.

A dictionary has no positions. Inside the square brackets, Python reads
`0` as a key, and there is no key `0` in `ages`. To get at the pairs in
order, loop over the dictionary.

</details>

**4.** After these lines run, what is `stock`?

```python
stock = {"apples": 12, "pears": 5}
stock["plums"] = 20
stock["apples"] = stock["apples"] - 3
stock["pears"] = 0
```

<details class="dl-answer"><summary>answer</summary>

`{'apples': 9, 'pears': 0, 'plums': 20}`.

- `"plums"` was a new key, so its line added a pair at the end.
- The `"apples"` line read the old value, 12, took away 3, and stored 9.
- The `"pears"` line changed the value to 0. The key is still there. A
  count of 0 pears and no `"pears"` key at all are two different things.

</details>

## Looping Over a Dictionary

This cell loops over `marks` in the two ways from the tutorial.

```python exec
id: looping-over-a-dictionary-practice-1
marks = {"Aoife": 72, "Ben": 65, "Cara": 88, "Dara": 59}
for name in marks:
    print(name, marks[name])
for name, mark in marks.items():
    print(name, mark)
```

**5.** Using `marks` from the cell above, print the total of the marks
and the average mark.

<details class="dl-answer"><summary>answer</summary>

```python
total = 0
for name, mark in marks.items():
    total = total + mark
average = total / len(marks)
print(total, average)
```

The total is 284, and the average is 71.0.

The loop does not use `name`. You could loop over the keys instead, and
add `marks[name]` each time. Both give the same total.

</details>

**6.** Which student has the highest mark? Print their name and their
mark.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Make two variables before the loop: one for the best name so far, and
   one for the best mark so far.
2. Loop over `marks.items()`.
3. When a mark is higher than the best mark so far, update both
   variables.

**Think about:** what should the best mark start as, so that the first
student is sure to beat it?

**Try this next:** can you find the student with the lowest mark?

</details>

<details class="dl-answer"><summary>answer</summary>

```python
best_name = ""
best_mark = -1
for name, mark in marks.items():
    if mark > best_mark:
        best_name = name
        best_mark = mark
print(best_name, best_mark)
```

Cara, with 88.

`best_mark` starts at -1, so any real mark beats it. Starting at 0 also
works here, because no mark is below 0. If two students tie, this loop
keeps the first one it finds, because `>` is not true for an equal mark.

</details>

**7.** Here is a dictionary of countries and their capitals. Can you
build a new dictionary that goes the other way, from capital to
country?

```python
capitals = {"Ireland": "Dublin", "France": "Paris", "Peru": "Lima"}
```

<details class="dl-answer"><summary>answer</summary>

```python
countries = {}
for country, city in capitals.items():
    countries[city] = country
print(countries)
```

`{'Dublin': 'Ireland', 'Paris': 'France', 'Lima': 'Peru'}`.

This works because every capital here is different. If two keys had the
same value, they would both try to become the same key in the new
dictionary, and the second would replace the first. Turning a
dictionary around only works when its values are all different.

</details>

## Looking Up and Counting

This cell shows `.get()` with and without a default, and counts the
letters in a short word.

```python exec
id: looking-up-and-counting-1
prices = {"tea": 2.5, "coffee": 3.2}
print(prices.get("tea", 0), prices.get("cake", 0), prices.get("cake"))

counts = {}
for letter in "banana":
    counts[letter] = counts.get(letter, 0) + 1
print(counts)
```

**8.** Here `prices = {"tea": 2.5, "coffee": 3.2}`. Predict each result,
then check.

- (a) `prices.get("coffee", 0)`
- (b) `prices.get("juice", 0)`
- (c) `prices.get("juice", "not sold here")`
- (d) `prices.get("juice")`
- (e) `prices["juice"]`

<details class="dl-answer"><summary>answer</summary>

(a) 3.2. (b) 0. (c) `not sold here`. (d) `None`. (e) a `KeyError`.

The default can be any value you like: a number, a string, or anything
else. Only the square brackets raise an error for a missing key.

</details>

**9.** A class voted for the end-of-term trip. Count the votes for each
place, then print the place with the most votes.

```python
votes = ["zoo", "cinema", "zoo", "beach", "cinema", "zoo", "beach", "zoo"]
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Start with an empty dictionary.
2. Loop over `votes`. For each vote, add 1 to that place's count, using
   `.get()` with a default of 0.
3. Then loop over the dictionary's items, and keep the place with the
   highest count so far, as in problem 6.

**Think about:** why do we need two loops, one after the other?

**Try this next:** count the votes for each place, and print how many
people voted in total.

</details>

<details class="dl-answer"><summary>answer</summary>

```python
counts = {}
for place in votes:
    counts[place] = counts.get(place, 0) + 1
print(counts)

winner = ""
most = 0
for place, count in counts.items():
    if count > most:
        winner = place
        most = count
print(winner, most)
```

`{'zoo': 4, 'cinema': 2, 'beach': 2}`, and the zoo wins with 4 votes.

We need two loops. The first loop builds the counts. The second loop
can only find the biggest count once every vote has been counted.

</details>

**10.** Count the letters in the sentence `"we meet at noon"`, but leave
out the spaces. Which letters appear more than once?

<details class="dl-answer"><summary>answer</summary>

```python
counts = {}
for letter in "we meet at noon":
    if letter != " ":
        counts[letter] = counts.get(letter, 0) + 1
print(counts)

for letter, count in counts.items():
    if count > 1:
        print(letter, count)
```

The counts are `{'w': 1, 'e': 3, 'm': 1, 't': 2, 'a': 1, 'n': 2, 'o': 2}`.
The letters that appear more than once are e (3 times), t, n and o
(2 times each).

The `if` skips the spaces. Without it, the space would be counted as a
character too, 3 times.

</details>

**11.** Sort these words into groups by their first letter. Make a
dictionary where each key is a letter, and each value is a list of the
words that start with that letter.

```python
words = ["apple", "banana", "avocado", "cherry", "blueberry", "apricot"]
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. `word[0]` gives the first letter of a word.
2. Start with an empty dictionary, and loop over `words`.
3. If the first letter is not a key yet, store an empty list under it.
4. Then append the word to the list stored under its first letter.

**Think about:** what should happen the first time a letter turns up,
and what should happen every time after that?

**Try this next:** group the same words by their length.

</details>

<details class="dl-answer"><summary>answer</summary>

```python
groups = {}
for word in words:
    first = word[0]
    if first not in groups:
        groups[first] = []
    groups[first].append(word)
print(groups)
```

`{'a': ['apple', 'avocado', 'apricot'], 'b': ['banana', 'blueberry'], 'c': ['cherry']}`.

This is the counting pattern again. Where counting starts each new key
at 0 and adds 1, grouping starts each new key at an empty list and
appends a word. `not in` is the opposite of `in`: it is `True` when the
key is missing.

</details>

## Dictionary or List?

**12.** For each of these, would you use a list or a dictionary? Give a
reason.

- (a) The price of each item on a café menu.
- (b) The finishing order of the runners in a race.
- (c) The number of pages in each chapter of a book, chapter 1 to 20.
- (d) Each student's email address.

<details class="dl-answer"><summary>answer</summary>

(a) A dictionary. You look up a price by the item's name.

(b) A list. The order is the whole point: index 0 is the winner.

(c) A list works well. The chapter number gives the position, if you
remember that chapter 1 is at index 0. A dictionary with chapter
numbers as keys also works, and it avoids that off-by-one.

(d) A dictionary, with the student's name as the key. Names can repeat
in a real class, though. A student number would make a safer key.

</details>

**13.** A program keeps names and marks in two lists, in matching order.
Turn them into one dictionary.

```python
names = ["Aoife", "Ben", "Cara"]
scores = [72, 65, 88]
```

<details class="dl-answer"><summary>answer</summary>

```python
marks = {}
for i in range(len(names)):
    marks[names[i]] = scores[i]
print(marks)
```

`{'Aoife': 72, 'Ben': 65, 'Cara': 88}`.

Two lists in matching order are easy to break. Sort one list, or delete
from one and not the other, and every name gets the wrong mark. In a
dictionary each mark is joined to its name, so this cannot happen.

</details>
