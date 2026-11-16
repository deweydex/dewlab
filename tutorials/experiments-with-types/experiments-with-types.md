---
title: "Experiments with types: what kind of thing is this?"
year: "2026-2027"
version: 2026.11.16.1
---

# Experiments with types: what kind of thing is this?

Every value in Python has a type, and the type decides what we can do with the value. The function `type` tells us the type of anything. Run each cell, change one thing at a time, and keep a note of each error name you meet.

## 1. Meeting the four basic types

**1.1** Run this. Which four types appear?

```python exec
id: meeting-the-four-basic-types-1
print(type(42))
print(type(3.14))
print(type("hello"))
print(type(True))
```

**1.2** Predict the type of each value before you run the cell. Then check.

```python exec
id: meeting-the-four-basic-types-2
print(type(7))
print(type(7.0))
print(type("7"))
print(type('7'))
print(type(7 == 7))
print(type("True"))
print(type(True))
print(type(-3))
print(type(1e3))
print(type(""))
```

**1.3** Are `"cat"` and `'cat'` the same value? Print `"cat" == 'cat'` and find out. Then try to make a string that holds the word `it's`, using each kind of quote in turn.

```python exec
id: meeting-the-four-basic-types-3
# your code here
```

```solution
for: meeting-the-four-basic-types-3
title: one way to do it
print("cat" == 'cat')
word = "it's"
print(word)
---
The two kinds of quote make the same string. A string with an apostrophe inside needs double quotes around it, or a backslash in front of the apostrophe.
```

**1.4** Try to print a string that contains both kinds of quote, for example `He said "it's fine"`.

```python exec
id: meeting-the-four-basic-types-4
# your code here
```

```solution
for: meeting-the-four-basic-types-4
title: one way to do it
print("He said \"it's fine\"")
```

**Worth knowing.** A backslash in front of a quote tells Python that the quote belongs to the text and does not end the string. We write `"He said \"hi\""`, and Python prints `He said "hi"`.

**1.5** Run this. What do `\t` and `\n` do?

```python exec
id: meeting-the-four-basic-types-5
print("a\tb")
print("a\nb")
```

**1.6** Print a string over two lines by using three quotes at each end.

```python exec
id: meeting-the-four-basic-types-6
print("""line one
line two""")
```

What happens to the line break inside the quotes?

## 2. Values that look alike

**2.1** Run this. Which of these comparisons print `True`?

```python exec
id: values-that-look-alike-1
print(7 == 7.0)
print(7 == "7")
print(type(7) == type(7.0))
print("7" == '7')
```

**2.2** The function `repr` shows a value the way Python writes it in code. Print `repr(7)`, `repr(7.0)` and `repr("7")`. How does `print` hide the difference between a number and a string?

```python exec
id: values-that-look-alike-2
print(7)
print("7")
print(repr(7))
print(repr("7"))
```

**2.3** Predict the two outputs, and then run them. What does `+` do for two strings?

```python exec
id: values-that-look-alike-3
print(7 + 7)
print("7" + "7")
```

**2.4** Run this and read the error from the bottom up. What does it say about the two types?

```python exec
id: values-that-look-alike-4
print("7" + 7)
```

**2.5** Run each line, one at a time. Which of these work, and what does `*` do to a string?

```python exec
id: values-that-look-alike-5
print("ha" * 3)
# print(3 * "ha")
# print("ha" * 0)
# print("ha" * -1)
# print("ha" * 2.5)
# print("ha" * "ha")
```

**2.6** Try `-` and `/` between two strings. Which operators work on strings?

```python exec
id: values-that-look-alike-6
print("7" - "2")
```

**2.7** Run this. What numbers do `True` and `False` stand for when we do arithmetic with them?

```python exec
id: values-that-look-alike-7
print(True + True)
print(True + 1)
print(True * 5)
print(False + 5)
```

**Worth knowing.** Python treats `True` as the whole number 1 and `False` as the whole number 0 when it does arithmetic. The type `bool` is a special kind of whole number.

## 3. Converting between types

**3.1** Predict the type of each result, and then run the cell.

```python exec
id: converting-between-types-1
print(type(int("42")))
print(type(float("42")))
print(type(str(42)))
print(type(bool(42)))
```

**3.2** Run this. Does `int` round a decimal number, or does it cut the decimal part off? Which test shows you?

```python exec
id: converting-between-types-2
print(int(3.9))
print(int(-3.9))
print(int(3.5))
```

**3.3** Compare `int` with `round`. Run this and look closely at the last three lines.

```python exec
id: converting-between-types-3
print(round(3.14159, 2))
print(round(3.14159))
print(round(0.5))
print(round(1.5))
print(round(2.5))
print(round(3.5))
```

What pattern do you see for the numbers that end in `.5`?

**3.4** Change the text inside `int` to each of these in turn, and note which ones fail: `"3.9"`, `"four"`, `""`, `" 7 "`, `"7 8"`, `"-5"`, `"+5"`.

```python exec
id: converting-between-types-4
print(int("42"))
```

**3.5** Do the same for `float`: `"3.5"`, `"abc"`, `"1e3"`, `".5"`, `"5."`, `"inf"`.

```python exec
id: converting-between-types-5
print(float("2.5"))
```

**3.6** Predict which of these print `False`, and then run the cell. What rule picks out the values that become `False`?

