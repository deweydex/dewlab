---
title: "A function that calls itself: recursion — Practice"
practice_for: a-function-that-calls-itself
year: "2026-2027"
version: 2026.09.25.1
---

# A function that calls itself: recursion — Practice

Each answer is hidden until you open it. Each one is one answer.
Yours may be different and work too. Where a problem asks you to predict,
the prediction is the exercise, so make one before you run anything.

Your toolkit is loaded on this page, so `count_items` is ready to use,
and so are `factorial`, `total` and the rest.

## Warm-up

Use this cell for any of the warm-up problems.

```python exec
id: calls-itself-practice-scratch-1
print(count_items([["a", "b"], "c"]))
```

**1. Predict.** A rocket launch counts down. What does
`countdown(3)` print, line by line?

```python
def countdown(seconds):
    """Count down from seconds to 0, then launch."""
    if seconds == 0:
        print("Lift off!")
        return
    print(seconds)
    countdown(seconds - 1)
```

<details class="dl-answer"><summary>answer</summary>

```text
3
2
1
Lift off!
```

The call for 3 prints 3, then calls `countdown(2)`, which prints 2 and
calls `countdown(1)`. That prints 1 and calls `countdown(0)`, which is
the base case. It prints "Lift off!" and makes no more calls. The
`return` with nothing after it ends the call and returns `None`.

</details>

**2. Predict.** You pack a bag for a trip. It has a pouch with your
passport and tickets, a pouch with a charger, and a book loose in the
bag. What do these two lines print?

```python
bag = [["passport", "tickets"], ["charger"], "book"]
print(len(bag))
print(count_items(bag))
```

<details class="dl-answer"><summary>answer</summary>

It prints `3`, then `4`.

`len` counts what is directly inside the bag: two pouches and a book.
`count_items` looks inside every pouch, and counts the things
themselves: passport, tickets, charger and book.

</details>

**3. Explain.** In `countdown` from problem 1, which lines are the base
case, and which are the recursive case? Why does the countdown always
reach its base case, for any whole number from 0 up?

<details class="dl-answer"><summary>answer</summary>

The base case is the `if seconds == 0:` branch. It prints "Lift off!"
and makes no more calls. The recursive case is the last two lines: print
the number, then hand `seconds - 1` to the same function.

Each call hands on a number one smaller. Starting from a whole number,
0 or more, the numbers go down one at a time, so they must land on 0.
That is the second rule for a recursion that ends: every call is a step
closer to the base case.

</details>

**4. Make.** A music app keeps playlists as folders. "Chill" has three
songs. "Workout" has two songs and a folder of two remixes. One song
sits outside every playlist. Use `count_items` to count every song.

```python
playlists = [
    ["Holocene", "Re: Stacks", "Skinny Love"],                          # Chill
    ["Titanium", "Levels", ["Levels (remix)", "Titanium (remix)"]],     # Workout
    "Song of the day",
]
```

<details class="dl-answer"><summary>answer</summary>

```python
print(count_items(playlists))    # 8
```

There are three in "Chill", four in "Workout" with its remixes, and
one on its own, so 8 songs. The playlists' names are in comments, not in the lists,
so they are not counted as songs.

</details>

## Core

Use this cell for the core problems.

```python exec
id: calls-itself-practice-scratch-2
# Use this cell for the core problems
```

**5. Make.** A power is a product of the same number, again and again.
In words, $b$ to the power $e$ is $b$ times $b$ to the power $e - 1$,
and any number to the power 0 is 1:

$$b^e = b \times b^{e-1}, \qquad b^0 = 1$$

Write `power(base, exponent)` as a recursive function, for whole-number
exponents from 0 up. An internet address of the older kind, called
IPv4, is 32 bits long. Use `power` to find how many different addresses
32 bits can make, and check against Python's `**`.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The base case: when `exponent == 0`, return 1.
2. The recursive case: return `base` times `power(base, exponent - 1)`.
3. Each bit doubles the number of patterns, as on
   [Everything is ones and zeros](tutorial:everything-is-ones-and-zeros),
   so 32 bits make `power(2, 32)`.

