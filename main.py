import json
import os

from deadflask.server import dbcore
# noinspection PyUnresolvedReferences
from deadflask.server import models
from deadflask.server.app import app
from deadflask.server.generation.city import preload_data, create_city

if __name__ == '__main__':
    config_path = os.path.join(os.path.dirname(__file__), "deadflask/config.json")
    with open(config_path, 'r') as file_stream:
        config = json.load(file_stream)

    db_config = config["db_config"]
    session = dbcore.connect_db(db_config)
    preloaded_data = preload_data(session)
    #create_city(session, preloaded_data)
    app.db_session = session
    app.app_config = config

    app.run()
