---
title: "Experiments with lists: poke, prod and break"
year: "2026-2027"
version: 2026.11.16.1
---

# Experiments with lists: poke, prod and break

A list holds several values in one variable. We write a list with square brackets and commas between the items. This sheet has no explanations to read first. Run each cell, predict what it will do, change it, and then try to break it. Errors are welcome here, because every error message tells you something true about how Python thinks. Keep a note of each error name you meet, because the last section asks you about them.

## 1. Making and reading lists

**1.1** Run this. What does each of the last two lines print?

```python exec
id: making-and-reading-lists-1
colours = ["red", "green", "blue"]
print(colours)
print(type(colours))
```

**1.2** Make a list of five numbers and print it. Then make a list that holds a string, an integer, a float and a boolean together. Does Python object?

```python exec
id: making-and-reading-lists-2
# your code here
```

```solution
for: making-and-reading-lists-2
title: one way to do it
numbers = [3, 1, 4, 1, 5]
mixed = ["hello", 42, 3.14, True]
print(numbers)
print(mixed)
```

**1.3** Make an empty list by writing nothing between the brackets. Print it, and print its type.

```python exec
id: making-and-reading-lists-3
# your code here
```

```solution
for: making-and-reading-lists-3
title: one way to do it
empty = []
print(empty)
print(type(empty))
```

**1.4** Print `colours[0]`, then `colours[1]`, then `colours[2]`. Which position holds the first item? We call a position an index.

```python exec
id: making-and-reading-lists-4
colours = ["red", "green", "blue"]
# your code here
```

```solution
for: making-and-reading-lists-4
title: one way to do it
colours = ["red", "green", "blue"]
print(colours[0])
print(colours[1])
print(colours[2])
```

**1.5** Now print `colours[3]`. Read the whole error message from the bottom up. Which line names the kind of error, and which line explains it in words?

```python exec
id: making-and-reading-lists-5
colours = ["red", "green", "blue"]
# your code here
```

**1.6** Try `colours[-1]`, `colours[-2]`, `colours[-3]` and `colours[-4]`. Describe the rule Python follows. Which of the four fails?

```python exec
id: making-and-reading-lists-6
colours = ["red", "green", "blue"]
# your code here
```

```solution
for: making-and-reading-lists-6
title: one way to do it
colours = ["red", "green", "blue"]
print(colours[-1])
print(colours[-2])
print(colours[-3])
---
`colours[-4]` is the one that fails, with an `IndexError`, because the list has only three items.
```

**1.7** Print `len(colours)`. Add a fourth colour to the list, run it again, and compare the new length with the largest index you can use. What relationship do you notice?

```python exec
id: making-and-reading-lists-7
colours = ["red", "green", "blue"]
# your code here
```

```solution
for: making-and-reading-lists-7
title: one way to do it
colours = ["red", "green", "blue"]
colours.append("yellow")
print(len(colours))
print(len(colours) - 1)
```

**1.8** A list can hold other lists. Run this, and predict `grid[1][0]` before you print it.

```python exec
id: making-and-reading-lists-8
grid = [[1, 2], [3, 4], [5, 6]]
print(grid[0])
print(grid[0][1])
```

**1.9** Print `grid[3]`, and then print `grid[0][2]`. Do both fail in the same way? Compare the two messages.

```python exec
id: making-and-reading-lists-9
grid = [[1, 2], [3, 4], [5, 6]]
# your code here
```

## 2. Changing a list

Start each task here from `colours = ["red", "green", "blue"]` unless it says otherwise.

**2.1** Replace the middle item with `"yellow"` by writing `colours[1] = "yellow"`, and print the list. Then replace the last item using a negative index.

```python exec
id: changing-a-list-1
colours = ["red", "green", "blue"]
# your code here
```

```solution
for: changing-a-list-1
title: one way to do it
colours = ["red", "green", "blue"]
colours[1] = "yellow"
print(colours)
colours[-1] = "purple"
print(colours)
```

**2.2** A string looks a little like a list of letters. Try this and read the error.

```python exec
id: changing-a-list-2
word = "cat"
word[0] = "b"
```

