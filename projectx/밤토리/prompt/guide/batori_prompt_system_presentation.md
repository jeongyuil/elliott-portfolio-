
# 밤토리 프롬프트 시스템 아키텍처 (Batori Prompt System Architecture)
## 지속 가능한 콘텐츠 엔진을 위한 엔지니어링 가이드

---

# 0. 핵심 철학: 스토리 우선 (Story-First) 설계

### "당신의 아이가 동화책의 주인공이 됩니다."

우리는 교육을 위해 재미없는 스토리를 만드는 것이 아니라, **'재미있는 동화'** 속에 아이를 주인공으로 초대합니다.

| 기존 방식 (Textbook-First) | **밤토리 방식 (Story-First)** |
|---|---|
| 교육 목표에 맞춰 대사를 억지로 낌 | 작가 집필 **고퀄리티 스토리** (불변의 뼈대) |
| AI가 전체 스토리를 생성 (일관성 부족) | **AI는 '즉흥 연기'만 담당** (상호작용) |
| 아이는 관찰자(Observer)에 머무름 | **아이는 주인공(Protagonist)이 되어 참여** |

> **워크플로우:**
> 1.  **Human Writer:** 재미있는 '골든 스토리' 집필 (Plot)
> 2.  **AI System:** 스토리 사이사이의 **'티키타카(Interaction)'** 빈칸을 채움
> 3.  **Result:** 내 아이가 주인공이 되는, 살아있는 동화책

---

# 0.1 창작 도구 vs 실행 도구 (Why Document Writer Prompts?)

"작가님이 스토리를 쓸 때 사용하는 프롬프트도 왜 시스템에 포함되나요?"

| 구분 | **스토리 창작 프롬프트 (Design-Time)** | **런타임 시스템 프롬프트 (Run-Time)** |
| :--- | :--- | :--- |
| **비유** | **시나리오 작가 & 감독** | **배우 (AI) & 현장 스태프** |
| **역할** | 재미있는 이야기와 교육적 상황을 **'설계'**함 | 설계된 상황 속에서 아이와 **'즉흥 연기'**를 함 |
| **파일** | `Curriculum_Storytelling_Prompt...md` | `character_operation_prompts.md` 등 |

> **핵심 가치:** 
> 작가마다 퀄리티가 들쑥날쑥하지 않도록, **'교육적 의도가 포함된 골든 스토리'**를 일관되게 생산하는 **'표준 제작 공정'**을 자산화한 것입니다.

---

# 1. 요약 (Executive Summary)

### 목표 (The Goal)
모든 대사를 하드코딩하지 않고도, 무한한 커리큘럼 변형과 스토리 아크를 생성할 수 있는 **'지속 가능한 콘텐츠 엔진'**을 구축하는 것입니다.

### 해결책 (The Solution)
우리는 프롬프트를 단순한 텍스트가 아닌 **'모듈화된 자산(Modular Assets)'**으로 취급합니다.
- **Before:** 하드코딩된 대화 트리 (유연하지 않음, 확장 어려움)
- **After:** **프롬프트 오케스트레이션 시스템** (동적, 상황 인지, 확장 가능)

### 엔지니어를 위한 핵심 메시지
> "챗봇을 만들지 마십시오. 문맥(Context)에 따라 프롬프트 블록을 조립하고 지휘하는 **'런타임 디렉터(Runtime Director)'**를 설계하십시오."

---

# 2. 시스템 개요: 9개의 핵심 모듈

시스템은 9개의 기능 모듈로 나뉩니다. 각 모듈은 프롬프트 자산(파일)들의 폴더입니다.

| 카테고리 | 역할 | 예시 (개념) |
|---|---|---|
| **1. 기본 시스템 (Base System)** | 캐릭터 정체성 (불변) | "너는 우주에서 온 아이 루나야..." |
| **2. 커리큘럼 스토리 (Curriculum)** | 서사 생성 | "이 닦기에 대한 미션을 만들어줘..." |
| **3. 캐릭터 운영 (Character Ops)** | 톤 & 매너 유지 | "설교하듯 하지 말고 친구처럼 말해." |
| **4. 아이 신호 해석 (Child Signal)** | 입력 의도 파악 | "아이가 침묵하나요? 지루한가요? 신났나요?" |
| **5. 난이도 조절 (Adaptive)** | 레벨 자동 조정 | "계속 틀리면 객관식으로 질문을 바꿔." |
| **6. 관계 형성 (Relationship)** | 장기 기억 활용 | "안녕 {이름}! 어제 했던 얘기 기억나?" |
| **7. 실패 대응 (Failure Ops)** | 에러/이탈 핸들링 | "틀려도 괜찮아, 이렇게 다시 해보자." |
| **8. 안전 (Safety)** | 경계 설정 | "개인정보를 물어보면 화제를 돌려." |
| **9. 디자인 도구 (Design Meta)** | 오프라인 설계 지원 | "5주차 스펙을 생성해줘." (런타임 미사용) |

