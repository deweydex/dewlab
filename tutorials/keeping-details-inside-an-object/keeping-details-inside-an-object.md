---
title: "Encapsulation: keeping an object's data behind its methods"
year: "2026-2027"
version: 2026.09.22.1
covers:
  one-place-for-the-rules:
    covers: [FOOP-LO3]
  reaching-in-from-outside:
    covers: [FOOP-LO3]
  what-a-caller-needs-to-know:
    covers: [FOOP-LO3]
    touches: [FOOP-LO4]
---

# Encapsulation: keeping an object's data behind its methods

In [Classes and objects: keeping data and actions together](tutorial:objects-and-classes)
we built a `BankAccount` class. Each account keeps its own owner and its
own balance, and methods such as `deposit()` change them.

This page asks a new question: who should be allowed to change the
balance? On this page we:

- put the rules about a balance in one place, inside the class
- see that Python lets code outside the class change a field anyway, and
  what programmers do about it
- look at a class from the outside, and ask what someone using it needs
  to know

## One place for the rules

The loose-variable version and the class version of a bank account store
the same numbers. What changed is who looks after them.

Suppose every change to the balance goes through a method. Then every
deposit and every withdrawal passes through one place, and that is the
place to put a rule. Say the bank does not allow a balance to go below
zero. The class needs to check that in one method, `withdraw()`. The
check does not have to be copied into every piece of code that changes a
balance.

What do you think the two withdrawals do? Run it to check.

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

The first withdrawal is refused, because 150 is more than the balance.
The second one goes through, and the balance ends at `60.0`. Any code
that calls `withdraw()` gets the check, whether its writer remembered it
or not.

This idea has a name. *Encapsulation* is keeping an object's data behind
its own methods. Code outside the class asks the object to make a
change, and the object's methods decide how. The rules about how the
data may change then live in one place, next to the data itself.

### Your turn

What would go wrong if `deposit()` allowed a negative amount, as in
`account.deposit(-50.0)`?

1. Run the cell below as it is, and look at the balance.
2. Add a check at the start of `deposit()` that refuses a negative
   amount, in the same way `withdraw()` refuses an amount that is too
   large.
3. Run it again. The balance should stay at `100.0`.

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

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Copy the shape of the check in `withdraw()`: an `if`, a message, and
   `return`.
2. This time, the condition is `amount < 0`.
3. Put the check before the line that changes `self.balance`. The
   `return` stops the method before the change happens.

</details>

## Reaching in from outside

The rule in `withdraw()` works when code calls `withdraw()`. But does
Python force code to call it? What happens if code outside the class
changes `balance` directly?

Predict the last line, then run it to check.

```python exec
id: reaching-in-from-outside-1
class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance

    def withdraw(self, amount):
        if amount > self.balance:
            print("Refused: not enough balance.")
            return
        self.balance = self.balance - amount

account = BankAccount("Alice", 100.0)
account.withdraw(500.0)                     # through the method: refused
account.balance = account.balance - 500.0   # reaching in: nothing checks it
print(account.balance)
```

It prints `-400.0`. The method refused the withdrawal, but the next line
went around the method and changed the field directly. Python did not
stop it.

Some languages, such as Java, can lock a field so that only the class's
own methods can change it. Python has no lock like that. It relies on a
*convention*: a habit that programmers agree to follow. A name that
starts with one underscore, such as `_balance`, means "this is private
to the class; use the methods instead". A *private* field is one that
only the class's own methods should read or change.

The class then gives other code a method to read the value, often
called a *getter*. A getter is a method that returns the value of a
private field. Here is the account with a private `_balance` and a
getter, `get_balance()`. What do you think it prints?

```python exec
id: reaching-in-from-outside-2
class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner
        self._balance = balance

    def get_balance(self):
        return self._balance

    def deposit(self, amount):
        if amount < 0:
            print("Refused: cannot deposit a negative amount.")
            return
        self._balance = self._balance + amount

    def withdraw(self, amount):
        if amount > self._balance:
            print("Refused: not enough balance.")
            return
        self._balance = self._balance - amount

account = BankAccount("Alice", 100.0)
account.deposit(25.0)
account.withdraw(500.0)
print(account.get_balance())
```

The deposit goes through, the withdrawal is refused, and it prints
`125.0`. Code outside the class now reads the balance with
`get_balance()`, and changes it only with `deposit()` and `withdraw()`.

The underscore is a sign for people, not a lock. `account._balance = -400.0`
would still work. But anyone who writes it can see they are breaking the
class's rules, and someone reading the code can see it quickly.

You may also see a name with two underscores at the start, such as
`__balance`. Python then adds the class name to the front of it, which
makes it harder to reach from outside. One underscore is the more common
choice.

