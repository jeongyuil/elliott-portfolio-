"""
Story Generation Pipeline
=========================

Orchestrates the full pipeline:
  1. Load curriculum context from seed files
  2. For each (unit, activity, persona): generate story via Claude API
  3. Validate the generated script
  4. Write JSON + Markdown output files
  5. Write validation reports

Concurrency: asyncio with a semaphore to respect API rate limits.
"""

from __future__ import annotations


import asyncio
import os
from dataclasses import dataclass, field
from typing import List, Optional

from .context_loader import ActivityContext, CurriculumContext, load_curriculum
from .generator import GeneratedStory, StoryGenerator
from .output_writer import (
    write_session_report,
    write_story,
    write_summary_report,
)
from .personas import ALL_PERSONA_KEYS, PERSONAS, Persona
from .validator import format_validation_report, is_passing, validate_story


@dataclass
class PipelineConfig:
    themes: list[str]                    # e.g. ["earth_crew", "kpop_hunters"]
    personas: list[str] = field(         # e.g. ["young_beginner", "older_intermediate"]
        default_factory=lambda: ALL_PERSONA_KEYS
    )
    week_filter: int | None = None       # Only process this week (1-4)
    session_filter: str | None = None    # Only process this curriculum_unit_id
    output_dir: str = "stories"          # Root output directory
    concurrency: int = 3                 # Parallel API calls
    dry_run: bool = False                # Skip API calls, produce empty stubs
    scripts_dir: str | None = None       # Override scripts/ path
    verbose: bool = True


@dataclass
class StoryResult:
    theme: str
    unit_id: str
    activity_id: str
    persona: str
    passed: bool
    issues: list[dict]
    json_path: str = ""
    md_path: str = ""
    error: str = ""                      # Set if an exception occurred during generation


