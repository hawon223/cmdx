from pydantic import BaseModel
from typing import Optional, Literal


class Intent(BaseModel):

    action: Literal[
        "list_files",
        "find_file",
        "delete_files",
        "show_history"
    ]

    target: Optional[str] = None

    recursive: bool = False
