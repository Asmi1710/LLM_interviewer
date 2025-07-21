# https://docs.python-cerberus.org/en/stable/
from cerberus import errors

# https://github.com/pyeve/cerberus/blob/master/cerberus/errors.py
class RequestErrorHandler(errors.BasicErrorHandler):
    messages = errors.BasicErrorHandler.messages.copy()
    messages[errors.REQUIRED_FIELD.code] = "can't be blank"
    messages[0x22] = "can't be blank" # EMPTY
    messages[errors.REGEX_MISMATCH.code] = "invalid value"
