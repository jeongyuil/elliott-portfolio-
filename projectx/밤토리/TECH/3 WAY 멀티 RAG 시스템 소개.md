# GraphRAG 시스템 기술 아키텍처

**작성일**: 2026-02-22
**용도**: RAG 시스템 기술 소개용 정리

---

## 시스템 개요

3-way 앙상블 GraphRAG 시스템으로 키워드 + 시맨틱 + 그래프 검색을 결합하여 정확도 극대화

---

## 시스템 아키텍처

### 1. 3-way 앙상블 구조

```
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│    BM25      │  │   Vector     │  │    Graph     │
│  (ES)        │  │ (pgvector)   │  │   (Neo4j)    │
│ 키워드 검색   │  │ 시맨틱 검색   │  │  관계 탐색   │
└──────┬───────┘  └──────┬───────┘  └──────┬───────┘
       ↓                 ↓                  ↓
   정확한 매칭      의미적 유사성      계층적 지식
       ↓                 ↓                  ↓
└─────────────────────────────────────────────────────────┘
                    RRF 결합
                        ↓
                    최종 결과
```

---

## 기술 스택

### BM25
- **기술 스택**: Elasticsearch 8.15.0
- **역할**: 키워드 검색 (정확한 매칭)

### Vector
- **기술 스택**: Postgres pgvector + OpenAI text-embedding-3-small
- **역할**: 시맨틱 검색 (의미적 유사성)

### Graph
- **기술 스택**: Neo4j (APOC 플러그인)
- **역할**: 그래프 검색 (관계 탐색)

### 앙상블
- **기술 스택**: RRF (Reciprocal Rank Fusion, k=60)
- **역할**: 결과 결합/재랭킹

---

## 그래프 DB 구조

### 노드 및 관계

```
Document (문서)
  └─[HAS_SECTION]→ Section (섹션)
         └─[CONTAINS_CONCEPT]→ Concept (개념)
```

### 그래프 통계

- **Document 노드**: 181개
- **Section 노드**: 9,625개
- **Concept 노드**: 6,011개
- **HAS_SECTION 관계**: 9,625개
- **CONTAINS_CONCEPT 관계**: 82,896개

---

## 데이터 현황

### 벡터화 결과

- **총 임베딩**: 9,625개
- **파일 수**: 181개
- **데이터 소스**:
  - `memory/` 폴더: 10개 파일 (일일 기록)
  - `diary/opsidian/` 폴더: 171개 파일 (옵시디언 노트)

### 주요 벡터화 파일

#### 마지막 버전.md (Hackerthon)
- 임베딩 수: 1,204개

#### Gabi93.md
- 임베딩 수: 1,204개

#### 설악동집 사업성 분석.md
- 임베딩 수: 160개

#### GE 팀과 AI 콜라보레이션 작업.md
- 임베딩 수: 148개

#### CodeGraph 연구.md
- 임베딩 수: 144개

---

## 데이터 파이프라인

### 1. 벡터화 단계

```bash
# 옵시디언 문서 벡터화
/home/ggugi/openclaw/.venv/bin/python /home/ggugi/openclaw/vectorize_obsidian.py

# 대화 기록 벡터화
/home/ggugi/openclaw/.venv/bin/python /home/ggugi/openclaw/vectorize_conversations.py
```

### 2. 데이터 동기화

```bash
# Postgres → Elasticsearch 데이터 동기화
/home/ggugi/openclaw/.venv/bin/python /home/ggugi/openclaw/scripts/elastic_search_setup.py

# Postgres → Neo4j 그래프 업데이트
/home/ggugi/openclaw/.venv/bin/python /home/ggugi/openclaw/build_neo4j_graph_v2.py
```

### 3. 자동화 크론

- **매일 00:00**: 옵시디언 커밋 & 푸시 + 벡터화 + 그래프 업데이트

---

## 검색 방법

### 하이브리드 검색 (BM25 + Vector + Graph)

