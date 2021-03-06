from deadflask.server.dbcore import Base
from sqlalchemy import Column, Integer, String, Boolean, Index, ForeignKey, UniqueConstraint
from deadflask.server.app import app

class BuildingType(Base):
    __tablename__ = "building_types"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    description = Column(String)
    width = Column(Integer, default=1)
    height = Column(Integer, default=1)
    has_outside_doors = Column(Boolean, default=True)
    has_inside_doors = Column(Boolean, default=False)
    has_inside = Column(Boolean, default=True)
    max_per_city = Column(Integer, default=-1)

    def __repr__(self):
        return f"<BuildingType(name='{self.name}')>"

    def __str__(self):
        return self.name


class Building(Base):
    __tablename__ = "buildings"

    # Identity Fields
    id = Column(Integer, primary_key=True)
    name = Column(String)
    city = Column(Integer, ForeignKey('cities.id'), index=True)
    coord_x = Column(Integer)
    coord_y = Column(Integer)
    description = Column(String)
    type = Column(Integer, ForeignKey('building_types.id'), index=True)

    # Current State Fields
    barricade_level = Column(Integer, default=0)
    doors_open = Column(Boolean, default=False)
    inside_blood_level = Column(Integer, default=0)
    outside_blood_level = Column(Integer, default=0)
    power_level = Column(Integer, default=0)
    ruin_level = Column(Integer, default=0)

    _index_coords = Index('idx_coordinates', coord_x, coord_y)
    _unq_name_city = UniqueConstraint(name, city)

    @classmethod
    def get_at(cls, coord_x, coord_y, city):
        return app.db_query(Building).filter_by(coord_x=coord_x, coord_y=coord_y, city=city).one_or_none()
