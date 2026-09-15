import pandas as pd

from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler

import src.olist_ml.preprocessing as preprocessing_module

from src.olist_ml.features import build_features
from src.olist_ml.preprocessing import (
    CATEGORICAL_FEATURES,
    FEATURES_TO_SCALE,
    NUMERIC_FEATURES,
    preprocess,)


def test_preprocess_returns_model_ready_features(monkeypatch):
    df = pd.DataFrame(
        {
            "customer_state": ["SP"],
            "seller_states": ["SP"],
            "total_price": [100.0],
            "total_freight": [10.0],
            "item_count": [1],
            "total_payment": [110.0],
            "payment_installments": [1],
            "payment_count": [1],
            "seller_count": [1],
            "seller_state_count": [1],
            "distance_km": [20.0],
            "order_purchase_timestamp": ["2018-06-21 08:00:00"],
            "order_approved_at": ["2018-06-21 10:00:00"],
            "order_estimated_delivery_date": ["2018-07-01 08:00:00"],
        }
    )

    engineered_df = build_features(df)

    numeric_imputer = SimpleImputer(strategy="median")
    numeric_imputer.fit(engineered_df[NUMERIC_FEATURES])

    encoder = OneHotEncoder(
        handle_unknown="ignore",
        sparse_output=False,
    )
    encoder.fit(engineered_df[CATEGORICAL_FEATURES])

    imputed_numeric = engineered_df[NUMERIC_FEATURES].copy()
    imputed_numeric[NUMERIC_FEATURES] = numeric_imputer.transform(
        engineered_df[NUMERIC_FEATURES]
    )

    scaler = StandardScaler()
    scaler.fit(imputed_numeric[FEATURES_TO_SCALE])

    encoded_feature_names = encoder.get_feature_names_out(
        CATEGORICAL_FEATURES
    )

    feature_list = list(NUMERIC_FEATURES) + list(
        encoded_feature_names
    )

    def mock_load_preprocessing_artifacts():
        return numeric_imputer, encoder, scaler, feature_list

    monkeypatch.setattr(
        preprocessing_module,
        "load_preprocessing_artifacts",
        mock_load_preprocessing_artifacts,
    )

    result = preprocess(engineered_df)

    assert result.shape[0] == 1
    assert result.isna().sum().sum() == 0
    assert result.columns.tolist() == feature_list