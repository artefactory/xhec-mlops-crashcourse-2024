import pickle
from typing import Any


def load_pickle(path: str):
    with open(path, "rb") as f:
        loaded_obj = pickle.load(f)
    return loaded_obj


def save_pickle(path: str, obj: Any):
    with open(path, "wb") as f:
        pickle.dump(obj, f)
