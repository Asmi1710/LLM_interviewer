import logging
import uuid
from celery.signals import after_setup_logger
from app.lib.helpers.flask_helper import current_request_id, current_caller_id

class RequestIDLogFilter(logging.Filter):
    def filter(self, log_record):
        try:
            log_record.request_id = current_request_id()
        except:
            # Executing outside context
            log_record.request_id = None
        return log_record

class CallerIDLogFilter(logging.Filter):
    def filter(self, log_record):
        try:
            log_record.caller_id = current_caller_id()
        except RuntimeError as e:
            # Executing outside context
            log_record.caller_id = None
        return log_record

# Celery log formatter config
@after_setup_logger.connect
def setup_celery_loggers(logger, *args, **kwargs):
    logger.handlers.clear()
    # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - request_id: %(request_id)s - %(message)s')

    # StreamHandler
    # logger.handlers = [ h for h in logger.handlers if not isinstance(h, logging.StreamHandler) ]
    sh = logging.StreamHandler()
    sh.setFormatter(formatter)
    logger.addHandler(sh)

class SafeFormatter(logging.Formatter):
    def format(self, record):
        if not hasattr(record, 'request_id') or not record.request_id:
            record.request_id = str(uuid.uuid4())
        if not hasattr(record, 'caller_id') or not record.caller_id:
            record.caller_id = 'system'
        return super().format(record)