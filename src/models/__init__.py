from sqlalchemy import Column, Integer, VARCHAR
from src.database import Base


class Categories(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    label = Column(VARCHAR(255))
