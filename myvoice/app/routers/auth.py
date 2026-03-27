"""Auth router: signup, login, email-verification, OAuth (Google/Kakao/Apple)."""
import logging
import secrets
import urllib.parse
from datetime import datetime, timedelta

import httpx
from authlib.integrations.starlette_client import OAuth
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.responses import RedirectResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.core.rate_limit import limiter
from app.core.security import create_access_token, hash_password, verify_password
from app.database import get_db
from app.models.family import FamilyAccount
from app.models.oauth_account import OAuthAccount
from app.schemas.auth import (
    ForgotPasswordRequest,
    LoginRequest,
    LoginResponse,
    ResendVerificationRequest,
    ResetPasswordRequest,
    SignupRequest,
    SignupResponse,
)
from app.services import email_service

logger = logging.getLogger(__name__)
router = APIRouter()

# ─── Authlib OAuth registry ──────────────────────────────────────────────────

_oauth = OAuth()
_registered_providers: set[str] = set()


def _get_google_client():
    s = get_settings()
    if "google" not in _registered_providers:
        _oauth.register(
            name="google",
            client_id=s.google_client_id,
            client_secret=s.google_client_secret,
            server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
            client_kwargs={"scope": "openid email profile"},
        )
        _registered_providers.add("google")
    return _oauth.google  # type: ignore[attr-defined]


def _get_kakao_client():
    s = get_settings()
    if "kakao" not in _registered_providers:
        _oauth.register(
            name="kakao",
            client_id=s.kakao_client_id,
            client_secret=s.kakao_client_secret,
            authorize_url="https://kauth.kakao.com/oauth/authorize",
            access_token_url="https://kauth.kakao.com/oauth/token",
            api_base_url="https://kapi.kakao.com/",
            client_kwargs={
                "scope": "profile_nickname account_email",
                "token_endpoint_auth_method": "client_secret_post",
            },
        )
        _registered_providers.add("kakao")
    return _oauth.kakao  # type: ignore[attr-defined]


# ─── Cookie helper ───────────────────────────────────────────────────────────

def _set_auth_cookie(response: Response, token: str) -> None:
    s = get_settings()
    response.set_cookie(
        key="access_token",
        value=f"Bearer {token}",
        httponly=True,
        secure=s.app_env == "production",
        samesite="lax",
        max_age=s.access_token_expire_minutes * 60,
    )


# ─── OAuth account linking ────────────────────────────────────────────────────

async def _find_or_create_oauth_user(
    db: AsyncSession,
    provider: str,
    provider_user_id: str,
    provider_email: str | None,
    access_token_value: str | None,
    display_name: str | None,
) -> FamilyAccount:
    # 1. Existing OAuth entry
    result = await db.execute(
        select(OAuthAccount).where(
            OAuthAccount.provider == provider,
            OAuthAccount.provider_user_id == provider_user_id,
        )
    )
    oauth_row = result.scalar_one_or_none()
    if oauth_row:
        family_result = await db.execute(
            select(FamilyAccount).where(FamilyAccount.family_id == oauth_row.family_id)
        )
        return family_result.scalar_one()

    family: FamilyAccount | None = None

    # 2. Match by email → auto-link
    if provider_email:
        result = await db.execute(
            select(FamilyAccount).where(FamilyAccount.contact_email == provider_email)
        )
        family = result.scalar_one_or_none()

    # 3. Create new family
    if not family:
        fallback_email = (
            provider_email or f"{provider}_{provider_user_id}@oauth.local"
        )
        fallback_name = display_name or (
            provider_email.split("@")[0] if provider_email else "User"
        )
        family = FamilyAccount(
            parent_name=fallback_name,
            contact_email=fallback_email,
            hashed_password=hash_password(secrets.token_hex(32)),
            email_verified=True,
        )
        db.add(family)
        await db.flush()

    # Add OAuth link
    oauth_account = OAuthAccount(
        family_id=family.family_id,
        provider=provider,
        provider_user_id=provider_user_id,
        provider_email=provider_email,
        access_token=access_token_value,
    )
    db.add(oauth_account)
    await db.flush()
    return family


# ─── Email / Password ─────────────────────────────────────────────────────────

@router.post("/signup", response_model=SignupResponse, status_code=201)
@limiter.limit("5/minute")
async def signup(
    req: SignupRequest,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(FamilyAccount).where(FamilyAccount.contact_email == req.email)
    )
    if result.scalar_one_or_none():
        raise HTTPException(status_code=409, detail="Email already registered")

    verification_token = secrets.token_urlsafe(32)

    family = FamilyAccount(
        parent_name=req.parent_name,
        contact_email=req.email,
        hashed_password=hash_password(req.password),
        email_verified=False,
        email_verification_token=verification_token,
        email_verification_expires=datetime.utcnow() + timedelta(hours=24),
    )
    db.add(family)
    await db.flush()

    await email_service.send_verification_email(req.email, verification_token)
    return SignupResponse(family_id=family.family_id)


