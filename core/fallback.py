from importlib.resources import files

from core.llm_parser import get_client

FALLBACK_PROMPT_NAME = "command_fallback_prompt.txt"


def build_fallback_prompt(query: str):
    template = files("prompts").joinpath(FALLBACK_PROMPT_NAME).read_text(
        encoding="utf-8"
    )
    return template.replace("{{USER_QUERY}}", query)


def clean_command_response(raw_text: str):
    cleaned = (
        raw_text
        .replace("```bash", "")
        .replace("```sh", "")
        .replace("```shell", "")
        .replace("```", "")
        .strip()
    )

    lines = [
        line.removeprefix("$").strip()
        for line in cleaned.splitlines()
        if line.strip()
    ]

    if not lines:
        raise ValueError("AI fallback did not return a command")

    if len(lines) > 1:
        raise ValueError("AI fallback must return exactly one command")

    return lines[0]


def suggest_command_with_gemini(query: str):
    prompt = build_fallback_prompt(query)

    response = get_client().models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return clean_command_response(response.text)
