# Shared setup: the small readings table several tutorials in this series use.
# Expanded into the tutorial's own source by build.py, then executed in the
# student's browser like any other cell.
import pandas as pd

readings = pd.DataFrame(
    {
        "site": ["Cork", "Galway", "Sligo", "Wexford"],
        "morning": [11.4, 10.1, 9.7, 12.2],
        "evening": [14.8, 13.6, 12.0, 15.1],
    }
)
