from app.repositories import _job_repository
from app.exceptions import InvalidDataError

def call(job_id, request):
    job = ~_job_repository().get(job_id)
    if not job:
        InvalidDataError("Invalid data", data="Invalid job_id")

    _job_repository().update(job, request) 

    return job   