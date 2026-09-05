---
title: "Lists and Sequences — Practice"
slug: lists-and-sequences-practice
practice_for: lists-and-sequences
module: mit-pdp-maths-prog-integration
module_title: "Programming and Maths, Integrated"
year: "2026-2027"
series: programming-foundations
version: 2026.08.23.1
---

# Lists and Sequences — Practice

Answers are folded. Indexing and slicing reward being tried rather than reasoned about, so run the tools cell and poke at it before answering from memory.

## Indexing and Slicing

```python exec
id: indexing-and-slicing-1
xs = [10, 20, 30, 40, 50]
print(xs[0], xs[4], xs[-1], xs[-2])
print(xs[1:4], xs[:3], xs[2:], xs[::-1])
```

**1.** With `xs = [10, 20, 30, 40, 50]`, give each.

- (a) `xs[0]`
- (b) `xs[2]`
- (c) `xs[-1]`
- (d) `xs[5]`
- (e) `len(xs)`

<details class="dl-answer"><summary>answer</summary>

(a) 10. (b) 30. (c) 50. (d) an `IndexError`. (e) 5.

The last valid index is always `len(xs) - 1`, and that off-by-one is worth saying out loud a few times until it stops being surprising.

</details>

**2.** Give each slice.

- (a) `xs[1:3]`
- (b) `xs[:2]`
- (c) `xs[3:]`
- (d) `xs[:]`
- (e) `xs[::2]`
- (f) `xs[::-1]`

<details class="dl-answer"><summary>answer</summary>

(a) `[20, 30]`. (b) `[10, 20]`. (c) `[40, 50]`. (d) the whole list. (e) `[10, 30, 50]`. (f) `[50, 40, 30, 20, 10]`.

A slice excludes its end, exactly like `range`. And `xs[:]` is not pointless — it makes a copy, which matters in the next question.

</details>

**3.** What does this print, and why?

```python
a = [1, 2, 3]
b = a
b.append(4)
print(a)
```

<details class="dl-answer"><summary>answer</summary>

`[1, 2, 3, 4]`.

`b = a` did not copy the list. Both names refer to the same list, so changing it through one name changes what the other sees. `b = a[:]` or `b = list(a)` makes an actual copy.

This is the single most common source of baffling behaviour in a first year of Python, and it comes from lists being changeable in a way that numbers and strings are not.

</details>

**4.** After `xs[1] = 99`, what is `xs`? What happens if you try the same with a string?

<details class="dl-answer"><summary>answer</summary>

`[10, 99, 30, 40, 50]`.

`s[1] = "x"` on a string raises a `TypeError`. Strings are immutable — you build a new one instead, with slicing or `replace`. Lists are mutable, and that difference is why a list can be quietly changed underneath you and a string cannot.

</details>

## Building Lists

**5.** Build a list of the first ten square numbers, two ways.

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

`[1, 4, 9, 16, 25, 36, 49, 64, 81, 100]`. The second is a comprehension, and it is the same loop written on one line.

</details>

**6.** Build a list of the even numbers from a list of mixed numbers.

<details class="dl-answer"><summary>answer</summary>

```python
evens = [n for n in numbers if n % 2 == 0]
```

The `if` at the end of a comprehension filters. Building a new list rather than removing from the old one is nearly always the right move — deleting from a list while looping over it skips items, in a way that looks like a bug in Python and is not.

</details>

**7.** Given `words = ["apple", "fig", "banana", "kiwi"]`, build a list of their lengths, and find the longest word.

<details class="dl-answer"><summary>answer</summary>

```python
lengths = [len(w) for w in words]     # [5, 3, 6, 4]

longest = words[0]
for w in words:
    if len(w) > len(longest):
        longest = w
```

`banana`. The one-line version is `max(words, key=len)`, and writing the loop once first is what makes that line readable when you meet it.

</details>

**8.** Reverse a list without using `reverse()` or `[::-1]`.

<details class="dl-answer"><summary>answer</summary>

```python
result = []
for item in xs:
    result.insert(0, item)
```

Or by walking backwards:

```python
result = [xs[i] for i in range(len(xs) - 1, -1, -1)]
```

The `-1` as the stop value is what makes it reach index 0, since the stop is excluded. Ranges counting down are where that exclusion stops feeling convenient.

</details>

## Working Through a List

**9.** Sum a list without `sum()`. Then find its mean.

<details class="dl-answer"><summary>answer</summary>

```python
total = 0
for n in numbers:
    total = total + n
mean = total / len(numbers)
```

An empty list divides by zero here. Deciding what the mean of nothing should be is a real question with no obvious answer, which is why most libraries raise an error rather than pick one.

</details>

**10.** Count how many numbers in a list are above the mean.

<details class="dl-answer"><summary>answer</summary>

```python
mean = sum(numbers) / len(numbers)
above = sum(1 for n in numbers if n > mean)
```

You need two passes: one to find the mean, one to compare against it. There is no way to do it in a single pass, because the mean depends on values you have not seen yet.

</details>

