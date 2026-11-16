---
title: "Experiments with loops: round and round"
year: "2026-2027"
version: 2026.11.16.1
---

# Experiments with loops: round and round

A loop asks Python to repeat a block of code. Python has two kinds, the for loop and the while loop. Run each cell, predict what it will print, and then change one thing at a time to see what moves. Some snippets are meant to fail, and some are meant to run forever. Where a cell could run forever, it carries a guard that stops it, so the page stays alive.

## 1. The for loop

**1.1** Run this and watch what happens on each pass.

```python exec
id: the-for-loop-1
colours = ["red", "green", "blue"]
for colour in colours:
    print(colour)
```

We call each pass through the loop an iteration. How many iterations happen? What value does `colour` hold at the start of each one?

**1.2** Rename `colour` to `banana`, then to `x`. Does Python mind? What does this tell you about the name after the word `for`?

```python exec
id: the-for-loop-2
colours = ["red", "green", "blue"]
for colour in colours:
    print(colour)
# your code here
```

**1.3** Indentation tells Python what sits inside the loop. Try each version and describe what changes.

```python exec
id: the-for-loop-3
colours = ["red", "green", "blue"]
for colour in colours:
    print(colour)
    print("pass complete")
```

```python exec
id: the-for-loop-4
colours = ["red", "green", "blue"]
for colour in colours:
    print(colour)
print("pass complete")
```

Then remove the indent from the line inside the loop and read the error.

**1.4** Remove the colon at the end of the `for` line and run it. Put the colon back and delete the word `in` instead. Which message points closer to the real problem?

```python exec
id: the-for-loop-5
colours = ["red", "green", "blue"]
for colour in colours:
    print(colour)
# your code here
```

**1.5** After the loop ends, print `colour`. What does it hold?

```python exec
id: the-for-loop-6
colours = ["red", "green", "blue"]
for colour in colours:
    print(colour)
# your code here
```

**1.6** Loop over an empty list, `[]`, with a print inside the loop. Does an error appear? Does anything print?

```python exec
id: the-for-loop-7
# your code here
```

```solution
for: the-for-loop-7
title: one way to do it
for item in []:
    print("this never prints")
print("done")
```

**1.7** Loop over the string `"python"` with `for letter in "python":` and print each letter. What does this suggest about how Python sees a string?

```python exec
id: the-for-loop-8
# your code here
```

```solution
for: the-for-loop-8
title: one way to do it
for letter in "python":
    print(letter)
```

**1.8** Loop over `["a", 1, True, 2.5]` and print `type(item)` on each pass. Does a loop care what kind of thing it meets?

```python exec
id: the-for-loop-9
# your code here
```

```solution
for: the-for-loop-9
title: one way to do it
for item in ["a", 1, True, 2.5]:
    print(type(item))
```

**1.9** Predict what this prints, then run it.

```python exec
id: the-for-loop-10
colours = ["red", "green", "blue"]
position = 1
for colour in colours:
    print(position, colour)
    position = position + 1
```

What happens if you move `position = 1` inside the loop?

## 2. Counting with range

**2.1** Run this, and then change the number inside `range`.

```python exec
id: counting-with-range-1
for i in range(5):
    print(i)
```

Does the loop start at 0 or at 1? Does it include 5?

**2.2** The function `range` accepts one, two or three numbers. Use each of these as a loop header and predict the output before you run it: `range(2, 7)`, `range(0, 10, 2)`, `range(10, 0, -1)`, `range(10, 0, -3)`, `range(5, 5)`, `range(5, 2)` and `range(0)`. Which ones print nothing, and why?

```python exec
id: counting-with-range-2
# your code here
```

```solution
for: counting-with-range-2
title: one way to do it
print(list(range(2, 7)))
print(list(range(0, 10, 2)))
print(list(range(10, 0, -1)))
print(list(range(10, 0, -3)))
print(list(range(5, 5)))
print(list(range(5, 2)))
print(list(range(0)))
---
The last three give an empty list, so a loop over them prints nothing. A range stops before its end value, and it does not count backwards unless the step is negative.
```

