"""Draw an entity relationship diagram, in crow's foot notation.

Takes a schema — either a live `sqlite3` connection or the same shape
written out by hand — and returns an SVG string.

Layout is ours rather than a library's, for one reason: this has to run in
Pyodide as well as here, so a student's own `CREATE TABLE` statements can be
drawn back to them, and Pyodide has no `dot` binary and no `subprocess` to
call one with. The arithmetic below is a few dozen lines, which is the same
trade `dev/draw_topic_graph.py` already made for the contents-page map.

Tables sit in columns by how far they are from one that points at nothing,
so an arrow always runs left to right and a reader can follow "this names a
row over there" in one direction. Edges are routed through the gutter
between two columns, never across a column, because a line crossing a box
reads as though it connects to it. Inside a column, tables are stacked in
whichever order leaves the fewest lines crossing one another (`_arrange`),
since a crossing is where a reader loses track of which line is which.
"""

from __future__ import annotations

import svgwrite

from palette import INK, MONO, MUTED, PANEL, RULE, SANS

HEADER_H = 26           # the band carrying a table's name
ROW_H = 21              # one column of that table
PAD = 10                # inside a box, left and right
GAP_Y = 26              # between two boxes in the same column
GUTTER = 92             # between two columns, where edges are routed
LANE = 11               # between two edges sharing a gutter
NAME_PT, ROW_PT = 12.5, 10.5


def schema_from(connection) -> dict:
    """Read a live database's own account of itself.

    `PRAGMA foreign_key_list` reports only what a `CREATE TABLE` actually
    declared, and reports it whether or not enforcement is switched on. A
    column called `product_id` that never said `REFERENCES
    product_tbl(product_id)` is an ordinary integer as far as this is
    concerned, and draws no arrow — which is the honest picture of what the
    schema says.
    """
    schema = {}
    for (name,) in connection.execute(
        "SELECT name FROM sqlite_master WHERE type='table' "
        "AND name NOT LIKE 'sqlite_%' ORDER BY name"
    ):
        references = {
            row[3]: (row[2], row[4])
            for row in connection.execute(f"PRAGMA foreign_key_list({name})")
        }
        schema[name] = {
            "columns": [
                {
                    "name": column[1],
                    "type": (column[2] or "").lower(),
                    "primary": bool(column[5]),
                    "references": references.get(column[1]),
                }
                for column in connection.execute(f"PRAGMA table_info({name})")
            ]
        }
    return schema


def _text_width(text: str, point_size: float) -> float:
    """Roughly how wide a string will be.

    Nothing here can measure a glyph, so this is an estimate, deliberately
    generous: a box slightly too wide looks considered, and one too narrow
    has its own text hanging out of it.
    """
    return len(text) * point_size * 0.62


def _depth(schema: dict) -> dict:
    """How many hops each table is from one that points at nothing."""
    depth = dict.fromkeys(schema, 0)
    for _ in range(len(schema)):
        settled = True
        for name, table in schema.items():
            parents = [
                column["references"][0]
                for column in table["columns"]
                if column["references"] and column["references"][0] in schema
            ]
            furthest = max((depth[parent] + 1 for parent in parents), default=0)
            if furthest > depth[name]:
                depth[name], settled = furthest, False
        if settled:
            break
    return depth


def _columns(schema: dict) -> dict[int, list[str]]:
    """Which tables share a column, alphabetically within it."""
    depth = _depth(schema)
    columns: dict[int, list[str]] = {}
    for name in sorted(schema, key=lambda n: (depth[n], n)):
        columns.setdefault(depth[name], []).append(name)
    return columns


