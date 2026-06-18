from google import genai
from dotenv import load_dotenv
from core.schema import Intent
from core.normalizer import normalize_intent_data

import os
import json
from pathlib import Path

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

PROMPT_PATH = Path(__file__).resolve().parent.parent / "prompts" / "parser_prompt.txt"


def build_prompt(query: str):
    template = PROMPT_PATH.read_text(encoding="utf-8")
    return template.replace("{{USER_QUERY}}", query)


def parse_with_gemini(query: str):

    prompt = build_prompt(query)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    raw_text = response.text



    cleaned = (
        raw_text
        .replace("```json", "")
        .replace("```", "")
        .strip()
    )
    
    data = json.loads(cleaned)
    data = normalize_intent_data(data)

    intent = Intent(**data)

    return intent
