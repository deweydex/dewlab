---
title: "A page that reads from a database"
slug: a-page-that-reads-from-a-database
module: full-stack
module_title: "Full Stack"
year: "2026-2027"
series: putting-it-together
version: 2026.09.12.1
---

# A page that reads from a database

[Database Methods](tutorial:a-table-is-a-list-of-rows) built tables.
[Web Authoring](tutorial:a-page-is-files) built pages. Neither one
reached into the other. A real website does not work that way. A shop's
page shows the products actually in its database, rather than a copy of
them typed into the page by hand. This page joins the two for the first
time.

## The table

This is the same small table a shop's own page will read from.

```sql exec
id: full-stack-seed-products
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

Run it. Nothing on the page shows this table yet. The next cell is what
will show it.

## A page that draws its own rows

A full-stack cell has three panes, the same three a site editor has, and
a Run button beside them. What makes it different from a site editor is
what its script is allowed to reach: this one can read the table above.

```html app
id: full-stack-read-html
app: read
<table>
  <thead>
    <tr><th>Name</th><th>Price</th></tr>
  </thead>
  <tbody></tbody>
</table>
```

```css app
id: full-stack-read-css
app: read
table { width: 100%; border-collapse: collapse; }
th, td { text-align: left; padding: 0.4rem 0.6rem; border-bottom: 1px solid #ccc; }
```

```js app
id: full-stack-read-js
app: read
async function draw() {
  const rows = await dlQuery("SELECT name, price FROM products ORDER BY name");
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

Press Run. The table above fills in with five rows, the same five the
SQL cell inserted.

## Reading the code

`dlQuery` sends a query to the shared database. Every cell on this page
reads and writes that one database, so a table one cell creates is
already there for the next cell to read. What comes back is a *result
set*: one row for every match, and each row is a plain object whose
fields are the column names the `SELECT` asked for. That is why
`row.name` and `row.price` work directly, with no further lookup.

The loop turns each row into a table row, and adds it to the `<tbody>`
already sitting in this cell's own HTML. `root` names this cell's own
piece of the page, so `root.querySelector("tbody")` finds the table
inside this cell rather than some other table elsewhere on the page.

Change the query to `"SELECT name, price FROM products WHERE price < 10
ORDER BY name"` and press Run again. Three rows come back this time, not
five. The *query* changed. The page's own HTML did not.

## Asking the database, not just reading it

A shop's page usually lets a visitor search, rather than only look. Add
a text box, and read what a visitor types into it.

```html app
id: full-stack-search-html
app: search
<table>
  <thead>
    <tr><th>Name</th><th>Price</th></tr>
  </thead>
  <tbody></tbody>
</table>
<label for="full-stack-search-input">Search by name</label>
<input type="text" id="full-stack-search-input" placeholder="Type part of a name…">
```

```js app
id: full-stack-search-js
app: search
async function draw(filter) {
  const sql = filter
    ? "SELECT name, price FROM products WHERE name LIKE ? ORDER BY name"
    : "SELECT name, price FROM products ORDER BY name";
  const rows = await dlQuery(sql, filter ? [`%${filter}%`] : []);
  const tbody = root.querySelector("tbody");
  tbody.innerHTML = "";
  for (const row of rows) {
    const tr = document.createElement("tr");
    tr.innerHTML = `<td>${row.name}</td><td>€${row.price.toFixed(2)}</td>`;
    tbody.appendChild(tr);
  }
}

root.querySelector("#full-stack-search-input").addEventListener("input", (event) => draw(event.target.value));
draw();
```

Run it, then type "bag" into the box. One row comes back.

The `?` in the query is a *placeholder*. `dlQuery`'s second argument
fills it in, rather than the typed text being pasted straight into the
query's own text. That difference is worth keeping: a visitor's own text
might contain a quote mark, and text pasted straight into a query can
change what the query does, not only what it matches. A placeholder
always holds its place as one plain value, whatever it is spelled, and
never becomes part of the query itself.

## Your turn

Add a second box, this time for a highest price. Its query needs two
placeholders, one for the name and one for the price, and `dlQuery`'s
second argument becomes a two-item list, `[name, maxPrice]`, in the same
order as the two `?`s in the query.

## What you have now

- **Full stack** is a page whose own HTML shows a database's real rows,
  rather than a copy of them typed in by hand.
- A **query** is the request a page's own script sends to a database. A
  full-stack page usually builds a fresh one each time something on the
  page changes, rather than writing one query for good.
- A **result set** is what a query hands back: one row for every match,
  ready to become part of the page the way this page's loop does.
- A **placeholder** is a `?` inside a query, filled in by a value passed
  separately rather than pasted into the query's own text.
