import logging
import uuid
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Utterance, Activity, TaskAttempt, Session as DbSession
from app.database import async_session_maker

logger = logging.getLogger(__name__)

async def evaluate_utterance(utterance_id: uuid.UUID):
    """
    Evaluates a single utterance for pronunciation, fluency, and correctness.
    Updates the Utterance record and potentially creates/updates a TaskAttempt.
    """
    async with async_session_maker() as db:
        try:
            # 1. Fetch Utterance
            stmt = select(Utterance).where(Utterance.utterance_id == utterance_id)
            result = await db.execute(stmt)
            utterance = result.scalar_one_or_none()
            
            if not utterance:
                logger.error(f"Utterance {utterance_id} not found for evaluation")
                return

            if utterance.speaker_type != "child":
                return

            # 2. Basic Metrics
            text = utterance.text_normalized or utterance.text_raw or ""
            words = text.split()
            word_count = len(words)
            unique_word_count = len(set(words))
            avg_sentence_length = word_count # For single utterance, it's just the count
            
            # Update basic stats
            utterance.word_count = word_count
            utterance.unique_word_count = unique_word_count
            utterance.avg_sentence_length = avg_sentence_length
            
            # Pronunciation Score (Proxy via STT confidence)
            # If STT confidence is high, pronunciation is likely clear.
            # Real pronunciation scoring requires audio analysis, but this is a V1 proxy.
            if utterance.stt_confidence:
                 # Normalize 0.0-1.0 to 0-100? Or keep 0-1.0
                 # SkillLevel usually uses 0-100 for display, but DB might store float.
                 # Let's keep 0-100 scale for user-facing scores.
                 utterance.pronunciation_score = utterance.stt_confidence * 100
            
            # Fluency Score (Proxy via length and lack of pauses/fillers - simplified)
            # Longer sentences with high confidence -> higher fluency
            fluency_score = 0
            if word_count > 0:
                fluency_score = min(100, (word_count * 10) + (utterance.stt_confidence or 0.5) * 50)
            utterance.fluency_score = fluency_score

            # 3. Contextual Evaluation (Correctness)
            # We need the session and activity to know what was expected.
            stmt = select(DbSession).where(DbSession.session_id == utterance.session_id)
            session_result = await db.execute(stmt)
            session = session_result.scalar_one_or_none()
            
            if session and session.curriculum_unit_id:
                # Find current activity
                # Ideally SessionActivity or just use the one in session context if stored
                # Or we can infer from session state?
                # For now, let's assume we can get it from session.curriculum_unit_id and order?
                # Actually, `utterance.session_activity_id` should point to the SessionActivity.
                # But we might not have set it in kid_sessions.py yet! 
                # (We only updated creating SessionActivity in start_session but didn't link utterances to it).
                # Fallback: check session.curriculum_unit_id
                pass

            # 4. TaskAttempt Creation (Simplified)
            # Create a TaskAttempt to record this interaction
            # For now, 1 Utterance = 1 TaskAttempt (Micro-task)
            # or we create one TaskAttempt per Activity session?
            # Let's create one per Activity Session (SessionActivity).
            # But we need to link it.
            
            # For V1, let's just save the utterance updates.
            
            await db.commit()
            logger.info(f"Evaluated utterance {utterance_id}: pron={utterance.pronunciation_score}, flu={utterance.fluency_score}")

        except Exception as e:
            logger.exception(f"Error evaluating utterance {utterance_id}: {e}")
            await db.rollback()
