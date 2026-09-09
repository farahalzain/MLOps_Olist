import pandas as pd

from src.olist_ml.features import build_features


def test_build_features_creates_expected_features():
    df = pd.DataFrame(
        {
            "order_purchase_timestamp": ["2018-06-21 08:00:00"],
            "order_approved_at": ["2018-06-21 10:00:00"],
            "order_estimated_delivery_date": ["2018-07-01 08:00:00"],
            "seller_state_count": [1],
            "seller_states": ["SP"],
        }
    )

    result = build_features(df)

    assert result["purchase_month"].iloc[0] == 6
    assert result["purchase_weekday"].iloc[0] == 3
    assert result["purchase_hour"].iloc[0] == 8
    assert result["approval_time_hours"].iloc[0] == 2.0
    assert result["estimated_delivery_days"].iloc[0] == 10.0
    assert result["seller_states"].iloc[0] == "SP"

def test_build_features_sets_multi_seller_state():
    df = pd.DataFrame(
        {
            "order_purchase_timestamp": ["2018-06-21 08:00:00"],
            "order_approved_at": ["2018-06-21 10:00:00"],
            "order_estimated_delivery_date": ["2018-07-01 08:00:00"],
            "seller_state_count": [2],
            "seller_states": ["SP,RJ"],
        }
    )

    result = build_features(df)

    assert result["seller_states"].iloc[0] == "MULTI"