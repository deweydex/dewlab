---
title: "Classes and objects: keeping data and actions together"
year: "2026-2027"
version: 2026.09.22.1
covers:
  one-thing-many-parts:
    covers: [FOOP-LO1, FOOP-LO3]
  printing-an-object:
    covers: [FOOP-LO3]
  class-attributes-and-instance-attributes:
    covers: [FOOP-LO3]
    touches: [FOOP-LO8]
---

# Classes and objects: keeping data and actions together

A program that tracks one bank account needs a balance and a couple of
functions: one to add money, and one to take it away. Now picture five
accounts. Each one needs its own balance, with its own variable name to
tell it from the others. Every function call has to be given the right
one. If you use the wrong name, you have paid money into the wrong
account.

*Object oriented programming* is a way of writing programs where a
thing's data and the actions on that data are kept together, as one
unit. A program can then have five accounts, or five hundred, without
five hundred variable names to keep straight.

On this page we:

- start with the version you already know how to write, and see where it
  gets hard
- build the same bank account as a class
- make an object print in a way a person can read
- see the difference between data that every object shares and data
  that each object keeps for itself

## One thing, many parts

Here is a bank account the way you already know how to write one: a
variable for the balance, and a function that changes it.

```python exec
id: one-thing-many-parts-1
balance = 100.0

def deposit(current_balance, amount):
    return current_balance + amount

balance = deposit(balance, 50.0)
print(balance)
```

That works for one account. A second account needs a second balance,
with its own name:

```python exec
id: one-thing-many-parts-2
alice_balance = 100.0
bob_balance = 250.0

alice_balance = deposit(alice_balance, 50.0)
bob_balance = deposit(bob_balance, 20.0)

print("Alice:", alice_balance)
print("Bob:", bob_balance)
```

This still works. But look at what we now have to keep in our heads. We
have to know which balance belongs to which person. We have to pass the
right one into `deposit()` every time. Nothing in the code connects
`alice_balance` to Alice. That connection lives only in the name, and it
holds only because you were careful.

A *class* is a description of one kind of thing: the data it holds and
the actions it can do. With a class, the code itself keeps each
account's data together, so you no longer have to remember which
variable goes with which person. Here is the same bank account as a
class.

What do you think the last two lines print? Run it to check.

```python exec
id: one-thing-many-parts-3
class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        self.balance = self.balance + amount

alice = BankAccount("Alice", 100.0)
bob = BankAccount("Bob", 250.0)

alice.deposit(50.0)
bob.deposit(20.0)

print(alice.owner, alice.balance)
print(bob.owner, bob.balance)
```

Compare it with the loose-variable version above. Each account now
carries its own owner and its own balance inside itself. So
`alice.deposit(50.0)` can only ever change Alice's balance. There is no
variable name to get wrong.

Now we can name the parts.

| Part | In the code | What it is |
|---|---|---|
| *class* | `BankAccount` | A description of what a bank account has (an owner, a balance) and what it can do (take a deposit). |
| *object* | `alice`, `bob` | One thing built from a class. Each object has its own values for the fields the class describes. |
| *field* | `owner`, `balance` | A piece of data that one object carries with it. |
| *method* | `deposit()` | A function that belongs to a class. It works on the fields of one particular object. |
| *constructor* | `__init__()` | The method Python runs by itself each time a new object is built. It sets up that object's fields from the values passed in. |

Every method has `self` as its first parameter. *self* is the name a
method uses for the object it was called on. Inside `deposit()`,
`self.balance` means "the balance of the account this method was called
on". When we write `alice.deposit(50.0)`, `self` is `alice`. That is why
`alice.deposit(50.0)` cannot touch Bob's balance.

Notice too that the fields hold different types of data. `owner` is a
string, and `balance` is a float. A class's fields can be any mix of
types that a program needs, in the same way a function's parameters
can.

### Your turn

The cell below has the `BankAccount` class again.

1. Add a `withdraw` method, with the same shape as `deposit`. It should
   take `amount` away from `self.balance`.
2. `my_account` starts with a balance of `0.0`. Deposit some money into
   it, then withdraw some.
3. Print the balance. Is it what you expected?

