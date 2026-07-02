from core.tools.command_tools import (
    CatTool,
    DeleteFilesTool,
    FindFileTool,
    GitLogTool,
    GitStatusTool,
    GrepTool,
    ListFilesTool,
    MkdirTool,
    PwdTool,
    ShowHistoryTool,
    TouchTool,
)

TOOLS = [
    ListFilesTool(),
    FindFileTool(),
    DeleteFilesTool(),
    ShowHistoryTool(),
    PwdTool(),
    MkdirTool(),
    TouchTool(),
    CatTool(),
    GrepTool(),
    GitStatusTool(),
    GitLogTool(),
]

TOOL_REGISTRY = {tool.action: tool for tool in TOOLS}


def get_tool(action: str):
    return TOOL_REGISTRY.get(action)
