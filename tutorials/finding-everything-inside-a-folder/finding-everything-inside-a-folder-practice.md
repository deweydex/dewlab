---
title: "Recursion: finding every file in a folder tree — Practice"
practice_for: finding-everything-inside-a-folder
year: "2026-2027"
version: 2026.09.05.1
---

# Recursion: finding every file in a folder tree — Practice

The answers are hidden in folds under each problem. Several problems ask
you to predict what the code will do before you run it. Try to answer
before you check. A wrong guess teaches you more than a lucky right one,
once you see why it was wrong.

```python exec
id: setup-1
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

def count_files(folder):
    total = len(folder["files"])
    for sub in folder["subfolders"]:
        total += count_files(sub)
    return total
```

## The base case

**1.** An empty folder, `{"name": "empty", "files": [], "subfolders": []}`,
holds no files and no subfolders.

1. Predict what `count_files` gives for it, before you run it.
2. Which line in `count_files` produces that answer?

```python exec
id: the-base-case-1
```

<details class="dl-answer"><summary>answer</summary>

It gives `0`. The line `total = len(folder["files"])` sets `total` to `0`, because
`files` is empty. Then the loop `for sub in folder["subfolders"]` runs zero
times, because there are no subfolders.

This is the base case at work. A folder with nothing inside it answers
at once. `count_files` is called only once, and never calls itself.

</details>

**2.** This is the tutorial's last-but-one exercise, if you have not done
it yet.

1. Write `deepest_level(folder, level=0)`. It returns how many levels
   down the deepest subfolder is.
2. Predict `deepest_level(photos)`, before you run it.

```python exec
id: the-base-case-2
hint: A folder with no subfolders is already at its own deepest level. A folder with subfolders is one level deeper than the deepest of them.
```

<details class="dl-answer"><summary>answer</summary>

```python
def deepest_level(folder, level=0):
    if not folder["subfolders"]:
        return level
    return max(deepest_level(sub, level + 1) for sub in folder["subfolders"])
```

`max(...)` picks the largest of the values it is given, here one value
for each subfolder.

The answer is `2`. `photos` is level `0`, `"2026"` is level `1`, and
`"trip"` is level `2`, the deepest branch. `"2025"` has no subfolders of
its own, so its branch stops at level `1`. That is less than `2`, so it
does not change the answer.

</details>

## A different tree

**3.** Here is a second folder. This one is for work, not photos.

```python exec
id: a-different-tree-1
work = {
    "name": "work",
    "files": ["report.docx"],
    "subfolders": [
        {
            "name": "clients",
            "files": [],
            "subfolders": [
                {"name": "acme", "files": ["invoice.pdf", "contract.pdf"], "subfolders": []},
            ],
        },
        {"name": "archive", "files": ["old.docx", "older.docx", "oldest.docx"], "subfolders": []},
    ],
}
```

Predict `count_files(work)` by hand. Add up every file at every level.
Then check with code.

```python exec
id: a-different-tree-2
```

<details class="dl-answer"><summary>answer</summary>

The total is `6`.

- One file is directly in `work`: `report.docx`.
- Two are in `"acme"`: `invoice.pdf` and `contract.pdf`.
- Three are in `"archive"`: `old.docx`, `older.docx` and `oldest.docx`.

`"clients"` holds no files of its own, only a subfolder. So it adds
nothing by itself.

</details>

## Visiting in a different order

**4.** The tutorial's `count_files_iterative` visits the most recently
added folder first. That is because `pop()`, with nothing in the
brackets, removes the last item from a list.

1. Change one line, so that it visits folders in the order they were
   added: first added, first visited.
2. Check that the total for `photos` is still the same.

```python exec
id: visiting-in-a-different-order-1
hint: pop(0) removes the first item from a list, rather than the last.
```

<details class="dl-answer"><summary>answer</summary>

```python
def count_files_iterative_ordered(folder):
    total = 0
    to_visit = [folder]
    while to_visit:
        current = to_visit.pop(0)
        total += len(current["files"])
        to_visit.extend(current["subfolders"])
    return total
```

The total for `photos` is still `5`. The one line to change is `pop()`
to `pop(0)`. Everything else stays the same. The same folders are
visited, and the same files are counted. Only the *order* changes. The
tutorial already showed that the order never changes the total.

</details>
