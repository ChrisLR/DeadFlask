import json
import os

from deadflask.server import dbcore
# noinspection PyUnresolvedReferences
from deadflask.server import models
from deadflask.server.app import app
from deadflask.server.generation.city import create_city
from deadflask.server.generation.preloading import preload_data

if __name__ == '__main__':
    config_path = os.path.join(os.path.dirname(__file__), "deadflask/config.json")
    with open(config_path, 'r') as file_stream:
        config = json.load(file_stream)

    db_config = config["db_config"]
    session_maker = dbcore.get_session_maker(db_config)
    app.session_maker = session_maker
    app.before_request(dbcore.prepare_new_session)
    app.after_request(dbcore.commit_session)
    preloaded_data = preload_data()
    app.preloaded_data = preloaded_data
    #create_city(session, preloaded_data)

    app.app_config = config

    app.run()
    app.db_session.close()
