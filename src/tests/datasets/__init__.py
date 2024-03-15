import pytest
import src.models as models

from sqlalchemy.orm import Session
from src.tests import engine
from src.utils.webtokens import hash_password

from src.database import Base


class Dataset:
    def __init__(self):
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
        self.session: Session = Session(bind=engine)

    def create_user(
        self, firstname: str, lastname: str, mail: str, password: str
    ) -> models.Users:
        user = models.Users(
            firstname=firstname,
            lastname=lastname,
            mail=mail,
            password=hash_password(password),
        )
        self.session.add(user)
        return user

    def create_role(self, name: str) -> models.Roles:
        role = models.Roles(name=name)
        self.session.add(role)
        return role

    def attribute_role_to_user(self, user: models.Users, role: models.Roles):
        user_has_role = models.UserHasRoles(user=user, role=role)
        self.session.add(user_has_role)


@pytest.fixture
def dataset():
    ds = Dataset()
    ds.user_1 = ds.create_user("Alain", "Terieur", "terieur_a@pytest.io", "0000")
    ds.role_admin = ds.create_role("admin")
    ds.attribute_role_to_user(user=ds.user_1, role=ds.role_admin)

    ds.session.commit()
    return ds
