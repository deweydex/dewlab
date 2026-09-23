---
title: "Composition: objects inside other objects — Practice"
practice_for: objects-inside-objects
year: "2026-2027"
version: 2026.09.22.1
---

# Composition: objects inside other objects — Practice

The answers are hidden until you open them. Many of these problems ask
you to predict an output before you run anything. Try not to check first.
When a prediction is wrong, finding out why teaches you more than a lucky
guess does.

## A bank holds its accounts

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

**1.** Predict the total before you run the cell. Then add a third
account of your own, and predict the new total.

<details class="dl-answer"><summary>answer</summary>

`450.0`, because `300.0 + 150.0 = 450.0`.

Adding a third account, say `BankAccount("Cara", 100.0)`, makes the
total `550.0`. `total_balance()` needs no change for a third account. It
loops over however many accounts `self.accounts` holds.

</details>

**2.** Add an `average_balance()` method to `Bank`. It should return
`total_balance()` divided by the number of accounts.

<details class="dl-answer"><summary>answer</summary>

```python
def average_balance(self):
    return self.total_balance() / len(self.accounts)
```

With Alice's and Ben's accounts, this returns `225.0`.

`average_balance()` calls `self.total_balance()`, and does not repeat its
loop. A method can build on another method of the same object.
[Reusable methods: one class that does many jobs](tutorial:one-class-many-methods)
looked at the same idea, with `constant_term()` and `self.evaluate(0)`.

</details>

**3.** Here is the `find_account()` method from the tutorial:

```python
def find_account(self, owner):
    for account in self.accounts:
        if account.owner == owner:
            return account
    return None
```

Add it to `Bank`. What does `bank.find_account("Zed")` return? What
happens if you then write `print(bank.find_account("Zed").balance)`?

<details class="dl-answer"><summary>answer</summary>

`bank.find_account("Zed")` returns `None`, because no account has the
owner `"Zed"`.

`print(bank.find_account("Zed").balance)` stops with
`AttributeError: 'NoneType' object has no attribute 'balance'`. `None` is
not an account, so it has no `balance` field. Code that calls
`find_account()` should check for `None` before it uses the result:

```python
account = bank.find_account("Zed")
if account is None:
    print("No account for Zed.")
else:
    print(account.balance)
```

</details>

## Is a, or has a?

**4.** `Bank` does not inherit from `BankAccount`. Why would
`class Bank(BankAccount):` be the wrong choice?

<details class="dl-answer"><summary>answer</summary>

Inheritance means "is a kind of", and a bank is not a kind of account. A
bank does not have its own `owner` and `balance` the way an account does.
It has accounts, held in a field. That is composition.

If `Bank` inherited from `BankAccount`, it would get a `deposit()` and a
`withdraw()` that make no sense for a bank. A bank holds accounts. It is
not one.

</details>

**5.** For each pair, is it "is a" or "has a"? Which would you use:
inheritance or composition?

- (a) `Square` and `Shape`
- (b) `Order` and `Item`
- (c) `Teacher` and `Person`
- (d) `House` and `Room`
- (e) `ElectricCar` and `Car`
- (f) `Car` and `Wheel`

<details class="dl-answer"><summary>answer</summary>

(a) A square is a shape: inheritance, `class Square(Shape):`.

(b) An order has items: composition, with a list of `Item` objects.

(c) A teacher is a person: inheritance, `class Teacher(Person):`.

(d) A house has rooms: composition, with a list of `Room` objects.

(e) An electric car is a car: inheritance, `class ElectricCar(Car):`.

(f) A car has wheels: composition. A wheel is not a kind of car, and a
car is not a kind of wheel.

</details>

**6.** Someone wrote a playlist this way:

```python
class Song:
    def __init__(self, title):
        self.title = title


class Playlist(Song):
    def __init__(self, name):
        super().__init__(name)
        self.songs = []
```

The code runs without an error. What is wrong with the design? How would
you fix it?

<details class="dl-answer"><summary>answer</summary>

"A playlist is a song" is false. "A playlist has songs" is true. So
`Playlist` should use composition, not inheritance.

With inheritance, every playlist gets a `title` field meant for one song,
and every method `Song` gains later. To fix it, remove `(Song)` and the
`super()` line:

```python
class Playlist:
    def __init__(self, name):
        self.name = name
        self.songs = []
```

</details>

## Accounts of every kind

```python exec
id: accounts-of-every-kind-practice-1
class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance


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
bank.open_account(SavingsAccount("Alice", 400.0, 0.1))
bank.open_account(CheckingAccount("Ben", -30.0, 100.0))
bank.open_account(BankAccount("Cara", 80.0))
print(bank.total_balance())
```

**7.** Predict the total before you run the cell.

<details class="dl-answer"><summary>answer</summary>

`450.0`, because `400.0 - 30.0 + 80.0 = 450.0`.

`total_balance()` reads `balance` from every account. Every kind of
account has that field, because each one gets it from `BankAccount`.

</details>

**8.** Suppose we add this method to `Bank`, to pay interest on every
account:

```python
def pay_interest(self):
    for account in self.accounts:
        account.add_interest()
```

What happens when you call `bank.pay_interest()`?

<details class="dl-answer"><summary>answer</summary>

Alice's balance becomes `440.0`. Then the loop reaches Ben's account and
stops with `AttributeError: 'CheckingAccount' object has no attribute
'add_interest'`.

Only `SavingsAccount` has `add_interest()`. `total_balance()` works for
every kind of account because it only uses what they all share. A method
that only one kind of account has cannot be called on all of them.

</details>

**9.** Write a `Customer` class that has a `name` and a list of
`accounts`, with an `add_account()` method and a `net_worth()` method.
Give Dan a `SavingsAccount` of `300.0` and a `CheckingAccount` of
`-40.0`, and print his net worth.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. A customer has accounts, so `Customer` does not inherit from anything.
2. `Customer` has the same shape as `Bank`: a name, and a list that starts
   empty.
3. `net_worth()` is the same loop as `total_balance()`.

**Think about:** `Customer` and `Bank` are almost the same class. What is
different about them, if anything?

</details>

<details class="dl-answer"><summary>answer</summary>

```python
class Customer:
    def __init__(self, name):
        self.name = name
        self.accounts = []

    def add_account(self, account):
        self.accounts.append(account)

    def net_worth(self):
        total = 0
        for account in self.accounts:
            total = total + account.balance
        return total


dan = Customer("Dan")
dan.add_account(SavingsAccount("Dan", 300.0, 0.05))
dan.add_account(CheckingAccount("Dan", -40.0, 100.0))
print(dan.net_worth())   # 260.0
```

The net worth is `260.0`, because `300.0 - 40.0 = 260.0`.

</details>
