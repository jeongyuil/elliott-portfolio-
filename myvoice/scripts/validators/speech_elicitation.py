"""
Speech Elicitation Validator for 밤토리 (MyVoice)
==================================================

Validates that intro_narrator_scripts follow the 3-step speech elicitation pattern:
1. 포포 시범 (Popo demonstrates first)
2. 선택지 제공 (Offer A/B choices)
3. 명확한 발화 유도 (Clear speech prompt ending)

Usage:
    from scripts.validators import validate_speech_elicitation

    issues = validate_speech_elicitation(activities)
    # activities = list of dicts with "activity_id" and "intro_narrator_script"

This module has NO database or framework dependencies — it operates purely on
dict data, so it can be used in any build regardless of ORM or DB setup.
"""

import re


def validate_speech_elicitation(activities: list[dict]) -> list[dict]:
    """Validate that every intro_narrator_script follows the 3-step speech elicitation pattern.

    Args:
        activities: List of dicts, each with at least:
            - "activity_id": str
            - "intro_narrator_script": str (optional, skipped if empty)

    Returns:
        List of issue dicts with keys: activity_id, check, message.
        Empty list means all scripts passed.
    """
    issues = []

    for act in activities:
        script = act.get("intro_narrator_script", "")
        act_id = act.get("activity_id", "UNKNOWN")

        if not script:
            continue

        # Check 1: 포포 시범 — "포포가 먼저" pattern
        if "포포가 먼저" not in script:
            issues.append({
                "activity_id": act_id,
                "check": "popo_demo",
                "message": "포포 시범 누락 ('포포가 먼저~' 패턴 없음)",
            })

        # Check 2: 선택지 제공 — options for the child
        has_choices = any(kw in script for kw in ["아니면", "중에", "골라서", "중에 하나"])
        if not has_choices:
            issues.append({
                "activity_id": act_id,
                "check": "choices",
                "message": "선택지 누락 ('아니면' / 'A, B 중에' 패턴 없음)",
            })

        # Check 3: 명확한 발화 유도 — ends with a clear prompt to speak
        last_popo_line = ""
        for line in script.strip().split("\n"):
            if line.startswith("[포포]"):
                last_popo_line = line
        has_prompt = any(kw in last_popo_line for kw in ["말해봐", "해볼래", "해봐", "해볼까", "골라줘"])
        if not has_prompt:
            issues.append({
                "activity_id": act_id,
                "check": "speech_prompt",
                "message": "발화 유도 누락 (마지막 [포포] 대사에 '말해봐/해볼래' 없음)",
            })

        # Check 5: 포포 발화 유도에 영어 표현 포함 여부
        # 포포의 시범/선택지/발화유도 대사에 영어 표현이 반드시 포함되어야 함
        # 작은따옴표로 감싼 영어 표현 ('Hello!', 'I like pizza') 패턴 체크
        popo_lines = [line for line in script.strip().split("\n") if line.startswith("[포포]")]
        has_english_in_popo = False
        for line in popo_lines:
            # 작은따옴표로 감싼 영어 표현 체크
            if re.search(r"'[A-Za-z].*?'", line):
                has_english_in_popo = True
                break
        if not has_english_in_popo:
            issues.append({
                "activity_id": act_id,
                "check": "english_in_popo",
                "message": "포포 대사에 영어 표현 누락 (포포가 'English phrase' 형태로 시범을 보여야 함)",
            })

        # Check 4: Character tags — every line must start with [나레이션], [포포], or [루나]
        valid_tags = ("[나레이션]", "[포포]", "[루나]")
        for line in script.strip().split("\n"):
            line = line.strip()
            if line and not any(line.startswith(tag) for tag in valid_tags):
                issues.append({
                    "activity_id": act_id,
                    "check": "character_tag",
                    "message": f"잘못된 태그: '{line[:60]}...'",
                })
                break  # Only report first bad line per script

        # Check 6: 루나 영어 전용 — [루나] lines must not contain Korean
        for line in script.strip().split("\n"):
            if not line.startswith("[루나]"):
                continue
            content = line[len("[루나]"):].strip()
            # Stage directions in parentheses are acceptable
            content_no_paren = re.sub(r"\(.*?\)", "", content).strip()
            if _HANGUL_RE.search(content_no_paren):
                issues.append({
                    "activity_id": act_id,
                    "check": "luna_english_only",
                    "message": (
                        f"[루나] 대사에 한국어 포함 (루나는 영어만 사용): "
                        f"'{content[:60]}'"
                    ),
                })
                break  # Report first offending line only

    return issues


# Korean character regex — used for luna_english_only check
_HANGUL_RE = re.compile(r"[\uAC00-\uD7A3\u3131-\u318E\uFFA1-\uFFDC]")


def print_validation_report(activities: list[dict]) -> bool:
    """Run validation and print a formatted report.

    Returns True if all passed, False if issues found.
    """
    print("=" * 60)
    print("  SPEECH ELICITATION VALIDATION")
    print("=" * 60)

    issues = validate_speech_elicitation(activities)

    if issues:
        print(f"\n  ⚠ {len(issues)} issue(s) found:\n")
        for issue in issues:
            print(f"  [{issue['activity_id']}] {issue['check']}: {issue['message']}")
        print(f"\n  Fix these before shipping to production.")
        print("=" * 60)
        return False
    else:
        print("  ✓ All scripts pass speech elicitation checks!")
        print("=" * 60)
        return True
