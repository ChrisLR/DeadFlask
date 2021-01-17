from deadflask.server.dbcore import Base
from sqlalchemy import Column, Integer, String, Boolean, Index, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship


class BuildingType(Base):
    __tablename__ = "building_types"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    description = Column(String)
    width = Column(Integer, default=1)
    height = Column(Integer, default=1)
    has_outside_doors = Column(Boolean, default=True)
    has_inside_doors = Column(Boolean, default=False)
    max_per_city = Column(Integer, default=-1)
    buildings = relationship("Building")

    def __repr__(self):
        return f"<BuildingType(name='{self.name}')>"

    def __str__(self):
        return self.name


class Building(Base):
    __tablename__ = "buildings"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    coord_x = Column(Integer)
    coord_y = Column(Integer)
    city = Column(Integer, ForeignKey('cities.id'))
    type = Column(Integer, ForeignKey('building_types.id'))

    _index_coords = Index('idx_coordinates', coord_x, coord_y)
    _unq_name_city = UniqueConstraint(name, city)
