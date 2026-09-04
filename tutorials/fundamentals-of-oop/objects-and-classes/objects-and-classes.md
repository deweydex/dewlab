---
title: "Objects and Classes"
slug: objects-and-classes
module: fundamentals-of-oop
module_title: "Fundamentals of Object Oriented Programming"
year: "2026-2027"
series: programming-with-objects
version: 2026.09.04.1
covers:
  one-thing-many-parts:
    covers: [FOOP-LO1, FOOP-LO3]
  keeping-details-to-itself:
    covers: [FOOP-LO3]
  building-on-what-already-exists:
    covers: [FOOP-LO3]
---

# Objects and Classes

**Fundamentals of Object Oriented Programming**

A program that tracks one bank account needs a balance and a couple of
functions: one to add money, one to take it away. Track five accounts the
same way and every one needs its own balance, with its own name to tell it
from the rest. Every function call has to be given the right one. Get a
name wrong and you have paid into the wrong account.

Object oriented programming keeps a thing's data and the operations on
that data together, as one unit. A program can then have five accounts,
or five hundred, without five hundred separate variable names to keep
straight. This tutorial builds up to that idea from the version without
it, so the problem is visible before the solution is.

## One Thing, Many Parts

Here is a bank account, the way you already know how to write one: a
variable for the balance, and a function that changes it.

```python exec
id: one-thing-many-parts-1
balance = 100.0

def deposit(current_balance, amount):
    return current_balance + amount

balance = deposit(balance, 50.0)
print(balance)
```

That works for one account. A second account needs a second balance, with
its own name:

```python exec
id: one-thing-many-parts-2
alice_balance = 100.0
bob_balance = 250.0

alice_balance = deposit(alice_balance, 50.0)
bob_balance = deposit(bob_balance, 20.0)

print("Alice:", alice_balance)
print("Bob:", bob_balance)
```

This still works, but notice what we now have to hold in our heads. We
have to know which balance belongs to which person, and pass the right
one into `deposit()` every single time. Nothing in the code itself
connects `alice_balance` to Alice. The connection lives only in the name,
and only because you were careful.

A *class* keeps a thing's data and the operations on it together, so that
connection is enforced by the code rather than remembered by the person
writing it. Here is the same bank account as a class:

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

Run that cell and read it against the loose-variable version above. Every
account now carries its own balance and its own owner inside itself. So
`alice.deposit(50.0)` can only ever change Alice's balance — there is no
name to get wrong.

Now we can name what just happened. `BankAccount` is a *class*:
a blueprint that says what a bank account has (an owner, a balance) and
what it can do (accept a deposit). `alice` and `bob` are *objects*: two
separate things built from that one blueprint, each with its own values for
the fields the blueprint describes. `owner` and `balance` are the object's
*fields*: the data it carries around with it. `deposit()` is a *method*: a
function that belongs to the class and acts on one particular object's own
fields. `__init__()` is the *constructor*, the method Python runs
automatically when a new object is built. Its job is to set up that
object's fields from whatever was passed in.

Every field and method needs `self` as a reminder of *which* object it
belongs to. `self.balance` inside `deposit()` means "the balance of
whichever account this method was called on." That is exactly why
`alice.deposit(50.0)` cannot touch Bob's balance. Notice too that a field
does not have to hold a number: `owner` is a string, `balance` is a float.
A class's fields can be any mix of data types a program needs, the same
way a function's parameters can.

### Your turn

Add a `withdraw` method to `BankAccount` below, following the same shape as
`deposit` — it should reduce `self.balance` by `amount`. Then create an
account of your own and try both methods on it.

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

## Keeping Details to Itself

The loose-variable version and the class version store exactly the same
numbers. What changed is who is responsible for them. With the class,
nothing outside `BankAccount` ever touches `self.balance` directly. Every
change goes through a method, so every deposit and withdrawal passes
through one place a rule could be enforced. A class that refuses to let a
balance go negative only has to check that in one method, not in every
piece of code that happens to change a balance.

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

account = BankAccount("Alice", 100.0)
account.withdraw(150.0)   # refused
account.withdraw(40.0)    # goes through
print(account.balance)
```

Run that and watch the first withdrawal get refused. There is no way to
skip that check by accident, because there is no other route to
`self.balance`. A caller can only ask the account to deposit or withdraw —
never reach in and change the number directly. This is *encapsulation*:
keeping an object's own data behind its own methods, so the rules about how
that data may change live in one place, next to the data itself.

*Abstraction* is the other half of the same idea, seen from outside the
class. `account.withdraw(150.0)` tells you what happens without telling
you how. A caller does not need to know the balance is stored as a float,
or that an `if` statement guards it, to use the account correctly. The
class's methods are the whole interface a reader needs.

### Your turn

What would go wrong if `deposit()` let a caller pass a negative amount —
`account.deposit(-50.0)`, say? Add a guard to the `deposit` method below
that refuses a negative amount the same way `withdraw` refuses an
over-large one.

```python exec
id: keeping-details-to-itself-2
class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        # Refuse a negative amount here, before changing self.balance
        self.balance = self.balance + amount

    def withdraw(self, amount):
        if amount > self.balance:
            print("Refused: not enough balance.")
            return
        self.balance = self.balance - amount

