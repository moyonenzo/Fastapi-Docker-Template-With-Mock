import pytest
import src.models as models


class Dataset:
    def __init__(self, session):
        self.session = session

    def create_categories(self, label: str) -> models.Categories:
        category = models.Categories(label=label)
        self.session.add(category)
        return category


@pytest.fixture
def dataset(session):
    ds = Dataset(session)
    ds.category_1 = ds.create_categories("first_category")

    ds.session.commit()
