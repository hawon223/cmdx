from typing import Literal, Optional

from pydantic import BaseModel, Field

from core.executor import execute
from core.generator import generate
from core.observation import Observation, observe_result
from core.plan_schema import PlanStep
from core.planner import parse_plan_with_gemini
from core.policy import check_policy
from core.reflection import Reflection, reflect_on_failure
from core.risk_analyzer import analyze
from core.schema import Intent
from core.session_memory import SessionMemory

BLOCKING_RISKS = {"HIGH", "CRITICAL"}


class AgentStepResult(BaseModel):
    step_index: int
    action: str
    command: str
    risk: str
    risk_reason: str
    policy_allowed: bool
    policy_reason: str
    status: Literal["dry_run", "executed", "blocked", "failed"]
    observation: Optional[Observation] = None
    reflection: Optional[Reflection] = None


class AgentRunResult(BaseModel):
    goal: str
    dry_run: bool
    completed: bool
    steps: list[AgentStepResult] = Field(default_factory=list)
    memory: SessionMemory = Field(default_factory=SessionMemory)
    stopped_reason: Optional[str] = None


def plan_step_to_intent(step: PlanStep):
    return Intent(
        action=step.action,
        target=step.target,
        pattern=step.pattern,
        recursive=step.recursive
    )


def run_agent(query: str, dry_run: bool = True, max_steps: int = 3):
    plan = parse_plan_with_gemini(query)
    result = AgentRunResult(
        goal=plan.goal,
        dry_run=dry_run,
        completed=True
    )

    steps = plan.steps[:max_steps]

    for index, step in enumerate(steps, start=1):
        command = generate(plan_step_to_intent(step))
        risk_result = analyze(command)
        policy_result = check_policy(command)

        if not policy_result["allowed"]:
            result.steps.append(
                build_step_result(
                    index=index,
                    step=step,
                    command=command,
                    risk_result=risk_result,
                    policy_result=policy_result,
                    status="blocked"
                )
            )
            result.completed = False
            result.stopped_reason = policy_result["reason"]
            break

        if risk_result["risk"] in BLOCKING_RISKS:
            result.steps.append(
                build_step_result(
                    index=index,
                    step=step,
                    command=command,
                    risk_result=risk_result,
                    policy_result=policy_result,
                    status="blocked"
                )
            )
            result.completed = False
            result.stopped_reason = risk_result["reason"]
            break

        if dry_run:
            result.steps.append(
                build_step_result(
                    index=index,
                    step=step,
                    command=command,
                    risk_result=risk_result,
                    policy_result=policy_result,
                    status="dry_run"
                )
            )
            continue

        execution_result = execute(command)
        observation = observe_result(
            step_index=index,
            step=step,
            command=command,
            result=execution_result
        )
        result.memory.add_observation(observation)

        status = "executed" if observation.success else "failed"
        result.steps.append(
            build_step_result(
                index=index,
                step=step,
                command=command,
                risk_result=risk_result,
                policy_result=policy_result,
                status=status,
                observation=observation
            )
        )

        if not observation.success:
            reflection = safe_reflect_on_failure(
                query=query,
                goal=plan.goal,
                failed_step=step,
                observation=observation,
                session_context=result.memory.to_prompt_context()
            )
            result.steps[-1].reflection = reflection
            result.completed = False
            result.stopped_reason = observation.summary
            break

    if result.completed and len(plan.steps) > max_steps:
        result.completed = False
        result.stopped_reason = f"Stopped after max_steps={max_steps}"

    return result


def safe_reflect_on_failure(
    query: str,
    goal: str,
    failed_step: PlanStep,
    observation: Observation,
    session_context: str = ""
):
    try:
        return reflect_on_failure(
            query=query,
            goal=goal,
            failed_step=failed_step,
            observation=observation,
            session_context=session_context
        )
    except Exception as e:
        return Reflection(
            status="stop",
            reason=f"Reflection failed: {e}",
            next_step=None
        )


def build_step_result(
    index: int,
    step: PlanStep,
    command: str,
    risk_result: dict,
    policy_result: dict,
    status: str,
    observation: Optional[Observation] = None
):
    return AgentStepResult(
        step_index=index,
        action=step.action,
        command=command,
        risk=risk_result["risk"],
        risk_reason=risk_result["reason"],
        policy_allowed=policy_result["allowed"],
        policy_reason=policy_result["reason"],
        status=status,
        observation=observation
    )
