from app.models import BaseDocument
from typing_extensions import TypedDict
from typing import Annotated
from bson import ObjectId
from bunnet.odm.fields import PydanticObjectId
from pymongo import IndexModel, ASCENDING
from app.models.job import Job
from app.models.candidate import Candidate


class Transcript(TypedDict, total=False):
    question: str
    answer_url: str
    answer_txt: str
    score: float = 0.0

class Interview(BaseDocument):
    job_id: Annotated[ObjectId, PydanticObjectId]
    role: str
    transcript: list[Transcript] | None = None
    overall_score: float = 0.0
    summary: str | None = None
    candidate_id: Annotated[ObjectId, PydanticObjectId]
    
    class Settings:
        name = "interviews"
        validate_on_save = True
        use_state_management = True
        indexes = [
            IndexModel(
                [
                    ("job_id", ASCENDING)
                ],
                unique=False,
            ),
            IndexModel(
                [
                    ("candidate_id", ASCENDING)
                ],
                unique=False,
            )
        ]

    @property
    def job(self):
        return ~Job.get(self.job_id)
    
    @property
    def candidate(self):
        return ~Candidate.get(self.candidate_id)

Interview.model_rebuild
