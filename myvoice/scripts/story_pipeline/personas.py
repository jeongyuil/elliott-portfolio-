"""
Learner Personas for Story Pipeline
=====================================

Defines the variation axes for story generation:
  - age_band:        "5-6" or "7-8"
  - language_level:  "beginner" or "intermediate"

These map to child profiles tracked in Child.development_stage_language
and Skill.age_band in the production app.
"""

from __future__ import annotations


from dataclasses import dataclass


@dataclass(frozen=True)
class Persona:
    key: str
    label: str                    # Human-readable Korean label
    age_band: str                 # "5-6" or "7-8"
    language_level: str           # "beginner" or "intermediate"
    korean_ratio: int             # Suggested Korean ratio (0-100%)
    vocabulary_complexity: str    # "very_simple" | "simple" | "moderate"
    sentence_guidance: str        # Guidance injected into the prompt
    example_utterance: str        # Canonical example child utterance


PERSONAS: dict[str, Persona] = {
    "young_beginner": Persona(
        key="young_beginner",
        label="5-6세 초급",
        age_band="5-6",
        language_level="beginner",
        korean_ratio=80,
        vocabulary_complexity="very_simple",
        sentence_guidance=(
            "아이는 5-6세이며 영어를 거의 처음 접합니다. "
            "단어 하나 또는 두 단어 발화만 기대하세요 (예: 'apple', 'happy'). "
            "포포는 아주 천천히 말하고, 영어 단어를 한국어로 즉시 설명해줍니다. "
            "루나의 영어도 매우 짧고 단순해야 합니다 (예: 'I like... apple!'). "
            "나레이션은 짧고 쉬운 문장으로 작성하세요."
        ),
        example_utterance="'apple!' 또는 'happy!'",
    ),
    "young_intermediate": Persona(
        key="young_intermediate",
        label="5-6세 중급",
        age_band="5-6",
        language_level="intermediate",
        korean_ratio=65,
        vocabulary_complexity="simple",
        sentence_guidance=(
            "아이는 5-6세이며 기본 영어 문장을 말할 수 있습니다. "
            "2-4단어 짧은 문장을 기대하세요 (예: 'I like pizza'). "
            "포포는 목표 표현의 전체 문장을 시범보이고, 아이가 따라 말하도록 유도합니다. "
            "루나는 짧지만 완전한 문장을 씁니다 (예: 'I am happy!'). "
            "나레이션은 생동감 있게, 어휘는 일상 기본 수준을 유지하세요."
        ),
        example_utterance="'I like pizza!' 또는 'My name is...'",
    ),
    "older_beginner": Persona(
        key="older_beginner",
        label="7-8세 초급",
        age_band="7-8",
        language_level="beginner",
        korean_ratio=70,
        vocabulary_complexity="simple",
        sentence_guidance=(
            "아이는 7-8세이며 영어를 처음 배웁니다. "
            "짧은 문장(2-4단어)을 기대하지만, 나레이션은 조금 더 복잡해도 됩니다. "
            "포포는 목표 표현을 시범보이고 대안을 제시합니다. "
            "루나는 짧은 영어 문장을 씁니다. "
            "나레이션에 이야기 요소(놀라움, 궁금증)를 더 풍부하게 넣을 수 있습니다."
        ),
        example_utterance="'I like apples' 또는 'This is my bed'",
    ),
    "older_intermediate": Persona(
        key="older_intermediate",
        label="7-8세 중급",
        age_band="7-8",
        language_level="intermediate",
        korean_ratio=55,
        vocabulary_complexity="moderate",
        sentence_guidance=(
            "아이는 7-8세이며 기본 영어 문장 구성이 가능합니다. "
            "완전한 문장(3-6단어)을 기대하세요 (예: 'I feel happy today'). "
            "포포는 문장을 확장하는 방법도 제안할 수 있습니다 (예: '왜 happy인지 말해봐!'). "
            "루나는 감정 표현이나 상황 묘사를 포함한 문장을 씁니다. "
            "나레이션은 더 드라마틱하고 이야기 몰입도를 높이는 방향으로 쓰세요."
        ),
        example_utterance="'I feel happy because...' 또는 'The book is on the desk'",
    ),
}

ALL_PERSONA_KEYS = list(PERSONAS.keys())
