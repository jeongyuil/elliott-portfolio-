"""
Curriculum Context Loader
=========================

Loads curriculum units and activities from the seed Python files.
No database connection required — works purely from the static seed data.

Themes:
  - "earth_crew"      → scripts/seed_curriculum.py
  - "kpop_hunters"    → scripts/seed_curriculum_kpop.py
  - "dino_expedition" → scripts/seed_curriculum_dino.py
"""

from __future__ import annotations


import ast
import os
import re
import sys
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class ActivityContext:
    activity_id: str
    name: str
    activity_type: str
    key_expression: str
    intro_narrator_script: str       # existing baseline (may be empty)
    instructions_for_ai: str
    estimated_duration_minutes: int
    target_skills: List[str]


@dataclass
class CurriculumContext:
    curriculum_unit_id: str
    title: str
    description: str
    week: int
    phase: int
    difficulty_level: int
    korean_ratio: int
    target_skills: List[str]
    story_theme: str
    activities: List[ActivityContext]


# Map theme key → seed module filename (relative to scripts/)
THEME_SEED_FILES: dict = {
    "earth_crew": "seed_curriculum.py",
    "kpop_hunters": "seed_curriculum_kpop.py",
    "dino_expedition": "seed_curriculum_dino.py",
}

THEME_LABELS: dict[str, str] = {
    "earth_crew": "어스 크루 대모험",
    "kpop_hunters": "케이팝 데몬 헌터스",
    "dino_expedition": "공룡 탐험대",
}


def _extract_list_literal(source: str, var_name: str) -> list:
    """
    Extract a top-level list literal assigned to `var_name` from Python source
    using the AST, without executing any imports.

    Handles multi-line strings (triple-quoted) inside list items by temporarily
    replacing them with placeholders so ast.literal_eval can parse cleanly.
    """
    # Find the assignment in the AST
    try:
        tree = ast.parse(source)
    except SyntaxError:
        # Python 3.9 may choke on newer syntax in type annotations.
        # Strip type annotations from the file before parsing (we only need data).
        source_stripped = _strip_type_annotations(source)
        tree = ast.parse(source_stripped)

    for node in ast.walk(tree):
        if not isinstance(node, ast.Assign):
            continue
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id == var_name:
                try:
                    return ast.literal_eval(node.value)
                except (ValueError, TypeError):
                    pass

    return []


def _strip_type_annotations(source: str) -> str:
    """
    Remove lines that cause Python 3.9 parse failures (like `Mapped[str | None]`)
    by replacing class/function bodies with pass where needed. For our purposes
    we only need to extract `CURRICULUM_UNITS` and `ACTIVITIES` list literals,
    so we can safely strip everything that isn't those two assignments.
    """
    lines = []
    capture = False
    depth = 0

    for line in source.split("\n"):
        stripped = line.strip()

        # Start of a target assignment
        if re.match(r"^(CURRICULUM_UNITS|ACTIVITIES)\s*=\s*\[", stripped):
            capture = True
            depth = 0

        if capture:
            depth += line.count("[") + line.count("(") + line.count("{")
            depth -= line.count("]") + line.count(")") + line.count("}")
            lines.append(line)
            if depth <= 0:
                capture = False
        # Skip import lines and class/function defs to avoid 3.10+ syntax errors
        elif stripped.startswith(("import ", "from ", "class ", "def ", "@")):
            lines.append("# stripped")
        elif "|" in line and "Mapped" in line:
            lines.append("# stripped")
        else:
            lines.append(line)

    return "\n".join(lines)


def _load_seed_data(theme: str, scripts_dir: str):
    """
    Load CURRICULUM_UNITS and ACTIVITIES from a seed file via AST extraction.
    No Python imports from the seed file are executed — safe for any Python version.
    """
    filename = THEME_SEED_FILES.get(theme)
    if not filename:
        raise ValueError(
            f"Unknown theme '{theme}'. Valid themes: {list(THEME_SEED_FILES)}"
        )

    seed_path = os.path.join(scripts_dir, filename)
    if not os.path.exists(seed_path):
        raise FileNotFoundError(
            f"Seed file not found: {seed_path}"
        )

    with open(seed_path, encoding="utf-8") as f:
        source = f.read()

    curriculum_units = _extract_list_literal(source, "CURRICULUM_UNITS")
    activities = _extract_list_literal(source, "ACTIVITIES")

    return curriculum_units, activities


def load_curriculum(
    theme: str,
    scripts_dir: Optional[str] = None,
    week_filter: Optional[int] = None,
    session_filter: Optional[str] = None,
) -> List[CurriculumContext]:
    """
    Load curriculum context for a given theme.

    Args:
        theme:          One of "earth_crew", "kpop_hunters", "dino_expedition"
        scripts_dir:    Path to scripts/ directory. Defaults to the scripts/ dir
                        next to this file's parent.
        week_filter:    Only load this week number (1-4).
        session_filter: Only load this curriculum_unit_id (e.g. "W1_S1_meet_luna_popo").

    Returns:
        List of CurriculumContext objects, each with their nested activities.
    """
    if scripts_dir is None:
        scripts_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    raw_units, raw_activities = _load_seed_data(theme, scripts_dir)

    # Build activity lookup: curriculum_unit_id → [activity, ...]
    act_by_unit = {}
    for act in raw_activities:
        uid = act.get("curriculum_unit_id", "")
        act_by_unit.setdefault(uid, []).append(act)

    results = []
    for unit in raw_units:
        uid = unit["curriculum_unit_id"]

        # Apply filters
        if week_filter is not None and unit.get("week") != week_filter:
            continue
        if session_filter is not None and uid != session_filter:
            continue

        activities: list[ActivityContext] = []
        for act in act_by_unit.get(uid, []):
            activities.append(ActivityContext(
                activity_id=act.get("activity_id", ""),
                name=act.get("name", ""),
                activity_type=act.get("activity_type", ""),
                key_expression=act.get("key_expression", ""),
                intro_narrator_script=act.get("intro_narrator_script", ""),
                instructions_for_ai=act.get("instructions_for_ai", ""),
                estimated_duration_minutes=act.get("estimated_duration_minutes", 5),
                target_skills=act.get("target_skills") or [],
            ))

        results.append(CurriculumContext(
            curriculum_unit_id=uid,
            title=unit.get("title", ""),
            description=unit.get("description", ""),
            week=unit.get("week", 0),
            phase=unit.get("phase", 1),
            difficulty_level=unit.get("difficulty_level", 1),
            korean_ratio=unit.get("korean_ratio", 65),
            target_skills=unit.get("target_skills") or [],
            story_theme=theme,
            activities=activities,
        ))

    return results


def list_themes() -> list[str]:
    return list(THEME_SEED_FILES.keys())