**Think about:** why does the base case return 1, and not 0 or `base`?

**Try this next:** how many calls does `power(2, 32)` make?

</details>

<details class="dl-answer"><summary>answer</summary>

```python
def power(base, exponent):
    """Give back base to the power exponent. exponent is a whole number, 0 or more."""
    if exponent == 0:
        return 1
    return base * power(base, exponent - 1)

print(power(2, 10))    # 1024
print(power(2, 32))    # 4294967296
print(2 ** 32)         # 4294967296
```

32 bits make 4,294,967,296 addresses, about 4.3 billion. That is fewer
than the number of people on Earth, which is one reason a newer kind of
address, IPv6, uses 128 bits. The base case returns 1 because
multiplying by 1 changes nothing, the same reason a running product
starts at 1 on [Doing it again](tutorial:doing-it-again).

</details>

**6. Fix.** A website has a menu, and some menu items open smaller
menus of their own. Schlomo, who is learning Python too, writes a
function to count the pages the menu leads to. He copied the shape of
`count_items`. There are 6 pages, and his
function says 1. Find the line that loses the rest.

```python exec
id: calls-itself-practice-fix-menu
menu = [
    ["Timetable", "Maps"],                    # Travel
    ["Courses", ["Python", "Maths"]],         # Learn, with a smaller menu of subjects
    "Contact",
]

def count_pages(nested):
    """Count the pages in nested, at any depth."""
    found = 0
    for item in nested:
        if isinstance(item, list):
            count_pages(item)
        else:
            found = found + 1
    return found

print(count_pages(menu))    # there are 6 pages
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Which items does the top call count itself? Only "Contact".
2. For each smaller menu, it calls `count_pages(item)`. What does it do
   with the number that call returns?
3. A call returns its answer to the line that made it. If that line
   does nothing with it, the answer is lost.

**Think about:** each call has its own `found`. Does adding to the
inner call's `found` change the outer one?

**Try this next:** change the function to count the menus instead.

</details>

<details class="dl-answer"><summary>answer</summary>

The line `count_pages(item)` makes the call, but loses its
answer. Each call has its own `found`, in its own space, so the inner
calls' counts never reach the top. The line needs to add the answer:

```python
        if isinstance(item, list):
            found = found + count_pages(item)
```

Now it prints 6. Schlomo is not alone here. A call that is made, and
whose answer is never used, is one of the most common slips in
recursion.

</details>

**7. Fix.** Before a game of tag, a child counts down in twos: 5, 3,
1, Go! This version never says "Go!". The cell is meant to fail. Left
alone, it would print about a thousand numbers before Python stopped
it, so we added a check. It stops with a `RecursionError` once the
count goes below −10. The numbers it prints are the clue. Find the
line that lets the count continue, and change it.

```python exec
id: calls-itself-practice-fix-twos
def count_in_twos(number):
    """Count down in twos from number, then say Go!"""
    if number < -10:  # a safety net, so the cell stops early
        raise RecursionError("the count went below -10 and never said Go!")
    if number == 0:
        print("Go!")
        return
    print(number)
    count_in_twos(number - 2)

count_in_twos(5)
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Write down `number` for each call: 5, 3, 1, then what?
2. Does `number` ever equal 0?
3. The base case should catch every number where the count is over.

**Think about:** would this version work if it started from 6?

**Try this next:** what should `count_in_twos(0)` do?

</details>

<details class="dl-answer"><summary>answer</summary>

`number` goes 5, 3, 1, −1, −3, and steps over 0. The base case is
never reached. The fix is to stop at 0 or below:

```python
    if number <= 0:
```

Now it prints 5, 3, 1 and "Go!". Starting from 6, the old version
worked, since 6, 4, 2, 0 lands on 0. A base case that catches only one
number is fragile when the steps are bigger than 1.

</details>

**8. Predict.** A lighthouse has stairs. This function walks down them,
then back up. What does `stairs(3)` print? Write all the lines before
you run it.

```python
def stairs(step):
    """Walk down from step to the ground, then back up."""
    if step == 0:
        print("ground floor")
        return
    print("down to", step - 1)
    stairs(step - 1)
    print("back up to", step)
```

