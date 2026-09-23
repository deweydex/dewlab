---
title: "A front end: a text menu for a class"
year: "2026-2027"
version: 2026.09.04.1
covers:
  a-program-only-its-author-can-use:
    covers: [FOOP-LO11]
  a-menu-loop:
    covers: [FOOP-LO11]
  leaving-the-loop-cleanly:
    covers: [FOOP-LO11]
---

# A front end: a text menu for a class

So far, we have used every `Bank` and `BankAccount` in the same way. We
wrote Python calls in a cell, as the author of the code. How could
someone who does not know Python use our bank?

A *front end* is the part of a program that lets somebody use it without
reading or writing any of its code. On this page we build the simplest
kind of front end, a text menu. We:

- see why a class on its own is hard for other people to use
- write a function that turns a menu choice into a method call
- put that function inside a loop that ends cleanly

## A program only its author can use

Here is a `Bank` again. What does the cell print?

```python exec
id: a-program-only-its-author-can-use-1
class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        self.balance = self.balance + amount


class Bank:
    def __init__(self, name):
        self.name = name
        self.accounts = []

    def open_account(self, owner, balance):
        self.accounts.append(BankAccount(owner, balance))

    def total_balance(self):
        total = 0
        for account in self.accounts:
            total = total + account.balance
        return total


bank = Bank("First Local")
bank.open_account("Alice", 300.0)
bank.open_account("Ben", 150.0)
print(bank.total_balance())
```

It prints `450.0`.

This `Bank` is a little different from the one in [Composition: objects
inside other objects](tutorial:objects-inside-objects). Here,
`open_account()` takes an owner and a balance, and creates the
`BankAccount` object itself. A person at a menu can type a name and a
number, but cannot type an object.

To open an account here, you have to call `bank.open_account(...)` by
hand, with the right arguments in the right order. Someone who has never
written Python cannot use this `Bank` at all. The program works. The
problem is that using it means editing its source code.

## A menu loop

A front end sits between the person using the program and the class. It
asks a plain question. Then it calls the method that the answer asks for.

We can write and test the part that chooses the method first, before any
real person types anything. In the cell below, `run_choice()` does that
job. The loop at the end hands it three choices, one at a time: `"2"`,
then `"1"`, then `"9"`. What do you think it prints for each one? Run it
to check.

```python exec
id: a-menu-loop-1
class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        self.balance = self.balance + amount


class Bank:
    def __init__(self, name):
        self.name = name
        self.accounts = []

    def open_account(self, owner, balance):
        self.accounts.append(BankAccount(owner, balance))

    def total_balance(self):
        total = 0
        for account in self.accounts:
            total = total + account.balance
        return total


def show_menu():
    print("1: Show total balance")
    print("2: Open a test account")
    print("9: Quit")


def run_choice(bank, choice):
    """Runs one menu choice. Returns False when the menu should stop."""
    if choice == "1":
        print("Total balance:", bank.total_balance())
    elif choice == "2":
        bank.open_account("New Customer", 100.0)
        print("Opened an account for New Customer.")
    elif choice == "9":
        return False
    else:
        print("Not a menu option:", choice)
    return True


bank = Bank("First Local")
for choice in ["2", "1", "9"]:
    still_running = run_choice(bank, choice)
    print("still running:", still_running)
```

For `"2"`, it opens an account. For `"1"`, it shows the total,
`100.0`. For `"9"`, it returns `False`, which means "stop". Every other
choice returns `True`, which means "keep going".

`run_choice()` never calls `input()` itself. It acts on whatever `choice`
it receives, the same way a method acts on the arguments it receives.
That is why we can test the cell without a person typing. The loop over
`["2", "1", "9"]` stands in for someone who types those three choices,
one after another.

### Your turn

1. Add a third option to `run_choice()`: `"3"` should deposit `50.0` into
   the first account in `bank.accounts`.
2. After the deposit, print the new total.
3. The list of choices at the end already has `"3"` after `"2"`. Run the
   cell to test your new option.

