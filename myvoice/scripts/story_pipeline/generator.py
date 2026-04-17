"""
Story Generator
===============

Calls the Claude API to generate story scripts for a given
(curriculum_unit, activity, persona) combination.

Why Claude over GPT-4o-mini:
  - Better Korean-English bilingual creative output
  - Stronger instruction-following for complex character rules
  - Already integrated in this project (story_writer_agent.py)
  - Structured JSON output reliability for mixed-language content
"""

from __future__ import annotations


import json
import os
import re
from dataclasses import dataclass

import anthropic

from .context_loader import ActivityContext, CurriculumContext
from .personas import Persona
from .prompt_builder import SYSTEM_PROMPT, build_user_prompt


@dataclass
class GeneratedStory:
    intro_narrator_script: str
    outro_narrator_script: str
    raw_response: str
    model: str
    input_tokens: int
    output_tokens: int


class StoryGenerator:
    """Async story generator backed by Claude API."""

    DEFAULT_MODEL = "claude-sonnet-4-6"

    def __init__(
        self,
        api_key: str | None = None,
        model: str | None = None,
        temperature: float = 0.85,
        max_tokens: int = 4096,
    ):
        key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not key:
            raise ValueError(
                "ANTHROPIC_API_KEY is not set. "
                "Export it with: export ANTHROPIC_API_KEY='sk-ant-...'"
            )
        self._client = anthropic.AsyncAnthropic(api_key=key)
        self.model = model or self.DEFAULT_MODEL
        self.temperature = temperature
        self.max_tokens = max_tokens

    async def generate(
        self,
        unit: CurriculumContext,
        activity: ActivityContext,
        persona: Persona,
    ) -> GeneratedStory:
        """Generate a story script for the given combination."""
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
# Response parser
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
    # Match "field_name": "...(possibly multiline)..."
    pattern = rf'"{re.escape(field)}"\s*:\s*"((?:[^"\\]|\\.)*)\"'
    match = re.search(pattern, text, re.DOTALL)
    if match:
        # Unescape JSON string escapes
        value = match.group(1)
        value = value.replace("\\n", "\n").replace('\\"', '"').replace("\\\\", "\\")
        return value.strip()
    return ""
