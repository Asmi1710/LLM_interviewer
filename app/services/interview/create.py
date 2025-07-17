from app.repositories import _candidate_repository, _job_repository

def call(request):
    candidate = ~_candidate_repository().get(request.get('candidate_id'))
    job = ~_job_repository().get(request.get('job_id'))

    # make a call to candidate with basic question1
    # record the answer and score it
    # generate next question and continue this loop for 5 times 
    # after interview is created, repo: after_create: calculate overall score (avg) & summary about the candidate
    # later make provision for additional queries in the call using the request body

    
