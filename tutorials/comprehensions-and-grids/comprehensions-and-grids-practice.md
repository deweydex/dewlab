---
title: "Comprehensions, grids and aliasing — Practice"
practice_for: comprehensions-and-grids
year: "2026-2027"
version: 2026.09.26.1
worlds:
  secret-messages: Codes and hidden messages, the kind spies and puzzle-setters make.
  pixel-art: Pictures made of small squares, the way a screen draws them.
---

# Comprehensions, grids and aliasing — Practice

These problems are on comprehensions, grids and two names for one list,
with three from earlier pages. Comprehensions and generator expressions are this
page's own tools, so the first solution to a problem may use them. Try each
problem before you open anything under it.

## 1. What each one gives

What does each of these give? Try them in the cell.

- (a) `[n * 2 for n in range(4)]`
- (b) `[n for n in range(10) if n % 3 == 0]`
- (c) `[word[0] for word in words]`
- (d) `sum(n for n in range(5))`
- (e) `"".join(str(n) for n in range(5))`
- (f) `[[0] * 2 for _ in range(3)]`

```python exec
id: what-each-one-gives-1
words = ["OTTER", "OWL", "HEDGEHOG", "BAT"]
print([n * 2 for n in range(4)])
```

<details class="dl-answer"><summary>answer</summary>

(a) `[0, 2, 4, 6]`. (b) `[0, 3, 6, 9]`. (c) `['O', 'O', 'H', 'B']`.
(d) `10`. (e) `'01234'`. (f) `[[0, 0], [0, 0], [0, 0]]`.

In (b), 0 passes the test: 0 divided by 3 is 0, with no remainder.
(e) looks like a number, but it is a string. `join()` always returns a
string. (f) is a grid with 3 rows and 2 columns. The number in `range()`
says how many rows, and the number after `*` how long each row is.

</details>

## 2. There and back

Can you write this loop as a comprehension, under the name `short`?

```python exec
id: there-and-back-1
words = ["OTTER", "OWL", "HEDGEHOG", "BAT"]
short_words = []
for word in words:
    if len(word) <= 3:
        short_words.append(word)
print(short_words)

short = []
print(short)
```

```inputs
short
```

```solution
words = ["OTTER", "OWL", "HEDGEHOG", "BAT"]
short_words = []
for word in words:
    if len(word) <= 3:
        short_words.append(word)
print(short_words)

short = [word for word in words if len(word) <= 3]
print(short)
---
The appended value goes at the front, the `for` line next, without its
colon, and the `if` at the end.
```

Then try the other direction. Can you write
`[len(word) * 10 for word in words]` as a loop?

<details class="dl-answer"><summary>answer</summary>

```python
tens = []
for word in words:
    tens.append(len(word) * 10)
```

Both give `[50, 30, 80, 30]`. If you turn a comprehension back into a loop,
you can check that you have read it the way Python does.

</details>

## 3. Without a list

With `words = ["OTTER", "OWL", "HEDGEHOG", "BAT"]`, can you use a
generator expression for each of these?

- (a) Count the words with more than 3 letters.
- (b) Join the first letter of each word into one string.
- (c) Count the letters in all the words together.

<details class="dl-answer"><summary>answer</summary>

```python
sum(1 for word in words if len(word) > 3)     # 2
"".join(word[0] for word in words)            # 'OOHB'
sum(len(word) for word in words)              # 19
```

(a) adds 1 for each word that passes the test: OTTER and HEDGEHOG. (c)
adds 5 + 3 + 8 + 3. None of these builds a list. Each value goes straight
to `sum()` or `join()`. With square brackets the answers are the same, and
a list is built first.

</details>

## 4. b = a

```python exec
id: b-equals-a-1
a = [1, 2, 3]
b = a
b.append(4)
print(a)
```

```predict
What will it print?

- [1, 2, 3]
  - Only `b` was changed.
- [1, 2, 3, 4]
  - `a` and `b` are two names for one list.
```

<details class="dl-answer"><summary>why</summary>

`[1, 2, 3, 4]`. `b = a` did not copy the list. Both names label the same
one, so a change through either shows through both. For a separate list,
write `b = a[:]` or `b = list(a)`.

</details>

## 5. A function that adds

```python exec
id: a-function-that-adds-1
def add_item(items):
    items.append("new")

things = ["a", "b"]
add_item(things)
print(things)
```

```predict
What will it print?

- ['a', 'b']
  - What happens inside a function stays inside it.
- ['a', 'b', 'new']
  - `items` and `things` are two names for one list.
```

<details class="dl-answer"><summary>why</summary>

`['a', 'b', 'new']`. The function never gave `items` a new value with
`=`, which would have stayed inside it. It changed the list `items` names,
and that is the list `things` names too. It is problem 4 again, with the
second name made by a call.

</details>

## 6. Two rows, one list

```python exec
id: two-rows-one-list-1
rows = [[0] * 3] * 2
rows[1][0] = 7
print(rows)
```

