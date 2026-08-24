from uuid import UUID

from pydantic import BaseModel
from app.schemas.base import CamelModel


class VocabularyCategoryResponse(CamelModel):
    id: str
    name: str
    emoji: str
    total_words: int
    words_learned: int


class VocabularyWordResponse(CamelModel):
    id: UUID
    word: str
    korean: str
    emoji: str

class VocabularyCompleteRequest(BaseModel):
    words_learned: int
    stars_earned: int
    xp_earned: int
