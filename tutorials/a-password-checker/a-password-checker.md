---
title: "A Password Checker: Rules, Scores and a Generator"
year: "2026-2027"
version: 2026.11.26.1
covers:
  2-week-one-one-rule-one-function:
    covers: [PDP-LO8, PDP-LO10]
  3-week-two-a-score-and-advice:
    covers: [PDP-LO6]
  5-release-and-review:
    covers: [PDP-LO11]
---

# A Password Checker: Rules, Scores and a Generator

Many sign-up forms check a new password before they accept it: it must be long enough, have a number in it, and so on. On this page we build that checker for the command line. Then we give each password a score with advice, and finally we write a generator that makes strong passwords. If you built the login, you can add the checker to it.

The project has three stages, about one week each. Each stage ends with a program that works. Each rule goes in its own small function, so you can test every rule on its own.

There are questions on this page to answer in words as well as in code. The **+ Text** button between cells adds a text cell where you can write your answers.

## 1. Plan First

**1.1** Write down five rules a strong password might have to follow. Then write a password that breaks each rule but still looks strong to a person.

<!-- answer -->

**1.2** Which rules make a password harder to guess, and which only make it harder to remember? Talk it over and write down what you decided.

<!-- answer -->

## 2. Week One: One Rule, One Function

**2.1** Predict what each line prints, then run the cell.

```python exec
id: week-one-one-rule-one-function-1
password = "Cable42!"
print(len(password))
print("7".isdigit(), "a".isupper(), "A".isupper(), "!".isalnum())
for character in password:
    print(character, character.isdigit())
```

<!-- answer -->

**2.2** Write four functions. Each one takes a password and hands back `True` or `False`:

1. `long_enough(password)` checks for at least 10 characters.
2. `has_digit(password)` checks for at least one digit.
3. `has_upper(password)` checks for at least one capital letter.
4. `has_symbol(password)` checks for at least one character that is not a letter or a digit.

```python exec
id: week-one-one-rule-one-function-2
def has_digit(password):
    # your code here
    return False

print(has_digit("Cable42!") == True)
print(has_digit("Cable!") == False)
print(has_digit("") == False)
```

```solution
def has_digit(password):
    for character in password:
        if character.isdigit():
            return True
    return False

print(has_digit("Cable42!") == True)
print(has_digit("Cable!") == False)
print(has_digit("") == False)
```

**2.3** Write a test cell like the one above for each of your other three functions, with at least three tests each, including an empty password.

```python exec
id: week-one-one-rule-one-function-3
# your functions and tests here
```

## 3. Week Two: A Score and Advice

**3.1** Write `check(password)`, which uses your four functions. It prints one line of advice for each rule the password breaks, such as "Add a capital letter", and then a score out of 4.

<!-- answer -->

**3.2** Some passwords pass every rule and are still easy to guess, such as `Password123!`. Make a list of ten common passwords, and add a rule that refuses any password on the list. Should the check ignore capital letters?

<!-- answer -->

**3.3** Add your checker to the login project, or write a small sign-up command that keeps asking for a new password until it passes.

<!-- answer -->

## 4. Week Three: A Generator

**4.1** Predict what this prints, then run it a few times.

```python exec
id: week-three-a-generator-1
import random
letters = "abcdefghijklmnopqrstuvwxyz"
print(random.choice(letters))
print(letters.upper())
print("".join([random.choice(letters) for count in range(8)]))
```

<!-- answer -->

**4.2** Write `generate(length)`, which makes a random password of that length from letters, capital letters, digits and symbols. Test it with your `check` function a hundred times. Does every password pass?

<!-- answer -->

**4.3** If some generated passwords fail, why? Change `generate` so every password it makes is sure to pass.

<!-- answer -->

**4.4** Another kind of strong password is four random words joined together, like `cable-orbit-lemon-switch`. Write a generator for that kind too. Which kind would you rather type?

<!-- answer -->

## 5. Release and Review

**5.1** Read another pair's rule functions without running them. Can you tell what each one does from its name alone? Suggest one better name or one useful comment.

<!-- answer -->

**5.2** Ask the other pair to find a password your checker scores 4 out of 4 that a person could still guess. What rule would catch it?

<!-- answer -->

## 6. More to Try

1. Refuse a password that contains the username.
2. Refuse three of the same character in a row, like `aaa`.
3. Show the score as a bar that fills up and changes from `weak` to `strong`.
4. Count how many different passwords of length 8 your generator could make. How long would it take to try them all at a million a second?

```python exec
id: more-to-try-1
import random
# your experiments here
```
