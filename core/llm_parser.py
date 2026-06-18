from google import genai
from dotenv import load_dotenv
from core.schema import Intent
from core.normalizer import normalize_intent_data

import os
import json
from importlib.resources import files

load_dotenv()

client = None


def get_client():
    global client

    if client is None:
        client = genai.Client(
            api_key=os.getenv("GEMINI_API_KEY")
        )

    return client


def build_prompt(query: str):
    template = files("prompts").joinpath("parser_prompt.txt").read_text(
        encoding="utf-8"
    )
    return template.replace("{{USER_QUERY}}", query)


def parse_with_gemini(query: str):

    prompt = build_prompt(query)

    response = get_client().models.generate_content(
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
