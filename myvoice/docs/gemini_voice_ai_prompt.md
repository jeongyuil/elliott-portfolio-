# Phase 4A: Voice AI 학습 파이프라인 — 밤토리 (Bamtory) MVP

> **상태**: 📝 **프롬프트 작성 완료, 구현 대기**
> 이 프롬프트는 Auth 전면 개편 완료 후 Gemini에게 전달 예정입니다.
> 선행 조건: Auth 개편 플랜 승인 → 구현 → 완료 후 이 Phase 진행.

## 프로젝트 개요

밤토리는 4-12세 아이를 위한 Voice AI 영어 학습 앱입니다.
현재까지 Phase 1-3을 완료하여 프론트엔드 (React + Vite + TS)와 백엔드 (FastAPI + PostgreSQL)가 기본적으로 연동되어 있습니다.

**이번 Phase의 핵심 목표:**
현재 `AdventurePlay.tsx`는 브라우저 내장 Web Speech API로 단어 발음만 평가하는 프로토타입 상태입니다.
이것을 **서버사이드 Whisper STT + GPT-4o 대화 AI + TTS 음성 합성**의 실제 Voice AI 파이프라인으로 교체합니다.

**구현 범위:**
1. **백엔드**: OpenAI Whisper STT → GPT-4o Conversational AI → OpenAI TTS 파이프라인
2. **백엔드**: 세션 시작 시 Activity/TaskDefinition 기반 시나리오 로딩
3. **프론트엔드**: `AdventurePlay.tsx`를 실제 AI 대화 인터페이스로 업그레이드
4. **프론트엔드**: 마이크 녹음 → 서버 전송 → AI 응답 재생의 전체 루프
5. **Seed 데이터**: Week 1 커리큘럼의 Activity + TaskDefinition 시드

---

## 기술 스택

| 항목 | 선택 |
|------|------|
| STT | **OpenAI Whisper API** (`whisper-1`) |
| LLM | **GPT-4o** (Chat Completions API) |
| TTS | **OpenAI TTS** (`tts-1`, voice: `nova`) |
| 오디오 포맷 (업로드) | WebM (MediaRecorder) → 서버에서 Whisper로 전달 |
| 오디오 포맷 (재생) | MP3 (TTS 출력) |
| 상태 관리 | React useState + useRef |
| API 통신 | fetch (binary upload/download) |

---

## 현재 코드 상태 (반드시 참조)

### 백엔드 — 이미 존재하는 모델/라우터

#### 1. `app/models/session.py` — Session 모델 (이미 존재)
```python
class Session(Base):
    session_id: UUID (PK)
    child_id: UUID (FK → children)
    session_type: str  # "curriculum"
    curriculum_unit_id: str | None  # ← 이 필드로 모험과 연결
    status: str  # "idle" | "active" | "ended"
    start_time: datetime
    end_time: datetime | None
    duration_seconds: int | None
    raw_audio_path: str | None
    stt_processed: bool
    # Relationships
    activities = relationship("SessionActivity")
    utterances = relationship("Utterance")
```

#### 2. `app/models/utterance.py` — Utterance 모델 (이미 존재)
```python
class Utterance(Base):
    utterance_id: UUID (PK)
    session_id: UUID (FK → sessions)
    session_activity_id: UUID | None
    turn_index: int  # 턴 순서
    speaker_type: str  # "child" | "ai"
    text_raw: str | None  # STT 원본 텍스트
    text_normalized: str | None
    language: str | None  # "en" | "ko"
    pronunciation_score: float | None
    fluency_score: float | None
    emotion_label: str | None
    stt_engine: str | None  # "whisper-1"
    stt_confidence: float | None
    created_at: datetime
```

#### 3. `app/models/curriculum.py` — 커리큘럼 모델 (이미 존재)
```python
class CurriculumUnit(Base):  # = 모험 1개
    curriculum_unit_id: str (PK)
    title: str
    description: str | None
    phase: int
    week: int
    difficulty_level: int
    language_mode: str  # "mixed"
    korean_ratio: int  # 50 = 한국어 50%

class Activity(Base):  # = 모험 안의 활동 1개
    activity_id: str (PK)
    curriculum_unit_id: str
    name: str
    activity_type: str  # "mission_call" | "guided_conversation" | "pronunciation_drill" | "free_talk"
    instructions_for_ai: str | None  # GPT 시스템 프롬프트
    intro_narrator_script: str | None  # 내레이터 대사 (한국어)
    transition_trigger: str | None  # "child_response" | "auto"
    estimated_duration_minutes: int | None

class TaskDefinition(Base):  # = 활동 안의 개별 과제
    task_definition_id: UUID (PK)
    activity_id: str
    prompt_template: str | None  # GPT에게 보낼 프롬프트 템플릿
    expected_response_pattern: str | None
    difficulty_level: int
```

