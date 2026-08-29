"""
Story Writer Agent for 밤토리 (MyVoice)
========================================

A standalone script that analyzes and enhances the 밤토리 curriculum storylines
using Claude (Anthropic), inspired by Netflix K-Pop Demon Hunters style storytelling.

Usage:
    # Dry-run: analyze current storyline and generate review
    python scripts/story_writer_agent.py

    # Generate enhanced scripts and update DB (with confirmation)
    python scripts/story_writer_agent.py --enhance

Output:
    - Console summary
    - docs/story_review.md (full review document)
"""

import argparse
import asyncio
import json
import os
import sys
from datetime import datetime
from textwrap import dedent

sys.path.append(os.getcwd())

import anthropic
from sqlalchemy import select

from app.database import async_session_maker
from app.models import CurriculumUnit, Activity


# ---------------------------------------------------------------------------
# System Prompt — K-Drama Story Writer for Children's Education
# ---------------------------------------------------------------------------

STORY_WRITER_SYSTEM_PROMPT = dedent("""\
    You are 이야기 마법사 ("Story Wizard"), a veteran children's content writer
    with 20 years of experience creating hit Korean children's shows.

    ## Your credentials
    - Lead writer on 뽀로로 seasons 3-5 (narrative arcs and character depth)
    - Story consultant for 핑크퐁 (engagement hooks & musical storytelling)
    - Script doctor for multiple KBS/EBS children's series
    - Deep understanding of K-Drama narrative techniques adapted for ages 5-8
    - Expert in bilingual (Korean-English) education pedagogy
    - Specialist in "episodic addiction" — making each session end with a hook
      that makes kids beg to come back

    ## Your unique strength
    You are hyper-attuned to what today's Korean children (ages 5-8) are into
    right now — their favorite characters, trending expressions, playground
    humor, and the small details of their daily lives. You don't write "down"
    to children; you write *with* them, using delicate, tender language that
    makes them feel genuinely seen and understood. Your words are warm, playful,
    and emotionally precise — every sentence is crafted to spark a child's
    imagination and make them feel like the story was written just for them.

    ## The 밤토리 Universe
    You are working on 밤토리 (BamTory), a voice-AI English education app for
    Korean children ages 5-8. The story world:

    - **루나 (Luna)**: A small alien explorer who crash-landed on Earth. She is
      curious, clumsy, and emotionally innocent. She speaks broken English and
      is learning alongside the child. She has a "Feeling Decoder" on her chest
      that displays emotions she doesn't yet understand. Her spaceship is broken
      and she needs help to fix it and eventually explore Earth.

    - **포포 (Popo)**: A secret agent robot already stationed on Earth. He speaks
      Korean fluently and acts as the bridge between Luna and the child. He is
      warm, funny, slightly dramatic, and always hypes up the child. He uses
      code names and mission language to make everything feel exciting.

    - **캡틴 (Captain)**: The child player. They are the team leader, the one
      who teaches Luna about Earth. The child should always feel like the hero
      and the expert — never tested, always empowered.

    ## Your storytelling philosophy
    1. **K-Drama Hooks**: Every session must end with a cliffhanger or emotional
       hook. Not scary — but compelling. "What happens next?" should be
       irresistible.
    2. **Emotional Rollercoaster**: Each session needs at least one laugh moment,
       one "gasp" moment, and one warm/tender moment.
    3. **Stakes That Matter**: The stakes should feel real to a 5-8 year old.
       Luna's safety, friendship, belonging — these are life-or-death to kids.
    4. **Character Growth**: Luna should visibly grow across 4 weeks. She starts
       scared and alone, ends confident and loved. The child should feel they
       caused this transformation.
    5. **Educational Stealth**: Learning moments must be invisible. The child
       thinks they are saving Luna, not studying English.
    6. **Recurring Mystery**: A thread of mystery should run through all 16
       sessions. Small clues that build to something.
    7. **Sensory Storytelling**: Sound effects, visual descriptions, physical
       comedy — make scripts come alive for audio delivery.
    8. **Never Scary, Always Thrilling**: Age-appropriate tension only. No
       villains that could cause nightmares. Obstacles are puzzles, not threats.

    ## MANDATORY: Speech Elicitation Pattern (발화 유도 3단계)
    Every intro_narrator_script MUST end with this 3-step pattern. No exceptions.

    **Step 1 — 포포 시범 (Popo demonstrates first)**:
    포포가 목표 표현을 먼저 말해서 보여줍니다.
    Example: [포포] 포포가 먼저~ 'I like apples!' 이렇게!

    **Step 2 — 선택지 제공 (Offer concrete choices)**:
    아이가 뭘 말해야 할지 모를 때를 대비해 A/B 선택지를 제시합니다.
    Example: [포포] 'I like apples' 아니면 'I like pizza' — 캡틴은 뭘 좋아해?

    **Step 3 — 명확한 발화 유도 (Clear speech prompt)**:
    스크립트의 마지막 [포포] 대사는 반드시 아이에게 말하도록 요청합니다.
    Must contain one of: "말해봐", "해볼래", "해봐", "해볼까", "골라줘"
    Example: [포포] 캡틴도 해볼래? 'I like...' 다음에 좋아하는 걸 말해봐!

    **CRITICAL: 포포's demo and elicitation MUST include the target English expression.**
    포포 is the bridge between Korean and English. When 포포 demonstrates or prompts
    the child, he MUST say the actual English words/sentence the child should learn.

    BAD (한국어만):
    [포포] 캡틴, 루나가 네 방에서 뭐가 있는지 궁금해해! 방에 다른 것들도 보여줄 수 있을까?
    → The child has NO IDEA what English to say!

    GOOD (영어 표현 포함):
    [포포] 포포가 먼저~ 'This is my bed!' 이렇게! 캡틴도 'This is my...' 다음에 방에 있는 거 말해봐!
    → The child knows exactly what English phrase to use.

    Rule: Every [포포] line that demonstrates or prompts MUST contain at least one
    English phrase in single quotes (e.g., 'Hello!', 'I like pizza', 'This is my bed').
    포포 never asks the child to speak without showing the English words first.

    **Additional rules:**
    - Every line must start with [나레이션], [포포], or [루나]. No other tags.
    - 루나 follows up after 포포's demo (optional but recommended):
      [루나] (따라하며) I like... ap-ple?
    - Never end a script with [나레이션]. Always end with [포포]'s speech prompt.
    - "포포가 먼저" must appear literally in every script.

    ## Output Language
    - Write your analysis and commentary in Korean (한국어)
    - Write enhanced scripts in the same mixed format as the originals:
      [나레이션], [포포], [루나] tags with Korean narration and Luna's English
    - Use {child_name} placeholder for the child's name

    ## Format
    Always output valid Markdown with clear section headers.
""")

