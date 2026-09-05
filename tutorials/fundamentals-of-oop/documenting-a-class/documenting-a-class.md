---
title: "Documenting a Class"
slug: documenting-a-class
module: fundamentals-of-oop
module_title: "Fundamentals of Object Oriented Programming"
year: "2026-2027"
series: programming-with-objects
version: 2026.09.04.1
covers:
  a-class-docstring:
    covers: [FOOP-LO9]
  documenting-each-method:
    covers: [FOOP-LO9]
  keeping-documentation-honest:
    covers: [FOOP-LO9]
---

# Documenting a Class

**Fundamentals of Object Oriented Programming**

A function's docstring says what it does, what it expects, and what it
returns. A class needs the same care, in two places at once: the class
itself, and every method on it. This tutorial adds both to `BankAccount`,
then looks at what happens when a docstring stops telling the truth.

## A Class Docstring

A function's docstring answers "what does this compute." A class's own
docstring answers a different question: what does one object of this class
*represent*. It goes in the same place a function's does, right under the
line that opens the class.

```python exec
id: a-class-docstring-1
class BankAccount:
    """Represents one customer's account: an owner and a balance, kept
    correct through deposit() and withdraw()."""

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


help(BankAccount)
```

Run the cell above. `help()` reads the docstring straight off the class and
shows it before anything else — before the constructor, before either
method. Anyone meeting `BankAccount` for the first time gets that one
sentence before reading a single line of its code. `account = BankAccount(...)`
never runs the docstring and never changes because of it. Python stores it
on the class and leaves it there for `help()`, an editor, or a reader to
find.

### Your turn

Write a docstring for a `Polynomial` class, the one from *One Class, Many
Methods*, describing what one object of it represents. Then check it with
`help()`.

```python exec
id: a-class-docstring-2
class Polynomial:
    # Write a class docstring here

    def __init__(self, coeffs):
        self.coeffs = coeffs

    def evaluate(self, x):
        result = 0
        for i in range(len(self.coeffs)):
            result = result + self.coeffs[i] * x ** i
        return result

# Call help() on Polynomial here
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. The docstring goes on its own line, right after `class Polynomial:`,
   before `def __init__`.
2. A `Polynomial` object *is* a list of coefficients acting as a
   mathematical expression — describe that. What `evaluate()` computes
   belongs to its own docstring, added in the next section.

</details>

## Documenting Each Method

The class docstring in the last section says what a `BankAccount` is. It
says nothing about what `deposit()` or `withdraw()` actually do. That
belongs to each method's own docstring, written the same way a function's
already is.

```python exec
id: documenting-each-method-1
class BankAccount:
    """Represents one customer's account: an owner and a balance, kept
    correct through deposit() and withdraw()."""

    def __init__(self, owner, balance):
        """Creates an account for owner, starting at balance."""
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        """Adds amount to the balance."""
        self.balance = self.balance + amount

    def withdraw(self, amount):
        """Subtracts amount from the balance, refusing to go below zero."""
        if amount > self.balance:
            print("Refused: not enough balance.")
            return
        self.balance = self.balance - amount


help(BankAccount.withdraw)
```

`help(BankAccount.withdraw)`, called on the method itself rather than on an
`account` object, shows `withdraw()`'s own docstring on its own. That is
useful the moment you already know which method you want, and only need
reminding what it expects. `help(BankAccount)`, from the last section,
would show all three together: the class's own docstring first, then each
method's.

### Your turn

Add a docstring to `evaluate()` below, describing what it computes and what
`x` is for. Then check it with `help()`.

```python exec
id: documenting-each-method-2
class Polynomial:
    """Represents a polynomial as a list of coefficients."""

    def __init__(self, coeffs):
        self.coeffs = coeffs

    def evaluate(self, x):
        # Write a docstring for evaluate() here
        result = 0
        for i in range(len(self.coeffs)):
            result = result + self.coeffs[i] * x ** i
        return result

