```exam
title: Student Registry Database Practical
exam_code: hvit-registry-2026
version: 2026.09.01.1
total_marks: 60
time_allowed: 2 hours
student_details: [full name, student number]
python: [sqlite3, pandas, matplotlib, openpyxl]
setup_code: |
  import sqlite3
  import pandas as pd
  import matplotlib.pyplot as plt
  from dewmark_tools import (show, show_table, text_input,
                             number_input, dropdown, button)

  conn = sqlite3.connect("hvit_registry.db")
  cursor = conn.cursor()
data_files:
  - path: data/hvit_registry.db
    as: hvit_registry.db
    description: The main student registry database — Tasks 1 to 4.
  - path: data/late_arrivals.xlsx
    as: late_arrivals.xlsx
    description: Students who arrived from a previous academic period — Task 5.
  - path: data/equipment_survey.xlsx
    as: equipment_survey.xlsx
    description: The institute equipment and safety survey — Task 6.
instructions: |
  Answer every task. Each task is worth 10 marks; the marks for each
  part are shown beside it. Write your code in the code box under each
  part and press Run to test it — you can run a box as many times as
  you like, and only your last run is recorded. The set-up code at the
  top of the paper runs automatically and gives you a database
  connection called `conn` and a cursor called `cursor`; every code box
  shares one running Python session, so anything you define in one box
  is still there in the next. The three data files are listed in the
  side panel — use their names in your code exactly as written.
```

```section
name: TASKS
```

## The Hill Valley Institute of Technology student registry

The Hill Valley Institute of Technology has just moved its student
registry from a filing cabinet in the converted clock tower to an
SQLite database. As the institute's first junior database technician,
you have been asked to audit the database, build a data entry form,
produce a chart, and import records from two spreadsheets.

The database has four tables: **students**, **courses**,
**supervisors**, and **labs**. The five programmes stored in the
database are Temporal Engineering, Applied Hoverboard Dynamics,
Computational Flux Theory, Sports Almanac Data Science, and Nuclear
Waste Management.

### Task 1 — Exploring the database

```question
name: task1
marks: 10
topic: database exploration
```

The registrar needs a full audit of the database before the new term
begins.

**(a)** Use `PRAGMA table_info()` to display the column structure of
the `students` table, printing each row on its own line. *(3 marks)*

```answer
name: task1.structure
type: python-code
marks: 3
starter_code: |
  # (a) show the column structure of the students table
model_answer_code: |
  cursor.execute("PRAGMA table_info(students)")
  for row in cursor.fetchall():
      print(row)
```

```marking
marks: 3
guidance:
  - 1 mark for running the PRAGMA, 1 for fetching the rows, 1 for one
    row per line
  - accept pd.read_sql on the PRAGMA as a full alternative
```

**(b)** Write a `COUNT(*)` query for each of the four tables and print
a labelled result for each. *(3 marks)*

```answer
name: task1.counts
type: python-code
marks: 3
starter_code: |
  # (b) count the records in students, courses, supervisors, labs
model_answer_code: |
  for table in ["students", "courses", "supervisors", "labs"]:
      cursor.execute(f"SELECT COUNT(*) FROM {table}")
      print(f"{table}: {cursor.fetchone()[0]} records")
```

```marking
marks: 3
guidance:
  - 2 marks when all four tables are counted, 1 when at least two are
  - 1 mark for labelling each printed count with its table
  - four separate copied-out queries earn the same as a loop
```

**(c)** Use `pd.read_sql()` and `.head()` to display the first five
rows of each of the four tables. *(4 marks)*

```answer
name: task1.preview
type: python-code
marks: 4
starter_code: |
  # (c) preview the first five rows of each table
model_answer_code: |
  for table in ["students", "courses", "supervisors", "labs"]:
      df = pd.read_sql(f"SELECT * FROM {table}", conn)
      print(f"--- {table} ---")
      show(df.head())
```

```marking
marks: 4
guidance:
  - 2 marks for reading each table through pd.read_sql, 1 for limiting
    the preview with .head(), 1 for showing all four
```

### Task 2 — Filtering and sorting

```question
name: task2
marks: 10
topic: filtering and sorting
```

**(a)** Use `pd.read_sql()` with a `WHERE` clause to find every
student enrolled in the **Temporal Engineering** programme, and
display the result with `show()`. *(4 marks)*

```answer
name: task2.where
type: python-code
marks: 4
starter_code: |
  # (a) students on the Temporal Engineering programme
model_answer_code: |
  df = pd.read_sql(
      "SELECT * FROM students WHERE programme = 'Temporal Engineering'",
      conn)
  show(df)
```

```marking
marks: 4
guidance:
  - 2 marks for a correct WHERE clause, 1 for the exact programme
    string, 1 for displaying the frame
```

**(b)** Retrieve all courses sorted by **credits** in descending
order, and display the result with `show()`. *(3 marks)*

