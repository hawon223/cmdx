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
