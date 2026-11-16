---
title: "Experiments with text: strings and quotes"
year: "2026-2027"
version: 2026.11.16.1
---

# Experiments with text: strings and quotes

A string is a piece of text. Run each cell, change one thing, and look at what comes back. Keep a note of each error name you meet. Each cell sets up everything it uses, so you can run the cells in any order.

## 1. Making a string

We make a string by putting characters between quotes. Python keeps every character between the quotes, spaces and digits included. It never looks inside the quotes for names.

**1.1** Run this. What type does Python report, and does it matter which kind of quote we use?

```python exec
id: making-a-string-1
print(type("hello"))
print(type('hello'))
print("cat" == 'cat')
```

**1.2** For each value in this cell, decide whether it is a string, a number or a name. Predict each line, and then run the cell.

```python exec
id: making-a-string-2
word = "word"
print(word)
print("word")
print(5)
print("5")
print(type(5), type("5"))
```

**1.3** Run this and read the error. Where does Python think the string ends? Fix it in two different ways.

```python exec
id: making-a-string-3
print('it's here')
```

```solution
for: making-a-string-3
title: one way to do it
print("it's here")
print('it\'s here')
```

**1.4** Run each of these broken lines, one at a time. Read each error and say what is missing.

```python exec
id: making-a-string-4
print("hello)
# print("hello')
# print(hello")
```

```solution
for: making-a-string-4
title: one way to do it
print("hello")
```

**1.5** Try to print `He said "it's fine"`, with both kinds of quote in the output.

```python exec
id: making-a-string-5
# your code here
```

```solution
for: making-a-string-5
title: one way to do it
print("He said \"it's fine\"")
```

**Worth knowing.** A backslash in front of a quote tells Python that the quote belongs to the text and does not end the string. We write `"He said \"hi\""`, and Python prints `He said "hi"`. A backslash in front of some letters makes a special character instead: `\n` starts a new line and `\t` jumps to the next tab stop.

**1.6** Run this. Then explain the last line, which prints something odd.

```python exec
id: making-a-string-6
print("a\tb")
print("a\nb")
print("Backslash: \\")
print("C:\new folder")
```

**1.7** Three quotes at each end let a string run over several lines. Run this. What happens to the line break inside the quotes?

```python exec
id: making-a-string-7
print("""line one
line two""")
```

## 2. Text that looks like a number

The string `"7"` holds the character 7. It looks the same as the number 7 when we print it, but Python treats it as text.

**2.1** Predict which comparisons print `True`, and then run the cell.

```python exec
id: text-that-looks-like-a-number-1
print(7 == 7.0)
print(7 == "7")
print("7" == '7')
```

**2.2** The function `repr` shows a value the way we would write it in code. How does `print` hide the difference between a number and a string?

```python exec
id: text-that-looks-like-a-number-2
print(7)
print("7")
print(repr(7))
print(repr("7"))
```

**2.3** Predict both lines, and then run them. What does `+` do with two strings?

```python exec
id: text-that-looks-like-a-number-3
print(7 + 7)
print("7" + "7")
```

**2.4** Run this and read the error from the bottom up. What does the error say about the two types?

```python exec
id: text-that-looks-like-a-number-4
print("7" + 7)
```

**2.5** Run each line, one at a time. Which of these work, and what does `*` do with a string?

```python exec
id: text-that-looks-like-a-number-5
print("ha" * 3)
# print(3 * "ha")
# print("ha" * 0)
# print("ha" * -1)
# print("ha" * 2.5)
# print("ha" * "ha")
```

**2.6** Try `-` between two strings. Which arithmetic operators work on strings?

```python exec
id: text-that-looks-like-a-number-6
print("7" - "2")
```

**Worth knowing.** We convert between types with `int`, `float` and `str`. The call `int("15")` gives back the number 15, and `str(15)` gives back the text `"15"`.

**2.7** This program should print `16`. Change one line so that it does.

```python exec
id: text-that-looks-like-a-number-7
age_text = "15"
print(age_text + 1)
```

```solution
for: text-that-looks-like-a-number-7
title: one way to do it
age_text = "15"
print(int(age_text) + 1)
```

**2.8** This program should print `You are 15 years old`. Change one line so that it does.

```python exec
id: text-that-looks-like-a-number-8
years = 15
print("You are " + years + " years old")
```

```solution
for: text-that-looks-like-a-number-8
title: one way to do it
years = 15
print("You are " + str(years) + " years old")
```

**2.9** Change the text inside `int` to each of these in turn, and note which ones fail: `"3.9"`, `"four"`, `""`, `" 7 "`, `"7 8"`, `"-5"`.

```python exec
id: text-that-looks-like-a-number-9
print(int("42"))
```

**2.10** Do the same for `float` with `"3.5"`, `"abc"`, `"1e3"`, `".5"` and `"inf"`.

```python exec
id: text-that-looks-like-a-number-10
print(float("2.5"))
```

## 3. Asking a string questions

A method is a function that belongs to a value. We call a method with a dot after the value, as in `"hello".upper()`. A string method never changes the string. It hands back a new value.

**3.1** Run this. Does `len` count spaces? Does it count the line break at the end of the last string?

```python exec
id: asking-a-string-questions-1
print(len("python"))
print(len(""))
print(len("a b"))
print(len("hello\n"))
```

**3.2** Predict each line, and then run the cell.