Python calls a value mutable when we can change it in place. Which of these two types is mutable, and which is not?

**2.3** Add an item with `colours.append("purple")` and print the list. Where did the new item land? Then run these two lines and explain the output.

```python exec
id: changing-a-list-3
colours = ["red", "green", "blue"]
print(colours.append("pink"))
colours = colours.append("black")
print(colours)
```

What does `append` hand back to you? What happened to your list?

**2.4** The method `insert` puts an item at a chosen position. Try `colours.insert(0, "black")`, then `insert(2, "gold")`, then `insert(100, "silver")`, then `insert(-1, "bronze")`. Where does each item end up? Does a huge index cause an error?

```python exec
id: changing-a-list-4
colours = ["red", "green", "blue"]
# your code here
```

```solution
for: changing-a-list-4
title: one way to do it
colours = ["red", "green", "blue"]
colours.insert(0, "black")
colours.insert(2, "gold")
colours.insert(100, "silver")
colours.insert(-1, "bronze")
print(colours)
```

**2.5** Remove an item by value with `colours.remove("green")`. Then try to remove a colour that is not in the list. Then build `[1, 2, 1, 3, 1]` and call `remove(1)`. How many ones disappear?

```python exec
id: changing-a-list-5
colours = ["red", "green", "blue"]
# your code here
```

```solution
for: changing-a-list-5
title: one way to do it
colours = ["red", "green", "blue"]
colours.remove("green")
print(colours)
numbers = [1, 2, 1, 3, 1]
numbers.remove(1)
print(numbers)
```

**2.6** The method `pop` removes an item by position and hands it back. Run this and look at both variables after each line.

```python exec
id: changing-a-list-6
colours = ["red", "green", "blue"]
last = colours.pop()
print(last, colours)
first = colours.pop(0)
print(first, colours)
```

Then call `pop()` on an empty list, and call `pop(10)` on a short list. What does each error say?

**2.7** The statement `del colours[0]` also removes an item by position. Compare it with `pop`. What happens if you write `print(del colours[0])`?

```python exec
id: changing-a-list-7
colours = ["red", "green", "blue"]
# your code here
```

```solution
for: changing-a-list-7
title: one way to do it
colours = ["red", "green", "blue"]
del colours[0]
print(colours)
---
`del` is a statement, so it cannot sit inside `print(...)`. It hands nothing back, where `pop` hands back the item.
```

**2.8** Predict the length of each list before you run this.

```python exec
id: changing-a-list-8
a = [1, 2]
a.append([3, 4])
b = [1, 2]
b.extend([3, 4])
print(a, len(a))
print(b, len(b))
```

Which one ended up with a list inside a list?

**2.9** Try each of these on its own: `[1, 2] + [3]`, `[0] * 5`, `[1, 2] * 3`, `[1, 2] - [1]`, `[1, 2] + 3`. Which ones work, which ones fail, and what does each error say?

```python exec
id: changing-a-list-9
# your code here
```

```solution
for: changing-a-list-9
title: one way to do it
print([1, 2] + [3])
print([0] * 5)
print([1, 2] * 3)
---
The other two, `[1, 2] - [1]` and `[1, 2] + 3`, raise a `TypeError`.
```

**2.10** Meet three more methods: `reverse()`, `sort()` and `clear()`. Call each one on a small list of numbers. Does any of them print something? Does any of them hand back a new list?

```python exec
id: changing-a-list-10
# your code here
```

```solution
for: changing-a-list-10
title: one way to do it
numbers = [3, 1, 2]
numbers.reverse()
print(numbers)
numbers.sort()
print(numbers)
numbers.clear()
print(numbers)
```

## 3. Asking questions of a list

**3.1** Run these and note the type of each answer.

```python exec
id: asking-questions-of-a-list-1
colours = ["red", "green", "blue"]
print("red" in colours)
print("Red" in colours)
print("pink" not in colours)
```

Does Python care about capital letters here?

**3.2** The call `colours.count("red")` tells you how many times a value appears, and `colours.index("green")` tells you where it first appears. Build a list with repeated items and try both. What happens when you ask for the index of a value that is not there?

