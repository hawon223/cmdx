from abc import ABC, abstractmethod
from shlex import quote

from core.schema import Intent

UNSUPPORTED_COMMAND = "지원되지 않는 명령"


def quote_value(value: str):
    return quote(value)


def quoted_target(intent: Intent):
    if not intent.target:
        return None

    return quote_value(intent.target)


class BaseTool(ABC):
    action: str

    @abstractmethod
    def build(self, intent: Intent, current_os: str) -> str:
        pass
