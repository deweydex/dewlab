---
title: "Dictionaries: looking things up by name"
year: "2026-2027"
version: 2026.09.22.1
covers:
  making-a-dictionary:
    touches: [PDP-LO4]
---

# Dictionaries: looking things up by name

In [Lists: keeping many values in order](tutorial:lists-and-sequences) we kept many
values together in a list, and found each one by its position. Position
works well when order matters: the first score, or the last temperature
of the week.

Often, though, we know a name, and we want the value that goes with it.
What is Ben's mark? How much is a coffee? What is the dentist's phone
number? With a list, we would have to go through it, item by item, until
we found Ben. Python has a better tool for this.

On this page we:

- keep values under names, in a dictionary, and look them up
- add values, change them, and check whether they are there
- loop over a dictionary
- count things, such as how often each word appears in a sentence
- decide when a dictionary is the right choice, and when a list is

## Making a Dictionary

Here is a small café menu. What do you think the second `print` line
shows? Run the cell to check.

```python exec
id: making-a-dictionary-1
prices = {"tea": 2.5, "coffee": 3.2, "scone": 2.8}
print(prices)
print(prices["coffee"])
print(len(prices))
```

A *dictionary* is a collection of pairs. Each pair joins a key to a
value. A *key* is the name we look something up by. A *value* is what is
stored under that key. In `prices`, the key `"coffee"` has the value
`3.2`.

We write a dictionary like this:

- curly brackets, `{` and `}`, go around the whole dictionary
- a colon, `:`, joins each key to its value
- commas go between the pairs

To look up a value, we write the dictionary's name, then the key in
square brackets: `prices["coffee"]`. The square brackets are the same as
for a list index. Inside them, we write a key, where a list would have a
position.

`len()` works on a dictionary too. It gives the number of pairs, so
`len(prices)` is 3. Python shows the strings with single quotes when it
prints a dictionary. Single and double quotes mean the same thing.

The name comes from a paper dictionary. There, you look up a word, and
you find its meaning beside it. The word is the key, and the meaning is
the value.

Here the keys are strings and the values are floats. A value can be any
type: a number, a string, a bool, or even a list. Each key appears only
once in a dictionary. Two keys can have the same value, though: tea and
a scone could both cost 2.5.

### Your turn

1. Make a dictionary called `capitals`. Use at least four countries as
   keys, with each country's capital city as its value.
2. Print the capital of one of the countries.
3. Print how many pairs your dictionary holds.

```python exec
id: making-a-dictionary-your-turn-1
# Your capitals dictionary here
```

## Adding and Changing Values

A dictionary is mutable, like a list: we can change it after we make it.

The cell below makes the menu again. The next two lines have the same
shape. One of them adds a new pair, and the other changes a pair that is
already there. Which is which? How many pairs will the menu have at the
end? Run it to check.

```python exec
id: adding-and-changing-values-1
prices = {"tea": 2.5, "coffee": 3.2, "scone": 2.8}
prices["muffin"] = 3.0
prices["tea"] = 2.7
print(prices)
print(len(prices))
```

`"muffin"` was not a key yet, so Python added a new pair. `"tea"` was
already a key, so Python replaced its value. The line looks the same
both times. What decides it is whether the key is already there.

Did you notice where the muffin went? A dictionary keeps its pairs in
the order they were added, so a new pair goes at the end.

This is one way a dictionary differs from a list. A list grows with
`append()`, and `scores[10] = 50` on a short list is an error. A
dictionary grows when we give a value to a new key.

We can also use a value to work out its own new value. The price of
coffee goes up by 30 cent. What do you think this prints?

```python exec
id: adding-and-changing-values-2
prices["coffee"] = prices["coffee"] + 0.3
print(prices["coffee"])
```

Python works out the right-hand side first. It reads the old price,
3.2, and adds 0.3. Then it stores the result, 3.5, back under
`"coffee"`. This is the same shape as `total = total + n` in the
accumulator pattern from
[Repeating steps with loops](tutorial:repeating-yourself). We use it again later
on this page, to count things.

### Your turn

A shop keeps its stock in a dictionary.

1. The shop gets 20 plums. Add `"plums"` to `stock`, with the value 20.
2. Someone buys 3 apples. Take 3 away from the value for `"apples"`,
   using its old value.
3. Print `stock`. What should it show, before you run it?

```python exec
id: adding-and-changing-values-your-turn-1
stock = {"apples": 12, "pears": 5}
# Your changes here
```

## Checking Whether a Key Is There

What happens if we ask for a key that is not in the dictionary? This
cell is meant to fail. Run it, and read the last line of the error.

