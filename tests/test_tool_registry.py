from core.tools import TOOL_REGISTRY, get_tool


def test_tool_registry_contains_supported_actions():
    assert set(TOOL_REGISTRY) == {
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
        "git_log",
        "git_diff",
        "git_branch",
        "head",
        "tail",
        "wc",
    }


def test_get_tool_returns_registered_tool():
    tool = get_tool("list_files")

    assert tool is not None
    assert tool.action == "list_files"


def test_get_tool_returns_none_for_unknown_action():
    assert get_tool("unknown_action") is None