<details class="dl-answer"><summary>answer</summary>

```text
down to 2
down to 1
down to 0
ground floor
back up to 1
back up to 2
back up to 3
```

Each call prints its "down" line, then waits while the call it made
runs. Only when that call has finished does it print its "back up"
line. So the "back up" lines come out in the opposite order: the last
call to start is the first to finish. That is the call stack at work.

</details>

**9. Make.** A zip file can hold files, and other zip files, and
those can hold zip files too. Here is one, as a nested list of the
sizes of the files inside it, in kilobytes (KB). Write
`sum_nested(nested)`, which adds up every size, at any depth. It has
the same shape as `count_items`. How many kilobytes are inside?

```python
archive = [450, [220, 110, [80, 80]], [1200], 325]
```

<details class="dl-answer"><summary>answer</summary>

```python
def sum_nested(nested):
    """Add up every number inside nested, a list that may hold lists, at any depth."""
    running = 0
    for item in nested:
        if isinstance(item, list):
            running = running + sum_nested(item)
        else:
            running = running + item
    return running

print(sum_nested(archive))    # 2465
```

There are 2,465 KB inside. Only one thing changed from `count_items`: a file adds its
own size, where a photo added 1. The running name is `running`, not
`total`, so the toolkit's `total` stays available.

</details>

**10. Another way.** Add up the same archive without recursion, with a
loop and a to-do list of zip files not yet opened, as in the last
section of the page. Do you get the same answer?

<details class="dl-answer"><summary>answer</summary>

```python
def sum_nested_by_loop(nested):
    """Add up every number inside nested, at any depth, with a to-do list."""
    running = 0
    to_open = [nested]
    while len(to_open) > 0:
        inner = to_open.pop()
        for item in inner:
            if isinstance(item, list):
                to_open.append(item)
            else:
                running = running + item
    return running

print(sum_nested_by_loop(archive))    # 2465
```

Yes, it gives the same 2,465 KB. The loop opens the zip files in a
different order from the recursion, but the order does not change a sum, so the sum
is the same.

</details>

**11. Explain.** `factorial_again(-1)` and `factorial_again(2.5)` both
stop with a `RecursionError`. Why? Schlomi, who is learning Python
too, suggests changing the base case to `if n <= 0: return 1`, so that
they give an answer. What would her change do?

<details class="dl-answer"><summary>answer</summary>

From −1, `n` goes −2, −3, −4, away from 0. From 2.5, it goes 1.5, 0.5,
−0.5, and steps over 0. Neither ever reaches the base case, so the calls
grow until Python's limit stops them.

