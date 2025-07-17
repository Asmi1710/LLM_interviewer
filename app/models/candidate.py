from pymongo import ASCENDING, IndexModel
from app.models import BaseDocument
from typing_extensions import TypedDict

class LocationSchema(TypedDict, total=False):
    country: str | None
    state: str | None
    city: str | None
    pincode: str | None

class Candidate(BaseDocument):
    full_name: str
    mobile_number: str
    email: str
    resume: str | None = None
    skills: list[str] = []
    experience_in_years: float = 0.0
    current_ctc: float | None = None
    expected_ctc: float | None = None
    current_location: LocationSchema | None = None
    open_for_locations: list[LocationSchema] = []
    notice_period_in_days: str | None = None

    class Settings:
        name = "candidates"
        validate_on_save = True
        use_state_management = True
        indexes = [
            IndexModel(
                [
                    ("mobile_number", ASCENDING),
                ],
                unique=True,
                name="index_mobile"
            ),
            IndexModel(
                [
                    ("mobile_number", ASCENDING),
                ],
                unique=True,
                name="index_email"
            )
        ]

Candidate.model_rebuild