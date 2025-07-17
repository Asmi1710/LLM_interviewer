from flask import current_app, abort, make_response
from app.lib.helpers import to_json_dict
from flask import current_app


def generate_response(success=True, response_data={}, response_code=None, message=None):
    success_response(response_data, response_code) if success else error_response(response_data, response_code, message)


def success_response(response_data, response_code):
    if not response_code: response_code = 200
    abort(make_response(to_json_dict(response_data), response_code))


def error_response(response_data, response_code, message):
    if not response_code: response_code = 400
    current_app.logger.error(f"RESPONSE: {response_code} - {message}")
    abort(make_response(to_json_dict({"data": response_data, "message": message}), response_code))


def filter_response(response_data, exclude=[]):
    data = to_json_dict(response_data)
    for key in exclude:
        data.pop(key, None)
    return data
