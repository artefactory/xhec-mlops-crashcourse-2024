import os
import pickle
from functools import lru_cache

from loguru import logger
from sklearn.pipeline import Pipeline


@lru_cache
def load_preprocessor(filepath: os.PathLike):
    with open(filepath, "rb") as f:
        return pickle.load(f)


@lru_cache
def load_model(filepath: os.PathLike):
    with open(filepath, "rb") as f:
        return pickle.load(f)