account = BankAccount("Alice", 100.0)
account.deposit(-50.0)
print(account.balance)   # should still be 100.0 if the guard works
```

## Building on What Already Exists

A savings account is a bank account that also earns interest. Writing it
from scratch would mean copying `__init__`, `deposit` and `withdraw` all
over again. Both copies would then need keeping in step by hand, every
time one of them changed. *Inheritance* avoids the copy: a new class can
be built on an existing one, keeping everything the original does and
adding only what is different.

```python exec
id: building-on-what-already-exists-1
class SavingsAccount(BankAccount):
    def __init__(self, owner, balance, interest_rate):
        super().__init__(owner, balance)
        self.interest_rate = interest_rate

    def add_interest(self):
        self.balance = self.balance + self.balance * self.interest_rate

savings = SavingsAccount("Alice", 1000.0, 0.05)
savings.deposit(200.0)   # inherited from BankAccount, not rewritten
savings.add_interest()   # new, only SavingsAccount has this
print(savings.balance)
```

`SavingsAccount(BankAccount)` says a savings account is a bank account,
plus something extra. The *parent class* (`BankAccount`) supplies deposit
and withdraw for free. The *child class* (`SavingsAccount`) adds
`interest_rate` and `add_interest()` on top. `super().__init__(owner,
balance)` hands the owner and balance straight to the parent's own
constructor, rather than repeating what it already does. Run the cell
above and check that `deposit()` still works on a `SavingsAccount`
object. `SavingsAccount` never defines it; it is there because
`BankAccount` already gave it one.

This is only a first look. Inheritance is where object oriented programs
get most of their real power. A later tutorial builds several classes on
top of one another, once there is more than one kind of account to share
code between.

### Your turn

`withdraw()` on a `SavingsAccount` currently behaves exactly like it does
on a plain `BankAccount` — inherited, unchanged. Suppose a savings account
should charge a small fee, say `2.0`, on every withdrawal. Write a new
`withdraw` method inside `SavingsAccount` that calls the parent's own
`withdraw()` for the amount plus the fee, using `super().withdraw(...)`.

```python exec
id: building-on-what-already-exists-2
class SavingsAccount(BankAccount):
    def __init__(self, owner, balance, interest_rate):
        super().__init__(owner, balance)
        self.interest_rate = interest_rate

    def add_interest(self):
        self.balance = self.balance + self.balance * self.interest_rate

    # Override withdraw here: charge a 2.0 fee on top of the amount

savings = SavingsAccount("Alice", 1000.0, 0.05)
savings.withdraw(100.0)
print(savings.balance)   # should be 1000 - 100 - 2 = 898.0 if the fee applied
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. This is called "overriding" a method: a method defined in
   `SavingsAccount` with the same name as one in `BankAccount` replaces
   it, for `SavingsAccount` objects.
2. Inside the new `withdraw`, call `super().withdraw(amount + 2.0)` rather
   than touching `self.balance` directly, so the parent's own "not enough
   balance" check still runs on the fee-adjusted amount.
3. The method still needs `self` and `amount` as parameters, the same as
   any other method.

**Think about:** why call `super().withdraw()` instead of just writing
`self.balance = self.balance - amount - 2.0` here directly?

**Try this next:** what happens if you withdraw more than the balance can
cover once the fee is added? Try it and see which check catches it.

</details>

## Wrapping Up

In this tutorial:

- A *class* is a blueprint; an *object* is one thing built from it, with
  its own values for the fields the blueprint describes.
- A *field* is data an object carries; a *method* is a function that acts
  on one object's own fields, using `self` to know which object.
- The *constructor* (`__init__`) sets up a new object's fields when it is
  built.
- *Encapsulation* keeps an object's data behind its own methods, so the
  rules about changing it live in one place.
- *Abstraction* is what a caller sees from outside: what a method does,
  not how.
- *Inheritance* lets one class (the child) build on another (the parent),
  keeping everything the parent does and adding only what differs.

Loose variables and functions can do everything a class can — nothing here
was impossible before. What changes is how much you have to hold in your
head as a program grows past one account, one shape, one anything.

### Reflection

A few sentences about this tutorial, whenever you are ready. Which felt
more natural at first, the loose-variable version or the class version?
What made the difference click, if it did?

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
