from lib.preprocessing import prepare_data
from loguru import logger
from sklearn.pipeline import Pipeline


def run_inference(payload: dict, pipeline: Pipeline) -> float:
    """Runs an inference on a single data point using a pre-fitted pipeline.

    Takes a pre-fitted pipeline (dictvectorizer + linear regression model) outputs the computed
    trip duration in minutes.

    Args:
        payload (dict): the data point to run inference on.
        pipeline (Pipeline): the pre-fitted pipeline containing a dictvectorizer and a linear
            model.

    Returns:
        float: the predicted trip duration in minutes.

    Example payload:
        {'PULocationID': 264, 'DOLocationID': 264, 'passenger_count': 1}
    """
    logger.info("Running inference on payload...")
    prep_features = prepare_data(payload)
    trip_duration_prediction = pipeline.predict(prep_features)[0]
    return trip_duration_prediction
