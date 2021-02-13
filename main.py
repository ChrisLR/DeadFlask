import json
import os

from deadflask.server import dbcore
from deadflask.server.app import app
from deadflask.server.generation.preloading import preload_data

if __name__ == '__main__':
    config_path = os.path.join(os.path.dirname(__file__), "deadflask/config.json")
    with open(config_path, 'r') as file_stream:
        config = json.load(file_stream)

    db_config = config["db_config"]
    db_connection = dbcore.DBConnection(db_config)
    app.db_connection = db_connection
    db_connection.connect()

    app.before_request(db_connection.prepare_new_session)
    app.after_request(db_connection.commit_session)

    db_connection.prepare_new_session()
    preloaded_data = preload_data(db_connection.session)
    app.preloaded_data = preloaded_data
    db_connection.commit_session(None)

    app.app_config = config

    app.run()
    app.db_connection.close()
