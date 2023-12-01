from fastapi.testclient import TestClient
from src.tests import app
from src.tests.datasets import dataset

from sqlalchemy import select
from src.models import Categories

client = TestClient(app)


def test_get_categories(dataset):
    url = "/categories"

    response = client.get(url)
    result = dataset.session.scalars(select(Categories)).all()
    assert response.status_code == 200
    assert {item["id"] for item in response.json()} == {item.id for item in result}


def test_get_category(dataset):
    url = f"/categories/{dataset.category_1.id}"

    response = client.get(url)
    result = dataset.session.scalars(
        select(Categories).where(Categories.id == dataset.category_1.id)
    ).first()
    assert response.status_code == 200
    assert response.json()["label"] == result.label


def test_create_category(dataset):
    url = "/categories"
    data = {"label": "voitures"}

    response = client.post(url, json=data)
    result = dataset.session.scalars(
        select(Categories).where(Categories.label == "voitures")
    ).first()
    assert response.status_code == 201
    assert result is not None


def test_delete_category(dataset):
    url = f"/categories/{dataset.category_1.id}"

    response = client.delete(url)
    result = dataset.session.scalars(
        select(Categories).where(Categories.id == dataset.category_1.id)
    ).first()
    assert response.status_code == 204
    assert result is None
