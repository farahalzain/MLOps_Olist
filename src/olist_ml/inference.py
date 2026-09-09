import logging
import joblib
import pandas as pd

from src.olist_ml.config import get_path, load_config
from src.olist_ml.features import build_features
from src.olist_ml.preprocessing import preprocess
from src.olist_ml.validation import validate_input
from src.olist_ml.logging_config import setup_logging

setup_logging()

logger = logging.getLogger(__name__)

def load_model():
    """Load the fitted final model."""

    logger.info("Loading final model")

    model = joblib.load(get_path("model"))

    logger.info("Final model loaded successfully")

    return model

def predict(df: pd.DataFrame) -> pd.DataFrame:
    """Predict late-delivery probability for new orders."""

    logger.info("Starting inference for %d order(s)", len(df))

    try:
        # 1. Validate raw input
        validate_input(df)
        logger.info("Input validation passed")

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
        model = load_model()

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
            }
        )

        logger.info("Inference completed successfully")

        return results

    except Exception:
        logger.exception("Inference failed")
        raise