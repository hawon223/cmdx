import pytest
from pydantic import ValidationError

from core.plan_schema import Plan


def test_plan_requires_at_least_one_step():
    with pytest.raises(ValidationError):
        Plan(goal="empty plan", steps=[])


def test_plan_accepts_supported_steps():
    plan = Plan(
        goal="README 파일을 찾아 출력한다",
        steps=[
            {
                "action": "find_file",
                "target": "README.md",
                "reason": "README 파일 위치를 찾는다"
            },
            {
                "action": "cat",
                "target": "README.md",
                "reason": "README 내용을 출력한다"
            }
        ]
    )

    assert plan.goal == "README 파일을 찾아 출력한다"
    assert len(plan.steps) == 2
    assert plan.steps[0].action == "find_file"


def test_plan_accepts_git_steps():
    plan = Plan(
        goal="git 상태와 변경 요약을 확인한다",
        steps=[
            {
                "action": "git_status"
            },
            {
                "action": "git_log",
                "target": "5"
            },
            {
                "action": "git_branch"
            },
            {
                "action": "git_diff"
            }
        ]
    )

    assert plan.steps[0].action == "git_status"
    assert plan.steps[1].action == "git_log"
    assert plan.steps[2].action == "git_branch"
    assert plan.steps[3].action == "git_diff"


def test_plan_accepts_file_inspection_steps():
    plan = Plan(
        goal="README 앞뒤와 줄 수를 확인한다",
        steps=[
            {
                "action": "head",
                "target": "README.md",
                "pattern": "10"
            },
            {
                "action": "tail",
                "target": "README.md",
                "pattern": "10"
            },
            {
                "action": "wc",
                "target": "README.md"
            }
        ]
    )

    assert plan.steps[0].action == "head"
    assert plan.steps[1].action == "tail"
    assert plan.steps[2].action == "wc"


def test_plan_rejects_unknown_action():
    with pytest.raises(ValidationError):
        Plan(
            goal="unknown",
            steps=[
                {
                    "action": "unknown_action"
                }
            ]
        )
