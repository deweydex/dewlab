---
title: "A front end: a text menu for a class — Practice"
practice_for: a-front-end-for-a-class
year: "2026-2027"
version: 2026.09.22.1
---

# A front end: a text menu for a class — Practice

The answers are hidden until you open them. Many of these problems ask
you to predict an output before you run anything. Try not to check first.
When a prediction is wrong, finding out why teaches you more than a lucky
guess does.

A cell on this page cannot wait for you to type, so none of the cells
call `input()`. We use plain functions, and lists of answers that stand
in for a person typing, as the tutorial did.

## A menu loop

This cell holds the `Bank` and the `run_choice()` function from the
tutorial. Run it first. The problems in this section use it.

```python exec
id: a-menu-loop-practice-1
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
for choice in ["1", "2", "2", "1", "9"]:
    run_choice(bank, choice)
```

**1.** The loop hands `run_choice()` five choices: `"1"`, `"2"`, `"2"`,
`"1"`, `"9"`. Predict every line the cell prints.

<details class="dl-answer"><summary>answer</summary>

```text
Total balance: 0
Opened an account for New Customer.
Opened an account for New Customer.
Total balance: 200.0
```

The first total is `0`, not `0.0`. `total_balance()` starts from
`total = 0`, and with no accounts there is nothing to add. After two
accounts of `100.0` each, the total is `200.0`.

Choice `"9"` prints nothing. It only returns `False`.

</details>

**2.** Predict what each of these calls prints, and what it returns:

- (a) `run_choice(bank, "one")`
- (b) `run_choice(bank, " 1")`, with a space before the `1`
- (c) `run_choice(bank, 9)`, with the number `9`, not the string `"9"`

<details class="dl-answer"><summary>answer</summary>

All three print a `Not a menu option` line, and all three return `True`.

(a) `"one"` is not `"1"`, `"2"` or `"9"`. It prints
`Not a menu option: one`.

(b) `" 1"` has two characters, a space and a `1`, so it is not equal to
`"1"`. It prints `Not a menu option:  1`, with two spaces: `print()`
adds one, and the string starts with the other.

(c) The number `9` is not equal to the string `"9"`. It prints
`Not a menu option: 9`, and the menu does not stop. This cannot happen
with a real menu, because `input()` always gives back a string.

</details>

**3.** Add a new option, `"4"`, that prints how many accounts the bank
has. Test it with the list `["2", "2", "4", "9"]`.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Add a new `elif` to `run_choice()`, before the `"9"` case.
2. `bank.accounts` is a list. `len()` tells you how many items a list
   has.

**Think about:** should `show_menu()` from the tutorial change too? What
would a person using the menu see if it did not?

</details>

<details class="dl-answer"><summary>answer</summary>

```python
def run_choice(bank, choice):
    """Runs one menu choice. Returns False when the menu should stop."""
    if choice == "1":
        print("Total balance:", bank.total_balance())
    elif choice == "2":
        bank.open_account("New Customer", 100.0)
        print("Opened an account for New Customer.")
    elif choice == "4":
        print("Number of accounts:", len(bank.accounts))
    elif choice == "9":
        return False
    else:
        print("Not a menu option:", choice)
    return True


bank = Bank("First Local")
for choice in ["2", "2", "4", "9"]:
    run_choice(bank, choice)
```

This prints `Opened an account for New Customer.` twice, then
`Number of accounts: 2`.

Remember to add `print("4: Show the number of accounts")` to
`show_menu()` as well. A person using the menu only knows about the
options the menu shows.

</details>

## Checking what the user typed

People often type something the program does not expect. Before a
program uses what someone typed, it should check it. This is called
*input validation*. Input validation is checking that what a person typed
makes sense, before the program uses it.

A menu choice is easy to check: `run_choice()` compares it with each
option. An amount of money is harder. `input()` gives back a string, and
`float("abc")` stops the program with a `ValueError`.

