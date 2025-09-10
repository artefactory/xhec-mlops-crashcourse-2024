import pickle
from pathlib import Path
from typing import Any


def load_pickle(path: str) -> Any:
    """..."""
    with Path(path).open("rb") as f:
        loaded_obj = pickle.load(f)
    return loaded_obj


def save_pickle(path: str, obj: Any) -> Any:
    """..."""
    with Path(path).open("wb") as f:
        pickle.dump(obj, f)
