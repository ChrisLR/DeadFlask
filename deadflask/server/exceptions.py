class APIError(Exception):
    """
    Base class for Internal API Errors
    """
    code = 500