**2.3** Give `range` a decimal with `range(2.5)` and read the error. Then try `range("5")`.

```python exec
id: counting-with-range-3
# your code here
```

**2.4** Print `range(5)` itself, without a loop. Then print `list(range(5))`. What does `list` do to a range?

```python exec
id: counting-with-range-4
# your code here
```

```solution
for: counting-with-range-4
title: one way to do it
print(range(5))
print(list(range(5)))
```

**2.5** Print a countdown from 10 to 1 and then print `Go!` after the loop. Do it twice, once with a negative step and once with an ordinary `range` and some arithmetic inside the loop.

```python exec
id: counting-with-range-5
# your code here
```

```solution
for: counting-with-range-5
title: one way to do it
for i in range(10, 0, -1):
    print(i)
print("Go!")
for i in range(10):
    print(10 - i)
print("Go!")
```

**2.6** Print the first ten multiples of 7 using the step alone, with no multiplication. Then print them again using multiplication.

```python exec
id: counting-with-range-6
# your code here
```

```solution
for: counting-with-range-6
title: one way to do it
for n in range(7, 71, 7):
    print(n)
for i in range(1, 11):
    print(i * 7)
```

**2.7** Print the first twelve square numbers. Then change one line so that the loop prints cubes instead.

```python exec
id: counting-with-range-7
# your code here
```

```solution
for: counting-with-range-7
title: one way to do it
for n in range(1, 13):
    print(n * n)
for n in range(1, 13):
    print(n * n * n)
```

## 3. Looping by position

**3.1** The function `len` gives the length of a list. Run this.

```python exec
id: looping-by-position-1
colours = ["red", "green", "blue"]
for i in range(len(colours)):
    print(i, colours[i])
```

What does `i` hold on each pass? How does this differ from looping over the items directly?

**3.2** Change `range(len(colours))` to `range(len(colours) + 1)` and read the error. Then try `range(1, len(colours))`. Which item goes missing?

```python exec
id: looping-by-position-2
colours = ["red", "green", "blue"]
# your code here
```

**3.3** Print the items in reverse order. Find one way that uses `range` with a negative step, and another way that uses a slice.

```python exec
id: looping-by-position-3
colours = ["red", "green", "blue"]
# your code here
```

```solution
for: looping-by-position-3
title: one way to do it
colours = ["red", "green", "blue"]
for i in range(len(colours) - 1, -1, -1):
    print(colours[i])
for colour in colours[::-1]:
    print(colour)
```

**3.4** Print only the items at even positions. Find two different ways to do it.

```python exec
id: looping-by-position-4
colours = ["red", "green", "blue"]
# your code here
```

```solution
for: looping-by-position-4
title: one way to do it
colours = ["red", "green", "blue"]
for i in range(0, len(colours), 2):
    print(colours[i])
for colour in colours[::2]:
    print(colour)
```

**3.5** Here we try to double every number in a list. Predict the result, then run it.

```python exec
id: looping-by-position-5
nums = [1, 2, 3]
for n in nums:
    n = n * 2
print(nums)
```

The list did not change. Now try this version and compare.

```python exec
id: looping-by-position-6
nums = [1, 2, 3]
for i in range(len(nums)):
    nums[i] = nums[i] * 2
print(nums)
```

Why did the second loop succeed where the first one failed?

**3.6** Predict what this prints, then run it.

```python exec
id: looping-by-position-7
nums = [2, 4, 6, 8]
for n in nums:
    if n % 2 == 0:
        nums.remove(n)
print(nums)
```

Every number is even, so how many items should remain once each one has been removed? Print `n` and `nums` on every pass to find out what goes on. Then find a safer way to get the result you wanted.

