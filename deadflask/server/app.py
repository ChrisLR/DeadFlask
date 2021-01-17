from flask import Flask, jsonify
from flask_cors import CORS


class DeadFlaskApp(Flask):
    def __init__(self):
        super().__init__(__name__)
        self.config["DEBUG"] = True
        self.db_session = None


app = DeadFlaskApp()

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('Pong!')
