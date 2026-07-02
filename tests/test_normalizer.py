from core.normalizer import normalize_action, normalize_intent_data


def test_normalize_history_alias():
    assert normalize_action("view_history") == "show_history"


def test_normalize_action_strips_spaces_and_lowercases():
    assert normalize_action(" View_History ") == "show_history"


def test_normalize_file_alias():
    assert normalize_action("search_file") == "find_file"


def test_normalize_pwd_alias():
    assert normalize_action("show_current_directory") == "pwd"


def test_normalize_grep_alias():
    assert normalize_action("search_text") == "grep"


def test_normalize_git_status_alias():
    assert normalize_action("show_git_status") == "git_status"


def test_normalize_git_log_alias():
    assert normalize_action("commit_history") == "git_log"


def test_normalize_git_diff_alias():
    assert normalize_action("git_changes") == "git_diff"


def test_normalize_git_branch_alias():
    assert normalize_action("current_branch") == "git_branch"


def test_normalize_head_alias():
    assert normalize_action("first_lines") == "head"


def test_normalize_tail_alias():
    assert normalize_action("last_lines") == "tail"


def test_normalize_wc_alias():
    assert normalize_action("line_count") == "wc"


def test_normalize_intent_data_keeps_unknown_action():
    result = normalize_intent_data({"action": "unknown_action"})

    assert result["action"] == "unknown_action"
