---
title: "One Parent, Many Children"
slug: one-parent-many-children
module: fundamentals-of-oop
module_title: "Fundamentals of Object Oriented Programming"
year: "2026-2027"
series: programming-with-objects
version: 2026.09.04.1
covers:
  another-kind-of-account:
    covers: [FOOP-LO6]
  many-kinds-one-loop:
    covers: [FOOP-LO6, FOOP-LO7]
  a-bank-holds-its-accounts:
    covers: [FOOP-LO7]
---

# One Parent, Many Children

**Fundamentals of Object Oriented Programming**

*Objects and Classes* ended with a promise: a later tutorial builds several
classes on top of one another. A real bank needs that, since it offers more
than savings accounts. This tutorial adds a second kind of account, then
asks what a program can do once it has more than one.

## Another Kind of Account

A checking account allows an *overdraft*: the balance can go below zero, up
to some limit, rather than refusing every withdrawal that would empty it.
That is one field and one changed method away from `BankAccount`, the same
way `SavingsAccount` was.

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
checking.withdraw(250.0)
print(checking.balance)   # 200 - 250 = -50, allowed: within the 100 limit
```

`CheckingAccount.withdraw()` does not call `super().withdraw()` the way the
*Objects and Classes* fee example did. There, the parent's own check —
"is `amount` more than `self.balance`?" — was still the right check, only
applied to a bigger number. Here the check itself is different: an overdraft
account compares `amount` against `self.balance + self.overdraft_limit`, not
`self.balance` alone. `deposit()` still needs no override at all. Money
coming in works the same way for every kind of account, so `CheckingAccount`
keeps the one `BankAccount` already has.

### Your turn

Add an `in_overdraft()` method to `CheckingAccount`, returning `True` when
`self.balance` is below zero and `False` otherwise. Then check it on the
`checking` object above, after the withdrawal already left it negative.

```python exec
id: another-kind-of-account-2
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

    # Add an in_overdraft method here

checking = CheckingAccount("Ben", 200.0, 100.0)
checking.withdraw(250.0)
# Call in_overdraft() on checking here
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. `in_overdraft()` needs no parameter beyond `self`, the same shape as
   `deposit()` and `withdraw()` above it.
2. The method body is a single comparison: `return self.balance < 0`.
3. Call it the same way `deposit()` and `withdraw()` are already called on
   `checking`: `checking.in_overdraft()`.

</details>

## Many Kinds, One Loop

`BankAccount`, `SavingsAccount` and `CheckingAccount` all understand
`deposit()` and `withdraw()` — every child either inherits them unchanged or
supplies its own version. A loop that calls those methods can then treat
every kind of account the same way, without asking first which one it has.

```python exec
id: many-kinds-one-loop-1
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


class SavingsAccount(BankAccount):
    def __init__(self, owner, balance, interest_rate):
        super().__init__(owner, balance)
        self.interest_rate = interest_rate

    def add_interest(self):
        self.balance = self.balance + self.balance * self.interest_rate


class CheckingAccount(BankAccount):
    def __init__(self, owner, balance, overdraft_limit):
        super().__init__(owner, balance)
        self.overdraft_limit = overdraft_limit

    def withdraw(self, amount):
        if amount > self.balance + self.overdraft_limit:
            print("Refused: over the overdraft limit.")
            return
        self.balance = self.balance - amount


savings = SavingsAccount("Alice", 500.0, 0.05)
checking = CheckingAccount("Ben", 200.0, 100.0)
plain = BankAccount("Cara", 50.0)

for account in [savings, checking, plain]:
    account.withdraw(250.0)
    print(account.owner, account.balance)
```

The same call, `account.withdraw(250.0)`, does three things: Alice loses
the full 250, Ben goes 50 into his overdraft, and Cara's withdrawal is
refused outright. A plain `BankAccount` allows no overdraft at all, which is
why only Cara's call fails. Nothing in the loop asked which kind of account
it had. Each object already
knows how to withdraw correctly for its own kind, and `account.withdraw()`
runs whichever version belongs to the object making the call. This is
*polymorphism*: one method name, several classes, each running the version
that fits the object it was called on.

### Your turn

Create a second `BankAccount` and a second `SavingsAccount` of your own.
Put all five accounts — the three above and your two new ones — in one
list. Then write a loop that deposits `20.0` into every one of them and
prints each owner's name alongside their new balance.

