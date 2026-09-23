---
title: "Composition: objects inside other objects"
year: "2026-2027"
version: 2026.09.22.1
covers:
  a-bank-holds-its-accounts:
    covers: [FOOP-LO7]
  is-a-or-has-a:
    covers: [FOOP-LO6, FOOP-LO7]
  accounts-of-every-kind:
    covers: [FOOP-LO6]
---

# Composition: objects inside other objects

A bank is not one account. It keeps track of many accounts. It opens new
ones, and it answers questions about all of them at once, such as "how
much money do we hold in total?"

On the last page, [Inheritance: one class built on
another](tutorial:one-parent-many-children), we built new kinds of
account on `BankAccount`. Is a bank one more kind of account? On this
page we:

- write a class whose fields are other objects
- learn a simple test for choosing between "is a" and "has a"
- put inheritance and composition together in one program

## A bank holds its accounts

A `Bank` class needs to keep track of many accounts. Its fields do not
have to be plain numbers or text. A field can hold a list of other
objects.

Before you run the cell, read `total_balance()`. What total do you
expect?

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

The total is `700.0`.

Look at what `Bank` does and does not do:

- `Bank` never stores an owner or a balance of its own.
- Its field `self.accounts` starts as an empty list. `open_account()`
  adds one account object to it at a time.
- `total_balance()` loops over that list and asks each account for its
  own `balance`.

This is like the `Polynomial` class in [Reusable methods: one class that
does many jobs](tutorial:one-class-many-methods). It stored one list of
coefficients, and did not need five separate numbers. `Bank` stores one
list of accounts, however many there are.

Building a class out of objects of another class like this is called
*composition*. Composition is a way to build one class from other
objects, held in its fields. A bank has accounts.

### Your turn

1. Add a `find_account(owner)` method to `Bank`. It should return the
   first account in `self.accounts` whose `owner` matches. If no account
   matches, it should return `None`.
2. Open a few accounts of your own.
3. Look one of them up by name, and print its balance.

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

1. `find_account(self, owner)` loops over `self.accounts`. It is the same
   loop that `total_balance()` already uses.
2. Inside the loop, compare `account.owner == owner`. The parameter and
   the field share a name, but they are two different things. The
   parameter `owner` comes from whoever called `find_account()`. The
   field `account.owner` belongs to each account.
3. Return the account as soon as you find a match. You do not need to
   wait for the loop to finish. If the loop ends with no match, write
   `return None` after it.

**Think about:** what would `find_account()` do if two accounts in the
same bank had the same owner name?

</details>

## Is a, or has a?

`SavingsAccount` and `Bank` are both built from `BankAccount`, but in two
different ways:

- A `SavingsAccount` is a `BankAccount`, with one extra field and one
  extra method. That is inheritance.
- A `Bank` has `BankAccount` objects. It is not a kind of account
  itself. That is composition.

What if we had used inheritance for `Bank` anyway? In the cell below,
`Bank` inherits from `BankAccount`. Python will not complain. What do you
think the two `print()` lines show? Run it to check.

```python exec
id: is-a-or-has-a-1
class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        self.balance = self.balance + amount


class Bank(BankAccount):   # the wrong choice: a bank is not an account
    def __init__(self, name):
        super().__init__(name, 0.0)
        self.accounts = []


bank = Bank("First Local")
bank.deposit(100.0)
print(bank.owner)
print(bank.balance)
```

It prints `First Local` and `100.0`. The bank now has an "owner" and a
balance of its own. Whose money is that `100.0`? It belongs to no
customer, and a `total_balance()` like the one in the last section
would never count it. Python raised no
error. The mistake is in the design, not in the code.

Here is a test that helps. Say the two sentences out loud, and ask which
one is true:

| Sentence | True? | Choose |
|---|---|---|
| "A savings account is a bank account." | Yes | inheritance |
| "A bank is a bank account." | No | — |
| "A bank has bank accounts." | Yes | composition |

An *is a* relationship means one class is a special kind of another. It
calls for inheritance. A *has a* relationship means one object holds
other objects. It calls for composition.

Sometimes both sentences seem to fit. Many programmers then choose "has
a", because a class that holds an object can swap it for another later.
A class that inherits from a parent keeps everything the parent does,
including the parts that make no sense for it, like the bank's `deposit()`
above.

### Your turn

For each pair, which sentence is true: "is a" or "has a"? Would you use
inheritance or composition?

1. `Car` and `Engine`
2. `Dog` and `Animal`
3. `Library` and `Book`
4. `ReferenceBook` and `Book`
5. `Playlist` and `Song`
6. `Course` and `Student`

<details class="dl-answer"><summary>answer</summary>

1. A car has an engine. Composition: `Car` keeps an `Engine` object in
   a field.
2. A dog is an animal. Inheritance: `class Dog(Animal):`.
3. A library has books, usually many. Composition: `Library` keeps a
   list of `Book` objects, the way `Bank` keeps a list of accounts.
4. A reference book is a book, perhaps one that cannot be borrowed.
   Inheritance: `class ReferenceBook(Book):`.
