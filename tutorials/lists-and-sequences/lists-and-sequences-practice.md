---
title: "Lists: keeping many values in order — Practice"
practice_for: lists-and-sequences
year: "2026-2027"
version: 2026.09.22.1
---

# Lists: keeping many values in order — Practice

The answers are hidden in folds under each problem. With indexing and
slicing, trying things out teaches more than working them out in your
head. So run the tools cell, change it, and test your guesses before you
answer from memory.

## Indexing and Slicing

```python exec
id: indexing-and-slicing-1
xs = [10, 20, 30, 40, 50]
print(xs[0], xs[4], xs[-1], xs[-2])
print(xs[1:4], xs[:3], xs[2:], xs[::-1])
```

**1.** Here `xs = [10, 20, 30, 40, 50]`. What does each of these give?

- (a) `xs[0]`
- (b) `xs[2]`
- (c) `xs[-1]`
- (d) `xs[5]`
- (e) `len(xs)`

<details class="dl-answer"><summary>answer</summary>

(a) 10. (b) 30. (c) 50. (d) an `IndexError`. (e) 5.

The last valid index is always `len(xs) - 1`. A list of 5 elements has
no index 5. This "off by one" trips up most people, so it is worth
saying out loud a few times, until it stops being a surprise.

</details>

**2.** What does each slice give?

- (a) `xs[1:3]`
- (b) `xs[:2]`
- (c) `xs[3:]`
- (d) `xs[:]`
- (e) `xs[::2]`
- (f) `xs[::-1]`

<details class="dl-answer"><summary>answer</summary>

(a) `[20, 30]`. (b) `[10, 20]`. (c) `[40, 50]`. (d) the whole list. (e) `[10, 30, 50]`. (f) `[50, 40, 30, 20, 10]`.

A slice leaves out its end index, in the same way as `range`. A third
number in a slice is the step: `::2` takes every second element, and
`::-1` walks backwards.

`xs[:]` makes a copy of the list. That is useful, and it matters in the
next question.

</details>

**3.** What does this print? Why?

```python
a = [1, 2, 3]
b = a
b.append(4)
print(a)
```

<details class="dl-answer"><summary>answer</summary>

`[1, 2, 3, 4]`.

The line `b = a` does not copy the list. After it, both names refer to
the same list. So a change made through one name shows up through the
other name too. To make a real copy, write `b = a[:]` or `b = list(a)`.

This is the most common cause of confusing behaviour in a first year of
Python. It happens because a list can be changed in place, and numbers
and strings cannot.

</details>

**4.** What does this print? Compare it with the last question.

```python
def add_item(items):
    items.append("new")


things = ["a", "b"]
add_item(things)
print(things)
```

<details class="dl-answer"><summary>answer</summary>

`['a', 'b', 'new']`.

In [Writing your own functions](tutorial:writing-your-own-functions) we
saw that giving a name a new value inside a function never changes a
variable outside it. This looks like it goes against that, but it does
not. The function did not *assign* anything to `items`. It changed the
list that `items` refers to, and that is the same list that `things`
refers to. It is the same thing that happened with `b = a` above.

So there are two different actions. Giving a name a new value, with
`=`, stays local to the function. Changing a list in place, with
something like `append`, is seen everywhere that list is used.

A function that changes its arguments without saying so often surprises
people. So decide on purpose whether a function returns a new list or
changes the list it was given, and make its name say which.

</details>

**5.** After `xs[1] = 99`, what is `xs`? What happens if you try the same thing with a string?

<details class="dl-answer"><summary>answer</summary>

`[10, 99, 30, 40, 50]`.

With a string `s`, the line `s[1] = "x"` raises a `TypeError`. Strings
are *immutable*: an immutable value is one that cannot be changed after
it is made. To change a string, we build a new one, with slicing or with
`replace`.

Lists are mutable. That difference is why a list can change without you
noticing, through another name, and a string cannot.

</details>

## Building Lists

**6.** Can you build a list of the first ten square numbers in two different ways?

<details class="dl-answer"><summary>answer</summary>

```python
squares = []
for n in range(1, 11):
    squares.append(n ** 2)
```

or

```python
squares = [n ** 2 for n in range(1, 11)]
```

Both give `[1, 4, 9, 16, 25, 36, 49, 64, 81, 100]`.

The second way is a list comprehension, from "Comprehensions: A Loop
That Builds a List" on the tutorial page. It does the same work as the
first way, on one line.

</details>

