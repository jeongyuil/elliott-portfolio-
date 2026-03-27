# GitHub Copilot Instructions for Bamtori VOICE AI Education Platform

## Project Overview
Bamtori is a voice-first English learning platform for children aged 4-12, using AI characters Luna (English-speaking alien) and Popo (Korean coach) for conversational sessions. MVP focuses on Phase 1 curriculum (Weeks 1-4) with ontology-based data tracking and parent reports.

## Architecture
- **Backend**: FastAPI (Python) with modules for Auth, Session Orchestrator, Curriculum Engine, Speech Pipeline (STT→LLM→TTS), Evaluation Engine, Report Generator.
- **Frontend**: Flutter/React Native app with real-time voice UI, avatar animations, waveform feedback.
- **Database**: PostgreSQL with ontology entities (FamilyAccount, Child, Session, Utterance, TaskAttempt, Skill, SkillLevel, Report); JSONB fields; S3 for audio storage.
- **AI Services**: Whisper (STT), GPT-4o (LLM), ElevenLabs/OpenAI (TTS); LangChain for dialogue management.
- **Key Files**: 
  - [fdd/FDD_MVP_v1.4.md](fdd/FDD_MVP_v1.4.md) - Feature design document
  - [fdd/온톨로지_정의서_v0.1.1.md](fdd/온톨로지_정의서_v0.1.1.md) - Domain model
  - [fdd/Skill_Dictionary_v0.1.md](fdd/Skill_Dictionary_v0.1.md) - Skills framework
  - [fdd/openapi_v1.yaml](fdd/openapi_v1.yaml) - API specification

## Development Workflow
- **Build**: Use `uvicorn main:app --reload` for FastAPI dev server; Flutter `flutter run` for app.
- **Test**: Run `pytest` for backend unit tests; focus on session orchestration and speech pipeline integration.
- **Debug**: Check PostgreSQL logs for data issues; use admin console for session/utterance inspection; monitor STT latency (<500ms target).
- **Deploy**: AWS EC2/RDS/S3; CI/CD with GitHub Actions for automated testing.

## Coding Conventions
- **Prompts**: Store AI character prompts in Python files (e.g., [커리큘럼/prompt.py](커리큘럼/prompt.py)) with clear sections for persona, rules, interaction flow.
- **Data Model**: Follow ontology v0.1.1; use `skill_id` like `SK_VOCAB_BASIC` for language skills, `SK_AFFECT_CONFIDENCE` for emotional.
- **API**: RESTful with OpenAPI spec; use WebSocket for real-time audio streaming.
- **Curriculum**: Structure sessions as activities/tasks/skills mappings (see [fdd/W1_Task_Activity_Skill_Mapping_v0.1.md](fdd/W1_Task_Activity_Skill_Mapping_v0.1.md)); evaluate TaskAttempt as correct/partial/incorrect.
- **Safety**: Implement fallback responses for AI failures; ensure child-friendly content (no corrections, positive reinforcement).

## Key Patterns
- **Session Flow**: Mission hook → Relationship rituals → Emotion check-in → Activity tasks → Celebration.
- **Voice Interaction**: On-device VAD for silence detection; stream OGG Opus audio; TTS responses with Luna/Popo JSON format.
- **Evaluation**: Track skills like `phonology/pronunciation`, `vocabulary`, `pragmatics`; percentile by age band.
- **Reports**: Generate monthly text-based reports with skill trends (↑/→/↓) and coaching tips.

## Common Pitfalls
- Avoid direct corrections; use Luna's "misunderstanding" to prompt child responses.
- Ensure low latency for child engagement; prioritize audio quality over complex UI.
- Validate ontology compliance; all entities link via foreign keys (e.g., Utterance → Session → Child).

For curriculum details, reference [fdd/W1_Week1_Spec_v0.1.md](fdd/W1_Week1_Spec_v0.1.md). For roadmap, see [draft/MVP_Development_Roadmap.md](draft/MVP_Development_Roadmap.md).</content>
<parameter name="filePath">/Users/yuil/Documents/github/project-x/projectx/밤토리/.github/copilot-instructions.md