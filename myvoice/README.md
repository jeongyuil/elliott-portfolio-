# 밤토리 (MyVoice) - Voice AI Education Platform

음성 AI 기반 어린이 영어 교육 플랫폼

## Quick Start

### 1. Prerequisites
- Python 3.9+
- Docker (for PostgreSQL & Redis)
- OpenAI API Key

### 2. Setup

```bash
# Install dependencies
uv venv
source .venv/bin/activate
uv pip install -e ".[dev]"

# Start infrastructure
docker compose up -d

# Run migrations
alembic upgrade head

# Start dev server
uvicorn app.main:app --reload --port 8000
```

### 3. API Documentation
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure

```
app/
├── main.py              # FastAPI entry point
├── config.py            # Environment settings
├── database.py          # Async SQLAlchemy
├── models/              # Domain models (15 entities)
├── schemas/             # Pydantic request/response
├── routers/             # API endpoints
├── services/            # Business logic
└── core/                # Security & utilities
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /v1/auth/signup | Register family |
| POST | /v1/auth/login | Login |
| POST | /v1/children | Create child |
| GET | /v1/children/{id} | Get child |
| POST | /v1/sessions | Start session |
| POST | /v1/sessions/{id}/utterances | Upload audio |
| POST | /v1/sessions/{id}/end | End session |
| GET | /v1/reports | List reports |
| GET | /v1/reports/{id} | Get report |
| POST | /v1/trial/quick-start | Quick trial |
