---
title: "Experiments with comprehensions: lists in one line"
year: "2026-2027"
version: 2026.11.16.1
---

# Experiments with comprehensions: lists in one line

A list comprehension builds a new list in one line. It does the same job as a loop that starts with an empty list and appends to it, only more compactly. Each section shows a loop beside its comprehension twin and then asks you to play. Run everything and change it, because reading comprehensions is much harder than writing them.

## 1. The loop and its twin

Here are two programs that build the same list. The first uses a loop and the second uses a comprehension.

```python exec
id: the-loop-and-its-twin-1
squares = []
for n in range(6):
    squares.append(n * n)
print(squares)
```

```python exec
id: the-loop-and-its-twin-2
squares = [n * n for n in range(6)]
print(squares)
```

The comprehension has three parts inside its brackets. The expression `n * n` makes each item, the variable `n` holds each value in turn, and the source `range(6)` supplies the values.

**1.1** Run both versions. Do they print the same thing? Match each part of the comprehension to a line of the loop.

**1.2** Change the expression `n * n` to `n * n * n`, then to `n + 100`, then to `-n`, then to `n % 3`. Predict each result before you run it.

```python exec
id: the-loop-and-its-twin-3
squares = [n * n for n in range(6)]
print(squares)
# your code here
```

**1.3** Change the source to `range(1, 11)`, then to `range(0, 20, 5)`, then to a list of your own such as `[2, 4, 6]`.

```python exec
id: the-loop-and-its-twin-4
squares = [n * n for n in range(6)]
print(squares)
# your code here
```

**1.4** Use a string as the source with `[letter for letter in "python"]`. Change the expression to `letter * 2`, and then to `letter.upper()`.

```python exec
id: the-loop-and-its-twin-5
print([letter for letter in "python"])
# your code here
```

**1.5** Build a list of the first ten even numbers twice, once with a loop and append, and once with a comprehension. Which version did you find easier to write? Which one is easier to read?

```python exec
id: the-loop-and-its-twin-6
# your code here
```

**1.6** Break it on purpose. Run each of these cells on its own and read what Python says.

```python exec
id: the-loop-and-its-twin-7
[n * n for n in range(6)
```

```python exec
id: the-loop-and-its-twin-8
[n * n n in range(6)]
```

```python exec
id: the-loop-and-its-twin-9
[n * n for n range(6)]
```

```python exec
id: the-loop-and-its-twin-10
[for n in range(6)]
```

**1.7** The brackets decide what kind of thing you build. Print each of these and compare.

```python exec
id: the-loop-and-its-twin-11
print((n * n for n in range(6)))
print({n * n for n in range(6)})
```

Python calls the first a generator and the second a set. We will not use either here, but wrap the first one in `list()` to see what it holds.

## 2. Changing every item

The expression at the front can be anything that makes a value, including a method call.

```python exec
id: changing-every-item-1
words = ["apple", "banana", "cherry"]
shout = [w.upper() for w in words]
print(shout)
```

**2.1** Run it. Then change the expression to `w + "!"`, then to `w[0]`, then to `len(w)`, then to `w[::-1]`. Which of these changes the type of the items in the list?

```python exec
id: changing-every-item-2
words = ["apple", "banana", "cherry"]
print([w.upper() for w in words])
# your code here
```

**2.2** Build a list of temperatures in Fahrenheit from `[0, 20, 37, 100]` in Celsius. The rule is `c * 9 / 5 + 32`.

```python exec
id: changing-every-item-3
celsius = [0, 20, 37, 100]
# your code here
```

**2.3** Convert between types. Predict each result, then run it.

```python exec
id: changing-every-item-4
nums = [1, 2, 3]
print([str(n) for n in nums])
print([int(s) for s in ["4", "5", "6"]])
print([float(s) for s in ["1.5", "2", "3.25"]])
```

**2.4** Now break one. Run `[int(s) for s in ["1", "two", "3"]]`. Which item does Python complain about? Does the list print anything before it fails?

```python exec
id: changing-every-item-5
print([int(s) for s in ["1", "two", "3"]])
# your code here
```

**2.5** Use the list `words` from above. Make a list of the first letter of each word. Then make a list of each word with its first letter capitalised, using the string method `capitalize()`. Which of these two lists keeps the same length as `words`?

```python exec
id: changing-every-item-6
words = ["apple", "banana", "cherry"]
# your code here
```

**2.6** Every item in the new list comes from one item in the old list. Use that fact to predict the length of `[n * 2 for n in range(7)]` without running it. Then check.

```python exec
id: changing-every-item-7
print(len([n * 2 for n in range(7)]))
# your code here
```

## 3. Filtering and choosing

An `if` at the end of a comprehension keeps only the items that pass the test.

```python exec
id: filtering-and-choosing-1
nums = [3, 8, 1, 12, 7, 10]
big = [n for n in nums if n > 5]
print(big)
```

