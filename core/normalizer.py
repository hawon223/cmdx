ACTION_MAPPINGS = {
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
