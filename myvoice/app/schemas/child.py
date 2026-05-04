"""Child request/response schemas."""
from pydantic import BaseModel, model_validator
from datetime import date
import uuid


class ChildCreate(BaseModel):
    name: str
    birth_date: date | None = None
    gender: str | None = None
    age: int | None = None  # Alternative to birth_date (converted to birth_date on server)
    interests: list[str] | None = None  # Stored as preferences_topics
    primary_language: str = "ko"
    development_stage_language: str | None = None
    avatar_id: str | None = None
    pin: str | None = None  # Optional PIN for Kids/Parent view switching


class ChildUpdate(BaseModel):
    name: str | None = None
    birth_date: date | None = None
    gender: str | None = None
    age: int | None = None
    interests: list[str] | None = None
    primary_language: str | None = None
    development_stage_language: str | None = None
    avatar_id: str | None = None
    pin: str | None = None


class ChildResponse(BaseModel):
    child_id: uuid.UUID
    family_id: uuid.UUID
    name: str
    birth_date: date
    gender: str | None = None
    primary_language: str
    development_stage_language: str | None = None
    avatar_id: str | None = None
    preferences_topics: dict | None = None
    interests: list[str] | None = None

    model_config = {"from_attributes": True}

    @model_validator(mode="after")
    def extract_interests(self):
        if self.preferences_topics and "interests" in self.preferences_topics:
            self.interests = self.preferences_topics["interests"]
        return self
