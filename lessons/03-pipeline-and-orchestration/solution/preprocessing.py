import os
from typing import List, Tuple

import numpy as np
import pandas as pd
import scipy.sparse
from config import CATEGORICAL_COLS
from loguru import logger
from prefect import flow, task
from sklearn.feature_extraction import DictVectorizer


@task
def compute_target(
    df: pd.DataFrame,
    pickup_column: str = "tpep_pickup_datetime",
    dropoff_column: str = "tpep_dropoff_datetime",
) -> pd.DataFrame:
    """Compute the trip duration in minutes based on pickup and dropoff time"""
    df["duration"] = df[dropoff_column] - df[pickup_column]
    df["duration"] = df["duration"].dt.total_seconds() / 60
    return df


@task
def filter_outliers(df: pd.DataFrame, min_duration: int = 1, max_duration: int = 60) -> pd.DataFrame:
    """
    Remove rows corresponding to negative/zero
    and too high target' values from the dataset
    """
    return df[df["duration"].between(min_duration, max_duration)]


@task
def encode_categorical_cols(df: pd.DataFrame, categorical_cols: List[str] = None) -> pd.DataFrame:
    """Encode categorical columns as strings"""
    if categorical_cols is None:
        categorical_cols = CATEGORICAL_COLS
    df.loc[:, categorical_cols] = df[categorical_cols].fillna(-1).astype("int")
    df.loc[:, categorical_cols] = df[categorical_cols].astype("str")
    return df


@task
def extract_x_y(
    df: pd.DataFrame,
    categorical_cols: List[str] = None,
    dv: DictVectorizer = None,
    with_target: bool = True,
) -> Tuple[scipy.sparse.csr_matrix, np.ndarray, DictVectorizer]:
    """Extract X and y from the dataframe"""
    if categorical_cols is None:
        categorical_cols = CATEGORICAL_COLS
    dicts = df[categorical_cols].to_dict(orient="records")

    y = None
    if with_target:
        if dv is None:
            dv = DictVectorizer()
            dv.fit(dicts)
        y = df["duration"].values

    x = dv.transform(dicts)
    return x, y, dv


@flow(name="Preprocess data")
def process_data(filepath: os.PathLike, dv=None, with_target: bool = True) -> scipy.sparse.csr_matrix:
    """
    Load data from a parquet file
    Compute target (duration column) and apply threshold filters (optional)
    Turn features to sparce matrix
    :return The sparce matrix, the target' values and the
    dictvectorizer object if needed.
    """
    df = pd.read_parquet(filepath)
    if with_target:
        logger.debug(f"{filepath} | Computing target...")
        df1 = compute_target(df)
        logger.debug(f"{filepath} | Filtering outliers...")
        df2 = filter_outliers(df1)
        logger.debug(f"{filepath} | Encoding categorical columns...")
        df3 = encode_categorical_cols(df2)
        logger.debug(f"{filepath} | Extracting X and y...")
        return extract_x_y(df3, dv=dv)
    else:
        logger.debug(f"{filepath} | Encoding categorical columns...")
        df1 = encode_categorical_cols(df)
        logger.debug(f"{filepath} | Extracting X and y...")
        return extract_x_y(df1, dv=dv, with_target=with_target)
