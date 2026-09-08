import holidays
import numpy as np
import pandas as pd


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create model features from order data."""
    df = df.copy()

    date_cols = [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_estimated_delivery_date",
    ]

    for col in date_cols:
        df[col] = pd.to_datetime(df[col])

    df["purchase_month"] = df["order_purchase_timestamp"].dt.month
    df["purchase_weekday"] = df["order_purchase_timestamp"].dt.dayofweek
    df["purchase_hour"] = df["order_purchase_timestamp"].dt.hour

    df["approval_time_hours"] = (
        df["order_approved_at"] - df["order_purchase_timestamp"]
    ).dt.total_seconds() / 3600

    df["estimated_delivery_days"] = (
        df["order_estimated_delivery_date"]
        - df["order_purchase_timestamp"]
    ).dt.total_seconds() / (24 * 3600)

    years = df["order_purchase_timestamp"].dt.year.unique()
    holiday_calendar = holidays.Brazil(years=years)

    df["is_holiday"] = (
        df["order_purchase_timestamp"]
        .dt.date
        .isin(holiday_calendar)
        .astype(int)
    )

    df["seller_states"] = np.where(
        df["seller_state_count"] == 1,
        df["seller_states"],
        "MULTI",
    )

    return df