#! /usr/bin/env python3
"""
Evaluate improving the speed of a very large pandas DataFrame by using a
feather file and by downcasting integer columns and convert an object column
to a category column.

Three methods of selecting rows are evaluated:
- bracket notation, def f1
- index, def f2
- .loc, def f3
"""

from typing import NoReturn
from pathlib import Path
import timeit
import time
import gc

import datasense as ds
import pandas as pd
import numpy as np


def f1(
    df: pd.DataFrame,
    column: str,
    value: str
) -> pd.DataFrame:
    """
    Selecting rows using bracket notation
    """
    df = df[df[column] == value]
    return df


def f2(
    df: pd.DataFrame,
    column: str,
    value: str
) -> pd.DataFrame:
    """
    Selecting rows using index
    """
    df = df.set_index(
        keys=column,
        drop=False
    )
    df = df.loc[value]
    return df


def f3(
    df: pd.DataFrame,
    column: str,
    value: str
) -> pd.DataFrame:
    """
    Selecting rows using .loc
    """
    df = df.loc[df[column] == value, :]
    return df


def compare_functions(
    repetitions: int,
    replications: int
) -> NoReturn:
    start_time = time.perf_counter()
    stmt_f1 = """df = f1(
        df=example_df,
        column=COLUMN,
        value=VALUE
    )"""
    stmt_f2 = """df = f2(
        df=example_df,
        column=COLUMN,
        value=VALUE
    )"""
    stmt_f3 = """df = f3(
        df=example_df,
        column=COLUMN,
        value=VALUE
    )"""
    time_f1 = timeit.repeat(
        stmt=stmt_f1,
        setup='pass',
        repeat=replications,
        number=repetitions,
        globals=globals()
    )
    time_f2 = timeit.repeat(
        stmt=stmt_f2,
        setup='pass',
        repeat=replications,
        number=repetitions,
        globals=globals()
    )
    time_f3 = timeit.repeat(
        stmt=stmt_f3,
        setup='pass',
        repeat=replications,
        number=repetitions,
        globals=globals()
    )
    print(f"Repetions   : {repetitions:>6.0f}")
    print(f"Replications: {replications:>6.0f}")
    print(f'Average time for f1: {min(time_f1) / repetitions} s')
    print(f'Average time for f2: {min(time_f2) / repetitions} s')
    print(f'Average time for f3: {min(time_f3) / repetitions} s')
    stop_time = time.perf_counter()
    ds.report_summary(
        start_time=start_time,
        stop_time=stop_time,
        print_heading=False
    )
    print()


def create_large_csv_file(
    path_csv: Path,
    rows_per_category: int
) -> NoReturn:
    df = pd.DataFrame(
        data=np.random.randint(
            low=0,
            high=100,
            size=(10000000, 50)
        )
    )
    df = df.rename(columns={i: f"x_{i}" for i in range(50)})
    df["category"] = ["A", "B", "C", "D"] * rows_per_category
    ds.save_file(
        df=df,
        file_name=path_csv
    )
    print("Create a DataFrame and save as a csv file")
    print()


def read_large_csv_file(
    path_csv: Path,
    chunksize: int
) -> pd.DataFrame:
    print("Reading csv file chunks")
    start_time = time.perf_counter()
    chunk = pd.read_csv(
        filepath_or_buffer=path_csv,
        chunksize=chunksize
    )
    stop_time = time.perf_counter()
    ds.report_summary(
        start_time=start_time,
        stop_time=stop_time,
        print_heading=False
    )
    print()
    print("Creating DataFrame from csv file chunks")
    start_time = time.perf_counter()
    df = pd.concat(objs=chunk)
    stop_time = time.perf_counter()
    ds.report_summary(
        start_time=start_time,
        stop_time=stop_time,
        print_heading=False
    )
    print()
    print("Information about the DataFrame:")
    start_time = time.perf_counter()
    print(df.info(verbose=False))
    stop_time = time.perf_counter()
    ds.report_summary(
        start_time=start_time,
        stop_time=stop_time,
        print_heading=False
    )
    print()
    return df


def optimize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = ds.optimize_columns(df=df)
    print("Information about the DataFrame after optimization of columns")
    print(df.info(verbose=False))
    return df


def save_csv_file_as_feather_file(
    df: pd.DataFrame,
    path_feather: Path
) -> pd.DataFrame:
    ds.save_file(
        df=df,
        file_name=path_feather
    )
    print("Save the DataFrame as a feather file")
    print()
    return df


def read_large_feather_file(
    path_feather: Path
) -> pd.DataFrame:
    print("Read feather file, create DataFrame")
    start_time = time.perf_counter()
    df = ds.read_file(file_name=path_feather)
    stop_time = time.perf_counter()
    ds.report_summary(
        start_time=start_time,
        stop_time=stop_time,
        print_heading=False
    )
    print()
    print("Information about the DataFrame:")
    start_time = time.perf_counter()
    print(df.info(verbose=False))
    stop_time = time.perf_counter()
    ds.report_summary(
        start_time=start_time,
        stop_time=stop_time,
        print_heading=False
    )
    print()
    return df


def main():
    global example_df, COLUMN, VALUE
    PATH_FEATHER = Path("very_large.feather")
    PATH_CSV = Path("very_large.csv")
    ROWS_PER_CATEGORY = 2500000
    CHUNKSIZE = 1000000
    COLUMN = "category"
    REPETITIONS = 10
    REPLICATIONS = 5
    VALUE = "A"
    gc.enable()
    # create_large_csv_file(
    #     path_csv=PATH_CSV,
    #     rows_per_category=ROWS_PER_CATEGORY
    # )
    # df = read_large_csv_file(path_csv=PATH_CSV)
    # df = optimize_columns(df=df)
    # save_csv_file_as_feather_file(
    #     df=df,
    #     path_feather=PATH_FEATHER
    # )
    print("Analysis using feather file")
    print("---------------------------")
    print()
    example_df = read_large_feather_file(path_feather=PATH_FEATHER)
    compare_functions(
        repetitions=REPETITIONS,
        replications=REPLICATIONS
    )
    print("Analysis using csv file")
    print("-----------------------")
    print()
    example_df = read_large_csv_file(
        path_csv=PATH_CSV,
        chunksize=CHUNKSIZE
    )
    compare_functions(
        repetitions=REPETITIONS,
        replications=REPLICATIONS
    )


if __name__ == "__main__":
    main()
