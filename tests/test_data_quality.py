import pandas as pd
import pytest

from src.olist_ml.data_quality import validate_data_quality


def make_valid_data():
    return pd.DataFrame({
            "customer_state": ["SP"],
            "total_price": [100.0],
            "total_freight": [10.0],
            "item_count": [1],
            "distance_km": [20.0],})


def test_data_quality_passes_for_valid_data():
    df = make_valid_data()
    assert validate_data_quality(df) is True


def test_data_quality_fails_for_negative_price():
    df = make_valid_data()
    df.loc[0, "total_price"] = -100

    with pytest.raises(ValueError, match="Data quality validation failed"):
        validate_data_quality(df)


def test_data_quality_fails_for_invalid_customer_state():
    df = make_valid_data()
    df.loc[0, "customer_state"] = "XX"

    with pytest.raises(ValueError, match="Data quality validation failed",):
        validate_data_quality(df)