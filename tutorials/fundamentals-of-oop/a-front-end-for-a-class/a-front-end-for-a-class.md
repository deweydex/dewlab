---
title: "A Front End for a Class"
slug: a-front-end-for-a-class
module: fundamentals-of-oop
module_title: "Fundamentals of Object Oriented Programming"
year: "2026-2027"
series: programming-with-objects
version: 2026.09.04.1
covers:
  a-program-only-its-author-can-use:
    covers: [FOOP-LO11]
  a-menu-loop:
    covers: [FOOP-LO11]
  leaving-the-loop-cleanly:
    covers: [FOOP-LO11]
---

# A Front End for a Class

**Fundamentals of Object Oriented Programming**

Every `Bank` and `BankAccount` so far has been used the same way: by
writing Python calls directly, in a cell, as its own author. A *front
end* is what lets somebody else use a finished program without writing or
reading a single line of it. This tutorial builds the simplest one there
is: a text menu.

## A Program Only Its Author Can Use

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

Opening an account here means calling `bank.open_account(...)` by hand,
with the right arguments in the right order. Someone who has never
written Python has no way to use this `Bank` at all. The program works
fine — the problem is that using it currently means editing its own
source code.

## A Menu Loop

A front end stands between a reader and the class itself: something that
asks a plain question, then calls whichever method the answer means. The
part that decides which method to call can be written and tested on its
own, with no need for an actual person typing yet.

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

`run_choice()` never calls `input()` itself. It takes whatever `choice`
it was handed and acts on it, the same way a method takes whatever
arguments it was called with. That is what makes the cell above testable
without a person present. The loop over `["2", "1", "9"]` stands in for
someone typing those three choices in turn.

### Your turn

Add a third real option: `"3"` should deposit `50.0` into the *first*
account in `bank.accounts` and print the new total. Test it by adding
`"3"` to the list of choices below, after `"2"`.

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

1. `bank.accounts[0]` is the first account opened, the same indexing any
   list uses.
2. Call `.deposit(50.0)` on it: `bank.accounts[0].deposit(50.0)`.
3. Print `bank.total_balance()` afterward, the same way choice `"1"`
   already does.

</details>

## Leaving the Loop Cleanly

`run_choice()` returning `False` is the signal a real loop uses to know
when to stop. Put together with an actual `input()` call, the cell below
is the whole front end. It is commented out here so it does not wait for
a person while this page builds. *Storing and Computing* left its own
`input()` example the same way, for you to try by hand.

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

Typing something that is not `"1"`, `"2"`, or `"9"` does not crash this
loop. `run_choice()`'s own `else` prints `Not a menu option` and returns
`True`. The menu shows again, rather than the whole program stopping over
a mistyped character. A front end a stranger actually uses has to
expect exactly that kind of mistake. Its whole point is being usable by
someone who has never seen `run_choice()`'s own code.

### Your turn

Predict what the loop above prints if the very first thing typed is
`"abc"`, before uncommenting and trying it yourself.

<details class="dl-answer"><summary>answer</summary>

`Not a menu option: abc`, then the menu shows again immediately — nothing
about `bank` changes, and the loop keeps running.

</details>

## Wrapping Up

In this tutorial:

- A *front end* is what lets somebody use a finished program without
  reading or writing its code. A menu is the simplest kind there is.
- Separating "what a choice means" (`run_choice()`) from "asking for the
  choice" (`input()`) makes the first part testable on its own. A list of
  choices can stand in for a person typing them.
- A front end has to handle input nobody expected, gracefully, since the
  person using it has never seen the code behind the menu.

### Reflection

A few sentences about this tutorial, whenever you are ready. Try the real,
uncommented menu loop above. What would you add to it next, if this were
a program you were actually going to hand to somebody else?

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
