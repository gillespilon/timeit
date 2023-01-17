#! /usr/bin/env python3
"""
Create a pandas series by replacing text from another column.
"""

from typing import Dict, NoReturn
import timeit
import gc

import pandas as pd


def main():
    global example_dataframe, replacement_dictionary
    gc.enable()
    example_dataframe = pd.DataFrame(
        {
            "Cal Yr-Mth": [
                "2021/01", "2021/02", "2021/03", "2021/04",
                "2021/05", "2021/06", "2021/07", "2021/08",
                "2021/09", "2021/10", "2021/11", "2021/12"
            ]
        }
    )
    replacement_dictionary = {
        "2021/01": "2021-1Q",
        "2021/02": "2021-1Q",
        "2021/03": "2021-1Q",
        "2021/04": "2021-2Q",
        "2021/05": "2021-2Q",
        "2021/06": "2021-2Q",
        "2021/07": "2021-3Q",
        "2021/08": "2021-3Q",
        "2021/09": "2021-3Q",
        "2021/10": "2021-4Q",
        "2021/11": "2021-4Q",
        "2021/12": "2021-4Q",
    }
    REPETITIONS = 1000
    REPLICATIONS = 10
    compare_functions(
        repetitions=REPETITIONS,
        replications=REPLICATIONS
    )


def f1(
    df: pd.DataFrame,
    dictionary: Dict
) -> pd.DataFrame:
    """
    Use map to replace cells
    """
    df["Yr-Qtr"] = df["Cal Yr-Mth"].map(dictionary.get)
    return df


def compare_functions(
    repetitions: int,
    replications: int
) -> NoReturn:
    #     setup_code_f1 = """
    # from __main__ import f1
    # """
    stmt_f1 = """df = f1(
        df=example_dataframe,
        dictionary=replacement_dictionary
        )"""
    times_f1 = timeit.repeat(
        stmt=stmt_f1,
        setup="pass",
        repeat=replications,
        number=repetitions,
        globals=globals()
    )
    print(f"Total time for f1: {min(times_f1)} s")


if __name__ == "__main__":
    main()
