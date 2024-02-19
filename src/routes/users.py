from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel

import src.models as models
import src.utils.exceptions as exceptions
from src.database import get_db

from src.middlewares.auth import auth_required

router = APIRouter()


class CreateUserModel(BaseModel):
    firstname: str
    lastname: str
    mail: str
    password: str


@router.get("/")
@auth_required
def get_users(request: Request, db: Session = Depends(get_db)):
    return db.query(models.Users).all()


@router.get("/{user_id}")
@auth_required
def get_user(user_id: int, request: Request, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id == user_id).first()
    print(user.login)
    if user is None:
        raise exceptions.notFound()
    return user


@router.post("/", status_code=201)
@auth_required
def create_user(body: CreateUserModel, request: Request, db: Session = Depends(get_db)):
    db.add(
        models.Users(
            firstname=body.firstname,
            lastname=body.lastname,
            password=body.password,
            mail=body.mail,
        )
    )
    db.commit()


@router.delete("/{user_id}", status_code=204)
@auth_required
def delete_user(user_id: int, request: Request, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id == user_id).first()
    if user is None:
        raise exceptions.notFound()

    db.delete(user)
    db.commit()
