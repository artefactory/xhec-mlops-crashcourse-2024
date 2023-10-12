import joblib
from loguru import logger
from sklearn.pipeline import Pipeline


def load_pipeline(path: str) -> Pipeline:
    logger.info(f"Loading pipeline from {path}")
    return joblib.load(path)
