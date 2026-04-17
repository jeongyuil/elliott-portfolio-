"""Auth extension: select-child endpoint for Kids View token."""
import uuid
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models.family import Child
from app.core.security import (
    get_current_family_id,
    create_access_token,
    verify_password,
)

router = APIRouter()


class SelectChildRequest(BaseModel):
    child_id: uuid.UUID
    pin: str | None = None


class SelectChildResponse(BaseModel):
    child_token: str
    child_id: uuid.UUID
    child_name: str



from fastapi import Response, Request
from app.config import get_settings
from app.core.rate_limit import limiter

@router.post("/select-child", response_model=SelectChildResponse)
@limiter.limit("5/minute")
async def select_child(
    req: SelectChildRequest,
    response: Response,
    request: Request,
    family_id: str = Depends(get_current_family_id),
    db: AsyncSession = Depends(get_db),
):
    """
    부모가 아이 프로필을 선택하여 Kids View용 child_token을 발급받습니다.
    PIN이 설정된 경우 검증합니다.
    """
    result = await db.execute(
        select(Child).where(
            Child.child_id == req.child_id,
            Child.family_id == uuid.UUID(family_id),
        )
    )
    child = result.scalar_one_or_none()

    # 보안: child not found / invalid PIN 을 동일 메시지로 통일 (사용자 열거 방지)
    _auth_error = HTTPException(status_code=401, detail="Authentication failed")

    if not child:
        raise _auth_error

    # PIN 검증 (설정된 경우)
    if child.pin_hash:
        if not req.pin or not verify_password(req.pin, child.pin_hash):
            raise _auth_error

    child_token = create_access_token({
        "family_id": family_id,
        "child_id": str(child.child_id),
        "scope": "kid",
    })
    
    # Set Cookie
    response.set_cookie(
        key="child_token",
        value=f"Bearer {child_token}",
        httponly=True,
        secure=get_settings().app_env == "production",
        samesite="lax",
        max_age=get_settings().access_token_expire_minutes * 60
    )
    
    return SelectChildResponse(
        child_token=child_token,
        child_id=child.child_id,
        child_name=child.name,
    )
