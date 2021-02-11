from sqlalchemy import Column, Integer, String, Boolean, Index, ForeignKey, BigInteger, DATETIME

from deadflask.server.dbcore import Base
from deadflask.server.models.cities import City
from sqlalchemy.orm import relationship


class CharacterType(Base):
    __tablename__ = "character_types"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    description = Column(String)


class Character(Base):
    __tablename__ = "characters"

    # Identity Fields
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    city = Column(Integer, ForeignKey('cities.id'), index=True)
    coord_x = Column(Integer, default=0)
    coord_y = Column(Integer, default=0)
    type = Column(Integer, ForeignKey('character_types.id'))
    type = Column(Integer, ForeignKey('character_types.id'), index=True)
    user = Column(Integer, ForeignKey('users.id'), index=True)

    # Current State Fields
    health = Column(Integer, default=50)
    experience = Column(Integer, default=0)
    is_bot = Column(Boolean, default=False)
    is_inside = Column(Boolean, default=False)

    # TODO Inventory
    # TODO Message Log

    _index_coords = Index('idx_character_coordinates', coord_x, coord_y)

    @classmethod
    def create(cls, session, name, character_type, user=None):
        city = session.query().first()
        if user:
            character = Character(name=name, type=character_type.id, user=user.id, city=city.id)
        else:
            character = Character(name=name, type=character_type.id, is_bot=True, city=city.id)

        session.add(character)

        return character

    @classmethod
    def exists(cls, session, name):
        character = session.query(Character).filter_by(name=name).one_or_none()
        return bool(character)

    @classmethod
    def get_at_building(cls, session, building, inside):
        characters = session.query(Character).filter(
            Character.coord_x == building.coord_x,
            Character.coord_y == building.coord_y,
            Character.city == building.city,
            Character.type == CharacterType.id,
            Character.is_inside == inside
        )

        return characters

    def __repr__(self):
        if self.is_bot:
            return f"<BotCharacter(name='{self.name}')>"
        else:
            return f"<Character(name='{self.name}')>"

    def __str__(self):
        return self.name