```solution
for: looping-by-position-7
title: one way to do it
nums = [2, 4, 6, 8]
for n in nums[:]:
    if n % 2 == 0:
        nums.remove(n)
print(nums)
nums = [2, 4, 6, 8]
kept = []
for n in nums:
    if n % 2 != 0:
        kept.append(n)
print(kept)
---
Removing from a list while looping over it skips items. Loop over a copy, or build a new list.
```

**3.7** Compare two lists position by position.

```python exec
id: looping-by-position-8
a = [3, 8, 2, 9]
b = [3, 5, 2, 7]
```

Print the positions where the two lists hold the same value. Then print the positions where they differ.

```solution
for: looping-by-position-8
title: one way to do it
a = [3, 8, 2, 9]
b = [3, 5, 2, 7]
for i in range(len(a)):
    if a[i] == b[i]:
        print("same at", i)
for i in range(len(a)):
    if a[i] != b[i]:
        print("different at", i)
```

## 4. Keeping a running tally

A variable that collects an answer while a loop runs is called an accumulator.

**4.1** Run this, and then print `total` inside the loop as well, indented, to watch it grow.

```python exec
id: keeping-a-running-tally-1
nums = [4, 8, 15, 16, 23, 42]
total = 0
for n in nums:
    total = total + n
print(total)
```

**4.2** Break it three ways. First delete the line `total = 0`. Then move `total = 0` inside the loop. Then change the starting value to 100. What happens each time, and why?

```python exec
id: keeping-a-running-tally-2
nums = [4, 8, 15, 16, 23, 42]
total = 0
for n in nums:
    total = total + n
print(total)
# your code here
```

**4.3** Count how many numbers in `nums` are greater than 10. Use an if statement inside the loop and a counter that starts at 0.

```python exec
id: keeping-a-running-tally-3
nums = [4, 8, 15, 16, 23, 42]
# your code here
```

```solution
for: keeping-a-running-tally-3
title: one way to do it
nums = [4, 8, 15, 16, 23, 42]
count = 0
for n in nums:
    if n > 10:
        count = count + 1
print(count)
```

**4.4** Multiply all the numbers in a list together. What should the starting value be? Try 0 first and see what happens, and then try 1.

```python exec
id: keeping-a-running-tally-4
# your code here
```

```solution
for: keeping-a-running-tally-4
title: one way to do it
nums = [2, 3, 4]
product = 1
for n in nums:
    product = product * n
print(product)
---
A product starts at 1, because starting at 0 makes every product 0.
```

**4.5** Find the largest number in a list without using `max`. Keep a variable called `biggest` and update it whenever you meet something larger. What should `biggest` start as? Test your loop on `[-5, -2, -9]`. Does a start of 0 survive?

```python exec
id: keeping-a-running-tally-5
# your code here
```

```solution
for: keeping-a-running-tally-5
title: one way to do it
nums = [-5, -2, -9]
biggest = nums[0]
for n in nums:
    if n > biggest:
        biggest = n
print(biggest)
---
Starting from the first item works for any list. Starting at 0 fails when every number is negative.
```

**4.6** Build a new list. Start with `evens = []` and append each even number from `range(20)`. Print `evens` after the loop. What happens if you put the print inside the loop?

```python exec
id: keeping-a-running-tally-6
# your code here
```

```solution
for: keeping-a-running-tally-6
title: one way to do it
evens = []
for n in range(20):
    if n % 2 == 0:
        evens.append(n)
print(evens)
```

**4.7** Build a string. Start with `word = ""` and add each letter of `"python"` on each pass. Compare what you get from `word = word + letter` with what you get from `word = letter + word`.

```python exec
id: keeping-a-running-tally-7
# your code here
```

```solution
for: keeping-a-running-tally-7
title: one way to do it
forward = ""
backward = ""
for letter in "python":
    forward = forward + letter
    backward = letter + backward
print(forward, backward)
```

