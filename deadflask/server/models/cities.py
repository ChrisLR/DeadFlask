from deadflask.server.dbcore import Base
from sqlalchemy import Column, Integer, String, Boolean, Index
from sqlalchemy.orm import relationship


class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    buildings = relationship("Building")

    def __repr__(self):
        return f"<City(name='{self.name}')>"

    def __str__(self):
        return self.name