**3.1** Run it. Then write the loop version that does the same job, with an `if` inside the loop. Which line of the loop matches the `if` in the comprehension?

```python exec
id: filtering-and-choosing-2
nums = [3, 8, 1, 12, 7, 10]
print([n for n in nums if n > 5])
# your code here
```

**3.2** From `nums`, build a list of the even numbers, then a list of the odd numbers, then a list of the multiples of 3.

```python exec
id: filtering-and-choosing-3
nums = [3, 8, 1, 12, 7, 10]
# your code here
```

**3.3** From `["apple", "fig", "banana", "kiwi", "cherry"]`, build a list of the words longer than 4 letters, and then a list of the words that contain the letter `a`.

```python exec
id: filtering-and-choosing-4
words = ["apple", "banana", "cherry"]
# your code here
```

**3.4** Run `[c for c in "comprehension" if c not in "aeiou"]`. What does the result look like? Wrap it in the string method `"".join(...)`, which glues a list of strings into one string, to get a single word back.

```python exec
id: filtering-and-choosing-5
print([c for c in "comprehension" if c not in "aeiou"])
# your code here
```

**3.5** Filter and change together. Square only the even numbers in `nums`. Which part of the comprehension does the squaring, and which part does the filtering?

```python exec
id: filtering-and-choosing-6
nums = [3, 8, 1, 12, 7, 10]
# your code here
```

**3.6** Move the `if` to the front, as in `[n for if n > 5 n in nums]`, and read the error. Where does Python expect the test to sit?

```python exec
id: filtering-and-choosing-7
nums = [3, 8, 1, 12, 7, 10]
print([n for if n > 5 n in nums])
# your code here
```

Now we meet a second kind of `if`. Run this one.

```python exec
id: filtering-and-choosing-8
labels = ["even" if n % 2 == 0 else "odd" for n in range(6)]
print(labels)
```

**3.7** Compare the length of `labels` with the length of `[n for n in range(6) if n % 2 == 0]`. One keeps every item and the other drops some. Which is which?

```python exec
id: filtering-and-choosing-9
# your code here
```

**3.8** Add an `else` to a filtering comprehension, as in `[n for n in range(6) if n % 2 == 0 else n]`, and read the error. Then explain in your own words why an `if` with an `else` belongs at the front, and an `if` without an `else` belongs at the end.

```python exec
id: filtering-and-choosing-10
print([n for n in range(6) if n % 2 == 0 else n])
words = ["apple", "banana", "cherry"]
# your code here
```

**3.9** Make a list that holds `"pass"` for every score of 50 or more and `"retry"` for every score below 50, from `[72, 45, 50, 38, 91]`.

```python exec
id: filtering-and-choosing-11
# your code here
```

## 4. Two loops in one

A comprehension can hold more than one `for`. Compare the loop version with the comprehension version.

```python exec
id: two-loops-in-one-1
table = []
for a in range(1, 4):
    for b in range(1, 4):
        table.append(a * b)
print(table)
```

```python exec
id: two-loops-in-one-2
table = [a * b for a in range(1, 4) for b in range(1, 4)]
print(table)
```

**4.1** Run both. Which `for` is the outer loop, and which is the inner loop? Swap the order of the two `for` parts in the comprehension and compare the results.

```python exec
id: two-loops-in-one-3
print([a * b for a in range(1, 4) for b in range(1, 4)])
# your code here
```

**4.2** Predict the result of `[c + n for c in "ab" for n in "123"]` before you run it. Then swap the two `for` parts.

```python exec
id: two-loops-in-one-4
print([c + n for c in "ab" for n in "123"])
# your code here
```

**4.3** Build a deck of cards with `[rank + suit for suit in "SHDC" for rank in "A23456789"]`. How many cards do you get? A real deck has thirteen ranks, so which ones are missing? Use a list of strings for the ranks instead of one string, and add them.

```python exec
id: two-loops-in-one-5
print([rank + suit for suit in "SHDC" for rank in "A23456789"])
# your code here
```

**4.4** A comprehension can build a list of lists. Run this and look closely at the brackets.

```python exec
id: two-loops-in-one-6
grid = [[row * col for col in range(4)] for row in range(3)]
print(grid)
```

Print `grid` one row per line using an ordinary loop. Which `for` builds the rows and which builds the items inside each row?

**4.5** Flatten the grid back into one list with `[x for row in grid for x in row]`. Compare the order of the two `for` parts here with the order in 4.4. What do you notice?

```python exec
id: two-loops-in-one-7
grid = [[row * col for col in range(4)] for row in range(3)]
print([x for row in grid for x in row])
# your code here
```

**4.6** Make a 5 by 5 grid in which every item is `0`. Then change the middle item to `1` with an assignment. Now try writing the grid as `[[0] * 5] * 5`, change one item, and print it. Which version behaves differently, and why?

```python exec
id: two-loops-in-one-8
# your code here
```

## 5. Puzzles and patterns