5. A playlist has songs. Composition, with a list.
6. A course has students. Composition, with a list. A student is not a
   kind of course, and a course is not a kind of student.

</details>

## Accounts of every kind

A bank holds savings accounts and checking accounts, not only plain ones.
Can `Bank` hold them all? `total_balance()` only reads `account.balance`,
and every kind of account has that field.

The cell below uses both relationships at once. `SavingsAccount` and
`CheckingAccount` inherit from `BankAccount`. `Bank` holds all three
kinds. Ben withdraws `250.0` from his checking account first. What total
do you expect? Run it to check.

```python exec
id: accounts-of-every-kind-1
class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance

    def withdraw(self, amount):
        if amount > self.balance:
            print("Refused: not enough balance.")
            return
        self.balance = self.balance - amount


class SavingsAccount(BankAccount):
    def __init__(self, owner, balance, interest_rate):
        super().__init__(owner, balance)
        self.interest_rate = interest_rate


class CheckingAccount(BankAccount):
    def __init__(self, owner, balance, overdraft_limit):
        super().__init__(owner, balance)
        self.overdraft_limit = overdraft_limit

    def withdraw(self, amount):
        if amount > self.balance + self.overdraft_limit:
            print("Refused: over the overdraft limit.")
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
bank.open_account(SavingsAccount("Alice", 500.0, 0.05))
bank.open_account(CheckingAccount("Ben", 200.0, 100.0))
bank.open_account(BankAccount("Cara", 50.0))

bank.accounts[1].withdraw(250.0)   # Ben's account is the second one opened
print(bank.total_balance())
```

The total is `500.0`. Ben's balance is now `-50.0`, so the sum is
`500.0 - 50.0 + 50.0`.

`total_balance()` never checks which kind each account is. It asks every
account for its `balance`, and every kind of account has one. This is
the same reason the loop in [Inheritance: one class built on
another](tutorial:one-parent-many-children#many-kinds-one-loop) worked for
every kind of account.

### Your turn

A customer can have more than one account: say, a savings account and a
checking account. Does a customer have accounts, or is a customer an
account?

1. Write a `Customer` class. Give it a `name` field and an `accounts`
   field that starts as an empty list.
2. Add an `add_account(account)` method.
3. Add a `net_worth()` method that returns the total balance of all the
   customer's accounts.
4. Create a customer called Dan with a `SavingsAccount` of `300.0` and a
   `CheckingAccount` of `-40.0`, and print Dan's `net_worth()`. What
   should it be?

```python exec
id: accounts-of-every-kind-2
class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance


class SavingsAccount(BankAccount):
    def __init__(self, owner, balance, interest_rate):
        super().__init__(owner, balance)
        self.interest_rate = interest_rate


class CheckingAccount(BankAccount):
    def __init__(self, owner, balance, overdraft_limit):
        super().__init__(owner, balance)
        self.overdraft_limit = overdraft_limit


# Write the Customer class here

# Create Dan, give him two accounts, and print his net worth here
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. A customer has accounts, so `Customer` does not inherit from
   anything. It starts `class Customer:`.
2. `Customer` looks a lot like `Bank`. `__init__(self, name)` sets
   `self.name = name` and `self.accounts = []`.
3. `add_account()` appends to `self.accounts`, the same as
   `Bank.open_account()`.
4. `net_worth()` is the same loop as `Bank.total_balance()`.
5. The checking account needs an owner, a balance and an overdraft
   limit: `CheckingAccount("Dan", -40.0, 100.0)`.

**Think about:** suppose the bank opens Dan's two accounts too, so
`Bank` and `Customer` hold the very same account objects. If Dan then
withdraws from his checking account, do both totals change?

</details>

## Wrapping up

On this page:

- A field can hold other objects, such as a list of accounts. Building a
  class this way is called *composition*.
- A `Bank` has accounts, so it holds them in a field. A `SavingsAccount`
  is a bank account, so it inherits from `BankAccount`.
- To choose, say both sentences out loud. "Is a" calls for inheritance.
  "Has a" calls for composition. If both seem to fit, "has a" is often the
  safer choice.
- A class that holds objects can hold every kind of child class, as long
  as it only uses what they all share.

### Reflection

Write a few sentences about this page, whenever you are ready. `Bank` and
`CheckingAccount` both build on something else. One does it by holding
objects, and the other by inheriting from a class. What is the difference
between the two, in your own words?

Double-click this cell to write your thoughts:

## Where to Read More

Downey, A. B. (2015). *Think Python: How to Think Like a Computer
Scientist* (2nd ed.). Green Tea Press. Section 18.8, Class diagrams,
names the two relationships on this page: HAS-A and IS-A.
Free at <https://greenteapress.com/wp/think-python-2e/>.

Real Python. *Inheritance and Composition: A Python OOP Guide*.
<https://realpython.com/inheritance-composition-python/>. A longer look at
exactly the choice `Bank` and `CheckingAccount` make differently in this
tutorial.
