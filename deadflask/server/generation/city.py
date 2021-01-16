from deadflask.server.data.buildingtypes import building_types
from deadflask.server.models.buildings import BuildingType


def preload_data(session):
    preloaded_data = {}
    for building_type in building_types:
        instance = get_or_create(session, BuildingType, building_type, name=building_type.name)
        preloaded_data.setdefault('building_types', {})[building_type.name] = instance

    return preloaded_data


def get_or_create(session, model, template, **kwargs):
    instance = session.query(model).filter_by(**kwargs).one_or_none()
    if instance:
        return instance
    else:
        session.add(template)
        session.commit()
        return template
