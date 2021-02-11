import logging

import flask
from sqlalchemy.exc import IntegrityError

from deadflask.server import auth, dbcore
from deadflask.server.rest import validation, map
from deadflask.server.app import app
from deadflask.server.models.characters import Character, CharacterType
from deadflask.server.models.buildings import Building
from deadflask.server.actions import general as general_actions

_create_character_fields = (
    validation.ValidatedField('name', str),
    validation.ValidatedField('character_type_id', int),
)


@app.route('/character', methods=['POST'])
@auth.require_user
@dbcore.with_session
def create_character(user, session):
    post_data = flask.request.get_json()
    valid_data, invalid_data = validation.validate_post_data(_create_character_fields, post_data)
    if invalid_data:
        return flask.jsonify({'message': list(invalid_data.values())}), 400

    name = valid_data['name']
    # TODO A Proper name regex validation must be made
    if not name or Character.exists(session, name):
        return flask.jsonify({'message': 'Character name already exists'}), 400

    character_type_id = valid_data['character_type_id']
    character_type = session.query(CharacterType).get(character_type_id)
    if not character_type:
        return flask.jsonify({'message': 'Invalid Character type'}), 400

    # TODO Should users have a maximum amount of characters?
    try:
        character = Character.create(session, name=name, character_type=character_type, user=user)
    except IntegrityError as e:
        logging.error(f"Create Character failed. {e}")
        session.rollback()
        return flask.jsonify({'message': 'Could not create character.'}), 500

    response = {'message': 'OK', 'character_id': character.id}

    return flask.jsonify(response)


@app.route('/character', methods=['GET'])
@auth.require_user
@dbcore.with_session
def get_characters(user, session):
    characters = session.query(Character).filter_by(user=user.id).all()
    if not characters:
        characters = []

    response = {
        'message': 'OK',
        'characters': [{'id': character.id, 'name': character.name} for character in characters]
    }

    return flask.jsonify(response)


@app.route('/character/<int:character_id>', methods=['GET'])
@auth.require_user
@dbcore.with_session
def get_character_info(user, character_id, session):
    character = session.query(Character).get(character_id)
    if not character:
        return flask.jsonify({'message': 'Unknown character id'}), 400

    if character.user != user.id:
        return flask.jsonify({'message': 'Invalid character id'}), 400

    character_type = session.query(CharacterType).get(character.type)
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
@dbcore.with_session
def get_character_types(user, session):
    character_types = session.query(CharacterType).all()
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
@dbcore.with_session
def get_character_map(user, character_id, session):
    character = session.query(Character).get(character_id)
    if not character:
        return flask.jsonify({'message': 'Unknown character id'}), 400

    if character.user != user.id:
        return flask.jsonify({'message': 'Invalid character id'}), 400

    building = session.query(Building).filter(
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
@dbcore.with_session
def get_character_look(user, character_id, session):
    character = session.query(Character).get(character_id)
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


