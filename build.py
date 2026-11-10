#!/usr/bin/env python3
"""Turn the markdown in tutorials/ into the hosted HTML series in site/.

    python3 build.py            build into site/
    python3 build.py --clean    remove site/ first

This file is only the command. The build is the `builder` package beside it,
and `builder/main.py` is where to start reading.
"""

import sys

from builder import main as _main

if __name__ == "__main__":
    raise SystemExit(_main.main())

# Imported, `build` is the build itself and not a copy of its names: a test
# or script that says `import build as b` gets builder.main, so that setting
# `b.something` changes what the build reads.
sys.modules[__name__] = _main
