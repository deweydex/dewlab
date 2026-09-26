---
title: "Mixed problems: programming with objects"
practice_across:
  - objects-and-classes
  - the-moves-you-already-know
  - the-tools-around-your-code
  - keeping-details-inside-an-object
  - one-class-many-methods
  - one-parent-many-children
  - objects-inside-objects
  - testing-what-a-class-does
  - documenting-a-class
  - a-front-end-for-a-class
year: "2026-2027"
version: 2026.09.04.1
---

# Mixed problems: programming with objects

Every problem here draws on more than one tutorial from this series. None
of them says which. Deciding whether a problem wants inheritance,
composition, a test, or all three is its own skill. It is separate from
being able to write any one of them.

Answers are folded, and most have more than one reasonable design. Where a
problem has a real decision in it, the answer says what was chosen and why.
It does not pretend there was only one way to build it.

## Warm-Up

```python exec
id: warm-up-1
class Book:
    """Represents one library book: a title, an author, and whether it is
    currently on the shelf."""

    def __init__(self, title, author):
        self.title = title
        self.author = author
        self.available = True


book = Book("Dune", "Frank Herbert")
print(book.available)
```

**1.** Write a class of your own, `Playlist`, with a constructor storing a
`name` and starting with an empty list, `songs`. Give the class its own
docstring, and add a method `add_song(title)` that appends `title` to
`songs`.

<details class="dl-answer"><summary>answer</summary>

```python
class Playlist:
    """Represents a named, ordered list of songs."""

    def __init__(self, name):
        self.name = name
        self.songs = []

    def add_song(self, title):
        """Appends title to this playlist's songs."""
        self.songs.append(title)


morning = Playlist("Morning")
morning.add_song("Here Comes the Sun")
print(morning.songs)
```

It has the same shape as `Bank` from [Composition: objects inside other
objects](tutorial:objects-inside-objects): a name, and a list that
starts empty. The list grows one song at a time, through a method.

</details>

**2.** Write `test_add_song()`, checking that adding one song to a fresh
`Playlist` leaves `songs` holding exactly that one title.

<details class="dl-answer"><summary>answer</summary>

```python
def test_add_song():
    playlist = Playlist("Test")
    playlist.add_song("Here Comes the Sun")
    assert playlist.songs == ["Here Comes the Sun"], "add_song should append to songs"


test_add_song()
print("Passed.")
```

The test makes a fresh `Playlist` every time it runs, as [Testing a
class with assert](tutorial:testing-what-a-class-does) did for
`BankAccount`. So nothing is left over from an earlier test to trip
this one up.

</details>

## Building on Several Ideas

```python exec
id: building-on-several-ideas-1
class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author
        self.available = True

    def checkout(self):
        if not self.available:
            print("Refused: already checked out.")
            return
        self.available = False


class ReferenceBook(Book):
    def checkout(self):
        print("Refused: reference books do not leave the library.")
```

**3.** `ReferenceBook(Book)` overrides `checkout()` entirely, rather than
calling `super().checkout()`. Predict what `ReferenceBook("Atlas",
"Various").checkout()` does to `available`, and explain why overriding
completely was the right call here.

<details class="dl-answer"><summary>answer</summary>

`available` never changes. It stays `True`, because `ReferenceBook`'s
own `checkout()` always refuses. It never reaches a line that would set
`self.available = False`.

Calling `super().checkout()` would only make sense if some part of the
parent's own check still applied. Here none of it does. A reference book
is refused every time, not just when it happens to already be unavailable,
so there is no shared logic left to reuse.

</details>

**4.** Create one `Book` and one `ReferenceBook`, put both in a list, and
loop over it calling `checkout()` on each. Which idea from *Many Kinds, One
Loop* does this loop demonstrate?

<details class="dl-answer"><summary>answer</summary>

```python
book = Book("Dune", "Frank Herbert")
atlas = ReferenceBook("Atlas", "Various")

for item in [book, atlas]:
    item.checkout()
    print(item.title, item.available)
```

