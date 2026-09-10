---
title: "The Tentacular Plushies quiz"
slug: the-tentacular-plushies-quiz
module: data
module_title: "Data"
series: practice
version: 2026.09.05.1
---

# The Tentacular Plushies quiz

You are the new database administrator for Tentacular Plushies, a shop
that sells stuffed cephalopod toys. Five tasks build its database, one
piece at a time. Nothing here is graded. Each task has a Check my work
button that tells you, instantly and only in your own browser, whether
that task's requirements are met. Use it as often as you like.

Write your SQL in this box as you go. It saves in this browser as you
run it, so a reload does not lose your work. Use the hints if you need
them — they are there for that.

```sql cell=quiz persist
-- Build the database here, one task at a time. Run this box after
-- every change, then use each task's Check my work button below.
```

## Task 1: a products table

Create a table called `products` with these columns:

- `id` — a whole number that identifies the row, filled in for you
- `product_name` — text
- `category` — text
- `price` — a number with a decimal point
- `stock_quantity` — a whole number
- `description` — text, optional

<details class="dl-hint"><summary>hint</summary>

Start with `CREATE TABLE products (`, then list each column with its
type, the way the pages before this quiz did.

</details>

```sql-check db=quiz task=check_products_table
```

```hint
for: check_products_table
after: 2 failed checks

Read what the check says is missing. It names the exact column it could
not find.

Compare that name, letter by letter, with the list task 1 asks for. A
column name with an extra space, a different case, or a small spelling
change is the most common reason this check still says something is
missing, even after you create the table.

**Try this:** run `PRAGMA table_info(products);` in the SQL box, and read
the `name` column of its result against the list above.
```

## Task 2: a transactions table

Create a second table, `transactions`, that refers to `products`:

- `id` — a whole number that identifies the row, filled in for you
- `product_id` — a whole number naming a row in `products`
- `customer_name` — text
- `quantity` — a whole number

<details class="dl-hint"><summary>hint</summary>

`product_id INTEGER` is enough for this task. If you want to go further,
`FOREIGN KEY (product_id) REFERENCES products(id)` names the connection
explicitly, the way [a second table and a
join](tutorial:a-second-table-and-a-join) covered.

</details>

```sql-check db=quiz task=check_transactions_table
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

```sql-check db=quiz task=check_products_rows
```

```hint
for: check_products_rows
after: 2 failed checks

Read what the check counted: how many rows it found, and how many
different categories among them. Both numbers are in its message.

Count your own `INSERT` statements the same way. A single `INSERT INTO
products (...) VALUES (...), (...), (...), (...);` with four rows and
four different `category` values meets both counts in one statement —
adding rows one at a time, or repeating the same category, is the usual
reason one count comes up short.
```

## Task 4: add transactions

Insert at least three transactions. Each one needs a `product_id` that
matches a real row in `products`.

<details class="dl-hint"><summary>hint</summary>

Run `SELECT id, product_name FROM products;` first, to see which `id`
belongs to which product.

</details>

```sql-check db=quiz task=check_transactions_rows
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

This check looks at whether your data can answer all three, not at the
queries themselves. There is more than one correct way to write a
`SELECT`.

```sql-check db=quiz task=check_quiz_queries
```

## One way to do it

Every check passing means your own database already meets the tasks.
This is one complete solution, not the only one, for comparing against
if you want to see a full example.

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
