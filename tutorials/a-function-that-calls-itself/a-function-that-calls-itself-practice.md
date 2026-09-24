---
title: "A function that calls itself: recursion — Practice"
practice_for: a-function-that-calls-itself
year: "2026-2027"
version: 2026.09.24.1
---

# A function that calls itself: recursion — Practice

Each answer is hidden until you open it. Where a problem asks you to
predict, the prediction is the exercise, so make one before you run
anything.

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
the base case: it prints "Lift off!" and makes no more calls. The
`return` with nothing after it ends the call and gives back `None`.

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

`3`, then `4`.

`len` counts what is directly inside the bag: two pouches and a book.
`count_items` looks inside every pouch, and counts the things
themselves: passport, tickets, charger and book.

</details>

**3. Explain.** In `countdown` from problem 1, which lines are the base
case, and which are the recursive case? Why does the countdown always
reach its base case, for any whole number from 0 up?

<details class="dl-answer"><summary>answer</summary>

The base case is the `if seconds == 0:` branch: it prints "Lift off!"
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

Three in "Chill", four in "Workout" with its remixes, and one on its
own: 8 songs. The playlists' names are in comments, not in the lists,
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
exponents from 0 up. Use it to find what €1,000 grows to in 10 years at
5% a year, and check against Python's `**`.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The base case: when `exponent == 0`, give back 1.
2. The recursive case: give back `base` times `power(base, exponent - 1)`.
3. €1,000 at 5% a year is multiplied by 1.05 each year, so after 10
   years it is `1000 * power(1.05, 10)`.

**Think about:** why does the base case give back 1, and not 0 or `base`?

**Try this next:** how many calls does `power(2, 10)` make?

</details>

<details class="dl-answer"><summary>answer</summary>

```python
def power(base, exponent):
    """Give back base to the power exponent. exponent is a whole number, 0 or more."""
    if exponent == 0:
        return 1
    return base * power(base, exponent - 1)

print(power(2, 10))                        # 1024
print(round(1000 * power(1.05, 10), 2))    # 1628.89
print(round(1000 * 1.05 ** 10, 2))         # 1628.89
```

€1,000 grows to €1,628.89. The base case gives back 1 because
multiplying by 1 changes nothing, the same reason a running product
starts at 1 on [Doing it again](tutorial:doing-it-again).

</details>

**6. Fix.** This function should count the recipes in a recipe book,
with sections inside sections. There are 6 recipes, and it says 1. Find
the one mistake.

```python exec
id: calls-itself-practice-fix-recipes
book = [
    ["Leek and potato", "Tomato"],            # Soups
    ["Soda bread", ["Brown", "White"]],       # Bread, with a section of yeast breads
    "Pancakes",
]

def count_recipes(nested):
    """Count the recipes in nested, at any depth."""
    found = 0
    for item in nested:
        if isinstance(item, list):
            count_recipes(item)
        else:
            found = found + 1
    return found

print(count_recipes(book))    # should be 6
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Which items does the top call count itself? Only "Pancakes".
2. For each section, it calls `count_recipes(item)`. What does it do
   with the number that call gives back?
3. A call gives its answer back to the line that made it. If that line
   does nothing with it, the answer is lost.

**Think about:** each call has its own `found`. Does adding to the
inner call's `found` change the outer one?

**Try this next:** change the function to count the sections instead.

</details>

<details class="dl-answer"><summary>answer</summary>

The line `count_recipes(item)` makes the call, but throws away its
answer. Each call has its own `found`, in its own space, so the inner
calls' counts never reach the top. The line must add the answer:

```python
        if isinstance(item, list):
            found = found + count_recipes(item)
```

Now it prints 6. This is the most common mistake in recursion: a call
that is made, and whose answer is never used.

</details>

**7. Fix.** Before a game of tag, a child counts down in twos: 5, 3,
1, Go! This version never says "Go!". The cell is meant to fail: it
prints a long column of numbers, then stops with a `RecursionError`.
The first few numbers are the clue. Find the mistake, and fix it.

```python exec
id: calls-itself-practice-fix-twos
def count_in_twos(number):
    """Count down in twos from number, then say Go!"""
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

