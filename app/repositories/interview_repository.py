from flask import current_app
from app.repositories import BaseRepository
class InterviewRepository(BaseRepository):
    def update(self, interview, request):
        return BaseRepository.update(self, interview, request)
    
    def after_create(self, interview):
        candidate = interview.candidate
        job = interview.job
        update_request = {
            'candidate_details': {
                'name': candidate.full_name,
                'mobile': candidate.mobile_number,
            },
            'job_details': {
                'name': job.role_name,
                'job_code': job.job_code
            }
        }
        self.update(interview, update_request)
