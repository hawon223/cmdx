from core.normalizer import normalize_action, normalize_intent_data


def test_normalize_history_alias():
    assert normalize_action("view_history") == "show_history"


def test_normalize_action_strips_spaces_and_lowercases():
    assert normalize_action(" View_History ") == "show_history"


def test_normalize_file_alias():
    assert normalize_action("search_file") == "find_file"


def test_normalize_intent_data_keeps_unknown_action():
    result = normalize_intent_data({"action": "unknown_action"})

    assert result["action"] == "unknown_action"
