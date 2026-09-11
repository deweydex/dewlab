
export function importPathSource(path) {
  return `
import sys as _dewlab_sys
_dewlab_path = ${JSON.stringify(path)}
if _dewlab_path not in _dewlab_sys.path:
    _dewlab_sys.path.insert(0, _dewlab_path)
del _dewlab_path, _dewlab_sys
`;
}

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