It prints:

```text
Dune False
Refused: reference books do not leave the library.
Atlas True
```

The loop demonstrates polymorphism. `item.checkout()` is the same line
for both objects, and each object runs its own class's version: the
`Book` goes off the shelf, and the `ReferenceBook` refuses.

</details>

**5.** Write a `Library` class: a constructor storing a `name` and an
empty `books` list, an `add_book(book)` method appending to it, and an
`available_titles()` method. It should return every book's `title` where
`available` is `True`.

<details class="dl-answer"><summary>answer</summary>

```python
class Library:
    """Holds a collection of books and reports which are on the shelf."""

    def __init__(self, name):
        self.name = name
        self.books = []

    def add_book(self, book):
        """Adds book to this library's collection."""
        self.books.append(book)

    def available_titles(self):
        """Returns the titles of every book currently available."""
        titles = []
        for book in self.books:
            if book.available:
                titles.append(book.title)
        return titles


library = Library("Central")
library.add_book(Book("Dune", "Frank Herbert"))
library.add_book(ReferenceBook("Atlas", "Various"))
print(library.available_titles())
```

A `Library` has books. That is
[composition](tutorial:objects-inside-objects), the same relationship
`Bank` has with its accounts. A library is not a kind of `Book`.

</details>

**6.** `available_titles()` never checks whether a `books` entry is a
`Book` or a `ReferenceBook`. Why does it not need to?

<details class="dl-answer"><summary>answer</summary>

Both classes have an `available` field and a `title` field. `Book` sets
them, and `ReferenceBook` inherits them unchanged. `available_titles()`
only ever reads those two fields, and every object in `self.books` has
them, whichever of the two classes it is.

</details>

## Putting Several Together

**7.** Extend `Library` with a `checkout_by_title(title)` method: find the
first book in `self.books` with a matching `title`, and call its own
`checkout()`. If no book matches, print a message saying so and change
nothing.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Loop over `self.books`, comparing `book.title == title`.
2. Once found, call `book.checkout()`. That method already knows how to
   refuse correctly for either kind of book, so `checkout_by_title()`
   itself never needs to ask which kind it found.
3. If the loop finishes with no match, that is the "not found" case,
   handled after the loop rather than inside it.

</details>

<details class="dl-answer"><summary>answer</summary>

```python
class Library:
    def __init__(self, name):
        self.name = name
        self.books = []

    def add_book(self, book):
        self.books.append(book)

    def checkout_by_title(self, title):
        """Checks out the first book matching title, or reports not found."""
        for book in self.books:
            if book.title == title:
                book.checkout()
                return
        print("Not found:", title)


library = Library("Central")
library.add_book(Book("Dune", "Frank Herbert"))
library.checkout_by_title("Dune")
library.checkout_by_title("Dune")
library.checkout_by_title("Nonexistent")
```

The same method gives three different outcomes. The first call checks
the book out. The second is refused, because the book is already out.
The third reports that no book has that title. `checkout_by_title()`
only ever calls `book.checkout()`. The rules for refusing still live on
`Book` and `ReferenceBook`, and are not copied here.

</details>

**8.** Write `test_checkout_by_title_refuses_twice()`. Check out the same
book twice through a fresh `Library`. Then assert that the book's
`available` is still `False`. (There is no error to test for:
`checkout()` handles a repeat by printing a message and returning.)

<details class="dl-answer"><summary>answer</summary>

```python
def test_checkout_by_title_refuses_twice():
    library = Library("Test")
    library.add_book(Book("Dune", "Frank Herbert"))
    library.checkout_by_title("Dune")
    library.checkout_by_title("Dune")
    assert library.books[0].available == False, "a second checkout should not un-refuse the book"


test_checkout_by_title_refuses_twice()
print("Passed.")
```

The test reads `library.books[0].available` rather than trusting that
nothing went wrong. That is the same habit [Testing a class with assert](tutorial:testing-what-a-class-does)
built around `assert`. Here it applies to a class made of other classes,
rather than to one class on its own.

