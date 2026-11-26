---
title: "A Number-Guessing Game: Higher, Lower, and a Computer That Guesses"
year: "2026-2027"
version: 2026.11.26.1
covers:
  3-week-two-the-computer-guesses:
    covers: [PDP-LO2]
  4-week-three-which-strategy-is-best:
    covers: [PDP-LO2, PDP-LO8]
---

# A Number-Guessing Game: Higher, Lower, and a Computer That Guesses

The computer thinks of a number from 1 to 100, and you guess. After each guess it says "higher" or "lower". The game takes one session to build. The interesting part comes next, when we turn the game around: you think of a number, and the computer has to find it in as few guesses as possible.

The project has three stages, about one week each. Each stage ends with a program that works.

There are questions on this page to answer in words as well as in code. The **+ Text** button between cells adds a text cell where you can write your answers.

## 1. Plan First

**1.1** Play the game with your partner on paper, with one person thinking of a number from 1 to 100. Count the guesses. Then swap roles. Did either of you use a plan?

<!-- answer -->

**1.2** Write the user flow for the game, including what happens when the person types something that is not a number.

<!-- answer -->

## 2. Week One: Higher or Lower

**2.1** Run this cell a few times. What changes, and what stays the same?

```python exec
id: week-one-higher-or-lower-1
import random
secret = random.randint(1, 100)
print(secret)
```

<!-- answer -->

**2.2** Write the game. It picks a secret number, asks for guesses, says "higher" or "lower" after each one, and stops when the guess is right. At the end it prints how many guesses it took.

```python exec
id: week-one-higher-or-lower-2
# your game here
```

**2.3** Add a limit of seven guesses. Is seven enough to find any number from 1 to 100, if you play well? Keep your answer, because section 3 checks it.

<!-- answer -->

## 3. Week Two: The Computer Guesses

Now you think of a number, and the computer guesses. You answer each guess with `h` for higher, `l` for lower, or `y` when it is right.

**3.1** A computer that guesses at random is slow. A better plan is to guess the middle of the numbers that are still possible, and then ignore the half that cannot hold the answer. This plan is called binary search. With numbers from 1 to 100, what is the first guess? If the answer is "higher", which numbers are still possible, and what is the next guess?

<!-- answer -->

**3.2** Write the computer guesser. Keep two variables, `low` and `high`, for the smallest and largest numbers still possible. Each guess is the middle, `(low + high) // 2`.

```python exec
id: week-two-the-computer-guesses-1
# your computer guesser here
```

<details class="dl-hint"><summary>smaller steps</summary>

1. Start with `low = 1` and `high = 100`.
2. Guess `(low + high) // 2` and ask the person for `h`, `l` or `y`.
3. If the answer is `h`, the secret is bigger than the guess, so `low` becomes the guess plus 1.
4. If the answer is `l`, which variable changes, and to what?

</details>

**3.3** Try to make the computer use more than seven guesses. Can you? What happens if you lie to it?

<!-- answer -->

## 4. Week Three: Which Strategy Is Best?

So far a person answers every guess. To test a strategy many times, the program needs to answer for itself.

**4.1** Write `guesses_needed(secret)`, which plays binary search against a secret it already knows and hands back how many guesses it took.

```python exec
id: week-three-which-strategy-is-best-1
def guesses_needed(secret):
    # your code here
    return 0

print(guesses_needed(50))
print(guesses_needed(1))
print(guesses_needed(100))
```

```solution
def guesses_needed(secret):
    low = 1
    high = 100
    count = 0
    while True:
        guess = (low + high) // 2
        count = count + 1
        if guess == secret:
            return count
        elif guess < secret:
            low = guess + 1
        else:
            high = guess - 1

print(guesses_needed(50))
print(guesses_needed(1))
print(guesses_needed(100))
```

**4.2** Call `guesses_needed` for every secret from 1 to 100. What is the largest number of guesses? Was your answer to 2.3 right?

<!-- answer -->

**4.3** Write a second strategy that guesses at random from the numbers still possible, and compare its average number of guesses with binary search.

<!-- answer -->

**4.4** What happens to the largest number of guesses when the range is 1 to 1000? 1 to a million? Make the range an argument of your function to find out.

<!-- answer -->

## 5. Release and Review

**5.1** Play your game against another pair's computer guesser, and theirs against yours. Did either one break when you typed something unexpected?

<!-- answer -->

## 6. More to Try

1. Let the person choose the range before the game starts.
2. Keep a best score, and say when it is beaten.
3. Draw the range that is still possible as a bar that shrinks after each guess.
4. Binary search is also how a program finds a word in a sorted list. Try it on a list of words.

```python exec
id: more-to-try-1
import random
# your experiments here
```