**7.** Given a list called `numbers` that holds a mix of numbers, build a list of only the even ones.

<details class="dl-answer"><summary>answer</summary>

```python
evens = [n for n in numbers if n % 2 == 0]
```

An `if` at the end of a comprehension is a filter. It keeps only the
values that pass the test.

Building a new list is nearly always better than removing values from
the old one. If you delete from a list while you loop over it, the loop
skips some items. That looks like a bug in Python, but it is not: the
positions shift under the loop as you delete.

</details>

**8.** Here `words = ["apple", "fig", "banana", "kiwi"]`. Can you build a list of the lengths of the words, and then find the longest word?

<details class="dl-answer"><summary>answer</summary>

```python
lengths = [len(w) for w in words]     # [5, 3, 6, 4]

longest = words[0]
for w in words:
    if len(w) > len(longest):
        longest = w
```

The longest word is `banana`.

Python can also do this in one line: `max(words, key=len)`. It is much
easier to read that line after you have written the loop yourself once.

</details>

**9.** Can you reverse a list without using `reverse()` or `[::-1]`?

<details class="dl-answer"><summary>answer</summary>

```python
result = []
for item in xs:
    result.insert(0, item)
```

`insert(0, item)` puts each item at the front of the list.

Another way is to walk through the indexes backwards:

```python
result = [xs[i] for i in range(len(xs) - 1, -1, -1)]
```

Here `range` counts down, from the last index to 0. The stop value is
`-1` because the stop is left out, so a stop of `-1` is what lets it
reach index 0. When a range counts down, leaving out the stop becomes
harder to think about.

</details>

## Comprehensions

```python exec
id: comprehensions-1
names = ["Ada", "Grace", "Alan", "Margaret", "Tim"]
words = ["apple", "fig", "banana", "kiwi"]
print([len(word) for word in words])
print(sum(len(word) for word in words))
```

**10.** Predict what each of these gives. Then check them in the cell
above.

- (a) `[n * 2 for n in range(4)]`
- (b) `[n for n in range(10) if n % 3 == 0]`
- (c) `[word[0] for word in words]`
- (d) `sum(n for n in range(5))`
- (e) `"".join(str(n) for n in range(5))`
- (f) `[[0] * 2 for _ in range(3)]`

<details class="dl-answer"><summary>answer</summary>

(a) `[0, 2, 4, 6]`. (b) `[0, 3, 6, 9]`. (c) `['a', 'f', 'b', 'k']`.
(d) `10`. (e) `'01234'`. (f) `[[0, 0], [0, 0], [0, 0]]`.

In (b), the filter keeps only the numbers with no remainder after
dividing by 3. 0 is one of them, because 0 divided by 3 is 0 with
nothing left over.

(d) adds 0 + 1 + 2 + 3 + 4. (e) looks like a number, but it is a
string: `join()` always gives back a string.

(f) is a grid with 3 rows and 2 columns. The number in `range()` says
how many rows. The number after `*` says how long each row is.

</details>

**11.** Write this loop as a list comprehension. Then write the
comprehension `[len(name) * 10 for name in names]` as a loop.

```python
short_names = []
for name in names:
    if len(name) <= 4:
        short_names.append(name)
```

<details class="dl-answer"><summary>answer</summary>

```python
short_names = [name for name in names if len(name) <= 4]
```

Both give `['Ada', 'Alan', 'Tim']`.

And the other way round:

```python
tens = []
for name in names:
    tens.append(len(name) * 10)
```

Both give `[30, 50, 40, 80, 30]`.

The value that was appended goes at the front of the comprehension. The
`for` line comes next, without its colon. The `if` line goes at the end.
Going from a comprehension back to a loop is a good way to check that
you have read one correctly.

</details>

**12.** What does this print? Why?

```python
rows = [[0] * 3] * 2
rows[1][0] = 7
print(rows)
```

<details class="dl-answer"><summary>answer</summary>

`[[7, 0, 0], [7, 0, 0]]`.

We changed only the row at index 1, but both rows show the 7. That is
because `* 2` did not make two rows. It put the same row into the outer
list twice. It is problem 3 again: two names for one list.

A comprehension runs `[0] * 3` once for each row, so each row is a new
list:

```python
rows = [[0] * 3 for _ in range(2)]
rows[1][0] = 7
print(rows)    # [[0, 0, 0], [7, 0, 0]]
```

</details>

