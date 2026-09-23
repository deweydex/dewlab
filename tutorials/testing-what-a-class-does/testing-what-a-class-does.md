---
title: "Testing a class with assert"
year: "2026-2027"
version: 2026.09.04.1
covers:
  a-bug-that-hides-in-another-class:
    covers: [FOOP-LO10]
  writing-a-test-for-one-method:
    covers: [FOOP-LO10]
  a-few-tests-run-together:
    covers: [FOOP-LO10]
---

# Testing a class with assert

Not every bug raises an error. Some bugs only produce a wrong number, and
nothing on the screen says it is wrong. How would you notice a bug like
that? On this page we:

- find a bug of this kind inside a class we know well
- use `assert` to make Python check a result for us
- write small test functions that check everything a class promises

## A bug that hides in another class

Here is `BankAccount` again, with one line changed from the version in
[Encapsulation: keeping an object's data behind its
methods](tutorial:keeping-details-inside-an-object). The comment says the
balance should be `0.0`. What do you think the cell prints? Run it to
check.

```python exec
id: a-bug-that-hides-in-another-class-1
class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        self.balance = self.balance + amount

    def withdraw(self, amount):
        if amount >= self.balance:
            print("Refused: not enough balance.")
            return
        self.balance = self.balance - amount


account = BankAccount("Alice", 100.0)
account.withdraw(100.0)
print(account.balance)   # should be 0.0
```

The cell prints `Refused: not enough balance.` and then `100.0`.

`withdraw()` now compares `amount >= self.balance`. The original compared
`amount > self.balance`. With `>=`, a withdrawal of the exact balance is
refused, so the balance stays at `100.0` when it should drop to `0.0`.

Nothing crashes, and no traceback appears. A program that never withdraws
the full balance would never show the bug at all. The bug waits inside
`BankAccount` for the one case that reaches it.

Other classes cannot see it either. A `Bank` from [Composition: objects
inside other objects](tutorial:objects-inside-objects) would add up this
balance without any problem. The balance is wrong, but it is not missing.
Bugs like this hide best in a class that every other class trusts without
checking.

### Your turn

1. In the cell below, find the comparison in `withdraw()` that changed.
2. Change it back to the comparison the original `BankAccount` had.
3. Run the cell. Does it print `0.0` now?

```python exec
id: a-bug-that-hides-in-another-class-2
expect: account.balance == 0.0
class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        self.balance = self.balance + amount

    def withdraw(self, amount):
        if amount >= self.balance:
            print("Refused: not enough balance.")
            return
        self.balance = self.balance - amount

# Fix the comparison in withdraw(), then run this cell
account = BankAccount("Alice", 100.0)
account.withdraw(100.0)
print(account.balance)   # should be 0.0 once the fix is in
```

```hint
after: 4 runs
What does the cell print, and what did the comment say it should print?
The two numbers differ because of one comparison inside `withdraw()`. Read
that `if` line aloud. When `amount` is exactly equal to the balance, which
branch does it take, and which one did you want?
```

## Writing a test for one method

We can check a printed balance by eye for one account, once. With many
accounts and many methods, that takes a long time, and on a busy day it
is easy to skip. Can Python do the checking for us?

The `assert` statement does this job. An `assert` checks that a claim is
true. If the claim is false, it stops the program with an
`AssertionError` and a message you choose.

The cell below has the same `>=` bug as before. It is meant to fail. What
do you think the error will say? Run it to check.

```python exec
id: writing-a-test-for-one-method-1
class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        self.balance = self.balance + amount

    def withdraw(self, amount):
        if amount >= self.balance:
            print("Refused: not enough balance.")
            return
        self.balance = self.balance - amount


account = BankAccount("Alice", 100.0)
account.withdraw(100.0)
assert account.balance == 0.0, "withdrawing the full balance should leave 0.0"
```

The error is `AssertionError: withdrawing the full balance should leave
0.0`. It says exactly what went wrong, and it points at the line that
checked it. In the last section, the same bug only gave us a wrong number
with no warning.

The message after the comma matters. Weeks later, when you have forgotten
the code around it, the message tells you what the `assert` was checking.

### Your turn

1. Fix the same bug again: change the comparison in `withdraw()` back to
   `amount > self.balance`.
2. Run the cell. Does the `assert` still stop the program?

```python exec
id: writing-a-test-for-one-method-2
expect: account.balance == 0.0
class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        self.balance = self.balance + amount

    def withdraw(self, amount):
        if amount >= self.balance:
            print("Refused: not enough balance.")
            return
        self.balance = self.balance - amount

# Fix the comparison in withdraw(), then run this cell
account = BankAccount("Alice", 100.0)
account.withdraw(100.0)
assert account.balance == 0.0, "withdrawing the full balance should leave 0.0"
print("Passed.")
```

