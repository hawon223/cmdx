import os
from types import SimpleNamespace

os.environ.setdefault("GEMINI_API_KEY", "test-api-key")

from core import llm_parser


def fake_client(text):
    return SimpleNamespace(
        models=SimpleNamespace(
            generate_content=lambda model, contents: SimpleNamespace(text=text)
        )
    )


def test_build_prompt_includes_query_and_few_shot_examples():
    prompt = llm_parser.build_prompt("히스토리 보여줘")

    assert "{{USER_QUERY}}" not in prompt
    assert "히스토리 보여줘" in prompt
    assert "view_history, display_history, history -> show_history" in prompt
    assert '"action": "show_history"' in prompt
    assert "git_status" in prompt
    assert "git_log" in prompt


def test_parse_with_gemini_strips_markdown_json_fence(monkeypatch):
    def fake_generate_content(model, contents):
        assert model == "gemini-2.5-flash"
        assert "파일 목록 보여줘" in contents
        assert "마크다운 코드블록, 설명 문장, 주석은 출력하지 마세요." in contents
        return SimpleNamespace(
            text='```json\n{"action": "list_files", "recursive": false}\n```'
        )

    monkeypatch.setattr(
        llm_parser,
        "get_client",
        lambda: SimpleNamespace(
            models=SimpleNamespace(generate_content=fake_generate_content)
        )
    )

    intent = llm_parser.parse_with_gemini("파일 목록 보여줘")

    assert intent.action == "list_files"
    assert intent.recursive is False


def test_parse_with_gemini_normalizes_action_alias(monkeypatch):
    monkeypatch.setattr(
        llm_parser,
        "get_client",
        lambda: fake_client('{"action": "view_history"}')
    )

    intent = llm_parser.parse_with_gemini("히스토리 보여줘")

    assert intent.action == "show_history"


def test_parse_with_gemini_accepts_git_action(monkeypatch):
    monkeypatch.setattr(
        llm_parser,
        "get_client",
        lambda: fake_client('{"action": "git_status"}')
    )

    intent = llm_parser.parse_with_gemini("git 상태 보여줘")

    assert intent.action == "git_status"