**4.8** Ask the user for five numbers with `input`, using a loop, and print their average. Where does `int` need to appear?

```python exec
id: keeping-a-running-tally-8
# your code here
```

## 5. The while loop

A while loop repeats for as long as its condition stays true.

**5.1** Predict what this prints, then run it.

```python exec
id: the-while-loop-1
count = 3
while count > 0:
    print(count)
    count = count - 1
print("Liftoff")
```

**5.2** Change `>` to `>=`. Then change the starting value to 0, and then to -2. For each version, say how many times the body will run before you run it.

```python exec
id: the-while-loop-2
count = 3
while count > 0:
    print(count)
    count = count - 1
print("Liftoff")
# your code here
```

**5.3** Delete the line `count = count - 1` and run the cell. Without it nothing changes the condition, so the loop would never finish. The variable `passes` is a guard that stops it after ten passes. What does the guard do?

```python exec
id: the-while-loop-3
count = 3
passes = 0
while count > 0 and passes < 10:
    print(count)
    count = count - 1
    passes = passes + 1
print("Liftoff")
```

**5.4** Run this guessing loop, and then try to get past it.

```python exec
id: the-while-loop-4
secret = "python"
guess = ""
while guess != secret:
    guess = input("Password? ")
print("Welcome in")
```

```typed
wrong
python
```

Why do we set `guess = ""` before the loop? Delete that line and read the error. Then change it to `guess = "python"` and predict what happens.

**5.5** The loop `while True:` runs until something inside it says `break`. Try this.

```python exec
id: the-while-loop-5
while True:
    answer = input("Type quit to leave: ")
    if answer == "quit":
        break
    print("You typed", answer)
print("Bye")
```

```typed
hello
quit
```

What happens if you type `QUIT`? Strings have a method called `lower`, so try `"HeLLo".lower()` first, and then let people leave in capitals as well.

**5.6** The word `continue` skips to the next pass. Run this and describe what it does.

```python exec
id: the-while-loop-6
for n in range(1, 11):
    if n % 3 == 0:
        continue
    print(n)
```

Now swap `continue` for `break`. What changes?

**5.7** Loop through `[4, 9, 2, 15, 8, 20]` and stop at the first number greater than 10, printing that number. Then change the list so that no number qualifies, and make your program print `none found` in that case.

```python exec
id: the-while-loop-7
# your code here
```

```solution
for: the-while-loop-7
title: one way to do it
nums = [4, 9, 2, 15, 8, 20]
found = False
for n in nums:
    if n > 10:
        print(n)
        found = True
        break
if not found:
    print("none found")
```

**5.8** The operator `//` divides and drops the remainder, so try `7 // 2` first. Start with 100 and keep halving with `//` until you reach 0, printing each value. How many steps does it take?

```python exec
id: the-while-loop-8
# your code here
```

```solution
for: the-while-loop-8
title: one way to do it
n = 100
steps = 0
while n > 0:
    print(n)
    n = n // 2
    steps = steps + 1
print(steps, "steps")
```

**5.9** Put one grain of rice on the first square of a chessboard and double the number of grains on each square after that. On which square does the count first pass a million?

```python exec
id: the-while-loop-9
# your code here
```

```solution
for: the-while-loop-9
title: one way to do it
grains = 1
square = 1
while grains <= 1000000:
    grains = grains * 2
    square = square + 1
print(square, grains)
```

## 6. Loops inside loops

**6.1** Predict what this prints, then run it. The `end=""` tells `print` to stay on the same line instead of starting a new one.

```python exec
id: loops-inside-loops-1
for row in range(3):
    for col in range(4):
        print("*", end="")
    print()
```

Change the 3 and the 4. Which number controls the height, and which controls the width? Delete the lone `print()` and see what happens. Then indent it one level further and see what happens.

**6.2** Print a square of `#` characters, five by five.

```python exec
id: loops-inside-loops-2
# your code here
```

