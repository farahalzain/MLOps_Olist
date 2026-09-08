import joblib
import pandas as pd

from src.olist_ml.config import get_path, load_config
from src.olist_ml.features import build_features
from src.olist_ml.preprocessing import preprocess
from src.olist_ml.validation import validate_input


def load_model():
    """Load the fitted final model."""
    model = joblib.load(get_path("model"))

    return model

def predict(df: pd.DataFrame) -> pd.DataFrame:
    """Predict late-delivery probability for new orders."""

    # 1. Validate raw input
    validate_input(df)

    # 2. Create engineered features
    engineered_df = build_features(df)

    # 3. Apply fitted preprocessing
    model_input = preprocess(engineered_df)

    # 4. Load the fitted model
    model = load_model()

    # 5. Get the probability of class 1 = Late
    late_class_index = list(model.classes_).index(1)

    late_probability = model.predict_proba(model_input)[:, late_class_index]

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

    return results