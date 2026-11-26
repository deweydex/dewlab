---
title: "A Pretend File System: A Storage Manager in Three Weeks"
year: "2026-2027"
version: 2026.11.26.1
covers:
  1-plan-first:
    covers: [PDP-LO6, PDP-LO10]
  3-week-two-folders:
    covers: [PDP-LO7]
  5-release-and-review:
    covers: [PDP-LO10, PDP-LO11]
---

# A Pretend File System: A Storage Manager in Three Weeks

A real computer keeps files in folders on a disk. On this page we build a pretend one inside Python. Each file is only a name and a size, and nothing is saved to a real disk. The commands are the ones a server's command line uses: `ls` lists files, `touch` makes a file, `rm` removes one, and `du` adds up how much space the files use.

The project has three stages, about one week each. Each stage ends with a program that works, so you can stop at any stage and still have something to show.

There are questions on this page to answer in words as well as in code. The **+ Text** button between cells adds a text cell where you can write your answers.

## 1. Plan First

**1.1** Write a sample run of your file system. Show someone listing the files, making a new one, removing one, and asking how much space is used.

<!-- answer -->

**1.2** Write the steps of the program in plain words, one step to a line, before you write any Python. This plan is called pseudocode. Use words like *ask*, *if*, *otherwise* and *repeat*.

<!-- answer -->

**1.3** Write a test plan: a short table of things a person might type, and what the program should do for each one. Include at least two things that should fail politely.

| A person types | The program should |
|---|---|
| `ls` | list every file with its size |
| `rm nothing.txt` | |
| | |

<!-- answer -->

## 2. Week One: Files in Two Lists

```python exec
id: week-one-files-in-two-lists-1
paths = ["readme.txt", "docs/notes.txt", "docs/plan.txt", "music/song.mp3"]
sizes = [5, 12, 30, 4000]
```

**2.1** Run the cell above. Then write a loop that prints every file with its size, like `docs/notes.txt  12 KB`.

```python exec
id: week-one-files-in-two-lists-2
# your loop here
```

```solution
for position in range(len(paths)):
    print(paths[position], " ", sizes[position], "KB")
```

**2.2** Add up the sizes with a loop and print the total. Then try `sum(sizes)`. Do you get the same answer?

```python exec
id: week-one-files-in-two-lists-3
# your total here
```

**2.3** Write the first version of the command line. It repeats until the person types `exit`. It knows `ls`, `du`, `touch` and `rm`. For `touch`, ask for a name and a size. For `rm`, ask for a name, and remove both the path and its size.

```python exec
id: week-one-files-in-two-lists-4
# your file system here
```

<details class="dl-hint"><summary>smaller steps</summary>

1. Start with a `while` loop that asks for a command and stops on `exit`.
2. Add `ls` using your loop from 2.1, and `du` using your total from 2.2.
3. Add `touch`. The size arrives as text, so turn it into an `int`.
4. Add `rm`. Find the position of the name with `index`, then `pop` that position from both lists.

</details>

**2.4** Use your test plan from 1.3. Which tests pass? Which ones fail? Write one line about each failure.

<!-- answer -->

## 3. Week Two: Folders

A folder in our file system is only the start of a path. Every path that starts with `docs/` is inside the folder `docs`.

**3.1** Predict what each line prints, then run the cell.

```python exec
id: week-two-folders-1
print("docs/notes.txt".startswith("docs/"))
print("readme.txt".startswith("docs/"))
print("docs/notes.txt".split("/"))
print("readme.txt".split("/"))
```

<!-- answer -->

**3.2** Change `ls` so it takes a folder. `ls docs` lists only the files in `docs`. Plain `ls` still lists everything.

<!-- answer -->

**3.3** Add a variable `here` that holds the current folder, starting as `""`. Add `cd docs` to change it, and `cd ..` to go back to the top. Show the current folder in the prompt, like `docs> `.

<!-- answer -->

**3.4** After `cd docs`, should `touch todo.txt` make `todo.txt` or `docs/todo.txt`? Decide, write the reason down, and make the code match.

<!-- answer -->

## 4. Week Three: A Disk That Can Fill Up

A real disk has a fixed size. In this stage, the disk holds 5000 KB.

**4.1** Change `touch` so it refuses a file that would make the total bigger than the disk. Print a clear message that says how much space is left.

<!-- answer -->

**4.2** Add a command `df` that shows how full the disk is as a bar. The cell below shows one way to draw a bar. Change `used` and run it a few times.

```python exec
id: week-three-a-disk-that-can-fill-up-1
disk = 5000
used = 4047
width = 20
filled = used * width // disk
print("[" + "#" * filled + "-" * (width - filled) + "]", used, "of", disk, "KB")
```

**4.3** Add a command `big` that lists only the files over a size the person chooses.

<!-- answer -->

**4.4** Look at your whole program. Is there any code you wrote twice? Put each repeated piece in a function with a clear name, and call it from both places.

<!-- answer -->

## 5. Release and Review

**5.1** Give your program to another pair with your test plan. Ask them to break it. Write down what they found.

<!-- answer -->

**5.2** Read your own code as if somebody else wrote it. Are the variable names clear? Is there a comment where a line is hard to understand? Fix one thing.

<!-- answer -->

## 6. More to Try

1. Add `mv`, which renames a file.
2. Add `tree`, which prints the files grouped under their folders.
3. Add a second user, so each file has an owner, and `rm` refuses to remove somebody else's file.
4. Make `ls` print the sizes in a straight column, using `ljust` on the names.

```python exec
id: more-to-try-1
# your experiments here
```