**13.** Build a 4 × 4 times table as a grid, with a comprehension. Row 1
should be `[1, 2, 3, 4]`, and row 4 should be `[4, 8, 12, 16]`.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Forget the grid for a moment. How would you write one row, the row
   for 3, as a comprehension?
2. That row is `[3 * column for column in range(1, 5)]`. Which part of
   it changes from row to row?
3. Put a second comprehension around the first one, with a loop over
   that part.

**Think about:** which loop makes the rows, and which loop makes the
values inside one row?

**Try this next:** an addition table, where each value is the row
number plus the column number.

</details>

<details class="dl-answer"><summary>answer</summary>

```python
times_table = [[row * column for column in range(1, 5)] for row in range(1, 5)]
for row in times_table:
    print(row)
```

```
[1, 2, 3, 4]
[2, 4, 6, 8]
[3, 6, 9, 12]
[4, 8, 12, 16]
```

The inner comprehension makes one row. The outer one makes one of those
rows for each `row` from 1 to 4.

Printing the grid one row at a time, with a loop, shows it as a square.
`print(times_table)` would put the whole grid on one long line.

</details>

**14.** With `words = ["apple", "fig", "banana", "kiwi"]`, use a
generator expression for each of these.

- (a) Count how many words have more than 3 letters.
- (b) Join the first letter of each word into one string.
- (c) Find how many letters there are in all the words together.

<details class="dl-answer"><summary>answer</summary>

```python
sum(1 for word in words if len(word) > 3)     # 3
"".join(word[0] for word in words)            # 'afbk'
sum(len(word) for word in words)              # 18
```

(a) adds 1 for each word that passes the test: apple, banana and kiwi.
Only fig has 3 letters or fewer.

(b) `word[0]` is the first letter of each word. `""` puts nothing
between the letters.

(c) adds 5 + 3 + 6 + 4.

None of these builds a list. A generator expression hands each value
straight to `sum()` or `join()`. Writing `sum([len(word) for word in
words])`, with square brackets, gives the same answer. The only
difference is that it builds a list first, and then adds it up.

</details>

## Working Through a List

**15.** Can you add up a list without `sum()`? Then find its mean.

<details class="dl-answer"><summary>answer</summary>

```python
total = 0
for n in numbers:
    total = total + n
mean = total / len(numbers)
```

If the list is empty, the last line divides by zero. What should the
mean of nothing be? That is a real question with no clear answer. This
is why most libraries raise an error, and do not choose an answer.

</details>

**16.** How could you count the numbers in a list that are above the mean?

<details class="dl-answer"><summary>answer</summary>

```python
mean = sum(numbers) / len(numbers)
above = sum(1 for n in numbers if n > mean)
```

The second line counts: it adds 1 for each number that is above the
mean.

We need to go through the list twice. The first pass finds the mean. The
second pass compares each number with it. One pass cannot do it, because
the mean depends on values we have not seen yet.

</details>

**17.** Multiply two lists element by element. For example, `[1, 2, 3]` and `[4, 5, 6]` give `[4, 10, 18]`.

<details class="dl-answer"><summary>answer</summary>

```python
products = [a * b for a, b in zip(xs, ys)]
```

`zip` takes two lists and pairs up their elements: the first with the
first, the second with the second, and so on.

Or we can use the index:

```python
products = [xs[i] * ys[i] for i in range(len(xs))]
```

`zip` stops at the end of the shorter list. Sometimes that is what you
want. Other times, lists of different lengths should have been an error,
and `zip` hides the problem without telling you.

</details>

**18.** Write `dot_product(a, b)`. Decide what it does when the lists have different lengths, and say why.

<details class="dl-answer"><summary>answer</summary>

```python
def dot_product(a, b):
    if len(a) != len(b):
        raise ValueError("dot product needs two lists of the same length")
    return sum(x * y for x, y in zip(a, b))
```

`[1, 2, 3] · [4, 5, 6]` is 32.

`raise` stops the function and reports an error on purpose.

Raising an error is better than returning `None`, and better than
quietly using the shorter list. The dot product of two vectors of
different lengths is a question that makes no sense. It is not a smaller
dot product. An error says so at the point where the mistake happened,
and not a few functions later.

</details>

## Sequences

**19.** Write functions for the square numbers and the triangular numbers. Print the first eight of each.

<details class="dl-answer"><summary>answer</summary>

```python
def square(n):
    return n ** 2


def triangular(n):
    return n * (n + 1) // 2
```

