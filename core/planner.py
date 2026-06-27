import json
from importlib.resources import files

from core.llm_parser import get_client
from core.normalizer import normalize_intent_data
from core.plan_schema import Plan

PLANNER_PROMPT_NAME = "planner_prompt.txt"


def build_planner_prompt(query: str):
    template = files("prompts").joinpath(PLANNER_PROMPT_NAME).read_text(
        encoding="utf-8"
    )
    return template.replace("{{USER_QUERY}}", query)


def clean_plan_response(raw_text: str):
    cleaned = (
        raw_text
        .replace("```json", "")
        .replace("```", "")
        .strip()
    )

    if not cleaned:
        raise ValueError("Planner did not return JSON")

    return cleaned


def normalize_plan_data(data: dict):
    normalized = data.copy()
    steps = normalized.get("steps", [])

    normalized["steps"] = [
        normalize_intent_data(step)
        for step in steps
    ]

    return normalized


def parse_plan_with_gemini(query: str):
    prompt = build_planner_prompt(query)

    response = get_client().models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    data = json.loads(clean_plan_response(response.text))
    data = normalize_plan_data(data)

    return Plan(**data)
