import logging

import werkzeug

from deadflask.server.app import app
from deadflask.server import exceptions

_logger = logging.getLogger()


@app.errorhandler(werkzeug.exceptions.InternalServerError)
def handle_500(e):
    original = getattr(e, "original_exception", None)
    _logger.error(original)
    if app.db_session:
        app.db_session.rollback()

    return {'error': 'Internal Server Error'}, 500


@app.errorhandler(exceptions.APIError)
def handle_api_error(e):
    _logger.warning(e)
    if app.db_session:
        app.db_session.rollback()

    return {'error': str(e)}, 500
