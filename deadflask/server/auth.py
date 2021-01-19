from functools import wraps

import flask
import jwt

from deadflask.server.app import app
from deadflask.server.models.user import User


def require_user(func):
    @wraps(func)
    def _verify(*args, **kwargs):
        auth_headers = flask.request.headers.get('Authorization', '').split()
        if len(auth_headers) != 2:
            return flask.jsonify({'message': 'Invalid token'}), 401

        try:
            token = auth_headers[1]
            data = jwt.decode(token, app.app_config['secret_key'])
            user_id = data.get("user_id")
            user = app.db_session.query(User).filter_by(id=user_id)
            if not user:
                return flask.jsonify({'message': 'Invalid User'}), 401

            return func(user, *args, **kwargs)
        except jwt.ExpiredSignatureError:
            return flask.jsonify({'message': 'Expired token'}), 401
        except (jwt.InvalidTokenError, Exception):
            return flask.jsonify({'message': 'Invalid token'}), 401

    return _verify