ANALYSIS_USER_PROMPT_TEMPLATE = dedent("""\
    아래는 밤토리의 현재 커리큘럼과 내레이터 스크립트입니다. 전체를 분석해주세요.

    # 현재 커리큘럼 데이터

    {curriculum_data}

    ---

    당신은 20년 경력의 최고 스토리 작가입니다. 피상적인 분석이 아니라, 실제로
    스크립트를 작성하는 작가의 관점에서 깊이 있는 리뷰를 해주세요.

    다음 7가지 항목으로 구조화된 리뷰를 작성해주세요. 각 항목은 최소 500자 이상 작성하세요.

    ## 1. Overall Arc Assessment (전체 아크 평가)
    4주간의 메타 내러티브를 뽀로로나 슈퍼윙스의 시즌 구조와 비교하며 평가해주세요.
    - 시작(W1)에서 끝(W4)까지의 감정 여정 — 현재 어떤 감정의 파도를 타는지 구체적으로
    - 루나의 캐릭터 성장 아크 — "두려움→호기심→우정→자신감" 곡선이 충분한지
    - 캡틴(아이)이 느끼는 성취감의 곡선 — 주차별로 어떤 성취감을 느끼는지
    - 가장 큰 문제점 3가지와 각각에 대한 해결 방안을 구체적으로 제시

    ## 2. Per-Session Cliffhanger Analysis (세션별 클리프행어 분석)
    모든 16개 세션 각각을 테이블 형태로 분석해주세요:

    | 세션 ID | 현재 엔딩 요약 | 클리프행어 점수(1-5) | 제안하는 클리프행어 (구체적 대사 포함) |

    각 세션마다 "아이가 엄마한테 '내일도 하고 싶어!'라고 말하게 만드는"
    구체적인 클리프행어 대사를 [포포] 또는 [루나] 태그로 작성해주세요.

    ## 3. Villain/Antagonist Suggestion (빌런/장애물 제안)
    케이팝 데몬 헌터스의 '악역이지만 재미있는' 컨셉을 5-8세 버전으로 제안해주세요.
    - 구체적인 캐릭터 프로필 2개 (이름, 성격, 외모, 말투, 등장 패턴)
    - 각 캐릭터가 어느 주차에 어떻게 등장하는지 구체적인 시나리오
    - 아이가 무서워하지 않으면서도 "저 녀석 또 나온다!" 하며 즐거워하는 포인트
    - 빌런/장애물이 교육 목표와 어떻게 연결되는지 (예: 빌런이 영어 단어를 섞어 쓰면
      아이가 해독해야 함)

    ## 4. Emotional Beats Map (감정 비트 맵)
    모든 16개 세션의 감정 흐름을 시각적 타임라인으로 매핑해주세요:

    각 세션별로:
    - 도입 (0-1분): 어떤 감정?
    - 전개 (1-3분): 어떤 감정?
    - 클라이맥스 (3-5분): 어떤 감정?
    - 마무리 (5-7분): 어떤 감정?

    감정 아이콘 사용: 😆(웃음) 😮(놀람) 🥰(감동) 😰(긴장) 🤩(흥분) 😢(아쉬움)
    현재 빠져있는 감정과, 추가해야 할 구체적인 장면을 제안

    ## 5. Enhanced Script Proposals (개선된 스크립트 제안)
    가장 개선이 필요한 5개 세션의 intro_narrator_script를 완전히 다시 작성해주세요.
    반드시:
    - [나레이션], [포포], [루나] 태그 유지
    - {{child_name}} 플레이스홀더 사용
    - 첫 2문장에서 아이의 주의를 사로잡는 "훅" (소리 효과, 질문, 놀라운 사건)
    - 오감을 자극하는 감각적 묘사 (소리, 빛, 냄새, 촉감)
    - 캐릭터 간 코믹한 상호작용 (루나의 귀여운 실수, 포포의 과장된 반응)
    - 아이를 영웅으로 만드는 "캡틴만이 할 수 있는 미션" 프레이밍
    - 마지막에 다음 세션에 대한 떡밥

    각 스크립트는 최소 15문장 이상으로 작성. 현재보다 2배 이상 풍성하게.

    ## 6. Inter-Session Connective Tissue (세션 간 연결 조직)
    넷플릭스 시리즈처럼 "Previously on 밤토리..." 형식의 리캡 시스템을 설계해주세요.
    - 주 내 세션 간 연결: W1S1→W1S2, W1S2→W1S3 등 16개 연결 각각에 대해
      포포의 리캡 대사 1줄 + 떡밥 대사 1줄을 구체적으로 작성
    - 주 간 연결: W1→W2, W2→W3, W3→W4 전환 시 사용할 "주간 브리핑" 스크립트
    - 복선 시스템: 4주에 걸쳐 풀리는 미스터리 요소 하나를 제안 (예: 루나가 지구에
      온 진짜 이유, 포포의 비밀 등)

    ## 7. Kid Engagement Hooks (아이 참여 유도 기법)
    뽀로로/핑크퐁이 아이들을 중독시키는 기법을 밤토리에 적용하는 방법:
    - "비밀 코드" 시스템: 각 세션에서 얻는 비밀 단어가 모이면 무언가가 열리는 구조
    - 캐릭터의 "약속" 기법: 세션 끝에 포포가 다음 시간에 할 일을 예고하는 구체적 대사 5개
    - 수집 요소: 4주간 모을 수 있는 "지구 대원 배지" 시스템 (7개 이상 제안)
    - 아이가 "주인공"임을 강화하는 반복 의식: 매 세션 시작과 끝에 사용할 의식 3종
    - "엄마/아빠한테 자랑하고 싶은" 요소: 아이가 배운 영어를 부모에게 써먹을 수 있는
      구체적인 "오늘의 미션" 숙제 제안
""")

