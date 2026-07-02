ACTION_MAPPINGS = {
    "current_directory": "pwd",
    "print_working_directory": "pwd",
    "show_current_directory": "pwd",
    "show_location": "pwd",
    "where_am_i": "pwd",
    "make_directory": "mkdir",
    "create_directory": "mkdir",
    "new_directory": "mkdir",
    "create_file": "touch",
    "new_file": "touch",
    "read_file": "cat",
    "show_file": "cat",
    "display_file": "cat",
    "search_text": "grep",
    "find_text": "grep",
    "search_in_file": "grep",
    "view_history": "show_history",
    "display_history": "show_history",
    "history": "show_history",
    "read_logs": "show_history",
    "show_logs": "show_history",
    "remove_files": "delete_files",
    "delete_file": "delete_files",
    "search_file": "find_file",
    "search_files": "find_file",
    "find_files": "find_file",
    "list": "list_files",
    "list_directory": "list_files",
    "git_status": "git_status",
    "show_git_status": "git_status",
    "git_state": "git_status",
    "repository_status": "git_status",
    "git_log": "git_log",
    "show_git_log": "git_log",
    "git_history": "git_log",
    "commit_history": "git_log",
    "show_head": "head",
    "file_head": "head",
    "first_lines": "head",
    "show_tail": "tail",
    "file_tail": "tail",
    "last_lines": "tail",
    "line_count": "wc",
    "count_lines": "wc",
    "word_count": "wc",
    "git_diff": "git_diff",
    "show_git_diff": "git_diff",
    "git_changes": "git_diff",
    "repository_diff": "git_diff",
    "git_branch": "git_branch",
    "show_git_branch": "git_branch",
    "current_branch": "git_branch",
    "current_git_branch": "git_branch",
}


def normalize_action(action: str):
    normalized_action = action.strip().lower()

    return ACTION_MAPPINGS.get(normalized_action, normalized_action)


def normalize_intent_data(data: dict):
    normalized = data.copy()

    if "action" in normalized:
        normalized["action"] = normalize_action(normalized["action"])

    return normalized
