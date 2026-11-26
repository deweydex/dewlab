---
title: "Experiments with a calculator: turning typed text into sums"
year: "2026-2027"
version: 2026.11.26.1
---

# Experiments with a calculator: turning typed text into sums

A calculator app asks for two numbers and an operation, and prints the answer. It sounds small, but `input` always hands back text, people type surprising things, and some sums have no answer.

There are questions on this page to answer in words as well as in code. The **+ Text** button between cells adds a text cell where you can write your answers.

## 1. Plan first

**1.1** There are at least two ways a calculator could ask for a sum. It could ask three questions: first number, operation, second number. It could also ask for the whole sum on one line, like `12 / 4`. Write a short sample run for each. Which would you rather use? Which would be easier to build?

<!-- answer -->

**1.2** Write the user flow for your calculator. Include how the person goes back to the menu, using the word the class agreed on.

<!-- answer -->

**1.3** List everything a person could type that would cause trouble. Try to find at least four.

<!-- answer -->

## 2. Text that looks like a number

**2.1** Predict what each line prints, then run the cell.

```python exec
id: text-that-looks-like-a-number-1
print("12" + "4")
print(int("12") + int("4"))
print(float("12") / float("4"))
print(float("2.5") * 2)
```

<!-- answer -->

**2.2** Try each of these, one at a time: `int("2.5")`, `float("ten")`, `float(" 7 ")`, `float("")`. Which ones work? For the ones that fail, what is the error called?

```python exec
id: text-that-looks-like-a-number-2
print(int("2.5"))
```

<!-- answer -->

**2.3** Why might a calculator use `float` rather than `int` to turn the typed text into a number?

<!-- answer -->

## 3. One sum

**3.1** Write a calculator that asks for two numbers and an operation once, and prints the answer. It should handle `+`, `-`, `*` and `/`.

```python exec
id: one-sum-1
# your calculator here
```

<details class="dl-hint"><summary>smaller steps</summary>

1. Ask for the first number and turn it into a float.
2. Ask for the operation, and keep it as text.
3. Ask for the second number and turn it into a float.
4. Use `if` and `elif` to choose the sum from the operation.
5. What should happen when the operation is something else, like `%` or `x`?

</details>

```solution
first = float(input("First number: "))
operation = input("Operation (+ - * /): ").strip()
second = float(input("Second number: "))
if operation == "+":
    print(first + second)
elif operation == "-":
    print(first - second)
elif operation == "*":
    print(first * second)
elif operation == "/":
    print(first / second)
else:
    print("I don't know the operation", operation)
```

```typed
12
/
4
```

**3.2** Divide a number by 0. What happens? Change your calculator so it prints a clear message instead.

<!-- answer -->

**3.3** Some people type `x` for multiply. Change your calculator so `x` works too.

<!-- answer -->

## 4. Many sums

**4.1** Put your calculator inside a `while` loop, so it keeps asking for sums until the person types the agreed word for going back. Check for that word before you try to turn the text into a number.

```python exec
id: many-sums-1
# your calculator with a loop here
```

```solution
while True:
    first_text = input("First number: ").strip()
    if first_text == "back":
        break
    first = float(first_text)
    operation = input("Operation (+ - * /): ").strip()
    second = float(input("Second number: "))
    if operation == "+":
        print(first + second)
    elif operation == "-":
        print(first - second)
    elif operation == "*" or operation == "x":
        print(first * second)
    elif operation == "/":
        if second == 0:
            print("You can't divide by zero.")
        else:
            print(first / second)
    else:
        print("I don't know the operation", operation)
```

```typed
12
/
4
5
/
0
back
```

**4.2** What happens if you type `back` as the second number instead of the first? Is that a problem? What would you change?

<!-- answer -->

**4.3** Make the answer look like the sample run: `12.0 / 4.0 = 3.0`. Can you make it show `12 / 4 = 3.0` instead?

<!-- answer -->

## 5. When the person types a word

The program stops with a `ValueError` when someone types `ten` as a number. Python can try a line and catch the error instead of stopping. This short example shows how.

```python exec
id: when-the-person-types-a-word-1
text = "ten"
try:
    number = float(text)
    print("That is the number", number)
except ValueError:
    print("That is not a number:", text)
```

**5.1** Change `"ten"` to `"10"`, and run it again. Which lines run this time?

<!-- answer -->

**5.2** Use `try` and `except` in your calculator, so a typed word gives a message and the calculator asks again.

```python exec
id: when-the-person-types-a-word-2
# your calculator here
```

## 6. More to try

Choose any of these, or invent your own.

1. Add `**` for powers and `%` for the remainder.
2. Remember the last answer, and let the person type `ans` to use it as a number.
3. Accept the whole sum on one line, such as `12 / 4`. The text method `split` turns `"12 / 4"` into `["12", "/", "4"]`.
4. Keep a list of every sum done so far, and print it when the person types `history`.

```python exec
id: more-to-try-1
# your experiments here
```
