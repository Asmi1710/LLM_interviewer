from cerberus import Validator
from .. import RequestErrorHandler

interview_create_validator = Validator({
    'interview':{
        'type': 'dict',
        'allow_unknown': False,
        'schema': {
            'job_id': {'type': 'str', 'required': True, 'empty': False},
            'candidate_id': {'type': 'str', 'required': True, 'empty': False},
            'role': {'type': 'str', 'required': True, 'empty': False},
        },
        'required': True
    }
}, allow_unknown=True, error_handler=RequestErrorHandler)