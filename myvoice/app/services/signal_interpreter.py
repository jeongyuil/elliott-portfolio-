"""
Signal Interpreter — Child Response Signal Extraction Layer

Core principle from 밤토리 Prompt System:
  "아이의 응답은 답이 아니라 신호(Signal)이다."

This lightweight layer converts raw child utterance into interpretable signals
that drive the Decision Engine (Popo) and Adaptive Difficulty system.

Signal flow:
  Raw utterance → Signal Interpreter → SessionContext.child_signal → Prompt Assembly
"""
from __future__ import annotations

import re
import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class ChildSignal:
    """Interpreted signal from child's response."""
    intent: str          # "self_expression", "answer", "question", "greeting", "silence", "playful", "avoidance", "safety_pass"
    emotion: str         # "happy", "excited", "neutral", "confused", "frustrated", "sad"
    engagement: str      # "high", "normal", "low"
    language_mix: str    # "korean_only", "english_only", "mixed", "unknown"
    word_count: int
    has_question: bool
    has_english: bool
    safety_pass: bool = False  # True when child says "패스" / "포포 도와줘"

    def to_dict(self) -> dict:
        return {
            "intent": self.intent,
            "emotion": self.emotion,
            "engagement": self.engagement,
            "language_mix": self.language_mix,
            "word_count": self.word_count,
            "has_question": self.has_question,
            "has_english": self.has_english,
            "safety_pass": self.safety_pass,
        }


# ---------------------------------------------------------------------------
# Korean pattern matchers
# ---------------------------------------------------------------------------

# "I don't know" patterns
_IDK_PATTERNS = re.compile(
    r"(몰라|모르겠|모르겠어|모르겠다|모르겠는데|모르지|몰라요|모르겠어요|i don.?t know|dunno|idk)",
    re.IGNORECASE,
)

# Question patterns
_QUESTION_PATTERNS = re.compile(
    r"(\?|뭐야|뭘|왜|어떻게|어디|누구|언제|뭐|what|why|how|where|who|when)",
    re.IGNORECASE,
)

# Positive emotion markers
_POSITIVE_MARKERS = re.compile(
    r"(ㅋㅋ|ㅎㅎ|하하|히히|좋아|재밌|신나|대박|우와|와|야호|yay|wow|cool|awesome|fun|haha|lol)",
    re.IGNORECASE,
)

# Frustration markers
_FRUSTRATION_MARKERS = re.compile(
    r"(싫어|안해|하기\s*싫|짜증|지루|심심|귀찮|no|don.?t want|boring|stop|hate)",
    re.IGNORECASE,
)

# English word detector (basic ASCII word check)
_ENGLISH_WORD = re.compile(r"[a-zA-Z]{2,}")

# Greeting patterns
_GREETING_PATTERNS = re.compile(
    r"^(안녕[\uac00-\ud7af]*|하이|헬로|hi|hello|hey|yo)\b",
    re.IGNORECASE,
)

# Laughter/sound patterns
_PLAYFUL_PATTERNS = re.compile(
    r"^(ㅋ{2,}|ㅎ{2,}|하하+|히히+|크크+|으아+|야+호+|haha+|lol+|hehe+)$",
    re.IGNORECASE,
)

# Safety Pass patterns — "패스", "포포 도와줘", "pass", "help me popo"
_SAFETY_PASS_PATTERNS = re.compile(
    r"(^패스$|패스해|패스할래|포포\s*도와|포포\s*도와줘|포포\s*도와주세요|포포\s*help|^pass$|help\s*me\s*popo)",
    re.IGNORECASE,
)


def interpret_signal(
    text: str,
    silence_count: int = 0,
    turn_count: int = 0,
) -> ChildSignal:
    """
    Interpret a child's utterance as a signal.

    This is a rule-based, fast interpreter (no LLM call).
    Runs synchronously — designed to add zero latency.

    Args:
        text: The child's raw utterance (from STT)
        silence_count: Number of consecutive silences before this utterance
        turn_count: Current turn number in session
    """
    text = text.strip()
    words = text.split()
    word_count = len(words)

    # --- Language mix ---
    has_english = bool(_ENGLISH_WORD.search(text))
    has_korean = bool(re.search(r"[\uac00-\ud7af]", text))

    if has_english and has_korean:
        language_mix = "mixed"
    elif has_english:
        language_mix = "english_only"
    elif has_korean:
        language_mix = "korean_only"
    else:
        language_mix = "unknown"

    has_question = bool(_QUESTION_PATTERNS.search(text))

    # --- Empty / silence ---
    if not text or text in ("(소리가 감지되지 않았어요)",):
        return ChildSignal(
            intent="silence",
            emotion="neutral",
            engagement="low",
            language_mix="unknown",
            word_count=0,
            has_question=False,
            has_english=False,
        )

    # --- Safety Pass (highest priority) ---
    safety_pass = bool(_SAFETY_PASS_PATTERNS.search(text))

    # --- Determine intent ---
    intent = "self_expression"  # default

    if safety_pass:
        intent = "safety_pass"
    elif _GREETING_PATTERNS.search(text):
        intent = "greeting"
    elif _PLAYFUL_PATTERNS.match(text):
        intent = "playful"
    elif _IDK_PATTERNS.search(text):
        intent = "avoidance"
    elif _FRUSTRATION_MARKERS.search(text):
        intent = "self_expression"  # frustration is self-expression, not answer
    elif has_question:
        intent = "question"
    elif word_count <= 3 and not has_question:
        intent = "answer"  # short answer

    # --- Determine emotion ---
    emotion = "neutral"

    if _POSITIVE_MARKERS.search(text):
        emotion = "happy"
    elif _FRUSTRATION_MARKERS.search(text):
        emotion = "frustrated"
    elif intent == "avoidance":
        emotion = "confused"
    elif intent == "question":
        emotion = "excited"  # curiosity signal

    # --- Determine engagement ---
    engagement = "normal"

    if word_count >= 8 or has_question or has_english:
        engagement = "high"
    elif word_count <= 1 or intent == "silence":
        engagement = "low"
    elif intent == "avoidance" and silence_count >= 1:
        engagement = "low"
    elif intent == "playful" or emotion == "happy":
        engagement = "high"

    signal = ChildSignal(
        intent=intent,
        emotion=emotion,
        engagement=engagement,
        language_mix=language_mix,
        word_count=word_count,
        has_question=has_question,
        has_english=has_english,
        safety_pass=safety_pass,
    )

    logger.debug(f"Child signal: {signal}")
    return signal
