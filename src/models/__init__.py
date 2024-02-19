from sqlalchemy import Column, Integer, String, cast
from src.database import Base


class Categories(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    label = Column(String(255))


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    lastname = Column(String(255))
    firstname = Column(String(255))
    mail = Column(String(255))
    password = Column(String(255))