```answer
name: task2.orderby
type: python-code
marks: 3
starter_code: |
  # (b) courses by credits, highest first
model_answer_code: |
  df = pd.read_sql("SELECT * FROM courses ORDER BY credits DESC", conn)
  show(df)
```

```marking
marks: 3
guidance:
  - 1 mark for ORDER BY credits, 1 for descending order, 1 for
    displaying the frame
  - sorting in pandas with sort_values earns the same marks
```

**(c)** Load the whole `students` table into a DataFrame, then use a
pandas boolean filter to find every student whose **year_of_study**
is 1, and display the result with `show()`. *(3 marks)*

```answer
name: task2.boolean
type: python-code
marks: 3
starter_code: |
  # (c) first-year students, filtered in pandas
model_answer_code: |
  df = pd.read_sql("SELECT * FROM students", conn)
  show(df[df["year_of_study"] == 1])
```

```marking
marks: 3
guidance:
  - 1 mark for loading the full table, 2 for filtering in pandas
    rather than in SQL — the question tests the boolean filter
```

### Task 3 — A data entry form

```question
name: task3
marks: 10
topic: forms and inserting
```

Build a data entry form that registers new students. The `students`
table takes a **name** (text), a **date_of_birth** (text, in the form
YYYY-MM-DD), a **gender** (`F`, `M`, or `Other`), a **programme** (one
of the five programmes above), and a **year_of_study** (a whole number
from 1 to 3).

Your form must have a text input for the name, a text input for the
date of birth, a dropdown for gender, a dropdown for programme, and a
number input for year of study (lowest 1, highest 3, starting at 1) —
and a **Register Student** button that inserts the new record into the
`students` table, commits the change, displays a confirmation message,
and clears the name and date of birth fields.

The side panel's reference section describes each form helper and
shows a small worked form.

```answer
name: task3.form
type: python-code
marks: 10
starter_code: |
  # build the registration form here
model_answer_code: |
  name_input = text_input("Student name:")
  dob_input = text_input("Date of birth (YYYY-MM-DD):")
  gender_dd = dropdown("Gender:", options=["F", "M", "Other"])
  prog_dd = dropdown("Programme:", options=[
      "Temporal Engineering",
      "Applied Hoverboard Dynamics",
      "Computational Flux Theory",
      "Sports Almanac Data Science",
      "Nuclear Waste Management",
  ])
  year_input = number_input("Year of study:", min_val=1, max_val=3,
                            default=1)

  @button("Register Student")
  def register():
      cursor.execute(
          "INSERT INTO students (name, date_of_birth, gender,"
          " programme, year_of_study) VALUES (?, ?, ?, ?, ?)",
          (name_input.value, dob_input.value, gender_dd.value,
           prog_dd.value, int(year_input.value)))
      conn.commit()
      show(f"Registered: {name_input.value} ({prog_dd.value})")
      name_input.clear()
      dob_input.clear()
```

```marking
limit: 10
points:
  - 4 marks - all five controls present with sensible labels and the
    right options and limits
  - 3 marks - the button's INSERT is correct and the change is
    committed
  - 2 marks - a confirmation message appears after registering
  - 1 mark - the name and date of birth fields clear after registering
```

### Task 4 — A chart from a query

```question
name: task4
marks: 10
topic: aggregation and charts
```

**(a)** Write a SQL query using `GROUP BY` to count the students
enrolled in each programme. The result should have two columns — the
programme and a count — displayed with `show()`. *(4 marks)*

```answer
name: task4.groupby
type: python-code
marks: 4
starter_code: |
  # (a) student count per programme
model_answer_code: |
  df = pd.read_sql(
      "SELECT programme, COUNT(*) AS count FROM students"
      " GROUP BY programme", conn)
  show(df)
```

```marking
marks: 4
guidance:
  - 2 marks for grouping by programme, 1 for counting, 1 for a
    two-column result displayed with show
```

**(b)** Using the result from part (a), draw a vertical bar chart of
student count by programme. Include a title, an x-axis label, a y-axis
label, and `plt.tight_layout()`, and display it with `show(fig)`.
*(6 marks)*

```answer
name: task4.chart
type: python-code
marks: 6
starter_code: |
  # (b) bar chart of the counts from part (a)
model_answer_code: |
  fig, ax = plt.subplots()
  ax.bar(df["programme"], df["count"])
  ax.set_title("Students by programme")
  ax.set_xlabel("Programme")
  ax.set_ylabel("Number of students")
  plt.tight_layout()
  show(fig)
```

```marking
marks: 6
guidance:
  - 3 marks for a correct bar chart of the grouped counts
  - 1 mark each for the title, the pair of axis labels, and the
    tight_layout call with the figure displayed
```

### Task 5 — Importing from a spreadsheet

```question
name: task5
marks: 10
topic: excel import
```

Five students have arrived from a previous academic period. Their
records are in `late_arrivals.xlsx`, whose columns match the
`students` table exactly.

**(a)** Use `pd.read_excel()` to load `late_arrivals.xlsx`. Display
the DataFrame with `show()` and print its shape. *(4 marks)*