---

# 3. 런타임 아키텍처 (Runtime Architecture)

한 번의 대화 턴(Turn)이 처리되는 과정입니다.

```mermaid
graph TD
    User((아이 음성)) --> STT[STT Layer]
    STT --> Signal[신호 해석 Layer]
    
    subgraph "Context Assembly (맥락 조립)"
        State[세션 상태] --> Context
        Memory[사용자 기억] --> Context
        Signal --> Context
    end
    
    Context --> Decision{포포(Popo) 결정 엔진}
    
    Decision -- "개입 필요" --> Popo[포포 프롬프트 조립]
    Decision -- "진행 계속" --> Luna[루나 프롬프트 조립]
    
    subgraph "Prompt Assembly (프롬프트 조립)"
        Luna --> LLM[LLM 생성]
        Popo --> LLM
    end
    
    LLM --> TTS[TTS 출력]
    TTS --> User
```

### 핵심 개념: "신호(Signal)" 레이어
우리는 아이의 생(Raw) 텍스트를 캐릭터에게 바로 전달하지 **않습니다**.
1. **Raw Input:** "..." (침묵)
2. **Signal Layer:** `{ "type": "hesitation", "intent": "thinking" }` (주저함/생각중)으로 해석
3. **Decision Layer:** 신호에 따라 "더 기다리기" 또는 "힌트 주기" 결정

---

# 4. 핵심 로직: 동적 프롬프트 조립 (Dynamic Prompt Assembly)

프롬프트는 **매핑 테이블(Mapping Table)**에 따라 레고 블록처럼 런타임에 조립됩니다.

### 예시: "퀴즈 실패" 시나리오

**입력 데이터 (Inputs):**
- Context: `2주차`, `Task: 색깔 놀이`, `실패 횟수: 2회`
- Signal: `오답(Wrong Answer)`

**조립 로직 (Assembly Logic):**
```python
final_prompt = [
    Base_System_Prompt,          # 1. 캐릭터 정체성 (항상 포함)
    Failure_Recovery_Prompt,     # 2. <--- 선택된 모듈 (실패 대응 전략)
    Task_Context_Prompt,         # 3. 현재 퀴즈 내용
    Adaptive_Difficulty_Prompt   # 4. <--- 난이도 하향 조정 지시
]
```

**결과 (Result):**
단순히 "틀렸어, 다시 해봐"라고 하는 대신, 시스템은 다음을 생성합니다:
> "어, 정말 헷갈리는 색깔인걸! 딸기랑 비슷하게 생겼네. 빨간색일까 파란색일까?" (힌트 + 격려)

---

# 5. 개발자 가이드: 시스템 확장 방법

### 시나리오 A: 새로운 주차(Week) 추가 시
**백엔드 작업:** 없음 (Zero Code).
**자산 작업:** 
1. `Curriculum Design Meta Prompts`를 사용해 해당 주차의 스펙 생성.
2. `Week_Story_Arc` 프롬프트 파일만 설정에 추가.

### 시나리오 B: 새로운 "스킬"(예: 리듬감) 추가 시
**백엔드 작업:** `Skill Dictionary` 업데이트.
**자산 작업:**
1. `Skill_Definition` 정의.
2. 기존 `Skill Integration Prompt`가 자동으로 스토리에 이를 반영함.

### 시나리오 C: LLM 모델 교체 시
**백엔드 작업:** API 엔드포인트 변경.
**자산 작업:** 없음 (프롬프트는 모델 불가지론적(Model-agnostic)이나, 튜닝은 필요할 수 있음).

---

# 6. 안전 및 경계 (Safety & Boundaries)

이 시스템은 **이중 안전망(Dual-Layer Safety Net)**을 구현합니다.

1. **시스템 프롬프트 레이어:** 최상위 지침 (주소 묻지 않기 등).
2. **런타임 개입:** 만약 `Safety_Boundary_Prompt` 조건이 트리거되면, **포포(Popo)**가 즉시 개입하여 화제를 전환합니다.

> **규칙:** 안전 프롬프트는 *모든* 컨텍스트 윈도우에 주입되지만, 가장 높은 우선순위를 가집니다.

---

# 7. 개발팀 다음 단계 (Next Steps)

1. **인프라 구축:** 마크다운 파일들을 동적으로 불러와 연결(Concatenate)하는 `Prompt Assembler` 서비스 구축.
2. **상태 관리:** "좌절 레벨", "몰입도" 등을 추적하는 `Session State` 스키마 설계.
3. **테스트:** "침묵"이나 "나쁜 말" 등을 입력했을 때, `Signal Layer`가 올바른 JSON을 뱉는지 검증하는 테스트 하네스 제작.

---
*문서 버전: 1.0 (Korean)*
*기반 디렉토리: `projectx/밤토리/prompt`*
