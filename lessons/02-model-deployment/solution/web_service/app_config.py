# MODELS
MODEL_VERSION = "0.0.1"
PATH_TO_PIPELINE = f"local_models/pipeline__v{MODEL_VERSION}.joblib"
CATEGORICAL_VARS = ["PULocationID", "DOLocationID", "passenger_count"]


# MISC
APP_TITLE = "TripDurationPredictionApp"
APP_DESCRIPTION = (
    "A simple API to predict trip duration in minutes "
    "for NYC yellow taxi trips, given a pickup, a dropoff location "
    "and a passenger count."
)
APP_VERSION = "0.0.1"
