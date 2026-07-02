from pydantic import BaseModel, Field
from typing import Literal, Optional

PlanAction = Literal[
    "list_files",
    "find_file",
    "delete_files",
    "show_history",
    "pwd",
    "mkdir",
    "touch",
    "cat",
    "grep",
    "git_status",
    "git_log"
]


class PlanStep(BaseModel):
    action: PlanAction
    target: Optional[str] = None
    pattern: Optional[str] = None
    recursive: bool = False
    reason: Optional[str] = None


class Plan(BaseModel):
    goal: str
    steps: list[PlanStep] = Field(min_length=1, max_length=5)