```python exec
id: asking-questions-of-a-list-2
colours = ["red", "green", "blue"]
# your code here
```

```solution
for: asking-questions-of-a-list-2
title: one way to do it
colours = ["red", "green", "blue", "red"]
print(colours.count("red"))
print(colours.index("green"))
```

**3.3** Try `min`, `max` and `sum` on `[4, 9, 2, 7]`. Then try `min` and `max` on `["pear", "apple", "fig"]`. Then try `sum` on the list of words. What does Python compare when it works with words?

```python exec
id: asking-questions-of-a-list-3
# your code here
```

```solution
for: asking-questions-of-a-list-3
title: one way to do it
print(min([4, 9, 2, 7]), max([4, 9, 2, 7]), sum([4, 9, 2, 7]))
print(min(["pear", "apple", "fig"]), max(["pear", "apple", "fig"]))
```

**3.4** Try `max([3, "a", 5])`. Why can Python not decide? The error names both types, so read it slowly.

```python exec
id: asking-questions-of-a-list-4
# your code here
```

**3.5** Sort a list of numbers with `nums.sort()` and print `nums`. Then print `nums.sort()` itself. Then try `sorted(nums)`. Which one changes the original list, and which one builds a new one? Add `reverse=True` inside the brackets of each and see what happens.

```python exec
id: asking-questions-of-a-list-5
# your code here
```

```solution
for: asking-questions-of-a-list-5
title: one way to do it
nums = [5, 2, 9, 1]
print(sorted(nums))
print(nums)
nums.sort()
print(nums)
print(sorted(nums, reverse=True))
```

**3.6** Sort `["banana", "Cherry", "apple", "Date"]`. Where do the capital letters go? Now sort `["10", "9", "100", "1"]`. Does Python order these the way you would order the numbers? What does that tell you about how it compares strings?

```python exec
id: asking-questions-of-a-list-6
letters = ["a", "b", "c", "d", "e", "f", "g"]
# your code here
```

```solution
for: asking-questions-of-a-list-6
title: one way to do it
print(sorted(["banana", "Cherry", "apple", "Date"]))
print(sorted(["10", "9", "100", "1"]))
---
Python compares strings character by character, and capital letters come before lower-case ones. `"10"` comes before `"9"` because `"1"` comes before `"9"`.
```

**3.7** The method `colours.reverse()` flips the list in place. Call it twice in a row and print after each call. Then compare it with the slice `colours[::-1]`. Which one leaves the original alone?

```python exec
id: asking-questions-of-a-list-7
colours = ["red", "green", "blue"]
# your code here
```

```solution
for: asking-questions-of-a-list-7
title: one way to do it
colours = ["red", "green", "blue"]
colours.reverse()
print(colours)
colours.reverse()
print(colours)
print(colours[::-1])
print(colours)
```

## 4. Slices

A slice picks out part of a list. Use this list for the whole section.

```python exec
id: slices-1
letters = ["a", "b", "c", "d", "e", "f", "g"]
```

**4.1** Print `letters[1:4]`. Which letters appear? Is the item at index 4 included?

```python exec
id: slices-2
letters = ["a", "b", "c", "d", "e", "f", "g"]
# your code here
```

```solution
for: slices-2
title: one way to do it
letters = ["a", "b", "c", "d", "e", "f", "g"]
print(letters[1:4])
```

**4.2** Predict, then print: `letters[:3]`, `letters[4:]`, `letters[:]` and `letters[-3:]`. What does it mean to leave out a number?

```python exec
id: slices-3
letters = ["a", "b", "c", "d", "e", "f", "g"]
# your code here
```

```solution
for: slices-3
title: one way to do it
letters = ["a", "b", "c", "d", "e", "f", "g"]
print(letters[:3])
print(letters[4:])
print(letters[:])
print(letters[-3:])
```

**4.3** Print `letters[::2]`, `letters[1::2]` and `letters[::-1]`. The third number is a step. What does a negative step do?

```python exec
id: slices-4
letters = ["a", "b", "c", "d", "e", "f", "g"]
# your code here
```

