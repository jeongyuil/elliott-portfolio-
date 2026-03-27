import re
from dataclasses import dataclass

@dataclass
class SafetyResult:
    is_safe: bool
    filtered_text: str
    reason: str | None = None
    safe_text: str = "" # Fallback text

# Basic profanity list (extend as needed)
PROFANITY_LIST = [
    "shit", "fuck", "damn", "bitch", "crap", "piss", "dick", "darn", "cock", "pussy", "ass", "asshole", "fag", "bastard", "slut", "douche",
    "개새끼", "시발", "씨발", "병신", "존나", "미친", "닥쳐", "꺼져"
]

def filter_input(text: str) -> SafetyResult:
    """Check child input for safety."""
    if not text:
        return SafetyResult(True, text, safe_text=text)
        
    # 1. Profanity Check
    for word in PROFANITY_LIST:
        if word in text.lower():
            # FAIL-SAFE: Return a friendly redirect message
            return SafetyResult(
                is_safe=False, 
                filtered_text=text, 
                reason="profanity_detected", 
                safe_text="우리 예쁜 말만 쓰기로 해요! 다시 말해줄래?" # "Let's use nice words! Can you say it again?"
            )
            
    # 2. PII Check (Simple Regex for Phone/Email)
    # Email
    if re.search(r'[\w\.-]+@[\w\.-]+', text):
        return SafetyResult(
            is_safe=False, 
            filtered_text=text, 
            reason="pii_email_detected", 
            safe_text="개인정보는 비밀이에요! 다른 이야기를 해볼까?"
        )
    # Phone (KR)
    if re.search(r'01[016789]-?\d{3,4}-?\d{4}', text):
        return SafetyResult(
            is_safe=False, 
            filtered_text=text, 
            reason="pii_phone_detected", 
            safe_text="전화번호는 알려주면 안돼요! 비밀!"
        )

    return SafetyResult(True, text, safe_text=text)

def filter_output(text: str) -> SafetyResult:
    """Check AI output for safety."""
    # Similar checks, maybe less strict on PII if it's Hallucination?
    # For now, apply same rules.
    return filter_input(text)
