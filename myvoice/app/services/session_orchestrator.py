import json
import logging
from dataclasses import dataclass, asdict
from typing import Optional, List
from redis import asyncio as aioredis
from app.config import get_settings
from redis import asyncio as aioredis
from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()
redis = aioredis.from_url(f"redis://{settings.redis_host}:{settings.redis_port}", encoding="utf-8", decode_responses=True)

# Constants
SESSION_TTL = 7200 # 2 hours
SILENCE_TIMEOUT = 15 # sent by client, but we track last_interaction here if needed

class InvalidStateTransition(Exception):
    def __init__(self, message="Invalid state transition"):
        self.message = message
        super().__init__(self.message)

@dataclass
class SessionState:
    session_id: str
    status: str # idle, active, paused, ended
    phase: str # narrator_intro, transition, interactive
    last_interaction_ts: float = 0.0
    silence_count: int = 0

VALID_TRANSITIONS = {
    "idle": ["active"],
    "active": ["paused", "ended"],
    "paused": ["active", "ended"],
    "ended": [], # Terminal state
}

async def get_session_state(session_id: str) -> Optional[SessionState]:
    key = f"session:{session_id}:state"
    data = await redis.get(key)
    if not data:
        return None
    
    try:
        dict_data = json.loads(data)
        return SessionState(**dict_data)
    except Exception as e:
        logger.error(f"State deserialize error: {e}")
        return None

async def create_session_state(session_id: str):
    import time
    state = SessionState(
        session_id=session_id,
        status="idle",
        phase="narrator_intro", # Default start phase
        last_interaction_ts=time.time()
    )
    await _save_state(state)
    return state

async def transition_state(session_id: str, new_status: str):
    state = await get_session_state(session_id)
    if not state:
        await create_session_state(session_id) # Should usually exist, but safe fallback
        state = await get_session_state(session_id)
        
    valid_next = VALID_TRANSITIONS.get(state.status, [])
    if new_status != state.status and new_status not in valid_next:
        logger.warning(f"Invalid transition {state.status} -> {new_status}")
        raise InvalidStateTransition(f"Cannot transition from {state.status} to {new_status}")
    
    state.status = new_status
    import time
    state.last_interaction_ts = time.time()
    await _save_state(state)
    return state

async def advance_phase(session_id: str, new_phase: str):
    state = await get_session_state(session_id)
    if state:
        state.phase = new_phase
        await _save_state(state)

async def _save_state(state: SessionState):
    key = f"session:{state.session_id}:state"
    data = json.dumps(asdict(state))
    await redis.set(key, data, ex=SESSION_TTL)

# Silence / Timeout Logic
@dataclass
class SilenceEvent:
    should_pause: bool
    reprompt_text: Optional[str] = None

async def handle_silence(session_id: str) -> SilenceEvent:
    state = await get_session_state(session_id)
    if not state or state.status != "active":
        return SilenceEvent(False)
    
    state.silence_count += 1
    await _save_state(state)
    
    if state.silence_count >= 3:
        # Pause session
        await transition_state(session_id, "paused")
        return SilenceEvent(True, "너무 조용하네? 잠깐 쉬었다 할까?")
    
    # Re-prompt
    prompts = [
        "무슨 말인지 잘 못 들었어. 다시 말해줄래?",
        "괜찮아, 천천히 다시 이야기해봐! 👂",
        "루나가 듣고 있어! 🐾"
    ]
    idx = min(state.silence_count - 1, len(prompts) - 1)
    return SilenceEvent(False, prompts[idx])

async def reset_silence_counter(session_id: str):
    state = await get_session_state(session_id)
    if state:
        state.silence_count = 0
        import time
        state.last_interaction_ts = time.time()
        await _save_state(state)
        
async def check_transition_trigger(session_id: str, text: str) -> bool:
    """Phase 2 -> 3 Trigger Check"""
    text = text.lower().strip()
    triggers = ["go", "고", "시작", "start", "출발", "hello", "안녕"]
    
    for t in triggers:
        if t in text:
            await advance_phase(session_id, "interactive")
            return True
            
    return False
