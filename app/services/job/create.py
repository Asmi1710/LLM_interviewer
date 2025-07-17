from app.repositories import _job_repository

def call(request):
    job = _job_repository().create(**request)

    return job