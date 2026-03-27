# MVP 개발 최소 인력 구성 (정예 3인 팀)

본 문서는 `MVP_Development_Roadmap.md`의 개발 일정과 목표를 달성하기 위한 **최적의 3인 팀 구성(Full Stack, Data Engineer, Data Analyst)**과 그 역할을 정의합니다.

## 1. 인력 구성 개요

기존 사업계획서의 조직 구성을 MVP 개발 단계에 맞춰 **실무 중심의 정예 멤버 3명**으로 압축하였습니다.

| 역할 (Role)                      | 담당 영역             | 핵심 역량                                     |
| :----------------------------- | :---------------- | :---------------------------------------- |
| **CTO / Full Stack Developer** | 기술 총괄 및 서비스 개발    | Tech Leadership, Flutter, Python, Infra   |
| **Data Engineer**              | AI 엔진 및 데이터 파이프라인 | LLM Chain, WebSocket, Data Engineering    |
| **Data Analyst**               | 교육 로직 및 프롬프트 설계   | Prompt Engineering, Data Analysis, Python |

---

## 2. 역할별 상세 R&R (Roadmap 연계)

### A. CTO / Full Stack Developer (기술 총괄 및 서비스 구축)
> **"기술적 의사결정을 주도하며, 사용자가 만나는 모든 화면과 기능을 구현합니다."**

*   **핵심 책임:**
    *   **Tech Lead:** 전체 기술 아키텍처 설계, 기술 스택 선정, 개발 일정 및 리스크 관리.
    *   **Frontend:** Flutter 기반의 iOS/Android 크로스 플랫폼 앱 개발. (AI 코딩 도구 활용으로 생산성 극대화)
    *   **Backend:** 사용자 인증, 결제, 구독 관리 등 서비스 로직 API 서버 개발.
    *   **Infra:** AWS/GCP 클라우드 환경 구축 및 배포 파이프라인(CI/CD) 관리.
*   **Roadmap 연계:**
    *   **Phase 1:** DB 스키마 설계 및 기술 스택 환경 설정.
    *   **Phase 2:** 회원가입/로그인(Auth) 및 기본 API 구현.
    *   **Phase 3:** **[Critical]** 앱 UI 구현 및 음성 인터페이스(마이크/스피커) 연동.
    *   **Phase 4:** 부모용 대시보드 및 리포트 뷰어 개발.

### B. Data Engineer (AI 기술의 뼈대)
> **"AI가 듣고 말할 수 있는 시스템과 데이터 흐름을 만듭니다."**

*   **핵심 책임:**
    *   **AI Pipeline:** STT(Whisper) → LLM(GPT) → TTS(ElevenLabs)로 이어지는 실시간 대화 엔진 구현.
    *   **Real-time:** WebSocket 기반의 저지연(Low-latency) 음성 스트리밍 서버 구축.
    *   **Data Ops:** 대화 로그 수집, 적재 및 분석을 위한 데이터 파이프라인 구축.
*   **Roadmap 연계:**
    *   **Phase 1:** AI 모델 성능 검증(PoC) 및 실시간 아키텍처 설계.
    *   **Phase 2:** **[Critical]** LangChain 기반 대화 관리자 및 핵심 엔진 개발.
    *   **Phase 3:** 대화 로그 적재 시스템 및 비동기 작업 큐(Celery) 설정.
    *   **Phase 5:** 서버 부하 테스트 및 Latency 최적화.

### C. Data Analyst (서비스의 두뇌)
> **"AI에게 교육적 페르소나를 부여하고, 학습 효과를 증명합니다."**

*   **핵심 책임:**
    *   **Prompt Engineering:** 연령별/상황별 AI 페르소나 설계 및 시스템 프롬프트 최적화.
    *   **Logic Design:** 발화량, 어휘력 등 교육적 지표 정의 및 분석 알고리즘(Python) 작성.
    *   **Quality Control:** AI 대화 품질 평가 및 환각(Hallucination) 제어.
*   **Roadmap 연계:**
    *   **Phase 1:** 교육 커리큘럼 정의 및 페르소나 기획.
    *   **Phase 2:** **[Critical]** 시스템 프롬프트 작성 및 테스트 데이터셋 구축.
    *   **Phase 4:** 리포트 생성 로직 구현 및 데이터 정합성 검증.
    *   **Phase 5:** 베타 테스터 피드백 분석 및 프롬프트 최종 튜닝.

---

## 3. 협업 시너지 전략

*   **Full Stack ↔ Data Engineer:**
    *   앱(Client)과 AI 서버 간의 통신 규격(WebSocket Protocol)을 초기에 확정하여 병렬 개발 진행.
*   **Data Engineer ↔ Data Analyst:**
    *   분석가가 설계한 프롬프트가 실제 시스템에서 의도대로 동작하는지 엔지니어가 기술적으로 검증 및 지원.
*   **Full Stack ↔ Data Analyst:**
    *   분석가가 산출한 데이터(JSON)를 앱에서 부모가 이해하기 쉬운 UI(차트/그래프)로 시각화.

## 4. 결론

이 3인 구성은 **"최소한의 인원으로 최대한의 기능"**을 구현하기 위한 최적의 조합입니다.
*   **Full Stack**은 서비스의 외형과 뼈대를,
*   **Data Engineer**는 서비스의 심장(AI 엔진)을,
*   **Data Analyst**는 서비스의 지능(교육 로직)을 담당하여 MVP를 성공적으로 런칭합니다.