class StoryPipeline:
    """End-to-end story generation pipeline."""

    def __init__(self, config: PipelineConfig, generator: StoryGenerator | None = None):
        self.config = config
        self._generator = generator  # Injected or created lazily

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    async def run(self) -> list[StoryResult]:
        """Run the pipeline for all configured themes / personas."""
        cfg = self.config
        all_results: list[StoryResult] = []

        if not cfg.dry_run and self._generator is None:
            self._generator = StoryGenerator()

        # Collect all (unit, activity, persona) jobs across themes
        jobs: list[tuple[CurriculumContext, ActivityContext, Persona]] = []
        for theme in cfg.themes:
            units = load_curriculum(
                theme=theme,
                scripts_dir=cfg.scripts_dir,
                week_filter=cfg.week_filter,
                session_filter=cfg.session_filter,
            )
            for unit in units:
                for activity in unit.activities:
                    for persona_key in cfg.personas:
                        persona = PERSONAS[persona_key]
                        jobs.append((unit, activity, persona))

        total = len(jobs)
        if cfg.verbose:
            print(f"\n[Pipeline] {total} jobs queued "
                  f"({len(cfg.themes)} theme(s) × "
                  f"{len(cfg.personas)} persona(s))")
            if cfg.dry_run:
                print("[Pipeline] DRY RUN — no API calls will be made")

        # Run with concurrency control
        sem = asyncio.Semaphore(cfg.concurrency)
        counter = {"done": 0}

        async def run_job(
            unit: CurriculumContext,
            activity: ActivityContext,
            persona: Persona,
        ) -> StoryResult:
            async with sem:
                counter["done"] += 1
                idx = counter["done"]
                label = f"{unit.curriculum_unit_id}/{persona.key}"
                if cfg.verbose:
                    print(f"  [{idx:3d}/{total}] generating {label} ...")
                result = await self._run_single(unit, activity, persona)
                status = "PASS" if result.passed else ("ERR" if result.error else "FAIL")
                if cfg.verbose:
                    print(f"  [{idx:3d}/{total}] {status:4s} {label}")
                return result

        tasks = [run_job(u, a, p) for u, a, p in jobs]
        all_results = list(await asyncio.gather(*tasks, return_exceptions=False))

        # Write per-session reports
        self._write_session_reports(all_results)

        # Write overall summary
        run_config = {
            "themes": cfg.themes,
            "personas": cfg.personas,
            "week_filter": cfg.week_filter,
            "session_filter": cfg.session_filter,
            "dry_run": cfg.dry_run,
        }
        summary_path = write_summary_report(cfg.output_dir, [r.__dict__ for r in all_results], run_config)

        # Print summary
        if cfg.verbose:
            self._print_summary(all_results, summary_path)

        return all_results

    # ------------------------------------------------------------------
    # Single-job execution
    # ------------------------------------------------------------------

    async def _run_single(
        self,
        unit: CurriculumContext,
        activity: ActivityContext,
        persona: Persona,
    ) -> StoryResult:
        cfg = self.config

        if cfg.dry_run:
            story = GeneratedStory(
                intro_narrator_script="[DRY RUN] 생성 건너뜀",
                outro_narrator_script="[DRY RUN]",
                raw_response="",
                model="dry-run",
                input_tokens=0,
                output_tokens=0,
            )
            issues: list[dict] = []
            passed = True
        else:
            try:
                story = await self._generator.generate(unit, activity, persona)
            except Exception as exc:
                return StoryResult(
                    theme=unit.story_theme,
                    unit_id=unit.curriculum_unit_id,
                    activity_id=activity.activity_id,
                    persona=persona.key,
                    passed=False,
                    issues=[],
                    error=str(exc),
                )

            issues = validate_story(
                activity_id=activity.activity_id,
                intro_script=story.intro_narrator_script,
                key_expression=activity.key_expression,
                outro_script=story.outro_narrator_script,
            )
            passed = is_passing(issues)

        json_path, md_path = write_story(
            base_dir=cfg.output_dir,
            unit=unit,
            activity=activity,
            persona=persona,
            story=story,
            issues=issues,
            validation_passed=passed,
        )

        return StoryResult(
            theme=unit.story_theme,
            unit_id=unit.curriculum_unit_id,
            activity_id=activity.activity_id,
            persona=persona.key,
            passed=passed,
            issues=issues,
            json_path=json_path,
            md_path=md_path,
        )

    # ------------------------------------------------------------------
    # Reporting helpers
    # ------------------------------------------------------------------

    def _write_session_reports(self, all_results: list[StoryResult]) -> None:
        # Group by (theme, unit_id)
        by_session: dict[tuple[str, str], list[dict]] = {}
        for r in all_results:
            key = (r.theme, r.unit_id)
            by_session.setdefault(key, []).append({
                "persona": r.persona,
                "activity_id": r.activity_id,
                "passed": r.passed,
                "issues": r.issues,
                "error": r.error,
            })

        for (theme, unit_id), session_results in by_session.items():
            write_session_report(
                base_dir=self.config.output_dir,
                theme=theme,
                unit_id=unit_id,
                session_results=session_results,
            )

    def _print_summary(self, results: list[StoryResult], summary_path: str) -> None:
        total = len(results)
        passed = sum(1 for r in results if r.passed)
        errors = sum(1 for r in results if r.error)
        failed = total - passed - errors

        print(f"\n{'='*60}")
        print("  PIPELINE COMPLETE")
        print(f"{'='*60}")
        print(f"  Total:   {total}")
        print(f"  Pass:    {passed}  ({passed/total*100:.0f}%)")
        print(f"  Fail:    {failed}")
        print(f"  Error:   {errors}")
        print(f"\n  Summary: {summary_path}")
        print(f"  Output:  {self.config.output_dir}/generated/")

        # Show failures
        failures = [r for r in results if not r.passed]
        if failures:
            print(f"\n  Failed stories ({len(failures)}):")
            for r in failures[:10]:
                label = f"{r.theme}/{r.unit_id}/{r.persona}"
                if r.error:
                    print(f"    [ERROR] {label}: {r.error[:80]}")
                else:
                    err_checks = [i["check"] for i in r.issues if i.get("severity") == "error"]
                    print(f"    [FAIL]  {label}: {', '.join(err_checks)}")
            if len(failures) > 10:
                print(f"    ... and {len(failures)-10} more (see _summary_report.json)")
        print(f"{'='*60}\n")
