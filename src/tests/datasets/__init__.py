import pytest
import src.models as models

from sqlalchemy.orm import Session
from src.tests import engine


class Dataset:
    def __init__(self):
        self.session: Session = Session(bind=engine)

    def create_category(self, label: str) -> models.Categories:
        category = models.Categories(label=label)
        self.session.add(category)
        return category

    def create_user(
        self, firstname: str, lastname: str, mail: str, password: str
    ) -> models.Users:
        user = models.Users(
            firstname=firstname, lastname=lastname, mail=mail, password=password
        )
        self.session.add(user)
        return user


@pytest.fixture
def dataset():
    ds = Dataset()
    ds.category_1 = ds.create_category("first_category")
    ds.user_1 = ds.create_user("Alain", "Terieur", "terieur_a@pytest.io", "0000")

    ds.session.commit()
    return ds
