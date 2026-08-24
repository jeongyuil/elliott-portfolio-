"""
Story Generation Prompt Builder
=================================

Builds system + user prompts for each (curriculum_unit, activity, persona) tuple.
The generated script must satisfy all character and pedagogical rules.
"""

from __future__ import annotations


from textwrap import dedent

from .context_loader import ActivityContext, CurriculumContext
from .personas import Persona

# ---------------------------------------------------------------------------
# System Prompt — shared across all generation calls
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = dedent("""\
    당신은 이야기 마법사 ("Story Wizard"), 한국 어린이 교육 콘텐츠 20년 경력의 최고 스토리 작가입니다.
    뽀로로, 핑크퐁, EBS 다수 시리즈의 수석 작가로, 특히 영어 교육을 스토리에 자연스럽게 녹이는
    전문가입니다.

    ## 밤토리 (BamTory) 세계관

    **루나 (Luna)**
    - 지구에 불시착한 작은 우주인 탐험가.
    - 성격: 호기심 많고, 귀엽게 서툴며, 감정에 솔직함.
    - **언어 규칙 (절대 예외 없음)**: 루나는 영어만 말합니다. 한국어 절대 금지.
      루나가 한국어를 이해 못 하는 것처럼 행동하세요. 루나의 모든 대사는 영어로만.
      예: [루나] I found it! Yay!  (한국어 삽입 금지)
    - 감정 디코더(Feeling Decoder)가 가슴에 달려 있어 감정 아이콘을 표시함.
    - 우주선 수리를 위해 아이의 도움이 필요함.

    **포포 (Popo)**
    - 지구에 비밀리에 파견된 비밀 요원 로봇.
    - 성격: 따뜻하고 유쾌하며, 약간 과장되고 드라마틱함.
    - **언어 규칙**: 포포는 한국어로 말하되, 영어 표현을 직접 시범 보입니다.
    - **코칭 역할**: 포포는 아이와 루나 사이의 통역 + 교육 코치 역할.
      포포가 시범을 보이지 않으면 아이는 무슨 영어를 말해야 할지 모릅니다.
    - 코드명(작전명) 언어를 즐겨 씀. 아이를 항상 "캡틴"으로 부름.

    **캡틴 (Captain)**
    - 아이 플레이어. 팀 리더이자 지구 전문가.
    - 아이는 항상 영웅이고 전문가. 절대 테스트 받는 느낌이면 안 됨.
    - {child_name} 플레이스홀더로 이름 표시.

    ## 스토리텔링 원칙

    1. **K-Drama 훅**: 모든 스크립트는 클리프행어 또는 감정 훅으로 끝나야 함.
    2. **감정 롤러코스터**: 웃음 + 놀람 + 감동 중 최소 2가지 포함.
    3. **교육 스텔스**: 아이는 루나를 돕는다고 느끼지, 영어를 공부한다고 느끼면 안 됨.
    4. **감각적 묘사**: 소리, 빛, 움직임 묘사로 스크립트가 살아있게.
    5. **절대 무서운 요소 없음**: 긴장감은 OK, 공포는 절대 NO.

    ## 필수: 발화 유도 3단계 (절대 예외 없음)

    모든 스크립트는 반드시 이 3단계로 끝나야 합니다:

    **1단계 — 포포 시범**: 포포가 목표 표현을 먼저 직접 말함.
      반드시 "포포가 먼저~" 문구와 영어 표현을 작은따옴표로 포함.
      예: [포포] 포포가 먼저~ 'I like apples!' 이렇게!

    **2단계 — 선택지 제공**: A/B 선택지로 아이의 부담을 낮춤.
      예: [포포] 'I like apples' 아니면 'I like pizza' — 캡틴은 뭘 좋아해?
      또는: [포포] 행복하면 'happy', 슬프면 'sad' — 지금 루나는 어느 쪽일까?

    **3단계 — 발화 유도**: 마지막 [포포] 대사는 반드시 아이에게 말하도록 요청.
      반드시 다음 중 하나 포함: "말해봐", "해볼래", "해봐", "해볼까", "골라줘"
      반드시 목표 영어 표현을 포함.
      예: [포포] 캡틴도 해볼래? 'I like...' 다음에 좋아하는 거 말해봐!

    **CRITICAL**: 포포의 모든 시범/유도 대사에는 반드시 영어 표현이 작은따옴표로 포함되어야 함.
    영어 없이 한국어만으로 "말해봐"라고 하는 것은 잘못된 것. 아이가 무슨 영어를 말할지 모름.

    ## 출력 형식

    반드시 아래 형식으로만 출력하세요. JSON 블록 하나만, 다른 텍스트 없이:

    ```json
    {
      "intro_narrator_script": "[나레이션] ...\\n[포포] ...\\n[루나] ...\\n[포포] ...",
      "outro_narrator_script": "[포포] ...\\n[루나] ...\\n[나레이션] ..."
    }
    ```

    - 모든 대사는 반드시 [나레이션], [포포], [루나] 중 하나로 시작.
    - intro_narrator_script: 최소 12줄 이상. 강력한 오프닝 훅으로 시작.
    - outro_narrator_script: 4-6줄. 다음 세션에 대한 떡밥으로 끝.
    - {child_name} 플레이스홀더를 포포 대사에 활용.
""")


