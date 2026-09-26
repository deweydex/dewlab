# Video library

Videos on YouTube (and Nebula) that could sit beside a dewlab page: a
companion to a tutorial, a build a project page could borrow, or background
for whoever is writing the next tutorial. Nothing here is on the site yet.
It is a list to reach for when writing, and to browse for ideas.

Snapshot taken 26 September 2026 from a list of 119 channels. View counts
and titles are as they stood that day.

## The three files

| File | Rows | What it is |
|---|---|---|
| `picks.csv` | 895 | Videos chosen by hand, each with a priority, topics and the dewlab tutorials it would sit beside. Start here. |
| `channels.csv` | 119 | Every channel on the source list, ranked by how much it has for dewlab, with a reason. |
| `all-videos.csv` | 8,625 | Every long-form video on the 58 channels that were reviewed, picked or not, for searching by keyword. |

All three open in any spreadsheet. Turn on a filter row and filter by column.

## Reading `picks.csv`

**`priority`**

- **A**: link it. It sits right beside an existing tutorial, and its length
  and level suit a learner who has just read that page. 244 videos.
- **B**: worth linking from a practice page or a project brief, or as a
  second video for a keen reader. 382 videos.
- **C**: for authors rather than learners. Advanced, long, or tangential;
  good for ideas, rarely a link. 269 videos.

**`use`**: `companion` (explains what a tutorial teaches), `build seed` (a
simulation, game or algorithm someone could build in a cell or a project),
`background` (no tutorial yet).

**`dewlab_tutorials`**: the tutorial folders it fits, separated by `;`.
Filter this column by a slug (`counting-darts`, `where-chains-lead`) to see
everything that would go on that page. `project-ideas` marks a build worth
offering as a project.

**`topics`**: a fixed list of 38 topics (sorting, probability, 3D graphics,
Markov chains, compression and error correction, and so on).

**`note`**: one line on why the video is here, written for us, not for a
reader.

**`nebula_url`**: filled in where the same video is on Nebula (90 of them).
Twenty of the 119 channels are on Nebula; `channels.csv` links each one.

## Reading `channels.csv`

- **1 core** (26): reviewed video by video, and a large share of what they
  make fits dewlab.
- **2 selective** (32): reviewed video by video; a few fit, most do not.
- **3 not yet reviewed** (23): might hold a video or two for a particular
  page, but their catalogues were not read.
- **4 out of scope** (38): food, music, cities, climate, politics, animals
  and the like.

## How the picks were made, and what that misses

Each reviewed channel's full list of titles was read, and picks were made
from titles and what is known of each creator's work. The videos were not
watched. Before linking one from a page, watch it: check that it says what
the note says, that its level suits the page, and that nothing in it would
jar in a classroom.

CrashCourse was reviewed only for its Computer Science, Statistics, AI and
Navigating Digital Information series. Patrick J has over two thousand
worked examples; about thirty are picked, and `all-videos.csv` is the way
to find a specific technique.

The `auto_topics` column in `all-videos.csv` is a keyword guess from the
title and is noisy. It helps to narrow a search, but it is no judgement.

## Linking a video from a page

A tutorial's `## Where to Read More` section is where outside material
goes, cited the same way as a book or a blog post: creator, year, title in
italics, the link, then a sentence or two on what the reader will get from
it. Anything a student will read follows
[`../PEDAGOGICAL_STYLE_GUIDE.md`](../PEDAGOGICAL_STYLE_GUIDE.md), so the
`note` column is a starting point for that sentence, never the sentence.

## Keeping it current

Add a video by adding a row to `picks.csv` by hand. To refresh a channel's
full list for `all-videos.csv`, [yt-dlp](https://github.com/yt-dlp/yt-dlp)
prints every video on a channel without downloading any:

```bash
yt-dlp --flat-playlist --print "%(id)s	%(title)s	%(duration)s" \
  "https://www.youtube.com/@SebastianLague/videos"
```
