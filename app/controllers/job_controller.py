from flask import request
from app.exceptions import InvalidDataError
from app.lib.helpers.response_helper import generate_response

def create():
    from app.validators.job_request_validator import job_create_validator as request_validator
    from app.services.job import create as create_service

    valid = request_validator.validate(request.json)
    if not valid:
        raise InvalidDataError('Invalid request', data=request_validator.errors)

    request_json = request.json.get('job', {})
    response_data = create_service.call(request_json)
    generate_response(success=True, response_data={'status': 'success', 'message': 'job created successfully', 'data': response_data})    
    

def search():
    from app.services.job import search as search_service
    from app.lib.helpers.search_helper import get_search_options

    request_json = request.json
    conditions = request_json.get('conditions', {})
    search_options = get_search_options(request_json)
    response_data = search_service.call(conditions, **search_options)
    generate_response(success=True, response_data={'status': 'success', 'message': 'jobs searched successfully', 'data': response_data})    
        

def update(job_id):
    from app.services.job import update as update_service

    request_json = request.json.get('job', {})
    response_data = update_service.call(job_id, request_json)
    generate_response(success=True, response_data={'status': 'success', 'message': 'job updated successfully', 'data': response_data})       