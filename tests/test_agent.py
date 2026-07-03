from core import agent
from core.agent import plan_step_to_intent, run_agent, safe_reflect_on_failure
from core.observation import Observation
from core.plan_schema import Plan, PlanStep
from core.reflection import Reflection


def test_plan_step_to_intent():
    step = PlanStep(
        action="grep",
        target="README.md",
        pattern="install",
        recursive=False
    )

    intent = plan_step_to_intent(step)

    assert intent.action == "grep"
    assert intent.target == "README.md"
    assert intent.pattern == "install"
    assert intent.recursive is False


def test_run_agent_dry_run(monkeypatch):
    plan = Plan(
        goal="README 파일을 찾아 출력한다",
        steps=[
            PlanStep(action="find_file", target="README.md"),
            PlanStep(action="cat", target="README.md"),
        ]
    )

    monkeypatch.setattr(
        agent,
        "parse_plan_with_gemini",
        lambda query: plan
    )

    result = run_agent(
        query="README 찾아서 보여줘",
        dry_run=True,
        max_steps=3
    )

    assert result.goal == "README 파일을 찾아 출력한다"
    assert result.completed is True
    assert len(result.steps) == 2
    assert result.steps[0].status == "dry_run"
    assert result.steps[0].command == 'find . -name "README.md"'
    assert result.steps[1].command == "cat README.md"
    assert result.steps[0].observation is None
    assert result.memory.observations == []


def test_run_agent_blocks_high_risk_step(monkeypatch):
    plan = Plan(
        goal="파일을 삭제한다",
        steps=[
            PlanStep(action="delete_files"),
        ]
    )

    monkeypatch.setattr(
        agent,
        "parse_plan_with_gemini",
        lambda query: plan
    )

    result = run_agent(
        query="파일 삭제해줘",
        dry_run=True,
        max_steps=3
    )

    assert result.completed is False
    assert len(result.steps) == 1
    assert result.steps[0].status == "blocked"
    assert result.steps[0].risk == "HIGH"
    assert result.stopped_reason is not None


def test_run_agent_execute_adds_observation(monkeypatch):
    plan = Plan(
        goal="현재 위치를 확인한다",
        steps=[
            PlanStep(action="pwd"),
        ]
    )

    monkeypatch.setattr(
        agent,
        "parse_plan_with_gemini",
        lambda query: plan
    )
    monkeypatch.setattr(
        agent,
        "execute",
        lambda command: {
            "success": True,
            "returncode": 0,
            "stdout": "/tmp/project\n",
            "stderr": "",
            "error": None,
        }
    )

    result = run_agent(
        query="내 위치 알려줘",
        dry_run=False,
        max_steps=3
    )

    assert result.completed is True
    assert result.steps[0].status == "executed"
    assert result.steps[0].observation is not None
    assert result.steps[0].observation.summary == (
        "Command succeeded with output: /tmp/project"
    )
    assert result.memory.to_prompt_context() == (
        "1. pwd: Command succeeded with output: /tmp/project"
    )


def test_run_agent_stops_on_execution_failure(monkeypatch):
    plan = Plan(
        goal="없는 파일을 출력한다",
        steps=[
            PlanStep(action="cat", target="missing.txt"),
            PlanStep(action="pwd"),
        ]
    )

    monkeypatch.setattr(
        agent,
        "parse_plan_with_gemini",
        lambda query: plan
    )
    monkeypatch.setattr(
        agent,
        "execute",
        lambda command: {
            "success": False,
            "returncode": 1,
            "stdout": "",
            "stderr": "No such file or directory\n",
            "error": None,
        }
    )
    monkeypatch.setattr(
        agent,
        "safe_reflect_on_failure",
        lambda query, goal, failed_step, observation, session_context: Reflection(
            status="retry",
            reason=f"missing.txt 경로를 다시 찾아야 한다: {session_context}",
            next_step=PlanStep(action="find_file", target="missing.txt")
        )
    )

    result = run_agent(
        query="없는 파일 보여줘",
        dry_run=False,
        max_steps=3
    )

    assert result.completed is False
    assert len(result.steps) == 1
    assert result.steps[0].status == "failed"
    assert result.steps[0].reflection is not None
    assert result.steps[0].reflection.status == "retry"
    assert "No such file or directory" in result.steps[0].reflection.reason
    assert result.steps[0].reflection.next_step.action == "find_file"
    assert result.stopped_reason == (
        "Command failed with stderr: No such file or directory"
    )


def test_run_agent_respects_max_steps(monkeypatch):
    plan = Plan(
        goal="여러 작업을 한다",
        steps=[
            PlanStep(action="pwd"),
            PlanStep(action="list_files"),
        ]
    )

    monkeypatch.setattr(
        agent,
        "parse_plan_with_gemini",
        lambda query: plan
    )

    result = run_agent(
        query="여러 작업 해줘",
        dry_run=True,
        max_steps=1
    )

    assert result.completed is False
    assert len(result.steps) == 1
    assert result.stopped_reason == "Stopped after max_steps=1"


def test_safe_reflect_on_failure_returns_stop_when_reflection_fails(monkeypatch):
    def raise_error(query, goal, failed_step, observation, session_context):
        raise ValueError("invalid reflection")

    monkeypatch.setattr(agent, "reflect_on_failure", raise_error)

    result = safe_reflect_on_failure(
        query="없는 파일 보여줘",
        goal="없는 파일을 출력한다",
        failed_step=PlanStep(action="cat", target="missing.txt"),
        observation=Observation(
            step_index=1,
            action="cat",
            command="cat missing.txt",
            success=False,
            returncode=1,
            stderr="No such file or directory\n",
            summary="Command failed with stderr: No such file or directory"
        )
    )

    assert result.status == "stop"
    assert result.reason == "Reflection failed: invalid reflection"
    assert result.next_step is None