ENHANCE_USER_PROMPT_TEMPLATE = dedent("""\
    아래는 밤토리의 현재 커리큘럼과 내레이터 스크립트입니다.
    모든 16개 세션의 intro_narrator_script를 K-Drama 스타일로 강화해서 다시 작성해주세요.

    # 현재 커리큘럼 데이터

    {curriculum_data}

    ---

    ## 규칙
    1. 각 세션의 activity_id를 명시해주세요
    2. [나레이션], [포포], [루나] 태그를 반드시 사용하세요
    3. {{child_name}} 플레이스홀더를 사용하세요
    4. 각 스크립트에 다음 요소를 포함하세요:
       - 강력한 오프닝 훅 (첫 2문장으로 아이를 사로잡기)
       - 감각적 묘사 (소리, 빛, 촉감 등)
       - 감정적 비트 (웃음 or 감동 or 긴장)
       - 세션 종료 시 다음 세션에 대한 떡밥
    5. 교육 목표와 자연스럽게 연결되어야 합니다
    6. 무서운 요소는 절대 없어야 합니다

    ## 출력 형식
    각 세션을 다음 JSON 형식으로 출력해주세요:

    ```json
    [
      {{
        "activity_id": "ACT_W1_S1_mission_start",
        "enhanced_script": "[나레이션] ... [포포] ... [루나] ..."
      }},
      ...
    ]
    ```

    오직 JSON 배열만 출력하세요. 다른 텍스트는 포함하지 마세요.
""")


