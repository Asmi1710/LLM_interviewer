from cerberus import Validator
from .. import RequestErrorHandler

candidate_create_validator = Validator({
    'candidate':{
        'type': 'dict',
        'allow_unknown': True,
        'schema': {
            'name': {'type': 'str', 'required': True, 'empty': False},
            'mobile_number': {'type': 'str', 'required': True, 'empty': False},
            'email': {'type': 'str', 'required': True, 'empty': False},
        },
        'required': True
    }
}, allow_unknown=True, error_handler=RequestErrorHandler)