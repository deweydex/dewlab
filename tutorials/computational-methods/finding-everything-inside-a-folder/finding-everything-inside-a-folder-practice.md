---
title: "Finding Everything Inside a Folder — Practice"
slug: finding-everything-inside-a-folder-practice
practice_for: finding-everything-inside-a-folder
module: computational-methods
module_title: "Computational Methods"
year: "2026-2027"
series: algorithms
version: 2026.09.05.1
---

# Finding Everything Inside a Folder — Practice

Answers are folded. Several of these ask you to predict an output before
running anything. Resist checking first — being wrong and finding out why
is worth more than being right by accident.

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

## The Base Case

**1.** An empty folder, `{"name": "empty", "files": [], "subfolders": []}`,
holds no files and no subfolders. Predict `count_files` on it before
running it, and say which line in `count_files` produces that answer.

```python exec
id: the-base-case-1
```

<details class="dl-answer"><summary>answer</summary>

`0`. `total = len(folder["files"])` sets `total` to `0`, since `files` is
empty, and the `for sub in folder["subfolders"]` loop runs zero times,
since there are no subfolders to add. This is the base case working
correctly: a folder with nothing branching from it answers immediately,
with no call to `count_files` needed beyond the first.

</details>

**2.** Try writing `deepest_level(folder, level=0)` so it returns how
many levels down the deepest subfolder sits, matching the tutorial's own
description. Predict `deepest_level(photos)` before running it.

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

`2`. `photos` is level `0`, `"2026"` is level `1`, and `"trip"` is level
`2`, the deepest branch. `"2025"` has no subfolders of its own, so it
stops at level `1` without adding to the deepest total.

</details>

## A Different Tree

**3.** A second folder, this time about work rather than photos:

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

Predict `count_files(work)` by hand, adding up every file at every level,
before checking with code.

```python exec
id: a-different-tree-2
```

<details class="dl-answer"><summary>answer</summary>

`6`. One file directly in `work` (`report.docx`), two in `"acme"`
(`invoice.pdf`, `contract.pdf`), and three in `"archive"` (`old.docx`,
`older.docx`, `oldest.docx`). `"clients"` itself holds no files directly,
only a subfolder, so it contributes nothing on its own.

</details>

## Visiting in a Different Order

**4.** The tutorial's `count_files_iterative` visits the most recently
added folder first, because `pop()` removes the last item from a list by
default. See if you can change one line so it visits folders in the
order they were added instead — first added, first visited — and confirm
the total is still the same on `photos`.

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

Still `5` on `photos`. Changing `pop()` to `pop(0)` is the one line that
needed to change — everything else about which folders get visited and
which files get counted stays the same. Only the *order* changes, and
the tutorial already showed that the order never changes the total.

</details>
