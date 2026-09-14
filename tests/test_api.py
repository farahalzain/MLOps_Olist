from fastapi.testclient import TestClient

from app.main import app


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


def test_predict_endpoint():
    response = client.post("/predict",json=VALID_ORDER,)

    assert response.status_code == 200

    data = response.json()

    assert data["prediction"] in [0, 1]
    assert data["label"] in ["Late", "On Time"]
    assert 0 <= data["late_probability"] <= 1
    assert data["model_version"] == "1"


def test_predict_batch_endpoint():
    response = client.post("/predict-batch",
                           json={"orders": [VALID_ORDER, VALID_ORDER,]},)

    assert response.status_code == 200

    data = response.json()

    assert len(data["predictions"]) == 2

    for prediction in data["predictions"]:
        assert prediction["prediction"] in [0, 1]
        assert prediction["label"] in ["Late", "On Time"]
        assert 0 <= prediction["late_probability"] <= 1
        assert prediction["model_version"] == "1"


def test_predict_rejects_invalid_input():
    invalid_order = VALID_ORDER.copy()
    invalid_order["total_price"] = -100

    response = client.post("/predict", json=invalid_order,)

    assert response.status_code == 422