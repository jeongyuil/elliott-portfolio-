from pydantic import BaseModel, ConfigDict
from datetime import datetime
from uuid import UUID
from typing import List, Optional

class SkillLevelResponse(BaseModel):
    skill_level_id: UUID
    child_id: UUID
    skill_id: str
    snapshot_date: datetime
    raw_score: Optional[float] = None
    level: int
    source: str
    
    model_config = ConfigDict(from_attributes=True)

class SkillListResponse(BaseModel):
    items: List[SkillLevelResponse]
