---
title: "Inheritance: one class built on another — Practice"
practice_for: one-parent-many-children
year: "2026-2027"
version: 2026.09.25.1
---

# Inheritance: one class built on another — Practice

The answers are hidden until you open them. Many of these problems ask
you to predict an output before you run anything. Try not to check first.
When a prediction is wrong, finding out why teaches you more than a lucky
guess does.

## A class built on another class

```python exec
id: a-class-built-on-another-class-practice-1
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


class SavingsAccount(BankAccount):
    def __init__(self, owner, balance, interest_rate):
        super().__init__(owner, balance)
        self.interest_rate = interest_rate

    def add_interest(self):
        self.balance = self.balance + self.balance * self.interest_rate


savings = SavingsAccount("Priya", 1000.0, 0.1)
savings.add_interest()
print(savings.balance)
```

**1.** Predict the balance the cell prints. Then create a second
`SavingsAccount` with an interest rate of `0.2` and the same starting
balance. What will its balance be after `add_interest()`?

<details class="dl-answer"><summary>answer</summary>

`1100.0`, because `1000.0 + 1000.0 * 0.1 = 1100.0`.

With a rate of `0.2`: `1200.0`, because `1000.0 + 1000.0 * 0.2 = 1200.0`.

The two objects never share a balance. Each `SavingsAccount` object has
its own fields, the same as any two `BankAccount` objects.

</details>

**2.** `savings.deposit(50.0)` works, but `SavingsAccount` never defines
`deposit()`. Why does it work?

<details class="dl-answer"><summary>answer</summary>

`SavingsAccount(BankAccount)` inherits everything `BankAccount` defines,
including `deposit()`. Python looks for `deposit()` in `SavingsAccount`
first. It does not find one, so it uses the version in `BankAccount`.

</details>

**3.** `SavingsAccount`'s constructor contains the line
`super().__init__(owner, balance)`. Suppose you delete that line, and
leave only `self.interest_rate = interest_rate`. What goes wrong?

<details class="dl-answer"><summary>answer</summary>

`self.owner` and `self.balance` are never set. The first time
`add_interest()` runs, it reads `self.balance`, and Python stops with
`AttributeError: 'SavingsAccount' object has no attribute 'balance'`.

`super().__init__(...)` passes the owner and balance to `BankAccount`'s
own constructor, which sets those two fields. Without that line, nothing
sets them.

</details>

**4.** Write a `CurrentAccount(BankAccount)` class with one new field,
`overdraft_limit`, and no new methods. Create one, and print its
`overdraft_limit`.

<details class="dl-answer"><summary>answer</summary>

```python
class CurrentAccount(BankAccount):
    def __init__(self, owner, balance, overdraft_limit):
        super().__init__(owner, balance)
        self.overdraft_limit = overdraft_limit


current = CurrentAccount("Priya", 200.0, 100.0)
print(current.overdraft_limit)   # 100.0
```

This `CurrentAccount` stores the limit, but does not use it yet. Its
`withdraw()` is still the one it inherits from `BankAccount`. The next
section gives it a `withdraw()` of its own.

</details>

## Another kind of account

```python exec
id: another-kind-of-account-1
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


class CurrentAccount(BankAccount):
    def __init__(self, owner, balance, overdraft_limit):
        super().__init__(owner, balance)
        self.overdraft_limit = overdraft_limit

    def withdraw(self, amount):
        if amount > self.balance + self.overdraft_limit:
            print("Refused: over the overdraft limit.")
            return
        self.balance = self.balance - amount


current = CurrentAccount("Ben", 200.0, 100.0)
current.withdraw(300.0)
print(current.balance)
```

**5.** Predict what the cell prints. Then change `300.0` to `301.0`, and
predict again.

<details class="dl-answer"><summary>answer</summary>

With `300.0`: `-100.0`. The withdrawal is allowed, because `300.0` is not
more than `self.balance + self.overdraft_limit`, which is
`200.0 + 100.0 = 300.0`.

With `301.0`: `Refused: over the overdraft limit.`, then `200.0`. One
more than the limit, and the whole withdrawal is refused. The balance does
not change.

</details>

