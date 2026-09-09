import pandas as pd

from src.olist_ml.features import build_features
from src.olist_ml.preprocessing import (
    load_preprocessing_artifacts,
    preprocess,
)


def test_preprocess_returns_model_ready_features():
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

    result = preprocess(engineered_df)

    _, _, _, feature_list = load_preprocessing_artifacts()

    assert result.shape == (1, 65)
    assert result.isna().sum().sum() == 0
    assert result.columns.tolist() == list(feature_list)