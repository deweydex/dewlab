---
title: "Inheritance: one class built on another"
year: "2026-2027"
version: 2026.09.25.1
covers:
  a-class-built-on-another-class:
    covers: [FOOP-LO3, FOOP-LO6]
  another-kind-of-account:
    covers: [FOOP-LO6]
  many-kinds-one-loop:
    covers: [FOOP-LO6, FOOP-LO7]
---

# Inheritance: one class built on another

A real bank offers more than one kind of account. A savings account earns
interest. A current account lets you spend a little more than you have.
Both are still bank accounts: money goes in, and money comes out.

Do we have to write each kind of account from scratch? On this page we:

- build a new class on top of `BankAccount`, keeping everything it
  already does
- give the new class its own version of a method
- write one loop that works with every kind of account

## A class built on another class

Here is a question to start with. A savings account is a bank account
that also earns interest. How much of `BankAccount` would you have to
copy to write a `SavingsAccount` class?

Copying would mean writing `__init__`, `deposit()` and `withdraw()` all
over again. Then every change to one copy would need the same change in
the other, by hand. Python gives us a better way.

Read the cell below before you run it. `SavingsAccount` never defines
`deposit()`. Do you think `savings.deposit(200.0)` will work? Run it to
check.

```python exec
id: a-class-built-on-another-class-1
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


savings = SavingsAccount("Alice", 1000.0, 0.05)
savings.deposit(200.0)   # inherited from BankAccount, not rewritten
savings.add_interest()   # new: only SavingsAccount has this
print(savings.balance)
```

It works. The cell prints `1260.0`: first `1000 + 200 = 1200`, then 5%
interest on `1200` adds `60`.

The first line, `class SavingsAccount(BankAccount):`, says "a savings
account is a bank account, plus something extra." This is *inheritance*.
Inheritance is a way to build a new class on an existing one. The new
class keeps everything the existing class does, and adds only what is
different.

Two names help us talk about it:

- The *parent class* is the existing class. Here it is `BankAccount`. It
  gives `deposit()` and `withdraw()` to the new class for free.
- The *child class* is the new class. Here it is `SavingsAccount`. It
  adds a field, `interest_rate`, and a method, `add_interest()`.

What does `super().__init__(owner, balance)` do? `super()` is a way to
reach the parent class. This line runs `BankAccount`'s own constructor,
which sets `self.owner` and `self.balance`. The child does not repeat that
work. Then it sets the one field that is new.

When you call `savings.deposit(200.0)`, Python looks for `deposit()` in
`SavingsAccount` first. It does not find one there, so it uses the one in
`BankAccount`.

Inheritance saves copying when the new class really is a special kind
of the old one. The next page shows a case where it looks tempting and
is wrong.

### Your turn

Right now, `withdraw()` on a `SavingsAccount` works exactly as it does on
a plain `BankAccount`. Suppose the bank charges a fee of `2.0` on every
withdrawal from a savings account.

1. Write a new `withdraw()` method inside `SavingsAccount`.
2. Inside it, call the parent's `withdraw()` with the amount plus the fee,
   using `super().withdraw(...)`.
3. Run the cell. If the fee works, the balance is `898.0`.

```python exec
id: a-class-built-on-another-class-2
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

    # Write a new withdraw() here: charge a 2.0 fee on top of the amount

savings = SavingsAccount("Alice", 1000.0, 0.05)
savings.withdraw(100.0)
print(savings.balance)   # 1000 - 100 - 2 = 898.0 if the fee applied
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. A method in `SavingsAccount` with the same name as one in
   `BankAccount` replaces it, for `SavingsAccount` objects.
2. The new method still needs `self` and `amount` as parameters, the same
   as any other method.
3. Inside it, call `super().withdraw(amount + 2.0)`. Do not change
   `self.balance` yourself. That way, the parent's "not enough balance"
   check still runs, on the amount with the fee added.

**Think about:** why call `super().withdraw()`, when you could write
`self.balance = self.balance - amount - 2.0` directly?

**Try this next:** what happens if you try to withdraw an amount the
balance can only cover without the fee? Try it, and see which check
catches it.

</details>

## Another kind of account

Your new `withdraw()` has the same name as the parent's, and it replaces
the parent's version for `SavingsAccount` objects. This is called
*overriding*. To override a method is to write a method in the child
class with the same name as one in the parent class.

Now for a second child class. A current account allows an *overdraft*.
An overdraft lets the balance go below zero, up to a set limit. A plain
`BankAccount` refuses every withdrawal that is bigger than the balance.
How much would we need to change to allow an overdraft? One new field,
and one overridden method.

What do you think Ben's balance will be after he withdraws `250.0` from
`200.0`, with an overdraft limit of `100.0`? Run the cell to check.

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


class CurrentAccount(BankAccount):
    def __init__(self, owner, balance, overdraft_limit):
        super().__init__(owner, balance)
        self.overdraft_limit = overdraft_limit

    def withdraw(self, amount):
        if amount > self.balance + self.overdraft_limit:
            print("Refused: over the overdraft limit.")
            return
        self.balance = self.balance - amount


current = CurrentAccount("Ben", 200.0, 100.0)
current.withdraw(250.0)
print(current.balance)   # 200 - 250 = -50, allowed: within the 100 limit
```

The balance is `-50.0`. That is below zero, but inside the limit of
`100.0`.

Notice that `CurrentAccount.withdraw()` does not call
`super().withdraw()`, as your fee version did. Why not?

- In the fee example, the parent's check was still the right check:
  "is the amount more than `self.balance`?" Only the amount changed, so
  the fee version could pass a bigger number to the parent.