```hint
after: 3 identical errors
The `assert` raised again. What does the message after the comma say
should be true? Add `print(account.balance)` on the line before the
`assert` and run once more. Is that the number you expected, and if not,
which method changed it last?
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The bug is the same one from the last section: `>=` should be `>`.
2. An `assert` that passes prints nothing. The `print("Passed.")` line
   after it shows that the fix worked. Without it, a cell with no output
   is easy to mistake for a cell that has not run.

</details>

## A few tests, run together

One `assert` checks one claim. A class usually makes several claims:

- depositing raises the balance
- withdrawing lowers it
- withdrawing too much is refused

We can put each claim in its own small function, called a test. Here, a
test is a function that sets up an object, uses it, and checks the
result with `assert`. (If you have written test functions in [Designing
and testing good functions](tutorial:building-reusable-tools), this is
the same idea, used on a class.) A class with three claims gets three
tests, run one after another.

```python exec
id: a-few-tests-run-together-1
class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        self.balance = self.balance + amount

    def withdraw(self, amount):
        if amount > self.balance:
            print("Refused: not enough balance.")
            return
        self.balance = self.balance - amount


def test_deposit():
    account = BankAccount("Alice", 100.0)
    account.deposit(50.0)
    assert account.balance == 150.0, "deposit should raise the balance"


def test_withdraw_leaves_balance_at_zero():
    account = BankAccount("Alice", 100.0)
    account.withdraw(100.0)
    assert account.balance == 0.0, "withdrawing the full balance should leave 0.0"


def test_withdraw_refuses_too_much():
    account = BankAccount("Alice", 100.0)
    account.withdraw(150.0)
    assert account.balance == 100.0, "an over-large withdrawal should change nothing"


test_deposit()
test_withdraw_leaves_balance_at_zero()
test_withdraw_refuses_too_much()
print("All tests passed.")
```

Each `test_` function builds its own new `BankAccount`. So one test's
`withdraw()` can never leave behind a balance that confuses the next test.

`"All tests passed."` prints only if every `assert` above it passed. One
`assert` checks one claim. This last line tells us that all three tests
passed together.

### Your turn

1. Write a fourth test, `test_deposit_then_withdraw()`.
2. In it, create a new account with `100.0`, deposit `50.0`, then
   withdraw `30.0`.
3. Assert that the balance ends at `120.0`.
4. Call your new test next to the call to `test_deposit()`, and run the
   cell.

```python exec
id: a-few-tests-run-together-2
expect: callable(test_deposit_then_withdraw)
class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        self.balance = self.balance + amount

    def withdraw(self, amount):
        if amount > self.balance:
            print("Refused: not enough balance.")
            return
        self.balance = self.balance - amount


def test_deposit():
    account = BankAccount("Alice", 100.0)
    account.deposit(50.0)
    assert account.balance == 150.0, "deposit should raise the balance"

# Write test_deposit_then_withdraw() here

test_deposit()
# Call test_deposit_then_withdraw() here
print("All tests passed.")
```

```hint
after: 3 identical errors
Which line is the error pointing at: the body of your new function, or
the call to it? If Python says a name is not defined, is the `def` line
spelled the same as the call, and does it come before the call? If it is
an `AssertionError`, what did you expect the balance to be after
depositing `50.0` into `100.0` and withdrawing `30.0`? Write that number
down, then compare it with the one in your `assert`.
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. `test_deposit_then_withdraw()` needs no parameters. It has the same
   shape as `test_deposit()` above it.
2. Create the account. Then call `deposit(50.0)`. Then call
   `withdraw(30.0)`. The order matters, because the final balance depends
   on both steps.
3. Write `assert account.balance == 120.0`, with a message that says what
   should be true, as the other tests do.

</details>

## Wrapping up

On this page:

- Not every bug raises an error. Some bugs leave an object with a wrong
  value, and nothing on the screen says so. The problem shows up later,
  when other code depends on that value.
- `assert claim, message` stops the program as soon as `claim` is false.
  The message says what broke, on the line that checked it.
- A test is a small function that checks one claim about a class. Each
  test uses its own new object, so one test's changes never affect the
  next. Several tests, called one after another, check everything a class
  promises to do.

### Reflection

Write a few sentences about this page, whenever you are ready. The bug on
this page never crashed anything. When is a bug that does not crash worse
than one that crashes right away?

Double-click this cell to write your thoughts:

## Where to Read More

Downey, A. B. (2015). *Think Python: How to Think Like a Computer
Scientist* (2nd ed.). Green Tea Press. Section 6.7 covers checking a
function's own preconditions with `assert`, the same tool this tutorial
uses on a class's methods instead. Free at
<https://greenteapress.com/wp/think-python-2e/>.

Python Software Foundation. *The Python Tutorial*, section 8.3: Handling
Exceptions. <https://docs.python.org/3/tutorial/errors.html#handling-exceptions>.
Covers `AssertionError` alongside the other exceptions Python raises, and
what a program can do once one is caught rather than letting it stop
everything.

Real Python. *Getting Started With Testing in Python*.
<https://realpython.com/python-testing/>. Picks up where this tutorial's
`test_` functions leave off, with the testing libraries a larger project
reaches for once there are more than a handful.
