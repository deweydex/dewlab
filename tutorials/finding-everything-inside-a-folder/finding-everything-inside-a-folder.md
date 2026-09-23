---
title: "Recursion: finding every file in a folder tree"
year: "2026-2027"
version: 2026.09.05.1
covers:
  a-structure-that-branches:
    covers: [CMPS-LO1]
  walking-it-with-recursion:
    covers: [CMPS-LO1]
  walking-it-without-recursion:
    covers: [CMPS-LO1]
---

# Recursion: finding every file in a folder tree

A grid has a fixed shape: so many rows, so many columns, and one value
where each row meets each column. A folder on a computer is different.
It holds files, and it holds other folders. Each of those can hold more
files and more folders, as many levels deep as anyone likes.

On this page we build that shape in Python. Then we count every file
inside it, in two different ways.

## A Structure That Branches

Here is one folder, written as a Python dictionary. It has three keys:
`"name"`, `"files"` and `"subfolders"`. The value for `"subfolders"` is a
list, and each item in that list is another folder, written the same
way. If you want a reminder of how dictionaries work, see
[Dictionaries: looking things up by name](tutorial:looking-things-up-by-name).

```python exec
id: a-structure-that-branches-1
photos = {
    "name": "photos",
    "files": ["beach.jpg", "party.jpg"],
    "subfolders": [
        {"name": "2025", "files": ["new_year.jpg"], "subfolders": []},
        {
            "name": "2026",
            "files": [],
            "subfolders": [
                {"name": "trip", "files": ["day1.jpg", "day2.jpg"], "subfolders": []}
            ],
        },
    ],
}

print(photos["name"])
print(photos["files"])
print(photos["subfolders"][0]["name"])
```

![The photos folder holds two files and two subfolders, 2025 and 2026. 2025
holds one file. 2026 holds no files and one subfolder, trip, which holds
two files.](photos-tree.svg)

This shape is called a *tree*. A tree is a structure where each value can
lead to several others, and following it never leads back to where you
started.

- `photos` holds two files, and two subfolders: `"2025"` and `"2026"`.
- `"2025"` holds one file, and no subfolders.
- `"2026"` holds no files of its own. It holds one subfolder, `"trip"`,
  which holds two files.

That makes three levels. But nothing in the dictionary says in advance
how many levels there will be. A grid in
[Matrices: adding, scaling and transposing a grid of numbers](tutorial:grid-of-numbers) is different: its number
of rows and columns is fixed as soon as it is made.

### Your turn

Look at `photos["subfolders"][1]["subfolders"][0]`.

1. Read the dictionary above. What is this folder's name, and how many
   files does it hold?
2. Check your answer with code.

```python exec
id: a-structure-that-branches-2
```

## Walking It With Recursion

We want to count every file, at every level. So we need one function
that can handle any folder: one that holds only files, one that holds
only more folders, and anything in between.

How many files do you count in the picture above? Run the cell to check.

```python exec
id: walking-it-with-recursion-1
def count_files(folder):
    total = len(folder["files"])
    for sub in folder["subfolders"]:
        total += count_files(sub)
    return total

print(count_files(photos))
```

Look at the loop inside `count_files`. The function calls itself, once
for every subfolder. A function that calls itself is using *recursion*.

Each call answers a smaller version of the same question: how many files
does *this* folder contain? Here is what happens when we call
`count_files(photos)`:

1. `photos` has 2 files of its own. Then it asks each of its subfolders.
2. `"2025"` has 1 file and no subfolders. The loop has nothing to do, so
   it answers 1 straight away.
3. `"2026"` has 0 files of its own. It asks its one subfolder, `"trip"`.
4. `"trip"` has 2 files and no subfolders, so it answers 2 straight away.
5. `"2026"` adds that up: 0 + 2 = 2.
6. `photos` adds everything up: 2 + 1 + 2 = 5.

A folder with no subfolders answers at once, using only
`len(folder["files"])`. It does not call `count_files` again. This case
is called the *base case*. The base case is the case a recursive
function can answer without calling itself.

Every branch of the tree ends in a folder with no subfolders, so every
chain of calls reaches a base case and stops. Without a base case, a
recursive function would call itself again and again, and never stop.

### Your turn

Write `deepest_level(folder, level=0)`. It returns how many levels down
the deepest subfolder is. `photos` itself is at level `0`, and `"trip"`
is at level `2`.

```python exec
id: walking-it-with-recursion-2
hint: A folder with no subfolders is already at its own deepest level. A folder with subfolders is one level deeper than the deepest of them.
```

## Walking It Without Recursion

We can do the same count without a function that calls itself. This
version uses a `while` loop, as in
[Repeating steps with loops](tutorial:repeating-yourself), and two list
methods you may not have met yet:

- `to_visit.pop()` removes the last item from the list `to_visit`, and
  gives it back.
- `to_visit.extend(other_list)` adds every item from `other_list` to the
  end of `to_visit`.

`while to_visit:` keeps going as long as the list is not empty. Python
treats an empty list as false, and a list with anything in it as true.

```python exec
id: walking-it-without-recursion-1
def count_files_iterative(folder):
    total = 0
    to_visit = [folder]
    while to_visit:
        current = to_visit.pop()
        total += len(current["files"])
        to_visit.extend(current["subfolders"])
    return total

print(count_files_iterative(photos))
```

`to_visit` holds every folder that is still waiting to be counted. It
starts with only `photos`. Each pass through the loop does three things:

1. It takes one folder off the list.
2. It counts that folder's files.
3. It adds that folder's subfolders to the list, for a later pass.

Nothing here calls itself. This version is *iterative*: it repeats a
loop, and it keeps its own list of what is left to do.

The recursive version needs a list like that too. Python keeps it
behind the scenes. Python always keeps a list of the function calls that
have started but not yet finished, called the *call stack*. In the
recursive version, the call stack keeps track of which folders are left.

Both versions visit the same folders, and count the same files. But they
visit them in a different order:

- `count_files` finishes `"2025"` completely before it starts `"2026"`.
- `count_files_iterative` always visits the folder that was added to
  `to_visit` most recently. So it visits `"2026"` and `"trip"` before
  `"2025"`.

The order depends on the order the subfolders were added. It is the same
on every run. And the order never changes the total.

### Your turn

Change `count_files_iterative` so that it visits folders in the order
they were added: first added, first visited. At the moment it does the
opposite: last added, first visited. Only one line needs to change.

```python exec
id: walking-it-without-recursion-2
hint: pop() takes the last item off a list by default. A different argument to pop() takes the first item instead.
```

## Where to Read More

Sedgewick, R. and Wayne, K. (2011). *Algorithms* (4th ed.). Addison-Wesley.
Chapter 4 covers graphs, and the depth-first and breadth-first traversal
strategies this page builds by hand for a tree, at a depth well past what
this course needs but worth knowing is there.

Python Software Foundation. *os.walk().*
<https://docs.python.org/3/library/os.html#os.walk>. The standard library
function that walks a real folder tree on disk, the same shape this page
built by hand with a plain dictionary.
