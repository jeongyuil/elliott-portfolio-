"""
Story Quality Validator
========================

Extends the existing scripts/validators/speech_elicitation.py with
additional checks specific to the story pipeline:

Existing checks (from speech_elicitation.py):
  [1] popo_demo         — "포포가 먼저" pattern present
  [2] choices           — A/B choice pattern present
  [3] speech_prompt     — last [포포] line has "말해봐/해볼래" etc.
  [4] english_in_popo   — [포포] lines contain English in single-quotes
  [5] character_tag     — all lines start with valid [tag]

New checks added here:
  [6] luna_english_only — [루나] lines must be English only (no Korean)
  [7] key_expression    — activity's key_expression appears in the script
  [8] popo_coaching     — [포포] has at least 2 lines (coach role present)
  [9] min_length        — script has at least 10 lines
"""

from __future__ import annotations


import re
import sys
import os

# Allow importing the existing validator from scripts/validators/
_SCRIPTS_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, _SCRIPTS_DIR)

from validators.speech_elicitation import validate_speech_elicitation

# Korean character range
_HANGUL_RE = re.compile(r"[\uAC00-\uD7A3\u3131-\u318E\uFFA1-\uFFDC]")

# English word pattern (simple: any ASCII letter sequence)
_ENGLISH_RE = re.compile(r"[A-Za-z]")


def validate_story(
    activity_id: str,
    intro_script: str,
    key_expression: str = "",
    outro_script: str = "",
) -> list[dict]:
    """
    Run all quality checks on a generated story script.

    Args:
        activity_id:    ID of the activity (for error messages)
        intro_script:   The generated intro_narrator_script
        key_expression: The activity's target English expression
        outro_script:   The generated outro_narrator_script (optional)

    Returns:
        List of issue dicts: {"activity_id", "check", "severity", "message"}
        Empty list = all checks passed.
    """
    issues: list[dict] = []

    # ------------------------------------------------------------------
    # Run existing speech elicitation checks on intro script
    # ------------------------------------------------------------------
    existing = validate_speech_elicitation([
        {"activity_id": activity_id, "intro_narrator_script": intro_script}
    ])
    # Promote existing issues to include severity
    for issue in existing:
        issues.append({**issue, "severity": "error"})

    # ------------------------------------------------------------------
    # [6] luna_english_only — [루나] lines must be English only
    # ------------------------------------------------------------------
    for line in intro_script.strip().split("\n"):
        if not line.startswith("[루나]"):
            continue
        # Remove the tag itself
        content = line[len("[루나]"):].strip()
        if not content:
            continue

        # Parenthetical stage directions like (따라하며) are OK to ignore
        content_no_paren = re.sub(r"\(.*?\)", "", content).strip()

        if _HANGUL_RE.search(content_no_paren):
            issues.append({
                "activity_id": activity_id,
                "check": "luna_english_only",
                "severity": "error",
                "message": (
                    f"[루나] 대사에 한국어 포함 (루나는 영어만 사용해야 함): "
                    f"'{content[:60]}'"
                ),
            })
            break  # Report once per script

    # ------------------------------------------------------------------
    # [7] key_expression — target English phrase must appear in script
    # ------------------------------------------------------------------
    if key_expression and key_expression.strip():
        # Normalise: lowercase, strip punctuation for loose matching
        expr_norm = re.sub(r"[^\w\s']", "", key_expression.lower()).strip()
        script_norm = intro_script.lower()

        # Check for any significant word from the key expression
        words = [w for w in expr_norm.split() if len(w) > 2]
        matched = any(w in script_norm for w in words) if words else False

        if not matched:
            issues.append({
                "activity_id": activity_id,
                "check": "key_expression",
                "severity": "warning",
                "message": (
                    f"핵심 표현이 스크립트에 등장하지 않음: '{key_expression}'"
                ),
            })

    # ------------------------------------------------------------------
    # [8] popo_coaching — [포포] must have at least 2 lines
    # ------------------------------------------------------------------
    popo_lines = [
        l for l in intro_script.strip().split("\n") if l.startswith("[포포]")
    ]
    if len(popo_lines) < 2:
        issues.append({
            "activity_id": activity_id,
            "check": "popo_coaching",
            "severity": "warning",
            "message": (
                f"[포포] 대사가 {len(popo_lines)}줄뿐 (코칭 역할 부족 — 최소 2줄 필요)"
            ),
        })

    # ------------------------------------------------------------------
    # [9] min_length — intro script should be at least 10 non-empty lines
    # ------------------------------------------------------------------
    script_lines = [l for l in intro_script.strip().split("\n") if l.strip()]
    if len(script_lines) < 10:
        issues.append({
            "activity_id": activity_id,
            "check": "min_length",
            "severity": "warning",
            "message": (
                f"스크립트가 너무 짧음: {len(script_lines)}줄 (최소 10줄 권장)"
            ),
        })

    # ------------------------------------------------------------------
    # [10] outro_cliffhanger — outro should be present and non-trivial
    # ------------------------------------------------------------------
    if outro_script:
        outro_lines = [l for l in outro_script.strip().split("\n") if l.strip()]
        if len(outro_lines) < 3:
            issues.append({
                "activity_id": activity_id,
                "check": "outro_cliffhanger",
                "severity": "warning",
                "message": (
                    f"outro 스크립트가 너무 짧음: {len(outro_lines)}줄 (최소 3줄 권장)"
                ),
            })
    else:
        issues.append({
            "activity_id": activity_id,
            "check": "outro_cliffhanger",
            "severity": "warning",
            "message": "outro_narrator_script가 비어있음 — 클리프행어 없음",
        })

    return issues


def is_passing(issues: list[dict]) -> bool:
    """True if there are no 'error' severity issues."""
    return not any(i.get("severity") == "error" for i in issues)


def format_validation_report(
    activity_id: str,
    issues: list[dict],
    show_passed: bool = True,
) -> str:
    """Return a human-readable validation summary string."""
    errors = [i for i in issues if i.get("severity") == "error"]
    warnings = [i for i in issues if i.get("severity") == "warning"]

    if not issues:
        return f"  [PASS] {activity_id}: 모든 검사 통과"

    lines = [f"  {'[FAIL]' if errors else '[WARN]'} {activity_id}:"]
    for issue in errors:
        lines.append(f"    ERROR  [{issue['check']}] {issue['message']}")
    for issue in warnings:
        lines.append(f"    WARN   [{issue['check']}] {issue['message']}")
    return "\n".join(lines)
