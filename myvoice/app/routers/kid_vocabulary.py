import base64
import logging

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from uuid import UUID

from app.database import get_db
from app.core.security import get_current_child_id
from app.models import VocabularyCategory, VocabularyWord, VocabularyProgress, ChildInventory, WeeklyGoal, Child
from app.schemas.vocabulary import VocabularyCategoryResponse, VocabularyWordResponse, VocabularyCompleteRequest
from app.services.speech_pipeline import text_to_speech

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("", response_model=list[VocabularyCategoryResponse])
async def get_vocabulary_categories(
    child_id: UUID = Depends(get_current_child_id),
    db: AsyncSession = Depends(get_db)
):
    # Get all categories
    stmt = select(VocabularyCategory).order_by(VocabularyCategory.sort_order)
    result = await db.execute(stmt)
    categories = result.scalars().all()
    
    # Get progress for this child
    progress_stmt = select(VocabularyProgress).where(VocabularyProgress.child_id == child_id)
    progress_result = await db.execute(progress_stmt)
    progress_map = {p.category_id: p.words_learned for p in progress_result.scalars()}
    
    response = []
    for cat in categories:
        response.append(VocabularyCategoryResponse(
            id=cat.id,
            name=cat.name,
            emoji=cat.emoji,
            total_words=cat.total_words,
            words_learned=progress_map.get(cat.id, 0)
        ))
        
    return response

class WordTTSRequest(BaseModel):
    text: str


@router.post("/tts")
async def vocabulary_tts(
    request: WordTTSRequest,
    _child_id: UUID = Depends(get_current_child_id),
):
    """Generate TTS for a vocabulary word (no session required)."""
    try:
        audio_bytes = await text_to_speech(request.text, character="luna")
        audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")
        return {"audio_base64": audio_base64}
    except Exception:
        logger.exception("Vocabulary TTS failed")
        raise HTTPException(status_code=502, detail="TTS generation failed")


@router.get("/{category_id}/words", response_model=list[VocabularyWordResponse])
async def get_vocabulary_words(
    category_id: str,
    child_id: UUID = Depends(get_current_child_id),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(VocabularyWord).where(
        VocabularyWord.category_id == category_id
    ).order_by(VocabularyWord.sort_order)
    result = await db.execute(stmt)
    words = result.scalars().all()
    
    return [VocabularyWordResponse.model_validate(w) for w in words]

@router.post("/{category_id}/complete")
async def complete_vocabulary_category(
    category_id: str,
    req: VocabularyCompleteRequest,
    child_id: UUID = Depends(get_current_child_id),
    db: AsyncSession = Depends(get_db)
):
    # 1. Update/Create Progress
    stmt = select(VocabularyProgress).where(
        VocabularyProgress.child_id == child_id,
        VocabularyProgress.category_id == category_id
    )
    result = await db.execute(stmt)
    progress = result.scalar_one_or_none()
    
    if not progress:
        progress = VocabularyProgress(
            child_id=child_id, 
            category_id=category_id, 
            words_learned=0
        )
        db.add(progress)
    
    # Only update if new words learned (simplification)
    # In real app, we'd track specific words
    progress.words_learned = max(progress.words_learned, req.words_learned)
    
    # 2. Update Inventory (Rewards)
    inv_stmt = select(ChildInventory).where(ChildInventory.child_id == child_id)
    inv_result = await db.execute(inv_stmt)
    inventory = inv_result.scalar_one_or_none()
    
    if inventory:
        inventory.stars += req.stars_earned
        
    # 3. Update Child XP
    child_stmt = select(Child).where(Child.child_id == child_id)
    child_result = await db.execute(child_stmt)
    child = child_result.scalar_one()
    child.xp += req.xp_earned

    # 4. Update Weekly Goal
    # ... (omitted for brevity, similar logic to inventory)
    
    await db.commit()
    return {"status": "success"}
