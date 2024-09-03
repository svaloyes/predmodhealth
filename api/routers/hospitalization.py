"""
Endpoint Elderly Hospitalization Prediction
Router Elderly Hospitalization Prediction
"""
from fastapi import APIRouter
from api.middleware.model_predict import predict_hospitalization

# Define the router for elderly hospitalization prediction
elderly_prediction = APIRouter(
    prefix="/queries",
    tags=["Elderly Hospitalization Prediction"],
    responses={404: {"status": "disconnected"}},
)

@elderly_prediction.get("/")
def home_page():
    """
    Home page for the Elderly Hospitalization Prediction router.
    """
    return {"page": "home", "version": "1.0", "update_date": "2023-03-04"}

@elderly_prediction.post("/predict")
def predict(data: dict):
    """ Predict hospitalization based on input data. """
    prediction, probability = predict_hospitalization(data)
    return {"prediction": prediction, "probability": probability}
