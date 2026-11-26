---
title: "A Word-Guessing Game: Scoring Each Letter"
year: "2026-2027"
version: 2026.11.26.1
covers:
  1-plan-first:
    covers: [PDP-LO6]
  3-week-two-the-wrong-place:
    covers: [PDP-LO2, PDP-LO10]
---

# A Word-Guessing Game: Scoring Each Letter

In this game the computer picks a secret five-letter word, and the player has six guesses. After each guess, the program marks every letter: right letter in the right place, right letter in the wrong place, or not in the word at all. Marking the letters correctly is a harder puzzle than it looks, and most of this page is about it.

The project has three stages, about one week each. Each stage ends with a game that works.

There are questions on this page to answer in words as well as in code. The **+ Text** button between cells adds a text cell where you can write your answers.

## 1. Plan First

We mark letters with three symbols: `G` for the right place, `Y` for the wrong place, and `.` for not in the word.

**1.1** The secret word is `cable`. Mark these guesses by hand: `table`, `bleak`, `level`.

<!-- answer -->

**1.2** Your mark for `level` probably took some thought, because `level` has two `e`s and two `l`s, and `cable` has only one of each. Write down the rule you used for repeated letters.

<!-- answer -->

**1.3** Write pseudocode for marking a guess.

<!-- answer -->

## 2. Week One: The Right Place

**2.1** Predict what each line prints, then run the cell.

```python exec
id: week-one-the-right-place-1
secret = "cable"
guess = "table"
print(secret[0], guess[0])
print(secret[1] == guess[1])
print("a" in secret)
for position in range(5):
    print(position, guess[position], secret[position])
```

<!-- answer -->

**2.2** Write `mark(guess, secret)`, which hands back a string of five symbols. For now, use only `G` and `.`.

```python exec
id: week-one-the-right-place-2
def mark(guess, secret):
    # your code here
    return "....."

print(mark("table", "cable") == ".GGGG")
print(mark("cable", "cable") == "GGGGG")
```

```solution
def mark(guess, secret):
    result = ""
    for position in range(5):
        if guess[position] == secret[position]:
            result = result + "G"
        else:
            result = result + "."
    return result

print(mark("table", "cable") == ".GGGG")
```

**2.3** Write a game loop with a fixed secret word and six guesses. After each guess, print the guess and its mark. Stop early if the guess is right.

```python exec
id: week-one-the-right-place-3
# your game here
```

**2.4** What should happen when the guess has four letters, or six? Make the game ask again without using up a guess.

<!-- answer -->

## 3. Week Two: The Wrong Place

**3.1** Change `mark` so a letter that is in the secret, but not in that place, gets `Y`. Test it with `bleak` against `cable`.

<!-- answer -->

**3.2** Now try `level` against `cable`, and compare the result with your mark from 1.1. A simple version marks too many `Y`s. Why?

<!-- answer -->

**3.3** Fix the repeated-letter problem. One way is to mark in two passes. The first pass marks every `G` and crosses those letters out of a copy of the secret. The second pass gives `Y` only to letters still left in the copy, and crosses each one out as it is used.

```python exec
id: week-two-the-wrong-place-1
def mark(guess, secret):
    # your two-pass version here
    return "....."

print(mark("table", "cable") == ".GGGG")
print(mark("bleak", "cable") == "YYYY.")
print(mark("level", "cable") == "YY...")
print(mark("eerie", "cable") == "....G")
```

<details class="dl-hint"><summary>smaller steps</summary>

1. Make `left = list(secret)` and `result = ["."] * 5`.
2. First pass: where the letters match, set `result[position] = "G"` and `left[position] = None`.
3. Second pass: for each position that is not already `G`, check whether the letter is in `left`. If it is, mark `Y` and remove one copy of it from `left`.
4. At the end, `"".join(result)` turns the list into a string.

</details>

```solution
def mark(guess, secret):
    left = list(secret)
    result = ["."] * 5
    for position in range(5):
        if guess[position] == secret[position]:
            result[position] = "G"
            left[position] = None
    for position in range(5):
        if result[position] != "G" and guess[position] in left:
            result[position] = "Y"
            left.remove(guess[position])
    return "".join(result)

print(mark("table", "cable") == ".GGGG")
print(mark("level", "cable") == "YY...")
print(mark("eerie", "cable") == "....G")
```

**3.4** Write three more tests of your own that each check a different case. Which case was hardest to get right?

<!-- answer -->

## 4. Week Three: A Real Game

**4.1** Make a list of at least ten five-letter words, and pick the secret with `random.choice`. Put `import random` at the top.

<!-- answer -->

**4.2** Show the letters the player has tried so far, so they know which letters to avoid. Where should that list live, and when does it change?

<!-- answer -->

**4.3** At the end, print the secret word and the number of guesses used.

<!-- answer -->

## 5. Release and Review

**5.1** Give your game to another pair. Ask them to find a guess that your game marks wrongly. If they find one, add it to your tests before you fix it.

<!-- answer -->

## 6. More to Try

1. Refuse guesses that are not in your word list.
2. Keep a record of how many guesses each game took, and print it as a bar chart made of `#` symbols.
3. Allow words of any length the player chooses.
4. Show the alphabet with each letter marked by the best result it has had so far.

```python exec
id: more-to-try-1
import random
# your experiments here
```
