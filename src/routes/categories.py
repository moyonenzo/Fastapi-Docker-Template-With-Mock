from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel

import src.models as models
import src.utils.exceptions as exceptions
from src.database import get_db

from src.middlewares.auth import auth_required

router = APIRouter()


class CreateCategoryModel(BaseModel):
    label: str


@router.get("/")
@auth_required
def get_categories(request: Request, db: Session = Depends(get_db)):
    return db.query(models.Categories).all()


@router.get("/{category_id}")
@auth_required
def get_category(category_id: int, request: Request, db: Session = Depends(get_db)):
    category = (
        db.query(models.Categories).filter(models.Categories.id == category_id).first()
    )
    if category is None:
        raise exceptions.notFound()
    return category


@router.post("/", status_code=201)
@auth_required
def create_category(
    body: CreateCategoryModel, request: Request, db: Session = Depends(get_db)
):
    category = (
        db.query(models.Categories).filter(models.Categories.label == body.label).all()
    )
    if len(category) > 0:
        raise exceptions.notFound()
    db.add(models.Categories(label=body.label))
    db.commit()


@router.delete("/{category_id}", status_code=204)
@auth_required
def delete_category(category_id: int, request: Request, db: Session = Depends(get_db)):
    category = (
        db.query(models.Categories).filter(models.Categories.id == category_id).first()
    )
    if category is None:
        raise exceptions.notFound()

    db.delete(category)
    db.commit()
