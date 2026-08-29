"""Auth request/response schemas."""
from pydantic import BaseModel, EmailStr
import uuid


class SignupRequest(BaseModel):
    email: EmailStr
    password: str
    parent_name: str


class SignupResponse(BaseModel):
    family_id: uuid.UUID
    message: str = "인증 이메일을 발송했습니다. 이메일을 확인해 주세요."


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    access_token: str
    family_id: uuid.UUID
    token_type: str = "bearer"


class ResendVerificationRequest(BaseModel):
    email: EmailStr


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str
