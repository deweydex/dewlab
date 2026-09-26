---
title: "Lists and looping over them — Practice"
practice_for: lists-and-sequences
year: "2026-2027"
version: 2026.09.26.1
worlds:
  secret-messages: Codes and hidden messages, the kind spies and puzzle-setters make.
  pixel-art: Pictures made of small squares, the way a screen draws them.
---

# Lists and looping over them — Practice

Problems on lists, and three from earlier pages. With indexing and slicing,
trying things out teaches more than working them out in your head, so run
the cells, change them, and test your guesses. Try each problem before you
open anything under it.

## 1. Which element

```python exec
id: which-element-1
xs = [10, 20, 30, 40, 50]
print(xs[-2])
```

```predict
type: number

What will it print?
```

Then, with the same `xs`, what does each of these give? Try them in the
cell.

- (a) `xs[0]`
- (b) `xs[2]`
- (c) `xs[-1]`
- (d) `xs[5]`
- (e) `len(xs)`

<details class="dl-answer"><summary>answer</summary>

(a) 10. (b) 30. (c) 50. (d) An `IndexError`: `list index out of range`.
(e) 5.

A list of 5 elements has indexes 0 to 4, so the last one is always
`len(xs) - 1`. There is no index 5. Saying it out loud a few times helps,
until it stops being a surprise.

</details>

## 2. Slices

With `xs = [10, 20, 30, 40, 50]`, what does each slice give?

- (a) `xs[1:3]`
- (b) `xs[:2]`
- (c) `xs[3:]`
- (d) `xs[:]`
- (e) `xs[::2]`
- (f) `xs[::-1]`

```python exec
id: slices-1
xs = [10, 20, 30, 40, 50]
print(xs[1:3])
```

<details class="dl-answer"><summary>answer</summary>

(a) `[20, 30]`. (b) `[10, 20]`. (c) `[40, 50]`. (d) the whole list, as a
new list. (e) `[10, 30, 50]`. (f) `[50, 40, 30, 20, 10]`.

A third number in a slice is the *step*. `::2` takes every second element,
and `::-1` walks backwards through the whole list.

</details>

## 3. Past the end

```python exec
id: past-the-end-1
xs = [10, 20, 30, 40, 50]
print(xs[3:100])
```

```predict
What will it print?

- [40, 50]
  - A slice stops at the end of the list, however far its number goes.
- An error
  - There is no index 100, so the slice fails, like `xs[100]` would.
```

<details class="dl-answer"><summary>why</summary>

`[40, 50]`, with no error. A slice stops at the ends of the list, so it
never goes out of range. An index that is out of range fails. That is
useful, and it can also hide a mistake: a slice that asks for more than
there is gives less, and says nothing.

</details>

## 4. MOON from NOON

A string cannot be changed, but a new one can be built from pieces of it.
Can you set `new_word` to `"MOON"`, using `word`?

```python exec
id: moon-from-noon-1
word = "NOON"

print(new_word)
```

```inputs
new_word
```

```solution
word = "NOON"
new_word = "M" + word[1:]
print(new_word)
---
`word[1:]` is `"OON"`, everything from index 1 to the end. `word` itself
is still `"NOON"`.
```

## 5. Ten squares

Can you build `squares`, the first ten square numbers, with a loop?

```python exec
id: ten-squares-1
squares = []

print(squares)
```

```inputs
squares
```

```solution
squares = []
for n in range(1, 11):
    squares.append(n ** 2)
print(squares)
---
`[1, 4, 9, 16, 25, 36, 49, 64, 81, 100]`. `range(1, 11)` starts at 1, and
stops before 11.
```

## 6. Fibonacci

The Fibonacci sequence starts 1, 1. After that, each term is the sum of
the two before it: 1, 1, 2, 3, 5, 8, 13, and so on. Can you build `fibs`,
the first fifteen terms?

```python exec
id: fibonacci-1
fibs = [1, 1]

print(fibs)
```

```inputs
fibs
```

```hint
`fibs[-1]` is the last term so far, and `fibs[-2]` the one before it. How
many times does the loop need to add a term, if two are there already?
```

