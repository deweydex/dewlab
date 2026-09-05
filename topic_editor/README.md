# The topic editor

A page for drawing the topic graph by hand: which topic a student needs
before which, what helps, what is applied where, and what goes both ways.
One self-contained file, no build step, no server. Open `index.html` in a
browser, or reach it on the site at `/topic_editor/`. Nothing on the site
links to it: it is a tool for whoever is drawing the graph, not a page a
student would open.

`help.html` is the guide, and ships beside it. The Help button opens it.

## Where the graph comes from and goes to

The page carries the graph as a JSON blob, written by
`dev/build_topic_editor.py` from the same sources the map is drawn from:
`topics.yaml`, the judgements and decisions under `review/`, and the wall in
`strands.yaml`. CI runs `--check` so the copy cannot drift.

The editor never writes a file. Export gives `topic-graph-edits.json`, and

    python3 dev/apply_topic_edits.py topic-graph-edits.json

writes it into `topics.yaml`, `strands.yaml` and `topic-positions.json`.
After that `topics.yaml` carries `authored: true`, and `draw_topic_graph.py`
reads the graph from the YAML rather than from the judgements, which stay as
the record of how it got there.

## The five kinds of link

| In the editor | In `topics.yaml` | Direction |
|---|---|---|
| requires | `needs`, on the topic that needs the other | one way, decides the order |
| helps | `helps`, on the topic that helps | one way |
| applied in | `applied_in`, on the tool | one way |
| interdependent | `interdependent`, on both | none |
| involves | `involves`, on both | none |

Only `requires` decides the rows on the map. A `requires` link that would
make a loop is refused in the editor and turned into `helps`.

## Layout

Nothing is imposed. Topics repel, links pull, and a one-way link leans its
far end lower, so an order emerges as it is drawn. Positions are the
author's once dragged, and go into the export under `pos`. *Build out from
here* is the other mode: one topic pinned at the centre and every unlinked
topic in hexagonal rings around it, a tap bringing one in.

The README is for a reader of the repository and is not copied to the
site; `help.html` is.
