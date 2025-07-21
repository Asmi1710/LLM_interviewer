from flask import request
from app.exceptions import InvalidDataError
from app.lib.helpers.response_helper import generate_response

def start():
    from app.validators.interview_request_validator import interview_start_validator as request_validator
    from app.services.interview import start as start_service

    valid = request_validator.validate(request.json)
    if not valid:
        raise InvalidDataError('Invalid request', data=request_validator.errors)

    request_json = request.json.get('interview', {})
    response_data = start_service.call(request_json)
    generate_response(success=True, response_data={'status': 'success', 'message': 'interview started successfully', 'data': response_data})    
    

def search():
    from app.services.interview import search as search_service
    from app.lib.helpers.search_helper import get_search_options

    request_json = request.json
    conditions = request_json.get('conditions', {})
    search_options = get_search_options(request_json)
    response_data = search_service.call(conditions, **search_options)
    generate_response(success=True, response_data={'status': 'success', 'message': 'interviews searched successfully', 'data': response_data})    
        

def create():
    from app.services.interview import create as create_service

    call_sid = request.values.get('CallSid')
    recording_url = request.values.get('RecordingUrl')
    req_args = request.args
    response_data = create_service.call(call_sid, recording_url, req_args.get('candidate_id'), req_args.get('job_id'), req_args.get('role'))
    generate_response(success=True, response_data={'status': 'success', 'message': 'interviews conducted successfully', 'data': response_data})    
        
