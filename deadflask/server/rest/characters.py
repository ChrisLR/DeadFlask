import logging

import flask
from sqlalchemy.exc import IntegrityError

from deadflask.server import auth, exceptions
from deadflask.server.actions import general as general_actions, listing
from deadflask.server.app import app
from deadflask.server.models.buildings import Building
from deadflask.server.models.characters import Character, CharacterType
from deadflask.server.rest import validation, map

_create_character_fields = (
    validation.ValidatedField('name', str),
    validation.ValidatedField('character_type_id', int),
)
_logger = logging.getLogger()


@app.route('/character', methods=['POST'])
@auth.require_user
def create_character(user):
    post_data = flask.request.get_json()
    valid_data, invalid_data = validation.validate_post_data(_create_character_fields, post_data)
    if invalid_data:
        return flask.jsonify({'message': list(invalid_data.values())}), 400

    name = valid_data['name']
    # TODO A Proper name regex validation must be made
    if not name or Character.exists(name):
        return flask.jsonify({'message': 'Character name already exists'}), 400

    character_type_id = valid_data['character_type_id']
    character_type = app.db_query(CharacterType).get(character_type_id)
    if not character_type:
        return flask.jsonify({'message': 'Invalid Character type'}), 400

    # TODO Should users have a maximum amount of characters?
    try:
        character = Character.create(name=name, character_type=character_type, user=user)
    except IntegrityError as e:
        _logger.error(e)
        raise exceptions.APIError("Could not create character.")

    response = {'message': 'OK', 'character_id': character.id}

    return flask.jsonify(response)


@app.route('/character', methods=['GET'])
@auth.require_user
def get_characters(user):
    characters = app.db_query(Character).filter_by(user=user.id).all()
    if not characters:
        characters = []

    response = {
        'message': 'OK',
        'characters': [{'id': character.id, 'name': character.name} for character in characters]
    }

    return flask.jsonify(response)


@app.route('/character/<int:character_id>', methods=['GET'])
@auth.require_user
def get_character_info(user, character_id):
    character = app.db_query(Character).get(character_id)
    if not character:
        return flask.jsonify({'message': 'Unknown character id'}), 400

    if character.user != user.id:
        return flask.jsonify({'message': 'Invalid character id'}), 400

    character_type = app.db_query(CharacterType).get(character.type)
    # TODO Maybe we'll have more than one?
    is_zombie = character_type.name == "Zombie"

    response = {
        'message': 'OK',
        'name': character.name,
        'health': character.health,
        'experience': character.experience,
        'is_zombie': is_zombie,
        'is_inside': character.is_inside,
    }

    return flask.jsonify(response)


@app.route('/character/types', methods=['GET'])
@auth.require_user
def get_character_types(user):
    character_types = app.db_query(CharacterType).all()
    response = {
        'message': 'OK',
        'character_types': [
            {'id': char_type.id, 'name': char_type.name}
            for char_type in character_types
        ]
    }

    return flask.jsonify(response)


@app.route('/character/<int:character_id>/map', methods=['GET'])
@auth.require_user
def get_character_map(user, character_id):
    character = app.db_query(Character).get(character_id)
    if not character:
        return flask.jsonify({'message': 'Unknown character id'}), 400

    if character.user != user.id:
        return flask.jsonify({'message': 'Invalid character id'}), 400

    building = app.db_query(Building).filter(
        Building.coord_x == character.coord_x,
        Building.coord_y == character.coord_y,
        Building.city == character.city
    ).one_or_none()

    result_rows = map.get_map(character.coord_x, character.coord_y, character.city)
    response = {
        'message': 'OK',
        'building_id': building.id,
        'rows': result_rows
    }

    return flask.jsonify(response)


@app.route('/character/<int:character_id>/look', methods=['GET'])
@auth.require_user
def get_character_look(user, character_id):
    character = app.db_query(Character).get(character_id)
    if not character:
        return flask.jsonify({'message': 'Unknown character id'}), 400

    if character.user != user.id:
        return flask.jsonify({'message': 'Invalid character id'}), 400

    result = general_actions.look(character)
    response = {
        'message': 'OK',
        'description': result['description'],
        'humans': {c.id: c.name for c in result['humans']},
        'zombies': {c.id: c.name for c in result['zombies']},
        'corpses': {c.id: c.name for c in result['corpses']},
    }

    return flask.jsonify(response)


@app.route('/character/<int:character_id>/actions', methods=['GET'])
@auth.require_user
def get_character_actions(user, character_id):
    character = app.db_query(Character).get(character_id)
    if not character:
        return flask.jsonify({'message': 'Unknown character id'}), 400

    if character.user != user.id:
        return flask.jsonify({'message': 'Invalid character id'}), 400

    actions = listing.get_for_character(character)
    json_actions = [{
        'name': action.name,
        'requires_select_target': action.requires_select_target,
        'requires_select_item': action.requires_select_item,
        'requires_freeform_text': action.requires_freeform_text,
    } for action in actions]

    return flask.jsonify(json_actions)


@app.route('/character/<int:character_id>/actions', methods=['POST'])
@auth.require_user
def execute_character_action(user, character_id):
    post_data = flask.request.get_json()
    if not post_data:
        return flask.jsonify({'message': 'Missing POST data'}), 400

    action_data = post_data.get("action")
    if not action_data:
        return flask.jsonify({'message': 'Missing Action'}), 400

    action_name = action_data.get('name')
    if not action_name:
        return flask.jsonify({'message': 'Invalid Action'}), 400

    action = listing.get_by_name(action_name)
    if not action:
        return flask.jsonify({'message': 'Missing Action'}), 400

    character = app.db_query(Character).get(character_id)
    if not character:
        return flask.jsonify({'message': 'Unknown character id'}), 400

    if character.user != user.id:
        return flask.jsonify({'message': 'Invalid character id'}), 400

    if not action.can_execute(character):
        return flask.jsonify({'message': 'Action may not execute'}), 400

    select_target = action_data.get('select_target')
    if action.requires_select_target and not select_target:
        return flask.jsonify({'message': 'Action requires select_target'}), 400

    select_item = action_data.get('select_item')
    if action.requires_select_item and not select_item:
        return flask.jsonify({'message': 'Action requires select_item'}), 400

    freeform_text = action_data.get('freeform_text')
    if action.requires_freeform_text and not freeform_text:
        return flask.jsonify({'message': 'Action requires freeform_text'}), 400

    result = action.execute(character, target=select_target, item=select_item, text=freeform_text)
    json_result = {'message': 'OK', 'success': result}

    return flask.jsonify(json_result)
