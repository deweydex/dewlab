---
title: "The Tentacular Plushies Quiz"
slug: the-tentacular-plushies-quiz
module: database-methods
module_title: "Database Methods"
year: "2026-2027"
series: practice
version: 2026.09.10.1
covers:
  task-1-a-products-table:
    covers: [DBM-LO10, DBM-LO11]
  task-2-a-transactions-table:
    covers: [DBM-LO10]
  task-3-add-products:
    touches: [DBM-LO4]
  task-5-query-the-data:
    touches: [DBM-LO5]
---

# The Tentacular Plushies Quiz

You are the new database administrator for Tentacular Plushies, a shop
that sells stuffed toys of octopuses, squid, and other tentacled sea
creatures. Five tasks build its database, one
piece at a time. Nothing here is graded. Each task has a check cell
below it. Run that cell, and it tells you, instantly and only in your
own browser, whether the task's requirements are met. Run it as often
as you like.

Write your SQL in this box as you go. Your code is saved on this
device, the same as every cell on this site. After a reload, run this
box again to rebuild your tables. Use the hints if you need them.

```sql exec
id: quiz-workspace
-- Build the database here, one task at a time. Run this box after
-- every change, then use each task's check cell below.
```

## Task 1: a products table

Create a table called `products` with these columns:

- `id` is a whole number that identifies the row, filled in for you.
- `product_name` is text.
- `category` is text.
- `price` is a number with a decimal point.
- `stock_quantity` is a whole number.
- `description` is text, and you can leave it blank.

<details class="dl-hint"><summary>hint</summary>

Start with `CREATE TABLE products (`, then list each column with its
type, the way the pages before this quiz did.

</details>

```python exec
id: check-products-table
# PRAGMA table_info lists a table's columns; an empty result means the
# table does not exist yet.
columns = {row[1] for row in db.execute("PRAGMA table_info(products)")}
required = {"id", "product_name", "category", "price", "stock_quantity"}
missing = required - columns
if not columns:
    print("There is no products table yet.")
elif missing:
    print("products is missing:", ", ".join(sorted(missing)) + ".")
check(not missing, True, label="products exists, with the columns this task asks for")
```

```hint
for: check-products-table
after: 2 failed checks

Read what the check says is missing. It names the exact column it could
not find.

Compare that name, letter by letter, with the list task 1 asks for. A
column name with an extra space, a different case, or a small spelling
change is usually the reason this check still says something is
missing, even after you create the table.

**Try this:** run `PRAGMA table_info(products);` in the SQL box, and read
the `name` column of its result against the list above.
```

## Task 2: a transactions table

Create a second table, `transactions`, that refers to `products`:

- `id` is a whole number that identifies the row, filled in for you.
- `product_id` is a whole number naming a row in `products`.
- `customer_name` is text.
- `quantity` is a whole number.

<details class="dl-hint"><summary>hint</summary>

`product_id INTEGER` is enough for this task. If you want to go further,
`FOREIGN KEY (product_id) REFERENCES products(id)` names the connection
explicitly, the way [a second table and a
join](tutorial:a-second-table-and-a-join) covered.

</details>

```python exec
id: check-transactions-table
columns = {row[1] for row in db.execute("PRAGMA table_info(transactions)")}
required = {"id", "product_id", "customer_name", "quantity"}
missing = required - columns
if not columns:
    print("There is no transactions table yet.")
elif missing:
    print("transactions is missing:", ", ".join(sorted(missing)) + ".")
check(not missing, True, label="transactions exists, with the columns this task asks for")
```

## Task 3: add products

Insert at least four products, across at least three categories. Give
each one a price between 10 and 60, and a stock quantity between 5 and
50.

<details class="dl-hint"><summary>hint</summary>

Categories like `'Octopus'`, `'Squid'`, `'Cuttlefish'` and `'Nautilus'`
work well for a shop like this. One `INSERT INTO products (...) VALUES
(...), (...), (...), (...);` can add all four rows at once.

</details>

```python exec
id: check-products-rows
columns = {row[1] for row in db.execute("PRAGMA table_info(products)")}
if not columns:
    print("products needs to exist before this check means anything.")
    enough_rows = False
    enough_categories = False
else:
    categories = [row[0] for row in db.execute("SELECT category FROM products")]
    print(f"products has {len(categories)} rows across {len(set(categories))} categories.")
    enough_rows = len(categories) >= 4
    enough_categories = len(set(categories)) >= 3
check(enough_rows and enough_categories, True, label="products has at least four rows across at least three categories")
```

```hint
for: check-products-rows
after: 2 failed checks

Read what the check counted: how many rows it found, and how many
different categories among them. Both numbers are in its message.

Count your own `INSERT` statements the same way. A single `INSERT INTO
products (...) VALUES (...), (...), (...), (...);` with four rows and
four different `category` values meets both counts in one statement.
Adding rows one at a time, or repeating the same category, is the usual
reason one count comes up short.
```