# Call help() on Polynomial.evaluate here
```

## Keeping Documentation Honest

A docstring is not checked against the code the way a syntax error is.
Nothing stops one from describing a method that no longer exists, or one
that used to work the way it says and was changed since.

```python exec
id: keeping-documentation-honest-1
class BankAccount:
    """Represents one customer's account: an owner and a balance, kept
    correct through deposit() and withdraw()."""

    def __init__(self, owner, balance):
        """Creates an account for owner, starting at balance."""
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        """Adds amount to the balance."""
        self.balance = self.balance + amount

    def withdraw(self, amount):
        """Subtracts amount from the balance. Always succeeds."""
        if amount > self.balance:
            print("Refused: not enough balance.")
            return
        self.balance = self.balance - amount


account = BankAccount("Alice", 50.0)
account.withdraw(100.0)
print(account.balance)   # still 50.0 -- the withdrawal above was refused
```

Run the cell above. `withdraw()`'s docstring says "Always succeeds." The
code, one line below it, refuses a withdrawal larger than the balance —
exactly what just happened. A reader who trusted the docstring instead of
the code would expect `account.balance` to be negative. Nothing in Python
caught the mismatch. A docstring is a string like any other, never run and
never checked against what the method actually does.

### Your turn

Fix `withdraw()`'s docstring so it describes what the method actually does,
including the refusal. Do not change the code itself — the balance should
still be `50.0` once you are done.

```python exec
id: keeping-documentation-honest-2
class BankAccount:
    """Represents one customer's account: an owner and a balance, kept
    correct through deposit() and withdraw()."""

    def __init__(self, owner, balance):
        """Creates an account for owner, starting at balance."""
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        """Adds amount to the balance."""
        self.balance = self.balance + amount

    def withdraw(self, amount):
        """Subtracts amount from the balance. Always succeeds."""
        # Fix this docstring, not the code below it
        if amount > self.balance:
            print("Refused: not enough balance.")
            return
        self.balance = self.balance - amount


account = BankAccount("Alice", 50.0)
account.withdraw(100.0)
print(account.balance)   # should still be 50.0
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Only the text between the triple quotes changes. `if amount >
   self.balance:` and everything below it stays exactly as it was.
2. Say what actually happens on a withdrawal larger than the balance —
   refused, with nothing subtracted — alongside what already happens on an
   ordinary one.

**Think about:** whose job is it to notice a docstring like this one has
gone stale, if nothing in Python checks it automatically?

</details>

## Wrapping Up

In this tutorial:

- A class's own docstring says what one object of it represents. It sits
  right under `class Name:`, the same position a function's docstring has.
- Each method keeps its own docstring too, saying what that one method
  does. `help()` on a class shows all of them together. `help()` on one
  method shows only its own.
- A docstring is never checked against the code it describes. Keeping one
  honest, once the code beneath it changes, is a habit a reader has to
  keep on purpose.

### Reflection

A few sentences about this tutorial, whenever you are ready. *Keeping
Documentation Honest* found a docstring that no longer matched its code.
Have you read code with a comment or docstring like that before, and if
so, what did you do about it?

Double-click this cell to write your thoughts:

## Where to Read More

Python Software Foundation. *The Python Tutorial*, section 4.7.6:
Documentation Strings. <https://docs.python.org/3/tutorial/controlflow.html#documentation-strings>.
The official convention this tutorial follows, including the exact
placement and quoting rules.

Python Software Foundation. *PEP 257 — Docstring Conventions*.
<https://peps.python.org/pep-0257/>. The fuller style guide behind that
convention, including the difference between a one-line docstring and a
longer one that needs more than a single sentence.

Real Python. *Documenting Python Code: A Complete Guide*.
<https://realpython.com/documenting-python-code/>. Covers docstrings
alongside the other kinds of documentation a larger project keeps, past
what one class on its own needs.