def _layout(schema: dict, columns: dict[int, list[str]] | None = None) -> dict:
    """Place every table, and say how big the drawing came out.

    `columns` fixes the top-to-bottom order inside each column; left out,
    it is alphabetical, and `_arrange` is what chooses a better one.
    """
    if columns is None:
        columns = _columns(schema)

    boxes, x = {}, 0.0
    for column in sorted(columns):
        names = columns[column]
        width = max(
            _text_width(name, NAME_PT) + PAD * 2
            for name in names
        )
        for name in names:
            for c in schema[name]["columns"]:
                label = (f"{c['name']}   {c['type']}   "
                         f"{'PK' if c['primary'] else ''}{' FK' if c['references'] else ''}")
                width = max(width, _text_width(label, ROW_PT) + PAD * 2)
        heights = {
            name: HEADER_H + ROW_H * len(schema[name]["columns"]) for name in names
        }
        y = 0.0
        for name in names:
            boxes[name] = {"x": x, "y": y, "w": width, "h": heights[name],
                           "column": column}
            y += heights[name] + GAP_Y
        x += width + GUTTER

    tallest = max(box["y"] + box["h"] for box in boxes.values())
    for box in boxes.values():                      # centre each column vertically
        column_bottom = max(
            other["y"] + other["h"] for other in boxes.values() if other["x"] == box["x"]
        )
        box["y"] += (tallest - column_bottom) / 2
    return {"boxes": boxes, "width": x - GUTTER, "height": tallest}


def _row_centre(placed: dict, table: dict, index: int) -> float:
    return placed["y"] + HEADER_H + ROW_H * (index + 0.5)


def _crows_foot(drawing, group, x: float, y: float, facing: int, size: float = 9.0) -> None:
    """The many end: three toes spreading out where the line meets the box.

    Orientation is the whole notation here. The three lines converge at a
    point out along the line and spread apart as they reach the entity, so
    the shape opens towards the many side. Converged at the box instead, it
    reads as an arrowhead — "points at" rather than "many of these".
    """
    apex = (x + facing * size * 1.6, y)
    for offset in (-size * 0.85, 0, size * 0.85):
        group.add(drawing.line(
            start=apex, end=(x, y + offset),
            stroke=INK, stroke_width=1.6, stroke_linecap="round"))


def _single_bar(drawing, group, x: float, y: float, size: float = 7.0) -> None:
    """The one end: one bar across the line, matching the foot's weight
    so the two ends read as a pair rather than as mark and accident."""
    group.add(drawing.line(
        start=(x, y - size), end=(x, y + size),
        stroke=INK, stroke_width=2.0, stroke_linecap="round"))


def _edges(schema: dict, boxes: dict) -> list[dict]:
    """Every foreign key as a pair of points: the parent's key row, where
    the line leaves, and the child's foreign-key row, where it arrives."""
    edges = []
    for name, table in schema.items():
        for index, column in enumerate(table["columns"]):
            if not column["references"]:
                continue
            parent = column["references"][0]
            if parent not in boxes or parent == name:
                continue
            child_box, parent_box = boxes[name], boxes[parent]
            # The line leaves the parent's own key column, not its name band:
            # a foreign key names a row through a column, and a line from the
            # header would say the relationship belongs to the whole table.
            parent_columns = schema[parent]["columns"]
            target = column["references"][1]
            parent_index = next(
                (i for i, c in enumerate(parent_columns) if c["name"] == target), 0)
            edges.append({
                "key": (name, column["name"]),
                "parent_box": parent_box, "child_box": child_box,
                "start": (parent_box["x"] + parent_box["w"],
                          _row_centre(parent_box, schema[parent], parent_index)),
                "end": (child_box["x"], _row_centre(child_box, table, index)),
                "reach": child_box["column"] - parent_box["column"],
            })
    return edges


