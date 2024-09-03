"""
main Elderly Hospitalization Prediction
"""
from fastapi import FastAPI
from routers import hospitalization

app = FastAPI(title="Elderly Hospitalization Prediction")

@app.get("/")
def home_page():
    """
    Home page of the Elderly Hospitalization Prediction service.
    """
    return {"page": "home", "version": "1.0", "update_date": "2023-03-04"}

# Include the router for elderly hospitalization prediction
app.include_router(hospitalization.elderly_prediction)
