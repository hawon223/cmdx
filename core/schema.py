from pydantic import BaseModel
from typing import Optional, Literal


class Intent(BaseModel):

    action: Literal[
        "list_files",
        "find_file",
        "delete_all"
    ]

    target: Optional[str] = None

    recursive: bool = False