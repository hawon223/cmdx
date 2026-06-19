from core.os_adapter import get_os
from core.schema import Intent
from core.tools import get_tool
from core.tools.base import UNSUPPORTED_COMMAND


def generate(intent: Intent):

    current_os = get_os()
    tool = get_tool(intent.action)

    if not tool:
        return UNSUPPORTED_COMMAND

    return tool.build(intent, current_os)
