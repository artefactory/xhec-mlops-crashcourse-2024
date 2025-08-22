# Introduction

Welcome to the MLOps Introduction Course! Over the course of the next sessions, we will present you some of the fundamental aspects of engineering applied to Machine Learning.

## Introduction to Coding Best Practices

The first step will be to cover the Coding Best Practices Guide available [here](../best-practices/best_practices_guide.md).

Once this step is done, you can start working on the use case that we will explore throughout this entire course.

## Introduction to the Use Case

The project focuses on predicting the duration of _New York City Taxi trips_. \
The objective is to use the available data to train a simple machine learning model
that can predict the trip duration based on inputs that could be available in a production environment.

The ultimate goal for this use case could be to predict trip durations in real time (similar to Google Maps or Waze itineraries),
but for simplicity, in this module, we will assume that we only need batch predictions. The data for which we need predictions
will be stored in a file for ingestion by an untrained model.

The machine learning phase primarily consists of the following steps:

- Data processing
- Model training
- Model evaluation
- Prediction

The data for this module can be downloaded from the [TLC Trip Record Data page](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page).
To complete this module, you will need three samples of data:

- `Sample 1 example`: [Yellow trip 2021-01 data](https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2021-01.parquet) (for model training)
- `Sample 2 example`: [Yellow trip 2021-02 data](https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2021-02.parquet) (for model evaluation)
- `Sample 3 example`: [Yellow trip 2021-03 data](https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2021-03.parquet) (for prediction)

> **Disclaimer** :
> The volumes of data used in this module are not significant enough to produce efficient models and
> interpretable performances. Here we use data volumes that fit locally and allow for pipeline building and fast execution, but we do not focus on model performance and interpretability as it is not the main focus of this course.

> **Data location** :
> Please place the downloaded files inside the "data" folder in the course root directory. \
> If the names are different, please rename your files to "yellow_tripdata_2021-01.parquet", "yellow_tripdata_2021-02.parquet", and "yellow_tripdata_2021-03.parquet" respectively.

### Introduction Notebook

A notebook implementing the machine learning steps to predict Taxi trip duration can be found [here](./practice-intro-subject.ipynb). Your first task is run this notebook and pay attention to:

- The features that are used
- The target variable and how it is computed
- The models that are used to fit the data

> Be sure to activate the virtual environment from the root directory of the course before running the notebook.
