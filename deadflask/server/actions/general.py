from deadflask.server.api.buildings import describe_building
from deadflask.server.api.characters import describe_characters_by_type, split_by_category
from deadflask.server.models.buildings import Building
from deadflask.server.models.characters import Character


def look(character, session):
    inside_str = "inside" if character.is_inside else "outside"
    building = session.query(Building).filter_by(
        coord_x=character.coord_x, coord_y=character.coord_y, city=character.city
    ).one_or_none()
    building_desc = describe_building(building, session)
    characters = Character.get_at_building(session, building, character.is_inside)
    characters = filter(lambda c: c is not character, characters)
    humans, zombies, corpses = split_by_category(characters, session)
    characters_desc = describe_characters_by_type(humans, zombies, corpses)

    description = f"You are {inside_str} {building.name}. {building_desc} {characters_desc}"
    result = {"description": description, 'humans': humans, 'zombies': zombies, 'corpses': corpses}

    return result
