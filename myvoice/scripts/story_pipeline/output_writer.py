"""
Output Writer
=============

Writes generated stories to:
  stories/generated/<theme>/<unit_id>/<persona_key>.json   — machine-readable
  stories/generated/<theme>/<unit_id>/<persona_key>.md     — human-readable review
  stories/generated/<theme>/<unit_id>/_report.json         — validation summary per session

Directory structure:
  stories/
    generated/
      earth_crew/
        W1_S1_meet_luna_popo/
          young_beginner.json
          young_beginner.md
          young_intermediate.json
          ...
          _report.json
      kpop_hunters/
        ...
    _summary_report.json     ← overall run summary
"""

from __future__ import annotations


import json
import os
from datetime import datetime, timezone

from .context_loader import ActivityContext, CurriculumContext
from .generator import GeneratedStory
from .personas import Persona
from .validator import format_validation_report


def story_output_dir(base_dir: str, theme: str, unit_id: str) -> str:
    return os.path.join(base_dir, "generated", theme, unit_id)


def write_story(
    base_dir: str,
    unit: CurriculumContext,
    activity: ActivityContext,
    persona: Persona,
    story: GeneratedStory,
    issues: list[dict],
    validation_passed: bool,
) -> tuple[str, str]:
    """
    Write JSON and Markdown files for one generated story.

    Returns:
        (json_path, md_path)
    """
    out_dir = story_output_dir(base_dir, unit.story_theme, unit.curriculum_unit_id)
    os.makedirs(out_dir, exist_ok=True)

    # ------------------------------------------------------------------
    # Build the payload
    # ------------------------------------------------------------------
    payload = {
        "meta": {
            "curriculum_unit_id": unit.curriculum_unit_id,
            "activity_id": activity.activity_id,
            "theme": unit.story_theme,
            "persona": persona.key,
            "persona_label": persona.label,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "model": story.model,
            "tokens": {
                "input": story.input_tokens,
                "output": story.output_tokens,
            },
        },
        "curriculum": {
            "title": unit.title,
            "description": unit.description,
            "week": unit.week,
            "difficulty_level": unit.difficulty_level,
            "korean_ratio": unit.korean_ratio,
            "target_skills": unit.target_skills,
            "key_expression": activity.key_expression,
        },
        "story": {
            "intro_narrator_script": story.intro_narrator_script,
            "outro_narrator_script": story.outro_narrator_script,
            "validation_passed": validation_passed,
            "validation_issues": issues,
        },
    }

    # ------------------------------------------------------------------
    # Write JSON
    # ------------------------------------------------------------------
    json_path = os.path.join(out_dir, f"{persona.key}.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    # ------------------------------------------------------------------
    # Write Markdown
    # ------------------------------------------------------------------
    md_path = os.path.join(out_dir, f"{persona.key}.md")
    md = _build_markdown(payload, issues, validation_passed)
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md)

    return json_path, md_path


def write_session_report(
    base_dir: str,
    theme: str,
    unit_id: str,
    session_results: list[dict],
) -> str:
    """Write _report.json with validation summary for all personas in a session."""
    out_dir = story_output_dir(base_dir, theme, unit_id)
    os.makedirs(out_dir, exist_ok=True)

    total = len(session_results)
    passed = sum(1 for r in session_results if r.get("passed"))
    failed = total - passed

    report = {
        "session": unit_id,
        "theme": theme,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "summary": {
            "total": total,
            "passed": passed,
            "failed": failed,
            "pass_rate": f"{(passed/total*100):.0f}%" if total else "N/A",
        },
        "personas": session_results,
    }

    report_path = os.path.join(out_dir, "_report.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    return report_path


def write_summary_report(
    base_dir: str,
    all_results: list[dict],
    run_config: dict,
) -> str:
    """Write _summary_report.json at the base stories/ directory."""
    total = len(all_results)
    passed = sum(1 for r in all_results if r.get("passed"))

    report = {
        "run": {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "config": run_config,
            "total_stories": total,
            "passed": passed,
            "failed": total - passed,
            "pass_rate": f"{(passed/total*100):.0f}%" if total else "N/A",
        },
        "stories": all_results,
    }

    os.makedirs(base_dir, exist_ok=True)
    report_path = os.path.join(base_dir, "_summary_report.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    return report_path


# ---------------------------------------------------------------------------
# Markdown renderer
# ---------------------------------------------------------------------------

def _build_markdown(payload: dict, issues: list[dict], passed: bool) -> str:
    meta = payload["meta"]
    cur = payload["curriculum"]
    story = payload["story"]

    status = "PASS" if passed else "FAIL"
    badge = "✅" if passed else "❌"

    errors = [i for i in issues if i.get("severity") == "error"]
    warnings = [i for i in issues if i.get("severity") == "warning"]

    lines = [
        f"# {cur['title']} — {meta['persona_label']}",
        "",
        f"**검증 결과**: {badge} {status}  ",
        f"**테마**: {meta['theme']}  ",
        f"**세션**: {meta['curriculum_unit_id']}  ",
        f"**Activity**: {meta['activity_id']}  ",
        f"**생성 모델**: {meta['model']}  ",
        f"**생성 일시**: {meta['generated_at']}  ",
        f"**토큰**: input {meta['tokens']['input']} / output {meta['tokens']['output']}",
        "",
        "---",
        "",
        "## 커리큘럼 정보",
        "",
        f"- **핵심 표현**: `{cur['key_expression']}`" if cur.get('key_expression') else "- **핵심 표현**: (없음)",
        f"- **학습 스킬**: {', '.join(cur['target_skills'])}",
        f"- **난이도**: {cur['difficulty_level']}/3",
        f"- **한국어 비율**: {cur['korean_ratio']}%",
        "",
        "---",
        "",
        "## 생성된 스크립트",
        "",
        "### Intro Narrator Script",
        "",
        "```",
        story["intro_narrator_script"],
        "```",
        "",
    ]

    if story.get("outro_narrator_script"):
        lines += [
            "### Outro Narrator Script",
            "",
            "```",
            story["outro_narrator_script"],
            "```",
            "",
        ]

    lines += [
        "---",
        "",
        "## 검증 결과",
        "",
    ]

    if not issues:
        lines.append("모든 검사 통과 ✅")
    else:
        if errors:
            lines.append("### Errors (수정 필요)")
            for e in errors:
                lines.append(f"- **[{e['check']}]** {e['message']}")
            lines.append("")
        if warnings:
            lines.append("### Warnings (검토 권장)")
            for w in warnings:
                lines.append(f"- [{w['check']}] {w['message']}")

    return "\n".join(lines) + "\n"
