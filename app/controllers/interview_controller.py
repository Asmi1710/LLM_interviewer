from flask import request, send_file, current_app
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

    current_app.logger.info(f"Twilio callback values: {dict(request.values)}")
    call_sid = request.values.get('CallSid')
    recording_url = request.values.get('RecordingUrl')
    req_args = request.args
    if not call_sid or not recording_url:
        raise InvalidDataError('Invalid request', data='call_sid or recording_url is missing')
    
    # Log raw values for debug
    current_app.logger.info(f"Incoming create call: CallSid={call_sid}, RecordingUrl={recording_url}, args={req_args}")
    response_data = create_service.call(call_sid, recording_url, req_args.get('candidate_id'), req_args.get('job_id'), req_args.get('role'))
    return response_data
        

def audio():
    from app.services.agents.audio_agent import generate_voice
    import os, time, hmac, hashlib

    text = request.args.get('text')
    timestamp = request.args.get('ts')
    client_signature = request.args.get('sig')
    if not timestamp or not text or not client_signature:
        raise InvalidDataError('Invalid request', data='client_signature, timestamp or text is missing')
    
    # Step 1: Check timestamp is recent
    try:
        timestamp = int(timestamp)
    except ValueError:
        raise InvalidDataError("Invalid timestamp format", data=timestamp)

    current_ts = int(time.time())
    allowed_drift = int(os.getenv('HMAC_SIGNATURE_EXPIRY', 60))

    if abs(current_ts - timestamp) > allowed_drift:
        raise InvalidDataError("Request expired", data="timestamp too old or in future")

    # Step 2: Validate HMAC signature
    secret_key = os.getenv('HMAC_SECRET_KEY', '')
    message = f"{text}{timestamp}".encode('utf-8')
    expected_signature = hmac.new(secret_key.encode('utf-8'), message, hashlib.sha256).hexdigest()

    if not hmac.compare_digest(expected_signature, client_signature):
        raise InvalidDataError("Invalid signature", data="unauthorized request")
    
    audio_data = generate_voice(text)
    return send_file(
        audio_data,
        mimetype="audio/wav",
        as_attachment=False
    ) 
        