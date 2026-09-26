#!/usr/bin/env python3
"""Check the glossary's Python entries against Python itself, and write the
signatures the reference shows beside them.

A glossary entry that names something in Python says which thing, with a
`python:` field: one dotted name, or a list of them.

    - term: append()
      python: list.append
    - term: math.sin(), math.cos()
      python: [math.sin, math.cos]
    - term: lambda
      python: lambda

The term is written for a reader and can say anything ("`.get()`,
default"); `python:` is written for this script, and names the object
exactly, owner included, since `append` alone could belong to any type.

For every such entry this checks, against the real object:

1. **The name exists.** It is a Python keyword, or it imports and every
   attribute along the dotted path is there. A misspelling, or a function a
   library has since removed, fails here.
2. **The example calls it the way Python allows.** Each call in the
   entry's `example` to a named function is bound against that function's
   own signature (`inspect.Signature.bind`), with stand-in values, so too
   many arguments, too few, or a keyword it does not take fails, without
   running anything. An example that is not Python, or not a whole
   statement, is skipped rather than failed: an example is there to be
   read, not run.

It then writes `assets/python-signatures.json`: the signature of each
named built-in, standard-library or `tutorial_tools` function, as Python
itself formats it, type hints left out because a reader has not met them.
The build attaches these to the entries, and the reference panel shows
them under the definition. Third-party libraries get checks 1 and 2 but no
signature: pandas' `to_csv()` takes twenty-odd parameters and matplotlib's
`plot()` ends in `**kwargs`, neither of which helps a reader.

Signatures depend on the Python version, so write the file with the one
Pyodide runs (3.13 for Pyodide 0.28; see `dev/fetch_pyodide.py`). `--check`
under another version still checks names and examples, and says it skipped
comparing signatures.

    python3.13 dev/glossary_python.py           # write the signatures file
    python3 dev/glossary_python.py --check      # fail on any problem

Needs numpy, pandas and matplotlib installed, as the unit tests do, since
entries name things in them.
"""

from __future__ import annotations

import argparse
import ast
import importlib
import inspect
import json
import keyword
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
SIGNATURES = ROOT / "assets" / "python-signatures.json"
PYTHON_BASICS = ROOT / "planning" / "curriculum" / "python-basics.yaml"

sys.path.insert(0, str(ROOT / "assets"))    # so `tutorial_tools.check` imports

# Modules whose functions get a signature: Python's own, and the course's.
OWN_MODULES = {"tutorial_tools"}

KEYWORD = object()   # what resolve() returns for `lambda`, `elif` and the rest


def glossary_files() -> list[Path]:
    files = sorted(ROOT.glob("tutorials/*/*.glossary.yaml"))
    if PYTHON_BASICS.is_file():
        files.append(PYTHON_BASICS)
    return files


def entries_of(path: Path) -> list[dict]:
    data = yaml.safe_load(path.read_text()) or {}
    if "groups" in data:
        return [entry for group in data["groups"] for entry in group.get("entries") or []]
    return data.get("entries") or []


def names_of(entry: dict) -> list[str]:
    names = entry.get("python")
    if names is None:
        return []
    return [names] if isinstance(names, str) else list(names)


def resolve(name: str):
    """The object a dotted name means, and the class it was looked up on
    (None for a module-level name)."""
    if keyword.iskeyword(name) or keyword.issoftkeyword(name):
        return KEYWORD, None
    parts = name.split(".")
    if len(parts) == 1:
        import builtins
        if hasattr(builtins, name):
            return getattr(builtins, name), None
        raise LookupError(f"{name!r} is not a keyword or a built-in")
    import builtins
    if hasattr(builtins, parts[0]):
        target, rest = getattr(builtins, parts[0]), parts[1:]
    else:
        for cut in range(len(parts) - 1, 0, -1):
            try:
                target = importlib.import_module(".".join(parts[:cut]))
            except ImportError:
                continue
            rest = parts[cut:]
            break
        else:
            raise LookupError(f"no module in {name!r} could be imported")
    owner = None
    for attribute in rest:
        if not hasattr(target, attribute):
            raise LookupError(f"{name!r}: {attribute!r} is not there")
        owner = target if inspect.isclass(target) else None
        target = getattr(target, attribute)
    return target, owner


def signature_of(obj):
    try:
        return inspect.signature(obj)
    except (TypeError, ValueError):
        return None


def module_of(obj, owner) -> str:
    return getattr(owner or obj, "__module__", None) or ""


def gets_a_signature(obj, owner) -> bool:
    module = module_of(obj, owner).split(".")[0]
    return module in sys.stdlib_module_names or module in OWN_MODULES


