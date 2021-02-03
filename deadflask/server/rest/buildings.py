import logging

import flask

from deadflask.server import auth
from deadflask.server.app import app
from deadflask.server.models.buildings import Building, BuildingType
from deadflask.server.models.characters import Character, CharacterType

_logger = logging.getLogger()


@app.route('/building/<int:building_id>', methods=['GET'])
@auth.require_user
def get_building_info(user, building_id):
    building = app.db_session.query(Building).get(building_id)
    if not building:
        return flask.jsonify({'message': 'Invalid building_id'}), 400

    building_type = app.db_session.query(BuildingType).get(building.type)
    if not building_type:
        _logger.error(f"Building {building} has invalid building_type {building.type}")
        return flask.jsonify({'message': 'Server error'}), 500



    doors_description = _describe_doors_and_barricades(building)

    response = {
        'message': 'OK',
        'name': building.name,
        'description': building.description or building_type.description,
        'doors_description': doors_description,
        'type': {'id': building_type.id, 'name': building_type.name},
        'humans': humans,
        'zombies': zombies,
        'corpses': corpses,
    }

    return flask.jsonify(response)