def _route(schema: dict, placed: dict, dropped_first: bool = True) -> list[list]:
    """The polyline for every edge, each in a lane of its own.

    Lanes are handed out by rule rather than in the order edges are met,
    because the order decides whether two lines cross. In the gutter a line
    leaves by, the one leaving highest takes the lane furthest out, so
    no line below has to cross it on the way out. A line that reaches past
    a column (below) drops under every box; the one furthest out drops
    least deep, and comes back up furthest from the table it points at,
    so the lines under the boxes nest rather than cross.
    `dropped_first` says whether those lines take the lanes nearer the
    parent or the ones beyond its neighbours'; `_arrange` tries both.
    """
    boxes = placed["boxes"]
    boxes_bottom = placed["height"]
    edges = sorted(_edges(schema, boxes), key=lambda e: e["key"])
    dropped = [e for e in edges if e["reach"] > 1]
    near = [e for e in edges if e["reach"] <= 1]

    # Highest start first: furthest out, shallowest floor, furthest back.
    dropped.sort(key=lambda e: (e["start"][1], e["key"]))
    for rank, edge in enumerate(dropped, 1):
        edge["floor"] = boxes_bottom + GAP_Y * 0.5 + LANE * rank
    for edge in dropped:
        sharing = [e for e in dropped if e["child_box"]["x"] == edge["child_box"]["x"]]
        edge["back"] = (edge["child_box"]["x"] - 14.4
                        - LANE * sum(1 for e in sharing if e["floor"] >= edge["floor"]))

    # Lanes out of each gutter, nearest the parent first.
    gutters: dict[float, list] = {}
    for edge in dropped + near:
        gutters.setdefault(edge["start"][0], []).append(edge)
    for edge_x, leaving in gutters.items():
        falling = [e for e in leaving if e["reach"] > 1]
        falling.sort(key=lambda e: (-e["start"][1], e["key"]))
        down = [e for e in leaving if e["reach"] <= 1 and e["end"][1] >= e["start"][1]]
        up = [e for e in leaving if e["reach"] <= 1 and e["end"][1] < e["start"][1]]
        down.sort(key=lambda e: (-e["start"][1], e["key"]))
        up.sort(key=lambda e: (e["start"][1], e["key"]))
        order = falling + down + up if dropped_first else down + up + falling
        # The first lane starts clear of the "one" bar drawn just outside
        # the box, so no line turns a corner on top of it.
        for lane, edge in enumerate(order, 1):
            edge["lane"] = edge_x + 7 + LANE * lane

    routes = []
    for edge in edges:
        start, end = edge["start"], edge["end"]
        meet = (end[0] - 14.4, end[1])   # where the foot's toes converge
        if edge["reach"] <= 1:
            # Neighbours: out into the gutter between them, along, and in.
            turn = edge["lane"]
            points = [start, (turn, start[1]), (turn, end[1]), meet]
        else:
            # A reach across a column has no clear gutter to turn in — the
            # straight run would cross whatever sits between. It drops
            # below every box instead, travels there, and comes back up in
            # the gutter immediately before the table it points at.
            out, floor, back = edge["lane"], edge["floor"], edge["back"]
            points = [start, (out, start[1]), (out, floor),
                      (back, floor), (back, end[1]), meet]
        routes.append(points)
    return routes


def _crossings(routes: list[list]) -> int:
    """How many times one line crosses or runs along another.

    Two lines leaving the same key row share their first stretch on
    purpose — that reads as a fork — so an overlap starting from one
    shared point is not counted.
    """
    def segments(points):
        return list(zip(points, points[1:]))

    count = 0
    for i, first in enumerate(routes):
        for second in routes[i + 1:]:
            for a, b in segments(first):
                for c, d in segments(second):
                    count += _meets(a, b, c, d)
    return count


def _meets(a, b, c, d) -> int:
    horizontal_1, horizontal_2 = a[1] == b[1], c[1] == d[1]
    if horizontal_1 != horizontal_2:
        (h1, h2), (v1, v2) = ((a, b), (c, d)) if horizontal_1 else ((c, d), (a, b))
        x, y = v1[0], h1[1]
        return int(min(h1[0], h2[0]) < x < max(h1[0], h2[0])
                   and min(v1[1], v2[1]) < y < max(v1[1], v2[1]))
    if a == c:
        return 0
    axis = 0 if horizontal_1 else 1
    if a[1 - axis] != c[1 - axis]:
        return 0
    low = max(min(a[axis], b[axis]), min(c[axis], d[axis]))
    high = min(max(a[axis], b[axis]), max(c[axis], d[axis]))
    return int(high > low)


