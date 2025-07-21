from cerberus import Validator
from . import RequestErrorHandler

interview_start_validator = Validator({
    'interview':{
        'type': 'dict',
        'allow_unknown': False,
        'schema': {
            'job_id': {'type': 'string', 'required': True, 'empty': False, 'nullable': False},
            'candidate_id': {'type': 'string', 'required': True, 'empty': False, 'nullable': False},
            'role': {'type': 'string', 'required': True, 'empty': False, 'nullable': False},
        },
        'required': True
    }
}, allow_unknown=True, error_handler=RequestErrorHandler)