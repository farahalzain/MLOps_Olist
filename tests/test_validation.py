import pandas as pd
import pytest

from src.olist_ml.validation import validate_input


def test_validate_input_passes_with_required_columns():
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
            "order_purchase_timestamp": ["2018-06-21 08:41:07"],
            "order_approved_at": ["2018-06-21 09:00:00"],
            "order_estimated_delivery_date": ["2018-07-01 00:00:00"],
        }
    )

    validate_input(df)

def test_validate_input_raises_error_for_missing_column():
    df = pd.DataFrame(
        {
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
            "order_purchase_timestamp": ["2018-06-21 08:41:07"],
            "order_approved_at": ["2018-06-21 09:00:00"],
            "order_estimated_delivery_date": ["2018-07-01 00:00:00"],
        }
    )

    with pytest.raises(
        ValueError,
        match="Missing required columns: customer_state",
    ):
        validate_input(df)