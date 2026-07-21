from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


def test_home():
    response = client.get("/")
    assert response.status_code == 200


def test_health():
    response = client.get("/health")
    assert response.status_code == 200


def test_chat():
    response = client.post(
        "/chat",
        json={
            "message": "Hello"
        }
    )

    assert response.status_code == 200
    assert "response" in response.json()


def test_empty_message():

    response = client.post(
        "/chat",
        json={
            "message": ""
        }
    )

    assert response.status_code == 400


def test_history():

    response = client.get("/history")

    assert response.status_code == 200


def test_clear():

    response = client.post("/clear")

    assert response.status_code == 200