## Task 4: add transactions

Insert at least three transactions. Each one needs a `product_id` that
matches a real row in `products`.

<details class="dl-hint"><summary>hint</summary>

Run `SELECT id, product_name FROM products;` first, to see which `id`
belongs to which product.

</details>

```python exec
id: check-transactions-rows
columns = {row[1] for row in db.execute("PRAGMA table_info(transactions)")}
if not columns:
    print("transactions needs to exist before this check means anything.")
    row_count = 0
else:
    row_count = db.execute("SELECT COUNT(*) FROM transactions").fetchone()[0]
    print(f"transactions has {row_count} rows.")
check(row_count >= 3, True, label="transactions has at least three rows")
```

## Task 5: query the data

Try writing and running each of these three queries:

- Products with a `price` over 30, ordered by `price` from highest to
  lowest.
- Products with a `stock_quantity` under 15.
- Every transaction, showing `customer_name` and `quantity`.

<details class="dl-hint"><summary>hint</summary>

`SELECT * FROM products WHERE price > 30 ORDER BY price DESC;` is the
first of the three.

</details>

```hint
for: quiz-workspace
after: 2 empty results

Two queries in a row in the box above came back with no rows.

Look under the result: the page adds a note whenever this happens,
naming how many rows the table you queried actually holds. What does
that note say about your table?
```

```hint
for: quiz-workspace
after: 5 empty results
title: some steps

1. Read the note under the empty result. It already counts the rows in
   the table you asked about, or names the closest table or column it
   can find to the one you typed.
2. If the note says the table has no rows, it still needs data. Go back
   and finish Task 3 or Task 4 first.
3. If the note says the table already has rows, run `SELECT * FROM
   products;` (or `transactions`) on its own, and compare every value
   in a row against the condition you wrote.

**Think about:** a filter that matches nothing is not always a mistake
in the filter. Sometimes the data does not hold what you expected yet.

**Try this next:** try the same filter with a smaller number, such as
`price > 10`, to check whether any rows come back at all.
```

This check looks at whether your data can answer the first two of
these, not at the queries themselves. There is more than one correct
way to write a `SELECT`.

```python exec
id: check-quiz-queries
products_columns = {row[1] for row in db.execute("PRAGMA table_info(products)")}
transactions_columns = {row[1] for row in db.execute("PRAGMA table_info(transactions)")}
if not products_columns or not transactions_columns:
    print("Both tables are needed before this check means anything.")
    over_30_count = 0
    under_15_count = 0
else:
    over_30_count = db.execute("SELECT COUNT(*) FROM products WHERE price > 30").fetchone()[0]
    under_15_count = db.execute("SELECT COUNT(*) FROM products WHERE stock_quantity < 15").fetchone()[0]
    if over_30_count == 0:
        print("No product has a price over 30, so the first query would return nothing.")
    if under_15_count == 0:
        print("No product has a stock_quantity under 15, so the second query would return nothing.")
check(over_30_count > 0 and under_15_count > 0, True, label="your data can answer the first two queries")
```

## One way to do it

Every check passing means your own database already meets the tasks.
This is one complete solution, not the only one. Compare it with your
own to see a full example.

<details class="dl-answer"><summary>a worked solution</summary>

```sql
CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    product_name TEXT NOT NULL,
    category TEXT NOT NULL,
    price REAL NOT NULL,
    stock_quantity INTEGER NOT NULL,
    description TEXT
);

CREATE TABLE transactions (
    id INTEGER PRIMARY KEY,
    product_id INTEGER NOT NULL,
    customer_name TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    FOREIGN KEY (product_id) REFERENCES products(id)
);

INSERT INTO products (product_name, category, price, stock_quantity, description) VALUES
    ('Squishy Squid', 'Squid', 25.0, 20, 'A soft squid, six arms too many to count correctly'),
    ('Cuddly Cuttlefish', 'Cuttlefish', 35.0, 10, 'Changes colour if you believe hard enough'),
    ('Nautical Nautilus', 'Nautilus', 45.0, 8, 'A spiral shell, purely decorative'),
    ('Octo Buddy', 'Octopus', 55.0, 5, 'Eight arms of fun');

INSERT INTO transactions (product_id, customer_name, quantity) VALUES
    (1, 'Jane Doe', 2),
    (2, 'John Smith', 1),
    (3, 'Sam Lee', 3);

SELECT * FROM products WHERE price > 30 ORDER BY price DESC;

SELECT * FROM products WHERE stock_quantity < 15;

SELECT customer_name, quantity FROM transactions;
```

Only the last statement in a box like this one shows its result when
run, the same as any other SQL cell on this site. Run the three
`SELECT` statements one at a time to see each result.

</details>