#### 4. `app/routers/kid_sessions.py` — 세션 라우터 (이미 존재, 수정 필요)
```python
# 현재 상태:
POST /v1/kid/sessions           → start_session (동작함)
POST /v1/kid/sessions/{id}/utterances  → upload_utterance (TODO: STT→LLM→TTS)
POST /v1/kid/sessions/{id}/end  → end_session (동작함)
```
⚠️ `upload_utterance`에 `# TODO: STT → LLM → TTS pipeline (M2)`로 표시되어 있음. 이것을 구현해야 합니다.

#### 5. `app/schemas/session.py` — 세션 스키마 (이미 존재, 수정 필요)
```python
class SessionCreate(BaseModel):
    child_id: UUID
    session_type: str = "curriculum"

class UtteranceRequest(BaseModel):
    audio_data: str  # Base64 encoded
    chunk_index: int | None
    is_final: bool = False

class UtteranceResponse(BaseModel):
    utterance_id: UUID
    ai_response_audio_url: str | None
    text_transcript: str | None
    speaker_type: str
```

#### 6. `app/config.py` — 설정 (이미 존재)
```python
class Settings(BaseSettings):
    openai_api_key: str = ""  # .env에서 OPENAI_API_KEY로 설정
    jwt_secret_key: str = "..."
    database_url: str = "postgresql+asyncpg://..."
```

### 프론트엔드 — 이미 존재하는 파일

#### 7. `frontend/src/pages/kid/AdventurePlay.tsx` (수정 필요)
- 현재: `missions` mock 데이터에서 시나리오 로드 + Web Speech API로 단어 발음 비교
- 변경: 서버에서 시나리오 로드 + 마이크 녹음 → 서버 전송 → AI 응답 수신 및 재생

#### 8. `frontend/src/pages/kid/AdventureDetail.tsx` (수정 필요)
- 현재: mock 데이터에서 모험 상세 표시
- 변경: 서버 API에서 모험 상세 + Activity 목록 로드

#### 9. `frontend/src/lib/speechRecognition.ts` (유지, 폴백용)
- Web Speech API 기반 발음 평가 (서버 AI 사용 불가 시 폴백으로 유지)

#### 10. `frontend/src/api/hooks/useAdventureDetail.ts` (수정 필요)
```typescript
// 현재: 단순 Adventure 타입 반환
// 변경: Activity 목록 포함한 상세 타입 반환
```

---

## 작업 목록

### 작업 1: OpenAI 서비스 모듈 생성

> `app/services/openai_service.py` [NEW]

OpenAI API와의 모든 상호작용을 캡슐화하는 서비스 모듈을 생성하세요.

```python
# app/services/openai_service.py

import io
from openai import AsyncOpenAI
from app.config import get_settings

settings = get_settings()
client = AsyncOpenAI(api_key=settings.openai_api_key)


async def transcribe_audio(audio_bytes: bytes, language: str = "en") -> dict:
    """Whisper STT: 오디오 → 텍스트 변환"""
    audio_file = io.BytesIO(audio_bytes)
    audio_file.name = "audio.webm"
    
    transcript = await client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file,
        language=language,
        response_format="verbose_json",  # word-level timestamps 포함
    )
    
    return {
        "text": transcript.text,
        "language": transcript.language,
        "duration": transcript.duration,
        "segments": transcript.segments if hasattr(transcript, 'segments') else [],
    }


async def chat_with_ai(
    system_prompt: str,
    conversation_history: list[dict],
    child_utterance: str,
) -> str:
    """GPT-4o: 대화형 AI 응답 생성"""
    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(conversation_history)
    messages.append({"role": "user", "content": child_utterance})
    
    response = await client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        temperature=0.7,
        max_tokens=200,  # 아이 대상이므로 짧은 응답
    )
    
    return response.choices[0].message.content


async def text_to_speech(text: str, voice: str = "nova") -> bytes:
    """TTS: 텍스트 → MP3 오디오 변환"""
    response = await client.audio.speech.create(
        model="tts-1",
        voice=voice,  # nova = 밝고 친근한 여성 목소리
        input=text,
        response_format="mp3",
    )
    
    return response.content
```

