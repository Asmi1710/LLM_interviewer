from cerberus import Validator
from . import RequestErrorHandler

candidate_create_validator = Validator({
    'candidate':{
        'type': 'dict',
        'allow_unknown': True,
        'schema': {
            'full_name': {'type': 'string', 'required': True, 'empty': False, 'nullable': False},
            'mobile_number': {'type': 'string', 'required': True, 'empty': False, 'nullable': False},
            'email': {'type': 'string', 'required': True, 'empty': False, 'nullable': False},
        },
        'required': True
    }
}, allow_unknown=True, error_handler=RequestErrorHandler)