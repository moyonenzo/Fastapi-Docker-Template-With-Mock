from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.orm import Session
from pydantic import BaseModel, ConfigDict

import src.models as models
import src.utils.exceptions as exceptions

from src.middlewares.auth import auth_required
from src.utils.webtokens import (
    create_access_token,
    retrieve_access_token,
    verify_password,
)
from src.database import get_db

router = APIRouter()


class AuthenticateModel(BaseModel):
    mail: str
    password: str


class IdentityResponseModel(BaseModel):
    id: int
    firstname: str
    lastname: str
    mail: str


@router.get("/")
@auth_required
def identity(request: Request, db: Session = Depends(get_db)) -> IdentityResponseModel:
    decoded = retrieve_access_token(request.cookies.get("access_token"))
    if decoded is None:
        raise exceptions.internalServerError()

    user = db.query(models.Users).where(models.Users.id == decoded["id"]).first()
    if user is None:
        raise exceptions.notFound()

    return IdentityResponseModel.model_validate(user, from_attributes=True)


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

    if verify_password(body.password, user.password):
        raise exceptions.permissionDenied()

    response.set_cookie(
        key="access_token", value=create_access_token(user), max_age=300
    )


@router.delete("/", status_code=204)
@auth_required
def logout(request: Request, response: Response):
    response.delete_cookie("access_token")
