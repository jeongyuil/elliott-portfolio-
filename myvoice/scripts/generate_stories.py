#!/usr/bin/env python3
"""
밤토리 Story Generation CLI
=============================

Generates story script variations for each (theme × curriculum_unit × persona)
combination using Claude API. Outputs JSON + Markdown files for human review
before importing into the database.

Usage examples:
    # Dry-run — verify structure without calling API
    python scripts/generate_stories.py --dry-run --theme earth_crew

    # Generate one week of stories for all personas
    python scripts/generate_stories.py --theme earth_crew --week 1

    # Generate a single session for a specific persona
    python scripts/generate_stories.py --theme earth_crew \\
        --session W1_S1_meet_luna_popo --persona young_beginner

    # Generate ALL themes, ALL weeks, ALL personas
    python scripts/generate_stories.py --all-themes

    # Show what would be generated (no API calls)
    python scripts/generate_stories.py --all-themes --dry-run

    # Validate already-generated output without re-generating
    python scripts/generate_stories.py --validate-only

Output:
    stories/generated/<theme>/<unit_id>/<persona>.json
    stories/generated/<theme>/<unit_id>/<persona>.md
    stories/generated/<theme>/<unit_id>/_report.json
    stories/_summary_report.json
"""

import argparse
import asyncio
import json
import os
import sys

# Make sure we can import from scripts/ and app/
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, REPO_ROOT)
sys.path.insert(0, SCRIPTS_DIR)

from story_pipeline import ALL_PERSONA_KEYS, PipelineConfig, StoryPipeline, list_themes
from story_pipeline.context_loader import load_curriculum
from story_pipeline.output_writer import story_output_dir
from story_pipeline.personas import PERSONAS
from story_pipeline.validator import format_validation_report, validate_story


# ---------------------------------------------------------------------------
# CLI argument parsing
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="generate_stories",
        description="밤토리 스토리 생성 파이프라인 CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )

    # Target selection
    target = parser.add_mutually_exclusive_group()
    target.add_argument(
        "--all-themes",
        action="store_true",
        help="모든 테마 (earth_crew, kpop_hunters, dino_expedition) 처리",
    )
    target.add_argument(
        "--theme",
        choices=list_themes(),
        metavar="|".join(list_themes()),
        help="처리할 스토리 테마",
    )

    # Scope filters
    parser.add_argument(
        "--week",
        type=int,
        choices=[1, 2, 3, 4],
        help="특정 주차만 처리 (1-4)",
    )
    parser.add_argument(
        "--session",
        type=str,
        metavar="UNIT_ID",
        help="특정 커리큘럼 세션만 처리 (예: W1_S1_meet_luna_popo)",
    )
    parser.add_argument(
        "--persona",
        choices=ALL_PERSONA_KEYS,
        metavar="|".join(ALL_PERSONA_KEYS),
        help="특정 페르소나만 처리 (기본: 전체)",
    )

    # Execution mode
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="생성 없이 구조만 확인 (테스트용)",
    )
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="기존 생성 파일만 검증 (새로 생성하지 않음)",
    )
    parser.add_argument(
        "--use-sdk",
        action="store_true",
        help=(
            "Anthropic Python SDK로 생성 (ANTHROPIC_API_KEY 필요). "
            "기본값은 Claude Code CLI 인증 사용."
        ),
    )

    # Output
    parser.add_argument(
        "--output-dir",
        default="stories",
        metavar="DIR",
        help="출력 디렉터리 (기본: stories/)",
    )
    parser.add_argument(
        "--concurrency",
        type=int,
        default=3,
        help="동시 생성 수 (기본: 3)",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="진행 상황 출력 최소화",
    )

    # Information
    parser.add_argument(
        "--list-personas",
        action="store_true",
        help="사용 가능한 페르소나 목록 출력 후 종료",
    )
    parser.add_argument(
        "--list-sessions",
        action="store_true",
        help="선택된 테마의 세션 목록 출력 후 종료",
    )

    return parser


# ---------------------------------------------------------------------------
# Validate-only mode
# ---------------------------------------------------------------------------

