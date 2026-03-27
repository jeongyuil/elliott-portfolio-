"""
Shared fixtures for E2E integration tests.
Uses real PostgreSQL + Redis (from docker-compose), mocks OpenAI calls.

Key: We replace app.database.engine and async_session_maker at the module
level with versions created on the test event loop, and override the
FastAPI get_db dependency, so all DB operations run on the correct loop.
"""
import uuid
import pytest
import pytest_asyncio
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch

from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool

import app.database as db_module
from app.main import app
from app.database import get_db
from app.config import get_settings
from app.core.security import create_access_token, hash_password
from app.models.family import FamilyAccount, Child


# ---------------------------------------------------------------------------
# Unique IDs per test run (avoid collisions on re-runs)
# ---------------------------------------------------------------------------

TEST_RUN_ID = uuid.uuid4().hex[:8]
TEST_EMAIL = f"e2e_{TEST_RUN_ID}@example.com"
TEST_PASSWORD = "TestPass123!"
TEST_PARENT_NAME = f"E2E Parent {TEST_RUN_ID}"
TEST_CHILD_NAME = f"E2E Child {TEST_RUN_ID}"

_FAMILY_ID = uuid.uuid4()
_CHILD_ID = uuid.uuid4()

_settings = get_settings()

# Will be set by setup_test_db
_test_session_maker = None


# ---------------------------------------------------------------------------
# Replace DB engine + seed data (session scope)
# ---------------------------------------------------------------------------

@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_test_db():
    """Replace module-level engine with one on the test event loop, then seed."""
    global _test_session_maker

    # Create new engine on the test event loop
    # NullPool prevents connection reuse across tasks, avoiding asyncpg's
    # "Future attached to a different loop" error with httpx ASGITransport.
    test_engine = create_async_engine(
        _settings.database_url,
        echo=False,
        poolclass=NullPool,
    )
    _test_session_maker = async_sessionmaker(
        test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    # Monkey-patch so all code paths use the test engine
    db_module.engine = test_engine
    db_module.async_session_maker = _test_session_maker

    # Replace the Redis client with a dict-backed fake (the real one was
    # created at import time on a different loop).
    import app.services.session_orchestrator as orch_module

    class FakeRedis:
        """In-memory Redis-like store for tests."""
        def __init__(self):
            self._store = {}
        async def get(self, key):
            return self._store.get(key)
        async def set(self, key, value, ex=None):
            self._store[key] = value
            return True
        async def delete(self, key):
            return self._store.pop(key, None) is not None
        async def ping(self):
            return True

    orch_module.redis = FakeRedis()

    # Override FastAPI dependency
    async def _test_get_db():
        async with _test_session_maker() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()

    app.dependency_overrides[get_db] = _test_get_db

    # Seed test data
    async with _test_session_maker() as db:
        family = FamilyAccount(
            family_id=_FAMILY_ID,
            parent_name=TEST_PARENT_NAME,
            contact_email=TEST_EMAIL,
            hashed_password=hash_password(TEST_PASSWORD),
            email_verified=True,
        )
        db.add(family)
        await db.flush()

        child = Child(
            child_id=_CHILD_ID,
            family_id=_FAMILY_ID,
            name=TEST_CHILD_NAME,
            birth_date=datetime(2020, 6, 15),
        )
        db.add(child)
        await db.commit()

    yield

    # Cleanup test data
    async with _test_session_maker() as db:
        from sqlalchemy import text
        cid = str(_CHILD_ID)
        fid = str(_FAMILY_ID)
        await db.execute(text(
            "DELETE FROM utterances WHERE session_id IN "
            "(SELECT session_id FROM sessions WHERE child_id = :cid)"
        ), {"cid": cid})
        await db.execute(text(
            "DELETE FROM session_activities WHERE session_id IN "
            "(SELECT session_id FROM sessions WHERE child_id = :cid)"
        ), {"cid": cid})
        await db.execute(text("DELETE FROM sessions WHERE child_id = :cid"), {"cid": cid})
        # Delete all child-referencing tables before children
        for tbl in ("skill_levels", "task_attempts", "weekly_goals",
                     "reports", "vocabulary_progress", "child_inventories"):
            await db.execute(text(f"DELETE FROM {tbl} WHERE child_id = :cid"), {"cid": cid})
        await db.execute(text("DELETE FROM children WHERE child_id = :cid"), {"cid": cid})
        await db.execute(text(
            "DELETE FROM family_accounts WHERE contact_email LIKE :pat"
        ), {"pat": f"e2e_{TEST_RUN_ID}%"})
        await db.execute(text(
            "DELETE FROM family_accounts WHERE contact_email LIKE :pat"
        ), {"pat": f"signup_{TEST_RUN_ID}%"})
        await db.execute(text("DELETE FROM family_accounts WHERE family_id = :fid"), {"fid": fid})
        await db.commit()

    app.dependency_overrides.clear()
    await test_engine.dispose()


# ---------------------------------------------------------------------------
# Disable rate limiter for tests
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def disable_rate_limiter():
    """Disable slowapi rate limiter during tests."""
    from app.core.rate_limit import limiter
    limiter.enabled = False
    yield
    limiter.enabled = True


# ---------------------------------------------------------------------------
# Simple fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def seed_family():
    """Return test family/child IDs."""
    return {"family_id": str(_FAMILY_ID), "child_id": str(_CHILD_ID)}


@pytest.fixture
def family_token(seed_family):
    """JWT token for parent endpoints."""
    return create_access_token({"family_id": seed_family["family_id"]})


@pytest.fixture
def child_token(seed_family):
    """JWT token for kid endpoints."""
    return create_access_token({
        "family_id": seed_family["family_id"],
        "child_id": seed_family["child_id"],
        "scope": "kid",
    })


@pytest_asyncio.fixture
async def client():
    """AsyncClient connected to the FastAPI app."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


# ---------------------------------------------------------------------------
# OpenAI + Email mocks (autouse)
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def mock_openai():
    """Mock all OpenAI API calls to avoid real API costs."""
    mock_transcription = MagicMock()
    mock_transcription.text = "Hello Luna!"
    mock_transcription.language = "en"
    mock_transcription.segments = [MagicMock(avg_logprob=-0.3)]

    mock_choice = MagicMock()
    mock_choice.message.content = '{"response": "Hi there! What a great job!", "emotion": "happy", "feedback": {"type": "good", "skill": "vocabulary", "level": 2, "message": "Nice words!"}}'
    mock_completion = MagicMock()
    mock_completion.choices = [mock_choice]

    mock_tts_response = MagicMock()
    mock_tts_response.content = b"\xff\xfb\x90\x00" + b"\x00" * 500

    async_client_mock = AsyncMock()
    async_client_mock.audio.transcriptions.create = AsyncMock(return_value=mock_transcription)
    async_client_mock.chat.completions.create = AsyncMock(return_value=mock_completion)
    async_client_mock.audio.speech.create = AsyncMock(return_value=mock_tts_response)

    with patch("app.services.speech_pipeline.client", async_client_mock):
        yield async_client_mock


@pytest.fixture(autouse=True)
def mock_email_service():
    """Mock email service to avoid sending real emails."""
    with patch("app.services.email_service.send_verification_email", new_callable=AsyncMock), \
         patch("app.services.email_service.send_welcome_email", new_callable=AsyncMock), \
         patch("app.services.email_service.send_password_reset_email", new_callable=AsyncMock):
        yield