**6.** The fee version of `SavingsAccount.withdraw()`, from the tutorial,
calls `super().withdraw(amount + 2.0)`. `CurrentAccount.withdraw()` above
does not call `super().withdraw()` at all. Why not?

<details class="dl-answer"><summary>answer</summary>

The parent's check, `amount > self.balance`, is the wrong check for a
`CurrentAccount`. It would refuse every withdrawal that goes into the
overdraft, and allowing those is the whole reason `CurrentAccount`
exists.

The savings fee only changes the *amount* that is checked, so the
parent's check still fits. `CurrentAccount` needs a different check, so
it writes its own. It does not pass anything to the parent's version.

</details>

**7.** Write a cell that creates a `CurrentAccount` with balance `50.0`
and overdraft limit `0.0`. Predict what `withdraw(50.0)` does, and then
what `withdraw(1.0)` does. Run it to check.

<details class="dl-answer"><summary>answer</summary>

```python
current = CurrentAccount("Ben", 50.0, 0.0)
current.withdraw(50.0)
print(current.balance)   # 0.0
current.withdraw(1.0)    # prints: Refused: over the overdraft limit.
print(current.balance)   # still 0.0
```

An overdraft limit of `0.0` behaves exactly like a plain `BankAccount`.
`amount > self.balance + 0.0` is the same comparison that
`BankAccount.withdraw()` makes. `CurrentAccount` does not need a
separate case for "no overdraft at all", because the general rule already
covers it.

</details>

## Many kinds, one loop

```python exec
id: many-kinds-one-loop-1
class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance

    def withdraw(self, amount):
        if amount > self.balance:
            print("Refused: not enough balance.")
            return
        self.balance = self.balance - amount


class CurrentAccount(BankAccount):
    def __init__(self, owner, balance, overdraft_limit):
        super().__init__(owner, balance)
        self.overdraft_limit = overdraft_limit

    def withdraw(self, amount):
        if amount > self.balance + self.overdraft_limit:
            print("Refused: over the overdraft limit.")
            return
        self.balance = self.balance - amount


plain = BankAccount("Cara", 80.0)
current = CurrentAccount("Ben", 80.0, 20.0)

for account in [plain, current]:
    account.withdraw(90.0)
    print(account.owner, account.balance)
```

**8.** Predict every line the cell prints before you run it.

<details class="dl-answer"><summary>answer</summary>

`Refused: not enough balance.`, then `Cara 80.0`. The amount `90.0` is
more than `plain`'s balance, and a plain account has no overdraft.

`Ben -10.0`. The amount `90.0` is within `current`'s limit of
`80.0 + 20.0 = 100.0`.

</details>

**9.** The loop calls `account.withdraw(90.0)`, and never checks which
class `account` belongs to. In your own words, what is *polymorphism*?
Where does it show up in this cell?

<details class="dl-answer"><summary>answer</summary>

Polymorphism is one method call running a different version of the
method, depending on the class of the object.

`account.withdraw(90.0)` is the same line for both objects in the loop.
For `plain`, it runs `BankAccount`'s check. For `current`, it runs
`CurrentAccount`'s check. The loop never needs to know which one it has.

</details>

**10.** Add a `SavingsAccount` to the list, next to `plain` and
`current`. Does the loop still work, with no change to the loop itself?

<details class="dl-answer"><summary>answer</summary>

Yes.

```python
class SavingsAccount(BankAccount):
    def __init__(self, owner, balance, interest_rate):
        super().__init__(owner, balance)
        self.interest_rate = interest_rate


savings = SavingsAccount("Priya", 200.0, 0.1)

for account in [plain, current, savings]:
    account.withdraw(90.0)
    print(account.owner, account.balance)
```

If you run this straight after the cell above, it prints `Refused: not
enough balance.`, `Cara 80.0`, `Refused: over the overdraft limit.`,
`Ben -10.0` and `Priya 110.0`. Ben's second withdrawal is refused because
he is already `10.0` into his overdraft.

`SavingsAccount` inherits `withdraw()` unchanged from `BankAccount`, so it
behaves the way `plain` does. The loop never names `SavingsAccount`, and
it does not need to.

</details>
