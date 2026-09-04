---
title: "Mixed Problems — Programming with Objects"
slug: mixed-programming-with-objects
practice_across:
  - objects-and-classes
  - one-class-many-methods
  - one-parent-many-children
  - testing-what-a-class-does
  - documenting-a-class
module: fundamentals-of-oop
module_title: "Fundamentals of Object Oriented Programming"
year: "2026-2027"
series: programming-with-objects
version: 2026.09.04.1
---

# Mixed Problems — Programming with Objects

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

Same shape as `Bank` from *One Parent, Many Children*: a name, and a list
that starts empty. It grows one item at a time through a method rather
than being set directly.

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

A fresh `Playlist` each time a test runs — the same discipline *Testing
What a Class Does* used for `BankAccount`. Nothing is left over from an
earlier test to trip this one up.

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

`available` never changes — it stays `True`. `ReferenceBook`'s own
`checkout()` refuses unconditionally and returns, never reaching a line
that would set `self.available = False`.

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

`Dune True` after checkout would be wrong — checking `book.available`
after `book.checkout()` gives `False`; `atlas.available` stays `True`.
Polymorphism: `item.checkout()` is the same line for both, and runs
whichever class's own version fits the object.

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

`Library` *has* books — composition, the same relationship `Bank` has with
its accounts — rather than being a kind of `Book` itself.

</details>

**6.** `available_titles()` never checks whether a `books` entry is a
`Book` or a `ReferenceBook`. Why does it not need to?

<details class="dl-answer"><summary>answer</summary>

Both classes have an `available` field and a `title` field — `Book`'s own,
inherited unchanged by `ReferenceBook`. `available_titles()` only ever
reads those two fields, which every object in `self.books` is guaranteed
to have, whichever of the two classes it actually is.

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

Three different outcomes from the same method. The first call succeeds,
the second refuses since the book is already out, the third reports the
title was never found. `checkout_by_title()` itself only ever calls
`book.checkout()` — the refusal logic still lives entirely on `Book` and
`ReferenceBook`, not duplicated here.

</details>

**8.** Write `test_checkout_by_title_refuses_twice()`. Check out the same
book twice through a fresh `Library`. Assert the book's `available` is
still `False` after both calls — not that it errors, since `checkout()`
already handles a repeat by printing and returning.

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
nothing went wrong. That is the same habit *Testing What a Class Does*
built around `assert`. Here it applies to a class made of other classes,
rather than to one class on its own.

</details>

**9.** `checkout_by_title()`'s docstring says "Checks out the first book
matching title, or reports not found." A future version instead checks out
*every* matching book. What would have to happen to the docstring for it
to stay honest?

<details class="dl-answer"><summary>answer</summary>

It would need rewriting to say so, something like "Checks out every book
matching title." Python would not catch the mismatch on its own.

*Keeping Documentation Honest* is exactly this situation, one level up, on
a method that itself calls another class's method rather than doing the
work directly.

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
