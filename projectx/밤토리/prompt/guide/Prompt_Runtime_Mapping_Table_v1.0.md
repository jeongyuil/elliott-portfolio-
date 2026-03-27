
# Prompt ↔ Runtime Mapping Table v1.0

본 문서는 런타임에서 **어떤 시점에 어떤 프롬프트 묶음(Prompt Bundle)** 이 호출되는지를 정의합니다.  
엔지니어, PM, 기획자가 동일한 기준으로 대화 흐름을 이해하도록 설계되었습니다.

---

## 1. Prompt Bundle 정의 요약

| Bundle ID | 포함 프롬프트 |
|---------|---------------|
| CORE_CHARACTER | character_operation_prompts |
| CHILD_SIGNAL | child_response_interpretation_prompts |
| ADAPTIVE | adaptive_difficulty_prompts |
| RELATIONSHIP | relationship_maintenance_prompts |
| FAILURE | failure_recovery_prompts |
| SAFETY | safety_boundary_prompts |
| META (비런타임) | curriculum_design_meta_prompts |

---

## 2. 세션 라이프사이클 기준 Runtime Mapping

### 2.1 Session Start (세션 진입)

| Trigger | 호출 Prompt Bundle | 목적 |
|------|-------------------|------|
| 세션 시작 | CORE_CHARACTER | Luna/Popo 캐릭터 톤 고정 |
|  | RELATIONSHIP | 재진입 친밀감 형성 |
|  | SAFETY | 정서적·개인정보 안전 가드 |

---

### 2.2 Warm-up & Emotion Check

| Trigger | 호출 Prompt Bundle | 목적 |
|------|-------------------|------|
| 아이 첫 발화 전 | CHILD_SIGNAL | 침묵/회피/긴장 상태 해석 |
|  | ADAPTIVE | 질문 밀도 조절 |
|  | RELATIONSHIP | 부담 없는 시작 |

---

### 2.3 Task Questioning (학습 태스크 구간)

| Trigger | 호출 Prompt Bundle | 목적 |
|------|-------------------|------|
| 질문 생성 시 | CORE_CHARACTER | 캐릭터 발화 규칙 유지 |
|  | ADAPTIVE | 난이도 실시간 조절 |
|  | SAFETY | 질문 범위 제한 |

---

### 2.4 Child Response Handling (아이 응답 처리)

| Child Response 유형 | 호출 Prompt Bundle | 설명 |
|-------------------|-------------------|------|
| 단답/한 단어 | CHILD_SIGNAL + ADAPTIVE | 확장 or 축소 판단 |
| 침묵/회피 | CHILD_SIGNAL + RELATIONSHIP | 압박 제거 |
| 오답/틀림 | FAILURE + ADAPTIVE | 실패 흡수 |
| 장난/농담 | CHILD_SIGNAL | 몰입 신호로 해석 |

---

### 2.5 Failure & Breakdown Moments

| Trigger | 호출 Prompt Bundle | 목적 |
|------|-------------------|------|
| 2회 연속 실패 | FAILURE | 좌절 방지 |
| 감정 저하 | RELATIONSHIP | 정서 복구 |
| 말하기 중단 | ADAPTIVE | 질문 구조 단순화 |

---

### 2.6 Safety Override (강제 개입)

| Trigger | 호출 Prompt Bundle | 동작 |
|------|-------------------|------|
| 개인정보 언급 | SAFETY | 질문 전환 |
| 현실/상상 혼동 | SAFETY + CORE_CHARACTER | 경계 재정의 |
| 감정 위험 신호 | SAFETY + RELATIONSHIP | 안정 우선 |

---

### 2.7 Session Closing

| Trigger | 호출 Prompt Bundle | 목적 |
|------|-------------------|------|
| 세션 종료 | RELATIONSHIP | 긍정 기억 고정 |
|  | CORE_CHARACTER | 캐릭터 일관된 마무리 |

---

## 3. 주차/세션별 기본 Prompt Bundle 세트

| Week / Session | Default Prompt Bundle |
|---------------|----------------------|
| W1 전체 | CORE_CHARACTER + RELATIONSHIP + CHILD_SIGNAL |
| W2 전체 | + ADAPTIVE |
| W3 전체 | + FAILURE |
| W4 전체 | + SAFETY |

---

## 4. 엔지니어링 관점 메모

- Prompt Bundle은 **순차 호출이 아니라 조합형 평가**
- 항상 CHILD_SIGNAL 결과가 다른 Bundle 호출을 트리거
- META Prompt는 런타임에서 호출되지 않음

---

## 5. 핵심 원칙

> ❝ 질문 → 답변 → 평가 ❞ 구조가 아니라  
> ❝ 신호 → 해석 → 반응 ❞ 구조로 런타임을 설계한다.

