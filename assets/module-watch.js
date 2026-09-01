/* The Python that makes a mounted folder importable, and that reports
 * when a file already imported from it has since been edited.
 *
 * Kept in its own module because both paths need exactly the same Python:
 * pyodide-engine.js runs it directly on the main-thread fallback, and
 * pyodide-worker.js runs it inside the Worker. Writing it twice would
 * mean two behaviours that drift apart while both look correct.
 *
 * Every function here returns a *source string*. Nothing is installed
 * into the interpreter at boot, so a page that never mounts a folder —
 * every tutorial page — pays nothing for this file existing.
 */

/* Puts one directory on Python's import search list.
 *
 * Mounting a folder makes its files readable. Python imports only from
 * directories named in `sys.path`, and a mount point is not one of them,
 * so without this a student can have two Python files in the workspace
 * and no way to use one from the other.
 *
 * Idempotent, so a caller may run it after every mount. `insert(0, …)`
 * rather than `append`: a student's own shapes.py should win over
 * anything of the same name further down the path, since a name clash
 * they can see and rename is better than one they cannot. */
export function importPathSource(path) {
  return `
import sys as _dewlab_sys
_dewlab_path = ${JSON.stringify(path)}
if _dewlab_path not in _dewlab_sys.path:
    _dewlab_sys.path.insert(0, _dewlab_path)
del _dewlab_path, _dewlab_sys
`;
}

/* Makes one directory Python's working directory.
 *
 * Without this a student's own `open("notes.txt", "w")` writes to
 * Pyodide's default directory, which is not the workspace: the file does
 * not appear in Files, is not on the import path, and is gone on the next
 * reload. Every part of the interface already tells them otherwise — the
 * Files panel calls itself "a real filesystem a cell can read and write
 * to" — so the working directory is what has to move, not the promise.
 *
 * Idempotent, and safe to run after every mount. */
export function workingDirectorySource(path) {
  return `
import os as _dewlab_os
try:
    _dewlab_os.chdir(${JSON.stringify(path)})
except OSError:
    pass
del _dewlab_os
`;
}

/* Reports every module imported from under `path`, with the last-modified
 * time of the file it was read from, as a JSON array of
 * `{name, file, mtime}`.
 *
 * The caller compares this against what it saw before; nothing is
 * remembered on the Python side. A module whose file has vanished is
 * reported with `mtime` null rather than omitted, so a caller can tell
 * "deleted" from "never imported".
 *
 * Wrapped in a function so none of its names survive in the namespace a
 * student's own cells run against — `_page_globals` is shared, and a
 * stray `os` appearing in the Workbench's variable list because dewmini
 * asked a question would be dewmini's mess showing through. */
export function importedModuleTimesSource(path) {
  return `
def _dewlab_module_times():
    import json, os, sys
    root = ${JSON.stringify(path)}
    prefix = root if root.endswith("/") else root + "/"
    out = []
    for name, module in list(sys.modules.items()):
        f = getattr(module, "__file__", None)
        if not f or not f.startswith(prefix):
            continue
        try:
            mtime = os.path.getmtime(f)
        except OSError:
            mtime = None
        out.append({"name": name, "file": f, "mtime": mtime})
    return json.dumps(out)

_dewlab_module_times()
`;
}

/* Re-reads the named modules from disk, returning JSON
 * `{reloaded: [...], failed: [{name, error}]}`.
 *
 * A failure is reported rather than raised. Editing a file into a syntax
 * error is an ordinary thing for a student to do, and the reload is
 * dewmini asking on their behalf — so the error belongs on screen as an
 * answer to "reload this", not as an exception from a cell that did
 * nothing wrong.
 *
 * Reloading rebinds the module object's own contents. A name imported
 * with `from shapes import area` still points at the old function: that
 * binding lives in the student's namespace, not in the module. Whatever
 * calls this has to say so. */
export function reloadModulesSource(names) {
  return `
def _dewlab_reload(names):
    import importlib, json, sys
    reloaded, failed = [], []
    for name in names:
        module = sys.modules.get(name)
        if module is None:
            continue
        try:
            importlib.reload(module)
            reloaded.append(name)
        except Exception as err:
            failed.append({"name": name, "error": f"{type(err).__name__}: {err}"})
    return json.dumps({"reloaded": reloaded, "failed": failed})

_dewlab_reload(${JSON.stringify(names)})
`;
}
