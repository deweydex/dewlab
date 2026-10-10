# The in-page editor spike: the measuring scripts

Throwaway tools behind `planning/IN_PAGE_EDITOR_SPIKE.md`. They are kept so the
numbers there can be checked again, not because anything depends on them. They
need `pip install playwright pillow` and a Chromium (`CHROMIUM=/path/to/chrome`
if Playwright cannot find one).

- `crepe_roundtrip.py N PER OUT.json` pushes up to PER prose blocks from each of
  N tutorials through the vendored Crepe editor unchanged, with maths protected
  and Crepe's list and table output tidied the way the editor would. `N=498
  PER=100000` is the whole corpus (about four minutes).
- `crepe_classify.py OUT.json` says, for each block that came back different,
  whether the finished page would differ (it renders both through `build.py`'s
  own markdown steps).
- `swap_blocks.py inplace.css PAGES THEMES` builds nothing itself. It opens
  pages from `site/` (build with `python3 build.py --source-map`), swaps one
  block at a time for an editor, and measures how far anything else on the page
  moves and how many pixels change. `inplace-entry.js` is the editor it loads:
  Crepe with the features that draw their own furniture switched off. Bundle it
  with esbuild (from `vendor-src/node_modules`) to
  `site/assets/vendor/spike.bundle.js` first. `inplace.css` is the whole of the
  styling it needs.

Set `SPIKE_OUT` to say where results are written (default `/tmp/editor-spike`).
