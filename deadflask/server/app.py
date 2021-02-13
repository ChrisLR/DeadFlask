import inflect
from flask import Flask, jsonify
from flask_cors import CORS


# SESSION CAN BE STORED ON APP IF REQUEST DECORATOR IS AXED ON COMMIT/ROLLBACK
class DeadFlaskApp(Flask):
    def __init__(self):
        super().__init__(__name__)
        self.config["DEBUG"] = True
        self.app_config = None
        self.preloaded_data = None
        self.inflect = inflect.engine()
        self.db_connection = None

    @property
    def db_query(self):
        return self.db_connection.query


app = DeadFlaskApp()

# enable CORS
CORS(app, resources=r'/*', origins=['http://localhost:8080'], supports_credentials=True)
app.config['CORS_HEADERS'] = 'Content-Type'


# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('Pong!')
