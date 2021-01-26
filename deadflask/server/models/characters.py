from sqlalchemy import Column, Integer, String, Boolean, Index, ForeignKey
from sqlalchemy.orm import relationship

from deadflask.server.dbcore import Base


class CharacterType(Base):
    __tablename__ = "character_types"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    description = Column(String)


class Character(Base):
    __tablename__ = "characters"

    # Identity Fields
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    city = Column(Integer, ForeignKey('cities.id'))
    coord_x = Column(Integer)
    coord_y = Column(Integer)
    type = relationship("CharacterType")
    user = relationship("User")

    # Current State Fields
    health = Column(Integer)
    experience = Column(Integer)
    is_bot = Column(Boolean, default=False)
    is_inside = Column(Boolean, default=False)

    # TODO Inventory
    # TODO Message Log

    _index_coords = Index('idx_coordinates', coord_x, coord_y)

    @classmethod
    def create(cls, name, character_type, user=None):
        if user:
            return Character(name=name, type=character_type, user=user)
        else:
            return Character(name=name, type=character_type, is_bot=True)

    def __repr__(self):
        if self.is_bot:
            return f"<BotCharacter(name='{self.name}')>"
        else:
            return f"<Character(name='{self.name}')>"

    def __str__(self):
        return self.name