This cell uses a string method, `.isdigit()`. It returns `True` when a
string is not empty and every character in it is a digit from `0` to
`9`. Otherwise it returns `False`.

```python exec
id: checking-what-was-typed-practice-1
def read_amount(text):
    """Returns text as a number, or None if it is not a whole number above zero."""
    if not text.isdigit():
        return None
    amount = float(text)
    if amount <= 0:
        return None
    return amount


print("50".isdigit())
print(read_amount("50"))
print(read_amount("abc"))
```

**4.** Predict what each of these gives, `True` or `False`:

- (a) `"50".isdigit()`
- (b) `"abc".isdigit()`
- (c) `"".isdigit()`, an empty string
- (d) `"2.5".isdigit()`
- (e) `"-5".isdigit()`
- (f) `" 50".isdigit()`, with a space before the `50`

<details class="dl-answer"><summary>answer</summary>

(a) `True`. Every character is a digit.

(b) `False`. No character is a digit.

(c) `False`. An empty string has no digits at all. This is what you get
when someone presses Enter without typing anything.

(d) `False`. The `.` is not a digit.

(e) `False`. The `-` is not a digit.

(f) `False`. The space is not a digit.

</details>

**5.** Predict what `read_amount()` returns for each of these:
`"50"`, `"abc"`, `"0"`, `"2.5"` and `""`.

<details class="dl-answer"><summary>answer</summary>

- `read_amount("50")` returns `50.0`.
- `read_amount("abc")` returns `None`, because `"abc"` is not all digits.
- `read_amount("0")` returns `None`. `"0"` is all digits, but a deposit of
  zero makes no sense, so the second check refuses it.
- `read_amount("2.5")` returns `None`, because the `.` is not a digit.
- `read_amount("")` returns `None`, because an empty string is not all
  digits.

Notice that `read_amount()` never calls `float()` on text it has not
checked. That is why `"abc"` gives `None`, and never a `ValueError`.

</details>

**6.** `read_amount("2.5")` refuses `2.5`, but `2.5` is a sensible amount
of money. Is that a bug? What could the program do about it?

<details class="dl-answer"><summary>answer</summary>

It is a limit of `.isdigit()`, and the program should at least be honest
about it. There are two simple choices:

- Tell the person the rule when you ask, for example
  `input("Amount, in whole euros: ")`. Then `2.5` breaking the rule is no
  surprise.
- Write a better check that also allows one `.` in the text. That takes
  more code, and it has more cases to test.

Either way, the program should never crash on `2.5`. Refusing it with a
clear message is much better than stopping with a `ValueError`.

</details>

**7.** Write a function `deposit_to_first(bank, amount_text)`. It should
use `read_amount()` to check `amount_text`.

- If the amount is not valid, print `Not a valid amount:` and the text,
  and change nothing.
- If it is valid, deposit it into the first account in the bank, and
  print the new total.

Test it with `"50"`, then `"abc"`, then `"-5"`. You need the cells above
to have run first.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Call `read_amount(amount_text)`, and keep the result in a variable.
2. If the result `is None`, print the message and `return`.
3. Otherwise, call `bank.accounts[0].deposit(...)` with the result.

**Think about:** what happens if the bank has no accounts yet?

</details>

<details class="dl-answer"><summary>answer</summary>

```python
def deposit_to_first(bank, amount_text):
    amount = read_amount(amount_text)
    if amount is None:
        print("Not a valid amount:", amount_text)
        return
    bank.accounts[0].deposit(amount)
    print("Total balance:", bank.total_balance())


bank = Bank("First Local")
bank.open_account("Alice", 100.0)
deposit_to_first(bank, "50")
deposit_to_first(bank, "abc")
deposit_to_first(bank, "-5")
```

This prints:

```text
Total balance: 150.0
Not a valid amount: abc
Not a valid amount: -5
```

With no accounts in the bank, `bank.accounts[0]` would stop the program
with `IndexError: list index out of range`. That is one more case to
check before a stranger uses the menu.

