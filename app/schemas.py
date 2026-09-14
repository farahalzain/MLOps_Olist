from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class OrderRequest(BaseModel):
    """Input schema for a single order prediction."""

    order_purchase_timestamp: datetime
    order_approved_at: datetime
    order_estimated_delivery_date: datetime

    customer_state: str = Field(min_length=2, max_length=2)
    seller_states: str

    total_price: float = Field(ge=0)
    total_freight: float = Field(ge=0)
    item_count: int = Field(ge=1)

    total_payment: float = Field(ge=0)
    payment_installments: int = Field(ge=0)
    payment_count: int = Field(ge=1)

    seller_count: int = Field(ge=1)
    seller_state_count: int = Field(ge=1)

    distance_km: float = Field(ge=0)


class PredictionResponse(BaseModel):
    """Output schema for a prediction."""

    prediction: int
    label: Literal["Late", "On Time"]
    late_probability: float = Field(ge=0, le=1)
    model_version: str

class BatchPredictionRequest(BaseModel):
    """Input schema for batch predictions."""

    orders: list[OrderRequest]


class BatchPredictionResponse(BaseModel):
    """Output schema for batch predictions."""

    predictions: list[PredictionResponse]