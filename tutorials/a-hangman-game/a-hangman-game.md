---
title: "A Hangman Game: Blanks, Guesses and Lives"
year: "2026-2027"
version: 2026.11.26.1
covers:
  1-plan-first:
    covers: [PDP-LO6]
  3-week-two-lives-and-repeats:
    covers: [PDP-LO6]
  5-release-and-review:
    covers: [PDP-LO10]
---

# A Hangman Game: Blanks, Guesses and Lives

In hangman, one player thinks of a word and shows only a blank for each letter. The other player guesses one letter at a time. A right guess fills in every blank where that letter belongs. A wrong guess costs a life. On this page the computer holds the word and the person guesses.

Hangman and the word-guessing game on another page both hide a word, but they ask different questions. Hangman asks about one letter at a time. The word-guessing game asks about a whole word.

The project has three stages, about one week each. Each stage ends with a game that works.

There are questions on this page to answer in words as well as in code. The **+ Text** button between cells adds a text cell where you can write your answers.

## 1. Plan First

**1.1** Play a round on paper with your partner. Write down everything the guesser can see after each turn.

<!-- answer -->

**1.2** Write pseudocode for one whole game. What does the program need to remember between turns?

<!-- answer -->

## 2. Week One: Blanks and Letters

**2.1** Predict what each line prints, then run the cell.

```python exec
id: week-one-blanks-and-letters-1
secret = "router"
guessed = ["r", "e"]
print("o" in secret)
print(secret.count("r"))
print(" ".join(["_", "_", "_"]))
for letter in secret:
    print(letter, letter in guessed)
```

<!-- answer -->

**2.2** Write `show_word(secret, guessed)`, which hands back the word with a blank for each letter not guessed yet. `show_word("router", ["r", "e"])` should hand back `"r _ _ _ e r"`.

```python exec
id: week-one-blanks-and-letters-2
def show_word(secret, guessed):
    # your code here
    return ""

print(show_word("router", ["r", "e"]))
print(show_word("router", []))
```

```solution
def show_word(secret, guessed):
    shown = []
    for letter in secret:
        if letter in guessed:
            shown.append(letter)
        else:
            shown.append("_")
    return " ".join(shown)

print(show_word("router", ["r", "e"]))
```

**2.3** Write a game loop that asks for a letter, adds it to `guessed`, and shows the word. The game ends when no blanks are left.

```python exec
id: week-one-blanks-and-letters-3
# your game here
```

## 3. Week Two: Lives and Repeats

**3.1** Give the player six lives. A wrong letter costs one life. The game ends with a win when the word is complete, or with a loss when the lives run out. Print the word at the end either way.

<!-- answer -->

**3.2** Guess the same wrong letter twice. Does it cost two lives? Should it? Make the game say "You already tried that" instead.

<!-- answer -->

**3.3** What should happen when the player types `ab`, `7`, `R` or nothing at all? Write your answers as a test plan, and then make the code match it.

<!-- answer -->

<details class="dl-hint"><summary>smaller steps</summary>

1. Use `strip` and `lower` on the guess first.
2. Check the length with `len`, and use `isalpha` to check that it is a letter.
3. Put each check before the line that costs a life.

</details>

## 4. Week Three: The Drawing and the Words

**4.1** Draw the hangman picture in stages with text, one stage for each life lost. Keep the stages in a list, so `stages[0]` is the empty frame and `stages[6]` is the whole figure. Print the right stage after each guess.

<!-- answer -->

**4.2** Make a list of at least ten words on a theme, such as networking words. Pick the secret with `random.choice`. Put `import random` at the top.

<!-- answer -->

**4.3** Show the wrong letters tried so far, in alphabetical order. The function `sorted` helps.

<!-- answer -->

## 5. Release and Review

**5.1** Give your game to another pair and ask them to break it with strange guesses. Add each one that worked to your test plan from 3.3, then fix it.

<!-- answer -->

## 6. More to Try

1. Let two people play: one types the secret word and the other guesses.
2. Add a hint that reveals one letter but costs a life.
3. Allow words with spaces, such as `access point`, and show the space instead of a blank.
4. Keep a score across several rounds.

```python exec
id: more-to-try-1
import random
# your experiments here
```
