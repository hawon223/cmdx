from core.tools.command_tools import (
    CatTool,
    DeleteFilesTool,
    FindFileTool,
    GitBranchTool,
    GitDiffTool,
    GitLogTool,
    GitStatusTool,
    GrepTool,
    HeadTool,
    ListFilesTool,
    MkdirTool,
    PwdTool,
    ShowHistoryTool,
    TailTool,
    TouchTool,
    WcTool,
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
    GitDiffTool(),
    GitBranchTool(),
    HeadTool(),
    TailTool(),
    WcTool(),
]

TOOL_REGISTRY = {tool.action: tool for tool in TOOLS}


def get_tool(action: str):
    return TOOL_REGISTRY.get(action)