```solution
title: with what you've met so far
fibs = [1, 1]
for count in range(13):
    fibs.append(fibs[-1] + fibs[-2])
print(fibs)
```

```solution
title: another way
fibs = [1, 1]
while len(fibs) < 15:
    fibs.append(fibs[-1] + fibs[-2])
print(fibs)
---
The `while` loop says what it is waiting for: fifteen terms. Negative
indexes do the rest: "the last two" needs no sums with the length.
```

## 7. The golden ratio

Divide each Fibonacci number by the one before it: 1/1, 2/1, 3/2, 5/3, and
so on. What happens to the answers?

```python exec
id: the-golden-ratio-1
fibs = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610]
for index in range(1, len(fibs)):
    print(fibs[index] / fibs[index - 1])
```

<details class="dl-answer"><summary>answer</summary>

They close in on 1.6180339887…, the *golden ratio*, which is exactly
(1 + √5)/2. The answers go above it, then below it, then above again, and
each time they come closer. That is a limit, reached from a very different
direction than [Limits: getting closer without arriving](tutorial:approaching-a-limit)
takes.

The loop goes by index because each step needs two elements: this one, and
the one before it.

</details>

## 8. Backwards

Can you build `result`, the list `xs` backwards, without `reverse()` or
`[::-1]`?

```python exec
id: backwards-1
xs = [10, 20, 30, 40, 50]
result = []

print(result)
```

```inputs
result
```

```hint
The last index is `len(xs) - 1`, and the first is 0. Can a `range` count
down between them?
```

```solution
title: with what you've met so far
xs = [10, 20, 30, 40, 50]
result = []
for index in range(len(xs) - 1, -1, -1):
    result.append(xs[index])
print(result)
---
`range` counts down from the last index to 0. Its stop is -1 because a
range stops *before* its stop, so -1 is what lets it reach 0.
```

```solution
title: a shorter way you'll meet later
xs = [10, 20, 30, 40, 50]
result = xs[::-1]
print(result)
---
A slice with a step of -1 walks backwards through the whole list.
```

## 9. The longest word

Can you set `longest` to the longest word in the list?

```python exec
id: the-longest-word-1
words = ["OTTER", "OWL", "HEDGEHOG", "BAT"]

print(longest)
```

```inputs
longest
```

```solution
title: with what you've met so far
words = ["OTTER", "OWL", "HEDGEHOG", "BAT"]
longest = words[0]
for word in words:
    if len(word) > len(longest):
        longest = word
print(longest)
```

```solution
title: a shorter way you'll meet later
words = ["OTTER", "OWL", "HEDGEHOG", "BAT"]
longest = max(words, key=len)
print(longest)
---
`key=len` tells `max()` to compare the words by their length. It is much
easier to read once you have written the loop yourself.
```

## 10. Above the average

How many of these numbers are above their average? Can you set `above`?

```python exec
id: above-the-average-1
numbers = [4, 8, 15, 16, 23, 42]

print(above)
```

```inputs
above
```

```solution
numbers = [4, 8, 15, 16, 23, 42]
total = 0
for number in numbers:
    total = total + number
average = total / len(numbers)

above = 0
for number in numbers:
    if number > average:
        above = above + 1
print(above)
---
The average is 18, and two numbers are above it. It takes two passes
through the list: the first finds the average, and the second compares
each number with it. One pass cannot do it, because the average depends on
numbers the loop has not reached yet.
```

## 11. Most often

Can you set `most` to the number that appears most often in the list?

```python exec
id: most-often-1
numbers = [3, 7, 3, 9, 7, 3, 1]

print(most)
```

```inputs
most
```

```hint
`numbers.count(n)` says how many times `n` appears. Keep the best number
so far, and how many times it appears.
```

```solution
numbers = [3, 7, 3, 9, 7, 3, 1]
most = numbers[0]
for number in numbers:
    if numbers.count(number) > numbers.count(most):
        most = number
print(most)
---
3, three times. `numbers.count()` walks the whole list, inside a loop that
walks the whole list too, so the work grows with the square of the length.
For seven numbers, nobody notices. For a million, you would wait. If two
numbers tie, the first one found wins here: the problem did not say.
```