```solution
for: loops-inside-loops-2
title: one way to do it
for row in range(5):
    for col in range(5):
        print("#", end="")
    print()
```

**6.3** Print this triangle with two loops. Then print it again with one loop, using the fact that `"*" * 3` gives `***`.

```
*
**
***
****
*****
```

```python exec
id: loops-inside-loops-3
# your code here
```

```solution
for: loops-inside-loops-3
title: one way to do it
for row in range(1, 6):
    for col in range(row):
        print("*", end="")
    print()
for row in range(1, 6):
    print("*" * row)
```

**6.4** Flip the triangle so that it counts down from five stars to one.

```python exec
id: loops-inside-loops-4
# your code here
```

```solution
for: loops-inside-loops-4
title: one way to do it
for row in range(5, 0, -1):
    print("*" * row)
```

**6.5** Print this pattern, where row `n` holds the digit `n` repeated `n` times. The function `str` will help.

```
1
22
333
4444
```

```python exec
id: loops-inside-loops-5
# your code here
```

```solution
for: loops-inside-loops-5
title: one way to do it
for n in range(1, 5):
    print(str(n) * n)
```

**6.6** Print a times table by using `print(i * j, end=" ")` inside a nested loop, with `i` and `j` running from 1 to 5. The columns will not line up. Why not? Can you use an if statement to fix it?

```python exec
id: loops-inside-loops-6
# your code here
```

```solution
for: loops-inside-loops-6
title: one way to do it
for i in range(1, 6):
    for j in range(1, 6):
        product = i * j
        if product < 10:
            print(" ", end="")
        print(product, end=" ")
    print()
```

**6.7** Run this checkerboard, and then explain why `(row + col) % 2` produces a pattern.

```python exec
id: loops-inside-loops-7
for row in range(6):
    for col in range(6):
        if (row + col) % 2 == 0:
            print("#", end="")
        else:
            print(".", end="")
    print()
```

Change the 6 to other numbers, change the characters, and change `== 0` to `== 1`.

**6.8** Run this pyramid, and work out how the spaces and the stars change from one row to the next.

```python exec
id: loops-inside-loops-8
for row in range(5):
    print(" " * (4 - row) + "*" * (2 * row + 1))
```

Flip it upside down. Then try to build a diamond from the two halves.

```solution
for: loops-inside-loops-8
title: one way to do it
for row in range(5):
    print(" " * (4 - row) + "*" * (2 * row + 1))
for row in range(3, -1, -1):
    print(" " * (4 - row) + "*" * (2 * row + 1))
```

**6.9** How many times does the innermost line run in a loop of 4 by 5? How many times does it run with three nested loops of 3, 4 and 5? Predict first, and then check with a counter variable.

```python exec
id: loops-inside-loops-9
# your code here
```

```solution
for: loops-inside-loops-9
title: one way to do it
count = 0
for a in range(4):
    for b in range(5):
        count = count + 1
print(count)
count = 0
for a in range(3):
    for b in range(4):
        for c in range(5):
            count = count + 1
print(count)
```

**6.10** Roll two dice. Print every pair of values from 1 to 6 whose total is 7, and count the pairs with a counter.

```python exec
id: loops-inside-loops-10
# your code here
```

```solution
for: loops-inside-loops-10
title: one way to do it
pairs = 0
for first in range(1, 7):
    for second in range(1, 7):
        if first + second == 7:
            print(first, second)
            pairs = pairs + 1
print(pairs, "pairs")
```

## 7. Puzzles

**7.1 FizzBuzz**

Count from 1 to 30. Print `Fizz` instead of the number for multiples of 3, `Buzz` for multiples of 5, and `FizzBuzz` for multiples of both. The operator `%` gives the remainder after a division, so `n % 3 == 0` asks whether `n` is a multiple of 3. Put the test for both last and see what goes wrong. What order do your tests need?

