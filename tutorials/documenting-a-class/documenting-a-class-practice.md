---
title: "Documenting a class with docstrings — Practice"
practice_for: documenting-a-class
year: "2026-2027"
version: 2026.09.04.1
---

# Documenting a class with docstrings — Practice

The answers are hidden until you open them. A few of these problems ask
you to predict an output before you run anything. Try not to check first.
When a prediction is wrong, finding out why teaches you more than a lucky
guess does.

## A class docstring

```python exec
id: a-class-docstring-1
class Book:
    """Represents one book: a title and an author."""

    def __init__(self, title, author):
        self.title = title
        self.author = author


help(Book)
```

**1.** `Book` above has a class docstring, but `__init__` has no
docstring. Does `help(Book)` still run? What does it show for `__init__`?

<details class="dl-answer"><summary>answer</summary>

It still runs. `__init__(self, title, author)` is listed under "Methods
defined here". Under it, Python shows a general line of its own:
`Initialize self.  See help(type(self)) for accurate signature.` That
line comes from Python itself, and says nothing about books. A method
with no docstring and no such built-in text, like `citation()` below
without its docstring, shows nothing under its name.

A docstring is optional. When one is missing, Python does not raise an
error.

</details>

**2.** Write a class docstring for `Polynomial` that says what one object
of the class represents. Then check it with `help()`.

<details class="dl-answer"><summary>answer</summary>

```python
class Polynomial:
    """Represents a polynomial as a list of coefficients."""

    def __init__(self, coeffs):
        self.coeffs = coeffs


help(Polynomial)
```

The docstring goes on its own line, straight after `class Polynomial:` and
before `def __init__`. `Book` and `BankAccount` put theirs in the same
place.

</details>

**3.** Does `book = Book("Dune", "Frank Herbert")` run the docstring of
`Book` in any way?

<details class="dl-answer"><summary>answer</summary>

No. Python stores a docstring on the class, for `help()`, an editor or a
reader to find. Creating an object never uses it. In the same way,
calling a function never runs the function's docstring.

</details>

## Documenting each method

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

**4.** Predict what `help(Book.citation)` shows. How is that different
from what `help(Book)` would show?

<details class="dl-answer"><summary>answer</summary>

`help(Book.citation)` shows only the docstring of `citation()`:
`Returns "title, by author" as one string.`

`help(Book)` would show all three docstrings. First the class docstring,
then the docstring of `__init__`, then the docstring of `citation()`.

</details>

**5.** Add a docstring to `evaluate()` below. Say what it computes and what
`x` is for.

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

One sentence is enough here. It says what the method returns, and it
names the one parameter. The docstring of `Book.citation()` above has the
same shape.

</details>

## Keeping documentation honest

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

**6.** Run the cell above. What does the docstring of `borrow()` say? What
does the code do on the second call?

<details class="dl-answer"><summary>answer</summary>

The docstring says "Always succeeds." The second `book.borrow()` prints
`Refused: already borrowed.` and changes nothing, because the book is
already out. `book.available` ends up `False`, which is correct. The code
is right, and the docstring is wrong.

</details>

**7.** Fix the docstring of `borrow()` so that it says what the method
really does. Do not change the code under it.

<details class="dl-answer"><summary>answer</summary>

```python
def borrow(self):
    """Marks the book as borrowed, refusing if it is already out."""
    if not self.available:
        print("Refused: already borrowed.")
        return
    self.available = False
```

Only the words between the triple quotes change. The line
`if not self.available:` and everything below it stay exactly as they
were.

</details>

**8.** The original docstring said `"Always succeeds."`, and that no
longer matches what the method does. Does Python give a warning or an
error about it?

<details class="dl-answer"><summary>answer</summary>

No. A docstring is a plain string. Python never runs it, and never
compares it with the code around it. Nothing in Python checks whether
"Always succeeds" is still true. Whoever reads the method next has to
notice the out-of-date docstring, and fix it.

</details>