```python exec
id: asking-a-string-questions-2
print("python".upper())
print("PyThOn".lower())
print("hello world".title())
print("hello world".capitalize())
```

**3.3** Leave off the brackets after `upper`, and run the cell. What does Python print this time?

```python exec
id: asking-a-string-questions-3
print("python".upper())
```

**3.4** Run this. Does `replace` change the text that `fruit` holds? Which line shows you?

```python exec
id: asking-a-string-questions-4
fruit = "banana"
print(fruit.replace("a", "o"))
print(fruit)
```

Change the program so that `fruit` holds the new text.

```solution
for: asking-a-string-questions-4
title: one way to do it
fruit = "banana"
fruit = fruit.replace("a", "o")
print(fruit)
```

**3.5** Predict each line, and then run the cell. What does `find` give back when the text is missing?

```python exec
id: asking-a-string-questions-5
print("banana".count("a"))
print("banana".count("an"))
print("banana".find("n"))
print("banana".find("z"))
```

**3.6** Run this. What type of value does `in` give back?

```python exec
id: asking-a-string-questions-6
print("an" in "banana")
print("AN" in "banana")
print(type("an" in "banana"))
```

**3.7** Run this. What does `strip` take away, and what does it leave alone?

```python exec
id: asking-a-string-questions-7
padded = "  hello  "
print(len(padded))
print(len(padded.strip()))
print(len(padded.lstrip()))
```

**3.8** Predict which lines print `True`, and then run the cell.

```python exec
id: asking-a-string-questions-8
print("hello".startswith("he"))
print("123".isdigit())
print("12.5".isdigit())
print("-5".isdigit())
print("abc".isalpha())
print("ab c".isalpha())
```

## 4. Pieces of a string

Each character in a string has a position, which we call an index. The first character sits at index 0.

**4.1** Run this. Which index gives the first letter, and which gives the last?

```python exec
id: pieces-of-a-string-1
word = "python"
print(word[0])
print(word[1])
print(word[-1])
print(word[-2])
```

**4.2** Run this and read the error. How many characters does `"cat"` have, and what is its largest index?

```python exec
id: pieces-of-a-string-2
pet_word = "cat"
print(pet_word[3])
```

**4.3** Run this and read the error. What does the error say about changing a string?

```python exec
id: pieces-of-a-string-3
animal = "cat"
animal[0] = "b"
```

**4.4** A colon inside the brackets takes a slice. Predict each line, and then run the cell.

```python exec
id: pieces-of-a-string-4
word = "python"
print(word[0:3])
print(word[2:])
print(word[:2])
print(word[::-1])
```

## 5. Printing text

**5.1** Run this. What does `print` put between values that we separate with commas?

```python exec
id: printing-text-1
name = "Sam"
print("Hello,", name)
print("Hello, " + name)
print("Hello,", name, "!")
print("Hello, " + name + "!")
```

**5.2** Run this. What do `sep` and `end` control?

```python exec
id: printing-text-2
print("a", "b", "c", sep="-")
print("a", end="")
print("b")
```

**5.3** Run this. What does the `f` in front of the quote do, and what do the curly brackets do?

```python exec
id: printing-text-3
name = "Sam"
years = 15
print(f"{name} is {years} years old")
print(f"Next year {name} will be {years + 1}")
print(f"{name.upper()} shouts")
```

**5.4** Remove the `f` from the first `print` in 5.3. What changes?

## 6. Puzzles

**6.1** Print a row of 20 equals signs without typing 20 of them.

```python exec
id: puzzles-1
# your code here
```

```solution
for: puzzles-1
title: one way to do it
print("=" * 20)
```

**6.2** Print a box around a name, so that the box fits any name. For `Sam` the output looks like this.

```
+-----+
| Sam |
+-----+
```

```python exec
id: puzzles-2
name = "Sam"
# your code here
```

```solution
for: puzzles-2
title: one way to do it
name = "Sam"
border = "+" + "-" * (len(name) + 2) + "+"
print(border)
print("| " + name + " |")
print(border)
---
The border is four characters longer than the name: two spaces and two corners. Its length comes from `len(name)`, so it fits any name.
```

**6.3** You have the values `5` and `"5"`, and the operators `+` and `*`. Write one `print` for each target: `10`, `55`, `555` and `25`.

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

**6.4** Print the initials `A.L.` from these two names, using indexes.

```python exec
id: puzzles-4
first = "Ada"
last = "Lovelace"
# your code here
```

```solution
for: puzzles-4
title: one way to do it
first = "Ada"
last = "Lovelace"
print(first[0] + "." + last[0] + ".")
```

**6.5** Make the first letter of `name` a capital and leave the rest alone, using an index, a slice and `upper`. Do not use `capitalize`.

```python exec
id: puzzles-5
name = "dublin"
# your code here
```

```solution
for: puzzles-5
title: one way to do it
name = "dublin"
print(name[0].upper() + name[1:])
```

**6.6** Is `"racecar"` the same backwards? Print `True` or `False` with one comparison. Try another word.

```python exec
id: puzzles-6
word = "racecar"
# your code here
```

```solution
for: puzzles-6
title: one way to do it
word = "racecar"
print(word == word[::-1])
```

## 7. Looking back

**7.1** Which error names did you meet on this page? Write one sentence for each that says what caused it.

**7.2** Write down three values that look the same when we print them but differ in type.