```python exec
id: puzzles-1
# your code here
```

```solution
for: puzzles-1
title: one way to do it
for n in range(1, 31):
    if n % 15 == 0:
        print("FizzBuzz")
    elif n % 3 == 0:
        print("Fizz")
    elif n % 5 == 0:
        print("Buzz")
    else:
        print(n)
---
Test for both first. A multiple of 15 is also a multiple of 3, so a test for 3 placed earlier catches it too soon.
```

**7.2 Collatz**

Pick a positive whole number. If it is even, halve it with `//`. If it is odd, triple it and add one. Keep going until you reach 1, and print each value along the way. Now count the steps. Which starting number below 30 takes the most steps? Nobody has found a starting number that fails to reach 1, but nobody has proved that none exists either.

```python exec
id: puzzles-2
# your code here
```

```solution
for: puzzles-2
title: one way to do it
best_start = 1
best_steps = 0
for start in range(1, 30):
    n = start
    steps = 0
    while n != 1:
        if n % 2 == 0:
            n = n // 2
        else:
            n = 3 * n + 1
        steps = steps + 1
    if steps > best_steps:
        best_steps = steps
        best_start = start
print(best_start, best_steps)
```

**7.3 Digit detective**

Add up the digits of a number with a while loop. Use `% 10` to read the last digit and `// 10` to drop it. Test your loop on 2024. Then find every number from 1 to 100 whose digits add up to 10.

```python exec
id: puzzles-3
# your code here
```

```solution
for: puzzles-3
title: one way to do it
n = 2024
total = 0
while n > 0:
    total = total + n % 10
    n = n // 10
print(total)
for number in range(1, 101):
    digit_sum = 0
    rest = number
    while rest > 0:
        digit_sum = digit_sum + rest % 10
        rest = rest // 10
    if digit_sum == 10:
        print(number)
```

**7.4 Primes**

A prime number is greater than 1 and has no divisors other than 1 and itself. Print all the primes below 50. You might use a nested loop, a variable called `is_prime` that starts as `True`, and a change to `False` whenever you find a divisor.

```python exec
id: puzzles-4
# your code here
```

```solution
for: puzzles-4
title: one way to do it
for n in range(2, 50):
    is_prime = True
    for d in range(2, n):
        if n % d == 0:
            is_prime = False
    if is_prime:
        print(n)
```

**7.5 Guess my number**

Choose a secret number in your code. Ask the player for guesses with `input`, and answer `too high`, `too low` or `correct`. Count the guesses and report the total at the end. Then add a limit of seven guesses.

```python exec
id: puzzles-5
# your code here
```

**7.6 Predict the output**

Write down your prediction for each program before you run it.

```python exec
id: puzzles-6
x = 1
for i in range(5):
    x = x * 2
    if x > 10:
        break
    print(x)
print("x ends as", x)
```

```python exec
id: puzzles-7
total = 0
for a in range(1, 4):
    for b in range(1, 4):
        if a == b:
            continue
        total = total + a * b
print(total)
```

**7.7 Spot the bug**

Each snippet has one bug. Say what each one is meant to do, run it, find the bug and fix it. The first one would run forever, so it carries a guard that stops it after twelve passes.

```python exec
id: puzzles-8
n = 10
passes = 0
while n > 0 and passes < 12:
    if n % 2 == 0:
        n = n - 1
    print(n)
    passes = passes + 1
```

```python exec
id: puzzles-9
# meant to print 1 to 5
for i in range(1, 5):
    print(i)
```

```python exec
id: puzzles-10
# meant to print the total of 4, 8 and 15
for n in [4, 8, 15]:
    total = 0
    total = total + n
print(total)
```

**7.8 Invent your own**

Write a loop puzzle for a neighbour. It can be a pattern to print or a short program with one planted bug. Swap, solve, and then compare your fixes.

```python exec
id: puzzles-11
# your code here
```