```python exec
id: one-thing-many-parts-4
class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        self.balance = self.balance + amount

    # Add a withdraw method here

my_account = BankAccount("You", 0.0)
# Try deposit() and withdraw() on it, then print the balance
```

## Printing an object

We printed `alice.owner` and `alice.balance` one at a time. What happens
if we print the whole object?

What do you think this prints? Run it to check.

```python exec
id: printing-an-object-1
class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        self.balance = self.balance + amount

alice = BankAccount("Alice", 100.0)
print(alice)
```

It prints something like `<__main__.BankAccount object at 0x7f3c32721cd0>`.
That is the name of the class and the place in the computer's memory
where this object is stored. The number will be different on your
screen, and it changes each time you run the cell. It tells us the
object exists, but not much else.

We can tell Python how to show an object as text. We do that with a
method called `__str__`. `__str__` is a method that returns the text
`print()` shows for an object. Like `__init__`, its name has two
underscores on each side. Python calls it for us: we never write
`alice.__str__()` ourselves.

In the cell below, `print(alice)` and `print(bob)` now use `__str__`.
Look at the last line too. What do you think `print([alice, bob])`
shows? Run it to check.

```python exec
id: printing-an-object-2
class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance

    def __str__(self):
        return f"{self.owner}: {self.balance}"

    def deposit(self, amount):
        self.balance = self.balance + amount

alice = BankAccount("Alice", 100.0)
bob = BankAccount("Bob", 250.0)
alice.deposit(50.0)

print(alice)
print(bob)
print([alice, bob])
```

The first two lines are easy to read: `Alice: 150.0` and `Bob: 250.0`.
Notice that `__str__` *returns* the text. It does not print it. `print()`
does the printing.

The list still shows the long memory form. When an object is inside a
list, Python uses a second method, `__repr__`. `__repr__` is a method
that returns text meant for the programmer. The usual habit is to make
it look like the code that would build the object:

```python
    def __repr__(self):
        return f"BankAccount('{self.owner}', {self.balance})"
```

With that method added, `print([alice, bob])` shows
`[BankAccount('Alice', 150.0), BankAccount('Bob', 250.0)]`.

### Your turn

The `Book` class below has a constructor but no `__str__`.

1. Run the cell as it is, and look at what `print(book)` shows.
2. Add a `__str__` method that returns the title and the author, like
   `Dune by Frank Herbert`.
3. Run the cell again. Does `print(book)` show your text now?

```python exec
id: printing-an-object-3
class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author

    # Add a __str__ method here

book = Book("Dune", "Frank Herbert")
print(book)
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. `__str__` takes only `self`, the same as any method that needs
   nothing extra.
2. Inside it, build the text from `self.title` and `self.author`. An
   f-string such as `f"{self.title} by {self.author}"` does this.
3. Use `return`, not `print()`. Python gives an error if `__str__`
   returns anything other than a string.

</details>

## Class attributes and instance attributes

An *attribute* is any name we reach with a dot after an object, such as
`alice.balance` or `alice.deposit`. An *instance* is another word for
an object: `alice` is an instance of `BankAccount`.

The fields we set on `self` in `__init__` are *instance attributes*. An
instance attribute belongs to one object. Alice's balance and Bob's
balance are two separate values.

Sometimes a value is the same for every object of a class. Every
account in our program is at the same bank, for example. A *class
attribute* is a value that belongs to the class itself, and every
object of that class shares it. We write it inside the class but
outside any method.

In the cell below, `bank_name` is a class attribute. Near the end, we
change it once, through the class. What do you think the last two lines
print? Run it to check.

```python exec
id: class-attributes-and-instance-attributes-1
class BankAccount:
    bank_name = "Dew Bank"

    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance

alice = BankAccount("Alice", 100.0)
bob = BankAccount("Bob", 250.0)

print(alice.bank_name, alice.balance)
print(bob.bank_name, bob.balance)

