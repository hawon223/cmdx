from types import SimpleNamespace

import pytest

from core import fallback


def fake_client(text):
    return SimpleNamespace(
        models=SimpleNamespace(
            generate_content=lambda model, contents: SimpleNamespace(text=text)
        )
    )


def test_build_fallback_prompt_includes_query():
    prompt = fallback.build_fallback_prompt("git 상태 보여줘")

    assert "{{USER_QUERY}}" not in prompt
    assert "git 상태 보여줘" in prompt
    assert "반드시 명령어 한 줄만 출력하세요." in prompt


def test_clean_command_response_strips_markdown_fence():
    command = fallback.clean_command_response("```bash\ngit status\n```")

    assert command == "git status"


def test_clean_command_response_rejects_multiple_commands():
    with pytest.raises(ValueError, match="exactly one command"):
        fallback.clean_command_response("git status\ngit log")


def test_suggest_command_with_gemini(monkeypatch):
    monkeypatch.setattr(
        fallback,
        "get_client",
        lambda: fake_client("git status")
    )

    command = fallback.suggest_command_with_gemini("git 상태 보여줘")

    assert command == "git status"