## 12. Once each

Can you build `once`, the list with its repeated values removed, keeping
the order they first appear in?

```python exec
id: once-each-1
numbers = [3, 7, 3, 9, 7, 3, 1]
once = []

print(once)
```

```inputs
once
```

```solution
numbers = [3, 7, 3, 9, 7, 3, 1]
once = []
for number in numbers:
    if number not in once:
        once.append(number)
print(once)
---
`[3, 7, 9, 1]`. `once` does two jobs: it is the answer, and it is the
record of what the loop has already seen. `number not in once` is `True`
when `number` is not in the list yet.
```

## 13. Next door

<div class="dl-world" data-world="secret-messages">

Doubled letters are a clue when breaking a code: in English, EE, LL, SS and
OO are common. Can you build `doubles`, the index of every letter that is
the same as the one after it?

```python exec
id: next-door-1--secret-messages
message = "MEET ME BY THE OLD TREE"
doubles = []

print(doubles)
```

```inputs
doubles
```

```hint
The loop needs each letter and the one after it, so loop by index. The
last letter has nothing after it: where should the range stop?
```

```solution
message = "MEET ME BY THE OLD TREE"
doubles = []
for index in range(len(message) - 1):
    if message[index] == message[index + 1]:
        doubles.append(index)
print(doubles)
---
`[1, 21]`, the EE in MEET and the EE in TREE. `range(len(message) - 1)`
stops one early, so `index + 1` never runs off the end.
```

</div>

<div class="dl-world" data-world="pixel-art">

An *edge* in a picture is where dark meets light. Can you build `edges`,
the index of every pixel below 128 whose right-hand neighbour is 128 or
more?

```python exec
id: next-door-1--pixel-art
row = [20, 30, 200, 210, 40, 250, 240, 10]
edges = []

print(edges)
```

```inputs
edges
```

```hint
The loop needs each pixel and the one after it, so loop by index. The last
pixel has nothing after it: where should the range stop?
```

```solution
row = [20, 30, 200, 210, 40, 250, 240, 10]
edges = []
for index in range(len(row) - 1):
    if row[index] < 128 and row[index + 1] >= 128:
        edges.append(index)
print(edges)
---
`[1, 4]`. `range(len(row) - 1)` stops one early, so `index + 1` never runs
off the end. Photo software finds edges this way, in every row and every
column.
```

</div>

## 14. From earlier: a condition that is always true

From *Making decisions with if, elif and else*. This is meant to say
whether a letter is a vowel. Why does it say `vowel` for every letter?

```python exec
id: from-earlier-always-true-1
letter = "T"
if letter == "A" or "E" or "I" or "O" or "U":
    print("vowel")
else:
    print("not a vowel")
```

<details class="dl-answer"><summary>answer</summary>

`or` joins whole conditions, and `"E"` on its own is not a comparison.
Python treats a non-empty string as true, so the whole condition is always
`True`. Each part needs its own comparison:
`letter == "A" or letter == "E" or ...`. Or, shorter, `letter in "AEIOU"`.

</details>

## 15. From earlier: how many times round

From *Repeating steps with loops*.

```python exec
id: from-earlier-how-many-times-1
count = 0
for number in range(2, 20, 3):
    count = count + 1
print(count)
```

```predict
type: number

What will it print?
```

<details class="dl-answer"><summary>why</summary>

6: the range gives 2, 5, 8, 11, 14 and 17. The next would be 20, and a
range stops before its stop.

</details>

## 16. From earlier: print or return

From *Writing your own functions*.

```python exec
id: from-earlier-print-or-return-1
def double(n):
    print(n * 2)

result = double(4)
print(result)
```

```predict
What will the last line print?

- 8
  - `result` holds what `double` worked out.
- None
  - `double` prints its answer, and gives nothing back.
- An error
  - A function with no `return` cannot be used after an `=`.
```

<details class="dl-answer"><summary>why</summary>

`8`, then `None`. `double` prints 8, and then ends without a `return`, so
it gives back `None`, and that is what `result` holds. With
`return n * 2` in place of the `print`, it would print 8 once.

</details>
