from fastapi.testclient import TestClient

from app.main import app
import app.main as main_module
import pandas as pd

client = TestClient(app)


VALID_ORDER = {
    "order_purchase_timestamp": "2018-06-21T08:41:07",
    "order_approved_at": "2018-06-22T02:59:29",
    "order_estimated_delivery_date": "2018-07-04T00:00:00",
    "customer_state": "SP",
    "seller_states": "SP",
    "total_price": 55.0,
    "total_freight": 7.65,
    "item_count": 1,
    "total_payment": 62.65,
    "payment_installments": 1,
    "payment_count": 1,
    "seller_count": 1,
    "seller_state_count": 1,
    "distance_km": 10.814251140678918,
}


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_model_info_endpoint():
    response = client.get("/model-info")
    assert response.status_code == 200
    data = response.json()

    assert data["model_name"] == "olist-late-delivery-model"
    assert data["model_version"] == "1"


def test_predict_endpoint(monkeypatch):
    def mock_predict(input_df):
        return pd.DataFrame(
            [{
                "prediction": 0,
                "label": "On Time",
                "late_probability": 0.2,
                "model_version": "1",
            }]
        )

    monkeypatch.setattr(main_module, "predict", mock_predict)

    response = client.post("/predict", json=VALID_ORDER)

    assert response.status_code == 200

    data = response.json()

    assert data["prediction"] == 0
    assert data["label"] == "On Time"
    assert data["late_probability"] == 0.2
    assert data["model_version"] == "1"


def test_predict_batch_endpoint(monkeypatch):
    def mock_predict(input_df):
        return pd.DataFrame(
            [
                {
                    "prediction": 0,
                    "label": "On Time",
                    "late_probability": 0.2,
                    "model_version": "1",
                }
                for _ in range(len(input_df))
            ]
        )

    monkeypatch.setattr(main_module, "predict", mock_predict)

    response = client.post(
        "/predict-batch",
        json={"orders": [VALID_ORDER, VALID_ORDER]},
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data["predictions"]) == 2

    for prediction in data["predictions"]:
        assert prediction["prediction"] == 0
        assert prediction["label"] == "On Time"
        assert prediction["late_probability"] == 0.2
        assert prediction["model_version"] == "1"

def test_predict_rejects_invalid_input():
    invalid_order = VALID_ORDER.copy()
    invalid_order["total_price"] = -100

    response = client.post(
        "/predict",
        json=invalid_order,
    )

    assert response.status_code == 422