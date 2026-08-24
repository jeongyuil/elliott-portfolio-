"""
Story Generator
===============

Two backend options for generating story scripts:

  ClaudeCliGenerator  (default)
    Uses `claude -p` CLI subprocess — no API key needed.
    Authentication comes from Claude Code CLI login (`claude login`).
    Concurrency via asyncio.create_subprocess_exec + Semaphore.

  StoryGenerator  (SDK-based, legacy)
    Uses the Anthropic Python SDK directly.
    Requires ANTHROPIC_API_KEY environment variable.
    Kept for CI/CD or environments without Claude Code installed.

The pipeline.py defaults to ClaudeCliGenerator unless --use-sdk is passed.
"""

from __future__ import annotations


import asyncio
import json
import os
import re
import shutil
from dataclasses import dataclass

from .context_loader import ActivityContext, CurriculumContext
from .personas import Persona
from .prompt_builder import SYSTEM_PROMPT, build_user_prompt


@dataclass
class GeneratedStory:
    intro_narrator_script: str
    outro_narrator_script: str
    raw_response: str
    model: str
    input_tokens: int    # -1 when using CLI (not reported)
    output_tokens: int   # -1 when using CLI (not reported)


# ---------------------------------------------------------------------------
# Claude Code CLI backend  (default)
# ---------------------------------------------------------------------------

class ClaudeCliGenerator:
    """
    Generates stories via `claude -p` subprocess.

    Prerequisites:
      - Claude Code CLI installed  (claude --version)
      - Logged in via  claude login
      - No ANTHROPIC_API_KEY required

    Concurrency is managed by the pipeline's asyncio Semaphore;
    each call spawns an independent subprocess so they run in parallel.
    """

    DEFAULT_MODEL = "sonnet"   # alias → resolved to latest claude-sonnet by CLI

    def __init__(
        self,
        model: str | None = None,
        timeout: int = 120,
    ):
        cli = shutil.which("claude")
        if not cli:
            raise RuntimeError(
                "Claude Code CLI not found. "
                "Install from https://claude.ai/code or check your PATH."
            )
        self._cli = cli
        self.model = model or self.DEFAULT_MODEL
        self.timeout = timeout

    async def generate(
        self,
        unit: CurriculumContext,
        activity: ActivityContext,
        persona: Persona,
    ) -> GeneratedStory:
        """Generate a story script via `claude -p` subprocess."""
        user_prompt = build_user_prompt(unit, activity, persona)
        raw = await self._run_cli(user_prompt)
        intro, outro = _parse_story_response(raw)

        return GeneratedStory(
            intro_narrator_script=intro,
            outro_narrator_script=outro,
            raw_response=raw,
            model=f"claude-cli/{self.model}",
            input_tokens=-1,   # not reported by CLI
            output_tokens=-1,
        )

    async def _run_cli(self, user_prompt: str) -> str:
        """Run `claude -p` as an async subprocess and return stdout.

        We use create_subprocess_exec (not shell=True) so SYSTEM_PROMPT
        is passed as a plain Python string argument — no escaping needed.
        """
        cmd = [
            self._cli,
            "--print",
            "--model", self.model,
            "--system-prompt", SYSTEM_PROMPT,
            "--no-session-persistence",
            "--output-format", "text",
            "--dangerously-skip-permissions",  # non-interactive: no file/tool access
        ]

        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        try:
            stdout, stderr = await asyncio.wait_for(
                proc.communicate(input=user_prompt.encode("utf-8")),
                timeout=self.timeout,
            )
        except asyncio.TimeoutError:
            proc.kill()
            raise RuntimeError(
                f"claude -p timed out after {self.timeout}s. "
                "Try increasing --timeout or reducing --concurrency."
            )

        if proc.returncode != 0:
            err_msg = stderr.decode("utf-8", errors="replace").strip()
            raise RuntimeError(
                f"claude -p exited with code {proc.returncode}: {err_msg[:200]}"
            )

        return stdout.decode("utf-8", errors="replace")


