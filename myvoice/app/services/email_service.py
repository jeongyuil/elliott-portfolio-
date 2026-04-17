"""Email delivery via Resend API."""
import logging
import resend

from app.config import get_settings

logger = logging.getLogger(__name__)


def _client() -> None:
    settings = get_settings()
    resend.api_key = settings.resend_api_key


async def send_verification_email(to_email: str, token: str) -> bool:
    """Send email verification link."""
    settings = get_settings()
    _client()
    verify_url = f"{settings.frontend_url}/verify-email?token={token}"
    try:
        resend.Emails.send({
            "from": f"{settings.email_from_name} <{settings.email_from}>",
            "to": [to_email],
            "subject": "[밤토리] 이메일 인증을 완료해 주세요",
            "html": f"""
<div style="font-family:sans-serif;max-width:480px;margin:0 auto">
  <h2 style="color:#58cc02">밤토리에 오신 걸 환영해요! 🌙</h2>
  <p>아래 버튼을 눌러 이메일 인증을 완료하세요.</p>
  <a href="{verify_url}"
     style="display:inline-block;background:#58cc02;color:#fff;
            padding:14px 28px;border-radius:12px;text-decoration:none;
            font-weight:bold;font-size:16px">
    이메일 인증하기
  </a>
  <p style="color:#999;font-size:12px;margin-top:24px">
    이 링크는 24시간 후 만료됩니다.<br>
    본인이 가입하지 않았다면 이 메일을 무시하세요.
  </p>
</div>
""",
        })
        return True
    except Exception as exc:
        logger.error("send_verification_email failed: %s", exc)
        return False


async def send_password_reset_email(to_email: str, token: str) -> bool:
    """Send password reset link."""
    settings = get_settings()
    _client()
    reset_url = f"{settings.frontend_url}/reset-password?token={token}"
    try:
        resend.Emails.send({
            "from": f"{settings.email_from_name} <{settings.email_from}>",
            "to": [to_email],
            "subject": "[밤토리] 비밀번호 재설정 안내",
            "html": f"""
<div style="font-family:sans-serif;max-width:480px;margin:0 auto">
  <h2 style="color:#58cc02">비밀번호 재설정</h2>
  <p>아래 버튼을 눌러 새 비밀번호를 설정하세요.</p>
  <a href="{reset_url}"
     style="display:inline-block;background:#58cc02;color:#fff;
            padding:14px 28px;border-radius:12px;text-decoration:none;
            font-weight:bold;font-size:16px">
    비밀번호 재설정하기
  </a>
  <p style="color:#999;font-size:12px;margin-top:24px">
    이 링크는 1시간 후 만료됩니다.<br>
    본인이 요청하지 않았다면 이 메일을 무시하세요.
  </p>
</div>
""",
        })
        return True
    except Exception as exc:
        logger.error("send_password_reset_email failed: %s", exc)
        return False


async def send_welcome_email(to_email: str, parent_name: str) -> bool:
    """Send welcome email after verified signup."""
    settings = get_settings()
    _client()
    try:
        resend.Emails.send({
            "from": f"{settings.email_from_name} <{settings.email_from}>",
            "to": [to_email],
            "subject": "[밤토리] 가입을 환영해요! 🎉",
            "html": f"""
<div style="font-family:sans-serif;max-width:480px;margin:0 auto">
  <h2 style="color:#58cc02">안녕하세요, {parent_name}님! 🌙</h2>
  <p>밤토리 가족이 되신 것을 환영해요.<br>
     아이와 함께 매일 10분, AI 친구 루나와 영어 여행을 시작해 보세요!</p>
  <a href="{settings.frontend_url}/select-child"
     style="display:inline-block;background:#58cc02;color:#fff;
            padding:14px 28px;border-radius:12px;text-decoration:none;
            font-weight:bold;font-size:16px">
    지금 시작하기
  </a>
</div>
""",
        })
        return True
    except Exception as exc:
        logger.error("send_welcome_email failed: %s", exc)
        return False
