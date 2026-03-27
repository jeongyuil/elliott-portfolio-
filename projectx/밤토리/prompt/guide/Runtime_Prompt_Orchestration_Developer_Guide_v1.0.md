# Runtime Prompt Orchestration – Developer Guide v1.0

## 1. Purpose
This document explains how the Luna–Popo Prompt Library is used at runtime.
It is intended for engineers implementing dialogue orchestration, state handling, and LLM prompt assembly.

---

## 2. One-Line Summary
Child input is not answered directly.
It passes through a **signal → decision → prompt assembly → character rendering** pipeline.

---

## 3. High-Level Runtime Flow

```
[Phase 1: Narrator Intro (TTS Only)]
 → [Phase 2: Transition Trigger (Wait for "Go!")]
 → [Phase 3: Interactive Loop Starts]

Child Voice Input
 → STT
 → Signal Interpretation
 → Dialogue State & Skill Context
 → Decision Engine (Popo)
 → Prompt Assembly
 → LLM Generation
 → Character Rendering (Luna / Popo)
 → TTS Output
```

---

## 4. Step-by-Step Breakdown

### 4.1 Signal Interpretation Layer
**Goal:** Convert raw child utterance into interpretable signals.

**Prompts Used**
- response_intent_classification_prompt
- emotional_state_inference_prompt
- engagement_level_detection_prompt

**Output Example**
```json
{
  "intent": "self_expression",
  "emotion": "excited",
  "engagement": "high"
}
```

---

### 4.2 Dialogue State & Skill Context
Combine:
- Week / Session / Task
- Target Skills
- Relationship Level

```json
{
  "week": 1,
  "session": "W1_S2",
  "skills": ["SELF_INTRO_BASIC"],
  "relationship_state": "warming_up"
}
```

---

### 4.3 Decision Engine (Popo)
Popo acts as the runtime decision-maker.

**Prompts Used**
- intervention_decision_prompt
- adaptive_difficulty_prompt
- silence_handling_prompt

**Decision Output**
```json
{
  "speaker": "Luna",
  "response_mode": "expand_story",
  "difficulty": "maintain",
  "relationship_action": "affection_reinforcement"
}
```

---

### 4.4 Prompt Assembly
Prompts are composed modularly.

```
Base System Prompt (Character)
+ Tone Guardrail Prompt
+ Session Story Prompt
+ Adaptive Difficulty Prompt
+ Relationship Block Prompt
+ Conversation Memory
```

---

### 4.5 Character Rendering
| Character | Identity | Role |
|--------|--------|------|
| Luna | 우주에서 온 아이 (살아있는 생명체, 친구) | English-only, imagination & storytelling |
| Popo | 정부 파견 비밀 요원 (코치) | Korean/English, coaching & safety |
| Narrator | 동화책을 읽어주는 화자 | Korean voice-only, storybook-style context setting (Phase 1) |
| Child | **주인공 (Protagonist)** | 모험의 리더, 캡틴 — Luna를 도와주는 선생님 |

Popo may intervene before or after Luna if needed.
The child is always framed as the **Captain/Protagonist** — never a passive learner.

---

## 5. Engineering Principles

- Prompts are assets, not hardcoded strings
- No correctness judgement exposed to child
- Runtime prompts must be stateless; state is injected
- Design-time prompts ≠ runtime prompts

---

## 6. Extension Points
- Add new weeks by adding prompts only
- Add new skills via Skill Dictionary
- Swap LLM without changing orchestration logic

---

## 7. Reference Files
- Prompt_Library_Structure_v1.0.md
- luna_base_system_prompt.md
- popo_base_system_prompt.md
- Skill_Dictionary_v0.1.md

---

## 8. Status
Version: v1.0  
Audience: Backend / AI Engineers  
Next: Popo Decision Prompt Implementation