```predict
What will it print?

- [[0, 0, 0], [7, 0, 0]]
  - Only row 1 was changed.
- [[7, 0, 0], [7, 0, 0]]
  - `* 2` put the same row in twice.
```

<details class="dl-answer"><summary>why</summary>

`[[7, 0, 0], [7, 0, 0]]`. `* 2` did not make two rows. It put one row into
the outer list twice. A comprehension runs `[0] * 3` once for each row,
so each row is a new list: `[[0] * 3 for _ in range(2)]`.

</details>

## 7. A copy that is not

```python exec
id: a-copy-that-is-not-1
grid = [[0, 0], [0, 0]]
copy = grid[:]
copy[0][0] = 1
print(grid)
```

```predict
What will it print?

- [[0, 0], [0, 0]]
  - `grid[:]` made a copy, so `grid` is left alone.
- [[1, 0], [0, 0]]
  - The copy is a new outer list, holding the same rows.
```

<details class="dl-answer"><summary>why</summary>

`[[1, 0], [0, 0]]`. `grid[:]` made a new outer list, and put the same two
rows in it. `copy[0]` and `grid[0]` are one row with two names. To copy
the rows as well, copy each one: `copy = [row[:] for row in grid]`.

</details>

## 8. A times table

Can you build `times_table`, a 4 × 4 grid with a comprehension, where row
1 is `[1, 2, 3, 4]` and row 4 is `[4, 8, 12, 16]`?

```python exec
id: a-times-table-1
times_table = []
for row in times_table:
    print(row)
```

```inputs
times_table
```

```hint
Forget the grid for a moment. How would you write the row for 3 as a
comprehension? Which part of it changes from row to row?
```

```solution
times_table = [[row * column for column in range(1, 5)] for row in range(1, 5)]
for row in times_table:
    print(row)
---
The inner comprehension makes one row, and the outer one makes a row for
each number from 1 to 4. Printing one row at a time shows the grid as a
square.
```

## 9. In the square, or out of it

<div class="dl-world" data-world="secret-messages">

Can you write `encode(word, square)`, which gives the Polybius pairs for a
word: each letter's row and column in the square, counting from 0?

```python exec
id: in-the-square-1--secret-messages
square = [
    ["A", "B", "C", "D", "E"],
    ["F", "G", "H", "I", "K"],
    ["L", "M", "N", "O", "P"],
    ["Q", "R", "S", "T", "U"],
    ["V", "W", "X", "Y", "Z"],
]

def encode(word, square):
    pairs = []
    return pairs
```

```inputs
guess: yes
encode("HELP", square)
encode("OTTER", square)
encode("", square)
```

```hint
For each letter, look through every row and every column. `enumerate()`
gives the index of each, so when the letter is found, both numbers are to
hand.
```

```solution
square = [
    ["A", "B", "C", "D", "E"],
    ["F", "G", "H", "I", "K"],
    ["L", "M", "N", "O", "P"],
    ["Q", "R", "S", "T", "U"],
    ["V", "W", "X", "Y", "Z"],
]

def encode(word, square):
    pairs = []
    for letter in word:
        for row_number, row in enumerate(square):
            for column_number, entry in enumerate(row):
                if entry == letter:
                    pairs.append([row_number, column_number])
    return pairs
---
Three loops, one inside the next: each letter, each row, each column.
What does it give for a J, which is not in the square? What should it
give?
```

</div>

<div class="dl-world" data-world="pixel-art">

Can you write `mirror(picture)`, which gives a new picture with each row
reversed, and leaves `picture` itself unchanged?

```python exec
id: in-the-square-1--pixel-art
picture = [
    [1, 0, 0, 0],
    [1, 1, 0, 0],
    [1, 1, 1, 0],
]

def mirror(picture):
    return []
```

```inputs
guess: yes
mirror(picture)
mirror([[1, 2, 3]])
mirror([])
```

```hint
For one row, can you build the row backwards, by counting its indexes
down? Then do that for every row, into a new grid.
```

```solution
title: with what you've met so far
picture = [
    [1, 0, 0, 0],
    [1, 1, 0, 0],
    [1, 1, 1, 0],
]

def mirror(picture):
    result = []
    for row in picture:
        backwards = []
        for index in range(len(row) - 1, -1, -1):
            backwards.append(row[index])
        result.append(backwards)
    return result
```

```solution
title: a shorter way you'll meet later
picture = [
    [1, 0, 0, 0],
    [1, 1, 0, 0],
    [1, 1, 1, 0],
]

def mirror(picture):
    return [row[::-1] for row in picture]
---
`row[::-1]` is a new list, so `picture` is left as it was. A version that
reversed each row in place would change the caller's picture too.
```

</div>

## 10. Pair by pair

Can you set `products` to the two lists multiplied element by element?
`[1, 2, 3]` and `[4, 5, 6]` give `[4, 10, 18]`.

```python exec
id: pair-by-pair-1
xs = [1, 2, 3]
ys = [4, 5, 6]

print(products)
```

```inputs
products
```