**주의사항:**
- `openai` 패키지 설치 필요: `pip install openai>=1.0`
- `.env`에 `OPENAI_API_KEY=sk-...` 설정 필요
- `AsyncOpenAI`를 사용 (FastAPI의 async와 호환)

---

### 작업 2: 대화 컨텍스트 매니저 생성

> `app/services/conversation_manager.py` [NEW]

세션 내 대화 기록을 관리하고, GPT에게 전달할 시스템 프롬프트를 구성하는 모듈입니다.

```python
# app/services/conversation_manager.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import CurriculumUnit, Activity, Utterance


def build_system_prompt(unit: CurriculumUnit, activity: Activity) -> str:
    """Activity의 instructions_for_ai와 커리큘럼 설정으로 시스템 프롬프트 구성"""
    
    base_prompt = f"""너는 4-12세 아이와 영어 학습을 하는 친근한 AI 캐릭터 '루나(Luna)'야.
    
## 현재 모험
- 제목: {unit.title}
- 설명: {unit.description}
- 한국어 비율: {unit.korean_ratio}% (나머지는 영어)
- 난이도: {unit.difficulty_level}/3

## 지침
{activity.instructions_for_ai or "자연스러운 대화를 통해 아이가 영어 단어와 문장을 연습하도록 유도해줘."}

## 규칙
1. 한국어와 영어를 {unit.korean_ratio}:{100 - unit.korean_ratio} 비율로 섞어서 말해
2. 문장은 짧고 간결하게 (최대 2-3문장)
3. 아이가 틀려도 격려하고, 올바른 표현을 자연스럽게 알려줘
4. 이모지를 적절히 사용해
5. 아이의 대답에 항상 반응하고, 다음 질문이나 활동으로 자연스럽게 이어가
"""
    return base_prompt


async def get_conversation_history(
    db: AsyncSession,
    session_id,
) -> list[dict]:
    """세션의 기존 대화 기록을 GPT 포맷으로 변환"""
    stmt = (
        select(Utterance)
        .where(Utterance.session_id == session_id)
        .order_by(Utterance.turn_index)
    )
    result = await db.execute(stmt)
    utterances = result.scalars().all()
    
    history = []
    for u in utterances:
        role = "assistant" if u.speaker_type == "ai" else "user"
        if u.text_raw:
            history.append({"role": role, "content": u.text_raw})
    
    return history
```

---

### 작업 3: kid_sessions 라우터 업그레이드

> `app/routers/kid_sessions.py` [MODIFY]

기존 `upload_utterance` 엔드포인트를 실제 STT → LLM → TTS 파이프라인으로 수정합니다.

**수정 사항:**

#### 3-1. `start_session` 수정 — curriculum_unit_id 연결
```python
@router.post("", response_model=SessionResponse, status_code=201)
async def start_session(
    req: SessionCreate,
    child_id: str = Depends(get_current_child_id),
    db: AsyncSession = Depends(get_db),
):
    """모험 시작: 세션 생성 + Activity 목록 반환"""
    session = Session(
        child_id=uuid.UUID(child_id),
        session_type=req.session_type,
        curriculum_unit_id=req.curriculum_unit_id,  # NEW: 어떤 모험인지
        status="active",
    )
    db.add(session)
    await db.flush()
    
    # Activity 목록도 함께 반환
    activities = []
    if req.curriculum_unit_id:
        stmt = select(Activity).where(
            Activity.curriculum_unit_id == req.curriculum_unit_id
        ).order_by(Activity.activity_id)
        result = await db.execute(stmt)
        activities = result.scalars().all()
    
    await db.commit()
    
    return SessionStartResponse(
        session_id=session.session_id,
        child_id=session.child_id,
        session_type=session.session_type,
        status=session.status,
        start_time=session.start_time,
        curriculum_unit_id=req.curriculum_unit_id,
        activities=[
            ActivityInfo(
                activity_id=a.activity_id,
                name=a.name,
                activity_type=a.activity_type,
                intro_narrator_script=a.intro_narrator_script,
                estimated_duration_minutes=a.estimated_duration_minutes,
            ) for a in activities
        ]
    )
```

#### 3-2. `upload_utterance` 전면 교체 — Voice AI 파이프라인