</details>

**9.** `checkout_by_title()`'s docstring says "Checks out the first book
matching title, or reports not found." A future version instead checks out
*every* matching book. What would have to happen to the docstring for it
to stay honest?

<details class="dl-answer"><summary>answer</summary>

It would need rewriting to say so, something like "Checks out every book
matching title." Python would not catch the mismatch on its own: a
sentence in a docstring is not something it can check.

[Documenting a class with docstrings](tutorial:documenting-a-class) met
the same problem with `withdraw()`. Here it is one level up, on a method
that calls another class's method to do the work.

</details>

**10.** In your own words: what would it take to add a `MagazineIssue`
class to this system, alongside `Book` and `ReferenceBook`? It should work
with `Library.available_titles()` and `checkout_by_title()`, with no
changes to `Library` itself.

<details class="dl-answer"><summary>answer</summary>

`MagazineIssue` needs its own `title` and `available` fields, and its own
`checkout()` method, written the way `ReferenceBook`'s own was. Its check
can be whatever makes sense for a magazine issue.

Nothing about `Library` mentions `Book` or `ReferenceBook` by name anywhere
in its own methods. It only ever asks each object in `self.books` for
`title`, `available`, and `checkout()`. Any class supplying those three
fits in without `Library` needing to know it exists.

</details>

## More of the series

**11.** Anyone can reach into a `Library` from outside and write
`library.books = "Dune"`. That replaces the whole list with a string,
and the next call to `available_titles()` fails. How could you show that
`books` is the library's own business, as
[Encapsulation: keeping an object's data behind its methods](tutorial:keeping-details-inside-an-object)
did? What does your change stop, and what does it not stop?

<details class="dl-answer"><summary>answer</summary>

Rename the field `_books`, everywhere inside the class, and let code
outside use only `add_book()` and `available_titles()`.

It stops nothing. Python still lets anybody write
`library._books = "Dune"`. The underscore is a sign for people, not a
lock. What it does is tell the next programmer which names are safe to
use. Then a change to how `Library` keeps its books, a dictionary in
place of a list, say, cannot break their code.

</details>

**12.** Write `run_choice(library, choice)` for a small menu: `"1"` prints
the available titles, `"9"` returns `False` to quit, and anything else
prints `Not a menu option` and returns `True`. A cell on this site cannot
wait for typing, so run it on the list `["1", "x", "9"]`, standing in for
a person.

<details class="dl-answer"><summary>answer</summary>

```python
def run_choice(library, choice):
    if choice == "1":
        print(library.available_titles())
    elif choice == "9":
        return False
    else:
        print("Not a menu option:", choice)
    return True


library = Library("Central")    # the Library from problem 5
library.add_book(Book("Dune", "Frank Herbert"))
library.add_book(ReferenceBook("Atlas", "Various"))

for choice in ["1", "x", "9"]:
    if not run_choice(library, choice):
        break
print("Goodbye.")
```

It prints `['Dune', 'Atlas']`, then `Not a menu option: x`, then
`Goodbye.`. `run_choice()` never calls `input()`, as in
[A front end: a text menu for a class](tutorial:a-front-end-for-a-class),
so a list of answers can test it. Inside it is the selection from
[Sequence, selection and iteration inside a class](tutorial:the-moves-you-already-know),
and the loop around it is the iteration.

</details>

**13.** Run `library.available_titels()`, with the typo. Read the last
line of the error. Which name does it say is missing? What would the
editor have offered you as you typed, before you ran anything?

<details class="dl-answer"><summary>answer</summary>

The last line is
`AttributeError: 'Library' object has no attribute 'available_titels'. Did you mean: 'available_titles'?`
It names the exact name Python could not find, on the exact object, and
then suggests the name you probably meant.

As [Your development environment: the tools around your code](tutorial:the-tools-around-your-code)
showed, the editor already knows the methods on `Library`. Type
`library.avail`, and it offers `available_titles()`, spelled right, so
the typo never happens.

</details>
