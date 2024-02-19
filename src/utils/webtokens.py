from jose import jwt
import src.models as models
import src.utils.exceptions as exception

import os
from dotenv import load_dotenv

load_dotenv()


def create_access_token(user: models.Users):
    data = {"id": user.id, "mail": user.mail}

    encoded = jwt.encode(data, os.getenv("SECRET_KEY"), algorithm="HS256")
    return encoded


def retrieve_access_token(token: str):
    try:
        return jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=["HS256"])
    except jwt.JWTError:
        raise exception.permissionDenied()