def run_validate_only(args: argparse.Namespace) -> int:
    """Re-validate already-generated JSON files. Returns exit code."""
    import glob

    pattern = os.path.join(args.output_dir, "generated", "**", "*.json")
    files = [f for f in glob.glob(pattern, recursive=True) if not os.path.basename(f).startswith("_")]

    if not files:
        print(f"No generated story files found under {args.output_dir}/generated/")
        return 1

    total = errors = warnings_only = passed = 0
    for path in sorted(files):
        with open(path, encoding="utf-8") as f:
            data = json.load(f)

        story = data.get("story", {})
        curriculum = data.get("curriculum", {})
        meta = data.get("meta", {})

        intro = story.get("intro_narrator_script", "")
        outro = story.get("outro_narrator_script", "")
        key_expr = curriculum.get("key_expression", "")
        act_id = meta.get("activity_id", os.path.basename(path))

        issues = validate_story(act_id, intro, key_expr, outro)
        err_issues = [i for i in issues if i.get("severity") == "error"]
        warn_issues = [i for i in issues if i.get("severity") == "warning"]

        total += 1
        if err_issues:
            errors += 1
            rel = os.path.relpath(path, args.output_dir)
            print(format_validation_report(rel, issues))
        elif warn_issues:
            warnings_only += 1
            rel = os.path.relpath(path, args.output_dir)
            print(format_validation_report(rel, issues))
        else:
            passed += 1

    print(f"\n{'='*60}")
    print(f"  검증 결과: {total}개 파일")
    print(f"  Pass:     {passed}")
    print(f"  Warning:  {warnings_only}")
    print(f"  Error:    {errors}")
    print(f"{'='*60}")
    return 0 if errors == 0 else 1


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

async def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    # ------------------------------------------------------------------
    # Info commands
    # ------------------------------------------------------------------
    if args.list_personas:
        print("\n사용 가능한 페르소나:")
        for key, p in PERSONAS.items():
            print(f"  {key:<25} {p.label}  ({p.age_band}세, {p.language_level}, 한국어 {p.korean_ratio}%)")
        return 0

    if args.list_sessions:
        themes = list_themes() if args.all_themes else ([args.theme] if args.theme else list_themes())
        for theme in themes:
            print(f"\n[{theme}]")
            units = load_curriculum(theme, scripts_dir=SCRIPTS_DIR)
            for unit in units:
                activities = unit.activities
                print(f"  W{unit.week}  {unit.curriculum_unit_id:<45} ({len(activities)} activities)")
        return 0

    # ------------------------------------------------------------------
    # Validate-only
    # ------------------------------------------------------------------
    if args.validate_only:
        return run_validate_only(args)

    # ------------------------------------------------------------------
    # Theme selection
    # ------------------------------------------------------------------
    if args.all_themes:
        themes = list_themes()
    elif args.theme:
        themes = [args.theme]
    else:
        parser.print_help()
        print("\nERROR: --theme 또는 --all-themes 중 하나를 지정하세요.")
        return 1

    # ------------------------------------------------------------------
    # Persona selection
    # ------------------------------------------------------------------
    personas = [args.persona] if args.persona else ALL_PERSONA_KEYS

    # ------------------------------------------------------------------
    # Run pipeline
    # ------------------------------------------------------------------
    # ------------------------------------------------------------------
    # Print auth mode info
    # ------------------------------------------------------------------
    if not args.dry_run and not getattr(args, "validate_only", False):
        if args.use_sdk:
            print("[Auth] Anthropic SDK 모드 (ANTHROPIC_API_KEY 필요)")
        else:
            print("[Auth] Claude Code CLI 모드 (claude login 인증 사용)")

    config = PipelineConfig(
        themes=themes,
        personas=personas,
        week_filter=args.week,
        session_filter=args.session,
        output_dir=args.output_dir,
        concurrency=args.concurrency,
        dry_run=args.dry_run,
        use_sdk=args.use_sdk,
        scripts_dir=SCRIPTS_DIR,
        verbose=not args.quiet,
    )

    pipeline = StoryPipeline(config)

    try:
        results = await pipeline.run()
    except KeyboardInterrupt:
        print("\n[!] 중단됨 (Ctrl+C)")
        return 130

    # Exit code: non-zero if any story failed validation
    failed = sum(1 for r in results if not r.passed)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
