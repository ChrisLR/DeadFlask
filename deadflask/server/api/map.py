import flask
import logging
from sqlalchemy.exc import SQLAlchemyError

from deadflask.server.api import validation
from deadflask.server.app import app
from deadflask.server.auth import require_user
from deadflask.server.models.buildings import Building, BuildingType
from deadflask.server.models.characters import Character, CharacterType

_move_to_fields = (
    validation.ValidatedField('building_id', int),
    validation.ValidatedField('character_id', int),
)

_logger = logging.getLogger()


def get_map(cx, cy, city):
    # Just some quick validation, make something better
    if cx < 0 or cy < 0 or cx > 20000 or cy > 20000:
        cx = 0
        cy = 0

    left = cx - 1
    right = cx + 1
    top = cy - 1
    bottom = cy + 1

    rows = app.db_session.query(Building, BuildingType).filter(
        Building.coord_x >= left,
        Building.coord_x <= right,
        Building.coord_y >= top,
        Building.coord_y <= bottom,
        Building.city == city,
        Building.type == BuildingType.id
    ).order_by(Building.coord_y, Building.coord_x)

    character_rows = app.db_session.query(Character, CharacterType).filter(
        Character.coord_x >= left,
        Character.coord_x <= right,
        Character.coord_y >= top,
        Character.coord_y <= bottom,
        Character.city == city,
        Character.type == CharacterType.id
    )
    humans_by_pos = {}
    zombies_by_pos = {}
    for row in character_rows:
        character = row.Character
        coords = (character.coord_x, character.coord_y)
        character_data = {'id': character.id, 'name': character.name}
        if row.CharacterType.name == 'Zombie':
            zombies_by_pos.setdefault(coords, []).append(character_data)
        else:
            humans_by_pos.setdefault(coords, []).append(character_data)

    r_array = [[None for _ in range(-1, 2)] for _ in range(-1, 2)]
    for row in rows:
        local_building_x = (row.Building.coord_x - left)
        local_building_y = (row.Building.coord_y - top)
        world_coords = (row.Building.coord_x, row.Building.coord_y)
        r_array[local_building_y][local_building_x] = {
                'name': row.Building.name,
                'type': row.BuildingType.name,
                'id': row.Building.id,
                'humans': humans_by_pos.get(world_coords, []),
                'zombies': zombies_by_pos.get(world_coords, []),
            }

    return r_array


@app.route('/move_to', methods=['POST'])
@require_user
def move_to(user):
    post_data = flask.request.get_json()
    valid_data, invalid_data = validation.validate_post_data(_move_to_fields, post_data)
    if invalid_data:
        return flask.jsonify({'message': list(invalid_data.values())}), 400

    building_id = valid_data['building_id']
    building = app.db_session.query(Building).get(building_id)
    if not building:
        return flask.jsonify({'message': 'Invalid building_id'}), 400

    character_id = valid_data['character_id']
    character = app.db_session.query(Character).get(character_id)
    if not character:
        return flask.jsonify({'message': 'Invalid character_id'}), 400

    try:
        character.coord_x = building.coord_x
        character.coord_y = building.coord_y
        app.db_session.commit()
    except SQLAlchemyError as e:
        _logger.error(f"Move To Failed: {e}")
        app.db_session.rollback()
        return flask.jsonify({'message': 'Server Error'}), 500

    result_rows = get_map(building.coord_x, building.coord_y, building.city)

    return flask.jsonify(result_rows)
