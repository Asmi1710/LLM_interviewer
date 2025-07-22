from flask import request, current_app
from app.lib.helpers.response_helper import generate_response

def before_request():
    if request.path != '/':    
        current_app.logger.info(f"""API REQUEST - {request.method} {request.path}
        HEADERS: {dict(request.headers)}
        ARGS   : {dict(request.args)}
        REQUEST: {request.json if (request.method not in ['GET', 'DELETE', 'OPTIONS']) else {} }
        """)


def after_request(response):
    if request.path == '/':
        return response
    current_app.logger.info(f"""API RESPONSE - {response.status_code} - {request.method} {request.path}
    HEADERS: {dict(response.headers)}
    RESPONSE: {response.json}
    """)
    return response


def index():
    generate_response(success=True, response_data={
        'status': 'success',
        'message': 'ai_interviewer_api_health_ok',
        'healthy': True,
        'flask_env': current_app.config['ENV']
    })