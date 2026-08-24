"""Session request/response schemas."""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
import uuid


class SessionStartRequest(BaseModel):
    session_type: str = "curriculum"
    curriculum_unit_id: Optional[str] = None


class ActivityInfo(BaseModel):
    activity_id: str
    name: str
    activity_type: str
    intro_narrator_script: Optional[str] = None
    outro_narrator_script: Optional[str] = None
    estimated_duration_minutes: Optional[int] = None
    image_path: Optional[str] = None # Added for Phase 5


class SessionResponse(BaseModel):
    """Legacy response model, kept for compatibility if needed, but SessionStartResponse is preferred."""
    session_id: uuid.UUID
    session_type: str
    status: str
    start_time: datetime
    
    model_config = {"from_attributes": True}


class SessionStartResponse(BaseModel):
    session_id: uuid.UUID
    child_id: uuid.UUID
    session_type: str
    status: str
    start_time: datetime
    curriculum_unit_id: Optional[str] = None
    activities: List[ActivityInfo] = []

    model_config = {"from_attributes": True}


class SessionEndResponse(BaseModel):
    duration_seconds: int
    engagement_score: Optional[float] = None
    total_turns: int = 0
    pronunciation_avg: Optional[float] = None
    earned_xp: int = 0
    new_level: int = 1
    level_up: bool = False


class UtteranceUploadRequest(BaseModel):# Was UtteranceRequest
    audio_data: Optional[str] = None  # Base64 encoded WebM audio
    text_input: Optional[str] = None  # Direct text input (bypass STT)
    activity_id: Optional[str] = None
    chunk_index: Optional[int] = None
    is_final: bool = False


class TTSRequest(BaseModel):
    text: str
    voice: str = "alloy"  # alloy, echo, fable, onyx, nova, shimmer
    character: str = "luna"  # luna, popo, narrator

class UtteranceFeedback(BaseModel):
    type: str  # excellent, good, try_again, neutral
    skill: str  # vocabulary, expression, pronunciation, confidence, none
    level: int  # 1, 2, 3
    message: str


class UtteranceResponse(BaseModel):
    utterance_id: uuid.UUID
    child_text: Optional[str] = None
    ai_response_text: Optional[str] = None
    ai_response_audio_base64: Optional[str] = None
    turn_index: int
    speaker_type: str
    text_transcript: Optional[str] = None  # Legacy field for compatibility
    feedback: Optional[UtteranceFeedback] = None
    next_phase: Optional[str] = None  # "transition" | "interactive" — tells frontend which phase to be in
