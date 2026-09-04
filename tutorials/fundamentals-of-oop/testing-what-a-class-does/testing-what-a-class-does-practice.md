---
title: "Testing What a Class Does — Practice"
slug: testing-what-a-class-does-practice
practice_for: testing-what-a-class-does
module: fundamentals-of-oop
module_title: "Fundamentals of Object Oriented Programming"
year: "2026-2027"
series: programming-with-objects
version: 2026.09.04.1
---

# Testing What a Class Does — Practice

Answers are folded. Several of these ask you to predict an output before
running anything. Resist checking first — being wrong and finding out why
is worth more than being right by accident.

## A Bug That Hides in Another Class

```python exec
id: a-bug-that-hides-in-another-class-1
class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        self.balance = self.balance - amount


account = BankAccount("Alice", 100.0)
account.deposit(50.0)
print(account.balance)
```

**1.** `deposit()` above has a bug: `-` where it should be `+`. Predict the
cell's output before running it. Does anything crash?

<details class="dl-answer"><summary>answer</summary>

`50.0`, not `150.0`. Nothing crashes — a deposit that subtracts instead of
adding is still valid Python, just the wrong arithmetic.

Fix it by changing `self.balance = self.balance - amount` to `self.balance
= self.balance + amount`.

</details>

**2.** A reader glances at the cell above, sees no error and no red text,
and moves on. What made this bug easy to miss?

<details class="dl-answer"><summary>answer</summary>

Nothing about running the cell looks wrong. `deposit()` still runs to
completion and prints a number — just the wrong one. A bug has to announce
itself somehow to be noticed, and this one produces ordinary-looking output
instead of a traceback.

</details>

**3.** A `withdraw()` with a similar bug (`+` instead of `-`) would let a
balance grow every time money left the account. Would `Bank.total_balance()`,
from *One Parent, Many Children*, raise an error because of a bug like
this?

<details class="dl-answer"><summary>answer</summary>

No. `total_balance()` only adds up whatever `balance` each account
currently holds — it has no way to know a withdrawal should have lowered
one of them. The wrong total it reports looks like an ordinary number,
with nothing about it flagged as suspicious.

</details>

## Writing a Test for One Method

```python exec
id: writing-a-test-for-one-method-1
class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        self.balance = self.balance - amount


account = BankAccount("Alice", 100.0)
account.deposit(50.0)
assert account.balance == 150.0, "deposit should raise the balance"
```

**4.** Predict what happens when the cell above runs.

<details class="dl-answer"><summary>answer</summary>

`AssertionError: deposit should raise the balance`. `account.balance` is
`50.0`, not the `150.0` the `assert` expects, so the claim is false and the
program stops right there.

</details>

**5.** What would the cell above show instead if the `assert` had no
message — just `assert account.balance == 150.0`?

<details class="dl-answer"><summary>answer</summary>

Still `AssertionError`, but with no text after it — just the line number
where the check failed. The message argument is what turns "something on
this line is false" into "here is what that line was actually checking."
That matters most once enough time has passed that the code itself no
longer explains it at a glance.

</details>

**6.** Write an `assert` that checks a fresh `BankAccount("Ben", 0.0)`
starts with a balance of exactly `0.0`, with a message saying what it
checks.

<details class="dl-answer"><summary>answer</summary>

```python
account = BankAccount("Ben", 0.0)
assert account.balance == 0.0, "a new account should start at the balance it was given"
```

This one passes silently on a correct `BankAccount`, the same way every
`assert` does when its claim holds. No output at all is what "the check
passed" looks like.

</details>

## A Few Tests, Run Together

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


def test_withdraw_refuses_too_much():
    account = BankAccount("Alice", 100.0)
    account.withdraw(150.0)
    assert account.balance == 100.0, "an over-large withdrawal should change nothing"


test_deposit()
test_withdraw_refuses_too_much()
print("All tests passed.")
```

**7.** Write `test_withdraw_leaves_balance_at_zero()`, checking that
withdrawing an account's exact balance leaves it at `0.0`. Add a call to
it alongside the two calls above.

<details class="dl-answer"><summary>answer</summary>

```python
def test_withdraw_leaves_balance_at_zero():
    account = BankAccount("Alice", 100.0)
    account.withdraw(100.0)
    assert account.balance == 0.0, "withdrawing the full balance should leave 0.0"


test_deposit()
test_withdraw_refuses_too_much()
test_withdraw_leaves_balance_at_zero()
print("All tests passed.")
```

Same shape as the two tests already there: build a fresh account, act on
it, `assert` what should be true afterward.

</details>

**8.** Each `test_` function above builds its own `BankAccount("Alice",
100.0)`, rather than sharing one account across all three. What would go
wrong if `test_deposit()` and `test_withdraw_refuses_too_much()` shared a
single account instead?

<details class="dl-answer"><summary>answer</summary>

Whichever test ran second would start from whatever balance the first one
left behind, not `100.0`. `test_withdraw_refuses_too_much()`, run after `test_deposit()` on a shared
account, would check against a starting balance of `150.0` rather than
`100.0`. Its own `assert` would need rewriting just because of what ran
before it.

</details>

**9.** Suppose `withdraw()` had the `>=` bug from *A Bug That Hides in
Another Class*, refusing a withdrawal that exactly empties the account.
Which of the three tests above would fail, and which would still pass?

<details class="dl-answer"><summary>answer</summary>

`test_withdraw_leaves_balance_at_zero()` would fail — it withdraws the
exact balance and expects `0.0`, which the `>=` bug refuses.
`test_deposit()` and `test_withdraw_refuses_too_much()` would still pass,
since neither withdraws an amount equal to the balance. `"All tests
passed."` would never print, since one `assert` failing stops the program
before reaching it.

</details>
