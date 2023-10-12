from app_config import (
    APP_DESCRIPTION,
    APP_TITLE,
    APP_VERSION,
    MODEL_VERSION,
    PATH_TO_PIPELINE,
)
from fastapi import FastAPI
from lib.modelling import run_inference
from lib.models import InputData, PredictionOut
from lib.utils import load_pipeline

app = FastAPI(title=APP_TITLE, description=APP_DESCRIPTION, version=APP_VERSION)


@app.get("/")
def home():
    return {"health_check": "OK", "model_version": MODEL_VERSION}


@app.post("/predict", response_model=PredictionOut, status_code=201)
def predict(payload: InputData):
    pipeline = load_pipeline(PATH_TO_PIPELINE)
    trip_duration_prediction = run_inference(payload.model_dump(), pipeline)
    return {"trip_duration_prediction": trip_duration_prediction}
