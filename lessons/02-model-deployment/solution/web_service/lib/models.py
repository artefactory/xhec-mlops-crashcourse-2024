from pydantic import BaseModel


class InputData(BaseModel):
    PULocationID: int
    DOLocationID: int
    passenger_count: int


class PredictionOut(BaseModel):
    trip_duration_prediction: float
