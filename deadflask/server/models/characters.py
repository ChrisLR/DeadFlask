from sqlalchemy import Column, Integer, String, Boolean, Index, ForeignKey, BigInteger, DateTime
from sqlalchemy.orm import relationship

from deadflask.server.dbcore import Base
from deadflask.server.app import app


class CharacterType(Base):
    __tablename__ = "character_types"

    id = Column(Integer, primary_key=True, index=True)
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
    logs = relationship("CharacterLog")
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
    def create(cls, name, character_type, user=None):
        session = app.db_session
        city = session.query().first()
        if user:
            character = Character(name=name, type=character_type.id, user=user.id, city=city.id)
        else:
            character = Character(name=name, type=character_type.id, is_bot=True, city=city.id)

        session.add(character)

        return character

    @classmethod
    def exists(cls, name):
        character = app.db_session.query(Character).filter_by(name=name).one_or_none()
        return bool(character)

    @classmethod
    def get_at_building(cls, building, inside):
        characters = app.db_session.query(Character).filter(
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


class CharacterLog(Base):
    __tablename__ = "character_logs"

    id = Column(BigInteger, primary_key=True, index=True)
    character = Column(Integer, ForeignKey('characters.id'), index=True)
    count = Column(Integer)
    has_read = Column(Boolean)
    message = Column(String)
    timestamp = Column(DateTime)

    _index_character_and_read = Index('idx_character_and_read', character, has_read)
