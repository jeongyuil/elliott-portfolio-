"""
MyVoice (밤토리) - Voice AI Education Platform
FastAPI application entry point.

API Namespace:
  /v1/auth/*           → 부모 인증 (signup, login, select-child)
  /v1/parent/*         → Parent View (children, reports, stats)
  /v1/kid/*            → Kids View (sessions)
  /v1/trial/*          → 체험 (비인증)
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from starlette.middleware.sessions import SessionMiddleware

from app.config import get_settings
from app.core.exceptions import (
    http_exception_handler,
    unhandled_exception_handler,
)
from app.core.rate_limit import limiter
from app.routers import auth, auth_child, trial
from app.routers import kid_sessions
from app.routers import parent_children, parent_dashboard

settings = get_settings()

app = FastAPI(
    title="MyVoice API",
    description="밤토리 - Voice AI Education Platform for Kids (4-12세)",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Rate limiter state
app.state.limiter = limiter

# Session (required for Authlib OAuth state/nonce)
app.add_middleware(SessionMiddleware, secret_key=settings.jwt_secret_key)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global exception handlers — standardize all error responses
from app.core.logging import setup_logging
import uuid
import time
import logging
from starlette.requests import Request
from starlette.types import ASGIApp, Receive, Scope, Send

# Initialize logging
setup_logging("INFO")
logger = logging.getLogger("app.middleware")


class LoggingMiddleware:
    """Pure ASGI middleware for request logging.

    Unlike @app.middleware("http") / BaseHTTPMiddleware, this does NOT
    spawn call_next in a separate task, which avoids asyncpg's
    "Future attached to a different loop" error.
    """

    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        request_id = str(uuid.uuid4())
        start_time = time.time()
        status_code = 500

        # Inject request_id into scope state so endpoints can read it
        if "state" not in scope:
            scope["state"] = {}
        scope["state"]["request_id"] = request_id

        request = Request(scope)
        logger.info(
            f"Request started: {request.method} {request.url.path}",
            extra={"request_id": request_id},
        )

        async def send_wrapper(message):
            nonlocal status_code
            if message["type"] == "http.response.start":
                status_code = message["status"]
                headers = list(message.get("headers", []))
                headers.append((b"x-request-id", request_id.encode()))
                message = {**message, "headers": headers}
            await send(message)

        try:
            await self.app(scope, receive, send_wrapper)
        except Exception as e:
            process_time = time.time() - start_time
            logger.error(
                f"Request failed: {e}",
                extra={
                    "request_id": request_id,
                    "duration_ms": round(process_time * 1000, 2),
                },
                exc_info=True,
            )
            raise
        else:
            process_time = time.time() - start_time
            logger.info(
                f"Request finished: {status_code}",
                extra={
                    "request_id": request_id,
                    "duration_ms": round(process_time * 1000, 2),
                    "status_code": status_code,
                },
            )


app.add_middleware(LoggingMiddleware)

app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)

# === Auth ===
app.include_router(auth.router, prefix="/v1/auth", tags=["Auth"])
app.include_router(auth_child.router, prefix="/v1/auth", tags=["Auth"])

# === Parent View ===
app.include_router(parent_children.router, prefix="/v1/parent/children", tags=["Parent - Children"])
app.include_router(parent_dashboard.router, prefix="/v1") # /v1/parent/dashboard & /v1/parent/reports

from app.routers import parent_insights
app.include_router(parent_insights.router, prefix="/v1/parent", tags=["Parent - Insights"])

# === Kids View ===
from app.routers import kid_home, kid_vocabulary, kid_shop, kid_profile, kid_goals, kid_adventures, kid_skills

app.include_router(kid_sessions.router, prefix="/v1/kid/sessions", tags=["Kid - Sessions"])
app.include_router(kid_home.router, prefix="/v1/kid/home", tags=["Kid - Home"])
app.include_router(kid_adventures.router, prefix="/v1/kid/adventures", tags=["Kid - Adventures"])
app.include_router(kid_vocabulary.router, prefix="/v1/kid/vocabulary", tags=["Kid - Vocabulary"])
app.include_router(kid_shop.router, prefix="/v1/kid/shop", tags=["Kid - Shop"])
app.include_router(kid_profile.router, prefix="/v1/kid/profile", tags=["Kid - Profile"])
app.include_router(kid_goals.router, prefix="/v1/kid/goals", tags=["Kid - Goals"])
app.include_router(kid_skills.router, prefix="/v1/kid/skills", tags=["Kid - Skills"])

# === Trial (no auth) ===
app.include_router(trial.router, prefix="/v1/trial", tags=["Trial"])

# === Voice WebSocket ===
from app.routers import ws_voice
app.include_router(ws_voice.router, prefix="/v1/kid", tags=["Kid - Voice"])



@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok", "service": "myvoice-api", "version": "0.1.0"}

from app.services.session_orchestrator import redis as redis_client
from app.database import get_db
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

@app.get("/health/deep", tags=["Health"])
async def deep_health_check(db: AsyncSession = Depends(get_db)):
    health_status = {
        "status": "ok",
        "service": "myvoice-api",
        "dependencies": {
            "database": "unknown",
            "redis": "unknown"
        }
    }
    
    # 1. Check Database
    try:
        await db.execute(text("SELECT 1"))
        health_status["dependencies"]["database"] = "ok"
    except Exception as e:
        health_status["dependencies"]["database"] = f"error: {str(e)}"
        health_status["status"] = "degraded"
        logger.error("Deep health check failed: Database", exc_info=True)

    # 2. Check Redis
    try:
        if await redis_client.ping():
             health_status["dependencies"]["redis"] = "ok"
        else:
             health_status["dependencies"]["redis"] = "error: ping failed"
             health_status["status"] = "degraded"
    except Exception as e:
        health_status["dependencies"]["redis"] = f"error: {str(e)}"
        health_status["status"] = "degraded"
        logger.error("Deep health check failed: Redis", exc_info=True)
        
    if health_status["status"] != "ok":
        raise HTTPException(status_code=503, detail=health_status)
        
    return health_status
