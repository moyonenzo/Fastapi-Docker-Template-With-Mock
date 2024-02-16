from fastapi.testclient import TestClient
from src.tests import app
from src.tests.datasets import dataset

from sqlalchemy import select
from src.models import Users

client = TestClient(app)


def test_get_users(dataset):
    url = "/users"

    response = client.get(url)
    result = dataset.session.scalars(select(Users)).all()
    assert response.status_code == 200
    assert {item["id"] for item in response.json()} == {item.id for item in result}


def test_get_user(dataset):
    url = f"/users/{dataset.user_1.id}"

    response = client.get(url)
    result = dataset.session.scalars(
        select(Users).where(Users.id == dataset.user_1.id)
    ).first()
    assert response.status_code == 200
    assert response.json()["id"] == result.id


def test_create_user(dataset):
    url = "/users"
    data = {"firstname": "Alex", "lastname": "Terieur", "password": "XXXX"}

    response = client.post(url, json=data)
    result = dataset.session.scalars(
        select(Users)
        .where(Users.firstname == data["firstname"])
        .where(Users.lastname == data["lastname"])
    ).first()
    assert response.status_code == 201
    assert result is not None


def test_delete_user(dataset):
    url = f"/users/{dataset.user_1.id}"

    response = client.delete(url)
    result = dataset.session.scalars(
        select(Users).where(Users.id == dataset.user_1.id)
    ).first()
    assert response.status_code == 204
    assert result is None
