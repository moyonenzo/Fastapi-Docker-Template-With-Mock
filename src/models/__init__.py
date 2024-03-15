from sqlalchemy import ForeignKey, Column, Integer, String
from sqlalchemy.orm import relationship
from src.database import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    lastname = Column(String(255))
    firstname = Column(String(255))
    mail = Column(String(255), unique=True)
    password = Column(String(255))

    _roles = relationship("UserHasRoles", viewonly=True)

    @property
    def roles(self):
        return [object.role for object in self._roles]


class Roles(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True)


class UserHasRoles(Base):
    __tablename__ = "user_has_roles"

    user_id = Column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    role_id = Column(
        ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True, index=True
    )

    user = relationship("Users")
    role = relationship("Roles")
