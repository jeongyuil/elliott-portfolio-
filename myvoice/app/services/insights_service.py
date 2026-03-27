"""
Insights Service — aggregates conversation data for parent insights dashboard.
Extracts keywords, sentiment trends, and activity timelines from Utterance/Session data.
"""
from collections import Counter
from datetime import datetime, timedelta
from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Session, Utterance


class InsightsService:

    @staticmethod
    async def get_keywords(
        db: AsyncSession, child_id: UUID, days: int = 30
    ) -> list[dict]:
        """
        Extract top keywords from child utterances.
        Returns list of {word, count} sorted by frequency.
        """
        since = datetime.utcnow() - timedelta(days=days)
        stmt = (
            select(Utterance.text_normalized)
            .join(Session, Session.session_id == Utterance.session_id)
            .where(
                Session.child_id == child_id,
                Utterance.speaker_type == "child",
                Utterance.text_normalized.isnot(None),
                Utterance.created_at >= since,
            )
        )
        result = await db.execute(stmt)
        texts = result.scalars().all()

        # Simple word frequency (skip short words)
        counter: Counter[str] = Counter()
        stop_words = {"the", "a", "an", "is", "are", "was", "were", "i", "me", "my",
                       "you", "he", "she", "it", "we", "they", "and", "or", "but",
                       "in", "on", "at", "to", "for", "of", "with", "do", "did",
                       "네", "응", "아", "음", "그", "이", "저", "것", "거", "좀"}
        for text in texts:
            words = text.lower().split()
            for word in words:
                cleaned = word.strip(".,!?;:\"'()[]")
                if len(cleaned) >= 2 and cleaned not in stop_words:
                    counter[cleaned] += 1

        return [{"word": w, "count": c} for w, c in counter.most_common(20)]

    @staticmethod
    async def get_sentiment_summary(
        db: AsyncSession, child_id: UUID, days: int = 30
    ) -> dict:
        """
        Aggregate emotion labels from utterances.
        Returns {emotions: [{label, count, percentage}], overall: str}
        """
        since = datetime.utcnow() - timedelta(days=days)
        stmt = (
            select(
                Utterance.emotion_label,
                func.count().label("cnt"),
            )
            .join(Session, Session.session_id == Utterance.session_id)
            .where(
                Session.child_id == child_id,
                Utterance.speaker_type == "child",
                Utterance.emotion_label.isnot(None),
                Utterance.created_at >= since,
            )
            .group_by(Utterance.emotion_label)
            .order_by(func.count().desc())
        )
        result = await db.execute(stmt)
        rows = result.all()

        total = sum(r.cnt for r in rows) or 1
        emotions = [
            {
                "label": r.emotion_label or "neutral",
                "count": r.cnt,
                "percentage": round(r.cnt / total * 100),
            }
            for r in rows
        ]

        overall = emotions[0]["label"] if emotions else "neutral"
        return {"emotions": emotions, "overall": overall}

    @staticmethod
    async def get_activity_timeline(
        db: AsyncSession, child_id: UUID, days: int = 14
    ) -> list[dict]:
        """
        Daily conversation activity for the last N days.
        Returns [{date, sessions, totalMinutes, totalTurns}]
        """
        since = datetime.utcnow() - timedelta(days=days)
        stmt = (
            select(
                func.date(Session.start_time).label("day"),
                func.count(Session.session_id).label("sessions"),
                func.coalesce(func.sum(Session.duration_seconds), 0).label("total_secs"),
            )
            .where(
                Session.child_id == child_id,
                Session.start_time >= since,
            )
            .group_by(func.date(Session.start_time))
            .order_by(func.date(Session.start_time))
        )
        result = await db.execute(stmt)
        rows = result.all()

        # Also get turn counts per day
        turns_stmt = (
            select(
                func.date(Utterance.created_at).label("day"),
                func.count(Utterance.utterance_id).label("turns"),
            )
            .join(Session, Session.session_id == Utterance.session_id)
            .where(
                Session.child_id == child_id,
                Utterance.speaker_type == "child",
                Utterance.created_at >= since,
            )
            .group_by(func.date(Utterance.created_at))
        )
        turns_result = await db.execute(turns_stmt)
        turns_map = {str(r.day): r.turns for r in turns_result.all()}

        return [
            {
                "date": str(r.day),
                "sessions": r.sessions,
                "totalMinutes": round(r.total_secs / 60),
                "totalTurns": turns_map.get(str(r.day), 0),
            }
            for r in rows
        ]

    @staticmethod
    async def get_language_mix(
        db: AsyncSession, child_id: UUID, days: int = 30
    ) -> dict:
        """
        Average Korean/English language mix ratio.
        """
        since = datetime.utcnow() - timedelta(days=days)
        stmt = (
            select(
                func.avg(Utterance.language_mix_ratio_ko).label("avg_ko"),
                func.avg(Utterance.language_mix_ratio_en).label("avg_en"),
                func.count().label("total"),
            )
            .join(Session, Session.session_id == Utterance.session_id)
            .where(
                Session.child_id == child_id,
                Utterance.speaker_type == "child",
                Utterance.created_at >= since,
            )
        )
        result = await db.execute(stmt)
        row = result.one()
        return {
            "koreanRatio": round((row.avg_ko or 0.5) * 100),
            "englishRatio": round((row.avg_en or 0.5) * 100),
            "totalUtterances": row.total,
        }

    @staticmethod
    async def get_behavior_patterns(
        db: AsyncSession, child_id: UUID, days: int = 30
    ) -> dict:
        """
        Behavioral patterns: avg session duration, engagement, pronunciation scores.
        """
        since = datetime.utcnow() - timedelta(days=days)

        session_stmt = (
            select(
                func.avg(Session.duration_seconds).label("avg_duration"),
                func.avg(Session.engagement_score).label("avg_engagement"),
                func.count().label("session_count"),
            )
            .where(
                Session.child_id == child_id,
                Session.start_time >= since,
                Session.duration_seconds.isnot(None),
            )
        )
        s_result = await db.execute(session_stmt)
        s_row = s_result.one()

        utt_stmt = (
            select(
                func.avg(Utterance.pronunciation_score).label("avg_pronunciation"),
                func.avg(Utterance.fluency_score).label("avg_fluency"),
                func.avg(Utterance.word_count).label("avg_words"),
            )
            .join(Session, Session.session_id == Utterance.session_id)
            .where(
                Session.child_id == child_id,
                Utterance.speaker_type == "child",
                Utterance.created_at >= since,
            )
        )
        u_result = await db.execute(utt_stmt)
        u_row = u_result.one()

        return {
            "avgSessionMinutes": round((s_row.avg_duration or 0) / 60, 1),
            "avgEngagement": round((s_row.avg_engagement or 0) * 100),
            "sessionCount": s_row.session_count,
            "avgPronunciation": round((u_row.avg_pronunciation or 0) * 100),
            "avgFluency": round((u_row.avg_fluency or 0) * 100),
            "avgWordsPerTurn": round(u_row.avg_words or 0, 1),
        }
