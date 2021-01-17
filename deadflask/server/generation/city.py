from deadflask.server.data.buildingtypes import building_types
from deadflask.server.models.buildings import BuildingType, Building
from deadflask.server.models.cities import City
import faker
import random


def preload_data(session):
    preloaded_data = {}
    for building_type in building_types:
        instance = get_or_create(session, BuildingType, building_type, name=building_type.name)
        preloaded_data.setdefault('building_types', {})[building_type.name] = instance

    return preloaded_data


def create_city(session, preload_data):
    my_faker = faker.Faker()
    city_name = my_faker.city()
    city = City(name=city_name)
    session.add(city)
    session.commit()
    building_type_list = list(preload_data["building_types"].values())
    new_buildings = []
    taken_names = set()
    for x in range(100):
        for y in range(100):
            building_type = random.choice(building_type_list)
            complete_name = None
            while complete_name is None:
                random_name = my_faker.city()
                complete_name = f"{random_name} {building_type.name}"
                if complete_name not in taken_names:
                    taken_names.add(complete_name)
                else:
                    complete_name = None

            building = Building(
                name=complete_name, coord_x=x, coord_y=y,
                city=city.id, type=building_type.id
            )
            new_buildings.append(building)

    session.add_all(new_buildings)
    session.commit()



def get_or_create(session, model, template, **kwargs):
    instance = session.query(model).filter_by(**kwargs).one_or_none()
    if instance:
        return instance
    else:
        session.add(template)
        session.commit()
        return template
