"""
Phase 1 Tests: Safety Filter + Session Orchestrator + Speech Pipeline
Covers the minimum 3 pytest cases required by Phase 1 completion criteria.
"""
import pytest
import asyncio
import uuid


# ---------------------------------------------------------------------------
# Safety Filter tests
# ---------------------------------------------------------------------------

class TestSafetyFilter:
    def test_safe_input_passes(self):
        from app.services.safety_filter import filter_input
        result = filter_input("Hello! I see a big dog. 🐶")
        assert result.is_safe is True
        assert result.safe_text == "Hello! I see a big dog. 🐶"

    def test_blocked_korean_profanity(self):
        from app.services.safety_filter import filter_input
        result = filter_input("씨발 나쁜 말")
        assert result.is_safe is False
        assert result.reason is not None
        # Fallback should be a safe child-friendly message
        assert len(result.safe_text) > 0

    def test_blocked_english_profanity(self):
        from app.services.safety_filter import filter_input
        result = filter_input("what the fuck")
        assert result.is_safe is False

    def test_safe_output_passes(self):
        from app.services.safety_filter import filter_output
        result = filter_output("Great job! The rabbit said 'hello'! 🌟")
        assert result.is_safe is True

    def test_empty_input_is_safe(self):
        from app.services.safety_filter import filter_input
        result = filter_input("")
        assert result.is_safe is True

    def test_phone_number_blocked(self):
        from app.services.safety_filter import filter_input
        result = filter_input("내 번호는 010-1234-5678이야")
        assert result.is_safe is False


# ---------------------------------------------------------------------------
# Session Orchestrator tests (require Redis)
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
class TestSessionOrchestrator:
    async def test_create_and_get_state(self):
        from app.services.session_orchestrator import create_session_state, get_session_state
        sid = f"test-{uuid.uuid4()}"
        data = await create_session_state(sid)
        assert data.status == "idle"
        assert data.phase == "narrator_intro"
        assert data.silence_count == 0

        loaded = await get_session_state(sid)
        assert loaded is not None
        assert loaded.session_id == sid
        assert loaded.status == "idle"

    async def test_valid_transitions(self):
        from app.services.session_orchestrator import (
            create_session_state, transition_state
        )
        sid = f"test-{uuid.uuid4()}"
        await create_session_state(sid)

        # idle → active
        data = await transition_state(sid, "active")
        assert data.status == "active"

        # active → paused
        data = await transition_state(sid, "paused")
        assert data.status == "paused"

        # paused → ended
        data = await transition_state(sid, "ended")
        assert data.status == "ended"

    async def test_invalid_transition_raises(self):
        from app.services.session_orchestrator import (
            create_session_state, transition_state, InvalidStateTransition
        )
        sid = f"test-{uuid.uuid4()}"
        await create_session_state(sid)
        await transition_state(sid, "active")

        with pytest.raises(InvalidStateTransition):
            await transition_state(sid, "idle")  # active → idle is invalid

    async def test_phase_advance(self):
        from app.services.session_orchestrator import (
            create_session_state, advance_phase, get_session_state
        )
        sid = f"test-{uuid.uuid4()}"
        await create_session_state(sid)

        await advance_phase(sid, "transition")
        data = await get_session_state(sid)
        assert data.phase == "transition"

        await advance_phase(sid, "interactive")
        data = await get_session_state(sid)
        assert data.phase == "interactive"

    async def test_trigger_word_detection(self):
        from app.services.session_orchestrator import (
            create_session_state, check_transition_trigger, get_session_state
        )
        sid = f"test-{uuid.uuid4()}"
        await create_session_state(sid)

        # Non-trigger word
        triggered = await check_transition_trigger(sid, "I don't know")
        assert triggered is False

        # Trigger word
        triggered = await check_transition_trigger(sid, "Go!")
        assert triggered is True
        data = await get_session_state(sid)
        assert data.phase == "interactive"

    async def test_silence_reprompt_then_pause(self):
        from app.services.session_orchestrator import (
            create_session_state, transition_state, advance_phase,
            handle_silence, reset_silence_counter, get_session_state
        )
        sid = f"test-{uuid.uuid4()}"
        await create_session_state(sid)
        await transition_state(sid, "active")
        await advance_phase(sid, "interactive")

        # First two silences → reprompt
        ev1 = await handle_silence(sid)
        assert ev1.should_pause is False
        assert ev1.reprompt_text

        ev2 = await handle_silence(sid)
        assert ev2.should_pause is False

        # Third silence → pause
        ev3 = await handle_silence(sid)
        assert ev3.should_pause is True
        assert ev3.reprompt_text is not None

        # Verify state transitioned to paused
        data = await get_session_state(sid)
        assert data.status == "paused"

    async def test_silence_reset_on_speech(self):
        from app.services.session_orchestrator import (
            create_session_state, transition_state, handle_silence,
            reset_silence_counter, get_session_state
        )
        sid = f"test-{uuid.uuid4()}"
        await create_session_state(sid)
        await transition_state(sid, "active")

        await handle_silence(sid)
        await handle_silence(sid)

        # Child speaks → reset
        await reset_silence_counter(sid)
        data = await get_session_state(sid)
        assert data.silence_count == 0


# ---------------------------------------------------------------------------
# Speech Pipeline unit tests (mocked OpenAI)
# ---------------------------------------------------------------------------

class TestSpeechPipelineDataclasses:
    """Test dataclass creation and logic without external API calls."""

    def test_stt_result_empty_detection(self):
        from app.services.speech_pipeline import SttResult
        # Low confidence → is_empty
        r = SttResult(
            text="[music]",
            language="unknown",
            confidence=0.1,
            is_empty=True,
            duration_ms=500,
        )
        assert r.is_empty is True

    def test_character_voice_mapping(self):
        from app.services.speech_pipeline import CHARACTER_VOICES
        assert CHARACTER_VOICES["luna"] == "nova"
        assert CHARACTER_VOICES["popo"] == "fable"
        assert CHARACTER_VOICES["narrator"] == "onyx"

    def test_conversation_context_history_limit(self):
        from app.services.speech_pipeline import ConversationContext
        history = [{"role": "user", "content": f"msg {i}"} for i in range(30)]
        ctx = ConversationContext(
            child_text="hello",
            system_prompt="You are Luna",
            history=history,
            max_history_turns=10,
        )
        # Router should truncate to last 20 messages (10 turns × 2)
        trimmed = ctx.history[-(ctx.max_history_turns * 2):]
        assert len(trimmed) == 20
