from fastapi.testclient import TestClient
from src.tests import app

client = TestClient(app)


def test_get_categories():
    url = "/categories"

    response = client.get(url)
    assert response.status_code == 200
    assert response.json() == []


def test_get_category():
    url = "/categories/1"

    response = client.get(url)
    assert response.status_code == 404


def test_create_category():
    url = "/categories"
    data = {"label": "voitures"}

    response = client.post(url, json=data)
    assert response.status_code == 201


def test_delete_category():
    url = "/categories/1"

    response = client.delete(url)
    assert response.status_code == 204