```python
@router.post("/{session_id}/utterances", response_model=UtteranceResponse)
async def upload_utterance(
    session_id: uuid.UUID,
    req: UtteranceRequest,
    child_id: str = Depends(get_current_child_id),
    db: AsyncSession = Depends(get_db),
):
    """아이 음성 → Whisper STT → GPT-4o → TTS → 응답"""
    import base64
    from app.services.openai_service import transcribe_audio, chat_with_ai, text_to_speech
    from app.services.conversation_manager import build_system_prompt, get_conversation_history
    
    # 1. 세션 검증
    result = await db.execute(
        select(Session).where(
            Session.session_id == session_id,
            Session.child_id == uuid.UUID(child_id),
            Session.status == "active",
        )
    )
    session = result.scalar_one_or_none()
    if not session:
        raise HTTPException(status_code=404, detail="Active session not found")
    
    # 2. 오디오 디코딩
    audio_bytes = base64.b64decode(req.audio_data)
    
    # 3. Whisper STT
    stt_result = await transcribe_audio(audio_bytes, language="en")
    child_text = stt_result["text"]

    # 4. 아이 발화 저장 (turn_index 계산)
    existing_count = await db.execute(
        select(func.count(Utterance.utterance_id))
        .where(Utterance.session_id == session_id)
    )
    turn_index = existing_count.scalar() or 0
    
    child_utterance = Utterance(
        session_id=session_id,
        turn_index=turn_index,
        speaker_type="child",
        text_raw=child_text,
        language=stt_result.get("language", "en"),
        stt_engine="whisper-1",
    )
    db.add(child_utterance)
    
    # 5. 대화 컨텍스트 구성
    unit = None
    activity = None
    if session.curriculum_unit_id:
        unit_result = await db.execute(
            select(CurriculumUnit).where(
                CurriculumUnit.curriculum_unit_id == session.curriculum_unit_id
            )
        )
        unit = unit_result.scalar_one_or_none()
        
        activity_result = await db.execute(
            select(Activity).where(
                Activity.curriculum_unit_id == session.curriculum_unit_id
            ).limit(1)
        )
        activity = activity_result.scalar_one_or_none()
    
    # 6. GPT-4o 대화
    system_prompt = build_system_prompt(unit, activity) if unit and activity else "You are a friendly English tutor for kids."
    conversation_history = await get_conversation_history(db, session_id)
    
    ai_response_text = await chat_with_ai(
        system_prompt=system_prompt,
        conversation_history=conversation_history,
        child_utterance=child_text,
    )
    
    # 7. AI 발화 저장
    ai_utterance = Utterance(
        session_id=session_id,
        turn_index=turn_index + 1,
        speaker_type="ai",
        text_raw=ai_response_text,
        language="mixed",
    )
    db.add(ai_utterance)
    
    # 8. TTS 생성
    tts_audio = await text_to_speech(ai_response_text)
    tts_base64 = base64.b64encode(tts_audio).decode("utf-8")
    
    await db.commit()
    
    return UtteranceResponse(
        utterance_id=ai_utterance.utterance_id,
        child_text=child_text,
        ai_response_text=ai_response_text,
        ai_response_audio_base64=tts_base64,
        turn_index=turn_index + 1,
        speaker_type="ai",
    )
```

---

### 작업 4: 스키마 업데이트

> `app/schemas/session.py` [MODIFY]

기존 스키마를 확장합니다.

```python
# app/schemas/session.py

from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import uuid


class SessionCreate(BaseModel):
    child_id: uuid.UUID
    session_type: str = "curriculum"
    curriculum_unit_id: str | None = None  # NEW


class ActivityInfo(BaseModel):
    activity_id: str
    name: str
    activity_type: str
    intro_narrator_script: str | None = None
    estimated_duration_minutes: int | None = None


class SessionStartResponse(BaseModel):
    session_id: uuid.UUID
    child_id: uuid.UUID
    session_type: str
    status: str
    start_time: datetime
    curriculum_unit_id: str | None = None
    activities: list[ActivityInfo] = []

    model_config = {"from_attributes": True}


class SessionEndResponse(BaseModel):
    duration_seconds: int
    engagement_score: Optional[float] = None
    total_turns: int = 0
    pronunciation_avg: Optional[float] = None


class UtteranceRequest(BaseModel):
    audio_data: str  # Base64 encoded WebM audio
    activity_id: str | None = None  # 현재 진행 중인 Activity
    is_final: bool = False


class UtteranceResponse(BaseModel):
    utterance_id: uuid.UUID
    child_text: str  # Whisper가 인식한 아이의 발화
    ai_response_text: str  # GPT가 생성한 AI 응답
    ai_response_audio_base64: str  # TTS 오디오 (Base64 MP3)
    turn_index: int
    speaker_type: str  # always "ai"
```

