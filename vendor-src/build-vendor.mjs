/* Builds assets/vendor/ from the pinned packages in package.json.
 *
 * The output is committed to the repo. That is deliberate: GitHub Actions runs
 * build.py and nothing else, and an author previewing a tutorial locally
 * shouldn't need a Node toolchain either. Re-run `npm run build` only when a
 * pin here changes.
 */
import { build } from "esbuild";
import { cp, mkdir, readdir, readFile, rm, writeFile } from "node:fs/promises";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = join(here, "..", "assets", "vendor");

await rm(outDir, { recursive: true, force: true });
await mkdir(join(outDir, "fonts"), { recursive: true });

await build({
  entryPoints: [join(here, "codemirror-entry.js")],
  outfile: join(outDir, "codemirror.bundle.js"),
  bundle: true,
  format: "esm",
  minify: true,
  sourcemap: false,
  target: ["es2020"],
  legalComments: "none",
});

/* KaTeX: the stylesheet every built page links, plus a bundle of the renderer
 * itself, which the runtime imports only on pages that contain maths.
 * Student-side rendering was settled as acceptable (DECISIONS_LOG 1.8), and doing it
 * here rather than from build.py keeps the property this whole directory exists
 * for: neither CI nor an author previewing locally needs Node. */
await build({
  entryPoints: [join(here, "katex-entry.js")],
  outfile: join(outDir, "katex.bundle.js"),
  bundle: true,
  format: "esm",
  minify: true,
  sourcemap: false,
  target: ["es2020"],
  legalComments: "none",
});

/* The whole runtime, rebuilt as one classic script for the standalone export.
 * A page opened from a file cannot load an ES module, so the hosted page's
 * module build is useless there; this is the same source, bundled differently.
 *
 * Committed like the rest of this directory so build.py needs no Node — but
 * unlike the others it depends on assets/tutorial-runtime.js rather than on a
 * pin, so it goes stale when the runtime changes. CI rebuilds it and fails if
 * the committed copy differs, which is what stops that going unnoticed. */
await build({
  entryPoints: [join(here, "..", "assets", "tutorial-runtime.js")],
  outfile: join(outDir, "standalone.bundle.js"),
  bundle: true,
  format: "iife",
  minify: true,
  sourcemap: false,
  target: ["es2020"],
  legalComments: "none",
});

/* Milkdown's Crepe preset, for the authoring editor's prose surface
 * (assets/editor.js). Only the structural stylesheet is imported in
 * milkdown-entry.js, not Crepe's themed skin — esbuild writes whatever CSS a
 * bundled entry point imports to a sibling file automatically, here
 * milkdown.bundle.css, which editor.html links same as katex.min.css. */
await build({
  entryPoints: [join(here, "milkdown-entry.js")],
  outfile: join(outDir, "milkdown.bundle.js"),
  bundle: true,
  format: "esm",
  minify: true,
  sourcemap: false,
  target: ["es2020"],
  legalComments: "none",
  /* Crepe's own structural CSS carries its math support's KaTeX font files.
   * `file` rather than `dataurl`: those fonts are the same ones already
   * vendored above for the reading pages, and inlining a second base64 copy
   * of each into this CSS file (three formats a piece) would have made it
   * over a megabyte for no reason — real font files, written out and cached
   * by the browser like any other asset, cost nothing until an author's
   * cell actually contains maths. */
  loader: { ".woff2": "file", ".woff": "empty", ".ttf": "empty", ".svg": "file" },
  assetNames: "milkdown-fonts/[name]",
});

/* The `empty` loader above leaves each stubbed woff/truetype alternative as a
 * bare, argument-less `url()` in the generated @font-face rules — every
 * browser dewlab targets supports woff2, so nothing is lost by dropping them,
 * but an empty `url()` is invalid CSS and risks the whole `src` declaration
 * being discarded rather than just that one alternative. Removed here rather
 * than trusted to parse leniently everywhere. */
{
  const cssPath = join(outDir, "milkdown.bundle.css");
  const css = await readFile(cssPath, "utf8");
  const cleaned = css.replace(/,url\(\)\s*format\("(?:woff|truetype)"\)/g, "");
  if (cleaned !== css) await writeFile(cssPath, cleaned);
}

