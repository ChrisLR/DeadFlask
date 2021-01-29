import flask
import logging
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from deadflask.server import auth
from deadflask.server.api import validation
from deadflask.server.app import app
from deadflask.server.models.characters import Character, CharacterType

_create_character_fields = (
    validation.ValidatedField('name', str),
    validation.ValidatedField('character_type_id', int),
)


@app.route('/character', methods=['POST'])
@auth.require_user
def create_character(user):
    post_data = flask.request.get_json()
    valid_data, invalid_data = validation.validate_post_data(_create_character_fields, post_data)
    if invalid_data:
        return flask.jsonify({'message': list(invalid_data.values())}), 400

    name = valid_data['name']
    # TODO A Proper name regex validation must be made
    if not name or Character.exists(app, name):
        return flask.jsonify({'message': 'Character name already exists'}), 400

    character_type_id = valid_data['character_type_id']
    character_type = app.db_session.query(CharacterType).get(character_type_id)
    if not character_type:
        return flask.jsonify({'message': 'Invalid Character type'}), 400

    # TODO Should users have a maximum amount of characters?
    try:
        character = Character.create(app, name=name, character_type=character_type, user=user)
        app.db_session.commit()
    except IntegrityError as e:
        logging.error(f"Create Character failed. {e}")
        app.db_session.rollback()
        return flask.jsonify({'message': 'Could not create character.'}), 500

    response = {'message': 'OK', 'character_id': character.id}

    return flask.jsonify(response)


@app.route('/character', methods=['GET'])
@auth.require_user
def get_characters(user):
    characters = app.db_session.query(Character).filter_by(user=user.id).all()
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
    character = app.db_session.query(Character).get(character_id)
    if not character:
        return flask.jsonify({'message': 'Unknown character id'}), 400

    if character.user != user.id:
        return flask.jsonify({'message': 'Invalid character id'}), 400

    character_type = app.db_session.query(CharacterType).get(character.type)
    # TODO Maybe we'll have more than one?
    is_zombie = character_type.name == "Zombie"

    response = {
        'message': 'OK',
        'name': character.name,
        'health': character.health,
        'experience': character.experience,
        'is_zombie': is_zombie
    }

    return flask.jsonify(response)


@app.route('/character/types', methods=['GET'])
@auth.require_user
def get_character_types(user):
    character_types = app.db_session.query(CharacterType).all()
    response = {
        'message': 'OK',
        'character_types': [
            {'id': char_type.id, 'name': char_type.name}
            for char_type in character_types
        ]
    }

    return flask.jsonify(response)