---

### 작업 5: Adventure Detail API 확장

> `app/routers/kid_adventures.py` [MODIFY]

`GET /v1/kid/adventures/{id}` 엔드포인트를 수정하여 Activity 목록을 포함합니다.

```python
@router.get("/{id}")
async def get_adventure_detail(
    id: str,  # curriculum_unit_id는 string
    child_id: UUID = Depends(get_current_child_id),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(CurriculumUnit).where(CurriculumUnit.curriculum_unit_id == id)
    result = await db.execute(stmt)
    unit = result.scalar_one_or_none()
    
    if not unit:
        raise HTTPException(status_code=404, detail="Adventure not found")
    
    # Activity 목록 가져오기
    activity_stmt = select(Activity).where(
        Activity.curriculum_unit_id == id
    ).order_by(Activity.activity_id)
    activity_result = await db.execute(activity_stmt)
    activities = activity_result.scalars().all()
    
    return {
        "id": unit.curriculum_unit_id,
        "title": unit.title,
        "description": unit.description,
        "emoji": "🚀",
        "difficulty": ["쉬움", "보통", "어려움"][min(unit.difficulty_level - 1, 2)],
        "duration": 600,
        "rewards": {"stars": 10, "xp": 50},
        "languageMode": unit.language_mode,
        "koreanRatio": unit.korean_ratio,
        "activities": [
            {
                "activityId": a.activity_id,
                "name": a.name,
                "activityType": a.activity_type,
                "introNarratorScript": a.intro_narrator_script,
                "estimatedDurationMinutes": a.estimated_duration_minutes,
            }
            for a in activities
        ]
    }
```

---

### 작업 6: Seed 데이터 확장 — Activity + TaskDefinition

> `app/seed.py` [MODIFY]

Week 1 모험 ("동물원 친구들 만나기")에 Activity와 TaskDefinition을 추가합니다.

```python
# seed.py에 추가할 데이터

ACTIVITIES = [
    # Week 1: 동물원 친구들 만나기
    {
        "activity_id": "W1-A1-mission-call",
        "curriculum_unit_id": None,  # seed 시 Week 1 unit의 ID로 대체
        "name": "루나의 미션 콜",
        "activity_type": "mission_call",
        "instructions_for_ai": """너는 '루나'라는 이름의 친근한 AI 캐릭터야.
동물원에 갔는데 동물 친구들이 영어 이름을 까먹었어!
아이에게 도움을 요청해. 
첫 번째로 강아지(dog)를 소개해줘.
한국어 70%, 영어 30%로 말해.""",
        "intro_narrator_script": "어느 날, 루나에게서 긴급 전화가 왔어요! 동물원 친구들이 영어 이름을 까먹었대요. 우리가 도와줄까요?",
        "transition_trigger": "child_response",
        "estimated_duration_minutes": 2,
    },
    {
        "activity_id": "W1-A2-guided-conversation",
        "curriculum_unit_id": None,
        "name": "동물 친구 소개하기",
        "activity_type": "guided_conversation",
        "instructions_for_ai": """아이와 함께 동물원의 동물들을 하나씩 소개하는 대화를 해.
대상 단어: dog, cat, lion, bear, rabbit
각 동물에 대해:
1. 한국어로 "이 친구는 누구지?" 질문
2. 아이가 영어로 대답하도록 유도
3. 맞으면 칭찬, 틀리면 힌트 제공
4. 다음 동물로 자연스럽게 이동
한국어 50%, 영어 50%로 말해.""",
        "intro_narrator_script": None,
        "transition_trigger": "auto",
        "estimated_duration_minutes": 5,
    },
    {
        "activity_id": "W1-A3-pronunciation-drill",
        "curriculum_unit_id": None,
        "name": "발음 연습",
        "activity_type": "pronunciation_drill",
        "instructions_for_ai": """아이의 영어 발음을 연습시켜줘.
단어: dog, cat, lion
각 단어를 또박또박 말해보도록 유도하고,
잘 따라하면 "Perfect! 👏" 칭찬해줘.
간단한 문장도 시도: "I see a dog!" """,
        "intro_narrator_script": "이제 동물 이름을 또박또박 말해볼까요?",
        "transition_trigger": "auto",
        "estimated_duration_minutes": 3,
    },
]

# seed_data() 함수 안에 Activity 시딩 추가
# Week 1의 curriculum_unit_id를 찾아서 Activity에 할당
```

