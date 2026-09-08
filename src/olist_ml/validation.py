import pandas as pd


REQUIRED_COLUMNS = [
    "customer_state",
    "seller_states",
    "total_price",
    "total_freight",
    "item_count",
    "total_payment",
    "payment_installments",
    "payment_count",
    "seller_count",
    "seller_state_count",
    "distance_km",
    "order_purchase_timestamp",
    "order_approved_at",
    "order_estimated_delivery_date",
]


def validate_input(df: pd.DataFrame) -> None:
    """Validate that required input columns are present."""

    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {', '.join(missing_columns)}"
        )