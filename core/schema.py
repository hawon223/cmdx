from pydantic import BaseModel
from typing import Optional, Literal


class Intent(BaseModel):

    action: Literal[
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

    target: Optional[str] = None

    pattern: Optional[str] = None

    recursive: bool = False