def _arrange(schema: dict) -> tuple[dict, list[list]]:
    """The layout, and its routes, with the fewest crossing lines.

    Tries every top-to-bottom order of the tables in each column, which is
    few for the schemas a student writes: three tables in a column is six
    orders. Past a few thousand it keeps the alphabetical one. A tie keeps
    the earlier candidate, so alphabetical wins when nothing beats it.
    """
    from itertools import permutations, product
    from math import factorial, prod

    columns = _columns(schema)
    keys = sorted(columns)
    if prod(factorial(len(columns[k])) for k in keys) > 2000:
        candidates = [columns]
    else:
        candidates = [
            dict(zip(keys, (list(order) for order in orders)))
            for orders in product(*(permutations(columns[k]) for k in keys))
        ]
    best = None
    for candidate in candidates:
        placed = _layout(schema, candidate)
        for dropped_first in (True, False):
            routes = _route(schema, placed, dropped_first)
            score = _crossings(routes)
            if best is None or score < best[0]:
                best = (score, placed, routes)
    return best[1], best[2]


def render(schema: dict, title: str | None = None) -> str:
    placed, routes = _arrange(schema)
    boxes = placed["boxes"]
    # Every edge that has to drop below the boxes needs a lane of its own down
    # there, and the canvas has to be tall enough to hold them.
    dropped = sum(1 for points in routes if len(points) > 4)
    placed["height"] += (GAP_Y + LANE * dropped) if dropped else 0
    margin = 14
    drawing = svgwrite.Drawing(
        size=(f"{placed['width'] + margin * 2:.0f}px",
              f"{placed['height'] + margin * 2:.0f}px"),
        viewBox=f"0 0 {placed['width'] + margin * 2:.0f} {placed['height'] + margin * 2:.0f}",
        debug=False,   # so a `var(--dl-…)` reaches the file instead of raising
    )
    drawing.attribs["fill"] = INK      # `fill` inherits: text with none still shows
    drawing.attribs["font-family"] = SANS
    if title:
        drawing.set_desc(title=title)
    root = drawing.g(transform=f"translate({margin},{margin})")

    # Edges first, so a box always sits over a line rather than under it.
    for points in routes:
        root.add(drawing.polyline(
            points=points, fill="none", stroke=INK, stroke_width=1.6,
            stroke_linejoin="round"))
        start, end = points[0], points[-1]
        _single_bar(drawing, root, start[0] + 7, start[1])
        _crows_foot(drawing, root, end[0] + 14.4, end[1], -1)

    for name, box in boxes.items():
        root.add(drawing.rect(
            insert=(box["x"], box["y"]), size=(box["w"], HEADER_H),
            fill=PANEL, stroke="none"))
        root.add(drawing.rect(
            insert=(box["x"], box["y"]), size=(box["w"], box["h"]),
            fill="none", stroke=INK, stroke_width=1.3, rx=4))
        root.add(drawing.line(
            start=(box["x"], box["y"] + HEADER_H),
            end=(box["x"] + box["w"], box["y"] + HEADER_H),
            stroke=INK, stroke_width=1.3))
        root.add(drawing.text(
            name, insert=(box["x"] + box["w"] / 2, box["y"] + HEADER_H / 2 + 4),
            text_anchor="middle", font_size=f"{NAME_PT}px", font_weight="bold",
            fill=INK))
        for index, column in enumerate(schema[name]["columns"]):
            centre = _row_centre(box, schema[name], index) + 3.5
            if index:
                root.add(drawing.line(
                    start=(box["x"] + 1, centre - ROW_H / 2 - 3.5),
                    end=(box["x"] + box["w"] - 1, centre - ROW_H / 2 - 3.5),
                    stroke=RULE, stroke_width=0.8))
            root.add(drawing.text(
                column["name"], insert=(box["x"] + PAD, centre),
                font_size=f"{ROW_PT}px", font_family=MONO, fill=INK))
            # A column can be both, and in a junction table every column is:
            # part of the composite key, and a foreign key into one of the two
            # tables being joined. Showing only "PK" there hides the very
            # thing the picture is meant to explain.
            marks = ("PK" if column["primary"] else "") + \
                    (" FK" if column["references"] else "")
            mark = marks.strip()
            root.add(drawing.text(
                f"{column['type']} {mark}".strip(),
                insert=(box["x"] + box["w"] - PAD, centre),
                text_anchor="end", font_size=f"{ROW_PT - 0.5}px", fill=MUTED))

    drawing.add(root)
    return drawing.tostring()
