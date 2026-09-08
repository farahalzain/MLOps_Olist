import joblib
import pandas as pd

from src.olist_ml.config import get_path


NUMERIC_FEATURES = [
    "total_price",
    "total_freight",
    "item_count",
    "total_payment",
    "payment_installments",
    "payment_count",
    "seller_count",
    "seller_state_count",
    "distance_km",
    "purchase_month",
    "purchase_weekday",
    "purchase_hour",
    "approval_time_hours",
    "estimated_delivery_days",
    "is_holiday",
]

CATEGORICAL_FEATURES = [
    "customer_state",
    "seller_states",
]

FEATURES_TO_SCALE = [
    "total_price",
    "total_freight",
    "item_count",
    "total_payment",
    "payment_installments",
    "payment_count",
    "distance_km",
    "approval_time_hours",
    "estimated_delivery_days",
]


def load_preprocessing_artifacts():
    """Load the fitted preprocessing artifacts."""
    numeric_imputer = joblib.load(get_path("numeric_imputer"))
    encoder = joblib.load(get_path("encoder"))
    scaler = joblib.load(get_path("scaler"))
    feature_list = joblib.load(get_path("feature_list"))

    return numeric_imputer, encoder, scaler, feature_list

def preprocess(df: pd.DataFrame) -> pd.DataFrame:
    """Transform engineered order data into model-ready features."""

    numeric_imputer, encoder, scaler, feature_list = (
        load_preprocessing_artifacts()
    )

    df = df.copy()

    # 1. Impute missing numeric values
    df[NUMERIC_FEATURES] = numeric_imputer.transform(
        df[NUMERIC_FEATURES]
    )

    # 2. Encode categorical features
    encoded = encoder.transform(
        df[CATEGORICAL_FEATURES]
    )

    encoded_feature_names = encoder.get_feature_names_out(
        CATEGORICAL_FEATURES
    )

    encoded_df = pd.DataFrame(
        encoded,
        columns=encoded_feature_names,
        index=df.index,
    )

    # 3. Combine numeric and encoded categorical features
    final_df = pd.concat(
        [df[NUMERIC_FEATURES], encoded_df],
        axis=1,
    )

    # 4. Scale the same features used during training
    final_df[FEATURES_TO_SCALE] = scaler.transform(
        final_df[FEATURES_TO_SCALE]
    )

    # 5. Enforce the exact feature order used during training
    final_df = final_df[feature_list]

    return final_df