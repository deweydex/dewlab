# `assets/map.js`, explained

`map.js` draws the topic map and runs it. `build.py` writes the page
(`write_map_page()`): an empty frame, `<div id="dl-tmap" hidden>`; a block of
JSON, `<script id="dewlab-map">`, that holds the whole map; and, under the
frame, the same map as a nested list of links that works with no script. The
script fills the frame and un-hides it. If it fails to load, the list is
still the map.

`map.css` has the styles. Everything is under `.dl-tmap`, and colours and type
come from the site's tokens, so the reader's theme, text size, font and
contrast settings reach the map. Only the sea, the coast and the land have
colours of their own, in a light set and a dark set.

## What the data is

`build.py`'s `map_data()` makes it from `map/graph.json`, `map/layout.json` and
the tutorials. For each town it holds the name, a plain sentence, what it
needs, where it stands, and its pages (title, section, link, courses). The
script never reads a tutorial. It draws what it is given.

## The pieces, in the order `start()` meets them

**The drawing.** An SVG in a group that is moved and scaled as one: the sea,
waves, coast, the plains, each country's land, each district's county, the
terrain pattern of mountains and forest, bridges, roads, then routes. Strokes
use `vector-effect: non-scaling-stroke`, so lines stay as thick as they are
drawn however far you zoom.

**Towns and names are HTML buttons laid over the SVG**, so they stay one size
at any zoom, can be focused, and have real names for a screen reader.

**Bridges.** A road between two continents is drawn through the ends of the
bridge between them (`via()`), so roads gather at a bridge as they do on a map.
Two continents with no bridge of their own go by way of the starting island. A
bridge is as wide as the roads it carries.

**Levels.** `lodFor()` turns the zoom into one of five levels: continents,
countries, districts, towns, streets. The levels are multiples of the scale
that shows the whole map (`baseK`), so the first view is continent names alone
whatever the size of the frame.

**Names.** A name is as wide on screen as its type makes it, so where it goes
depends on the screen. `placeNames()` gives each name places to choose from (a
continent's are round its coast, a country's are well inside its land, both from
`layout.json`) and takes the one that covers the fewest towns, bridges, other
names and controls, inside the view. It keeps the choice while the zoom stays
about the same (`placeAll()`), so names do not jump about as the map is moved.
At the country level, towns under a name are left out (`is-under-name`).

**Town names** go down most important first, and any that would collide with one
already down stay hidden (`render()`).

**Pointer.** Drag, pinch and wheel. The pointer is captured only once a press
becomes a drag. Capturing on the press sends the click to the stage, and a town
never gets it.

**The panel.** `select()` opens a town and `showTown()` fills it: its pages as
streets, what it needs, what it leads to, landmarks that use it. "How do I get
here?" (`showDirections()`) lists every town it needs, nearest the start first,
and draws that route. "I have been here" is kept in this browser
(`dewlab:map:visited`). It is the reader's own mark, not a record of work.

**The docks.** The page's corner docks and its feedback button stay put as the
page scrolls, so they pass over the frame. `avoidDocks()` slides the map's own
controls out from under them, and places the names again once scrolling stops.

## Changing it

The page's levels, names and bridges are checked in a browser by
`tests/e2e/test_map.py`, over the small map in `tests/e2e/fixture/map/`. The
build side is `tests/build/test_map.py`. Nothing here is bundled with
`tutorial-runtime.js`, so changing it needs no vendor rebuild.
