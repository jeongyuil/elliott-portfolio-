
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import CurriculumUnit, Activity, Utterance
from app.services.prompt_builder import SessionContext, build_voice_instructions


def build_system_prompt(
    unit: CurriculumUnit | None,
    activity: Activity | None,
    child_name: str = "",
    child_age: int = 7,
    child_level: int = 1,
) -> str:
    """
    Construct system prompt using the 밤토리 3-character prompt system.

    Used by the REST API path (kid_sessions.py upload_utterance).
    The WebSocket path uses voice_proxy._build_instructions() which
    calls the same prompt_builder internally.
    """
    ctx = SessionContext(
        child_name=child_name,
        child_age=child_age,
        child_level=child_level,
        session_type="curriculum" if unit else "free_talk",
    )

    if unit:
        ctx.unit_title = unit.title or ""
        ctx.unit_description = unit.description or ""
        ctx.unit_week = unit.week or 0
        ctx.difficulty_level = unit.difficulty_level or 1
        ctx.korean_ratio = unit.korean_ratio if unit.korean_ratio is not None else 50
        ctx.target_skills = unit.target_skills or []

    if activity:
        ctx.activity_name = activity.name or ""
        ctx.activity_type = activity.activity_type or ""
        ctx.instructions_for_ai = activity.instructions_for_ai or ""
        ctx.story_content = activity.story_content or ""
        ctx.key_expression = activity.key_expression or ""

        # Inject intro script as story context so the AI knows what was shown
        # during the narrator_intro phase and continues from there
        if activity.intro_narrator_script and not ctx.story_content:
            ctx.story_content = (
                f"[직전 인트로에서 아이에게 보여준 내용 — 이 내용을 이어서 진행하세요]\n"
                f"{activity.intro_narrator_script}"
            )

    return build_voice_instructions(ctx)


async def get_conversation_history(
    db: AsyncSession,
    session_id,
) -> list[dict]:
    """Retrieve session conversation history and format for GPT"""
    stmt = (
        select(Utterance)
        .where(Utterance.session_id == session_id)
        .order_by(Utterance.turn_index)
    )
    result = await db.execute(stmt)
    utterances = result.scalars().all()

    history = []
    for u in utterances:
        # Map speaker_type to OpenAI role
        role = "assistant" if u.speaker_type == "ai" else "user"
        content = u.text_raw

        # Only include utterances that have text
        if content:
            history.append({"role": role, "content": content})

    return history
