from types import SimpleNamespace

import pytest
from pydantic import ValidationError

from core import reflection
from core.observation import Observation
from core.plan_schema import PlanStep
from core.reflection import Reflection


def fake_client(text):
    return SimpleNamespace(
        models=SimpleNamespace(
            generate_content=lambda model, contents: SimpleNamespace(text=text)
        )
    )


def failed_observation():
    return Observation(
        step_index=1,
        action="cat",
        command="cat README.md",
        success=False,
        returncode=1,
        stderr="No such file or directory\n",
        summary="Command failed with stderr: No such file or directory"
    )


def test_reflection_accepts_retry_with_next_step():
    result = Reflection(
        status="retry",
        reason="README 위치를 먼저 찾아야 한다",
        next_step={
            "action": "find_file",
            "target": "README.md"
        }
    )

    assert result.status == "retry"
    assert result.next_step.action == "find_file"


def test_reflection_rejects_unknown_status():
    with pytest.raises(ValidationError):
        Reflection(status="unknown", reason="invalid")


def test_build_reflection_prompt_includes_context():
    prompt = reflection.build_reflection_prompt(
        query="README 찾아서 보여줘",
        goal="README 파일을 찾아 출력한다",
        failed_step=PlanStep(action="cat", target="README.md"),
        observation=failed_observation(),
        session_context="1. find_file: Command succeeded with no output"
    )

    assert "{{USER_QUERY}}" not in prompt
    assert "README 찾아서 보여줘" in prompt
    assert "README 파일을 찾아 출력한다" in prompt
    assert "Command failed with stderr" in prompt
    assert "Session Memory" in prompt
    assert "1. find_file: Command succeeded with no output" in prompt
    assert "git_status" in prompt
    assert "git_log" in prompt
    assert "git_diff" in prompt
    assert "git_branch" in prompt
    assert "head" in prompt
    assert "tail" in prompt
    assert "wc" in prompt


def test_clean_reflection_response_strips_markdown_json_fence():
    cleaned = reflection.clean_reflection_response(
        '```json\n{"status": "stop", "reason": "done"}\n```'
    )

    assert cleaned == '{"status": "stop", "reason": "done"}'


def test_normalize_reflection_data_normalizes_next_step_action():
    data = {
        "status": "retry",
        "reason": "히스토리를 보여준다",
        "next_step": {
            "action": "view_history"
        }
    }

    normalized = reflection.normalize_reflection_data(data)

    assert normalized["next_step"]["action"] == "show_history"


def test_reflect_on_failure(monkeypatch):
    raw_reflection = """
    {
      "status": "retry",
      "reason": "README.md 경로를 먼저 찾아야 한다",
      "next_step": {
        "action": "find_file",
        "target": "README.md",
        "recursive": false,
        "reason": "README.md 위치를 찾는다"
      }
    }
    """

    monkeypatch.setattr(
        reflection,
        "get_client",
        lambda: fake_client(raw_reflection)
    )

    result = reflection.reflect_on_failure(
        query="README 찾아서 보여줘",
        goal="README 파일을 찾아 출력한다",
        failed_step=PlanStep(action="cat", target="README.md"),
        observation=failed_observation()
    )

    assert result.status == "retry"
    assert result.next_step.action == "find_file"