`number` goes 5, 3, 1, −1, −3, and steps right over 0. The base case is
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

**9. Make.** An online shop keeps an order as a list of prices. A bag
inside the order is a list, and a bag can hold a smaller bag. Write
`sum_nested(nested)`, which adds up every price, at any depth. It has
the same shape as `count_items`. What does this order cost?

```python
order = [4.50, [2.20, 1.10, [0.80, 0.80]], [12.00], 3.25]
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

print(round(sum_nested(order), 2))    # 24.65
```

The order costs €24.65. Only one thing changed from `count_items`: a
price adds its own value, where a photo added 1. The running name is
`running`, not `total`, so the toolkit's `total` stays available.

</details>

**10. Another way.** Add up the same order without recursion, with a
loop and a to-do list of bags not yet opened, as in the last section of
the page. Do you get the same answer?

<details class="dl-answer"><summary>answer</summary>

```python
def sum_nested_by_loop(nested):
    """Add up every number inside nested, at any depth, with a to-do list."""
    running = 0
    to_open = [nested]
    while len(to_open) > 0:
        bag = to_open.pop()
        for item in bag:
            if isinstance(item, list):
                to_open.append(item)
            else:
                running = running + item
    return running

print(round(sum_nested_by_loop(order), 2))    # 24.65
```

The same €24.65. The loop opens the bags in a different order from the
recursion, but adding does not care about order, so the answer is the
same.

</details>

**11. Explain.** `factorial_again(-1)` and `factorial_again(2.5)` both
stop with a `RecursionError`. Why? Someone suggests changing the base
case to `if n <= 0: return 1`, so that they give an answer. Is that a
good idea?

<details class="dl-answer"><summary>answer</summary>

From −1, `n` goes −2, −3, −4, away from 0. From 2.5, it goes 1.5, 0.5,
−0.5, and steps over 0. Neither ever reaches the base case, so the calls
pile up until Python's limit stops them.

The suggested change stops the error, but it gives wrong answers
quietly: `factorial_again(2.5)` would give $2.5 \times 1.5 \times 0.5 =
1.875$, which is not a factorial of anything. The inputs are outside the
promise's domain, whole numbers from 0 up. A clearer fix checks the
domain at the top, as on
[Machines that take a number](tutorial:machines-that-take-a-number#what-goes-in-and-what-comes-out):

```python
assert n >= 0 and n == int(n), "n must be a whole number, 0 or more"
```

An error with a message says what went wrong. A wrong answer says
nothing.

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

4 calls: one for "Holidays" itself, and one for each folder inside it,
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
`deepest(nested)`, which gives back how many levels deep the deepest
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
3. At the end, give back 1 more than the deepest found inside, for the
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

A list with no lists inside is the base case: the loop makes no calls,
and it gives back 1.

</details>

**14. Another way.** On
[Finding things fast](tutorial:finding-things-fast), binary search
looked at the middle of a sorted list, then kept only the half that
could hold the target. Keeping half is the same search on a smaller
problem, so binary search can be written as a recursion. Finish this
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
3. In each case, give back what the same function gives back for that
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

It looks at 10 parts, from "0 to 999" down to "999 to 999", and gives
back 999, the last place. $\log_2 1000$ is about 9.97, so about 10
halvings bring 1,000 places down to 1. Searching for 2000 also takes 10
looks, and gives back −1: the part shrinks to nothing, and `low > high`
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
call makes two more, and the two ask the same questions again:
`rabbits(8)` is worked out once for month 10, and again inside the call
for month 9. The page
[Making change: brute force, memoization and greedy algorithms](tutorial:three-ways-to-make-change)
shows how to remember an answer once it is worked out, so that it is
never worked out twice.

</details>

**16. Make.** Write `all_items(nested)`, which gives back a new list of
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
3. For an item that is a list, `all_items(item)` gives back a list.
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
same as `count_items(library)`, which is a good test: two routes, one
answer.

</details>
