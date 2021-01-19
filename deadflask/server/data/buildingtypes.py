from deadflask.server.models.buildings import BuildingType


building_types = [
    BuildingType(name="Bank"),
    BuildingType(name="Building"),
    BuildingType(name="Church"),
    BuildingType(name="Cinema"),
    BuildingType(name="Club"),
    BuildingType(name="Factory"),
    BuildingType(name="Fire Station"),
    BuildingType(name="Hospital"),
    BuildingType(name="Hotel"),
    BuildingType(name="Junkyard"),
    BuildingType(name="Library"),
    BuildingType(name="Museum"),
    BuildingType(name="Police Department"),
    BuildingType(name="Public House"),
    BuildingType(name="Railway Station"),
    BuildingType(name="School"),
    BuildingType(name="Street", has_inside=False),
    BuildingType(name="Tower"),
    BuildingType(name="Warehouse"),
]
