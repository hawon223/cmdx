from core.schema import Intent

ALLOWED_ACTIONS = [
    "list_files",
    "find_file",
    "delete_files",
    "show_history"
]


def validate_intent(intent: Intent):

    if intent.action not in ALLOWED_ACTIONS:
        raise ValueError(
            f"Invalid action: {intent.action}"
        )

    return True
