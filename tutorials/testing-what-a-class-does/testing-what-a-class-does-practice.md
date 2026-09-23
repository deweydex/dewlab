---
title: "Testing a class with assert — Practice"
practice_for: testing-what-a-class-does
year: "2026-2027"
version: 2026.09.04.1
---

# Testing a class with assert — Practice

The answers are hidden until you open them. Many of these problems ask
you to predict an output before you run anything. Try not to check first.
When a prediction is wrong, finding out why teaches you more than a lucky
guess does.

## A bug that hides in another class

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

**1.** `deposit()` above has a bug: it uses `-` where it should use `+`.
Predict what the cell prints before you run it. Does anything crash?

<details class="dl-answer"><summary>answer</summary>

It prints `50.0`, not `150.0`. Nothing crashes. A deposit that subtracts
is still valid Python. The arithmetic is wrong, but Python cannot know
that.

To fix it, change `self.balance = self.balance - amount` to
`self.balance = self.balance + amount`.

</details>

**2.** Someone looks at the cell above quickly. They see no error and no
red text, and they move on. Why was this bug easy to miss?

<details class="dl-answer"><summary>answer</summary>

Nothing about the run looks wrong. `deposit()` runs to the end and a
number is printed. The number is wrong, but it looks ordinary. We notice
a bug only when something shows us it is there, and this bug shows no
traceback at all.

</details>

**3.** Suppose `withdraw()` had a similar bug, with `+` instead of `-`.
Then a balance would grow every time money left the account. Would
`Bank.total_balance()`, from [Composition: objects inside other
objects](tutorial:objects-inside-objects), raise an error because of a
bug like this?

<details class="dl-answer"><summary>answer</summary>

No. `total_balance()` adds up whatever `balance` each account holds right
now. It has no way to know that a withdrawal should have lowered one of
them. The wrong total looks like an ordinary number, and nothing marks it
as strange.

</details>

## Writing a test for one method

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
`50.0`, but the `assert` expects `150.0`. The claim is false, so the
program stops on that line.

</details>

**5.** Suppose the `assert` had no message: only
`assert account.balance == 150.0`. What would the cell show then?

<details class="dl-answer"><summary>answer</summary>

It would still show `AssertionError`, but with no text after it. The
traceback still shows the line where the check failed. Without a message,
you only learn "something on this line is false". With a message, you
learn what that line was checking. That matters most weeks later, when
you no longer remember the code.

</details>

**6.** Write an `assert` that checks that a new `BankAccount("Ben", 0.0)`
starts with a balance of exactly `0.0`. Give it a message that says what
it checks.

<details class="dl-answer"><summary>answer</summary>

```python
account = BankAccount("Ben", 0.0)
assert account.balance == 0.0, "a new account should start at the balance it was given"
```

On a correct `BankAccount`, this `assert` passes and prints nothing. Every
`assert` behaves this way when its claim is true. No output means the
check passed.

</details>

## A few tests, run together

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

**7.** Write `test_withdraw_leaves_balance_at_zero()`. It should check
that withdrawing an account's exact balance leaves it at `0.0`. Add a call
to it next to the two calls above.

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

It has the same shape as the two tests already there. First create a new
account. Then use it. Then `assert` what should be true afterwards.

</details>

**8.** Each `test_` function above creates its own
`BankAccount("Alice", 100.0)`. The tests do not share one account. What
would go wrong if `test_deposit()` and `test_withdraw_refuses_too_much()`
shared a single account?

<details class="dl-answer"><summary>answer</summary>

The second test would start from the balance the first test left behind,
not from `100.0`. If `test_withdraw_refuses_too_much()` ran after
`test_deposit()` on a shared account, the starting balance would be
`150.0`. Withdrawing `150.0` would then succeed and leave `0.0`, so its
`assert` would fail. You would have to rewrite that test because of what
ran before it.

</details>

**9.** Suppose `withdraw()` had the `>=` bug from the first section of the
tutorial. It refuses a withdrawal that would leave exactly `0.0`. Which
of the three tests would fail, and which would still pass?

<details class="dl-answer"><summary>answer</summary>

`test_withdraw_leaves_balance_at_zero()` would fail. It withdraws the
exact balance and expects `0.0`, and the `>=` bug refuses that
withdrawal.

`test_deposit()` and `test_withdraw_refuses_too_much()` would still pass.
Neither one withdraws an amount equal to the balance.

`"All tests passed."` would never print. The failing `assert` stops the
program before it reaches that line.

</details>