```python exec
id: converting-between-types-6
print(bool(0))
print(bool(1))
print(bool(-1))
print(bool(""))
print(bool(" "))
print(bool("False"))
print(bool(0.0))
print(bool(0.1))
```

**3.7** Run this. What do `int` and `float` do with `True` and `False`?

```python exec
id: converting-between-types-7
print(int(True))
print(float(True))
print(int(False))
print(str(True))
print(str(3.0))
```

**3.8** This program should print `16`. Change one line so that it does.

```python exec
id: converting-between-types-8
age = "15"
print(age + 1)
```

```solution
for: converting-between-types-8
title: one way to do it
age = "15"
print(int(age) + 1)
```

**3.9** This program should print `You are 15 years old`. Change one line so that it does.

```python exec
id: converting-between-types-9
age = 15
print("You are " + age + " years old")
```

```solution
for: converting-between-types-9
title: one way to do it
age = 15
print("You are " + str(age) + " years old")
```

**3.10** Predict the two lines, then run them. What is the difference between the two?

```python exec
id: converting-between-types-10
print("5" * 3)
print(int("5") * 3)
```

## 4. Asking a string questions

**4.1** Run this. Does `len` count spaces? Does it count the line break in the last string?

```python exec
id: asking-a-string-questions-1
print(len("python"))
print(len(""))
print(len("a b"))
print(len("hello\n"))
```

**4.2** Predict each line, and then run the cell.

```python exec
id: asking-a-string-questions-2
print("python".upper())
print("PyThOn".lower())
print("hello world".title())
print("hello world".capitalize())
print("PyThOn".swapcase())
```

**4.3** Leave off the brackets in the first line. What does Python print this time?

```python exec
id: asking-a-string-questions-3
print("python".upper())
```

**4.4** Run this. Does `replace` change the variable `word`? Which line shows you?

```python exec
id: asking-a-string-questions-4
word = "banana"
print(word.replace("a", "o"))
print(word)
word.replace("a", "o")
print(word)
```

How would you keep the changed word?

```solution
for: asking-a-string-questions-4
title: one way to do it
word = "banana"
word = word.replace("a", "o")
print(word)
---
A string cannot change, so `replace` hands back a new string. We keep it by attaching a name to it.
```

**4.5** Predict each line, then run them.

```python exec
id: asking-a-string-questions-5
print("banana".count("a"))
print("banana".count("an"))
print("banana".count("x"))
print("banana".find("n"))
print("banana".find("z"))
```

**4.6** Change `find` to `index` in the last line. How does the behaviour differ when the letter is missing?

```python exec
id: asking-a-string-questions-6
print("banana".find("z"))
```

**4.7** Run this. What type does `in` give back?

```python exec
id: asking-a-string-questions-7
print("an" in "banana")
print("AN" in "banana")
print("" in "banana")
print(type("an" in "banana"))
```

**4.8** Run this. What does `strip` take away, and what does it leave alone?

```python exec
id: asking-a-string-questions-8
text = "  hello  "
print(len(text))
print(len(text.strip()))
print(len(text.lstrip()))
print(len(text.rstrip()))
```

**4.9** Predict which of these print `True`, and then run the cell.

```python exec
id: asking-a-string-questions-9
print("hello".startswith("he"))
print("hello".endswith("lo"))
print("123".isdigit())
print("12.5".isdigit())
print("-5".isdigit())
print("".isdigit())
print("abc".isalpha())
print("ab c".isalpha())
```

## 5. Puzzles

**5.1** Predict the type of each expression, and then run the cell. Which results are surprising?

```python exec
id: puzzles-1
print(type(3 + 4))
print(type(3 + 4.0))
print(type(3 / 1))
print(type(3 // 1))
print(type("3" * 2))
print(type(3 > 2))
print(type(2 ** 3))
print(type(2 ** -1))
```

**5.2** Sort these five lines into groups that print the same thing. Make a prediction before you run them.

```python exec
id: puzzles-2
print(1 + 1)
print("1" + "1")
print("1" * 2)
print(int("1") + int("1"))
print(str(1) + str(1))
```

**5.3** You have the values `5` and `"5"`, and the operators `+` and `*`. Write one `print` for each target: `10`, `55`, `555` and `25`.

```python exec
id: puzzles-3
# your code here
```

```solution
for: puzzles-3
title: one way to do it
print(5 + 5)
print("5" + "5")
print("5" * 3)
print(5 * 5)
```

**5.4** Find a whole number `x` so that `type(x)` is `int` but `str(x)` has exactly five characters. Is there more than one answer?

```python exec
id: puzzles-4
x = 0
print(type(x))
print(len(str(x)))
```

```solution
for: puzzles-4
title: one way to do it
x = 12345
print(type(x))
print(len(str(x)))
---
Any whole number from 10000 to 99999 works. A negative number such as `-1234` also has five characters, because the minus sign counts.
```

**5.5** Make `bool(x)` print `False` in three different ways, using three different types.

```python exec
id: puzzles-5
# your code here
```

```solution
for: puzzles-5
title: one way to do it
print(bool(0))
print(bool(0.0))
print(bool(""))
```

**5.6** Using `"3"` and `3`, write one line that prints `6` and another that prints `33`.

```python exec
id: puzzles-6
# your code here
```

```solution
for: puzzles-6
title: one way to do it
print(int("3") + 3)
print("3" + str(3))
```

## 6. Looking back

**6.1** Which error names did you meet? Write one sentence for each that says what caused it.

**6.2** Write down three values that look the same when we print them but differ in type.
