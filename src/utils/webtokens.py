from fastapi.testclient import TestClient
from jose import jwt
from passlib.context import CryptContext

import src.models as models
import src.utils.exceptions as exception

import os
from dotenv import load_dotenv

load_dotenv()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(user: models.Users):
    data = {"id": user.id, "mail": user.mail}

    encoded = jwt.encode(data, os.getenv("SECRET_KEY"), algorithm="HS256")
    return encoded


def retrieve_access_token(token: str):
    try:
        return jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=["HS256"])
    except jwt.JWTError:
        raise exception.permissionDenied()


def verify_password(password, hashed):
    return pwd_context.verify(password, hashed)


def hash_password(password):
    return pwd_context.hash(password)


class logged_as(object):
    def __init__(self, client: TestClient, user: models.Users):
        self.client = client
        self.token = create_access_token(user)

    def __enter__(self):
        self.client.cookies = {"access_token": self.token}

    def __exit__(self, *args):
        self.client.cookies = None
