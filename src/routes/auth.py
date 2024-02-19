from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy import select
from sqlalchemy.orm import Session
from pydantic import BaseModel

import src.models as models
import src.utils.exceptions as exceptions

from src.middlewares.auth import auth_required
from src.utils.webtokens import create_access_token
from src.database import get_db

router = APIRouter()


class AuthenticateModel(BaseModel):
    mail: str
    password: str


@router.post("/")
def authenticate(
    body: AuthenticateModel,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    user = db.query(models.Users).filter(models.Users.mail == body.mail).first()

    if user is None:
        raise exceptions.notFound()

    if user.password != body.password:
        raise exceptions.permissionDenied()

    response.set_cookie(
        key="access_token", value=create_access_token(user), max_age=300
    )


@router.delete("/")
@auth_required
def logout(request: Request, response: Response):
    response.delete_cookie("access_token")
