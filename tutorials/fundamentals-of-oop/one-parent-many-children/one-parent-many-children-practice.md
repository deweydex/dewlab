---
title: "One Parent, Many Children — Practice"
slug: one-parent-many-children-practice
practice_for: one-parent-many-children
module: fundamentals-of-oop
module_title: "Fundamentals of Object Oriented Programming"
year: "2026-2027"
series: programming-with-objects
version: 2026.09.04.1
---

# One Parent, Many Children — Practice

Answers are folded. Several of these ask you to predict an output before
running anything. Resist checking first — being wrong and finding out why
is worth more than being right by accident.

## Another Kind of Account

```python exec
id: another-kind-of-account-1
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


class CheckingAccount(BankAccount):
    def __init__(self, owner, balance, overdraft_limit):
        super().__init__(owner, balance)
        self.overdraft_limit = overdraft_limit

    def withdraw(self, amount):
        if amount > self.balance + self.overdraft_limit:
            print("Refused: over the overdraft limit.")
            return
        self.balance = self.balance - amount


checking = CheckingAccount("Ben", 200.0, 100.0)
checking.withdraw(300.0)
print(checking.balance)
```

**1.** Predict the cell's output before running it. Then change `300.0` to
`301.0` and predict again.

<details class="dl-answer"><summary>answer</summary>

At `300.0`: `-100.0`. The withdrawal is allowed since `300.0` is not more
than `self.balance + self.overdraft_limit` (`200.0 + 100.0 = 300.0`).

At `301.0`: `Refused: over the overdraft limit.` then `200.0` — one cent
over the limit and the whole withdrawal is refused, balance unchanged.

</details>

**2.** `SavingsAccount`'s fee-charging `withdraw()`, from *Objects and
Classes*, calls `super().withdraw(amount + 2.0)`. `CheckingAccount`'s
`withdraw()` above does not call `super().withdraw()` at all. Why not?

<details class="dl-answer"><summary>answer</summary>

The parent's own check, `amount > self.balance`, is not the check a
`CheckingAccount` needs. It would refuse every withdrawal that dips into
the overdraft, which is exactly what `CheckingAccount` exists to allow.
`SavingsAccount`'s fee only changes the *amount* being checked, so the
parent's own check still applies. `CheckingAccount` needs a different
check entirely, so it writes its own rather than adjusting what it passes
to the parent's.

</details>

**3.** Write a `savings_withdraw_test` cell: create a `CheckingAccount`
with balance `50.0` and overdraft limit `0.0`. Predict what `withdraw(50.0)`
and then `withdraw(1.0)` do, then run it and check.

<details class="dl-answer"><summary>answer</summary>

```python
checking = CheckingAccount("Ben", 50.0, 0.0)
checking.withdraw(50.0)
print(checking.balance)   # 0.0
checking.withdraw(1.0)
print(checking.balance)   # still 0.0, refused
```

An overdraft limit of `0.0` behaves exactly like a plain `BankAccount` —
`amount > self.balance + 0.0` is the same comparison `BankAccount.withdraw()`
makes. `CheckingAccount` does not need a separate case for "no overdraft
at all"; the general formula already covers it.

</details>

## Many Kinds, One Loop

```python exec
id: many-kinds-one-loop-1
class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance

    def withdraw(self, amount):
        if amount > self.balance:
            print("Refused: not enough balance.")
            return
        self.balance = self.balance - amount


class CheckingAccount(BankAccount):
    def __init__(self, owner, balance, overdraft_limit):
        super().__init__(owner, balance)
        self.overdraft_limit = overdraft_limit

    def withdraw(self, amount):
        if amount > self.balance + self.overdraft_limit:
            print("Refused: over the overdraft limit.")
            return
        self.balance = self.balance - amount


plain = BankAccount("Cara", 80.0)
checking = CheckingAccount("Ben", 80.0, 20.0)

for account in [plain, checking]:
    account.withdraw(90.0)
    print(account.owner, account.balance)
```

**4.** Predict both lines of output before running the cell.

<details class="dl-answer"><summary>answer</summary>

`Refused: not enough balance.` then `Cara 80.0` — `90.0` is more than
`plain`'s balance, with no overdraft to allow it.

`Ben -10.0` — `90.0` is within `checking`'s `80.0 + 20.0 = 100.0` limit.

</details>

**5.** The loop above calls `account.withdraw(90.0)` without ever checking
which class `account` actually is. In your own words: what is
*polymorphism*, and where does it show up in this cell?

<details class="dl-answer"><summary>answer</summary>

Polymorphism is one method call running a different version of the method
depending on which class the object actually belongs to. `account.withdraw(90.0)`
is the same line for both objects in the loop. It runs `BankAccount`'s own
check for `plain` and `CheckingAccount`'s own check for `checking`, with
the loop never needing to know which.

</details>

**6.** Add a `SavingsAccount` (from *Objects and Classes*) to the list
above, alongside `plain` and `checking`. Does the loop still work with no
changes to its own code?

<details class="dl-answer"><summary>answer</summary>

Yes.

```python
class SavingsAccount(BankAccount):
    def __init__(self, owner, balance, interest_rate):
        super().__init__(owner, balance)
        self.interest_rate = interest_rate


savings = SavingsAccount("Priya", 200.0, 0.1)

for account in [plain, checking, savings]:
    account.withdraw(90.0)
    print(account.owner, account.balance)
```

`SavingsAccount` inherits `withdraw()` unchanged from `BankAccount`, so it
behaves like `plain` did. The loop's own code never mentions
`SavingsAccount` by name and does not need to.

</details>

## A Bank Holds Its Accounts

```python exec
id: a-bank-holds-its-accounts-1
class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance


class Bank:
    def __init__(self, name):
        self.name = name
        self.accounts = []

    def open_account(self, account):
        self.accounts.append(account)

    def total_balance(self):
        total = 0
        for account in self.accounts:
            total = total + account.balance
        return total


bank = Bank("First Local")
bank.open_account(BankAccount("Alice", 300.0))
bank.open_account(BankAccount("Ben", 150.0))
print(bank.total_balance())
```

**7.** Predict the total before running it. Then add a third account of
your own and predict the new total.

<details class="dl-answer"><summary>answer</summary>

`450.0` — `300.0 + 150.0`.

Adding a third, say `BankAccount("Cara", 100.0)`, brings the total to
`550.0`. `total_balance()` needed no change to handle a third account,
since it loops over however many `self.accounts` actually holds.

</details>

**8.** `Bank` is not a `BankAccount`, and does not inherit from it. Why
would making `Bank(BankAccount)` be the wrong choice here?

<details class="dl-answer"><summary>answer</summary>

Inheritance means "is a kind of." A bank is not a kind of account. It does
not have its own `owner` and `balance` the way an account does. It *has*
accounts, as a field, which is composition rather than inheritance. Making
`Bank` inherit from `BankAccount` would hand it a `deposit()` and
`withdraw()` that make no sense for an institution holding accounts,
rather than being one.

</details>

**9.** Add an `average_balance()` method to `Bank`, returning
`total_balance()` divided by how many accounts there are.

<details class="dl-answer"><summary>answer</summary>

```python
def average_balance(self):
    return self.total_balance() / len(self.accounts)
```

`average_balance()` calls `self.total_balance()` rather than repeating its
loop. A method is free to build on another already sitting on the same object.
*One Class, Many Methods* asked the same question about `constant_term()`
calling `self.evaluate(0)` instead.

</details>