```bash
export OPENAI_API_KEY='your-api-key'
/home/ggugi/openclaw/.venv/bin/python /home/ggugi/openclaw/search_conversations.py "검색어" [결과개수] [최소유사도]
```

### 예시

```bash
# 기본 검색 (5개 결과)
./search_conversations.py "FOTLD"

# 10개 결과
./search_conversations.py "설악동" 10

# 최소 유사도 지정
./search_conversations.py "검색어" 10 0.3
```

### 그래프 전용 검색

```bash
/home/ggugi/openclaw/.venv/bin/python /home/ggugi/openclaw/search_graph.py "검색어" 5
```

---

## RRF (Reciprocal Rank Fusion) 알고리즘

### 공식

```
score(d) = Σ (k / (k + rank_i(d)))
```

- **k = 60**: 조정 파라미터 (순위의 영향력 조절)
- 각 검색 방법의 순위를 결합하여 최종 랭킹 도출

### 장점

- **자동 가중치 조정**: 순위 기반이라 점수 스케일 무관
- **안정성**: 단일 검색 방법의 노이즈에 강함
- **최적화**: 다양한 검색 방법의 장점 결합

---

## 주요 파일 구조

```
/home/ggugi/openclaw/
├── search_conversations.py      # GraphRAG 메인 (3-way 앙상블)
├── graph_rag.py                  # GraphRAG 구현
├── search_graph.py               # 그래프 검색
├── build_neo4j_graph_v2.py       # Neo4j 그래프 구축
├── hybrid_search.py              # 하이브리드 검색 (레거시)
├── elastic_search_setup.py       # ES 데이터 동기화
├── vectorize_obsidian.py         # 옵시디언 벡터화
├── vectorize_conversations.py    # 대화 기록 벡터화
└── ~/docker/elastic-search/
    ├── docker-compose.yml        # 엘라스틱서치 도커 설정
    └── README.md                 # 시스템 문서
```

---

## 성능 개선 효과

1. **정확도 향상**: 키워드 + 의미 + 관계 결합
2. **검색 범위 확장**: 정확한 매칭 + 유의어 + 계층적 지식
3. **자동 가중치 조정**: RRF 알고리즘으로 최적 랭킹
4. **하이브리드 검색**: BM25 + Vector + Graph = Best of All Worlds

---

## 향후 개선 계획

- [ ] **한국어 형태소 분석기 (nori)** 플러그인 설치
- [ ] **검색 결과 캐싱**: 반복 검색 성능 향상
- [ ] **쿼리 자동 확장** (Query Expansion)
- [ ] **검색 결과 재랭킹** (Re-ranking)
- [ ] **검색 성능 모니터링 대시보드**
- [ ] **그래프 관계 확장**: SIMILAR_TO, REFERENCES 관계 추가

---

## 핵심 포인트

1. **3-way 앙상블**: 키워드(정확도) + 시맨틱(의미) + 그래프(맥락) → 완벽한 검색
2. **대규모 데이터**: 9,625개 섹션, 82,896개 관계 → 풍부한 지식 베이스
3. **자동화 파이프라인**: 매일 00:00 자동 업데이트 → 최신 정보 유지
4. **RRF 앙상블**: 순위 기반 결합 → 안정적이고 강력한 검색

이 시스템은 키워드 검색의 정확성, 시맨틱 검색의 유연성, 그래프 검색의 맥락 이해 능력을 모두 결합하여 완벽한 지검색 경험을 제공합니다! :tada:

---

## 참고 문서

- **Neo4j 공식 문서**: https://neo4j.com/docs/
- **Elasticsearch 공식 문서**: https://www.elastic.co/guide/
- **LangChain GraphRAG**: https://python.langchain.com/docs/integrations/graphs/neo4j_graphrag
- **RRF 논문**: "Reciprocal Rank Fusion outperforms Condorcet and individual Rank Learning Methods"
