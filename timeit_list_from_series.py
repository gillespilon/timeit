#! /usr/bin/env python3
"""
Use timeit to compare multiple ways to create a list from a pandas series.

Requires:
- datasense: https://github.com/gillespilon/datasense
"""

from typing import List
import timeit
import gc

import datasense as ds
import pandas as pd


def main():
    global random_dataframe, SERIES_COLUMN
    SERIES_COLUMN = 'col7'
    REPLICATIONS = 100
    REPETITIONS = 1000
    gc.enable()
    random_dataframe = ds.create_dataframe_norm()
    compare_functions(
        repetitions=REPETITIONS,
        replications=REPLICATIONS
    )


def f1(
    df: pd.DataFrame,
    column: str
) -> List:
    """
    Using series.tolist(). This a pandas method.
    """
    list_from_series = df[column].tolist()
    return list_from_series


def f2(
    df: pd.DataFrame,
    column: str
) -> List:
    """
    Using list(series).
    """
    list_from_series = list(df[column])
    return list_from_series


def f3(
    df: pd.DataFrame,
    column: str
) -> List:
    """
    Using list(series.array).
    """
    list_from_series = list(df[column].array)
    return list_from_series


def f4(
    df: pd.DataFrame,
    column: str
) -> List:
    """
    Using list(series.to_numpy()).
    """
    list_from_series = list(df[column].to_numpy())
    return list_from_series


def compare_functions(
    repetitions: int,
    replications: int
):
    stmt_code_f1 = """list = f1(
        df=random_dataframe,
        column=SERIES_COLUMN
    )"""
    stmt_code_f2 = """list = f2(
        df=random_dataframe,
        column=SERIES_COLUMN
    )"""
    stmt_code_f3 = """list = f3(
        df=random_dataframe,
        column=SERIES_COLUMN
    )"""
    stmt_code_f4 = """list = f4(
        df=random_dataframe,
        column=SERIES_COLUMN
    )"""
    times_f1 = timeit.repeat(
        stmt=stmt_code_f1,
        setup='pass',
        repeat=replications,
        number=repetitions,
        globals=globals()
    )
    times_f2 = timeit.repeat(
        stmt=stmt_code_f2,
        setup='pass',
        repeat=replications,
        number=repetitions,
        globals=globals()
    )
    times_f3 = timeit.repeat(
        stmt=stmt_code_f3,
        setup='pass',
        repeat=replications,
        number=repetitions,
        globals=globals()
    )
    times_f4 = timeit.repeat(
        stmt=stmt_code_f4,
        setup='pass',
        repeat=replications,
        number=repetitions,
        globals=globals()
    )
    print(f'Total time for f1: {min(times_f1)} s')
    print(f'Total time for f2: {min(times_f2)} s')
    print(f'Total time for f3: {min(times_f3)} s')
    print(f'Total time for f4: {min(times_f4)} s')


if __name__ == '__main__':
    main()