```python exec
id: many-kinds-one-loop-2
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


class SavingsAccount(BankAccount):
    def __init__(self, owner, balance, interest_rate):
        super().__init__(owner, balance)
        self.interest_rate = interest_rate

    def add_interest(self):
        self.balance = self.balance + self.balance * self.interest_rate


class CheckingAccount(BankAccount):
    def __init__(self, owner, balance, overdraft_limit):
        super().__init__(owner, balance)
        self.overdraft_limit = overdraft_limit

    def withdraw(self, amount):
        if amount > self.balance + self.overdraft_limit:
            print("Refused: over the overdraft limit.")
            return
        self.balance = self.balance - amount


savings = SavingsAccount("Alice", 500.0, 0.05)
checking = CheckingAccount("Ben", 200.0, 100.0)
plain = BankAccount("Cara", 50.0)

# Create your own BankAccount and SavingsAccount here

# Build a list of all five accounts and loop over it here
```

## A Bank Holds Its Accounts

A bank is not one account. It keeps track of many: opening new ones, and
answering questions across all of them, such as how much money it holds in
total. That tracking is itself a class, one whose fields are other objects
rather than plain numbers or text.

```python exec
id: a-bank-holds-its-accounts-1
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
bank.open_account(BankAccount("Alice", 500.0))
bank.open_account(BankAccount("Ben", 200.0))
print(bank.total_balance())
```

`Bank` never mentions `owner` or `balance` directly. It stores a list of
account objects and asks each one for its own `balance` inside
`total_balance()`. *One Class, Many Methods* stored a list of coefficients
the same way, rather than five separate numbers. `SavingsAccount` and
`CheckingAccount` objects belong on `bank.accounts` just as well as plain
`BankAccount` ones do. `total_balance()` never checks which kind an account
is, for the same reason the loop in the last section did not.

This is a different relationship from inheritance. `SavingsAccount`
*is a* `BankAccount`, one field and method short of it. `Bank` *has*
accounts; it is not a kind of account itself, and does not extend
`BankAccount` the way `SavingsAccount` does. Building one class out of
objects of another, rather than by inheriting from it, is called
*composition*. It is the other way one class is built from smaller pieces.

### Your turn

Add a `find_account(owner)` method to `Bank`, returning the first account in
`self.accounts` whose `owner` matches, or `None` if none does. Then open a
few accounts of your own and look one up by name.

```python exec
id: a-bank-holds-its-accounts-2
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

    # Add a find_account method here

bank = Bank("First Local")
bank.open_account(BankAccount("Alice", 500.0))
bank.open_account(BankAccount("Ben", 200.0))

# Call find_account() here, and print the balance of whichever account it finds
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. `find_account(self, owner)` loops over `self.accounts`, the same loop
   `total_balance()` already uses.
2. Inside the loop, compare `account.owner == owner` — the parameter and the
   field share a name, but they are two different things: one belongs to
   `Bank`'s caller, the other to each account.
3. Return the account the moment a match is found, rather than waiting for
   the loop to finish. If the loop ends with no match, `return None` after
   it.

**Think about:** what would `find_account()` do differently if two accounts
on the same bank had the same owner name?

</details>

## Wrapping Up

In this tutorial:

- A parent class can have more than one child. `SavingsAccount` and
  `CheckingAccount` both build on `BankAccount`, each adding something
  different, without touching one another.
- *Polymorphism* lets the same method call run a different version
  depending on which class the object belongs to. `account.withdraw(amount)`
  needs no check first to know which version is right.
- *Composition* builds a class out of objects of another class, as fields,
  rather than by inheriting from it. `Bank` has accounts; it is not one.

### Reflection

A few sentences about this tutorial, whenever you are ready. `Bank` and
`CheckingAccount` both build on something else — one by holding objects,
one by inheriting from a class. What is the difference between the two,
in your own words?

Double-click this cell to write your thoughts:

## Where to Read More

Downey, A. B. (2015). *Think Python: How to Think Like a Computer
Scientist* (2nd ed.). Green Tea Press. Chapter 18 covers inheritance
between several classes at once, continuing from chapter 15's first look.
Free at <https://greenteapress.com/wp/think-python-2e/>.

Python Software Foundation. *The Python Tutorial*, section 9.5: Inheritance.
<https://docs.python.org/3/tutorial/classes.html#inheritance>. The official
reference on building one class from another, including cases with more
than one parent that this tutorial did not need.

Real Python. *Inheritance and Composition: A Python OOP Guide*.
<https://realpython.com/inheritance-composition-python/>. A longer look at
exactly the choice `Bank` and `CheckingAccount` make differently in this
tutorial.
