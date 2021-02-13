from deadflask.server.app import app
from deadflask.server.models.buildings import BuildingType


def describe_building(building):
    basic_desc = building.description
    if not basic_desc:
        building_type = app.db_query(BuildingType).get(building.type)
        basic_desc = building_type.description or ""

    doors_desc = describe_doors_and_barricades(building)

    result = basic_desc + doors_desc

    return result


def describe_doors_and_barricades(building):
    if building.barricade_level is None:
        building.barricade_level = 0

    if building.barricade_level <= 0:
        return "The doors are open." if building.doors_open else "The doors are closed."
    elif building.barricade_level == 1:
        return "The building is loosely barricaded."
    elif 1 < building.barricade_level <= 4:
        return "The building is lightly barricaded."
    elif 4 < building.barricade_level <= 7:
        return "The building is quite strongly barricaded."
    elif 7 < building.barricade_level <= 10:
        return "The building is very strongly barricaded."
    elif 10 < building.barricade_level <= 13:
        return "The building is heavily barricaded."
    elif 13 < building.barricade_level <= 16:
        return "The building is very heavily barricaded."
    elif building.barricade_level > 16:
        return "The building is extremely heavily barricaded."
    else:
        return "The doors are open." if building.doors_open else "The doors are closed."
