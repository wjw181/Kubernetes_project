from fastapi.testclient import TestClient
# import sys,os
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import app
client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["docs"] == "/docs"
    assert data["health"] == "/health"


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "service" in data
    assert "env" in data
    assert "token_loaded" in data


def test_get_users():
    response = client.get("/users/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_get_user_by_id():
    response = client.get("/users/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1


def test_create_user():
    payload = {
        "name": "Charlie",
        "age": 23,
        "email": "charlie@example.com"
    }
    response = client.post("/users/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Charlie"
    assert data["age"] == 23
    assert data["email"] == "charlie@example.com"
    assert "id" in data


def test_metrics_exists():
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "fastapi_requests_total" in response.text or "python_info" in response.text