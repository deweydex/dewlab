---
title: "Asking with input()"
year: "2026-2027"
version: 2026.09.27.1
---

# Asking with input()

## A cell that asks

```python exec
id: ask-name
name = input("What is your name? ")
print("Hello, " + name)
```

## A function that asks until the answer makes sense

```python exec
id: ask-shift
def ask_shift():
    while True:
        text = input("Shift, 1 to 25: ")
        if text.isdigit() and 1 <= int(text) <= 25:
            return int(text)
        print("Please type a whole number from 1 to 25.")
```

```typed
seven
30
7
```

```inputs
ask_shift()
```

```solution
def ask_shift():
    while True:
        text = input("Shift, 1 to 25: ")
        if text.isdigit() and 1 <= int(text) <= 25:
            return int(text)
```