</details>

## Leaving the loop cleanly

This cell runs the whole menu loop from the tutorial. In place of
`input()`, it uses `fake_input()`, which takes the next answer from the
list `typed`. `typed.pop(0)` removes the first item from the list and
gives it back. `fake_input()` also prints the prompt and the answer, so
the output looks like a real session. The menu itself is not shown, to
keep the output short.

The cell uses `run_choice()` from the first cell on this page, so run
that cell first.

```python exec
id: leaving-the-loop-cleanly-practice-1
typed = ["2", "abc", "1", "9"]


def fake_input(prompt):
    answer = typed.pop(0)
    print(prompt + answer)
    return answer


bank = Bank("First Local")
running = True
while running:
    choice = fake_input("Choose: ")
    running = run_choice(bank, choice)
print("Goodbye.")
```

**8.** Predict every line the cell prints before you run it.

<details class="dl-answer"><summary>answer</summary>

```text
Choose: 2
Opened an account for New Customer.
Choose: abc
Not a menu option: abc
Choose: 1
Total balance: 100.0
Choose: 9
Goodbye.
```

The loop runs four times. On the fourth time, `run_choice()` returns
`False`, so `running` becomes `False` and the loop ends. Then
`Goodbye.` prints once, after the loop.

</details>

**9.** Change the first line to `typed = ["2", "1"]`, with no `"9"`.
What happens? What would happen with a real person and a real `input()`?

<details class="dl-answer"><summary>answer</summary>

The cell prints the first two answers as before. Then `fake_input()`
tries to take a third answer from an empty list, and Python stops with
`IndexError: pop from empty list`. `Goodbye.` never prints.

With a real person, the loop would ask `Choose: ` again, and keep asking,
until they typed `9`. The loop ends only when `run_choice()` returns
`False`. This is why a menu must always show how to quit.

</details>

**10.** Many programs quit when you type `q`. Change `run_choice()` so
that `"9"`, `"q"` and `"Q"` all end the loop. Test it with
`typed = ["1", "Q"]`.

<details class="dl-hint"><summary>stuck? here are some steps</summary>

1. Only one line of `run_choice()` needs to change: the `elif` for
   `"9"`.
2. The `in` operator checks whether a value is in a list:
   `choice in ["9", "q", "Q"]`.

**Try this next:** `choice.lower()` gives back the same string in small
letters, so `"Q".lower()` is `"q"`. Could you use it so that you only
need to list `"q"` once?

</details>

<details class="dl-answer"><summary>answer</summary>

```python
def run_choice(bank, choice):
    """Runs one menu choice. Returns False when the menu should stop."""
    if choice == "1":
        print("Total balance:", bank.total_balance())
    elif choice == "2":
        bank.open_account("New Customer", 100.0)
        print("Opened an account for New Customer.")
    elif choice in ["9", "q", "Q"]:
        return False
    else:
        print("Not a menu option:", choice)
    return True
```

Run this cell, then run the loop cell with `typed = ["1", "Q"]`. It
prints:

```text
Choose: 1
Total balance: 0
Choose: Q
Goodbye.
```

</details>

**11.** `run_choice()` returns `False` to say "stop". Why does it not
stop the loop itself? And why is `print("Goodbye.")` after the loop,
and not inside the `"9"` case of `run_choice()`?

<details class="dl-answer"><summary>answer</summary>

`run_choice()` cannot see the loop. The loop is in the code that calls
it. A function can only hand a value back to its caller, so it returns
`False`, and the caller decides what that means. This also keeps
`run_choice()` easy to test with a plain list of choices.

`Goodbye.` belongs to the end of the loop, not to one choice. It should
print once, however the loop ends. Suppose that later, the loop also ends
after three wrong answers in a row. A `Goodbye.` inside the `"9"` case
would not print then. A `Goodbye.` after the loop always prints.

</details>