```python exec
id: checking-whether-a-key-is-there-1
prices = {"tea": 2.5, "coffee": 3.2, "scone": 2.8}
print(prices["cake"])
```

Sometimes we might notice this error in a program that worked well
yesterday. A `KeyError` means that Python looked for a key and did not
find it. The last line of the error names the missing key: here it is
`'cake'`. Often the key is there, but spelled another way. `"Tea"` and
`"tea"` are two different keys. We look at errors like this one, in
bigger programs, in [Finding bugs in bigger programs](tutorial:when-it-goes-wrong).

We can ask before we look. The `in` operator checks whether a key is in
a dictionary. It gives `True` or `False`.

What do you think each line prints? The last one is the tricky one.

```python exec
id: checking-whether-a-key-is-there-2
print("tea" in prices)
print("cake" in prices)
print(2.5 in prices)
```

The last line prints `False`, even though 2.5 is the price of tea. `in`
checks the keys of a dictionary. It does not look at the values.

Together with `if`, `in` lets a program decide what to do before it
looks anything up:

```python exec
id: checking-whether-a-key-is-there-3
item = "cake"
if item in prices:
    print(item, "costs", prices[item])
else:
    print("Sorry, we have no", item)
```

### Your turn

Can you write a small price checker for the café?

1. Make a variable called `order`, holding the name of one item.
2. If the item is on the menu, print its price. If it is not, print a
   message that says so.
3. Run it twice: once with an item on the menu, and once with an item
   that is not.

```python exec
id: checking-whether-a-key-is-there-your-turn-1
prices = {"tea": 2.5, "coffee": 3.2, "scone": 2.8}
# Your price checker here
```

## Looping Over a Dictionary

A `for` loop can go through a dictionary. What do you think the loop
gives us each time: a key, a value, or both? Run it to check.

```python exec
id: looping-over-a-dictionary-1
marks = {"Aoife": 72, "Ben": 65, "Cara": 88}
for name in marks:
    print(name)
```

A loop over a dictionary goes through its keys. Once we have a key, we
can look up its value:

```python exec
id: looping-over-a-dictionary-2
for name in marks:
    print(name, "got", marks[name])
```

There is a neater way. `.items()` gives us each pair, as a key and a
value together. We write two names after `for`: the first gets the key,
and the second gets the value. Does this remind you of `enumerate()` in
[Lists: keeping many values in order](tutorial:lists-and-sequences)? It works the same
way.

```python exec
id: looping-over-a-dictionary-3
for name, mark in marks.items():
    print(name, "got", mark)
```

### Your turn

1. Loop over `marks`, and add up all the marks with the accumulator
   pattern.
2. Print the average mark.
3. Print the name of each student whose mark is above 70.

```python exec
id: looping-over-a-dictionary-your-turn-1
marks = {"Aoife": 72, "Ben": 65, "Cara": 88}
# Your loop here
```

## Looking Up with a Default

Checking with `in` before every lookup takes four lines. `.get()` does
the same job in one. What do you think each line prints?

```python exec
id: looking-up-with-a-default-1
prices = {"tea": 2.5, "coffee": 3.2, "scone": 2.8}
print(prices.get("tea", 0))
print(prices.get("cake", 0))
print(prices.get("cake"))
```

`prices.get(key, default)` gives back the key's value if the key is
there. If it is not, `.get()` gives back the *default*. A default is the
value we choose to get when nothing else is there, and here we chose 0.
With no default, `.get()` gives back `None`, which is Python's value for
"nothing". `.get()` never raises a `KeyError`.

So which should you use? It depends on what a missing key means.

- If a missing key is a mistake, use `prices["cake"]`. The `KeyError`
  tells you about the mistake straight away.
- If a missing key is normal, use `.get()` with a default that makes
  sense.

### Your turn

1. Use `.get()` to look up `"Doctor"` in `phone_book`. Use the default
   `"not in the phone book"`.
2. Look up `"Vet"` in the same way. What do you expect it to print?

```python exec
id: looking-up-with-a-default-your-turn-1
phone_book = {"Dentist": "01 555 0101", "Doctor": "01 555 0199"}
# Your lookups here
```

## Counting Things

How many times does each word appear in a sentence? First, we need the
words. The string method `.split()` breaks a string into a list of
words. It cuts the string wherever there is a space.

```python exec
id: counting-things-1
sentence = "the cat sat on the mat and the dog sat on the cat"
words = sentence.split()
print(words)
```

In [Repeating steps with loops](tutorial:repeating-yourself) we counted with one
variable, and added 1 to it each time. Here we need one count for every
different word. But we do not know the words before we start. A
dictionary solves this. Each word is a key, and its count is the value.

Here is the plan in pseudocode:

```
START with an empty dictionary
FOR each word in the list
    IF the word is already a key: ADD 1 to its count
    OTHERWISE: store the word with a count of 1
DISPLAY the dictionary
```

`{}` is an empty dictionary, in the same way that `[]` is an empty list.
Before you run the cell, can you count the word "the" by hand?

```python exec
id: counting-things-2
counts = {}
for word in words:
    if word in counts:
        counts[word] = counts[word] + 1
    else:
        counts[word] = 1
print(counts)
```

This is the accumulator pattern again, with one accumulator for each
key.

`.get()` makes the loop shorter. Why do you think the default is 0 here?

```python exec
id: counting-things-3
counts = {}
for word in words:
    counts[word] = counts.get(word, 0) + 1
print(counts)
```

The first time a word appears, it has no count yet. `.get()` gives back
0, and 0 + 1 stores a count of 1. After that, `.get()` gives back the
count so far. Both versions give the same dictionary, so you can use
whichever one you find easier to read.

### Your turn

A `for` loop can go through a string one character at a time, in the
same way it goes through a list. `for letter in "banana":` gives `"b"`,
then `"a"`, then `"n"`, and so on.

1. Write a function `count_letters(word)`. It returns a dictionary with
   each letter of `word` as a key, and the number of times that letter
   appears as the value. You can plan it in pseudocode first, in
   comments at the top of the cell.
2. In the second cell, test it with `"banana"`. You should get
   `{'b': 1, 'a': 3, 'n': 2}`.
3. How many times does `"s"` appear in `"mississippi"`? Use your
   function to find out.

```python exec
id: counting-things-your-turn-1
# Pseudocode:
#

# Your count_letters function
```

```hint
Look at the loop in the cell with `.get()` above. What is it looping
over, and what would you loop over in `count_letters`? What does your
function give back at the end?
```

```python exec
id: counting-things-your-turn-2
# Test it
```

## Dictionary or List?

Lists and dictionaries both keep many values together. How do we choose
between them? This table puts the two side by side.

| | List | Dictionary |
|---|---|---|
| We find a value by | its position: `scores[0]` | its key: `marks["Ben"]` |
| We write it with | square brackets, `[ ]` | curly brackets, `{ }` |
| It is a good choice when | order matters, or the values have no names | each value has a name we look it up by |
| An example | a week of temperatures | students and their marks |
| A missing item gives | `IndexError` | `KeyError` |

One question decides most cases. Will you look values up by a name? If
so, use a dictionary. If you care about the order, or you only go
through all the values one by one, use a list.

We can also use both together. A dictionary's value can be a list. Here
each student has a list of marks. The f-string from
[Variables, data types and text](tutorial:storing-and-computing) rounds each
average to two decimal places.

```python exec
id: dictionary-or-list-1
results = {"Aoife": [72, 80, 91], "Ben": [65, 70, 58]}
for name, mark_list in results.items():
    average = sum(mark_list) / len(mark_list)
    print(f"{name}: average {average:.2f}")
```

### Your turn

For each of these, would you use a list or a dictionary? Write your
answer and your reason as a comment in the cell.

1. The ten songs in a playlist, in the order they play.
2. The number of goals each player on a team has scored.
3. The rainfall on each day of March.
4. A phrasebook that gives the English word for each Irish word.
5. The names of the people waiting in a queue.

```python exec
id: dictionary-or-list-your-turn-1
# 1.
# 2.
# 3.
# 4.
# 5.
```

<details class="dl-answer"><summary>answer</summary>

1. A list. The order the songs play in is the point.
2. A dictionary. Each player's name is the key, and their goals are the
   value.
3. A list. The position is the day: index 0 is the 1st of March.
4. A dictionary. You look up an Irish word, and you find the English
   word under it.
5. A list. A queue is all about order: who is first, and who is next.

Some of these could go either way. You could keep the rainfall in a
dictionary, with the date as the key. If your reason makes sense, your
answer is a good one.

</details>

## Reflection

On this page we met dictionaries. We made them with keys and values,
looked values up by key, added new pairs and changed old ones. We
checked for a key with `in`, and looked up safely with `.get()`. We
looped over keys and over `.items()`. Then we counted words, with one
accumulator for each key.

A list answers the question "what is at position 3?". A dictionary
answers "what goes with this name?". Many real programs need both.

Think of a program you use every day: a phone's contacts, a shopping
app, or a timetable. Where do you think it keeps values under names?

## Where to Read More

Python Software Foundation. *The Python Tutorial — Data Structures:
Dictionaries.* <https://docs.python.org/3/tutorial/datastructures.html#dictionaries>.
The official reference for dictionaries, including the methods this page
does not cover.
