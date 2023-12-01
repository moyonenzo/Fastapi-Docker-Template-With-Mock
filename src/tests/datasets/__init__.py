import pytest
import src.models as models

from sqlalchemy.orm import Session
from src.tests import engine


class Dataset:
    def __init__(self):
        self.session: Session = Session(bind=engine)

    def create_categories(self, label: str) -> models.Categories:
        category = models.Categories(label=label)
        self.session.add(category)
        return category


@pytest.fixture
def dataset():
    ds = Dataset()
    ds.category_1 = ds.create_categories("first_category")

    ds.session.commit()
    return ds
