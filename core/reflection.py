import json
from importlib.resources import files
from typing import Literal, Optional

from pydantic import BaseModel

from core.llm_parser import get_client
from core.normalizer import normalize_intent_data
from core.observation import Observation
from core.plan_schema import PlanStep

REFLECTION_PROMPT_NAME = "reflection_prompt.txt"


class Reflection(BaseModel):
    status: Literal["retry", "continue", "stop"]
    reason: str
    next_step: Optional[PlanStep] = None


def build_reflection_prompt(
    query: str,
    goal: str,
    failed_step: PlanStep,
    observation: Observation
):
    template = files("prompts").joinpath(REFLECTION_PROMPT_NAME).read_text(
        encoding="utf-8"
    )
    return (
        template
        .replace("{{USER_QUERY}}", query)
        .replace("{{GOAL}}", goal)
        .replace("{{FAILED_STEP}}", failed_step.model_dump_json())
        .replace("{{OBSERVATION}}", observation.summary)
    )


def clean_reflection_response(raw_text: str):
    cleaned = (
        raw_text
        .replace("```json", "")
        .replace("```", "")
        .strip()
    )

    if not cleaned:
        raise ValueError("Reflector did not return JSON")

    return cleaned


def normalize_reflection_data(data: dict):
    normalized = data.copy()
    next_step = normalized.get("next_step")

    if next_step:
        normalized["next_step"] = normalize_intent_data(next_step)

    return normalized


def reflect_on_failure(
    query: str,
    goal: str,
    failed_step: PlanStep,
    observation: Observation
):
    prompt = build_reflection_prompt(
        query=query,
        goal=goal,
        failed_step=failed_step,
        observation=observation
    )

    response = get_client().models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    data = json.loads(clean_reflection_response(response.text))
    data = normalize_reflection_data(data)

    return Reflection(**data)
