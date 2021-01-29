from sqlalchemy import Column, Integer, String, Boolean, Index, ForeignKey

from deadflask.server.dbcore import Base
from deadflask.server.models.cities import City


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
    coord_x = Column(Integer, default=0)
    coord_y = Column(Integer, default=0)
    type = Column(Integer, ForeignKey('character_types.id'))
    user = Column(Integer, ForeignKey('users.id'))

    # Current State Fields
    health = Column(Integer, default=50)
    experience = Column(Integer, default=0)
    is_bot = Column(Boolean, default=False)
    is_inside = Column(Boolean, default=False)

    # TODO Inventory
    # TODO Message Log

    _index_coords = Index('idx_character_coordinates', coord_x, coord_y)

    @classmethod
    def create(cls, app, name, character_type, user=None):
        city = app.db_session.query(City).first()
        if user:
            character = Character(name=name, type=character_type.id, user=user.id, city=city.id)
        else:
            character = Character(name=name, type=character_type.id, is_bot=True, city=city.id)

        app.db_session.add(character)

        return character

    @classmethod
    def exists(cls, app, name):
        character = app.db_session.query(Character).filter_by(name=name).one_or_none()
        return bool(character)

    def __repr__(self):
        if self.is_bot:
            return f"<BotCharacter(name='{self.name}')>"
        else:
            return f"<Character(name='{self.name}')>"

    def __str__(self):
        return self.name