Squares: 1, 4, 9, 16, 25, 36, 49, 64. Triangular numbers: 1, 3, 6, 10, 15, 21, 28, 36.

The triangular function uses `//`, whole-number division, and not `/`.
This keeps the answer a whole number. Nothing is lost, because `n(n+1)`
is always even.

</details>

**20.** Add pairs of triangular numbers that sit next to each other: 1+3, 3+6, 6+10, 10+15. What do you get?

<details class="dl-answer"><summary>answer</summary>

4, 9, 16, 25. These are the square numbers.

Take two triangles of the same size, and flip one. They fit together
into a square. This is one of the few results here that a picture shows
faster than a proof. The algebra is short, though:
n(n+1)/2 + (n+1)(n+2)/2 = (n+1)².

</details>

**21.** Can you generate the first fifteen Fibonacci numbers?

<details class="dl-answer"><summary>answer</summary>

```python
fibs = [1, 1]
while len(fibs) < 15:
    fibs.append(fibs[-1] + fibs[-2])
print(fibs)
```

1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610.

Here `fibs[-1]` and `fibs[-2]` show why negative indexes are useful. To
get "the last two", we do not need to do any sums with the length.

</details>

**22.** Divide each Fibonacci number by the one before it. What happens?

<details class="dl-answer"><summary>answer</summary>

The results settle on about 1.6180339887. This number is the golden
ratio, which is exactly (1 + √5)/2.

```python
for i in range(2, len(fibs)):
    print(fibs[i] / fibs[i - 1])
```

The results go above it, then below it, then above it again, and each
time they come closer. That is a limit. We reach it here from a very
different direction than
[Approaching a Limit](tutorial:approaching-a-limit) does.

</details>

**23.** Write `generate_sequence(rule, n)`. It takes a *function* and returns the first n terms of the sequence that the function defines.

<details class="dl-answer"><summary>answer</summary>

```python
def generate_sequence(rule, n):
    return [rule(i) for i in range(1, n + 1)]


print(generate_sequence(square, 5))       # [1, 4, 9, 16, 25]
print(generate_sequence(triangular, 5))   # [1, 3, 6, 10, 15]
```

Passing a function as an argument feels strange the first time. It works
the same way as passing a number. `square` without brackets is the
function itself. `square(3)` is the result of calling it. The difference
between those two is the whole idea.

</details>

## From the Everlearning Problem Bank

**24.** Given a list of whole numbers, find the number that appears most often.

<details class="dl-answer"><summary>answer</summary>

```python
def most_frequent(numbers):
    best, best_count = numbers[0], 0
    for n in numbers:
        count = numbers.count(n)
        if count > best_count:
            best, best_count = n, count
    return best
```

`numbers.count(n)` walks through the whole list. It sits inside a loop
that also walks through the whole list. So the work grows with the
square of the list's length. For a few hundred numbers, you will not
notice. For a few hundred thousand, you could wait for minutes.
`Counter`, from Python's standard library, does the same job in one pass.

If two numbers tie, the one found first wins here. The problem does not
say how to break a tie, so whether this is right depends on a question
nobody answered.

</details>

**25.** Reverse the order of the words in a sentence, but keep each word the same.

<details class="dl-answer"><summary>answer</summary>

```python
def reverse_words(sentence):
    return " ".join(sentence.split()[::-1])
```

`"the quick brown fox"` becomes `"fox brown quick the"`.

`split()` with nothing in the brackets splits on any run of spaces, and
drops empty pieces. So it handles double spaces without you having to
think about them. `split(" ")` does not do this.

</details>

**26.** Take a string, and return four copies of its last four characters.

<details class="dl-answer"><summary>answer</summary>

```python
def four_of_the_last_four(text):
    return text[-4:] * 4
```

`"Python"` gives `"thonthonthonthon"`.

What if the string is shorter than four characters? Then `text[-4:]`
returns the whole string, with no error. A slice never goes out of
range: it stops at the ends. An index that is out of range fails. Is that what we want here? Again, the
problem does not say.

</details>

**27.** Given a list of numbers, return a new list with the repeated values removed. Keep the original order.

<details class="dl-answer"><summary>answer</summary>

```python
def unique(numbers):
    seen, result = [], []
    for n in numbers:
        if n not in seen:
            seen.append(n)
            result.append(n)
    return result
```

`set(numbers)` also removes repeated values, in one word, but it loses
the order. Keeping the order is the hard part, and it is the reason the
`seen` list is there.

</details>
