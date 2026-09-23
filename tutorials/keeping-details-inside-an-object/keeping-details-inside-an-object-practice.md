---
title: "Encapsulation: keeping an object's data behind its methods — Practice"
practice_for: keeping-details-inside-an-object
year: "2026-2027"
version: 2026.09.22.1
---

# Encapsulation: keeping an object's data behind its methods — Practice

The answers are hidden in folds under each problem. Several problems ask
you to predict what a piece of code prints. Try to answer before you
run anything. Being wrong and finding out why teaches you more than
being right by luck.

## One place for the rules

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


account = BankAccount("Priya", 100.0)
account.withdraw(150.0)
print(account.balance)
```

**1.** Predict what the cell prints before you run it. Then change
`150.0` to `50.0`, and predict again before you run it.

<details class="dl-answer"><summary>answer</summary>

With `150.0`: `Refused: not enough balance.`, then `100.0`. The
withdrawal is refused, so the balance never moves.

With `50.0`: `withdraw()` prints nothing itself, then the last line
prints `50.0`. The balance drops from 100.0 to 50.0.

</details>

**2.** A teammate suggests removing `withdraw()`. Instead, wherever the
program makes a withdrawal, they would write
`account.balance = account.balance - 150`. What is lost if we do that?

<details class="dl-answer"><summary>answer</summary>

The refusal check is lost. Every one of those lines would need its own
copy of `if amount > self.balance`. If one place forgets it, the
balance can go below zero there.

This is what encapsulation gives us. The rule about changing `balance`
lives in exactly one method. Every caller gets the rule without having
to remember it.

</details>

**3.** `deposit()` above has no check against a negative `amount`. Add
one, so a negative deposit is refused in the same way as a withdrawal
that is too large.

<details class="dl-answer"><summary>answer</summary>

```python
def deposit(self, amount):
    if amount < 0:
        print("Refused: cannot deposit a negative amount.")
        return
    self.balance = self.balance + amount
```

The shape matches the check in `withdraw()`. First check. If the check
fails, refuse and return early. Otherwise, make the change.

</details>

**4.** In your own words, what is the difference between encapsulation
and abstraction?

<details class="dl-answer"><summary>answer</summary>

Encapsulation is keeping an object's data behind its own methods, so
code outside the class asks the methods to change it. Abstraction is
what a caller sees from outside: `account.withdraw(50)`, with no need to
know about the comparison and the subtraction inside.

The two usually come together. Keeping the data behind methods
(encapsulation) is what lets a caller see only a method's name and what
it does (abstraction). They still answer different questions.
Encapsulation is about where the code and the rules live. Abstraction
is about what a caller has to know.

</details>

## Reaching in from outside

```python exec
id: keeping-details-inside-an-object-practice-thermostat-1
class Thermostat:
    def __init__(self, temperature):
        self._temperature = temperature

    def get_temperature(self):
        return self._temperature

    def set_temperature(self, new_temperature):
        if new_temperature < 5 or new_temperature > 30:
            print("Refused: choose 5 to 30 degrees.")
            return
        self._temperature = new_temperature


heating = Thermostat(20)
heating.set_temperature(35)
heating.set_temperature(22)
print(heating.get_temperature())
heating._temperature = 50
print(heating.get_temperature())
```

**5.** Predict all the output before you run the cell. Does the
underscore stop the line `heating._temperature = 50`?

<details class="dl-answer"><summary>answer</summary>

`Refused: choose 5 to 30 degrees.`, then `22`, then `50`.

The underscore does not stop it. In Python, a name that starts with an
underscore is a convention: it tells people the field is private, but
Python still lets code change it. The line skips the check in
`set_temperature()`, and the heating is now set to 50 degrees.

</details>

**6.** Why write `heating.set_temperature(22)` rather than
`heating._temperature = 22`, when both give the same result here?

<details class="dl-answer"><summary>answer</summary>

The method checks the value, and the direct change does not. `22` is a
safe value, so today both give the same result. But the next value
might not be safe. Calling the method means the check always runs.

The underscore is also a message from whoever wrote the class: "use the
methods". Code that reaches in breaks that agreement, and it may stop
working if the class changes how it stores the temperature.

</details>

**7.** Which of these names, written inside a class, does the class's
writer mean to be private?

- `self.name`
- `self._pin_code`
- `self.get_pin_code`
- `self._attempts`

<details class="dl-answer"><summary>answer</summary>

`self._pin_code` and `self._attempts`. Both start with one underscore.

`self.name` has no underscore, so other code may use it.
`get_pin_code` has no underscore either. If it exists, it is a method
the writer means other code to call.

</details>

## What a caller needs to know

```python exec
id: keeping-details-inside-an-object-practice-cents-1
class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner
        self._cents = round(balance * 100)

    def get_balance(self):
        return self._cents / 100

    def can_afford(self, amount):
        return round(amount * 100) <= self._cents


account = BankAccount("Alice", 100.0)
print(account.can_afford(99.99))
print(account.can_afford(100.01))
print(account.can_afford(100.0))
```

**8.** Predict the three lines before you run the cell. Does
`can_afford(100.0)` give `True` or `False`?

<details class="dl-answer"><summary>answer</summary>

`True`, `False`, `True`.

The account holds 10000 cents. `99.99` is 9999 cents, which is less, so
`True`. `100.01` is 10001 cents, which is more, so `False`. `100.0` is
exactly 10000 cents, and `<=` allows equal, so `True`.

</details>

**9.** A caller writes `print(account.get_balance())` for this class,
and later the class goes back to storing a float in `_balance`. Does
the caller's line need to change? What if the caller had written
`print(account._cents / 100)` instead?

<details class="dl-answer"><summary>answer</summary>

`print(account.get_balance())` does not need to change. The class's
writer updates `get_balance()` to return `self._balance`, and every
caller gets the new version.

`print(account._cents / 100)` breaks. After the change, the object has
no `_cents` field, so Python stops with an `AttributeError`. Callers
that used only the methods are safe. Callers that reached in are not.

</details>
