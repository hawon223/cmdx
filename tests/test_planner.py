from types import SimpleNamespace

from core import planner


def fake_client(text):
    return SimpleNamespace(
        models=SimpleNamespace(
            generate_content=lambda model, contents: SimpleNamespace(text=text)
        )
    )


def test_build_planner_prompt_includes_query_and_schema():
    prompt = planner.build_planner_prompt("README 찾아서 보여줘")

    assert "{{USER_QUERY}}" not in prompt
    assert "README 찾아서 보여줘" in prompt
    assert "shell command를 직접 만들지 마세요." in prompt
    assert '"steps"' in prompt
    assert "git_status" in prompt
    assert "git_log" in prompt
    assert "git_diff" in prompt
    assert "git_branch" in prompt
    assert "head" in prompt
    assert "tail" in prompt
    assert "wc" in prompt


def test_clean_plan_response_strips_markdown_json_fence():
    cleaned = planner.clean_plan_response('```json\n{"goal": "test"}\n```')

    assert cleaned == '{"goal": "test"}'


def test_normalize_plan_data_normalizes_step_actions():
    data = {
        "goal": "히스토리를 보여준다",
        "steps": [
            {
                "action": "view_history"
            }
        ]
    }

    normalized = planner.normalize_plan_data(data)

    assert normalized["steps"][0]["action"] == "show_history"


def test_parse_plan_with_gemini(monkeypatch):
    raw_plan = """
    {
      "goal": "README 파일을 찾아 내용을 출력한다",
      "steps": [
        {
          "action": "find_file",
          "target": "README.md",
          "recursive": false,
          "reason": "README 파일 위치를 찾는다"
        },
        {
          "action": "cat",
          "target": "README.md",
          "recursive": false,
          "reason": "README 내용을 출력한다"
        }
      ]
    }
    """

    monkeypatch.setattr(
        planner,
        "get_client",
        lambda: fake_client(raw_plan)
    )

    plan = planner.parse_plan_with_gemini("README 찾아서 보여줘")

    assert plan.goal == "README 파일을 찾아 내용을 출력한다"
    assert len(plan.steps) == 2
    assert plan.steps[0].action == "find_file"
    assert plan.steps[1].action == "cat"


def test_parse_plan_with_gemini_accepts_git_steps(monkeypatch):
    raw_plan = """
    {
      "goal": "git 상태와 변경 요약을 확인한다",
      "steps": [
        {
          "action": "git_status",
          "recursive": false,
          "reason": "working tree 상태를 확인한다"
        },
        {
          "action": "git_log",
          "target": "5",
          "recursive": false,
          "reason": "최근 커밋을 확인한다"
        },
        {
          "action": "git_branch",
          "recursive": false,
          "reason": "현재 브랜치를 확인한다"
        },
        {
          "action": "git_diff",
          "recursive": false,
          "reason": "변경 요약을 확인한다"
        }
      ]
    }
    """

    monkeypatch.setattr(
        planner,
        "get_client",
        lambda: fake_client(raw_plan)
    )

    plan = planner.parse_plan_with_gemini("git 상태와 최근 커밋 보여줘")

    assert plan.steps[0].action == "git_status"
    assert plan.steps[1].action == "git_log"
    assert plan.steps[1].target == "5"
    assert plan.steps[2].action == "git_branch"
    assert plan.steps[3].action == "git_diff"


def test_parse_plan_with_gemini_accepts_file_inspection_steps(monkeypatch):
    raw_plan = """
    {
      "goal": "README 앞부분과 줄 수를 확인한다",
      "steps": [
        {
          "action": "head",
          "target": "README.md",
          "pattern": "10",
          "recursive": false,
          "reason": "README 앞부분을 확인한다"
        },
        {
          "action": "wc",
          "target": "README.md",
          "recursive": false,
          "reason": "README 줄 수를 확인한다"
        }
      ]
    }
    """

    monkeypatch.setattr(
        planner,
        "get_client",
        lambda: fake_client(raw_plan)
    )

    plan = planner.parse_plan_with_gemini("README 앞부분과 줄 수 보여줘")

    assert plan.steps[0].action == "head"
    assert plan.steps[0].pattern == "10"
    assert plan.steps[1].action == "wc"