# ---------------------------------------------------------------------------
# Anthropic SDK backend  (needs ANTHROPIC_API_KEY)
# ---------------------------------------------------------------------------

class StoryGenerator:
    """
    Async story generator backed by Anthropic Python SDK.

    Requires:  export ANTHROPIC_API_KEY='sk-ant-...'

    Use this when:
      - Running in CI/CD (no Claude Code CLI installed)
      - You want explicit temperature / max_tokens control
      - You need accurate token counts for cost tracking
    """

    DEFAULT_MODEL = "claude-sonnet-4-6"

    def __init__(
        self,
        api_key: str | None = None,
        model: str | None = None,
        temperature: float = 0.85,
        max_tokens: int = 4096,
    ):
        try:
            import anthropic as _anthropic
        except ImportError:
            raise ImportError(
                "anthropic package not installed. "
                "Run: pip install anthropic>=0.40.0"
            )

        key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not key:
            raise ValueError(
                "ANTHROPIC_API_KEY is not set.\n"
                "Either export it, or use the default ClaudeCliGenerator "
                "(which uses Claude Code CLI auth — no key needed)."
            )
        self._client = _anthropic.AsyncAnthropic(api_key=key)
        self.model = model or self.DEFAULT_MODEL
        self.temperature = temperature
        self.max_tokens = max_tokens

    async def generate(
        self,
        unit: CurriculumContext,
        activity: ActivityContext,
        persona: Persona,
    ) -> GeneratedStory:
        """Generate a story script via Anthropic SDK."""
        user_prompt = build_user_prompt(unit, activity, persona)

        response = await self._client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_prompt}],
            temperature=self.temperature,
        )

        raw = "".join(
            block.text for block in response.content if block.type == "text"
        )

        intro, outro = _parse_story_response(raw)

        return GeneratedStory(
            intro_narrator_script=intro,
            outro_narrator_script=outro,
            raw_response=raw,
            model=self.model,
            input_tokens=response.usage.input_tokens,
            output_tokens=response.usage.output_tokens,
        )


# ---------------------------------------------------------------------------
# Shared response parser
# ---------------------------------------------------------------------------

def _parse_story_response(raw: str) -> tuple[str, str]:
    """
    Extract intro_narrator_script and outro_narrator_script from the LLM response.

    Expected format:
        ```json
        {
          "intro_narrator_script": "...",
          "outro_narrator_script": "..."
        }
        ```

    Falls back to regex extraction if JSON parsing fails.
    """
    # Step 1: strip ```json ... ``` fences
    json_str = raw.strip()
    fence_match = re.search(r"```(?:json)?\s*([\s\S]+?)\s*```", json_str)
    if fence_match:
        json_str = fence_match.group(1).strip()

    # Step 2: try JSON parse
    try:
        data = json.loads(json_str)
        intro = data.get("intro_narrator_script", "").strip()
        outro = data.get("outro_narrator_script", "").strip()
        if intro:
            return intro, outro
    except (json.JSONDecodeError, AttributeError):
        pass

    # Step 3: regex fallback — extract the two fields individually
    intro = _extract_field(raw, "intro_narrator_script")
    outro = _extract_field(raw, "outro_narrator_script")

    if not intro:
        # Last resort: treat the whole response as the intro script
        intro = raw.strip()

    return intro, outro


def _extract_field(text: str, field: str) -> str:
    """Extract a JSON string field using regex, handling multi-line values."""
    pattern = rf'"{re.escape(field)}"\s*:\s*"((?:[^"\\]|\\.)*)\"'
    match = re.search(pattern, text, re.DOTALL)
    if match:
        value = match.group(1)
        value = value.replace("\\n", "\n").replace('\\"', '"').replace("\\\\", "\\")
        return value.strip()
    return ""