---

### 작업 7: 프론트엔드 — 오디오 녹음 유틸리티

> `frontend/src/lib/audioRecorder.ts` [NEW]

MediaRecorder API를 사용하여 마이크 입력을 녹음하는 유틸리티를 생성합니다.

```typescript
// frontend/src/lib/audioRecorder.ts

export class AudioRecorder {
    private mediaRecorder: MediaRecorder | null = null;
    private audioChunks: Blob[] = [];
    private stream: MediaStream | null = null;

    async start(): Promise<void> {
        this.stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        this.mediaRecorder = new MediaRecorder(this.stream, {
            mimeType: "audio/webm;codecs=opus",
        });
        this.audioChunks = [];

        this.mediaRecorder.ondataavailable = (event) => {
            if (event.data.size > 0) {
                this.audioChunks.push(event.data);
            }
        };

        this.mediaRecorder.start();
    }

    stop(): Promise<Blob> {
        return new Promise((resolve) => {
            if (!this.mediaRecorder) {
                resolve(new Blob());
                return;
            }

            this.mediaRecorder.onstop = () => {
                const audioBlob = new Blob(this.audioChunks, { type: "audio/webm" });
                this.cleanup();
                resolve(audioBlob);
            };

            this.mediaRecorder.stop();
        });
    }

    private cleanup() {
        if (this.stream) {
            this.stream.getTracks().forEach((track) => track.stop());
            this.stream = null;
        }
        this.mediaRecorder = null;
        this.audioChunks = [];
    }

    get isRecording(): boolean {
        return this.mediaRecorder?.state === "recording";
    }
}

export async function blobToBase64(blob: Blob): Promise<string> {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onloadend = () => {
            const base64 = (reader.result as string).split(",")[1];
            resolve(base64);
        };
        reader.onerror = reject;
        reader.readAsDataURL(blob);
    });
}

export function playAudioFromBase64(base64: string): Promise<void> {
    return new Promise((resolve, reject) => {
        const audio = new Audio(`data:audio/mp3;base64,${base64}`);
        audio.onended = () => resolve();
        audio.onerror = () => reject(new Error("Audio playback failed"));
        audio.play();
    });
}
```

---

### 작업 8: 프론트엔드 — AdventurePlay.tsx 전면 리팩토링

> `frontend/src/pages/kid/AdventurePlay.tsx` [MODIFY — 전면 교체]

현재 mock 데이터 + Web Speech API 기반 코드를 **실제 Voice AI 대화 인터페이스**로 교체합니다.

**핵심 변경 사항:**
1. `missions` mock 데이터 import 제거 → API에서 모험 데이터 로드
2. Web Speech API (`startSpeechRecognition`) 제거 → `AudioRecorder`로 녹음 + 서버 전송
3. 단일 단어 발음 비교 → 멀티턴 대화 인터페이스
4. 대화 말풍선 UI 추가 (채팅 형태)

**UI 흐름:**

```
┌─────────────────────────────────┐
│  타이머    │  난이도  │  힌트     │  ← Top Bar (유지)
├─────────────────────────────────┤
│                                 │
│  🚀 캐릭터 이모지               │
│                                 │
│  [내레이터 스크립트 (한국어)]     │  ← intro_narrator_script
│                                 │
│  ┌──────────────────────┐       │
│  │ 🤖 루나: "안녕! ..."  │       │  ← AI 응답 말풍선
│  └──────────────────────┘       │
│            ┌───────────────┐    │
│            │ 👦 나: "Dog!" │    │  ← 아이 발화 말풍선
│            └───────────────┘    │
│  ┌──────────────────────┐       │
│  │ 🤖 루나: "맞아! ..."  │       │  ← AI 응답 말풍선
│  └──────────────────────┘       │
│                                 │
├─────────────────────────────────┤
│  [포기]    🎤 마이크    [힌트]   │  ← Bottom Controls
└─────────────────────────────────┘
```

