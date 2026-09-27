---
title: "A function that calls itself: recursion"
year: "2026-2027"
version: 2026.09.26.1
covers:
  folders-inside-folders:
    touches: [MIT-6.8, PDP-LO6]
  a-promise-that-uses-itself:
    covers: [MIT-6.8]
    touches: [PDP-LO8]
  what-happens-when-calls-that-wait:
    covers: [MIT-6.8, PDP-LO8]
  where-the-promise-stops-the-base-case:
    covers: [MIT-6.8]
    touches: [PDP-LO9]
  counting-every-file:
    covers: [MIT-6.8, PDP-LO8]
  recursion-or-a-loop:
    covers: [MIT-6.8]
    touches: [PDP-LO6]
---

# A function that calls itself: recursion

The photo folder on your laptop is called "Holidays". It has some photos
in it, and some folders. Some of those folders have folders of their
own. How many photos are there in all, counting every folder inside
every folder?

A loop cannot answer that on its own, and you will see why. The answer
is a function that uses itself. That sounds like a circle, the kind of
answer that says "a word means the word". But if you are
careful, it works, and it can be the shortest code on the page.

On this page we:

- keep a folder of folders as a list of lists
- see why a loop, or two loops, cannot count every photo
- write a function that calls itself, and keeps its promise by using
  that promise on a smaller problem
- watch the calls wait for each other, one inside another
- see what happens when a promise never stops, and why every recursion
  needs a place to stop
- add `count_items` to the toolkit
- count the same photos with a loop and a to-do list, and compare

