from werkzeug.exceptions import HTTPException
from requests.exceptions import HTTPError
from app.lib.helpers import to_json_dict
from flask import current_app

def configure_exception_handler(app):
    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        current_app.logger.exception(str(e))
        return to_json_dict({"message": str(e)}), e.code

    @app.errorhandler(HTTPError)
    def handle_http_exception(e):
        current_app.logger.exception(str(e))
        error_message = "Unauthorized" if e.response.status_code==401 else str(e)
        return to_json_dict({"message": error_message}), e.response.status_code

    @app.errorhandler(Exception)
    def handle_exception(e):
        current_app.logger.exception(str(e))
        return to_json_dict({"message": str(e)}), 500

    @app.errorhandler(InvalidDataError)
    def handle_exception(e):
        current_app.logger.exception(e.message)
        return to_json_dict({"message": e.message, "data": e.data}), e.status_code or 400

class InvalidDataError(Exception):
    def __init__(self, message, status_code=None, data={}):
        Exception.__init__(self)
        self.message = message
        self.status_code = status_code or 400
        self.data = data

    def __str__(self):
        return self.message or ""

class UnauthenticatedError(InvalidDataError):
    def __init__(self, message=None, status_code=None, data={}):
        Exception.__init__(self)
        self.message = message or 'Invalid Credentials'
        self.status_code = status_code or 401
        self.data = data