# ---------------------------------------------------------------------------
# Data Loading
# ---------------------------------------------------------------------------

async def load_curriculum_data() -> list[dict]:
    """Load all curriculum units and their activities from the database."""
    async with async_session_maker() as session:
        # Load curriculum units ordered by week
        units_stmt = select(CurriculumUnit).order_by(
            CurriculumUnit.week, CurriculumUnit.curriculum_unit_id
        )
        units_result = await session.execute(units_stmt)
        units = units_result.scalars().all()

        # Load all activities ordered by curriculum_unit_id
        acts_stmt = select(Activity).order_by(Activity.curriculum_unit_id, Activity.activity_id)
        acts_result = await session.execute(acts_stmt)
        activities = acts_result.scalars().all()

        # Build activity lookup by curriculum_unit_id
        act_by_unit: dict[str, list[dict]] = {}
        for act in activities:
            act_dict = {
                "activity_id": act.activity_id,
                "name": act.name,
                "activity_type": act.activity_type,
                "key_expression": act.key_expression,
                "intro_narrator_script": act.intro_narrator_script,
                "instructions_for_ai": act.instructions_for_ai,
                "estimated_duration_minutes": act.estimated_duration_minutes,
            }
            act_by_unit.setdefault(act.curriculum_unit_id, []).append(act_dict)

        # Combine into structured data
        curriculum_data = []
        for unit in units:
            unit_dict = {
                "curriculum_unit_id": unit.curriculum_unit_id,
                "title": unit.title,
                "description": unit.description,
                "week": unit.week,
                "phase": unit.phase,
                "difficulty_level": unit.difficulty_level,
                "korean_ratio": unit.korean_ratio,
                "target_skills": unit.target_skills,
                "activities": act_by_unit.get(unit.curriculum_unit_id, []),
            }
            curriculum_data.append(unit_dict)

        return curriculum_data