- Here the check itself is different. A current account compares the
  amount with `self.balance + self.overdraft_limit`, not with
  `self.balance` alone. The parent's check would refuse Ben's withdrawal.
  So `CurrentAccount` writes its own check.

`deposit()` needs no override at all. Money comes in the same way for
every kind of account, so `CurrentAccount` keeps the `deposit()` that
`BankAccount` already has.

A parent class can have more than one child. `SavingsAccount` and
`CurrentAccount` both build on `BankAccount`. Each adds something
different, and neither one changes the other.

### Your turn

1. Add an `in_overdraft()` method to `CurrentAccount`. It should return
   `True` when `self.balance` is below zero, and `False` otherwise.
2. Call it on `current` at the end of the cell. The withdrawal has
   already made the balance negative, so what should it print?

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


class CurrentAccount(BankAccount):
    def __init__(self, owner, balance, overdraft_limit):
        super().__init__(owner, balance)
        self.overdraft_limit = overdraft_limit

    def withdraw(self, amount):
        if amount > self.balance + self.overdraft_limit:
            print("Refused: over the overdraft limit.")
            return
        self.balance = self.balance - amount

    # Add an in_overdraft method here

current = CurrentAccount("Ben", 200.0, 100.0)
current.withdraw(250.0)
# Call in_overdraft() on current here
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. `in_overdraft()` needs no parameter except `self`. It has the same
   shape as `deposit()` and `withdraw()` above it.
2. The body is one comparison: `return self.balance < 0`.
3. Call it the same way `withdraw()` is already called on `current`:
   `print(current.in_overdraft())`.

</details>

## Many kinds, one loop

`BankAccount`, `SavingsAccount` and `CurrentAccount` all have
`deposit()` and `withdraw()` methods. Each child either inherits them
unchanged or has its own version. So can one loop call `withdraw()` on
every kind of account, without asking first which kind it has?

The loop below withdraws `250.0` from three accounts:

- Alice has a `SavingsAccount` with `500.0`.
- Ben has a `CurrentAccount` with `200.0` and an overdraft limit of
  `100.0`.
- Cara has a plain `BankAccount` with `50.0`.

Predict each person's balance after the loop. Then run it to check.

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


class CurrentAccount(BankAccount):
    def __init__(self, owner, balance, overdraft_limit):
        super().__init__(owner, balance)
        self.overdraft_limit = overdraft_limit

    def withdraw(self, amount):
        if amount > self.balance + self.overdraft_limit:
            print("Refused: over the overdraft limit.")
            return
        self.balance = self.balance - amount


savings = SavingsAccount("Alice", 500.0, 0.05)
current = CurrentAccount("Ben", 200.0, 100.0)
plain = BankAccount("Cara", 50.0)

for account in [savings, current, plain]:
    account.withdraw(250.0)
    print(account.owner, account.balance)
```

The same line, `account.withdraw(250.0)`, did three different things:

- Alice lost the full `250.0`, leaving `250.0`.
- Ben went `50.0` into his overdraft, leaving `-50.0`.
- Cara's withdrawal was refused. A plain `BankAccount` allows no
  overdraft, so only Cara's call failed.

The loop never asked which kind of account it had. Each object already
knows how to withdraw for its own kind. `account.withdraw()` runs the
version that belongs to the object it is called on.

This is *polymorphism*. Polymorphism is one method name working across
several classes, where each object runs the version that fits its own
class.

### Your turn

1. Create a second `BankAccount` and a second `SavingsAccount` of your
   own.
2. Put all five accounts in one list: the three above and your two new
   ones.
3. Write a loop that deposits `20.0` into every account.
4. In the same loop, print each owner's name and their new balance.

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


class CurrentAccount(BankAccount):
    def __init__(self, owner, balance, overdraft_limit):
        super().__init__(owner, balance)
        self.overdraft_limit = overdraft_limit

    def withdraw(self, amount):
        if amount > self.balance + self.overdraft_limit:
            print("Refused: over the overdraft limit.")
            return
        self.balance = self.balance - amount


savings = SavingsAccount("Alice", 500.0, 0.05)
current = CurrentAccount("Ben", 200.0, 100.0)
plain = BankAccount("Cara", 50.0)

# Create your own BankAccount and SavingsAccount here

# Build a list of all five accounts and loop over it here
```

## Wrapping up

On this page:

- *Inheritance* builds a child class on a parent class. The child keeps
  everything the parent does, and adds only what is different.
  `super().__init__(...)` lets the child reuse the parent's constructor.
- A parent class can have more than one child. `SavingsAccount` and
  `CurrentAccount` both build on `BankAccount`, each adding something
  different, and neither one changes the other.
- *Overriding* replaces a parent's method with a child's own version. The
  child can still call the parent's version with `super()`, as the fee
  did, or write a new check, as the overdraft did.
- *Polymorphism* lets the same method call run a different version,
  depending on the object's class. `account.withdraw(amount)` needs no
  check first to know which version is right.

Inheritance is one way to build a class from another. The next page,
[Composition: objects inside other objects](tutorial:objects-inside-objects),
looks at a second way: a `Bank` that holds its accounts.

### Reflection

Write a few sentences about this page, whenever you are ready.
`SavingsAccount` added a method that `BankAccount` does not have.
`CurrentAccount` replaced a method that `BankAccount` already had. Can
you think of another kind of account a bank might offer? Which of these
two things would its class need to do?

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
inheritance, and at the choice between inheritance and composition that
the next page makes.
