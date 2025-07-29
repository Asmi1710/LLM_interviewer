from app.models import BaseDocument
from typing_extensions import TypedDict
from enum import Enum


class StatusEnum(str, Enum):
    created = "created"
    in_review = "in_review"
    approved = "approved"
    published = "published"
    unpublished = "unpublished"
    closed = "closed"
    discarded = 'discarded'

class LocationSchema(TypedDict, total=False):
    country: str | None
    state: str | None
    city: str | None
    pincode: str | None

class Job(BaseDocument):
    role_name: str
    years_of_experience: int = 0
    primary_skills: list[str] | None = None
    secondary_skills: list[str] | None = None
    minimum_salary: float = 0.0
    maximum_salary: float = 0.0
    decription: str | None = None
    location: LocationSchema | None = None
    status: StatusEnum = StatusEnum.created
    job_code: str | None = None

    class Settings:
        name = "jobs"
        validate_on_save = True
        use_state_management = True

Job.model_rebuild        