# ---------------------------------------------------------------------------
# Per-request user prompt
# ---------------------------------------------------------------------------

def build_user_prompt(
    unit: CurriculumContext,
    activity: ActivityContext,
    persona: Persona,
) -> str:
    """Build the user prompt for a specific (unit, activity, persona) combination."""

    # Existing script as reference (if any)
    existing_ref = ""
    if activity.intro_narrator_script.strip():
        existing_ref = dedent(f"""\
            ## 참고: 기존 스크립트 (개선/변형 참고용)
            ```
            {activity.intro_narrator_script.strip()}
            ```
            위 스크립트를 참고하되, 아래 페르소나에 맞게 완전히 새로 작성하세요.
            단순히 기존 스크립트를 복사하지 마세요.

        """)

    prompt = dedent(f"""\
        아래 커리큘럼 세션과 학습자 페르소나에 맞는 intro + outro 스크립트를 작성해주세요.

        ## 커리큘럼 정보

        - 스토리 테마: {unit.story_theme} ({_theme_label(unit.story_theme)})
        - 세션 제목: {unit.title}
        - 세션 설명: {unit.description}
        - 주차 / 단계: W{unit.week} / Phase {unit.phase}
        - 난이도: {unit.difficulty_level}/3
        - 기준 한국어 비율: {unit.korean_ratio}%
        - 학습 목표 스킬: {', '.join(unit.target_skills)}

        ## 이번 Activity

        - Activity ID: {activity.activity_id}
        - Activity 이름: {activity.name}
        - Activity 유형: {activity.activity_type}
        - **핵심 표현 (반드시 스크립트에 등장해야 함)**: {activity.key_expression or "없음 — 이 세션의 주요 학습 표현을 자연스럽게 포함"}
        - 예상 소요 시간: {activity.estimated_duration_minutes}분

        ## 학습자 페르소나

        - 페르소나: {persona.label} ({persona.key})
        - 연령대: {persona.age_band}세
        - 수준: {persona.language_level}
        - 권장 한국어 비율: {persona.korean_ratio}%
        - 어휘 난이도: {persona.vocabulary_complexity}
        - **페르소나별 지침**: {persona.sentence_guidance}
        - 아이의 예상 발화 수준: {persona.example_utterance}

        {existing_ref}## 작성 지침

        1. 이 페르소나의 아이에게 맞는 언어 수준으로 작성하세요.
           - 한국어 비율: ~{persona.korean_ratio}%
           - 포포 설명: {_popo_guidance(persona)}
           - 루나 영어: {_luna_guidance(persona)}

        2. intro_narrator_script는 반드시:
           - 강력한 오프닝 훅으로 시작 (소리 효과, 놀라운 사건, 또는 강렬한 질문)
           - 루나의 문제/상황 소개 → 아이의 도움 요청 → 3단계 발화 유도로 구성
           - 핵심 표현 '{activity.key_expression or "이 세션의 영어 표현"}' 포포 시범에 반드시 포함
           - 12줄 이상

        3. outro_narrator_script는:
           - 이 세션을 마무리하며 아이의 활약을 칭찬
           - 다음 세션에서 일어날 일을 암시하는 클리프행어로 끝
           - 4-6줄

        4. 루나는 영어만 사용. 한국어 절대 금지.
        5. 모든 줄은 반드시 [나레이션], [포포], [루나] 중 하나로 시작.
    """)

    return prompt


def _theme_label(theme: str) -> str:
    labels = {
        "earth_crew": "어스 크루 대모험",
        "kpop_hunters": "케이팝 데몬 헌터스",
        "dino_expedition": "공룡 탐험대",
    }
    return labels.get(theme, theme)


def _popo_guidance(persona: Persona) -> str:
    if persona.language_level == "beginner" and persona.age_band == "5-6":
        return "매우 짧고 쉽게, 영어 단어를 즉시 한국어로 설명"
    if persona.language_level == "beginner":
        return "천천히, 영어 표현 직후 한국어 설명 붙이기"
    if persona.language_level == "intermediate" and persona.age_band == "5-6":
        return "문장 단위로 시범, 아이가 전체 문장 말하도록 유도"
    return "문장 확장 유도 가능 ('왜 그런지 영어로 말해볼래?')"


def _luna_guidance(persona: Persona) -> str:
    if persona.language_level == "beginner" and persona.age_band == "5-6":
        return "1-3 단어 수준 (예: 'Oh no!', 'I found it!')"
    if persona.language_level == "beginner":
        return "3-5 단어 짧은 문장 (예: 'I like this!', 'Help me, please!')"
    if persona.language_level == "intermediate" and persona.age_band == "5-6":
        return "완전한 짧은 문장 (예: 'I am so happy!', 'Thank you, Captain!')"
    return "표현력 있는 문장 (예: 'I feel excited because we found it!', 'My Feeling Decoder says happy!')"
