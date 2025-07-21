from cerberus import Validator
from . import RequestErrorHandler

job_create_validator = Validator({
    'job':{
        'type': 'dict',
        'allow_unknown': True,
        'schema': {
            'role_name': {'type': 'string', 'required': True, 'empty': False, 'nullable': False},
        },
        'required': True
    }
}, allow_unknown=True, error_handler=RequestErrorHandler)