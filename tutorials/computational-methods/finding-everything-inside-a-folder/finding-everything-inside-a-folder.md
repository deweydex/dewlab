---
title: "Finding Everything Inside a Folder"
slug: finding-everything-inside-a-folder
module: computational-methods
module_title: "Computational Methods"
year: "2026-2027"
series: algorithms
version: 2026.09.05.1
covers:
  a-structure-that-branches:
    covers: [CMPS-LO1]
  walking-it-with-recursion:
    covers: [CMPS-LO1]
  walking-it-without-recursion:
    covers: [CMPS-LO1]
---

# Finding Everything Inside a Folder

A grid has a fixed shape: so many rows, so many columns, one value at each
crossing. A folder on a disk does not work that way. It holds files, and
it holds other folders, each of which can hold more files and more
folders again, as many levels deep as anyone likes. This tutorial builds
that shape in Python, then counts everything inside it two different
ways.

## A Structure That Branches

One folder, written as a Python dictionary.

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

This is a *tree*: a structure where each value can lead to several others,
and following it never leads back to where it started. `photos` holds two
files directly and two subfolders, `"2025"` and `"2026"`. `"2025"` holds
one file and no subfolders of its own. `"2026"` holds no files directly
but one subfolder, `"trip"`, which holds two files. Three levels, and
nothing about the dictionary says in advance how many levels there will
be — unlike a grid from *A Grid of Numbers*, whose row and column counts
are fixed the moment it is created.

### Your turn

How many files does `photos["subfolders"][1]["subfolders"][0]` hold, and
what is its name? Answer by reading the dictionary above, then check with
code.

```python exec
id: a-structure-that-branches-2
```

## Walking It With Recursion

Counting every file, at every level, needs a function that can handle a
folder holding files directly and one holding only more folders, and
everything in between.

```python exec
id: walking-it-with-recursion-1
def count_files(folder):
    total = len(folder["files"])
    for sub in folder["subfolders"]:
        total += count_files(sub)
    return total

print(count_files(photos))
```

`count_files` calls itself, once for every subfolder. This is
*recursion*. Each call answers a smaller version of the same question:
how many files does *this* folder, one level down, contain? A folder
with no subfolders answers immediately, using only `len(folder["files"])`.
A folder with subfolders answers by asking each of its subfolders the
same question, then combining those answers. Without that immediate
case, `count_files` would call itself on a smaller folder, then a
smaller one again, and never stop.

### Your turn

Try writing `deepest_level(folder, level=0)`, returning how many levels
down the deepest subfolder sits. `photos` itself is level `0`; `"trip"`
is level `2`.

```python exec
id: walking-it-with-recursion-2
hint: A folder with no subfolders is already at its own deepest level. A folder with subfolders is one level deeper than the deepest of them.
```

## Walking It Without Recursion

The same count, without a function ever calling itself.

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

`to_visit` holds every folder still waiting to be counted, starting with
just `photos`. Each pass through the loop removes one folder from that
list, counts its files, and adds its subfolders to the list for a later
pass. Nothing here calls itself. The *iterative* version keeps its own
explicit list of what is left to do. The recursive version let Python's
own call stack track that instead.

Both versions visit the same folders and count the same files, in a
different order. `count_files` finishes `"2025"` completely before
starting `"2026"`, while `count_files_iterative` visits whichever folder
was added to `to_visit` most recently. Which folder that is changes from
one run to the next, depending on the order subfolders were added, but
the final total does not.

### Your turn

Try rewriting `count_files_iterative` so it counts subfolders in the
order they appear in `folder["subfolders"]`, first added first visited,
rather than last added first visited. One line needs to change.

```python exec
id: walking-it-without-recursion-2
hint: pop() takes the last item off a list by default. A different argument to pop() takes the first item instead.
```

## Where to Read More

Sedgewick, R. and Wayne, K. (2011). *Algorithms* (4th ed.). Addison-Wesley.
Chapter 4 covers trees and the traversal strategies this page builds by
hand, at a depth well past what this course needs but worth knowing is
there.

Python Software Foundation. *os.walk().*
<https://docs.python.org/3/library/os.html#os.walk>. The standard library
function that walks a real folder tree on disk, the same shape this page
built by hand with a plain dictionary.
