import logging

from deadflask.server.data.buildingtypes import building_types
from deadflask.server.data.charactertypes import character_types
from deadflask.server.generation import utils
from deadflask.server.models.buildings import BuildingType
from deadflask.server.models.characters import CharacterType


MODELS_AND_DATA = (
    (BuildingType, building_types),
    (CharacterType, character_types),
)

_logger = logging.getLogger()


def preload_data():
    preloaded_data = {}
    for model, data_instances in MODELS_AND_DATA:
        _logger.debug("Preloading {model.__tablename__} instances...")
        for data_instance in data_instances:
            instance = utils.get_or_create(session, model, data_instance, name=data_instance.name)
            preloaded_data.setdefault(model.__tablename__, {})[data_instance.name] = instance

    return preloaded_data
