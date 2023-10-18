import os
from typing import Optional

import numpy as np
from helpers import load_pickle, save_pickle
from loguru import logger
from modeling import evaluate_model, predict, train_model
from prefect import flow
from preprocessing import process_data
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LinearRegression


@flow(name="Train model")
def train_model_workflow(
    train_filepath: str,
    test_filepath: str,
    artifacts_filepath: Optional[str] = None,
) -> dict:
    """Train a model and save it to a file"""
    logger.info("Processing training data...")
    X_train, y_train, dv = process_data(filepath=train_filepath, with_target=True)
    logger.info("Processing test data...")
    X_test, y_test, _ = process_data(filepath=test_filepath, with_target=True, dv=dv)
    logger.info("Training model...")
    model = train_model(X_train, y_train)
    logger.info("Making predictions and evaluating...")
    y_pred = predict(X_test, model)
    rmse = evaluate_model(y_test, y_pred)

    if artifacts_filepath is not None:
        logger.info(f"Saving artifacts to {artifacts_filepath}...")
        save_pickle(os.path.join(artifacts_filepath, "dv.pkl"), dv)
        save_pickle(os.path.join(artifacts_filepath, "model.pkl"), model)

    return {"model": model, "dv": dv, "rmse": rmse}


@flow(name="Batch predict", retries=1, retry_delay_seconds=30)
def batch_predict_workflow(
    input_filepath: str,
    model: Optional[LinearRegression] = None,
    dv: Optional[DictVectorizer] = None,
    artifacts_filepath: Optional[str] = None,
) -> np.ndarray:
    """Make predictions on a new dataset"""
    if dv is None:
        dv = load_pickle(os.path.join(artifacts_filepath, "dv.pkl"))
    if model is None:
        model = load_pickle(os.path.join(artifacts_filepath, "model.pkl"))

    X, _, _ = process_data(filepath=input_filepath, with_target=False, dv=dv)
    y_pred = predict(X, model)

    return y_pred


if __name__ == "__main__":
    from config import DATA_DIRPATH, MODELS_DIRPATH

    train_model_workflow(
        train_filepath=os.path.join(DATA_DIRPATH, "yellow_tripdata_2021-01.parquet"),
        test_filepath=os.path.join(DATA_DIRPATH, "yellow_tripdata_2021-02.parquet"),
        artifacts_filepath=MODELS_DIRPATH,
    )

    batch_predict_workflow(
        input_filepath=os.path.join(DATA_DIRPATH, "yellow_tripdata_2021-03.parquet"),
        artifacts_filepath=MODELS_DIRPATH,
    )
