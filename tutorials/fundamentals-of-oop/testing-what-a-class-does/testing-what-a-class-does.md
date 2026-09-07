---
title: "Testing What a Class Does"
slug: testing-what-a-class-does
module: fundamentals-of-oop
module_title: "Fundamentals of Object Oriented Programming"
year: "2026-2027"
series: programming-with-objects
version: 2026.09.04.1
covers:
  a-bug-that-hides-in-another-class:
    covers: [FOOP-LO10]
  writing-a-test-for-one-method:
    covers: [FOOP-LO10]
  a-few-tests-run-together:
    covers: [FOOP-LO10]
---

# Testing What a Class Does

**Fundamentals of Object Oriented Programming**

Not every bug raises an error. Some just produce a number that is quietly
wrong, with nothing on the screen to say so. This tutorial finds one of
those inside a familiar class. It then builds a way to catch it that does
not depend on noticing the wrong number by eye.

## A Bug That Hides in Another Class

Here is `BankAccount` again, with one line changed from *Objects and
Classes*.

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

Run the cell above. `withdraw()` now compares `amount >= self.balance`
instead of `amount > self.balance`, so withdrawing the exact balance is
refused instead of leaving it at zero. Nothing crashes. No traceback
appears. A program that only ever withdraws less than the full balance
would never see this at all. The bug sits quietly inside `BankAccount`,
waiting for the one case that reaches it.

`Bank.total_balance()`, from *One Parent, Many Children*, would still add
up correctly here — the balance is only wrong, not missing. A bug like this
one hides best inside the class that owns it, in the code every other class
trusts without checking.

### Your turn

Run the cell above again and confirm the printed balance is `100.0`, not
`0.0`. Then find the one changed comparison and fix it back to what
*Objects and Classes* had.

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

## Writing a Test for One Method

Reading the printed balance and checking it by eye works for one account,
once. It does not scale, and it is easy to skip on a day when there are
five other things to check. `assert` checks a claim for you, and stops the
program with a clear message the moment the claim is false.

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

Run the cell above. `AssertionError: withdrawing the full balance should
leave 0.0` names exactly what went wrong, on the exact line that checks it.
Compare that to *A Bug That Hides in Another Class*, where the same bug
left nothing behind but a quietly wrong number. The message after the
comma is not decoration. It is what tells you, later, what the assertion
was actually checking, once the code around it has slipped from memory.

### Your turn

Fix the same bug as before: change `withdraw()`'s comparison back to
`amount > self.balance`. Run the cell again and confirm the `assert` no
longer raises anything.

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
2. An `assert` that raises nothing prints nothing by itself — the
   `print("Passed.")` line after it is what confirms the fix, since a
   cell with no output at all is easy to mistake for one that has not run.

</details>

## A Few Tests, Run Together

One `assert` catches one claim. A class usually makes several: depositing
raises the balance, withdrawing lowers it, withdrawing too much is refused.
Each claim can live inside its own small function, so a class with three
things to check gets three tests, run one after another.

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

Each `test_` function builds its own fresh `BankAccount`, so one test's
`withdraw()` can never leave a balance the next test trips over by
surprise. `"All tests passed."` only prints if every `assert` above it ran
without raising. That is the same guarantee one `assert` gives a single
claim, now covering everything the three functions check together.

### Your turn

Write a fourth test, `test_deposit_then_withdraw()`, that deposits `50.0`
into a fresh `100.0` account, withdraws `30.0`, and asserts the balance
ends at `120.0`. Add a call to it alongside the three calls above.

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

1. `test_deposit_then_withdraw()` needs no parameters, the same shape as
   the three tests above it.
2. Build the account, call `deposit(50.0)`, then call `withdraw(30.0)` —
   in that order, since the expected ending balance depends on both
   happening one after the other.
3. `assert account.balance == 120.0`, with a message saying what should be
   true, the same style every test above it already uses.

</details>

## Wrapping Up

In this tutorial:

- Not every bug raises an error. Some leave a class in a quietly wrong
  state, with nothing on the screen to say so until something much later
  depends on it.
- `assert claim, message` stops a program the moment `claim` is false. It
  names what broke on the line that checked it, rather than leaving the
  problem to surface somewhere else.
- A small `test_` function checks one claim about a class, using its own
  fresh object so one test's changes never leak into the next. Several of
  them, called one after another, cover everything a class promises to do.

### Reflection

A few sentences about this tutorial, whenever you are ready. The bug in
this tutorial never crashed anything. What would have to be true of a bug
for it to be worse than one that crashes right away?

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