BankAccount.bank_name = "Dew Savings Bank"
print(alice.bank_name)
print(bob.bank_name)
```

Both accounts show `Dew Savings Bank`. There is only one `bank_name`,
stored on the class. `alice.bank_name` and `bob.bank_name` both reach
that one value. Their balances, though, stay separate, because each
balance is an instance attribute.

A class attribute can also keep a count across every object. Here, the
constructor adds one to `accounts_opened` each time a new account is
built. How many accounts does the last line report?

```python exec
id: class-attributes-and-instance-attributes-2
class BankAccount:
    accounts_opened = 0

    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance
        BankAccount.accounts_opened = BankAccount.accounts_opened + 1

alice = BankAccount("Alice", 100.0)
bob = BankAccount("Bob", 250.0)
carol = BankAccount("Carol", 75.0)
print(BankAccount.accounts_opened)
```

It prints `3`. Notice that the constructor writes
`BankAccount.accounts_opened`, not `self.accounts_opened`. The count
belongs to the class, so we change it through the class.

This matters, and it trips most people up at least once. Assigning to a
name through an object never changes the class attribute. It makes a
new instance attribute on that one object instead:

```python
alice.bank_name = "Alice's Bank"
print(alice.bank_name)        # Alice's Bank
print(bob.bank_name)          # Dew Bank
print(BankAccount.bank_name)  # Dew Bank
```

So read a class attribute through any object, but change it through the
class.

| | Instance attribute | Class attribute |
|---|---|---|
| Where it is written | On `self`, usually in `__init__` | In the class, outside any method |
| Who has it | Each object has its own value | One value, shared by every object |
| Example | `self.balance = balance` | `bank_name = "Dew Bank"` |
| How to change it | `alice.balance = 0.0` changes Alice's only | `BankAccount.bank_name = "..."` changes it for all |

### Your turn

1. Add a class attribute `currency = "EUR"` to `BankAccount` below.
2. Print `currency` through `alice`, through `bob`, and through the
   class itself. Do all three agree?
3. Suppose the bank opens a branch in Belfast. Change `currency` to
   `"GBP"` through the class, and print it through `alice` again. What
   do you see?

```python exec
id: class-attributes-and-instance-attributes-3
class BankAccount:
    # Add a class attribute here

    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance

alice = BankAccount("Alice", 100.0)
bob = BankAccount("Bob", 250.0)
# Print currency three ways, then change it through the class
```

## Wrapping up

On this page:

- A *class* describes one kind of thing. An *object* is one thing built
  from a class, with its own values for the fields the class describes.
- A *field* is data an object carries. A *method* is a function that
  works on one object's own fields. It uses `self` to know which object.
- The *constructor*, `__init__`, sets up a new object's fields when the
  object is built.
- `__str__` returns the text `print()` shows for an object. `__repr__`
  returns text for the programmer, which Python uses for an object
  inside a list.
- An *instance attribute* belongs to one object. A *class attribute*
  belongs to the class, and every object shares it.

Loose variables and functions can do everything a class can. Nothing
here was impossible before. What changes is how much you have to hold in
your head as a program grows past one account, one shape, one anything.

Next, [Sequence, selection and iteration inside a class](tutorial:the-moves-you-already-know)
looks inside methods and finds the same `if` statements and loops you
already write. After that,
[Encapsulation: keeping an object's data behind its methods](tutorial:keeping-details-inside-an-object)
asks who should be allowed to change a field like `balance`.

### Reflection

Write a few sentences about this page, whenever you are ready. Which
felt more natural at first, the loose-variable version or the class
version? If the class version made sense in the end, what made it
click?

Double-click this cell to write your thoughts:

## Where to Read More

Downey, A. B. (2015). *Think Python: How to Think Like a Computer
Scientist* (2nd ed.). Green Tea Press. Chapter 15 covers classes and
objects at greater length, from the same starting point as this tutorial.
Free at <https://greenteapress.com/wp/think-python-2e/>.

Python Software Foundation. *The Python Tutorial*, section 9: Classes.
<https://docs.python.org/3/tutorial/classes.html>. The official reference,
including more of what `self` and inheritance can do than this tutorial
had room for.

Real Python. *Object-Oriented Programming (OOP) in Python 3*.
<https://realpython.com/python3-object-oriented-programming/>. A longer,
example-heavy walkthrough covering the same core ideas.