@router.post("/login", response_model=LoginResponse)
@limiter.limit("10/minute")
async def login(
    req: LoginRequest,
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(FamilyAccount).where(FamilyAccount.contact_email == req.email)
    )
    family = result.scalar_one_or_none()

    if not family or not verify_password(req.password, family.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    if not family.email_verified:
        raise HTTPException(status_code=403, detail="email_not_verified")

    token = create_access_token({"family_id": str(family.family_id)})
    _set_auth_cookie(response, token)
    return LoginResponse(access_token=token, family_id=family.family_id)


@router.post("/login/mock", response_model=LoginResponse)
async def login_mock(response: Response, db: AsyncSession = Depends(get_db)):
    if get_settings().app_env != "development":
        raise HTTPException(status_code=404, detail="Not found")

    result = await db.execute(select(FamilyAccount).limit(1))
    family = result.scalar_one_or_none()
    if not family:
        raise HTTPException(status_code=404, detail="No mock user found. Run seed.")

    token = create_access_token({"family_id": str(family.family_id)})
    _set_auth_cookie(response, token)
    return LoginResponse(access_token=token, family_id=family.family_id)


# ─── Email Verification ───────────────────────────────────────────────────────

@router.get("/verify-email")
async def verify_email(
    token: str,
    response: Response,
    db: AsyncSession = Depends(get_db),
):
    s = get_settings()
    result = await db.execute(
        select(FamilyAccount).where(FamilyAccount.email_verification_token == token)
    )
    family = result.scalar_one_or_none()

    if not family:
        return RedirectResponse(url=f"{s.frontend_url}/verify-email?error=invalid")

    if family.email_verification_expires and datetime.utcnow() > family.email_verification_expires:
        return RedirectResponse(
            url=f"{s.frontend_url}/verify-email?error=expired&email={family.contact_email}"
        )

    family.email_verified = True
    family.email_verification_token = None
    family.email_verification_expires = None
    await db.flush()

    access_token = create_access_token({"family_id": str(family.family_id)})
    _set_auth_cookie(response, access_token)

    await email_service.send_welcome_email(family.contact_email, family.parent_name)
    return RedirectResponse(url=f"{s.frontend_url}/select-child")


@router.post("/resend-verification")
@limiter.limit("3/minute")
async def resend_verification(
    req: ResendVerificationRequest,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(FamilyAccount).where(FamilyAccount.contact_email == req.email)
    )
    family = result.scalar_one_or_none()

    if not family or family.email_verified:
        return {"message": "인증 이메일을 발송했습니다."}

    verification_token = secrets.token_urlsafe(32)
    family.email_verification_token = verification_token
    family.email_verification_expires = datetime.utcnow() + timedelta(hours=24)
    await db.flush()

    await email_service.send_verification_email(req.email, verification_token)
    return {"message": "인증 이메일을 발송했습니다."}


# ─── Password Reset ───────────────────────────────────────────────────────────

@router.post("/forgot-password")
@limiter.limit("3/minute")
async def forgot_password(
    req: ForgotPasswordRequest,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(FamilyAccount).where(FamilyAccount.contact_email == req.email)
    )
    family = result.scalar_one_or_none()

    if family:
        reset_token = secrets.token_urlsafe(32)
        family.password_reset_token = reset_token
        family.password_reset_expires = datetime.utcnow() + timedelta(hours=1)
        await db.flush()
        await email_service.send_password_reset_email(req.email, reset_token)

    return {"message": "비밀번호 재설정 이메일을 발송했습니다."}


@router.post("/reset-password")
async def reset_password(
    req: ResetPasswordRequest,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(FamilyAccount).where(FamilyAccount.password_reset_token == req.token)
    )
    family = result.scalar_one_or_none()

    if not family:
        raise HTTPException(status_code=400, detail="Invalid or expired reset token")

    if family.password_reset_expires and datetime.utcnow() > family.password_reset_expires:
        raise HTTPException(status_code=400, detail="Reset token has expired")

    if len(req.new_password) < 8:
        raise HTTPException(status_code=422, detail="Password must be at least 8 characters")

    family.hashed_password = hash_password(req.new_password)
    family.password_reset_token = None
    family.password_reset_expires = None
    await db.flush()

    return {"message": "비밀번호가 변경되었습니다."}


# ─── Google OAuth ─────────────────────────────────────────────────────────────

@router.get("/google")
async def google_login(request: Request):
    s = get_settings()
    if not s.google_client_id:
        raise HTTPException(status_code=501, detail="Google OAuth not configured")
    client = _get_google_client()
    redirect_uri = f"{s.app_base_url}/v1/auth/google/callback"
    return await client.authorize_redirect(request, redirect_uri)


@router.get("/google/callback")
async def google_callback(
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    s = get_settings()
    client = _get_google_client()
    try:
        token_data = await client.authorize_access_token(request)
    except Exception as exc:
        logger.warning("Google OAuth token exchange failed: %s", exc)
        return RedirectResponse(url=f"{s.frontend_url}/login?error=oauth_failed")

    user_info = token_data.get("userinfo") or {}
    provider_user_id = user_info.get("sub")
    if not provider_user_id:
        return RedirectResponse(url=f"{s.frontend_url}/login?error=oauth_no_user")

    family = await _find_or_create_oauth_user(
        db, "google", provider_user_id,
        user_info.get("email"), token_data.get("access_token"), user_info.get("name"),
    )
    access_token = create_access_token({"family_id": str(family.family_id)})
    redirect_url = f"{s.frontend_url}/select-child?token={access_token}&family_id={family.family_id}"
    redirect = RedirectResponse(url=redirect_url)
    _set_auth_cookie(redirect, access_token)
    return redirect


# ─── Kakao OAuth ──────────────────────────────────────────────────────────────

@router.get("/kakao")
async def kakao_login(request: Request):
    s = get_settings()
    if not s.kakao_client_id:
        raise HTTPException(status_code=501, detail="Kakao OAuth not configured")
    client = _get_kakao_client()
    redirect_uri = f"{s.app_base_url}/v1/auth/kakao/callback"
    return await client.authorize_redirect(request, redirect_uri)


@router.get("/kakao/callback")
async def kakao_callback(
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    s = get_settings()
    client = _get_kakao_client()
    try:
        token_data = await client.authorize_access_token(request)
    except Exception as exc:
        logger.warning("Kakao OAuth token exchange failed: %s", exc)
        return RedirectResponse(url=f"{s.frontend_url}/login?error=oauth_failed")

    async with httpx.AsyncClient() as http:
        r = await http.get(
            "https://kapi.kakao.com/v2/user/me",
            headers={"Authorization": f"Bearer {token_data['access_token']}"},
        )
    kakao_user = r.json()

    provider_user_id = str(kakao_user.get("id", ""))
    if not provider_user_id:
        return RedirectResponse(url=f"{s.frontend_url}/login?error=oauth_no_user")

    kakao_account = kakao_user.get("kakao_account", {})
    family = await _find_or_create_oauth_user(
        db, "kakao", provider_user_id,
        kakao_account.get("email"),
        token_data.get("access_token"),
        kakao_user.get("properties", {}).get("nickname"),
    )
    access_token = create_access_token({"family_id": str(family.family_id)})
    redirect_url = f"{s.frontend_url}/select-child?token={access_token}&family_id={family.family_id}"
    redirect = RedirectResponse(url=redirect_url)
    _set_auth_cookie(redirect, access_token)
    return redirect


# ─── Apple Sign In ────────────────────────────────────────────────────────────

@router.get("/apple")
async def apple_login(_request: Request):
    s = get_settings()
    if not s.apple_team_id:
        raise HTTPException(status_code=501, detail="Apple Sign In not configured")

    redirect_uri = f"{s.app_base_url}/v1/auth/apple/callback"
    params = {
        "client_id": s.apple_bundle_id,
        "redirect_uri": redirect_uri,
        "response_type": "code id_token",
        "scope": "name email",
        "response_mode": "form_post",
        "state": secrets.token_urlsafe(16),
    }
    url = "https://appleid.apple.com/auth/authorize?" + urllib.parse.urlencode(params)
    return RedirectResponse(url=url)


@router.post("/apple/callback")
async def apple_callback(
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_db),
):
    import json as _json
    from authlib.jose import JsonWebKey
    from authlib.jose import jwt as authlib_jwt

    s = get_settings()
    form = await request.form()
    id_token_str = form.get("id_token")

    if not id_token_str:
        return RedirectResponse(url=f"{s.frontend_url}/login?error=apple_no_token")

    try:
        async with httpx.AsyncClient() as http:
            keys_resp = await http.get("https://appleid.apple.com/auth/keys")
        keys = JsonWebKey.import_key_set(keys_resp.json())
        claims = authlib_jwt.decode(id_token_str, keys)
        claims.validate()
        provider_user_id = claims["sub"]
        provider_email = claims.get("email")
    except Exception as exc:
        logger.warning("Apple id_token validation failed: %s", exc)
        return RedirectResponse(url=f"{s.frontend_url}/login?error=apple_invalid_token")

    display_name = None
    user_form = form.get("user")
    if user_form:
        try:
            user_data = _json.loads(user_form)
            name = user_data.get("name", {})
            parts = [name.get("firstName", ""), name.get("lastName", "")]
            display_name = " ".join(p for p in parts if p) or None
        except Exception:
            pass

    family = await _find_or_create_oauth_user(
        db, "apple", provider_user_id, provider_email, None, display_name
    )
    access_token = create_access_token({"family_id": str(family.family_id)})
    _set_auth_cookie(response, access_token)
    return RedirectResponse(url=f"{s.frontend_url}/select-child")