**11.** Multiply two lists element by element: `[1, 2, 3]` and `[4, 5, 6]` gives `[4, 10, 18]`.

<details class="dl-answer"><summary>answer</summary>

```python
products = [a * b for a, b in zip(xs, ys)]
```

or by index:

```python
products = [xs[i] * ys[i] for i in range(len(xs))]
```

`zip` stops at the shorter list, which is either exactly what you want or a silent bug, depending on whether unequal lengths should have been an error.

</details>

**12.** Write `dot_product(a, b)`. Decide what it does when the lists are different lengths, and say why.

<details class="dl-answer"><summary>answer</summary>

```python
def dot_product(a, b):
    if len(a) != len(b):
        raise ValueError("dot product needs two lists of the same length")
    return sum(x * y for x, y in zip(a, b))
```

`[1, 2, 3] · [4, 5, 6]` is 32.

Raising is better than returning `None` or silently using the shorter list, because the dot product of two different-length vectors is not a smaller dot product — it is a question that does not make sense. An error says so at the point where the mistake was made, rather than a few functions later.

</details>

## Sequences

**13.** Write functions for the square numbers and the triangular numbers, and print the first eight of each.

<details class="dl-answer"><summary>answer</summary>

```python
def square(n):
    return n ** 2


def triangular(n):
    return n * (n + 1) // 2
```

Squares: 1, 4, 9, 16, 25, 36, 49, 64. Triangulars: 1, 3, 6, 10, 15, 21, 28, 36.

`//` rather than `/` in the triangular one keeps it a whole number. `n(n+1)` is always even, so nothing is lost.

</details>

**14.** Add consecutive triangular numbers: 1+3, 3+6, 6+10, 10+15. What do you get?

<details class="dl-answer"><summary>answer</summary>

4, 9, 16, 25 — the square numbers.

Two triangles of the same size, one flipped, fit together into a square. It is one of the few results in this area you can see in a picture faster than you can prove it algebraically, though the algebra is short: n(n+1)/2 + (n+1)(n+2)/2 = (n+1)².

</details>

**15.** Generate the first fifteen Fibonacci numbers.

<details class="dl-answer"><summary>answer</summary>

```python
fibs = [1, 1]
while len(fibs) < 15:
    fibs.append(fibs[-1] + fibs[-2])
print(fibs)
```

1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610.

`fibs[-1]` and `fibs[-2]` are why negative indices earn their keep: "the last two" needs no arithmetic on the length.

</details>

**16.** Divide each Fibonacci number by the one before it. What happens?

<details class="dl-answer"><summary>answer</summary>

The ratios settle on about 1.6180339887 — the golden ratio, exactly (1 + √5)/2.

```python
for i in range(2, len(fibs)):
    print(fibs[i] / fibs[i - 1])
```

They alternate above and below it, closing in from both sides. That is a limit, arrived at from a completely different direction than *Approaching a Limit* comes at it.

</details>

**17.** Write `generate_sequence(rule, n)` that takes a *function* and returns the first n terms of the sequence it defines.

<details class="dl-answer"><summary>answer</summary>

```python
def generate_sequence(rule, n):
    return [rule(i) for i in range(1, n + 1)]


print(generate_sequence(square, 5))       # [1, 4, 9, 16, 25]
print(generate_sequence(triangular, 5))   # [1, 3, 6, 10, 15]
```

Passing a function as an argument feels strange the first time. It is the same as passing a number: `square` without brackets is the function itself, `square(3)` is the result of calling it, and the difference between those two is the whole idea.

</details>

## From the Everlearning Problem Bank

**18.** Given a list of integers, find the number that appears most often.

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

`numbers.count(n)` walks the whole list, and it is inside a loop over the whole list, so this does n² work. For a few hundred numbers that is invisible; for a few hundred thousand it is a coffee break. A `Counter` from the standard library does it in one pass.

Ties are unresolved here — the first one found wins. Whether that is right depends on a question the problem did not answer.

</details>

**19.** Reverse the words of a sentence, keeping the words themselves intact.

<details class="dl-answer"><summary>answer</summary>

```python
def reverse_words(sentence):
    return " ".join(sentence.split()[::-1])
```

`"the quick brown fox"` becomes `"fox brown quick the"`.

`split()` with no argument splits on any run of whitespace and drops empties, which handles double spaces without you thinking about it. `split(" ")` does not.

</details>

**20.** Take a string and return four copies of its last four characters.

<details class="dl-answer"><summary>answer</summary>

```python
def four_of_the_last_four(text):
    return text[-4:] * 4
```

`"Python"` gives `"thonthonthonthon"`.

For a string shorter than four characters, `text[-4:]` quietly returns the whole thing rather than failing — slices clamp, indexes do not. Whether that is the desired behaviour is again a question the problem left open.

</details>

**21.** Given a list of numbers, return a new list with the duplicates removed, keeping the original order.

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

`set(numbers)` removes duplicates in one word and loses the order. Keeping the order is the whole difficulty, and it is why the `seen` list exists.

</details>
