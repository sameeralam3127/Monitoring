import os

os.environ["OTEL_SDK_DISABLED"] = "true"

import app as demo_app


def test_health_endpoint_returns_healthy_status():
    client = demo_app.app.test_client()

    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json() == {"status": "healthy"}


def test_index_endpoint_returns_service_status_and_latency(monkeypatch):
    client = demo_app.app.test_client()
    monkeypatch.setattr(demo_app.random, "uniform", lambda *_args: 0)
    monkeypatch.setattr(demo_app.time, "sleep", lambda *_args: None)

    response = client.get("/")
    payload = response.get_json()

    assert response.status_code == 200
    assert payload["service"] == "python-observability-demo"
    assert payload["status"] == "ok"
    assert isinstance(payload["latency_seconds"], float)
    assert payload["latency_seconds"] >= 0
