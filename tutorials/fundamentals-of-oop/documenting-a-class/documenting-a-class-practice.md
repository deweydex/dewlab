---
title: "Documenting a Class — Practice"
slug: documenting-a-class-practice
practice_for: documenting-a-class
module: fundamentals-of-oop
module_title: "Fundamentals of Object Oriented Programming"
year: "2026-2027"
series: programming-with-objects
version: 2026.09.04.1
---

# Documenting a Class — Practice

Answers are folded. A few of these ask you to predict an output before
running anything. Resist checking first — being wrong and finding out why
is worth more than being right by accident.

## A Class Docstring

```python exec
id: a-class-docstring-1
class Book:
    """Represents one book: a title and an author."""

    def __init__(self, title, author):
        self.title = title
        self.author = author


help(Book)
```

**1.** `Book` above has a class docstring but no docstring on `__init__`.
Predict whether `help(Book)` still runs, and what it shows for `__init__`.

<details class="dl-answer"><summary>answer</summary>

It still runs. `__init__(self, title, author)` is listed under "Methods
defined here," with no description under it. A docstring is optional, not
required, and Python has nothing to show when one is missing rather than
raising an error.

</details>

**2.** Write a class docstring for `Polynomial`, saying what one object of
it represents, then check it with `help()`.

<details class="dl-answer"><summary>answer</summary>

```python
class Polynomial:
    """Represents a polynomial as a list of coefficients."""

    def __init__(self, coeffs):
        self.coeffs = coeffs


help(Polynomial)
```

The docstring goes on its own line right after `class Polynomial:`, before
`def __init__`, the same position `Book`'s and `BankAccount`'s both use.

</details>

**3.** Does writing `book = Book("Dune", "Frank Herbert")` run `Book`'s
docstring in any way?

<details class="dl-answer"><summary>answer</summary>

No. A docstring is stored on the class for `help()`, an editor, or a
reader to find. Creating an object never touches it, the same way running
a function never touches its own docstring either.

</details>

## Documenting Each Method

```python exec
id: documenting-each-method-1
class Book:
    """Represents one book: a title and an author."""

    def __init__(self, title, author):
        """Creates a Book with the given title and author."""
        self.title = title
        self.author = author

    def citation(self):
        """Returns "title, by author" as one string."""
        return self.title + ", by " + self.author


help(Book.citation)
```

**4.** Predict what `help(Book.citation)` shows, compared to what
`help(Book)` would show.

<details class="dl-answer"><summary>answer</summary>

`help(Book.citation)` shows only `citation()`'s own docstring: `Returns
"title, by author" as one string.` `help(Book)` would show all three
instead. The order would be the class's own docstring, `__init__`'s, then
`citation()`'s.

</details>

**5.** Add a docstring to `evaluate()` below, saying what it computes and
what `x` is for.

```python exec
id: documenting-each-method-2
class Polynomial:
    """Represents a polynomial as a list of coefficients."""

    def __init__(self, coeffs):
        self.coeffs = coeffs

    def evaluate(self, x):
        result = 0
        for i in range(len(self.coeffs)):
            result = result + self.coeffs[i] * x ** i
        return result

# Add a docstring to evaluate() above, then call help() on it here
```

<details class="dl-answer"><summary>answer</summary>

```python
def evaluate(self, x):
    """Returns this polynomial's value at x."""
    result = 0
    for i in range(len(self.coeffs)):
        result = result + self.coeffs[i] * x ** i
    return result
```

A one-sentence docstring is enough here. It says what the method returns
and names its one parameter, the same shape `Book.citation()`'s own
docstring above used.

</details>

## Keeping Documentation Honest

```python exec
id: keeping-documentation-honest-1
class Book:
    def __init__(self, title, author, available=True):
        self.title = title
        self.author = author
        self.available = available

    def borrow(self):
        """Marks the book as borrowed. Always succeeds."""
        if not self.available:
            print("Refused: already borrowed.")
            return
        self.available = False


book = Book("Dune", "Frank Herbert")
book.borrow()
book.borrow()
print(book.available)
```

**6.** Run the cell above. What does `borrow()`'s docstring claim, and what
does the code actually do on the second call?

<details class="dl-answer"><summary>answer</summary>

The docstring says "Always succeeds." The second `book.borrow()` prints
`Refused: already borrowed.` and changes nothing, since the book is already
unavailable. `book.available` ends up `False`, which is correct — the
docstring is the part that is wrong.

</details>

**7.** Fix `borrow()`'s docstring so it describes what the method actually
does, without changing the code beneath it.

<details class="dl-answer"><summary>answer</summary>

```python
def borrow(self):
    """Marks the book as borrowed, refusing if it is already out."""
    if not self.available:
        print("Refused: already borrowed.")
        return
    self.available = False
```

Only the words between the triple quotes change. `if not self.available:`
and everything below it stays exactly as it was.

</details>

**8.** Does Python raise any warning or error when a docstring like the
original `"Always succeeds."` no longer matches what a method does?

<details class="dl-answer"><summary>answer</summary>

No. A docstring is a plain string, never run and never compared against
the code around it. Nothing in Python checks whether "Always succeeds" is
still true. Noticing a stale docstring, and fixing it, is entirely on
whoever reads the method next.

</details>
