---
title: "Experiments with if: one decision"
year: "2026-2027"
version: 2026.11.16.1
---

# Experiments with if: one decision

An `if` statement lets a program choose whether to run some lines. Run each cell, change the numbers, and find out which lines run. Keep a note of each error name you meet. Each cell sets up everything it uses.

## 1. The parts of an if

An `if` statement has four parts: the word `if`, a condition, a colon, and an indented block underneath. Python runs the block only when the condition is `True`. The block ends at the first line that is not indented.

**1.1** Run this. Then change `25` to `10` and run it again. Which lines print each time?

```python exec
id: the-parts-of-an-if-1
temperature = 25
if temperature > 20:
    print("warm")
print("done")
```

**1.2** Find the four parts of the `if` in this program, and decide which lines belong to the block. Predict the output when `x` is 3 and when `x` is 12, and then check.

```python exec
id: the-parts-of-an-if-2
x = 3
print("start")
if x > 10:
    print("big")
    print("very big")
print("end")
```

**1.3** Write an `if` with these parts. The condition is `score >= 50`, and the block prints `pass` and then `well done`. Test it with a score above 50 and a score below 50.

```python exec
id: the-parts-of-an-if-3
score = 64
# your code here
```

```solution
for: the-parts-of-an-if-3
title: one way to do it
score = 64
if score >= 50:
    print("pass")
    print("well done")
```

**1.4** Each of the next four cells breaks one part of an `if`. Run each one, read the error, and fix it. This one has lost its colon.

```python exec
id: the-parts-of-an-if-4
level = 4
if level > 3
    print("high")
```

```solution
for: the-parts-of-an-if-4
title: one way to do it
level = 4
if level > 3:
    print("high")
```

**1.5** This one has lost its indentation.

```python exec
id: the-parts-of-an-if-5
level = 4
if level > 3:
print("high")
```

```solution
for: the-parts-of-an-if-5
title: one way to do it
level = 4
if level > 3:
    print("high")
```

**1.6** This one uses the wrong kind of equals sign.

```python exec
id: the-parts-of-an-if-6
level = 4
if level = 4:
    print("four")
```

```solution
for: the-parts-of-an-if-6
title: one way to do it
level = 4
if level == 4:
    print("four")
```

**1.7** This one indents its block by four spaces on one line and by two on the next.

```python exec
id: the-parts-of-an-if-7
level = 4
if level > 3:
    print("high")
  print("very high")
```

```solution
for: the-parts-of-an-if-7
title: one way to do it
level = 4
if level > 3:
    print("high")
    print("very high")
```

**1.8** Run this with `x` set to 3 and to 12. Then indent the last line by four spaces, and run it with both values again. What moved?

```python exec
id: the-parts-of-an-if-8
x = 3
if x > 10:
    print("big")
print("checked")
```

**1.9** Remove the `print` from the block, so that the `if` has an empty block, and run the cell. Then put the word `pass` in the block. What does `pass` do?

```python exec
id: the-parts-of-an-if-9
x = 3
if x > 10:
    print("big")
print("end")
```

**1.10** A condition does not have to be a comparison. Replace `5` with each of `0`, `""`, `"no"`, `True`, `False` and `" "`. Which values make the block run?

```python exec
id: the-parts-of-an-if-10
if 5:
    print("ran")
```

## 2. Where the boundary sits

**2.1** Run this with `age` set to 17, 18 and 19. Then change `>=` to `>` and run all three again. Which age changed its answer?

```python exec
id: where-the-boundary-sits-1
age = 18
if age >= 18:
    print("can vote")
```

**2.2** A shop gives free delivery on orders of 50 euros or more. Write the `if` so that an order of exactly 50 gets free delivery. Test it with 49.99, 50 and 50.01.

```python exec
id: where-the-boundary-sits-2
order = 50
# your code here
```

```solution
for: where-the-boundary-sits-2
title: one way to do it
order = 50
if order >= 50:
    print("free delivery")
```

**2.3** The condition below should be true for numbers from 1 to 10, including both ends. Run it with 0, 1, 10 and 11, and fix the mistake.

```python exec
id: where-the-boundary-sits-3
n = 10
if n > 1 and n < 10:
    print("in range")
```

```solution
for: where-the-boundary-sits-3
title: one way to do it
n = 10
if n >= 1 and n <= 10:
    print("in range")
```

## 3. else

