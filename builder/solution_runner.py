"""Run one page's cells and solutions, in a Python of their own.

Started by builder/solutions.py, never imported: a page's code must not run
inside the program that checks it. The job arrives as JSON on standard input
and the results leave as JSON on standard output.
"""
import asyncio, json, os, signal, sys
os.environ["MPLBACKEND"] = "Agg"
job = json.load(sys.stdin)
sys.path.insert(0, job["assets"])
import tutorial_tools as tt

tt._page_globals.update({name: getattr(tt, name) for name in tt.__all__})
tt._page_globals["__name__"] = "__dewlab__"


def local(name):
    if name.startswith(("http://", "https://")):
        if name not in job["addresses"]:
            raise ConnectionError(f"the build does not fetch {name}")
        name = job["addresses"][name]
    return os.path.join(job["data"], name)


async def load_csv(name, **kwargs):
    import pandas
    return pandas.read_csv(local(name), **kwargs)


async def load_text(name):
    with open(local(name), encoding="utf-8") as handle:
        return handle.read()


tt._page_globals["load_csv"] = load_csv
tt._page_globals["load_text"] = load_text
if job["sqlite"]:
    import sqlite3
    tt._page_globals["db"] = sqlite3.connect(":memory:")


class Slow(Exception):
    pass


def alarm(signum, frame):
    raise Slow()


timed = hasattr(signal, "SIGALRM")
if timed:
    signal.signal(signal.SIGALRM, alarm)


missing = None  # the first package a cell asked for and this Python lacks


async def run(code, name, typed=None):
    global missing
    tt._begin(name, tt._RecordingSink(), code, typed=typed)
    if timed:
        signal.alarm(job["seconds"])
    try:
        await tt._run_code(code, tt._page_globals, name)
    except ModuleNotFoundError as exc:
        # The cell stopped at its import, so whatever it would have made
        # after that is missing for every solution below it.
        missing = missing or f"{type(exc).__name__}: {exc}"
    except BaseException:
        pass  # a cell that fails as written is the page's own business
    finally:
        if timed:
            signal.alarm(0)
        tt._end(None)


async def main():
    for code in job["toolkit"]:
        await run(code, "toolkit")
    report = []
    for cell in job["cells"]:
        await run(cell["code"], cell["id"], cell.get("typed"))
        if "solution" in cell:
            if timed:
                signal.alarm(job["seconds"])
            typed = json.dumps(cell["typed"]) if cell.get("typed") else None
            try:
                result = json.loads(await tt.compare(
                    cell["solution"], json.dumps(cell["inputs"]), None, typed))
            except Slow:
                result = {"solutionError": "the solution did not finish", "rows": []}
            finally:
                if timed:
                    signal.alarm(0)
            if missing:
                result["missingModule"] = missing
            report.append({"cell": cell["id"], "result": result})
    sys.__stdout__.write(json.dumps(report))


asyncio.run(main())
