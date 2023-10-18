import numpy as np
import scipy.sparse
from prefect import task
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error


@task(name="Train model")
def train_model(X: scipy.sparse.csr_matrix, y: np.ndarray) -> LinearRegression:
    """Train and return a linear regression model"""
    lr = LinearRegression()
    lr.fit(X, y)
    return lr


@task(name="Make predictions")
def predict(X: scipy.sparse.csr_matrix, model: LinearRegression) -> np.ndarray:
    """Make predictions with a trained model"""
    return model.predict(X)


@task(name="Evaluate model")
def evaluate_model(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Calculate mean squared error for two arrays"""
    return mean_squared_error(y_true, y_pred, squared=False)
