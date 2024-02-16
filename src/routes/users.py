from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

import src.models as models
import src.utils.exceptions as exceptions
from src.database import get_db

router = APIRouter()


class CreateUserModel(BaseModel):
    firstname: str
    lastname: str
    password: str


@router.get("/")
def get_users(db: Session = Depends(get_db)):
    return db.query(models.Users).all()


@router.get("/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = (
        db.query(models.Users).filter(models.Users.id == user_id).first()
    )
    if user is None:
        raise exceptions.notFound()
    return user


@router.post("/", status_code=201)
def create_user(body: CreateUserModel, db: Session = Depends(get_db)):
    db.add(models.Users(
        firstname=body.firstname,
        lastname=body.lastname,
        password=body.password
    ))
    db.commit()


@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = (
        db.query(models.Users).filter(models.Users.id == user_id).first()
    )
    if user is None:
        raise exceptions.notFound()

    db.delete(user)
    db.commit()