```answer
name: task5.load
type: python-code
marks: 4
starter_code: |
  # (a) load and inspect late_arrivals.xlsx
model_answer_code: |
  df_late = pd.read_excel("late_arrivals.xlsx")
  show(df_late)
  print(df_late.shape)
```

```marking
marks: 4
guidance:
  - 2 marks for reading the file, 1 for displaying it, 1 for printing
    the shape
```

**(b)** Use `.to_sql()` to append the DataFrame to the `students`
table — with `if_exists='append'` and `index=False`, never
`'replace'`, which would delete every existing record. Then confirm
the new total number of students with a `COUNT(*)` query and display
it. *(6 marks)*

```answer
name: task5.append
type: python-code
marks: 6
starter_code: |
  # (b) append the late arrivals and confirm the new total
model_answer_code: |
  df_late.to_sql("students", conn, if_exists="append", index=False)
  cursor.execute("SELECT COUNT(*) FROM students")
  show(f"Total students now in database: {cursor.fetchone()[0]}")
```

```marking
marks: 6
guidance:
  - 3 marks for the append with the right if_exists and index
    settings; using 'replace' loses these marks
  - 3 marks for confirming and displaying the new count
```

### Task 6 — Analysing the equipment survey

```question
name: task6
marks: 10
topic: spreadsheet analysis
```

The institute has completed an equipment and safety survey. The
results are in `equipment_survey.xlsx`, which has two sheets: **Survey
Results** and **Lab Summary**. The Survey Results sheet has four
columns — **staff_name**, **department**, **equipment_rating** (1 to
10), and **safety_rating** (1 to 10).

**(a)** Use `pd.read_excel()` with the `sheet_name` argument to load
the **Survey Results** sheet, and display its first few rows with
`show()`. *(3 marks)*

```answer
name: task6.load
type: python-code
marks: 3
starter_code: |
  # (a) load the Survey Results sheet
model_answer_code: |
  df_survey = pd.read_excel("equipment_survey.xlsx",
                            sheet_name="Survey Results")
  show(df_survey.head())
```

```marking
marks: 3
guidance:
  - 2 marks for naming the sheet in read_excel, 1 for showing the
    head of the frame
```

**(b)** Using a pandas boolean filter, find every staff member whose
**equipment_rating** is below 5, and display the result with
`show()`. *(3 marks)*

```answer
name: task6.filter
type: python-code
marks: 3
starter_code: |
  # (b) staff with an equipment rating below 5
model_answer_code: |
  show(df_survey[df_survey["equipment_rating"] < 5])
```

```marking
marks: 3
guidance:
  - 2 marks for the boolean filter on the right column, 1 for the
    strict comparison and display
```

**(c)** Draw a horizontal bar chart with each **staff_name** on the
y-axis and their **equipment_rating** on the x-axis. Add a vertical
line at 5 to mark the midpoint, include a title and axis labels, and
display it with `show(fig)`. *(4 marks)*

```answer
name: task6.chart
type: python-code
marks: 4
starter_code: |
  # (c) horizontal bar chart of equipment ratings
model_answer_code: |
  fig, ax = plt.subplots()
  ax.barh(df_survey["staff_name"], df_survey["equipment_rating"])
  ax.axvline(x=5, color="red", linestyle="--", label="Midpoint")
  ax.legend()
  ax.set_title("Equipment ratings by staff member")
  ax.set_xlabel("Equipment rating")
  ax.set_ylabel("Staff member")
  plt.tight_layout()
  show(fig)
```

```marking
marks: 4
guidance:
  - 2 marks for a correct horizontal bar chart, 1 for the midpoint
    line, 1 for the title and axis labels together
```

```reference
title: The form and display helpers
text: |
  The set-up code imports these helpers for you.

  - `show(value)` displays a value under your code: a DataFrame
    becomes a table, a matplotlib figure becomes a picture, and
    anything else is printed.
  - `show_table(rows, columns)` displays a list of rows as a table.
  - `text_input(label)` puts a labelled text box in your output and
    returns a handle; `handle.value` reads what was typed and
    `handle.clear()` empties the box.
  - `number_input(label, min_val, max_val, default)` is the same for
    numbers.
  - `dropdown(label, options)` is the same for a list of choices.
  - `@button("Label")` above a function makes a button that runs the
    function when clicked; anything the function shows appears under
    the button.
```

```reference
title: A worked form example
text: |
  This small form books a lab, and uses every helper the registration
  form needs:

      room = text_input("Room name:")
      seats = number_input("Seats needed:", min_val=1, max_val=40,
                           default=10)

      @button("Book room")
      def book():
          show(f"Booked {room.value} for {seats.value} seats")
          room.clear()
```

```reference
title: The database tables
text: |
  - **students** — student_id, name, date_of_birth, gender,
    programme, year_of_study
  - **courses** — course_id, course_name, credits, department
  - **supervisors** — supervisor_id, name, specialisation, year_joined
  - **labs** — lab_id, lab_name, building, capacity
```