```solution
title: with what you've met so far
xs = [1, 2, 3]
ys = [4, 5, 6]
products = [xs[index] * ys[index] for index in range(len(xs))]
print(products)
```

```solution
title: a shorter way you'll meet later
xs = [1, 2, 3]
ys = [4, 5, 6]
products = [x * y for x, y in zip(xs, ys)]
print(products)
---
`zip()` pairs up two lists: first with first, second with second. It stops
at the end of the shorter one. Sometimes that is what you want. Other
times, lists of different lengths should have been a mistake, and `zip()`
hides it without a word.
```

## 11. Different lengths

Can you write `dot_product(a, b)` so that it does something on purpose when
the two lists have different lengths? Decide what, and say why.

```python exec
id: different-lengths-1
def dot_product(a, b):
    return 0
```

```inputs
guess: yes
dot_product([1, 2, 3], [4, 5, 6])
dot_product([1, 2], [3, 4, 5])
```

```solution
title: with what you've met so far
def dot_product(a, b):
    if len(a) != len(b):
        return None
    total = 0
    for index in range(len(a)):
        total = total + a[index] * b[index]
    return total
---
`None` says "there is no answer" to whoever called it. It is better than
quietly using the shorter list, which gives an answer to a question that
was never asked.
```

```solution
title: a shorter way you'll meet later
def dot_product(a, b):
    if len(a) != len(b):
        raise ValueError("dot_product needs two lists of the same length")
    return sum(x * y for x, y in zip(a, b))
---
`raise` stops the function with an error of its own. It is louder than
`None`, which can travel a long way through a program before anything goes
wrong. An error says so where the mistake happened.
```

## 12. Triangles make squares

Add each triangular number to the one after it: 1 + 3, 3 + 6, 6 + 10,
10 + 15. What do you get?

```python exec
id: triangles-make-squares-1
triangular = [n * (n + 1) // 2 for n in range(1, 9)]
print(triangular)
print([triangular[i] + triangular[i + 1] for i in range(len(triangular) - 1)])
```

<details class="dl-answer"><summary>answer</summary>

4, 9, 16, 25, 36 and so on: the square numbers. Take two staircases of
blocks, one a step bigger than the other, rotate one, and they fit
together into a square. The algebra agrees:
$\frac{n(n+1)}{2} + \frac{(n+1)(n+2)}{2} = (n+1)^2$.

</details>

## 13. The odd numbers

Can you write a rule, `odd(n)`, for the odd numbers 1, 3, 5, 7, …, so that
`generate_sequence(odd, 5)` gives `[1, 3, 5, 7, 9]`? Then add up the first
few odd numbers. What do you notice?

```python exec
id: the-odd-numbers-1
def generate_sequence(rule, n):
    return [rule(i) for i in range(1, n + 1)]

def odd(n):
    return 0
```

```inputs
guess: yes
generate_sequence(odd, 5)
sum(generate_sequence(odd, 5))
sum(generate_sequence(odd, 10))
```

```solution
def generate_sequence(rule, n):
    return [rule(i) for i in range(1, n + 1)]

def odd(n):
    return 2 * n - 1
---
The sums are square numbers: the first 5 odd numbers make 25, and the
first 10 make 100. Each odd number adds one more L-shaped layer round a
square.
```

## 14. From earlier: where the cut is

From *Lists and looping over them*.

```python exec
id: from-earlier-where-the-cut-is-1
word = "ALGORITHMS"
print(word[2:5])
```

```predict
What will it print?

- GOR
  - The slice stops before index 5.
- GORI
  - From 2 to 5 is four letters.
- LGOR
  - Counting from 1, index 2 is L.
```

<details class="dl-answer"><summary>why</summary>

`GOR`. A string slices the same way as a list. The numbers are the cuts
between letters, and a slice keeps what lies between two cuts.

</details>

## 15. From earlier: one name, two places

From *Writing your own functions*.

```python exec
id: from-earlier-one-name-two-places-1
total = 5

def add_one():
    total = 10
    return total + 1

print(add_one())
print(total)
```

```predict
What will the last line print?

- 5
  - The `total` inside the function is a different variable.
- 10
  - The function set `total` to 10.
- 11
  - The function added one to `total`.
```

<details class="dl-answer"><summary>why</summary>

5. The `total = 10` inside the function made a local variable, which
disappears when the function returns. The `total` outside was never
touched. Compare problem 5. There, nothing was assigned, and a list was
changed in place.

</details>

## 16. From earlier: a number that is text

From *Variables, data types and text*.

```python exec
id: from-earlier-a-number-that-is-text-1
width = "320"
print(width * 2)
```

```predict
What will it print?

- 640
  - Two times 320 is 640.
- 320320
  - `*` with a string repeats it.
- An error
  - Text cannot be multiplied.
```

<details class="dl-answer"><summary>why</summary>

`320320`. The quotes make `width` a string, and `*` repeats a string. To
get 640, turn it into a number first: `int(width) * 2`.

</details>
