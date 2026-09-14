#!/usr/bin/env python3
"""Step 1 of refactor/PLAN.md: move placement out of the tutorials and into
courses/.

    python3 refactor/migrate_tutorials.py                # dry run: report only
    python3 refactor/migrate_tutorials.py --apply        # write, git mv, delete
    python3 refactor/migrate_tutorials.py --rename computational-methods/first-steps=first-steps-cm

Reads `tutorials/<module>/<slug>/*.md`, every `*.order.yaml`, each module's
`series.yaml`, `tutorials/modules.yaml`, `MODULE_INFO` in build.py, and the
card fences in `pages/home.md`. Refuses to apply while an id collides across
modules without a `--rename`. Idempotent in the sense that a second run on a
migrated tree reports nothing to do.

What it writes with --apply:

- every tutorial, practice and release file: frontmatter minus `module`,
  `module_title`, `series`, `slug` (line removal; nothing else in the file
  is touched);
- `tutorials/<id>/` for every tutorial (git mv from `tutorials/<module>/<slug>/`,
  files inside a renamed folder renamed to match);
- `courses/<module>.yaml`, `courses/index.yaml`, `courses/redirects.yaml`;
- `tutorial:` links that named a renamed slug, inside the renamed module;
- removes the module folders' order files, `series.yaml`, `modules.yaml`.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
TUTORIALS = ROOT / "tutorials"
COURSES = ROOT / "courses"
ORDER_SUFFIX = ".order.yaml"
PLACEMENT_FIELDS = ("module", "module_title", "series", "slug")


def fail(message: str) -> None:
    print(f"error: {message}", file=sys.stderr)
    sys.exit(1)


def split_frontmatter(text: str) -> tuple[str, str]:
    if not text.startswith("---\n"):
        return "", text
    end = text.find("\n---\n", 4)
    if end == -1:
        return "", text
    return text[4:end], text[end + 5:]


def field(front: str, key: str) -> str | None:
    match = re.search(rf"^{key}:\s*(.*?)\s*$", front, re.M)
    if not match:
        return None
    value = match.group(1)
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        value = value[1:-1]
    return value


def strip_placement(front: str) -> str:
    """Remove the four top-level placement lines. A top-level key is one at
    column 0; nested `covers:` entries are indented and untouched."""
    kept = []
    for line in front.split("\n"):
        key = line.split(":", 1)[0] if not line.startswith((" ", "\t")) else None
        if key in PLACEMENT_FIELDS:
            continue
        kept.append(line)
    return "\n".join(kept)


class Found:
    def __init__(self) -> None:
        self.tutorials: dict[tuple[str, str], Path] = {}     # (module, slug) -> folder
        self.files: dict[tuple[str, str], list[Path]] = defaultdict(list)
        self.practice_for: dict[tuple[str, str], str] = {}
        self.mixed: dict[str, list[str]] = defaultdict(list)  # module -> mixed slugs
        self.orders: dict[tuple[str, str], tuple[str, list[str]]] = {}  # (module, series) -> (title, slugs)
        self.chains: dict[str, list[str]] = {}
        self.modules: list[str] = []


def scan() -> Found:
    found = Found()
    if not TUTORIALS.is_dir():
        fail("no tutorials/ folder")
    modules_file = TUTORIALS / "modules.yaml"
    if modules_file.is_file():
        found.modules = (yaml.safe_load(modules_file.read_text()) or {}).get("order") or []
    for module_dir in sorted(p for p in TUTORIALS.iterdir() if p.is_dir()):
        module = module_dir.name
        chain = module_dir / "series.yaml"
        if chain.is_file():
            found.chains[module] = (yaml.safe_load(chain.read_text()) or {}).get("order") or []
        for order in sorted(module_dir.glob(f"*{ORDER_SUFFIX}")):
            data = yaml.safe_load(order.read_text()) or {}
            found.orders[(module, order.name[: -len(ORDER_SUFFIX)])] = (
                str(data.get("series") or order.name[: -len(ORDER_SUFFIX)]),
                [str(s) for s in data.get("order") or []],
            )
        for folder in sorted(p for p in module_dir.iterdir() if p.is_dir()):
            mds = sorted(folder.glob("*.md"))
            if not mds:
                continue
            slug = folder.name
            found.tutorials[(module, slug)] = folder
            for md in mds:
                front, _ = split_frontmatter(md.read_text())
                found.files[(module, slug)].append(md)
                own_slug = field(front, "slug") or ""
                pf = field(front, "practice_for")
                if pf:
                    found.practice_for[(module, own_slug)] = pf
                if re.search(r"^practice_across:", front, re.M) and own_slug and own_slug == slug:
                    found.mixed[module].append(own_slug)
    return found


def collisions(found: Found) -> dict[str, list[str]]:
    by_slug: dict[str, list[str]] = defaultdict(list)
    for module, slug in found.tutorials:
        by_slug[slug].append(module)
    return {slug: mods for slug, mods in by_slug.items() if len(mods) > 1}


def home_cards() -> dict[str, dict[str, str]]:
    """Per module, the `card:` text and the `meta:` code line from the
    ```card fences in pages/home.md — the code because two modules
    (database-methods, web-authoring) have no MODULE_INFO entry today and
    the home card is the only place their QQI code is written."""
    home = ROOT / "pages" / "home.md"
    if not home.is_file():
        return {}
    cards: dict[str, dict[str, str]] = {}
    for match in re.finditer(r"```card\n(.*?)```", home.read_text(), re.S):
        body = match.group(1)
        url = re.search(r"^url:\s*(\S+)", body, re.M)
        if not url or not url.group(1).endswith(".html"):
            continue
        module = url.group(1)[: -len(".html")]
        meta = re.search(r"^meta:\s*(.+?)\s*$", body, re.M)
        lines = [ln for ln in body.split("\n") if not re.match(r"^(url|status|meta|wide):", ln)]
        lines = [ln for ln in lines if not ln.startswith("#")]
        text = " ".join(ln.strip() for ln in lines if ln.strip())
        cards[module] = {"card": text, "code": meta.group(1) if meta else ""}
    return cards


def module_info() -> dict[str, dict]:
    sys.path.insert(0, str(ROOT))
    try:
        import build  # noqa: WPS433 — the dictionary lives there today
        return dict(build.MODULE_INFO)
    except Exception as err:  # pragma: no cover — reported, not fatal
        print(f"note: could not import build.MODULE_INFO ({err}); courses get no code/description")
        return {}


def module_title_of(found: Found, module: str, info: dict) -> str:
    for (m, slug), files in found.files.items():
        if m != module:
            continue
        for md in files:
            front, _ = split_frontmatter(md.read_text())
            title = field(front, "module_title")
            if title:
                return title
    return str(info.get(module, {}).get("title") or module)


def plan(found: Found, renames: dict[str, str]) -> dict:
    """Everything --apply would do, as data, so the dry run can print it."""
    info = module_info()
    cards = home_cards()
    new_id: dict[tuple[str, str], str] = {}
    for module, slug in found.tutorials:
        new_id[(module, slug)] = renames.get(f"{module}/{slug}", slug)

    courses: dict[str, dict] = {}
    for module in sorted({m for m, _ in found.tutorials} | {m for m, _ in found.orders}):
        entry = info.get(module, {})
        chain = found.chains.get(module, [])
        series_keys = [s for s in chain if (module, s) in found.orders]
        series_keys += sorted(s for (m, s) in found.orders if m == module and s not in series_keys)
        contents = []
        for s in series_keys:
            title, slugs = found.orders[(module, s)]
            ids = []
            for entry_slug in slugs:
                if "/" in entry_slug:  # the borrowed form from #234
                    owner, borrowed = entry_slug.split("/", 1)
                    ids.append(new_id.get((owner, borrowed), borrowed))
                else:
                    ids.append(new_id.get((module, entry_slug), entry_slug))
            contents.append({"title": title, "tutorials": ids})
        course = {
            "title": module_title_of(found, module, info),
            "code": entry.get("code") or cards.get(module, {}).get("code") or None,
            "status": "beta",
            "card": cards.get(module, {}).get("card") or None,
            "description": "\n\n".join(entry.get("description", [])) or None,
            "contents": contents,
        }
        mixed = [new_id.get((module, s), s) for s in found.mixed.get(module, [])]
        if mixed:
            course["mixed"] = mixed
        courses[module] = {k: v for k, v in course.items() if v is not None}

    redirects: list[tuple[str, str]] = []
    for (module, slug), folder in found.tutorials.items():
        ident = new_id[(module, slug)]
        redirects.append((f"tutorials/{module}/{slug}.html", f"tutorials/{ident}.html"))
        for md in found.files[(module, slug)]:
            front, _ = split_frontmatter(md.read_text())
            own = field(front, "slug") or ""
            if md.name.startswith("v") and md.name != f"{slug}.md":
                version = md.name[1:-3]
                redirects.append((f"tutorials/{module}/{slug}/v{version}.html",
                                  f"tutorials/{ident}/v{version}.html"))
            elif own and own != slug:  # a practice page beside its tutorial
                new_own = own if ident == slug else own.replace(slug, ident, 1)
                redirects.append((f"tutorials/{module}/{own}.html", f"tutorials/{new_own}.html"))
    for module in courses:
        redirects.append((f"{module}.html", f"courses/{module}.html"))

    order = [m for m in found.modules if m in courses] + sorted(set(courses) - set(found.modules))
    return {"new_id": new_id, "courses": courses, "redirects": redirects, "order": order}


def apply(found: Found, planned: dict) -> None:
    def git(*args: str) -> None:
        subprocess.run(["git", *args], check=True, cwd=ROOT)

    COURSES.mkdir(exist_ok=True)
    # 1. frontmatter and links, in place, before moving anything.
    for (module, slug), files in found.files.items():
        ident = planned["new_id"][(module, slug)]
        for md in files:
            text = md.read_text()
            front, body = split_frontmatter(text)
            if front:
                text = "---\n" + strip_placement(front) + "\n---\n" + body
            # Anything in this module that named a renamed slug: tutorial:
            # links in the body, and practice_for / practice_across in the
            # frontmatter (a renamed tutorial's own practice page, or a mixed
            # set in the same module that draws on it). Without this the
            # practice page of the renamed tutorial points at the *other*
            # tutorial of that name — found by check.py on the first dry run.
            for (m, s), new in planned["new_id"].items():
                if m == module and new != s:
                    text = re.sub(rf"\(tutorial:{re.escape(s)}([)#])", rf"(tutorial:{new}\1", text)
                    text = re.sub(rf"^(practice_for:\s*){re.escape(s)}\s*$", rf"\g<1>{new}", text, flags=re.M)
                    text = re.sub(rf"^(\s*-\s*){re.escape(s)}\s*$", rf"\g<1>{new}", text, flags=re.M) \
                        if re.search(r"^practice_across:", text, re.M) else text
            md.write_text(text)
    # 2. moves
    for (module, slug), folder in found.tutorials.items():
        ident = planned["new_id"][(module, slug)]
        target = TUTORIALS / ident
        if target.exists():
            fail(f"{target} already exists")
        git("mv", str(folder), str(target))
        if ident != slug:
            for path in sorted(target.iterdir()):
                if path.name.startswith(slug):
                    git("mv", str(path), str(target / (ident + path.name[len(slug):])))
    # 3. course files
    for module, course in planned["courses"].items():
        (COURSES / f"{module}.yaml").write_text(yaml.safe_dump(course, sort_keys=False, allow_unicode=True, width=78))
    (COURSES / "index.yaml").write_text(yaml.safe_dump({"order": planned["order"]}, sort_keys=False))
    (COURSES / "redirects.yaml").write_text(
        "# old address -> new address, one per line; build.py writes a stub page at each old one.\n"
        + yaml.safe_dump({old: new for old, new in planned["redirects"]}, sort_keys=True, width=120)
    )
    # 4. the old placement files
    for path in list(TUTORIALS.rglob(f"*{ORDER_SUFFIX}")) + list(TUTORIALS.glob("*/series.yaml")):
        git("rm", "-q", str(path))
    if (TUTORIALS / "modules.yaml").is_file():
        git("rm", "-q", str(TUTORIALS / "modules.yaml"))
    # The old module folders: a .gitkeep is the one thing left in some of
    # them; anything else is a surprise and is left for a person to look at.
    for module_dir in [p for p in TUTORIALS.iterdir() if p.is_dir() and not any(p.glob("*.md"))]:
        keep = module_dir / ".gitkeep"
        if keep.is_file():
            git("rm", "-q", str(keep))  # git also drops the folder once it is empty
        if not module_dir.exists():
            continue
        if not any(module_dir.iterdir()):
            module_dir.rmdir()
        else:
            print(f"note: {module_dir.relative_to(ROOT)} still holds files that are not tutorials; left in place")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--apply", action="store_true", help="write; without it, report only")
    parser.add_argument("--rename", action="append", default=[], metavar="MODULE/SLUG=NEW_ID",
                        help="resolve an id collision; may repeat")
    args = parser.parse_args()
    renames: dict[str, str] = {}
    for spec in args.rename:
        if "=" not in spec or "/" not in spec.split("=")[0]:
            fail(f"--rename wants MODULE/SLUG=NEW_ID, got {spec!r}")
        old, new = spec.split("=", 1)
        renames[old] = new

    found = scan()
    if not found.tutorials:
        print("nothing to migrate: no tutorials/<module>/<slug>/ folders (already migrated?)")
        return
    clashes = collisions(found)
    unresolved = {}
    for slug, mods in clashes.items():
        resolved = [m for m in mods if f"{m}/{slug}" in renames]
        if len(mods) - len(resolved) > 1:
            unresolved[slug] = mods
    planned = plan(found, renames)

    print(f"tutorial folders: {len(found.tutorials)}  (files: {sum(len(v) for v in found.files.values())})")
    print(f"modules: {len(planned['courses'])} -> courses in order: {', '.join(planned['order'])}")
    for module, course in planned["courses"].items():
        n = sum(len(s["tutorials"]) for s in course["contents"])
        print(f"  {module}: {len(course['contents'])} series, {n} listed"
              + (f", {len(course['mixed'])} mixed" if course.get("mixed") else "")
              + ("" if course.get("card") else "  [no card text found in home.md]")
              + ("" if course.get("code") else "  [no code in MODULE_INFO or home.md]"))
    print(f"redirects: {len(planned['redirects'])}")
    if clashes:
        print("id collisions across modules:")
        for slug, mods in clashes.items():
            print(f"  {slug}: {', '.join(mods)}"
                  + ("" if slug not in unresolved else
                     f"   -> add e.g. --rename {mods[0]}/{slug}={slug}-{''.join(w[0] for w in mods[0].split('-'))}"))
    renamed = {k: v for k, v in planned["new_id"].items() if v != k[1]}
    for (module, slug), new in renamed.items():
        print(f"rename: {module}/{slug} -> {new}")
    if unresolved:
        fail("resolve every collision with --rename before --apply")
    if not args.apply:
        print("dry run: nothing written. Add --apply to write.")
        return
    apply(found, planned)
    print("applied. Next: refactor/PLAN.md step 2 (the build does not read courses/ yet).")


if __name__ == "__main__":
    main()
