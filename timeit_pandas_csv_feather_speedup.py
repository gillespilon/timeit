#! /usr/bin/env python3
"""
Evaluate improving the speed of a very large pandas DataFrame by using a
feather file and by downcasting integer columns and convert an object column
to a category column.
"""

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
    df = df[df[column] == value]
    return df


def f2(
    df: pd.DataFrame,
    column: str,
    value: str
) -> pd.DataFrame:
    df = df.set_index(keys=column, drop=False)
    df = df.loc[value]
    return df


def f3(
    df: pd.DataFrame,
    column: str,
    value: str
) -> pd.DataFrame:
    df = df.loc[df[column] == value, :]
    return df


def compare_functions(
    repetitions: int,
    replications: int
):
    start_time = time.perf_counter()
    stmt_f1 = 'result = f1(df=df, column="category", value="A")'
    stmt_f1 = 'result = f2(df=df, column="category", value="A")'
    stmt_f1 = 'result = f3(df=df, column="category", value="A")'
    time_f1 = timeit.repeat(
        stmt=stmt_f1,
        setup='pass',
        repeat=replications,
        number=repetitions,
        globals=globals()
    )
    time_f2 = timeit.repeat(
        stmt=stmt_f1,
        setup='pass',
        repeat=replications,
        number=repetitions,
        globals=globals()
    )
    time_f3 = timeit.repeat(
        stmt=stmt_f1,
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


def create_large_csv_file(path_csv: Path):
    df = pd.DataFrame(np.random.randint(0, 100, size=(10000000, 50)))
    df = df.rename(columns={i: f"x_{i}" for i in range(50)})
    df["category"] = ["A", "B", "C", "D"] * 2500000
    ds.save_file(df=df, file_name=path_csv)
    print("Create a DataFrame and save as a csv file")
    print()


def read_large_csv_file(path_csv: Path):
    print("Reading csv file chunks")
    start_time = time.perf_counter()
    chunk = pd.read_csv(
        filepath_or_buffer=path_csv,
        chunksize=1000000
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


def optimize_columns(df: pd.DataFrame):
    df = ds.optimize_columns(df=df)
    print("Information about the DataFrame after optimization of columns")
    print(df.info(verbose=False))
    return df


def save_csv_file_as_feather_file(
    df: pd.DataFrame,
    path_feather: Path
):
    ds.save_file(df=df, file_name=path_feather)
    print("Save the DataFrame as a feather file")
    print()
    return df


def read_large_feather_file(
    path_feather: Path
):
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
    global df
    path_feather = Path("very_large.feather")
    path_csv = Path("very_large.csv")
    repetitions = 10
    replications = 5
    gc.enable()
    # create_large_csv_file(path_csv=path_csv)
    # df = read_large_csv_file(path_csv=path_csv)
    # df = optimize_columns(df=df)
    # save_csv_file_as_feather_file(
    #     df=df,
    #     path_feather=path_feather
    # )
    print("Analysis using feather file")
    print("---------------------------")
    print()
    df = read_large_feather_file(path_feather=path_feather)
    compare_functions(repetitions=repetitions, replications=replications)
    print("Analysis using csv file")
    print("-----------------------")
    print()
    df = read_large_csv_file(path_csv=path_csv)
    compare_functions(repetitions=repetitions, replications=replications)


if __name__ == "__main__":
    main()
