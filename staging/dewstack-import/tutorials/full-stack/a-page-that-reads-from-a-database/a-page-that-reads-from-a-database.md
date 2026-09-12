---
title: "A page that reads from a database"
slug: a-page-that-reads-from-a-database
module: full-stack
module_title: "Full stack"
series: putting-it-together
version: 2026.09.06.1
---

# A page that reads from a database

Every earlier page kept its database and its page apart: a SQL cell's
own table on one side, HTML and CSS on the other, never in the same
sentence. A real website is not built that way. A shop's page shows the
products actually in its database, not a copy typed into the HTML by
hand — the two are joined. This page joins them for the first time, in
about a dozen lines.

## The table

The same shop database earlier pages have used, small enough to read
in one glance.

```sql cell=products
CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    name TEXT,
    price REAL
);

INSERT INTO products (name, price) VALUES
    ('Mug', 8.5),
    ('Notebook', 3.0),
    ('Tote bag', 12.0),
    ('Sticker sheet', 4.5),
    ('Water bottle', 15.0);
```

Run it. Nothing on the page shows this table yet — the cell below is
what will.

## A page that draws its own rows

```html app=read
<table>
  <thead>
    <tr><th>Name</th><th>Price</th></tr>
  </thead>
  <tbody></tbody>
</table>
```

```css app=read
table { width: 100%; border-collapse: collapse; }
th, td { text-align: left; padding: 0.4rem 0.6rem; border-bottom: 1px solid #ccc; }
```

```js app=read
async function draw() {
  const rows = await dlQuery("products", "SELECT name, price FROM products ORDER BY name");
  const tbody = root.querySelector("tbody");
  tbody.innerHTML = "";
  for (const row of rows) {
    const tr = document.createElement("tr");
    tr.innerHTML = `<td>${row.name}</td><td>€${row.price.toFixed(2)}</td>`;
    tbody.appendChild(tr);
  }
}

draw();
```

Press Run. The table above fills in — five rows, the same five the SQL
cell inserted.

## Reading the dozen lines

`dlQuery("products", "SELECT name, price FROM products ORDER BY name")`
runs that query against the `products` table — the exact table the SQL
cell above built, since this cell shares its name. What comes back is a
**result set**: one row per match, each row a plain object whose keys
are the column names the `SELECT` asked for. `row.name` and `row.price`
read straight off it.

The loop turns each row into a `<tr>`, and `tbody.appendChild(tr)` adds
it to the table already sitting in this cell's own HTML pane. `root` is
this cell's own little piece of the page — the only part its JavaScript
is meant to touch, the way `root.querySelector("tbody")` finds the one
inside it rather than some other table elsewhere on the page.

Change the query to
`"SELECT name, price FROM products WHERE price < 10 ORDER BY name"` and
press Run again. Three rows, not five — the table changed because the
**query** changed, not because anything about the page's own HTML did.

## Asking the database, not just reading it

A shop's page usually lets a visitor search, not just look. Add an
input, and read it.

```html app=search
<table>
  <thead>
    <tr><th>Name</th><th>Price</th></tr>
  </thead>
  <tbody></tbody>
</table>
<label for="search">Search by name</label>
<input type="text" id="search" placeholder="Type part of a name…">
```

```js app=search
async function draw(filter) {
  const sql = filter
    ? "SELECT name, price FROM products WHERE name LIKE ? ORDER BY name"
    : "SELECT name, price FROM products ORDER BY name";
  const rows = await dlQuery("products", sql, filter ? [`%${filter}%`] : []);
  const tbody = root.querySelector("tbody");
  tbody.innerHTML = "";
  for (const row of rows) {
    const tr = document.createElement("tr");
    tr.innerHTML = `<td>${row.name}</td><td>€${row.price.toFixed(2)}</td>`;
    tbody.appendChild(tr);
  }
}

root.querySelector("#search").addEventListener("input", (event) => draw(event.target.value));
draw();
```

Run it, then type "bag" into the box. One row. The `?` in the query is
a placeholder — `dlQuery`'s third argument fills it in, rather than the
typed text being pasted straight into the SQL. That difference matters:
a visitor's own text might contain a quote mark, or something stranger,
and text pasted directly into a query can change what the query does,
not just what it matches. A placeholder holds its place as one value,
whatever it is spelled, and never becomes SQL of its own.

## Your turn

Add a second search box, this time filtering by a maximum price. Its
query needs two placeholders — one for the name text, one for the
price — and `dlQuery`'s third argument becomes a two-item list,
`[name, maxPrice]`, in the same order as the two `?`s in the SQL.

## What you have now

- **Full stack** — a page whose HTML shows a database's own rows,
  rather than a copy of them typed in by hand. This page, start to
  finish, is a small one.
- **Query** — the `SELECT` a page's own JavaScript sends to its
  database, built fresh each time something changes rather than
  written once.
- **Result set** — what a query hands back: one row per match, ready
  to become HTML the way this page's loop does.
- **Placeholder** — a `?` in a query, filled in by a value passed
  separately rather than pasted into the query's own text.
