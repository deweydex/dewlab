/* Builds dewlab/assets/vendor/ from the pinned packages in package.json.
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

/* KaTeX ships the stylesheet the built pages use; the maths itself is rendered
 * at build time by build.py, so no KaTeX JavaScript reaches a student. */
const katex = join(here, "node_modules", "katex", "dist");
await cp(join(katex, "katex.min.css"), join(outDir, "katex.min.css"));

/* woff2 only. Every browser dewlab targets supports it, and carrying the ttf
 * and woff fallbacks as well would quadruple this directory for nothing. */
const fonts = await readdir(join(katex, "fonts"));
for (const file of fonts.filter((f) => f.endsWith(".woff2"))) {
  await cp(join(katex, "fonts", file), join(outDir, "fonts", file));
}

console.log(`vendor/ rebuilt: codemirror.bundle.js, katex.min.css, ${
  fonts.filter((f) => f.endsWith(".woff2")).length} fonts`);