```solution
for: slices-4
title: one way to do it
letters = ["a", "b", "c", "d", "e", "f", "g"]
print(letters[::2])
print(letters[1::2])
print(letters[::-1])
```

**4.4** What does `letters[2:100]` give you? What does `letters[5:2]` give you? Does either one raise an error? Compare both with `letters[100]`.

```python exec
id: slices-5
letters = ["a", "b", "c", "d", "e", "f", "g"]
# your code here
```

```solution
for: slices-5
title: one way to do it
letters = ["a", "b", "c", "d", "e", "f", "g"]
print(letters[2:100])
print(letters[5:2])
---
A slice never raises an error for going past the end. `letters[100]` does, with an `IndexError`.
```

**4.5** Does a slice change the original list? Take a slice, print `letters` afterwards, and find out.

```python exec
id: slices-6
letters = ["a", "b", "c", "d", "e", "f", "g"]
# your code here
```

```solution
for: slices-6
title: one way to do it
letters = ["a", "b", "c", "d", "e", "f", "g"]
piece = letters[1:4]
print(piece)
print(letters)
```

**4.6** A slice can sit on the left of an equals sign. Reset `letters` before each line, try these one at a time, and describe what each one does.

```python exec
id: slices-7
letters = ["a", "b", "c", "d", "e", "f", "g"]
letters[1:3] = ["X"]
```

```python exec
id: slices-8
letters = ["a", "b", "c", "d", "e", "f", "g"]
letters[1:3] = ["X", "Y", "Z"]
```

```python exec
id: slices-9
letters = ["a", "b", "c", "d", "e", "f", "g"]
letters[1:3] = []
```

**4.7** Which slice gives the last two items, whatever the length of the list? Which slice gives everything except the first and last items? Test your answers on lists of several different lengths, including a list of two items and an empty list.

```python exec
id: slices-10
# your code here
```

```solution
for: slices-10
title: one way to do it
letters = ["a", "b", "c", "d", "e", "f", "g"]
print(letters[-2:])
print(letters[1:-1])
```

## 5. Two names, one list

**5.1** Predict what each print shows, then run it.

```python exec
id: two-names-one-list-1
a = [1, 2, 3]
b = a
b.append(4)
print(a)
print(b)
```

**5.2** Now compare that with numbers.

```python exec
id: two-names-one-list-2
x = 5
y = x
y = 6
print(x)
print(y)
```

Why did changing `y` leave `x` alone, while changing `b` changed `a`? Write your own explanation in one sentence.

**5.3** Make real copies in two different ways and test them.

```python exec
id: two-names-one-list-3
a = [1, 2, 3]
c = a.copy()
d = a[:]
c.append(99)
d.append(100)
print(a, c, d)
```

**5.4** The words `==` and `is` ask different questions. Predict the four answers, then run it.

```python exec
id: two-names-one-list-4
a = [1, 2, 3]
b = a
c = a.copy()
print(a == b, a is b)
print(a == c, a is c)
```

Which question does `is` ask, and which does `==` ask?

**5.5** Here is a trap. Predict what this prints, then run it.

```python exec
id: two-names-one-list-5
row = [0, 0, 0]
board = [row, row, row]
board[0][0] = 1
print(board)
```

Why did three cells change? Rebuild `board` so that only one cell changes.

```solution
for: two-names-one-list-5
title: one way to do it
board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
board[0][0] = 1
print(board)
---
`[row, row, row]` holds the same list three times. Three separate lists change one cell at a time.
```

## 6. Puzzles and patterns

**6.1 The mystery list**

Here is a list to investigate.

```python exec
id: puzzles-and-patterns-1
mystery = [3, 1, 4, 1, 5, 9, 2, 6]
```

Print the biggest item, the smallest item, the number of ones, the sum of all the items, the list in reverse order, and the list sorted from largest to smallest. Your code must leave `mystery` itself unchanged. Check by printing `mystery` at the end.

```solution
for: puzzles-and-patterns-1
title: one way to do it
mystery = [3, 1, 4, 1, 5, 9, 2, 6]
print(max(mystery))
print(min(mystery))
print(mystery.count(1))
print(sum(mystery))
print(mystery[::-1])
print(sorted(mystery, reverse=True))
print(mystery)
```