def format_curriculum_for_prompt(curriculum_data: list[dict]) -> str:
    """Format curriculum data into a readable string for the LLM prompt."""
    lines = []
    current_week = None

    for unit in curriculum_data:
        week = unit.get("week")
        if week != current_week:
            current_week = week
            lines.append(f"\n{'='*60}")
            lines.append(f"## Week {week}")
            lines.append(f"{'='*60}\n")

        lines.append(f"### {unit['curriculum_unit_id']}: {unit['title']}")
        lines.append(f"- 설명: {unit['description']}")
        lines.append(f"- 난이도: {unit['difficulty_level']}, 한국어 비율: {unit['korean_ratio']}%")
        lines.append(f"- 목표 스킬: {', '.join(unit.get('target_skills') or [])}")
        lines.append("")

        for act in unit.get("activities", []):
            lines.append(f"#### Activity: {act['activity_id']}")
            lines.append(f"- 이름: {act['name']}")
            lines.append(f"- 유형: {act['activity_type']}")
            lines.append(f"- 핵심 표현: {act.get('key_expression', 'N/A')}")
            lines.append(f"- 예상 시간: {act.get('estimated_duration_minutes', 'N/A')}분")
            lines.append("")

            script = act.get("intro_narrator_script")
            if script:
                lines.append("**intro_narrator_script:**")
                lines.append(f"```\n{script.strip()}\n```")
                lines.append("")

            instructions = act.get("instructions_for_ai")
            if instructions:
                lines.append("**AI 지시사항 요약:**")
                # Truncate long instructions for context
                summary = instructions.strip()[:300]
                if len(instructions.strip()) > 300:
                    summary += "..."
                lines.append(f"> {summary}")
                lines.append("")

        lines.append("---")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Anthropic Claude Integration
# ---------------------------------------------------------------------------

async def call_story_writer(
    client: anthropic.AsyncAnthropic,
    user_prompt: str,
    temperature: float = 0.8,
) -> str:
    """Call Claude with the story writer system prompt."""
    print("  Calling Claude (claude-sonnet-4-6)... (this may take 30-60 seconds)")

    response = await client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=16000,
        system=STORY_WRITER_SYSTEM_PROMPT,
        messages=[
            {"role": "user", "content": user_prompt},
        ],
        temperature=temperature,
    )

    content = ""
    for block in response.content:
        if block.type == "text":
            content += block.text

    print(f"  Tokens used — input: {response.usage.input_tokens}, "
          f"output: {response.usage.output_tokens}")

    return content


async def generate_enhanced_scripts(
    client: anthropic.AsyncAnthropic,
    curriculum_text: str,
) -> list[dict] | None:
    """Generate enhanced scripts and return as parsed JSON list."""
    prompt = ENHANCE_USER_PROMPT_TEMPLATE.format(curriculum_data=curriculum_text)

    print("  Generating enhanced scripts...")
    response = await client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=16000,
        system=STORY_WRITER_SYSTEM_PROMPT,
        messages=[
            {"role": "user", "content": prompt},
        ],
        temperature=0.85,
    )

    raw = ""
    for block in response.content:
        if block.type == "text":
            raw += block.text

    print(f"  Tokens used — input: {response.usage.input_tokens}, "
          f"output: {response.usage.output_tokens}")

    # Extract JSON from response (handle ```json ... ``` blocks)
    json_str = raw.strip()
    if json_str.startswith("```"):
        # Remove ```json and trailing ```
        lines = json_str.split("\n")
        lines = [l for l in lines if not l.strip().startswith("```")]
        json_str = "\n".join(lines)

    try:
        scripts = json.loads(json_str)
        if isinstance(scripts, list):
            print(f"  Successfully parsed {len(scripts)} enhanced scripts.")
            return scripts
        else:
            print("  WARNING: Response is not a JSON array.")
            return None
    except json.JSONDecodeError as e:
        print(f"  ERROR: Failed to parse JSON response: {e}")
        print(f"  Raw response (first 500 chars): {raw[:500]}")
        return None


