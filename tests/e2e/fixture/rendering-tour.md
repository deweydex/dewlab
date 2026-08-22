---
title: "Rendering Tour"
slug: rendering-tour
module: fixtures
year: "2026-2027"
series: e2e
version: 1
covers:
  matplotlib:
    covers: [MIT-5.10]
  when-it-goes-wrong:
    covers: [PDP-LO9]
---

<!--
A test fixture, not a tutorial. Its cells exist to exercise every branch of the
output renderer in one page — printed text, a last expression, a DataFrame, a
figure, a traceback, the tools, the widgets — so the browser tests can drive
them all against one Pyodide boot. Nothing here is meant to teach anything, and
it deliberately does not live in tutorials/.

Keep the cell ids stable: the tests select on them.
-->

## Running code

Every cell below is live. Edit it, press **Run** (or Ctrl-Enter), and the
output appears directly underneath — the same prose, cell, output rhythm every
dewlab tutorial follows.

```python exec
id: plain-python
# Printed text and the value of the last expression both show up.
for n in range(3):
    print("counting:", n)

2 ** 10
```

## numpy

Whole arrays at once.

```python exec
id: numpy-basics
hint: Arrays behave like a whole column at once, not one number at a time.
import numpy as np

readings = np.array([12.5, 13.0, 11.75, 14.25])
print("mean:", readings.mean())
readings * 2
```

## pandas

A DataFrame renders as a table.

```python exec
id: pandas-table
import pandas as pd

df = pd.DataFrame({
    "country": ["Ireland", "Spain", "Japan", "Kenya"],
    "life_expectancy": [82.4, 83.2, 84.8, 66.7],
})
df[df["life_expectancy"] > 75]
```

## matplotlib

A figure renders as an image.

```python exec
id: matplotlib-figure
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 2 * np.pi, 200)
plt.plot(x, np.sin(x))
plt.title("One period of sin(x)")
```

Every textbook ends a plot with `plt.show()`, so students write it. It renders
the figure rather than warning about a canvas it cannot open.

```python exec
id: matplotlib-show
import matplotlib.pyplot as plt

plt.plot([1, 4, 9, 16])
plt.title("Squares")
plt.show()
print("after the plot")
```

## When it goes wrong

Errors are part of the lesson.

```python exec
id: error-traceback
# A mistake should point at the student's own line,
# not at dewlab's plumbing.
total = 0
for value in [1, 2, "three"]:
    total += value
```

## Checking your own answer

```python exec
id: tools-show-check
hint: check() is feedback, not a mark. Nothing is recorded.
show("show() renders anything, mid-cell.")
show_table(df, max_rows=3, caption="First three rows")

check(sum([1, 2, 3]), 6, label="Does the total come out right?")
check(0.1 + 0.2, 0.3)          # floats compare within a tolerance
check(2 + 2, 5)                # and a wrong answer says so
```

## Widgets

Type something, then press the button.

```python exec
id: tools-widgets
name = text_input("Your name", value="")
units = dropdown("Units", ["metric", "imperial"])

def greet():
    print(f"Hello {name.value or 'there'} — using {units.value} units.")

button("Say hello", on_click=greet)
```
