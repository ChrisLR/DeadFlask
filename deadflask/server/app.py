from flask import Flask, jsonify
from flask_cors import CORS


class DeadFlaskApp(Flask):
    def __init__(self):
        super().__init__(__name__)
        self.config["DEBUG"] = True
        self.db_session = None
        self.app_config = None
        self.preloaded_data = None


app = DeadFlaskApp()

# enable CORS
CORS(app, resources=r'/*', origins=['http://localhost:8080'], supports_credentials=True)
app.config['CORS_HEADERS'] = 'Content-Type'


# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('Pong!')
