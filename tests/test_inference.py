import numpy as np
import pandas as pd

import src.olist_ml.inference as inference_module

from src.olist_ml.inference import predict


class MockModel:
    classes_ = np.array([0, 1])

    def predict_proba(self, X):
        return np.array([[0.3, 0.7] for _ in range(len(X))])


def test_predict_returns_expected_output(monkeypatch):
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

    def mock_preprocess(engineered_df):
        return pd.DataFrame({"feature": [1.0]})

    def mock_load_model():
        return MockModel(), "1"

    monkeypatch.setattr(
        inference_module,
        "preprocess",
        mock_preprocess,
    )

    monkeypatch.setattr(
        inference_module,
        "load_model",
        mock_load_model,
    )

    result = predict(df)

    assert result.shape == (1, 4)

    assert result.columns.tolist() == [
        "prediction",
        "label",
        "late_probability",
        "model_version",
    ]

    assert result["prediction"].iloc[0] == 1
    assert result["label"].iloc[0] == "Late"
    assert result["late_probability"].iloc[0] == 0.7
    assert str(result["model_version"].iloc[0]) == "1"