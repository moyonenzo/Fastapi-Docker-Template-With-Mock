from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

import src.models as models
import src.utils.exceptions as exceptions
from src.database import get_db

router = APIRouter()


class CreateCategoryModel(BaseModel):
    label: str


@router.get("/")
def get_categories(db: Session = Depends(get_db)):
    return db.query(models.Categories).all()


@router.get("/{category_id}")
def get_category(category_id: int, db: Session = Depends(get_db)):
    category = (
        db.query(models.Categories).filter(models.Categories.id == category_id).first()
    )
    if category is None:
        raise exceptions.notFound()
    return category


@router.post("/", status_code=201)
def create_category(body: CreateCategoryModel, db: Session = Depends(get_db)):
    category = (
        db.query(models.Categories).filter(models.Categories.label == body.label).all()
    )
    if len(category) > 0:
        raise exceptions.notFound()
    db.add(models.Categories(label=body.label))
    db.commit()


@router.delete("/{category_id}", status_code=204)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    category = (
        db.query(models.Categories).filter(models.Categories.id == category_id).first()
    )
    if category is None:
        raise exceptions.notFound()

    db.delete(category)
    db.commit()
