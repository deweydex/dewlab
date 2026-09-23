---
title: "Classes and objects: keeping data and actions together — Practice"
practice_for: objects-and-classes
year: "2026-2027"
version: 2026.09.22.1
---

# Classes and objects: keeping data and actions together — Practice

The answers are hidden in folds under each problem. Several problems ask
you to predict what a piece of code prints. Try to answer before you
run anything. Being wrong and finding out why teaches you more than
being right by luck.

## One thing, many parts

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

**1.** In the cell above, create two separate `BankAccount` objects,
called `account_a` and `account_b`. Deposit money into `account_a` only.
Does `account_b`'s balance change too? Predict first, then run it to
check.

<details class="dl-answer"><summary>answer</summary>

No. `account_b.balance` stays at whatever it started with.

Each object has its own `self`. Inside `deposit()`, `self.balance` means
"the balance of the object this call was made on". So
`account_a.deposit(...)` never touches `account_b`.

</details>

**2.** Here is a `Dog` class with a broken constructor. What is missing?

```python
class Dog:
    def __init__(name, breed):
        self.name = name
        self.breed = breed
```

<details class="dl-answer"><summary>answer</summary>

`self` is missing as the first parameter. The line should read
`def __init__(self, name, breed):`.

Without it, Python still passes the new object in as the first
argument. So `name` receives the object, and the real name has nowhere
to go. `Dog("Rex", "Collie")` fails with a `TypeError`: it says
`__init__` takes 2 arguments but 3 were given.

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

The shape is the same as `BankAccount`'s constructor, with different
field names. Every class's `__init__` follows this pattern: first
`self`, then whatever the object needs to start with.

</details>

**4.** What does a method need in its parameter list that a plain
function does not? What is it for?

<details class="dl-answer"><summary>answer</summary>

A method needs `self`, always first. `self` is how the method knows
which object's fields to read and change.

A plain function has no object attached to it, so there is nothing for
`self` to refer to. We call a method through an object, as in
`account.deposit(...)`. `self` is Python's way of handing that object
to the method's body.

</details>

## Printing an object

```python exec
id: objects-and-classes-practice-printing-1
class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance

    def __str__(self):
        return f"{self.owner} has {self.balance}"


account = BankAccount("Priya", 200.0)
print(account)
print([account])
```

**5.** Predict both lines of output before you run the cell. Which line
uses `__str__`, and which does not?

<details class="dl-answer"><summary>answer</summary>

The first line is `Priya has 200.0`. `print(account)` uses `__str__`.

The second line is something like
`[<__main__.BankAccount object at 0x7f...>]`. The number at the end
will be different on your screen. An object inside a list is shown with
`__repr__`, and this class does not define one yet.

</details>

**6.** Add a `__repr__` method to the class above, so the second line
prints `[BankAccount('Priya', 200.0)]`.

<details class="dl-answer"><summary>answer</summary>

```python
    def __repr__(self):
        return f"BankAccount('{self.owner}', {self.balance})"
```

It sits inside the class, next to `__str__`, with the same indent.
Now the list shows the text `__repr__` returns. `print(account)` still
uses `__str__`, so the first line does not change.

</details>

**7.** This `Pet` class has a `__str__` method, but `print(pet)` fails.
What is wrong with it?

```python
class Pet:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        print("Pet called " + self.name)


pet = Pet("Rex")
print(pet)
```

<details class="dl-answer"><summary>answer</summary>

`__str__` prints the text instead of returning it. It does print
`Pet called Rex` first. Then it returns nothing, which in Python is
`None`. `print()` needs a string from `__str__`, so it stops with
`TypeError: __str__ returned non-string (type NoneType)`.

The fix is to change `print(...)` to `return ...` inside `__str__`.

</details>

## Class attributes and instance attributes

```python exec
id: objects-and-classes-practice-attributes-1
class BankAccount:
    bank_name = "Dew Bank"

    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance


alice = BankAccount("Alice", 100.0)
bob = BankAccount("Bob", 250.0)

alice.bank_name = "Alice's Bank"
print(alice.bank_name)
print(bob.bank_name)
print(BankAccount.bank_name)
```

**8.** Predict all three lines before you run the cell. Did the class
attribute change?

<details class="dl-answer"><summary>answer</summary>

`Alice's Bank`, then `Dew Bank`, then `Dew Bank`.

The class attribute did not change. `alice.bank_name = ...` made a new
instance attribute on `alice` alone. From then on, `alice.bank_name`
finds her own value first. `bob` has no instance attribute of that
name, so `bob.bank_name` still reaches the class's value.

</details>

**9.** Someone writes the account counter like this, with `self`
instead of `BankAccount`:

```python
class BankAccount:
    accounts_opened = 0

    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance
        self.accounts_opened = self.accounts_opened + 1


alice = BankAccount("Alice", 100.0)
bob = BankAccount("Bob", 250.0)
print(alice.accounts_opened)
print(bob.accounts_opened)
print(BankAccount.accounts_opened)
```

What do the three lines print? Why is the count wrong?

<details class="dl-answer"><summary>answer</summary>

`1`, `1`, then `0`.

`self.accounts_opened + 1` reads the class's value, `0`, and adds one.
But `self.accounts_opened = ...` stores the result as a new instance
attribute on this one object. Each account ends up with its own count
of `1`, and the class's count stays at `0`. Writing
`BankAccount.accounts_opened` on both sides fixes it.

</details>

**10.** A `Student` class is used for every student at one college.
Which of these should be class attributes, and which should be instance
attributes?

- the student's name
- the college's name
- the student's grade
- the highest grade anyone can get, which is 100

<details class="dl-answer"><summary>answer</summary>

Instance attributes: the student's name and the student's grade. Each
student has their own.

Class attributes: the college's name and the highest grade. They are
the same for every student, so one shared value is enough. If the
college changes its name, we change it in one place.

</details>