**6.2 The swap**

Swap the first and last items of a list of numbers. Use a third variable to hold one value while you move the other. Then look for a way to do it with no third variable. Try writing `a, b = b, a` with two ordinary variables first, and see what it does.

```python exec
id: puzzles-and-patterns-2
# your code here
```

```solution
for: puzzles-and-patterns-2
title: one way to do it
nums = [10, 20, 30, 40]
temp = nums[0]
nums[0] = nums[-1]
nums[-1] = temp
print(nums)
nums[0], nums[-1] = nums[-1], nums[0]
print(nums)
---
The second swap, with two assignments on one line, needs no third variable. It swaps the two back.
```

**6.3 The scrambled sentence**

```python exec
id: puzzles-and-patterns-3
words = ["fun", "are", "Lists", "so"]
```

Use only indexes to print the words in an order that makes a sentence. Then try `print(" ".join(words))`. The string method `join` glues a list of strings together with the text in front of the dot between them. Try a dash, an empty string, and a comma followed by a space in place of the single space.

```solution
for: puzzles-and-patterns-3
title: one way to do it
words = ["fun", "are", "Lists", "so"]
print(words[2], words[1], words[3], words[0])
ordered = [words[2], words[1], words[3], words[0]]
print(" ".join(ordered))
print("-".join(ordered))
print("".join(ordered))
```

**6.4 Your own shopping list**

Ask the user for three items with `input` and store them in a list. Print the second item. Ask for a fourth item and append it. Then ask which item to remove, and remove it. What happens if the user types something that is not in the list? Make your program survive that by checking with `in` and an if statement first.

```python exec
id: puzzles-and-patterns-4
# your code here
```

**6.5 Palindromes**

A palindrome reads the same in both directions.

```python exec
id: puzzles-and-patterns-5
letters = ["r", "a", "c", "e", "c", "a", "r"]
print(letters == letters[::-1])
```

Try other lists of letters. Find one palindrome with an odd number of items and one with an even number. Then find a list of numbers that is a palindrome.

```solution
for: puzzles-and-patterns-5
title: one way to do it
print(["a", "b", "a"] == ["a", "b", "a"][::-1])
print(["a", "b", "b", "a"] == ["a", "b", "b", "a"][::-1])
print([1, 2, 1] == [1, 2, 1][::-1])
```

**6.6 Buried treasure**

```python exec
id: puzzles-and-patterns-6
board = [[".", ".", "."], [".", ".", "."], [".", ".", "."]]
```

Hide an `"X"` in the bottom right corner by changing one item. Print the board one row per line, using a separate print for each row. Move the X to the middle. Then make the X appear using only negative indexes.

```solution
for: puzzles-and-patterns-6
title: one way to do it
board = [[".", ".", "."], [".", ".", "."], [".", ".", "."]]
board[2][2] = "X"
print(board[0])
print(board[1])
print(board[2])
board[2][2] = "."
board[1][1] = "X"
board[1][1] = "."
board[-1][-1] = "X"
print(board[-1])
```

**6.7 Build it backwards**

Start from `nums = [1, 2, 3, 4, 5]` and produce each of these lists without typing the answer by hand, and without changing `nums`: `[5, 4, 3, 2, 1]`, `[1, 3, 5]`, `[2, 4]` and `[3, 4, 5, 1, 2]`. The last one needs two slices and a `+`.

```python exec
id: puzzles-and-patterns-7
nums = [1, 2, 3, 4, 5]
# your code here
```

```solution
for: puzzles-and-patterns-7
title: one way to do it
nums = [1, 2, 3, 4, 5]
print(nums[::-1])
print(nums[::2])
print(nums[1::2])
print(nums[2:] + nums[:2])
print(nums)
```

**6.8 The error collection**

Look back through this sheet. Write down every error name you met, which is the word before the colon in the message, what caused it, and one sentence in your own words about what Python was telling you. Which error did you meet most often? Then write one short snippet that causes each of the errors, swap snippets with a neighbour, and predict the error before you run theirs.

```python exec
id: puzzles-and-patterns-8
# your code here
```