Schlomi's change does stop the error. But then it quietly gives answers
that mean nothing. `factorial_again(2.5)` would give $2.5 \times 1.5 \times 0.5 =
1.875$, which is not a factorial of anything. The inputs are outside the
promise's domain, whole numbers from 0 up. A clearer fix checks the
domain at the top, as on
[Machines that take a number](tutorial:machines-that-take-a-number#what-goes-in-and-what-comes-out):

```python
assert n >= 0 and n == int(n), "n must be a whole number, 0 or more"
```

An error with a message says what happened.

</details>

**12. Predict.** How many times is `count_items` called, in all, when
you run `count_items(holidays)` on the "Holidays" folder from the page?
Use the folder below.

```python
holidays = [
    "sunset.jpg",
    ["kerry-1.jpg", "kerry-2.jpg", "kerry-3.jpg"],
    "cake.jpg",
    ["paris-1.jpg", ["louvre-1.jpg", "louvre-2.jpg"], "paris-2.jpg"],
]
```

<details class="dl-answer"><summary>answer</summary>

It is called 4 times: once for "Holidays" itself, and one for each folder inside it,
"kerry", "paris" and "louvre". A photo never makes a call. So the number
of calls is 1 more than the number of folders, however many photos
there are.

</details>

## Stretch

Use this cell for the stretch problems.

```python exec
id: calls-itself-practice-scratch-3
# Use this cell for the stretch problems
```

**13. Make.** A set of Russian dolls has a doll inside a doll inside a
doll. As a nested list, the smallest doll is inside five lists. Write
`deepest(nested)`, which returns how many levels deep the deepest
list goes, counting `nested` itself as 1.

```python
dolls = [[[[["tiny doll"]]]]]
```

`deepest(dolls)` should be 5, `deepest([])` should be 1, and
`deepest(holidays)` should be 3.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Keep a name for the deepest list found inside so far, starting at 0.
2. For each item that is a list, find `deepest(item)`, and keep it if
   it is bigger. Python's `max(a, b)` gives the bigger of two numbers.
3. At the end, return 1 more than the deepest found inside, for the
   level of `nested` itself.

**Think about:** what is the base case? Which list makes no more calls?

**Try this next:** how deep does `library` from the page go?

</details>

<details class="dl-answer"><summary>answer</summary>

```python
def deepest(nested):
    """Give back how many levels deep nested goes, counting nested itself as 1."""
    deepest_inside = 0
    for item in nested:
        if isinstance(item, list):
            deepest_inside = max(deepest_inside, deepest(item))
    return 1 + deepest_inside

print(deepest(dolls), deepest([]), deepest(holidays))    # 5 1 3
```

A list with no lists inside is the base case. The loop makes no calls,
and the function returns 1.

</details>

**14. Another way.** On
[Finding things fast](tutorial:finding-things-fast), binary search
looked at the middle of a sorted list, then kept only the half that
could hold the target. That page called this divide and conquer.
Keeping half is the same search on a smaller problem, so binary search
can be written as a recursion. Finish this
version, which searches between the places `low` and `high`, and prints
each part it looks at. How many parts does it look at to find the last
of 1,000 ticket numbers?

```python
def binary_search_again(sorted_values, target, low, high):
    """Give back the place of target in sorted_values, between low and high, or -1."""
    if low > high:
        return -1
    middle = (low + high) // 2
    print("looking at", low, "to", high)
    if sorted_values[middle] == target:
        return middle
    # Your two recursive cases: the upper half, or the lower half


tickets = list(range(1000, 4000, 3))    # 1,000 ticket numbers, in order
print(binary_search_again(tickets, 3997, 0, len(tickets) - 1))
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. If the middle value is smaller than the target, the target can only
   be in the upper half, from `middle + 1` to `high`.
2. Otherwise it can only be in the lower half, from `low` to
   `middle - 1`.
3. In each case, return what the same function returns for that
   half.

**Think about:** what is the base case when the target is not there?

**Try this next:** search for 2000, which is not a ticket number.

</details>

<details class="dl-answer"><summary>answer</summary>

```python
    if sorted_values[middle] < target:
        return binary_search_again(sorted_values, target, middle + 1, high)
    return binary_search_again(sorted_values, target, low, middle - 1)
```

It looks at 10 parts, from "0 to 999" down to "999 to 999", and returns
999, the last place. $\log_2 1000$ is about 9.97, so about 10
halvings bring 1,000 places down to 1. Searching for 2000 also takes 10
looks, and returns −1. The part shrinks to nothing, and `low > high`
is the base case that says "not here".

</details>

**15. Predict.** In 1202, Fibonacci asked how rabbits breed. In his
puzzle, month 1 and month 2 have 1 pair each. After that, each month has
as many pairs as the two months before it added together. Here it is as
a recursion, with a second function that counts how many calls the
first one makes.

```python
def rabbits(month):
    """Give back the pairs of rabbits in month, in Fibonacci's puzzle."""
    if month <= 2:
        return 1
    return rabbits(month - 1) + rabbits(month - 2)


def rabbit_calls(month):
    """Give back how many calls rabbits(month) makes, counting itself."""
    if month <= 2:
        return 1
    return 1 + rabbit_calls(month - 1) + rabbit_calls(month - 2)
```

`rabbits(10)` is 55. Before you run anything, guess how many calls it
makes. Then run `rabbit_calls` for months 5, 10, 20 and 25.

<details class="dl-answer"><summary>answer</summary>

```python
for month in [5, 10, 20, 25]:
    print(month, rabbits(month), rabbit_calls(month))
```

```text
5 5 9
10 55 109
20 6765 13529
25 75025 150049
```

`rabbits(10)` makes 109 calls, and `rabbits(25)` makes 150,049. Each
call makes two more, and the two ask the same questions again.
`rabbits(8)` is calculated once for month 10, and again inside the call
for month 9. The page
[Making change: brute force, memoization and greedy algorithms](tutorial:three-ways-to-make-change)
shows how to remember an answer once it is calculated, so that it is
never calculated twice.

</details>

**16. Make.** Write `all_items(nested)`, which returns a new list of
every item in `nested`, at any depth, in order. For the music `library`
on the page, it should give the seven songs as one list.

```python
library = [
    [["Take Me to Church", "Cherry Wine"], ["Too Sweet", "Eat Your Young"]],  # Hozier
    [["Linger", "Dreams", "Zombie"]],                                        # The Cranberries
]
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Start with an empty list, `found = []`.
2. For an item that is not a list, `append` it to `found`.
3. For an item that is a list, `all_items(item)` returns a list.
   `found + that_list` joins two lists into one.

**Think about:** how could you check your answer with `count_items`?

**Try this next:** use `all_items` on `holidays`. Are the photos in the
order you would read them?

</details>

<details class="dl-answer"><summary>answer</summary>

```python
def all_items(nested):
    """Give back a new list of every item in nested, at any depth, in order."""
    found = []
    for item in nested:
        if isinstance(item, list):
            found = found + all_items(item)
        else:
            found.append(item)
    return found

songs = all_items(library)
print(songs)
print(len(songs) == count_items(library))    # True
```

The list is `['Take Me to Church', 'Cherry Wine', 'Too Sweet',
'Eat Your Young', 'Linger', 'Dreams', 'Zombie']`. Its length is 7, the
same as `count_items(library)`, which makes a useful test. Two routes give one
answer.

</details>

**17. Predict.** A recursion can draw as well as count. This cell
draws a tree. Each branch draws itself, then hands two shorter
branches, turned a little left and a little right, to the same
function. The two lines with `cos` and `sin` calculate where a branch
ends. A later unit explains them, and here you can read them as "go
this far in this direction". `depth` says how many more levels of
branches to draw, so `depth == 0` is the base case.

Before you run it, how many lines will a tree of depth 6 have? Then
change the 6 to 10 and predict again.

```python exec
id: calls-itself-practice-tree
import math
import matplotlib.pyplot as plt


def branch(x, y, angle, length, depth):
    """Draw a branch from (x, y), and two smaller branches from its tip.

    Give back how many lines were drawn, this branch and all below it.
    """
    if depth == 0:
        return 0
    tip_x = x + length * math.cos(math.radians(angle))
    tip_y = y + length * math.sin(math.radians(angle))
    plt.plot([x, tip_x], [y, tip_y], color="C2")
    left = branch(tip_x, tip_y, angle + 25, length * 0.7, depth - 1)
    right = branch(tip_x, tip_y, angle - 25, length * 0.7, depth - 1)
    return 1 + left + right


print(branch(0, 0, 90, 1, 6), "lines")
plt.axis("equal")
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Depth 1 draws one line, the trunk, and makes two calls with depth 0,
   which draw nothing.
2. Depth 2 draws its trunk, and two trees of depth 1.
3. Write the counts for depth 1, 2 and 3. What pattern do you see?

**Think about:** how many lines are at the very tips of the tree,
compared with all the lines below them?

</details>

<details class="dl-answer"><summary>answer</summary>

Depth 6 draws 63 lines, and depth 10 draws 1,023. Each level has twice
as many branches as the one before: 1, 2, 4, 8, 16 and 32 for depth 6.
Together that is $2^6 - 1 = 63$, one less than a power of 2, which is
the chessboard's pattern from the next page,
[Doubling and halving](tutorial:doubling-and-halving#grains-on-a-chessboard).
A shape made of smaller copies of itself, like this tree, is called a
*fractal*. Ferns, rivers and coastlines have shapes a little like it, and
programs draw trees and mountains in games this way.

</details>