**새로운 state 구조:**
```typescript
interface ConversationTurn {
    speaker: "narrator" | "ai" | "child";
    text: string;
    audioBase64?: string;
}

// State
const [sessionId, setSessionId] = useState<string | null>(null);
const [conversation, setConversation] = useState<ConversationTurn[]>([]);
const [isRecording, setIsRecording] = useState(false);
const [isProcessing, setIsProcessing] = useState(false);  // 서버 응답 대기
const [isPlayingAudio, setIsPlayingAudio] = useState(false);
```

**핵심 로직:**
```typescript
// 1. 페이지 진입 시: 세션 시작 + 내레이터 스크립트 표시
useEffect(() => {
    startAdventureSession();
}, []);

async function startAdventureSession() {
    // POST /v1/kid/sessions { curriculum_unit_id: id }
    const session = await api.post('/v1/kid/sessions', {
        child_id: childId,
        session_type: 'curriculum',
        curriculum_unit_id: id,
    });
    setSessionId(session.sessionId);
    
    // 내레이터 스크립트가 있으면 먼저 표시
    if (session.activities?.[0]?.introNarratorScript) {
        setConversation([{
            speaker: "narrator",
            text: session.activities[0].introNarratorScript,
        }]);
    }
}

// 2. 마이크 버튼 클릭: 녹음 시작/중지
async function handleMicPress() {
    if (isRecording) {
        // 녹음 중지 + 서버 전송
        const audioBlob = await recorder.stop();
        setIsRecording(false);
        setIsProcessing(true);
        
        const base64 = await blobToBase64(audioBlob);
        
        // POST /v1/kid/sessions/{sessionId}/utterances
        const response = await api.post(
            `/v1/kid/sessions/${sessionId}/utterances`,
            { audio_data: base64 },
            { headers: { 'X-Idempotency-Key': crypto.randomUUID() } }
        );
        
        // 아이 발화 추가
        setConversation(prev => [...prev, {
            speaker: "child",
            text: response.childText,
        }]);
        
        // AI 응답 추가
        setConversation(prev => [...prev, {
            speaker: "ai",
            text: response.aiResponseText,
            audioBase64: response.aiResponseAudioBase64,
        }]);
        
        // AI 음성 재생
        setIsPlayingAudio(true);
        await playAudioFromBase64(response.aiResponseAudioBase64);
        setIsPlayingAudio(false);
        
        setIsProcessing(false);
    } else {
        // 녹음 시작
        await recorder.start();
        setIsRecording(true);
    }
}

// 3. 세션 종료
async function handleEndSession() {
    await api.post(`/v1/kid/sessions/${sessionId}/end`);
    navigate(`/kid/adventure/${id}/result?success=true`);
}
```

**중요:** `mockData.ts`의 `missions` import를 완전히 제거하고, 모든 데이터를 API에서 가져오세요.

---

### 작업 9: AdventureDetail.tsx 수정

> `frontend/src/pages/kid/AdventureDetail.tsx` [MODIFY]

mock 데이터 대신 API에서 모험 상세를 가져오도록 수정합니다.

```typescript
// 변경 전:
import { missions } from "@/lib/mockData";
const mission = missions.find(m => m.id === missionId);

// 변경 후:
import { useAdventureDetail } from "@/api/hooks/useAdventureDetail";
const { data: adventure, isLoading } = useAdventureDetail(id!);
```

**API 반환 구조에 맞춰 렌더링 수정:**
- `mission.title` → `adventure.title`
- `mission.duration` → `adventure.duration`
- `mission.rewards.stars` → `adventure.rewards.stars`
- `mission.emoji` → `adventure.emoji`
- Activity 목록 표시 추가 (선택사항)

---

### 작업 10: API 타입 및 훅 업데이트

> `frontend/src/api/types.ts` [MODIFY]
> `frontend/src/api/hooks/useAdventureDetail.ts` [MODIFY]

```typescript
// types.ts에 추가
export interface AdventureDetail {
    id: string;
    title: string;
    description: string;
    emoji: string;
    difficulty: string;
    duration: number;
    rewards: { stars: number; xp: number };
    languageMode: string;
    koreanRatio: number;
    activities: ActivityInfo[];
}

export interface ActivityInfo {
    activityId: string;
    name: string;
    activityType: string;
    introNarratorScript: string | null;
    estimatedDurationMinutes: number | null;
}

export interface SessionStartResponse {
    sessionId: string;
    childId: string;
    sessionType: string;
    status: string;
    startTime: string;
    curriculumUnitId: string | null;
    activities: ActivityInfo[];
}

export interface ConversationResponse {
    utteranceId: string;
    childText: string;
    aiResponseText: string;
    aiResponseAudioBase64: string;
    turnIndex: number;
    speakerType: string;
}
```