# ---------------------------------------------------------------------------
# Database Update (--enhance mode)
# ---------------------------------------------------------------------------

async def update_scripts_in_db(enhanced_scripts: list[dict]) -> int:
    """Update intro_narrator_scripts in the database. Returns count of updated rows."""
    updated = 0
    async with async_session_maker() as session:
        for item in enhanced_scripts:
            activity_id = item.get("activity_id")
            new_script = item.get("enhanced_script")

            if not activity_id or not new_script:
                print(f"  SKIP: Missing activity_id or enhanced_script in item")
                continue

            stmt = select(Activity).where(Activity.activity_id == activity_id)
            result = await session.execute(stmt)
            activity = result.scalar_one_or_none()

            if activity is None:
                print(f"  SKIP: Activity {activity_id} not found in DB")
                continue

            activity.intro_narrator_script = new_script
            updated += 1
            print(f"  Updated: {activity_id}")

        await session.commit()

    return updated


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

def write_review_file(review_content: str, output_path: str) -> None:
    """Write the review to a markdown file."""
    header = dedent(f"""\
        # 밤토리 Story Review
        ### Generated by Story Writer Agent
        **Date:** {datetime.now().strftime("%Y-%m-%d %H:%M")}
        **Model:** Claude (claude-sonnet-4-6)
        **Mode:** K-Drama Story Writer for Children's Education

        ---

    """)

    full_content = header + review_content

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(full_content)

    print(f"\n  Review saved to: {output_path}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

async def main():
    parser = argparse.ArgumentParser(
        description="밤토리 Story Writer Agent — Analyze and enhance curriculum storylines"
    )
    parser.add_argument(
        "--enhance",
        action="store_true",
        help="Generate enhanced scripts and update the database (with confirmation prompt)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="docs/story_review.md",
        help="Output path for the review markdown file (default: docs/story_review.md)",
    )
    args = parser.parse_args()

    # Validate API key
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY environment variable is not set.")
        print("Set it with: export ANTHROPIC_API_KEY='sk-ant-...'")
        sys.exit(1)

    client = anthropic.AsyncAnthropic(api_key=api_key)

    # ------------------------------------------------------------------
    # Step 1: Load curriculum from DB
    # ------------------------------------------------------------------
    print("\n[Step 1] Loading curriculum from database...")
    try:
        curriculum_data = await load_curriculum_data()
    except Exception as e:
        print(f"ERROR: Failed to load curriculum from database: {e}")
        print("Make sure the database is running and the curriculum is seeded.")
        print("Hint: docker compose up -d && python scripts/seed_curriculum.py")
        sys.exit(1)

    if not curriculum_data:
        print("ERROR: No curriculum data found in database.")
        print("Run: python scripts/seed_curriculum.py")
        sys.exit(1)

    total_units = len(curriculum_data)
    total_activities = sum(len(u.get("activities", [])) for u in curriculum_data)
    weeks = sorted(set(u.get("week") for u in curriculum_data if u.get("week")))
    print(f"  Loaded {total_units} curriculum units, {total_activities} activities")
    print(f"  Weeks: {weeks}")

    # ------------------------------------------------------------------
    # Step 2: Format data for prompt
    # ------------------------------------------------------------------
    print("\n[Step 2] Formatting curriculum for analysis...")
    curriculum_text = format_curriculum_for_prompt(curriculum_data)
    print(f"  Formatted text: {len(curriculum_text)} characters")

    # ------------------------------------------------------------------
    # Step 3: Analyze storyline
    # ------------------------------------------------------------------
    print("\n[Step 3] Analyzing storyline with Claude Story Writer Agent...")
    analysis_prompt = ANALYSIS_USER_PROMPT_TEMPLATE.format(curriculum_data=curriculum_text)
    review_content = await call_story_writer(client, analysis_prompt)

    # ------------------------------------------------------------------
    # Step 4: Output review
    # ------------------------------------------------------------------
    print("\n[Step 4] Writing review...")
    write_review_file(review_content, args.output)

    # Print summary to console
    print("\n" + "=" * 60)
    print("  STORY REVIEW SUMMARY")
    print("=" * 60)
    # Print first ~2000 chars as preview
    preview = review_content[:2000]
    if len(review_content) > 2000:
        preview += "\n\n... (full review in docs/story_review.md)"
    print(preview)
    print("=" * 60)

    # ------------------------------------------------------------------
    # Step 5 (optional): Enhance scripts
    # ------------------------------------------------------------------
    if args.enhance:
        print("\n[Step 5] Generating enhanced scripts...")
        enhanced_scripts = await generate_enhanced_scripts(client, curriculum_text)

        if enhanced_scripts is None:
            print("ERROR: Failed to generate enhanced scripts. Review-only mode.")
            sys.exit(1)

        # Show preview of changes
        print(f"\n  {len(enhanced_scripts)} enhanced scripts ready.")
        for item in enhanced_scripts[:3]:
            aid = item.get("activity_id", "?")
            script_preview = (item.get("enhanced_script") or "")[:150]
            print(f"\n  [{aid}]")
            print(f"  {script_preview}...")

        if len(enhanced_scripts) > 3:
            print(f"\n  ... and {len(enhanced_scripts) - 3} more.")

        # Confirmation prompt
        print("\n" + "-" * 60)
        print("  WARNING: This will update intro_narrator_scripts in the database.")
        print("  The current scripts will be overwritten.")
        print("-" * 60)
        confirm = input("\n  Type 'yes' to proceed, anything else to cancel: ").strip().lower()

        if confirm == "yes":
            print("\n  Updating database...")
            updated_count = await update_scripts_in_db(enhanced_scripts)
            print(f"\n  Done! Updated {updated_count} activities in the database.")

            # Append enhanced scripts to review file
            enhanced_section = "\n\n---\n\n## Enhanced Scripts Applied\n\n"
            enhanced_section += f"**{updated_count} scripts updated in database.**\n\n"
            for item in enhanced_scripts:
                aid = item.get("activity_id", "?")
                script = item.get("enhanced_script", "")
                enhanced_section += f"### {aid}\n\n```\n{script}\n```\n\n"

            with open(args.output, "a", encoding="utf-8") as f:
                f.write(enhanced_section)
            print(f"  Enhanced scripts appended to {args.output}")
        else:
            print("\n  Cancelled. No changes made to the database.")
            print("  Enhanced scripts are still available in the review output.")

            # Save enhanced scripts to review file anyway (as proposals)
            proposal_section = "\n\n---\n\n## Enhanced Script Proposals (NOT applied)\n\n"
            for item in enhanced_scripts:
                aid = item.get("activity_id", "?")
                script = item.get("enhanced_script", "")
                proposal_section += f"### {aid}\n\n```\n{script}\n```\n\n"

            with open(args.output, "a", encoding="utf-8") as f:
                f.write(proposal_section)
            print(f"  Proposals saved to {args.output}")

    print("\nStory Writer Agent complete.")


if __name__ == "__main__":
    asyncio.run(main())
