from flask import request
from app.exceptions import InvalidDataError
from app.lib.helpers.response_helper import generate_response

def create():
    from app.validators.candidate_request_validator import candidate_create_validator as request_validator
    from app.services.candidate import create as create_service

    valid = request_validator.validate(request.json)
    if not valid:
        raise InvalidDataError('Invalid request', data=request_validator.errors)

    request_json = request.json.get('candidate', {})
    response_data = create_service.call(request_json)
    generate_response(success=True, response_data={'status': 'success', 'message': 'candidate created successfully', 'data': response_data})    
    

def search():
    from app.services.candidate import search as search_service
    from app.lib.helpers.search_helper import get_search_options

    request_json = request.json
    conditions = request_json.get('conditions', {})
    search_options = get_search_options(request_json)
    response_data = search_service.call(conditions, **search_options)
    generate_response(success=True, response_data={'status': 'success', 'message': 'candidates searched successfully', 'data': response_data})    
        