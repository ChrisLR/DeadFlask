from datetime import datetime, timedelta

import flask
import jwt

from deadflask.server.app import app
from deadflask.server.models.user import User


@app.route('/login', methods=['POST'])
def post_login():
    post_data = flask.request.get_json()
    email = post_data.get('email', '')
    password = post_data.get('password', '')

    user = User.authenticate(app, email, password)
    if not user:
        response = {'message': "Invalid credentials", 'token': None}
        return flask.jsonify(response), 401

    token_payload = {
        'user_id': user.id,
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(minutes=30)
    }
    token = jwt.encode(key=app.app_config['secret_key'], payload=token_payload)
    response = {'message': "OK", 'token': token.decode('UTF-8')}

    return flask.jsonify(response)

