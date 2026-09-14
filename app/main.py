import pandas as pd

from fastapi import FastAPI, HTTPException
from app.schemas import (BatchPredictionRequest, BatchPredictionResponse, OrderRequest, PredictionResponse,)

from src.olist_ml.config import load_config
from src.olist_ml.inference import predict


app = FastAPI(
    title="Olist Late Delivery API",
    description="API for predicting whether an Olist order will be delivered late.",
    version="1.0.0",)


@app.get("/health")
def health_check():
    """Check whether the API service is running."""

    return {"status": "healthy",}


@app.get("/model-info")
def model_info():
    "Return information about the model used by the API"

    config = load_config()

    return{
        "model_name": config["mlflow"]["model_name"],
        "model_version": str(config["mlflow"]["model_version"]),
    }


@app.post("/predict", response_model=PredictionResponse)
def predict_order(order:OrderRequest):
    """Predict whether a single order will be delivered late."""

    try:
        input_df = pd.DataFrame([order.model_dump()]) 
        result = predict(input_df)
        prediction = result.iloc[0]
        return {
            "prediction": int(prediction["prediction"]),
            "label": prediction["label"],
            "late_probability": float(prediction["late_probability"]),
            "model_version": str(prediction["model_version"]),
        }

    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc),) from exc
    
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Prediction failed.",) from exc


@app.post("/predict-batch", response_model=BatchPredictionResponse,)
def predict_batch(batch: BatchPredictionRequest):
    """Predict late delivery for multiple orders."""

    try:
        input_df = pd.DataFrame([order.model_dump() for order in batch.orders])
        results = predict(input_df)
        predictions = []

        for _, row in results.iterrows():
            predictions.append(
                {
                "prediction": int(row["prediction"]),
                "label": row["label"],
                "late_probability": float(
                    row["late_probability"]),

                "model_version": str(
                    row["model_version"]
                ),
                }
            )

        return {"predictions": predictions,}

    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc),) from exc

    except Exception as exc:
        raise HTTPException(status_code=500, detail="Batch prediction failed.",) from exc