**5.1 The secret code**

Python has two small tools called `ord` and `chr`. The first turns a character into its number, and the second turns a number back into a character. Try `ord("A")` and `chr(66)`, and then run this.

```python exec
id: puzzles-and-patterns-1
shifted = [chr(ord(c) + 1) for c in "HAL"]
print(shifted)
print("".join(shifted))
```

The string method `join` glues a list of strings into one string. What word did `HAL` turn into? Change the `+ 1` to another number, and shift your own name.

**5.2 Decode it**

Every letter in `"Ifmmp"` was shifted up by one. Write a comprehension that shifts each letter down by one and joins the result. Then decode `"Uif dbu tbu"`. The spaces will cause trouble. Fix them with an `if` and `else` at the front of your expression, so that a space stays a space.

```python exec
id: puzzles-and-patterns-2
# your code here
```

**5.3 Count the vowels**

Use a comprehension with an `if` at the end to collect the vowels from a sentence of your own, and then use `len` to count them. Which vowel appears most often in your sentence?

```python exec
id: puzzles-and-patterns-3
# your code here
```

**5.4 Divisors**

What does `[d for d in range(1, 13) if 12 % d == 0]` produce? Change the 12 to other numbers. Which numbers between 2 and 30 produce only two items, a 1 and the number itself?

```python exec
id: puzzles-and-patterns-4
print([d for d in range(1, 13) if 12 % d == 0])
# your code here
```

**5.5 Perfect numbers**

A number is perfect when its divisors, not counting the number itself, add up to the number. Predict how many perfect numbers lie below 500, then run this.

```python exec
id: puzzles-and-patterns-5
for n in range(2, 500):
    divisors = [d for d in range(1, n) if n % d == 0]
    if sum(divisors) == n:
        print(n)
```

**5.6 Read it slowly**

This comprehension has another comprehension inside it. Which list is built first? Predict the output, and then run it.

```python exec
id: puzzles-and-patterns-6
primes = [n for n in range(2, 30) if len([d for d in range(2, n) if n % d == 0]) == 0]
print(primes)
```

Why does the test `len(...) == 0` find the primes? Change `range(2, 30)` to find the primes below 100.

**5.7 FizzBuzz in one line**

Run `["Fizz" if n % 3 == 0 else n for n in range(1, 16)]`. Extend it so that multiples of 5 become `"Buzz"` and multiples of both become `"FizzBuzz"`. You will need an `if` and `else` inside another `else`. How does the line look now? Would you rather read this version or a loop?

```python exec
id: puzzles-and-patterns-7
print(["Fizz" if n % 3 == 0 else n for n in range(1, 16)])
# your code here
```

## 6. Rewrite, repair and judge

**6.1 Loop to comprehension**

Rewrite each loop as a comprehension. Check that both versions print the same list.

```python exec
id: rewrite-repair-and-judge-1
result = []
for n in range(10):
    result.append(n * 3)
```

```python exec
id: rewrite-repair-and-judge-2
result = []
for word in ["sun", "moon", "star"]:
    if len(word) > 3:
        result.append(word.upper())
```

```python exec
id: rewrite-repair-and-judge-3
result = []
for n in range(1, 8):
    if n % 2 == 0:
        result.append("even")
    else:
        result.append("odd")
```

**6.2 Comprehension to loop**

Rewrite each comprehension as a loop. Which one was harder to turn into a loop?

```python exec
id: rewrite-repair-and-judge-4
[n * n for n in range(10) if n % 2 == 1]
```

```python exec
id: rewrite-repair-and-judge-5
[a + b for a in "xy" for b in "123"]
```

**6.3 Spot the bug**

Each cell has one problem. Run it, read the message, and fix it.

```python exec
id: rewrite-repair-and-judge-6
[n for n in range(10) if n % 2 == 0 else n]
```

```python exec
id: rewrite-repair-and-judge-7
nums = [1, 2, 3]
[num * 2 for n in nums]
```

```python exec
id: rewrite-repair-and-judge-8
[n * 2 for n in range(5)]]
```

**6.4 A curious one**

Run this and look at what is printed, and then at what the list holds. Why does the list hold what it holds?

```python exec
id: rewrite-repair-and-judge-9
result = [print(n) for n in range(3)]
print(result)
```

**6.5 Too far?**

This line works, but would you want to find it in someone else's program? Rewrite it as a loop with a clear variable name on each step, and say which version you would rather read next month.

```python exec
id: rewrite-repair-and-judge-10
out = [("FizzBuzz" if n % 15 == 0 else "Fizz" if n % 3 == 0 else "Buzz" if n % 5 == 0 else n) for n in range(1, 31)]
```

**6.6 Your own**

Invent a small puzzle for a neighbour. Give them a list and a goal, such as turning `["3", "x", "7"]` into `[3, 7]`, and see whether they can solve it with a comprehension.

```python exec
id: rewrite-repair-and-judge-11
# your code here
```
