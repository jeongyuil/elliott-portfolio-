# Prompt Library Structure v1.0

## 1. Overview
This document defines the full Prompt Library structure for the Luna–Popo Voice AI Curriculum system.
Each prompt category represents a reusable operational asset for curriculum design, runtime dialogue control, safety, and future scaling.

---

## 2. Prompt Categories

### 2.1 Base System Prompts
**Purpose:** Define immutable character identity and worldview.

- luna_base_system_prompt.md
- popo_base_system_prompt.md

---

### 2.2 Curriculum Storytelling Prompts
**Purpose:** Generate narrative-driven learning flows.

- week_story_arc_prompt
- mission_generation_prompt
- narrative_continuity_prompt

---

### 2.3 Character Operation Prompts
**Purpose:** Maintain character consistency across sessions.

- tone_guardrail_prompt
- intervention_decision_prompt
- silence_handling_prompt

---

### 2.4 Child Signal Interpretation Prompts
**Purpose:** Interpret child responses as signals, not correctness.

- response_intent_classification_prompt
- emotional_state_inference_prompt
- engagement_level_detection_prompt

---

### 2.5 Adaptive Difficulty Prompts
**Purpose:** Dynamically adjust challenge and pacing.

- simplification_prompt
- expansion_prompt
- recovery_rephrasing_prompt

---

### 2.6 Relationship Maintenance Prompts
**Purpose:** Build emotional continuity and attachment.

- reentry_welcome_prompt
- memory_callback_prompt
- affection_reinforcement_prompt

---

### 2.7 Failure & Recovery Prompts
**Purpose:** Convert failure into safe learning moments.

- mistake_normalization_prompt
- guided_retry_prompt
- confidence_restoration_prompt

---

### 2.8 Safety & Boundary Prompts
**Purpose:** Ensure child safety and ethical boundaries.

- personal_data_avoidance_prompt
- reality_fantasy_boundary_prompt
- sensitive_topic_deflection_prompt

---

### 2.9 Curriculum Design Meta Prompts
**Purpose:** Support designers and operators.

- week_design_prompt
- session_quality_review_prompt
- curriculum_gap_analysis_prompt

---

## 3. Versioning Rules
- Each prompt file must include version, owner, and last update date.
- Runtime prompts and design-time prompts must be separated.

---

## 4. Future Expansion
- Localization prompts
- Parent-facing report generation prompts
- Multi-character orchestration prompts
