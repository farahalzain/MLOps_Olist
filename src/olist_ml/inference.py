import logging
import pandas as pd
import time
import mlflow
import mlflow.sklearn
import os

from src.olist_ml.config import get_path, load_config
from src.olist_ml.features import build_features
from src.olist_ml.preprocessing import preprocess
from src.olist_ml.validation import validate_input
from src.olist_ml.logging_config import setup_logging
from src.olist_ml.data_quality import validate_data_quality

setup_logging()

logger = logging.getLogger(__name__)

def load_model():
    """Load the registered model from MLflow Model Registry."""

    config = load_config()

    tracking_uri = os.getenv("MLFLOW_TRACKING_URI", config["mlflow"]["tracking_uri"],)

    model_name = os.getenv("MLFLOW_MODEL_NAME", config["mlflow"]["model_name"],)

    model_version = os.getenv("MLFLOW_MODEL_VERSION", str(config["mlflow"]["model_version"]),)

    mlflow.set_tracking_uri(tracking_uri)

    model_uri = f"models:/{model_name}/{model_version}"

    logger.info("Loading registered model | name=%s | version=%s", model_name, model_version,)

    model = mlflow.sklearn.load_model(model_uri)

    logger.info("Registered model loaded successfully")

    return model, model_version


def predict(df: pd.DataFrame) -> pd.DataFrame:
    """Predict late-delivery probability for new orders."""

    start_time = time.perf_counter()

    logger.info("Starting inference for %d order(s)", len(df))
    logger.info("Prediction input | %s", df.to_dict(orient="records"),)

    try:
        # 1. Validate raw input
        validate_input(df)
        logger.info("Input validation passed")

        validate_data_quality(df)
        logger.info("Data quality validation passed")

        # 2. Create engineered features
        engineered_df = build_features(df)
        logger.info("Feature engineering completed")

        # 3. Apply fitted preprocessing
        model_input = preprocess(engineered_df)
        logger.info(
            "Preprocessing completed with shape %s",
            model_input.shape,
        )

        # 4. Load the fitted model
        model, model_version = load_model()

        # 5. Get the probability of class 1 = Late
        late_class_index = list(model.classes_).index(1)

        late_probability = model.predict_proba(model_input)[
            :, late_class_index
        ]

        # 6. Load prediction threshold from configuration
        config = load_config()
        threshold = config["model"]["prediction_threshold"]

        # 7. Convert probability into a class prediction
        predictions = (late_probability >= threshold).astype(int)

        # 8. Create readable output
        results = pd.DataFrame(
            {
                "prediction": predictions,
                "label": [
                    "Late" if prediction == 1 else "On Time"
                    for prediction in predictions
                ],
                "late_probability": late_probability,
                "model_version": model_version,
            }
        )

        logger.info("Inference completed successfully")

        latency = time.perf_counter() - start_time

        logger.info("Prediction completed | input_rows=%d | output=%s | latency=%.4fs | model_version=%s",
            len(df),results.to_dict(orient="records"),latency, model_version)
        
        return results

    except Exception:
        logger.exception("Inference failed")
        raise