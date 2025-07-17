from flask import request
from celery import current_task
from flask_log_request_id import current_request_id as flask_request_id

def current_request_id():
    if (request_id := flask_request_id()):
        return request_id

    if current_task and hasattr(current_task, 'request'):
        return current_task.request.id

def current_caller_id():
    try:
        return request.headers.get('x_caller_id') or request.headers.get('caller_id')
    except RuntimeError as e:
        # Executing outside context
        return None
