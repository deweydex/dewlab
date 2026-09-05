---
title: "Objects and Classes — Practice"
slug: objects-and-classes-practice
practice_for: objects-and-classes
module: fundamentals-of-oop
module_title: "Fundamentals of Object Oriented Programming"
year: "2026-2027"
series: programming-with-objects
version: 2026.09.04.1
---

# Objects and Classes — Practice

Answers are folded. Several of these ask you to predict an output before
running anything. Resist checking first — being wrong and finding out why
is worth more than being right by accident.

## One Thing, Many Parts

```python exec
id: one-thing-many-parts-1
class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        self.balance = self.balance + amount


account = BankAccount("Priya", 200.0)
account.deposit(50.0)
print(account.balance)
```

**1.** Create two separate `BankAccount` objects above, both called
`account_a` and `account_b`. Deposit into `account_a` only. Predict, then
check: does `account_b`'s balance change too?

<details class="dl-answer"><summary>answer</summary>

No. `account_b.balance` stays whatever it started at.

Each object has its own `self`. `self.balance` inside `deposit()` means
"the balance of whichever object this call was made on," so calling
`account_a.deposit(...)` never touches `account_b` at all.

</details>

**2.** Here is a `Dog` class with a broken constructor. What is missing?

```python
class Dog:
    def __init__(name, breed):
        self.name = name
        self.breed = breed
```

<details class="dl-answer"><summary>answer</summary>

`self` as the first parameter. It should read `def __init__(self, name,
breed):`.

Without it, Python still passes the new object as the first argument. So
`name` inside the method actually receives the object, and the real `name`
argument has nowhere to go. `Dog("Rex", "Collie")` fails with a `TypeError`
about too many arguments, since `__init__` was only written to accept two.

</details>

**3.** Write a `Book` class with a constructor that stores `title` and
`author`. Create one `Book` object and print its `title`.

<details class="dl-answer"><summary>answer</summary>

```python
class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author


book = Book("Dune", "Frank Herbert")
print(book.title)
```

The shape is identical to `BankAccount`'s constructor, with different field
names. Every class's `__init__` follows this same pattern: `self`, then
whatever the object needs to start with.

</details>

**4.** What does a method need in its parameter list that a plain function
never does, and what is it for?

<details class="dl-answer"><summary>answer</summary>

`self`, always first. It is how the method knows which object's own fields
to read and change.

A plain function has no object attached to it, so it has nothing for a
hidden first parameter to refer to. A method is only ever called through an
object (`account.deposit(...)`), and `self` is Python's way of handing that
object to the method's own body.

</details>

## Keeping Details to Itself

```python exec
id: keeping-details-to-itself-1
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


account = BankAccount("Priya", 100.0)
account.withdraw(150.0)
print(account.balance)
```

**5.** Predict the cell's output before running it. Then change `150.0` to
`50.0` and predict again before running.

<details class="dl-answer"><summary>answer</summary>

`Refused: not enough balance.` then `100.0` — the withdrawal is refused, so
the balance never moves.

With `50.0` instead: nothing printed by `withdraw()` itself, then `50.0` —
the balance drops from 100.0 to 50.0.

</details>

**6.** A teammate suggests removing `withdraw()` entirely and just writing
`account.balance = account.balance - 150` wherever a withdrawal happens in
the program. What is lost by doing that?

<details class="dl-answer"><summary>answer</summary>

The refusal check. Every one of those scattered lines would need its own
copy of `if amount > self.balance`. Missing it in even one place lets the
balance go negative there.

This is what encapsulation buys: the rule about changing `balance` lives in
exactly one method. Every caller gets it for free, rather than needing to
remember it themselves.

</details>

**7.** `deposit()` above has no guard against a negative `amount`. Add one,
so a negative deposit is refused the same way an over-large withdrawal is.

<details class="dl-answer"><summary>answer</summary>

```python
def deposit(self, amount):
    if amount < 0:
        print("Refused: cannot deposit a negative amount.")
        return
    self.balance = self.balance + amount
```

The shape matches `withdraw()`'s own guard: check first, refuse and return
early if the check fails, otherwise make the change.

</details>

**8.** In your own words: what is the difference between encapsulation and
abstraction?

<details class="dl-answer"><summary>answer</summary>

Encapsulation is keeping an object's data behind its own methods, so
nothing outside the class touches it directly. Abstraction is what a
caller sees from outside: `account.withdraw(50)`, with no need to know
there is a comparison and a `self.balance -` happening underneath.

They usually arrive together. Hiding the data (encapsulation) is what makes
it possible to show a caller only the method's name and effect
(abstraction). They still answer different questions: encapsulation is
about where the code lives, abstraction is about what a caller has to
know.

</details>

## Building on What Already Exists

```python exec
id: building-on-what-already-exists-1
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


savings = SavingsAccount("Priya", 1000.0, 0.1)
savings.add_interest()
print(savings.balance)
```

**9.** Predict the balance above before running it. Then create a second
`SavingsAccount` with an interest rate of `0.2` on the same starting
balance, and predict its balance too.

<details class="dl-answer"><summary>answer</summary>

`1100.0` — `1000.0 + 1000.0 * 0.1`.

At `0.2`: `1200.0` — `1000.0 + 1000.0 * 0.2`. The two objects never share a
balance, the same way `account_a` and `account_b` did not in question 1.

</details>

**10.** `savings.deposit(50.0)` works, even though `SavingsAccount` never
defines `deposit()`. Why?

<details class="dl-answer"><summary>answer</summary>

`SavingsAccount(BankAccount)` inherits everything `BankAccount` defines,
`deposit()` included. Python looks for `deposit()` on `SavingsAccount`
first, does not find one, and falls back to `BankAccount`'s own.

</details>

**11.** `super().__init__(owner, balance)` appears in `SavingsAccount`'s
constructor. What would go wrong if that line were deleted, leaving only
`self.interest_rate = interest_rate`?

<details class="dl-answer"><summary>answer</summary>

`self.owner` and `self.balance` would never be set. `add_interest()` reads
`self.balance` and would raise `AttributeError: 'SavingsAccount' object has
no attribute 'balance'` the first time it ran.

`super().__init__(...)` is what hands the owner and balance to
`BankAccount`'s own constructor, the same way calling `BankAccount(...)`
directly would. Skipping it skips everything that constructor sets up.

</details>

**12.** Write a `CheckingAccount(BankAccount)` with one new field,
`overdraft_limit`, and no new methods yet. Create one and print its
`overdraft_limit`.

<details class="dl-answer"><summary>answer</summary>

```python
class CheckingAccount(BankAccount):
    def __init__(self, owner, balance, overdraft_limit):
        super().__init__(owner, balance)
        self.overdraft_limit = overdraft_limit


checking = CheckingAccount("Priya", 200.0, 100.0)
print(checking.overdraft_limit)
```

`CheckingAccount` returns properly in a later tutorial, with a
`withdraw()` of its own that actually uses this field.

</details>