def display(name: str, obj, owner) -> str | None:
    """`name(params)` as Python formats them, minus type hints and minus
    the `self` a method is written with but never passed by a reader."""
    signature = signature_of(obj)
    if signature is None:
        return None
    parameters = [p.replace(annotation=inspect.Parameter.empty)
                  for p in signature.parameters.values()]
    if owner is not None and parameters and parameters[0].name == "self":
        parameters = parameters[1:]
    plain = signature.replace(parameters=parameters,
                              return_annotation=inspect.Signature.empty)
    # A reader calls the course's own helpers by their bare names, since
    # every cell already has them: `show(...)`, never `tutorial_tools.show`.
    if name.split(".")[0] in OWN_MODULES:
        name = name.split(".", 1)[1]
    return f"{name}{plain}"


def parse(example: str):
    for source in (example, example + "\n    pass"):
        try:
            return ast.parse(source)
        except SyntaxError:
            continue
    return None


def example_problems(example: str, name: str, obj, owner) -> list[str]:
    """Each call in the example to `name` bound against its signature."""
    signature = signature_of(obj)
    tree = parse(example) if signature else None
    if tree is None:
        return []
    last = name.split(".")[-1]
    problems = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        called = func.id if isinstance(func, ast.Name) else (
            func.attr if isinstance(func, ast.Attribute) else None)
        if called != last:
            continue
        if any(isinstance(a, ast.Starred) for a in node.args) or \
                any(k.arg is None for k in node.keywords):
            continue
        args = [None] * len(node.args)
        # `scores.append(50)` passes the list itself as self; `str.find(s, x)`
        # written on the class name does not.
        on_class = isinstance(func, ast.Attribute) and isinstance(func.value, ast.Name) \
            and owner is not None and func.value.id == owner.__name__
        if owner is not None and not on_class and not isinstance(
                inspect.getattr_static(owner, last, None), (staticmethod, classmethod)):
            if next(iter(signature.parameters), None) == "self":
                args = [None] + args
        try:
            signature.bind(*args, **{k.arg: None for k in node.keywords})
        except TypeError as err:
            problems.append(f"the example calls {last}() in a way its own "
                            f"signature rejects: {err}")
    return problems


def survey() -> tuple[dict[str, str], list[str], int]:
    signatures: dict[str, str] = {}
    problems: list[str] = []
    checked = 0
    for path in glossary_files():
        where = path.relative_to(ROOT)
        for entry in entries_of(path):
            names = entry.get("python")
            if names is not None and not (
                    isinstance(names, str)
                    or (isinstance(names, list) and all(isinstance(n, str) for n in names))):
                problems.append(f"{where}: {entry.get('term')!r}: `python:` must be "
                                "a dotted name or a list of them")
                continue
            for name in names_of(entry):
                checked += 1
                try:
                    obj, owner = resolve(name)
                except LookupError as err:
                    problems.append(f"{where}: {entry.get('term')!r}: {err}")
                    continue
                if obj is KEYWORD:
                    continue
                for problem in example_problems(str(entry.get("example") or ""), name, obj, owner):
                    problems.append(f"{where}: {entry.get('term')!r}: {problem}")
                if gets_a_signature(obj, owner):
                    text = display(name, obj, owner)
                    if text:
                        signatures[name] = text
    return dict(sorted(signatures.items())), problems, checked


def written(signatures: dict[str, str]) -> str:
    version = f"{sys.version_info.major}.{sys.version_info.minor}"
    return json.dumps({"python": version, "signatures": signatures},
                      indent=2, ensure_ascii=False) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--check", action="store_true",
                        help="report problems and a stale signatures file; write nothing")
    args = parser.parse_args()

    signatures, problems, checked = survey()
    for problem in problems:
        print(problem)

    here = f"{sys.version_info.major}.{sys.version_info.minor}"
    if args.check:
        recorded = json.loads(SIGNATURES.read_text()) if SIGNATURES.is_file() else {}
        if recorded.get("python") == here:
            if recorded.get("signatures") != signatures:
                problems.append("stale")
                print(f"{SIGNATURES.relative_to(ROOT)} is out of date: "
                      f"run python{here} dev/glossary_python.py")
        else:
            print(f"signatures were written under Python {recorded.get('python')}; "
                  f"this is {here}, so only names and examples were checked")
    else:
        SIGNATURES.write_text(written(signatures))
        print(f"wrote {SIGNATURES.relative_to(ROOT)}: {len(signatures)} signatures")

    if problems:
        print(f"\n{len([p for p in problems if p != 'stale'])} problem(s) in the glossary's Python entries.")
        return 1
    print(f"{checked} Python names in the glossary, each checked against Python.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
