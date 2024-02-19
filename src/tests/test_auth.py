from fastapi.testclient import TestClient
from src.tests import app
from src.tests.datasets import dataset
from src.utils.webtokens import logged_as

from sqlalchemy import select
from src.models import Users

client = TestClient(app)


def test_get_identity(dataset):
    url = "/auth"

    response = client.get(url)
    assert response.status_code == 403

    with logged_as(client, dataset.user_1):
        response = client.get(url)
        result = dataset.session.scalars(select(Users).where(Users.id == dataset.user_1.id)).first()
        assert response.status_code == 200
        assert response.json()['id'] == result.id == dataset.user_1.id


def test_authenticate(dataset):
    url = "/auth"
    data = {"mail": dataset.user_1.mail, "password": dataset.user_1.password}

    response = client.post(url)
    assert response.status_code == 422

    response = client.post(url, json=data)
    assert response.status_code == 200

    response = client.get(url)
    assert response.status_code == 200


def test_logout(dataset):
    url = "/auth"

    client.cookies = None
    response = client.delete(url)
    assert response.status_code == 403

    with logged_as(client, dataset.user_1):
        response = client.delete(url)
        assert response.status_code == 204