```typescript
// useAdventureDetail.ts 수정
import type { AdventureDetail } from '../types';

export function useAdventureDetail(id: string) {
    return useQuery({
        queryKey: ['adventure', id],
        queryFn: () => api.get<AdventureDetail>(`/v1/kid/adventures/${id}`),
        enabled: !!id,
    });
}
```

---

## 검증 기준

### 1. 백엔드 테스트 (curl)
```bash
# .env에 OPENAI_API_KEY 설정 확인
echo "OPENAI_API_KEY=sk-..." >> .env

# 서버 시작
.venv/bin/uvicorn app.main:app --reload

# 1. 세션 시작
curl -X POST http://localhost:8000/v1/kid/sessions \
  -H "Authorization: Bearer $CHILD_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"child_id":"11111111-1111-1111-1111-111111111111","session_type":"curriculum","curriculum_unit_id":"<WEEK1_UNIT_ID>"}'
# → session_id, activities 배열 반환 확인

# 2. 발화 업로드 (테스트용 base64 오디오)
curl -X POST http://localhost:8000/v1/kid/sessions/<SESSION_ID>/utterances \
  -H "Authorization: Bearer $CHILD_TOKEN" \
  -H "Content-Type: application/json" \
  -H "X-Idempotency-Key: test-1" \
  -d '{"audio_data":"<BASE64_WEBM_AUDIO>"}'
# → child_text, ai_response_text, ai_response_audio_base64 반환 확인

# 3. 세션 종료
curl -X POST http://localhost:8000/v1/kid/sessions/<SESSION_ID>/end \
  -H "Authorization: Bearer $CHILD_TOKEN"
```

### 2. 프론트엔드 테스트 (브라우저)
1. `http://localhost:5173/kid/adventures` 접속
2. Week 1 모험 카드 클릭 → 모험 상세 페이지
3. "모험 시작하기" 클릭 → AdventurePlay 페이지
4. 마이크 버튼 클릭 → 녹음 시작 (빨간 불 표시)
5. "Hello" 또는 "Dog" 말하기 → 녹음 중지
6. 서버 응답 대기 (loading 표시)
7. AI 응답이 텍스트로 표시 + 음성으로 재생
8. 대화가 채팅 형태로 누적 표시

### 3. 빌드 확인
```bash
cd frontend && npm run build
# → 에러 없음
```

---

## ⛔ 금지 사항

- tRPC 사용 금지 (REST API만 사용)
- Web Speech API를 기본 STT로 사용 금지 (폴백으로만 유지)
- 동기(sync) OpenAI 클라이언트 사용 금지 (`AsyncOpenAI` 사용)
- `.env`에 API 키를 하드코딩하지 않되, 코드에서 키가 없을 때의 에러 핸들링 필수
- `mockData.ts`에서 데이터 import하지 않기 (API에서 가져오기)

---

## 디렉토리 변경 요약

```
app/
├── services/           [NEW 디렉토리]
│   ├── __init__.py
│   ├── openai_service.py      ← STT, Chat, TTS
│   └── conversation_manager.py ← 시스템 프롬프트, 대화 기록
├── routers/
│   ├── kid_sessions.py        ← [MODIFY] STT→GPT→TTS 파이프라인
│   └── kid_adventures.py      ← [MODIFY] Activity 목록 포함
├── schemas/
│   └── session.py             ← [MODIFY] 새 Request/Response 스키마
└── seed.py                    ← [MODIFY] Activity 시드 추가

frontend/src/
├── lib/
│   └── audioRecorder.ts       ← [NEW] 마이크 녹음 유틸리티
├── api/
│   ├── types.ts               ← [MODIFY] 새 타입 추가
│   └── hooks/
│       └── useAdventureDetail.ts ← [MODIFY] 상세 타입 변경
└── pages/kid/
    ├── AdventurePlay.tsx      ← [MODIFY] 전면 리팩토링
    └── AdventureDetail.tsx    ← [MODIFY] API 연동
```

## 의존성 설치

```bash
# 백엔드
pip install openai>=1.0

# 프론트엔드 (추가 패키지 없음 — 기존 fetch 사용)
```