### Your turn

The `Student` class below keeps its grade in a private field, `_grade`.
A grade must be from 0 to 100.

1. Fill in `set_grade()`. If `new_grade` is below 0 or above 100, print
   a message and change nothing. Otherwise, store it in `self._grade`.
2. Replace the line `pass` with your code. `pass` is a line that does
   nothing. It is there only so the empty method can run.
3. Run the cell. It should print a refusal for `140`, then `85`.

```python exec
id: reaching-in-from-outside-3
class Student:
    def __init__(self, name, grade):
        self.name = name
        self._grade = grade

    def get_grade(self):
        return self._grade

    def set_grade(self, new_grade):
        # Refuse a grade below 0 or above 100, otherwise store it
        pass

student = Student("Ana", 72)
student.set_grade(85)
student.set_grade(140)
print(student.get_grade())
```

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Check both limits in one condition:
   `if new_grade < 0 or new_grade > 100:`
2. Inside that `if`, print a message and `return`. After the `if`,
   write `self._grade = new_grade`.

</details>

## What a caller needs to know

A *caller* is any code that uses an object's methods, such as the lines
`account.deposit(25.0)` and `account.get_balance()`.

*Abstraction* is the other half of encapsulation, seen from the
caller's side. Abstraction means a caller uses what a method does,
without needing to know how it does it. `account.withdraw(150.0)` tells
you what will happen: the account pays out 150, or refuses. You do not
need to know that the balance is stored as a float, or that an `if`
statement guards it. A class's methods are all a caller needs.

This gives the class's writer a lot of freedom. The inside of the class
can change, and callers never notice.

Here is an example. Decimals such as `0.1` cannot be stored exactly in
a computer; `0.1 + 0.2` gives `0.30000000000000004`. So banks often
count money in whole cents. Below, the class now stores `_cents`, a
whole number. `round()` gives the nearest whole number.

Compare the last four lines with the cell in the section above. Which
of them had to change?

```python exec
id: what-a-caller-needs-to-know-1
class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner
        self._cents = round(balance * 100)

    def get_balance(self):
        return self._cents / 100

    def deposit(self, amount):
        if amount < 0:
            print("Refused: cannot deposit a negative amount.")
            return
        self._cents = self._cents + round(amount * 100)

    def withdraw(self, amount):
        if round(amount * 100) > self._cents:
            print("Refused: not enough balance.")
            return
        self._cents = self._cents - round(amount * 100)

account = BankAccount("Alice", 100.0)
account.deposit(25.0)
account.withdraw(500.0)
print(account.get_balance())
```

None of them changed, and the output is the same: a refusal, then
`125.0`. The way the balance is stored is completely different. But the
callers only ever used the methods, so they did not need to change.

If callers had written `account.balance` all over the program, every one
of those lines would now be broken. That is what encapsulation and
abstraction protect us from.

### Your turn

1. Add a method `can_afford(self, amount)` to the class below. It should
   return `True` if the account has at least `amount`, and `False`
   otherwise.
2. Work in cents inside the method, the way `withdraw()` does.
3. Run the cell. It should print `True`, then `False`.

```python exec
id: what-a-caller-needs-to-know-2
class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner
        self._cents = round(balance * 100)

    def get_balance(self):
        return self._cents / 100

    # Add a can_afford method here

account = BankAccount("Alice", 100.0)
print(account.can_afford(99.99))
print(account.can_afford(100.01))
```

## Wrapping up

On this page:

- *Encapsulation* keeps an object's data behind its own methods. The
  rules about changing the data then live in one place.
- Python does not lock a field. A name that starts with an underscore,
  such as `_balance`, is a *convention* that marks it *private*: only
  the class's own methods should use it.
- A *getter* is a method that returns a private field's value, such as
  `get_balance()`.
- *Abstraction* is what a *caller* sees from outside: what a method
  does, not how. Because callers use only the methods, the inside of a
  class can change without breaking them.

### Reflection

Write a few sentences about this page, whenever you are ready. Did it
surprise you that Python lets code reach in and change a field? Can you
think of something in daily life that works the same way, with a rule
that people follow even though nothing forces them to?

Double-click this cell to write your thoughts:

## Where to Read More

Python Software Foundation. *The Python Tutorial*, section 9.6: Private
Variables. <https://docs.python.org/3/tutorial/classes.html#private-variables>.
The official note on the one-underscore convention and on names with two
underscores.

Downey, A. B. (2015). *Think Python: How to Think Like a Computer
Scientist* (2nd ed.). Green Tea Press. Chapter 17 discusses keeping a
class's interface separate from how it works inside.
Free at <https://greenteapress.com/wp/think-python-2e/>.
