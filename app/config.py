# https://github.com/Workable/flask-log-request-id

import os, yaml
from logging.config import dictConfig
from flask_log_request_id import RequestID
from dotenv import load_dotenv
from app.lib.helpers.logging_helper import RequestIDLogFilter, CallerIDLogFilter

class BaseConfig(object):
    load_dotenv(dotenv_path=f'.env')
    ENV = os.getenv('FLASK_ENV')
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv('SECRET_KEY')

    AI_INTERVIEWER_BACKEND_DB_URI = os.getenv('AI_INTERVIEWER_BACKEND_DB_URI')
    AI_INTERVIEWER_BACKEND_DB_NAME = os.getenv('AI_INTERVIEWER_BACKEND_DB_NAME')

    REDIS_URL=os.getenv('REDIS_URL')

    TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
    TWILIO_AUTH_TOKEN= os.getenv('TWILIO_AUTH_TOKEN')
    TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')


class TestConfig(BaseConfig):
    AI_INTERVIEWER_BACKEND_DB_URI = os.getenv('AI_INTERVIEWER_BACKEND_DB_URI')
    AI_INTERVIEWER_BACKEND_DB_NAME = 'ai_interviewer_backend_test'

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = True

    # CELERY_SCHEDULE_SYNC_ZOHO_DATA = crontab(minute=0)

class DevConfig(BaseConfig):
    DEBUG = True
    TESTING = True

    # CELERY_SCHEDULE_SYNC_ZOHO_DATA = crontab(minute=0)

class StagingConfig(BaseConfig):
    TESTING = True

    # CELERY_SCHEDULE_SYNC_ZOHO_DATA = crontab(minute=0)

class ProductionConfig(BaseConfig):
    DEBUG = False
    TESTING = False

    # CELERY_SCHEDULE_SYNC_ZOHO_DATA = crontab(minute=0)

config = {
    "test": "app.config.TestConfig",
    "development": "app.config.DevelopmentConfig",
    "dev": "app.config.DevConfig",
    "staging": "app.config.StagingConfig",
    "production": "app.config.ProductionConfig"
}

def configure_app(app):
    config_name = os.getenv('FLASK_ENV', 'development')
    app.config.from_object(config[config_name]) # object-based default configuration
    configure_logger(app)
    configure_redis(app)
    configure_openai(app)
    # configure_apm(app)

def configure_redis(app):
    from redis import Redis
    redis_client = Redis.from_url(os.getenv('REDIS_URL'))
    app.extensions['redis'] = redis_client

def configure_openai(app):
    from openai import OpenAI
    openai_client = OpenAI(api_key= os.getenv('OPENAI_API_KEY'))
    app.extensions['openai_client'] = openai_client
# To use within application
# app.config[key]

# def configure_celery(app) -> Celery:
#     import dill
#     from kombu.serialization import pickle_loads, pickle_protocol, registry
#     from kombu.utils.encoding import str_to_bytes

#     def register_dill():
#         def encode(obj, dumper=dill.dumps):
#             return dumper(obj, protocol=pickle_protocol)

#         def decode(s):
#             return pickle_loads(str_to_bytes(s), load=dill.load)

#         registry.register(
#             name='dill',
#             encoder=encode,
#             decoder=decode,
#             content_type='application/x-python-serialize',
#             content_encoding='binary'
#         )

#     register_dill()

#     class FlaskTask(Task):
#         def __call__(self, *args: object, **kwargs: object) -> object:
#             with app.app_context():
#                 return self.run(*args, **kwargs)
            
#         def on_retry(self, exc, task_id, args, kwargs, einfo):
#             with app.app_context():
#                 app.logger.error(f"Retrying task {task_id} due to exception: {exc}")
#                 notify_exception(exc)

#         def on_failure(self, exc, task_id, args, kwargs, einfo):
#             with app.app_context():
#                 app.logger.error(f"Task {task_id} failed due to exception: {exc}")
#                 notify_exception(exc)    

#     celery_app = Celery(app.name, task_cls=FlaskTask)
#     celery_app.conf.task_default_queue = app.config["CELERY_REDIS_QUEUE_NAME"]
#     celery_app.conf.task_routes = {
#         'app.jobs.*': { 'queue': app.config["CELERY_REDIS_QUEUE_NAME"]}
#     }
#     celery_app.config_from_object(app.config["CELERY"])
#     celery_app.set_default()
#     app.extensions["celery"] = celery_app
#     return celery_app

def configure_logger(app):
    dictConfig(yaml.full_load(open(f'config/{os.getenv("FLASK_ENV")}/logging.conf')))
    RequestID(app)
    app.logger.addFilter(RequestIDLogFilter())
    app.logger.addFilter(CallerIDLogFilter())

# def configure_apm(app):
#     from elasticapm.contrib.flask import ElasticAPM
#     if os.getenv('ELASTIC_APM_SERVER_URL'):
#         apm = ElasticAPM()
#         apm.init_app(app, service_name='Awign Experts Backend', server_url=os.getenv('ELASTIC_APM_SERVER_URL'), environment=os.getenv('FLASK_ENV', 'development'), debug=True)
