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
}


def normalize_action(action: str):
    normalized_action = action.strip().lower()

    return ACTION_MAPPINGS.get(normalized_action, normalized_action)


def normalize_intent_data(data: dict):
    normalized = data.copy()

    if "action" in normalized:
        normalized["action"] = normalize_action(normalized["action"])

    return normalized