The word `else` adds a second block, which runs when the condition is `False`. Exactly one of the two blocks runs, never both and never neither.

**3.1** Run this with `age` set to 17 and 18.

```python exec
id: else-1
age = 15
if age >= 18:
    print("adult")
else:
    print("minor")
```

**3.2** This `else` has a condition. Run it, read the error and fix it.

```python exec
id: else-2
age = 15
if age >= 18:
    print("adult")
else age < 18:
    print("minor")
```

```solution
for: else-2
title: one way to do it
age = 15
if age >= 18:
    print("adult")
else:
    print("minor")
```

**3.3** This `else` has no `if` above it. Run it and read the error.

```python exec
id: else-3
age = 15
else:
    print("minor")
```

**3.4** These two programs both use two blocks. Run each with `x` set to 3 and to 12. Do they always print the same? Change one program so that it prints something different from the other for some value of `x`.

```python exec
id: else-4
x = 3
if x > 10:
    print("big")
else:
    print("small")
```

```python exec
id: else-5
x = 3
if x > 10:
    print("big")
if x <= 10:
    print("small")
```

## 4. Programs with one decision

**4.1** Ask for a whole number and print `even` or `odd`.

```python exec
id: programs-with-one-decision-1
# your code here
```

```typed
7
```

```solution
for: programs-with-one-decision-1
title: one way to do it
n = int(input("Number: "))
if n % 2 == 0:
    print("even")
else:
    print("odd")
```

**4.2** Ask for a password. Print `welcome` if it is `swordfish` and `denied` otherwise. Then change the program so that `Swordfish` and `SWORDFISH` work as well.

```python exec
id: programs-with-one-decision-2
# your code here
```

```typed
Swordfish
```

```solution
for: programs-with-one-decision-2
title: one way to do it
password = input("Password: ")
if password.lower() == "swordfish":
    print("welcome")
else:
    print("denied")
---
Turning the answer into lower case before comparing lets `Swordfish` and `SWORDFISH` through as well.
```

**4.3** Ask for two numbers and print the larger one.

```python exec
id: programs-with-one-decision-3
# your code here
```

```typed
8
3
```

```solution
for: programs-with-one-decision-3
title: one way to do it
a = float(input("First: "))
b = float(input("Second: "))
if a > b:
    print(a)
else:
    print(b)
```

**4.4** Ask for some text. If the text is made only of digits, print the number doubled. Otherwise print `that is not a whole number`.

```python exec
id: programs-with-one-decision-4
# your code here
```

```typed
12
```

```solution
for: programs-with-one-decision-4
title: one way to do it
text = input("Type a whole number: ")
if text.isdigit():
    print(int(text) * 2)
else:
    print("that is not a whole number")
```

**4.5** Ask for a price. Take 10 percent off when the price is over 100, and print what the customer pays.

```python exec
id: programs-with-one-decision-5
# your code here
```

```typed
120
```

```solution
for: programs-with-one-decision-5
title: one way to do it
price = float(input("Price: "))
if price > 100:
    price = price * 0.9
print(price)
```

## 5. A decision in one line

**5.1** Run this. How does the last line compare with the four lines above it?

```python exec
id: a-decision-in-one-line-1
age = 15
if age >= 18:
    print("adult")
else:
    print("minor")
print("adult" if age >= 18 else "minor")
```

**Worth knowing.** The form `A if condition else B` is a single expression. It gives back `A` when the condition is true and `B` when it is false. We can put it inside a `print`, or on the right of an `=`.

**5.2** Rewrite this program with a one-line `if` and `else` on the right of the `=`.

```python exec
id: a-decision-in-one-line-2
n = 7
if n % 2 == 0:
    kind = "even"
else:
    kind = "odd"
print(kind)
```

```solution
for: a-decision-in-one-line-2
title: one way to do it
n = 7
kind = "even" if n % 2 == 0 else "odd"
print(kind)
```

**5.3** Make `a` hold the smaller of two values and `b` hold the larger, using one `if` and a third name.

```python exec
id: a-decision-in-one-line-3
a = 9
b = 4
# your code here
print(a, b)
```

```solution
for: a-decision-in-one-line-3
title: one way to do it
a = 9
b = 4
if a > b:
    temporary = a
    a = b
    b = temporary
print(a, b)
```

## 6. Looking back

**6.1** Which error names did you meet on this page? Write one sentence for each that says what caused it.

**6.2** How does Python know where the block of an `if` ends?
