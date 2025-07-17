#from redis import Redis
from bunnet import init_bunnet
from pymongo import MongoClient

celery_redis = None

def init_db(app):
    #init_celery_redis(app)
    init_ai_interviewer_backend_db(app)


# def init_celery_redis(app):
#     global celery_redis
#     celery_redis_url = app.config['CELERY_REDIS_URL']
#     celery_redis = Redis.from_url(celery_redis_url)


def init_ai_interviewer_backend_db(app):
    # Create Motor client
    ai_interviewer_backend_db_uri = app.config['AI_INTERVIEWER_BACKEND_DB_URI']
    client = MongoClient(ai_interviewer_backend_db_uri)

    # Init bunnet with the Product document class
    ai_interviewer_backend_database = client[app.config["AI_INTERVIEWER_BACKEND_DB_NAME"]]
    init_bunnet(
        database=ai_interviewer_backend_database,
        document_models=[
            "app.models.job.Job",
            "app.models.candidate.Candidate",
            "app.models.interview.Interview",
        ]
    )