```python exec
id: a-menu-loop-2
class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        self.balance = self.balance + amount


class Bank:
    def __init__(self, name):
        self.name = name
        self.accounts = []

    def open_account(self, owner, balance):
        self.accounts.append(BankAccount(owner, balance))

    def total_balance(self):
        total = 0
        for account in self.accounts:
            total = total + account.balance
        return total


def show_menu():
    print("1: Show total balance")
    print("2: Open a test account")
    print("3: Deposit 50.0 into the first account")
    print("9: Quit")


def run_choice(bank, choice):
    if choice == "1":
        print("Total balance:", bank.total_balance())
    elif choice == "2":
        bank.open_account("New Customer", 100.0)
        print("Opened an account for New Customer.")
    # Add the "3" case here
    elif choice == "9":
        return False
    else:
        print("Not a menu option:", choice)
    return True


bank = Bank("First Local")
for choice in ["2", "3", "1", "9"]:
    still_running = run_choice(bank, choice)
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. `bank.accounts[0]` is the first account opened. This is the same
   indexing that any list uses.
2. Call `.deposit(50.0)` on it: `bank.accounts[0].deposit(50.0)`.
3. Then print `bank.total_balance()`, the same way choice `"1"` already
   does.

</details>

## Leaving the loop cleanly

When `run_choice()` returns `False`, a real loop knows it is time to
stop. The cell below puts `run_choice()` together with a real `input()`
call, and that is the whole front end.

The last lines are comments, so the cell does not wait for someone to
type while this page builds. [Variables, data types and
text](tutorial:storing-and-computing) left its own `input()` example the
same way, for you to try by hand. To try the menu, remove the `#` at the
start of each of those lines, then run the cell.

```python exec
id: leaving-the-loop-cleanly-1
class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        self.balance = self.balance + amount


class Bank:
    def __init__(self, name):
        self.name = name
        self.accounts = []

    def open_account(self, owner, balance):
        self.accounts.append(BankAccount(owner, balance))

    def total_balance(self):
        total = 0
        for account in self.accounts:
            total = total + account.balance
        return total


def show_menu():
    print("1: Show total balance")
    print("2: Open a test account")
    print("9: Quit")


def run_choice(bank, choice):
    if choice == "1":
        print("Total balance:", bank.total_balance())
    elif choice == "2":
        bank.open_account("New Customer", 100.0)
        print("Opened an account for New Customer.")
    elif choice == "9":
        return False
    else:
        print("Not a menu option:", choice)
    return True


# Uncomment these lines to try the real menu (they will wait for you to type something)
# bank = Bank("First Local")
# running = True
# while running:
#     show_menu()
#     choice = input("Choose: ")
#     running = run_choice(bank, choice)
# print("Goodbye.")
```

The loop keeps running while `running` is `True`. When someone types
`9`, `run_choice()` returns `False`, the loop ends, and the program says
`Goodbye.`

What if someone types something that is not `1`, `2` or `9`? The loop does
not crash. The `else` in `run_choice()` prints `Not a menu option` and
returns `True`, so the menu shows again. One wrong key does not stop the
whole program.

A front end has to expect mistakes like this. The people who use it have
never seen the code of `run_choice()`, and they cannot fix it. Checking
what a person typed, before the program uses it, is called *input
validation*. The practice page has more of it, including amounts of money
typed as text.

### Your turn

Suppose the first thing someone types is `abc`. What does the loop print?
Predict it, then remove the `#` marks and try it yourself.

<details class="dl-answer"><summary>answer</summary>

It prints `Not a menu option: abc`. Then the menu shows again straight
away. Nothing about `bank` changes, and the loop keeps running.

</details>

## Wrapping up

On this page:

- A *front end* lets somebody use a finished program without reading or
  writing its code. A text menu is the simplest kind.
- We kept two jobs apart. `run_choice()` decides what a choice means.
  `input()` asks for the choice. Because they are apart, we can test
  `run_choice()` on its own, with a list of choices standing in for a
  person.
- A front end has to handle input that nobody expected, without
  crashing. The person using it has never seen the code behind the menu.
  Checking what they typed is called *input validation*.

### Reflection

Write a few sentences about this page, whenever you are ready. Try the
real menu loop above, with the `#` marks removed. If you were going to
give this program to somebody else, what would you add to it next?

Double-click this cell to write your thoughts:

## Where to Read More

Python Software Foundation. *The Python Tutorial*, section 7.1: Fancier
Output Formatting. <https://docs.python.org/3/tutorial/inputoutput.html>.
Covers `input()` and formatted output together, past what a plain
`print()` menu needs.

Real Python. *Build a Command-Line To-Do App With Python and Typer*.
<https://realpython.com/python-typer-cli/>. A longer look at a proper
command-line front end, using a library rather than a hand-written
`while` loop.
