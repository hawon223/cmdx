from google import genai
from dotenv import load_dotenv

import os
import json

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def parse_with_gemini(query: str):

    prompt = f"""
사용자의 요청을 JSON intent로 변환하세요.

반드시 JSON만 출력하세요.

예시:
{{
  "action": "list_files",
  "target": "current_directory",
  "recursive": false
}}

사용자 입력:
{query}
"""

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

    return json.loads(cleaned)