/* Unmodified, not bundled: it has no imports, and esbuild's minifier is not
 * worth running on a 4 KB script that needs to stay readable enough for
 * `Service-Worker-Allowed`-less debugging (OPEN_QUESTIONS.md, "the Web
 * Worker migration"). build.py additionally copies this one file to the
 * site root rather than assets/ -- a service worker's scope is the
 * directory it is served from, and assets/ would be too narrow to cover
 * every tutorial the reload needs to reach. */
await cp(
  join(here, "node_modules", "coi-serviceworker", "coi-serviceworker.js"),
  join(outDir, "coi-serviceworker.js")
);

const katex = join(here, "node_modules", "katex", "dist");
await cp(join(katex, "katex.min.css"), join(outDir, "katex.min.css"));

/* woff2 only. Every browser dewlab targets supports it, and carrying the ttf
 * and woff fallbacks as well would quadruple this directory for nothing. */
const fonts = await readdir(join(katex, "fonts"));
for (const file of fonts.filter((f) => f.endsWith(".woff2"))) {
  await cp(join(katex, "fonts", file), join(outDir, "fonts", file));
}

/* Two accessible reading fonts (planning/DEWMINI_WORKBENCH.md's texture
 * settings; DECISIONS_LOG.md 7.123): Atkinson Hyperlegible (Braille
 * Institute of America) and OpenDyslexic, both SIL OFL 1.1. Self-hosted
 * from the @fontsource packages — matching every other vendored asset
 * here rather than a Google Fonts CDN `<link>`, which this repository's
 * own offline bundle (write_dewmini_bundle(), DECISIONS_LOG.md 7.92)
 * could never reach anyway. Regular and bold, roman and italic — four
 * faces per font, the minimum for a page's own bold/italic markdown to
 * render as a real face rather than a synthetic one.
 *
 * @fontsource ships one CSS file and one woff2 per face; concatenated
 * into a single accessible-fonts.css here rather than linked separately,
 * so a page adds one stylesheet regardless of how many of these faces it
 * ends up using.
 *
 * The woff2 files land directly in fonts/, flat, beside KaTeX's own —
 * not fonts/accessible/ — so build.py's standalone_html() can find them
 * with the exact same FONT_URL_RE it already uses to inline KaTeX's own
 * fonts into a downloaded single-file tutorial page, rather than needing
 * a second copy of that regex and inlining step. Collision with a KaTeX
 * file name is not a real risk: the two projects share no naming
 * convention at all. */
const ACCESSIBLE_FONTS = [
  { pkg: "@fontsource/atkinson-hyperlegible", slug: "atkinson-hyperlegible" },
  { pkg: "@fontsource/opendyslexic", slug: "opendyslexic" },
];
const FACES = ["latin-400", "latin-400-italic", "latin-700", "latin-700-italic"];

let accessibleCss = "";
for (const { pkg, slug } of ACCESSIBLE_FONTS) {
  const pkgDir = join(here, "node_modules", pkg);
  for (const face of FACES) {
    // The package's own file names are "<slug>-<face>-normal.woff2" for a
    // roman face ("latin-400" -> "...-latin-400-normal.woff2") and
    // "<slug>-<face>.woff2" for an italic one, since "face" already ends
    // "-italic" there — two different suffix rules, not a typo.
    const isItalic = face.endsWith("-italic");
    const srcFile = isItalic ? `${slug}-${face}.woff2` : `${slug}-${face}-normal.woff2`;
    const outFile = `${slug}-${face}.woff2`;
    await cp(join(pkgDir, "files", srcFile), join(outDir, "fonts", outFile));

    const css = await readFile(join(pkgDir, `${face}.css`), "utf8");
    // Only woff2 (every browser dewlab targets supports it, the same call
    // katex's own fonts above already made), and pointed at where this
    // copies the file to rather than the package's own relative path.
    accessibleCss += css
      .replace(/src: url\([^)]+\) format\('woff2'\),\s*url\([^)]*\) format\('woff'\);/,
                `src: url('fonts/${outFile}') format('woff2');`)
      + "\n";
  }
}
await writeFile(join(outDir, "accessible-fonts.css"), accessibleCss);

console.log(`vendor/ rebuilt: codemirror.bundle.js, katex.bundle.js, standalone.bundle.js, ` +
  `milkdown.bundle.js, milkdown.bundle.css, katex.min.css, coi-serviceworker.js, ${
  fonts.filter((f) => f.endsWith(".woff2")).length} fonts, accessible-fonts.css (${
  ACCESSIBLE_FONTS.length * FACES.length} faces)`);
