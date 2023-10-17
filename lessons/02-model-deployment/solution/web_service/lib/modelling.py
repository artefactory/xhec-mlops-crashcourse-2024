from typing import List

import numpy as np
import pandas as pd
from lib.models import InputData
from lib.preprocessing import CATEGORICAL_COLS, encode_categorical_cols
from sklearn.base import BaseEstimator
from sklearn.feature_extraction import DictVectorizer


def run_inference(
    input_data: List[InputData], dv: DictVectorizer, model: BaseEstimator
) -> np.ndarray:
    """Run inference on a list of input data.

    Args:
        payload (dict): the data point to run inference on.
        dv (DictVectorizer): the fitted DictVectorizer object.
        model (BaseEstimator): the fitted model object.

    Returns:
        np.ndarray: the predicted trip durations in minutes.

    Example payload:
        {'PULocationID': 264, 'DOLocationID': 264, 'passenger_count': 1}
    """
    df = pd.DataFrame([x.dict() for x in input_data])
    df = encode_categorical_cols(df)
    dicts = df[CATEGORICAL_COLS].to_dict(orient="records")
    X = dv.transform(dicts)
    y = model.predict(X)
    return y
