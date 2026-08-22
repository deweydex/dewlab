/* Builds assets/vendor/ from the pinned packages in package.json.
 *
 * The output is committed to the repo. That is deliberate: GitHub Actions runs
 * build.py and nothing else, and an author previewing a tutorial locally
 * shouldn't need a Node toolchain either. Re-run `npm run build` only when a
 * pin here changes.
 */
import { build } from "esbuild";
import { cp, mkdir, readdir, rm } from "node:fs/promises";
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

const katex = join(here, "node_modules", "katex", "dist");
await cp(join(katex, "katex.min.css"), join(outDir, "katex.min.css"));

/* woff2 only. Every browser dewlab targets supports it, and carrying the ttf
 * and woff fallbacks as well would quadruple this directory for nothing. */
const fonts = await readdir(join(katex, "fonts"));
for (const file of fonts.filter((f) => f.endsWith(".woff2"))) {
  await cp(join(katex, "fonts", file), join(outDir, "fonts", file));
}

console.log(`vendor/ rebuilt: codemirror.bundle.js, katex.bundle.js, standalone.bundle.js, katex.min.css, ${
  fonts.filter((f) => f.endsWith(".woff2")).length} fonts`);