> **The space we're in.** We use lists, from
> [A row of numbers](tutorial:a-row-of-numbers), and functions, which
> can call any function they can see. This page adds one new idea. A
> function can see its own name, so it can call itself. Every call gets a fresh space
> of names, as on
> [What a function can see](tutorial:what-a-function-can-see#a-fresh-space-for-every-call).
> We usually do not say it, but Python only lets calls wait inside
> other calls to a certain depth, usually about a thousand.

## Warm-up

Two questions from earlier units. The first is from
[What a function can see](tutorial:what-a-function-can-see), and the
second from [Orders and choices](tutorial:orders-and-choices).

```question
id: calls-itself-warm-up-1
type: multiple-choice
answer: 2

A function makes the name `stamps` inside itself. It is called three
times. What happens to the `stamps` from the first call?

- The second call starts with it, and adds to it.
  - This is what would happen if a function's names lived on after the call ended.
- It is thrown away when the first call ends. Each call gets a fresh space.
  - Each call builds its own space for its names, and clears it when it ends.
- It becomes a global name on the page.
  - A name made inside a function stays inside it, unless the function says `global`.
```

```question
id: calls-itself-warm-up-2
type: fill-in-the-blank

$5! = 5 \times 4 \times 3 \times 2 \times 1 = 120$, and
$4! = 24$. So $5! = 5 \times {24}$.
```

## Folders inside folders

A folder can hold two kinds of thing: files, and other folders. A list
can hold two kinds of thing too: values, and other lists. So let's keep
a file as its name, in quotes, and a folder as a list of what is inside
it. Here is "Holidays":

```python exec
id: calls-itself-folders-1
holidays = [
    "sunset.jpg",
    ["kerry-1.jpg", "kerry-2.jpg", "kerry-3.jpg"],
    "cake.jpg",
    ["paris-1.jpg", ["louvre-1.jpg", "louvre-2.jpg"], "paris-2.jpg"],
]
print(len(holidays))
```

Count the photos by eye first. There are 9. Before you run the cell,
what will `len(holidays)` say?

It says 4. `len` counts what is directly inside the list: two photos
and two folders. It does not look inside the folders. A list that holds
lists is called a *nested list*, and each list inside another is one
*level* deeper.

<img src="holidays-folders.svg" alt="The Holidays folder drawn the way a file browser shows it, one item to a line, with each level further to the right. Level 1, directly inside Holidays, holds sunset.jpg, a folder called kerry, cake.jpg, and a folder called paris. These four are shaded, and they are what len counts. Inside kerry, at level 2, are kerry-1.jpg, kerry-2.jpg and kerry-3.jpg. Inside paris are paris-1.jpg, a folder called louvre, and paris-2.jpg. Inside louvre, at level 3, are louvre-1.jpg and louvre-2.jpg. There are 9 photos in all.">

To look inside, a loop has to tell a folder from a photo.
`isinstance(item, list)` gives `True` when `item` is a list, and `False`
when it is anything else. Here is a loop that counts a folder by its
`len`, and a photo as 1. How many will it find?

```python exec
id: calls-itself-folders-2
photos_found = 0
for item in holidays:
    if isinstance(item, list):
        photos_found = photos_found + len(item)
    else:
        photos_found = photos_found + 1
print(photos_found)
```

It finds 8, one short. The "paris" folder has a folder inside it,
"louvre", and `len` counted that folder as one photo. We could put a
second loop inside the first, to look inside "louvre". But then a
folder inside "louvre" would need a third loop, and a folder inside
that, a fourth. We need one loop for each level, and we cannot know how
many levels there are until we look.

## A promise that uses itself

Let's put the folders aside for a moment, and look at a smaller question
with the same shape. The warm-up found that $5! = 5 \times 4!$. The
factorial of 5 has the factorial of 4 inside it. And the factorial of 4
has the factorial of 3 inside it, and so on down.

In words: the factorial of $n$ is $n$ times the factorial of the number
one smaller. In symbols:

$$n! = n \times (n - 1)!$$

That rule uses factorial to explain factorial, so on its own it would go
on for ever: $1! = 1 \times 0!$, then $0! = 0 \times (-1)!$, and so on.
It needs a place to stop. On
[Orders and choices](tutorial:orders-and-choices#what-is-0) we found
that $0! = 1$. That is where it stops.

Here is the rule as a Python function. Your toolkit already has a
`factorial`, so this one is called `factorial_again`, to leave the tool
alone. What will it give for 5?

```python exec
id: calls-itself-promise-1
def factorial_again(n):
    """Give back n!, which is 1 x 2 x ... x n. n is a whole number, 0 or more."""
    if n == 0:
        return 1
    return n * factorial_again(n - 1)

print(factorial_again(5))
```

It gives 120. Look at the last line of the function. `factorial_again`
calls `factorial_again`. A function that calls itself is a *recursive
function*. *Recursion* is solving a problem by using the same promise
on a smaller problem.

Here is how to read that last line. Do not follow the call down. Trust
the promise instead. `factorial_again(n - 1)` returns $(n - 1)!$,
because that is what the docstring promises. Then $n \times (n - 1)!$
is $n!$, which is what this call promised. So the promise keeps itself,
as long as it stops somewhere.

If trusting the promise feels like cheating, the next section can help.
It follows every call, one at a time, so you can see that nothing is
hidden. You can read it first and come back.

Every recursive function has two parts:

- The *base case* is an input small enough to answer straight away,
  with no more calls. Here it is $n = 0$, and the answer is 1. It is
  the place where the promise stops.
- The *recursive case* is every other input. It hands a smaller problem
  to the same function, and builds its own answer from what comes back.

Let's check the promise. Does `factorial_again` agree with the
`factorial` you wrote on Orders and choices? The cell prints each $n$,
then the two answers side by side.

```python exec
id: calls-itself-promise-2
for n in [0, 1, 5, 10, 20]:
    print(n, factorial_again(n), factorial(n))
```

Where the last two numbers on a line differ, look again at one of the
two functions.

### Your turn

1. The sum $1 + 2 + \dots + n$ has the same shape. In words, the sum up
   to $n$ is $n$ plus the sum up to $n - 1$. What is the sum up to 0?
2. Finish `sum_up_to` in the cell below, with a base case and a
   recursive case.
3. Check it against Gauss's formula from
   [Doing it again](tutorial:doing-it-again#sigma-a-loop-written-by-mathematicians):
   `sum_up_to(100)` should be 5050.

```python exec
id: calls-itself-promise-your-turn
def sum_up_to(n):
    """Give back 1 + 2 + ... + n. n is a whole number, 0 or more."""
    ...

print(sum_up_to(100))
```

## What happens when: calls that wait

When you write recursion, you trust the promise. Now let's watch what
Python does. This version of the function prints a line when each call
starts, and another when it returns its answer. The name `depth` is
there only for the printing. It moves each deeper call four more spaces
to the right. How many "starts" lines will there be?

```python exec
id: calls-itself-wait-1
def factorial_shown(n, depth=0):
    """Give back n!, and print each call as it starts and ends."""
    indent = "    " * depth
    print(indent + "factorial_shown(" + str(n) + ") starts")
    if n == 0:
        answer = 1
    else:
        answer = n * factorial_shown(n - 1, depth + 1)
    print(indent + "factorial_shown(" + str(n) + ") gives back " + str(answer))
    return answer

factorial_shown(4)
```

Five calls start, for 4, 3, 2, 1 and 0. Here is what happens, in order.

1. The call for 4 starts. It needs `factorial_shown(3)` before it can
   multiply, so it waits, and the call for 3 starts.
2. The call for 3 waits for 2, 2 waits for 1, and 1 waits for 0.
3. The call for 0 is the base case. It returns 1 at once.
4. Now the call for 1 can finish: $1 \times 1 = 1$. Then 2 finishes
   with $2 \times 1 = 2$, then 3 with $3 \times 2 = 6$, then 4 with
   $4 \times 6 = 24$.

<img src="calls-that-wait.svg" alt="Five boxes in a staircase, each one lower and further right than the one before: factorial_shown(4), then factorial_shown(3), (2), (1) and (0). An arrow marked waits for runs down from each box to the next. Beside each box is what it gives back, and when it starts and finishes. The call for 0 is the base case: it gives back 1, starts 5th and finishes 1st. The call for 1 gives back 1 × 1 = 1. The call for 2 gives back 2 × 1 = 2. The call for 3 gives back 3 × 2 = 6. The call for 4 gives back 4 × 6 = 24: it starts 1st and finishes 5th.">

The call for 4 starts first and finishes last. While the call for 0
runs, four other calls are waiting, each at the same line. Each one has
its own space of names, and in each space `n` is a different number:

| Call | Its own `n` | Waiting for | Then returns |
|---|---|---|---|
| first | 4 | the call for 3 | $4 \times 6 = 24$ |
| second | 3 | the call for 2 | $3 \times 2 = 6$ |
| third | 2 | the call for 1 | $2 \times 1 = 2$ |
| fourth | 1 | the call for 0 | $1 \times 1 = 1$ |
| fifth | 0 | nothing: the base case | 1 |

There are five names called `n`, all at once, and they never get in
each other's way. This is the fresh space for every call, from
[What a function can see](tutorial:what-a-function-can-see#a-fresh-space-for-every-call),
and here it does real work.

The calls that have started and not yet finished make a list, with the
newest at the top. This list is the *call stack*. A new call goes on
top, and only the call on top can run. When it returns its answer, it
comes off, and the call under it continues. It works like a stack of
plates: the last plate put on is the first one taken off.

```question
id: calls-itself-wait-2
type: fill-in-the-blank

`factorial_again(10)` calls itself for 9, 8, and so on down to 0. In
all, counting the first call, there are {11} calls.
```

<aside class="dl-note" id="calls-itself-note-search">

**Did you mean: recursion?** For years, a search for the word
"recursion" on Google has shown the line "Did you mean:
recursion". Click it, and you are back where you started. It is a
programmers' joke: the definition of recursion that uses recursion,
with no base case to stop it.

</aside>

## Where the promise stops: the base case

What if we forget the base case? Here is `factorial_again` with its
first two lines removed. This cell is meant to fail. Before you run
it, which numbers will `n` be, one call after another?

```python exec
id: calls-itself-stop-1
def factorial_no_stop(n):
    """Meant to give back n!, but it has no base case."""
    return n * factorial_no_stop(n - 1)

factorial_no_stop(4)
```

`n` is 4, then 3, 2, 1, 0, then −1, −2, −3, and nothing tells it to
stop. The traceback shows the same line many times, then a note like
`[Previous line repeated 996 more times]`. The last line says:

```text
RecursionError: maximum recursion depth exceeded
```

Every waiting call keeps its space of names, and that takes memory. So
Python sets a limit on how many calls may wait at once. A
*RecursionError* is Python stopping a recursion that went deeper than
that limit. You can ask Python what the limit is here:

```python exec
id: calls-itself-stop-2
import sys
print(sys.getrecursionlimit())
```

On most computers it is 1000. So the error means we have reached the
limit of this space. In maths, the rule $n! = n \times (n - 1)!$ would
go on for ever too, without $0! = 1$ to stop it. The computer does not
go on for ever. It has no more room.

On [Doing it again](tutorial:doing-it-again#until-something-is-true-while)
we asked of every `while` loop: what makes it end? Recursion needs the
same question, and it has a two-part answer.

1. There is a base case, an input that makes no more calls.
2. Every call hands on a smaller problem, one that is closer to the
   base case.

Break the second rule, and the base case is never reached. Run the
cell below, then change the 3 to 2.5 and run it again. Before you do,
what will `n` be, call after call? Will it ever equal 0?

```python exec
id: calls-itself-stop-3
print(factorial_again(3))
```

`n` goes 2.5, 1.5, 0.5, −0.5, and steps over 0, so the same error
appears. Whole numbers from 0 up are the domain of the promise, as on
[Machines that take a number](tutorial:machines-that-take-a-number#what-goes-in-and-what-comes-out).
Outside it, the steps never land on the place where they stop.

## Counting every file

Back to the photos. Let's say the promise first, in words:
`count_items(folder)` returns how many photos are inside `folder`,
at any depth.

Now keep the promise by using it on a smaller problem. Look at the
folder one item at a time, and keep a running count:

- if the item is a photo, add 1;
- if the item is a folder, add `count_items(item)`: the same promise,
  on a smaller folder.

Where is the base case? A folder that holds only photos never calls
again. Its loop runs to the end and returns its count. An empty
folder returns 0. So the recursion stops at the bottom of every
branch, even without an `if` for it.

This goes in your toolkit, with the name `nested` for the list it is
given, since it counts items in any nested list, not only photos. The
body is yours to write:

1. Start a count at 0. Call it `found`, since `total` is a toolkit tool.
2. Loop over every `item` in `nested`.
3. If `isinstance(item, list)`, add `count_items(item)` to `found`.
   Otherwise, add 1.
4. After the loop, return `found`.

```python exec
id: calls-itself-toolkit
toolkit: yes
def count_items(nested):
    """Count the items inside nested, a list that may hold lists, at any depth.

    A list inside counts for what it holds, not as an item itself.
    count_items(["a", ["b", "c"], []]) is 3.
    """
    ...
```

```python toolkit-reference
for: calls-itself-toolkit
def count_items(nested):
    """Count the items inside nested, a list that may hold lists, at any depth.

    A list inside counts for what it holds, not as an item itself.
    count_items(["a", ["b", "c"], []]) is 3.
    """
    found = 0
    for item in nested:
        if isinstance(item, list):
            found = found + count_items(item)
        else:
            found = found + 1
    return found
```

```hint
What does `count_items(["a.jpg"])` give back now? A function whose body
is only `...` gives back `None`. Start with the smallest folders: an
empty one, and one with a single photo.
```

```hint
after: 10 errors
title: some steps
1. The line after the docstring is `found = 0`, pushed in as far as the
   docstring.
2. The loop is `for item in nested:`. Inside it, an `if` with
   `isinstance(item, list)`, and an `else`.
3. In the `if` branch, `found = found + count_items(item)`. In the
   `else` branch, add 1.
4. `return found` sits after the loop, at the same level as `for`.

**Think about:** what does the call for an empty folder give back, and
why is 0 the count it should give?
```

How does your `count_items` compare with one way to write it? The table
below runs the same calls on your function and on a solution, side by
side. Look at the fourth row: what is a folder of empty folders worth?
Where a row is different, try that call on its own.

```inputs
for: calls-itself-toolkit
count_items([])
count_items(["only.jpg"])
count_items(holidays)
count_items([[[[]]]])                  # folders, and no photos
count_items([[["deep.jpg"]]])
count_items([1, [2, [3, [4, [5]]]]])   # items need not be names
```

```solution
for: calls-itself-toolkit
def count_items(nested):
    """Count the items inside nested, a list that may hold lists, at any depth.

    A list inside counts for what it holds, not as an item itself.
    count_items(["a", ["b", "c"], []]) is 3.
    """
    found = 0
    for item in nested:
        if isinstance(item, list):
            found = found + count_items(item)
        else:
            found = found + 1
    return found
```

It counts 9 photos in "Holidays", where the loop found 8. It does not
matter how deep a folder is. Each folder is counted by its own call,
and each call only has to look one level down.

### Your turn

If you have not written `count_items` yet, open the solution under the
table and copy it into the stub.

1. A music library has a folder for each artist, and inside it a folder
   for each album. The artists' names are in comments, so that
   `count_items` counts only songs. Before you run the cell, how many
   songs are there?
2. Add a third artist to `library`, with one album of three songs, and
   count the songs again.
3. Copy `count_items` into the cell, and change it into
   `count_folders(nested)`, which counts the folders inside instead of
   the files. It needs two changes. What does a folder add, besides the
   folders inside it?

```python exec
id: calls-itself-count-your-turn
library = [
    [["Take Me to Church", "Cherry Wine"], ["Too Sweet", "Eat Your Young"]],  # Hozier
    [["Linger", "Dreams", "Zombie"]],                                        # The Cranberries
]
print(count_items(library))
```

## Recursion or a loop?

Can a loop count every photo after all? It can, if it keeps a list of
the folders it has not opened yet. Call that list `to_open`. Here is the
plan:

1. Put the whole folder in `to_open`.
2. While `to_open` is not empty, take one folder out of it, and look at
   each item inside. Count each photo. Put each folder you meet into
   `to_open`, for later.

`to_open.pop()` removes the last item from the list, and returns it.
Will this loop find 9 photos, too?

```python exec
id: calls-itself-loop-1
def count_items_by_loop(nested):
    """Count the items inside nested, at any depth, with a loop and a to-do list."""
    found = 0
    to_open = [nested]
    while len(to_open) > 0:
        folder = to_open.pop()
        for item in folder:
            if isinstance(item, list):
                to_open.append(item)
            else:
                found = found + 1
    return found

print(count_items_by_loop(holidays), count_items(holidays))
```

Both find 9. The list `to_open` does the job the call stack did for
`count_items`: it remembers the work that is still waiting. Any
recursion can be written as a loop with a list like this, and any loop
can be written as a recursion. So which is better?

| | Recursion | A loop with a to-do list |
|---|---|---|
| How it reads | close to the promise in words | more lines, and the to-do list is ours to manage |
| What waits | calls, on Python's call stack | folders, in our own list |
| How deep it can go | about 1,000 levels, then a RecursionError | as deep as memory allows |

A folder tree is rarely 1,000 levels deep, so for folders, recursion
reads better and costs nothing. For a list of a million numbers, a
recursion that makes one call per number, like `factorial_again`, runs
out of room, and a loop is the better tool. Ask what this space lets us
do.

<details class="dl-why"><summary>Why this way?</summary>

This page asked you to trust the promise before it showed you the
calls. You read `n * factorial_again(n - 1)` as "$n$ times $(n-1)!$",
and only then watched five calls wait inside each other.

Many courses go the other way: trace every call first, with a diagram of
the call stack, and let the promise come later. The trace shows that
there is no magic, and it is the view a debugger gives you when a
recursion does something you did not expect.

We led with the promise because tracing stops working quickly. You can
trace `factorial_again(4)`. You cannot trace a folder of ten thousand
photos. The two checks you learned, a base case that stops and a promise
kept for one step, work at any size. Mathematicians use the same two
checks to prove a rule for every whole number.

</details>

## Four questions, looking back

| The question | On this page |
|---|---|
| What is named here? | a folder, as a list of what is inside it; a function's own name, used inside its body; a different `n` in every call |
| What is promised? | `factorial_again(n)` promises $n!$ and keeps it by using the promise on $n - 1$; `count_items` promises every item, at any depth |
| What happens when? | each call waits for the one it made; the first call waits until all the others finish; the base case returns first |
| What does this space let us do? | a function can call itself; Python allows about 1,000 waiting calls; a loop with a to-do list has no such limit |

## What we have now

| Term or tool | What it means |
|---|---|
| nested list, level | a list with lists inside it; each list inside is one level deeper |
| `isinstance(item, list)` | `True` when `item` is a list |
| recursion, recursive function | using a promise on a smaller problem to keep it; a function that calls itself |
| base case | an input answered straight away, with no more calls: where the promise stops |
| recursive case | every other input: hand a smaller problem to the same function, and build on its answer |
| $n! = n \times (n - 1)!$, $0! = 1$ | factorial, written as a recursion |
| call stack | the calls that have started and not finished, newest on top |
| `RecursionError` | too many calls waiting at once, usually because the recursion never reaches its base case |
| `sys.getrecursionlimit()` | how many calls Python lets wait at once |
| `list.pop()` | removes the last item from a list, and returns it |
| `count_items(nested)` | your toolkit tool: every item in a nested list, at any depth |

The practice page is next. After it,
[Doubling and halving](tutorial:doubling-and-halving) asks why a rumour
spreads so fast.

## Where to read more

The dewlab page
[Recursion: finding every file in a folder tree](tutorial:finding-everything-inside-a-folder)
walks through real folders on a computer, with and without recursion.
[Making change: brute force, memoization and greedy algorithms](tutorial:three-ways-to-make-change)
shows a recursion that repeats the same work, and a way to remember
what it already calculated.

Reducible (2019). *5 Simple Steps for Solving Any Recursive Problem.*
<https://www.youtube.com/watch?v=ngCos392W4w>. Reducible solves three
recursive problems, each harder than the last, by asking the question this
page asks: if a smaller case were already solved, how would we use it?
About twenty-one minutes.
