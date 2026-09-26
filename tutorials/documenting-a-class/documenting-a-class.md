---
title: "Documenting a class with docstrings"
year: "2026-2027"
version: 2026.09.04.1
covers:
  a-class-docstring:
    covers: [FOOP-LO9]
  documenting-each-method:
    covers: [FOOP-LO9]
  keeping-documentation-honest:
    covers: [FOOP-LO9]
---

# Documenting a class with docstrings

A docstring is a description written in triple quotes at the top of a
function. We met docstrings in [Designing and testing good
functions](tutorial:building-reusable-tools). A function's docstring says
what the function does, what it expects, and what it returns.

A class needs docstrings in two places: on the class itself, and on every
method. On this page we:

- add a docstring to the `BankAccount` class
- add a docstring to each of its methods
- see what happens when a docstring stops telling the truth

## A class docstring

A function's docstring answers the question "what does this compute?" A
class's docstring answers a different question: "what does one object of
this class represent?" It goes in the same place as a function's
docstring, on the line straight after the line that opens the class.

The last line of the cell calls `help()`. The `help()` function shows the
docstrings of whatever you give it. What do you think it will show first?
Run the cell to find out.

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

`help()` reads the docstring from the class and shows it first, before
the constructor and before either method. So someone who meets
`BankAccount` for the first time reads that one sentence before any of
its code.

Creating an object, as in `account = BankAccount(...)`, never runs the
docstring, and never changes it. Python stores the docstring on the class
and keeps it there, for `help()`, an editor or a reader to find.

### Your turn

1. The cell below holds the `Polynomial` class from [A class with many methods: building a polynomial class](tutorial:one-class-many-methods). Write a class docstring that
   says what one `Polynomial` object represents.
2. Call `help()` on `Polynomial` to check it.

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

1. The docstring goes on its own line, straight after
   `class Polynomial:` and before `def __init__`.
2. A `Polynomial` object is a list of coefficients that represents a
   mathematical expression. Describe that. What `evaluate()` computes
   belongs in its own docstring, which we add in the next section.

</details>

## Documenting each method

The class docstring in the last section says what a `BankAccount` is. It
says nothing about what `deposit()` or `withdraw()` do. Each method gets
its own docstring for that, written the same way as a function's.

This time, `help()` is called on one method, `BankAccount.withdraw`, and
not on the whole class. How much do you think it will show? Run the cell
to check.

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

`help(BankAccount.withdraw)` shows only the docstring of `withdraw()`. Use
it when you already know which method you want, and need a reminder of
what it expects. Notice that it is called on the class, `BankAccount`,
and not on an `account` object.

`help(BankAccount)`, from the last section, would show all of them: the
class docstring first, then the docstring of each method.

### Your turn

1. Add a docstring to `evaluate()` below. Say what it computes and what
   `x` is for.
2. Call `help()` on `Polynomial.evaluate` to check it.

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

## Keeping documentation honest

Python checks your code for syntax errors. Does it check that a docstring
matches the code? Nothing stops a docstring from describing a method that
no longer exists, or a method that has changed since the docstring was
written.

Read the docstring of `withdraw()` in the cell below. Then read the code
under it. Do they agree? Run the cell to find out.

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

The docstring of `withdraw()` says "Always succeeds." The code directly under
it refuses a withdrawal that is larger than the balance, and that is what
happened here. Someone who trusted the docstring would expect
`account.balance` to be negative after the withdrawal.

Python did not notice the mismatch. A docstring is a string like any
other. Python does not run it, and does not compare it with what the
method does.

There is one exception worth knowing. A docstring can hold an example,
written the way Python's own prompt shows it: a line starting with `>>>`,
then the output you expect on the next line. Python's `doctest` module
can run every example like that, and report any output that does not
match. So an example in a docstring can be checked. A sentence like
"Always succeeds" cannot.

### Your turn

1. Fix the docstring of `withdraw()` so that it says what the method
   really does, including the refusal.
2. Do not change the code itself. When you run the cell, the balance
   should still be `50.0`.

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

1. Only the text between the triple quotes changes. The line
   `if amount > self.balance:` and everything below it stay exactly as
   they are.
2. Say what happens to an ordinary withdrawal. Then say what happens to a
   withdrawal larger than the balance: it is refused, and nothing is
   subtracted.

**Think about:** nothing in Python checks docstrings for you. So whose
job is it to notice that a docstring like this one is out of date?

</details>

## Wrapping up

On this page:

- A class docstring says what one object of the class represents. It goes
  on the line straight after `class Name:`, the same place as a
  function's docstring.
- Each method has its own docstring too, saying what that one method
  does. `help()` on a class shows all of them together. `help()` on one
  method shows only that method's docstring.
- Python never checks a docstring against the code it describes. When the
  code changes, someone has to update the docstring on purpose.

### Reflection

Write a few sentences about this page, whenever you are ready. In the
last section, we found a docstring that no longer matched its code. Have
you ever read code with a comment or docstring like that? If so, what did
you do about it?

You could write your thoughts in **Your notes**, in the **Notes** panel at
the top right of the page.

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
