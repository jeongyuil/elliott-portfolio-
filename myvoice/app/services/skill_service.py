import logging
import uuid
from datetime import datetime, time
from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Utterance, SkillLevel, Skill
from app.database import async_session_maker

logger = logging.getLogger(__name__)

async def calculate_skill_levels(child_id: str):
    """
    Aggregates child's performance and updates SkillLevel snapshots.
    """
    async with async_session_maker() as db:
        try:
            logger.info(f"Calculating skill levels for child {child_id}")
            child_uuid = uuid.UUID(child_id)
            # Use midnight for snapshot date to allow one per day
            today = datetime.combine(datetime.utcnow().date(), time.min)

            # 1. Vocabulary (Unique Words)
            # Fetch all child utterances
            stmt = select(Utterance.text_normalized).where(
                and_(Utterance.speaker_type == "child", Utterance.text_normalized.is_not(None))
            ).join(Utterance.session).where(Utterance.session.has(child_id=child_uuid))
            
            # Note: joining Utterance.session is tricky if relationship is not loaded or lazy
            # Better to join explicitly:
            # select(Utterance.text_normalized).join(Session, Utterance.session_id == Session.session_id).where(...)
            # 1. Vocabulary (Unique Words) -> LANG_VOCAB_DAILY_01
            from app.models import Session
            stmt = select(Utterance.text_normalized).join(Session, Utterance.session_id == Session.session_id).where(
                Session.child_id == child_uuid,
                Utterance.speaker_type == "child", 
                Utterance.text_normalized.is_not(None)
            )
            result = await db.execute(stmt)
            texts = result.scalars().all()
            
            all_words = set()
            for t in texts:
                all_words.update(t.lower().split())
            
            vocab_count = len(all_words)
            # Map count to 0-100 score for frontend display (approximate)
            # Goal: 100 words = 100 score? Or mapped to level.
            # Frontend uses 0-100 for score_0_100 unit.
            vocab_score = min(100, vocab_count) 
            vocab_level = _map_vocab_to_level(vocab_count)
            
            await _update_skill_snapshot(db, child_uuid, "LANG_VOCAB_DAILY_01", vocab_level, vocab_score, today)

            # 2. Pronunciation (Average Score) -> LANG_PRON_BASIC_01
            stmt = select(func.avg(Utterance.pronunciation_score)).join(Session, Utterance.session_id == Session.session_id).where(
                Session.child_id == child_uuid,
                Utterance.speaker_type == "child",
                Utterance.pronunciation_score.is_not(None)
            )
            result = await db.execute(stmt)
            pron_avg = result.scalar() or 0.0
            pron_level = _map_score_to_level(pron_avg)

            await _update_skill_snapshot(db, child_uuid, "LANG_PRON_BASIC_01", pron_level, pron_avg, today)

            # 3. Fluency (Average Score) -> LANG_SENT_BASIC_SVO_01 (Proxy)
            stmt = select(func.avg(Utterance.fluency_score)).join(Session, Utterance.session_id == Session.session_id).where(
                Session.child_id == child_uuid,
                Utterance.speaker_type == "child",
                Utterance.fluency_score.is_not(None)
            )
            result = await db.execute(stmt)
            fluency_avg = result.scalar() or 0.0
            fluency_level = _map_score_to_level(fluency_avg)

            await _update_skill_snapshot(db, child_uuid, "LANG_SENT_BASIC_SVO_01", fluency_level, fluency_avg, today)

            # 4. Consistency (Days active / Sessions count)
            # Simple count for now
            # 4. Consistency (Sessions) -> COGN_ATTENTION_SESSION_01
            stmt = select(func.count(Session.session_id)).where(Session.child_id == child_uuid)
            session_count = (await db.execute(stmt)).scalar() or 0
            # Map to 1-5 level
            consistency_level = min(5, (session_count // 5) + 1)

            await _update_skill_snapshot(db, child_uuid, "COGN_ATTENTION_SESSION_01", consistency_level, session_count, today)

            await db.commit()
            logger.info("Skill levels updated successfully")

        except Exception as e:
            logger.exception(f"Error calculating skill levels: {e}")
            await db.rollback()

async def _update_skill_snapshot(db, child_id, skill_name, level, raw_score, snapshot_date):
    # Find skill_id first (assuming skill names are standard)
    # We might need to seed Skills table first? 
    # Or assume they exist. Let's assume they exist or we create them.
    # For MVP, checking simply by name in known list.
    
    # Check if Skill exists
    stmt = select(Skill).where(Skill.name == skill_name)
    result = await db.execute(stmt)
    skill = result.scalar_one_or_none()
    
    if not skill:
        # Create skill on the fly? Or fail.
        # Let's create.
        skill = Skill(
            skill_id=str(uuid.uuid4()), # Assuming string ID
            name=skill_name,
            category="core",
            mode="auto"
        )
        db.add(skill)
        await db.flush() # to get ID if needed, though we set it
        
    # Check if snapshot exists for today
    stmt = select(SkillLevel).where(
        SkillLevel.child_id == child_id,
        SkillLevel.skill_id == skill.skill_id,
        SkillLevel.snapshot_date == snapshot_date
    )
    result = await db.execute(stmt)
    snapshot = result.scalar_one_or_none()
    
    if snapshot:
        snapshot.level = level
        snapshot.raw_score = raw_score
    else:
        snapshot = SkillLevel(
            child_id=child_id,
            skill_id=skill.skill_id,
            level=level,
            raw_score=raw_score,
            snapshot_date=snapshot_date
        )
        db.add(snapshot)

def _map_vocab_to_level(count):
    if count < 5: return 1
    if count < 20: return 2
    if count < 50: return 3
    if count < 100: return 4
    return 5

def _map_score_to_level(score):
    # Score 0-100
    if score < 20: return 1
    if score < 40: return 2
    if score < 60: return 3
    if score < 80: return 4
    return 5
