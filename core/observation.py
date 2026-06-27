from typing import Optional

from pydantic import BaseModel

from core.plan_schema import PlanStep


class Observation(BaseModel):
    step_index: int
    action: str
    command: str
    success: bool
    returncode: Optional[int] = None
    stdout: str = ""
    stderr: str = ""
    error: Optional[str] = None
    summary: str


def observe_result(step_index: int, step: PlanStep, command: str, result: dict):
    stdout = result.get("stdout", "")
    stderr = result.get("stderr", "")
    error = result.get("error")
    success = result.get("success", False)

    return Observation(
        step_index=step_index,
        action=step.action,
        command=command,
        success=success,
        returncode=result.get("returncode"),
        stdout=stdout,
        stderr=stderr,
        error=error,
        summary=build_summary(success, stdout, stderr, error)
    )


def build_summary(success: bool, stdout: str, stderr: str, error: Optional[str]):
    if success:
        if stdout.strip():
            return f"Command succeeded with output: {truncate(stdout.strip())}"

        return "Command succeeded with no output"

    if stderr.strip():
        return f"Command failed with stderr: {truncate(stderr.strip())}"

    if error:
        return f"Command failed with error: {truncate(error)}"

    return "Command failed without output"


def truncate(text: str, limit: int = 200):
    if len(text) <= limit:
        return text

    return text[:limit].rstrip() + "..."
