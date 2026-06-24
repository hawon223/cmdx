import json

from core.logger import log_command, read_history
from core.schema import Intent


def test_log_creation(tmp_path):
    log_path = tmp_path / "history.jsonl"

    intent = Intent(
        action="list_files",
        target="current_directory",
        recursive=False
    )

    result = log_command(
        query="파일 목록 보여줘",
        intent=intent,
        command="ls -al",
        risk="LOW",
        result={
            "success": True,
            "returncode": 0,
            "stdout": "README.md\n",
            "stderr": "",
            "execution_time": 0.01,
            "error": None
        },
        log_path=str(log_path)
    )

    assert result is True

    log_entry = json.loads(log_path.read_text(encoding="utf-8").strip())

    assert log_entry["query"] == "파일 목록 보여줘"
    assert log_entry["intent"]["action"] == "list_files"
    assert log_entry["command"] == "ls -al"
    assert log_entry["risk"] == "LOW"
    assert log_entry["result"]["success"] is True
    assert log_entry["result"]["stdout"] == "README.md\n"


def test_read_history_returns_recent_entries(tmp_path):
    log_path = tmp_path / "history.jsonl"

    intent = Intent(action="list_files", target="current_directory")

    log_command("first", intent, "ls -al", "LOW", log_path=str(log_path))
    log_command("second", intent, "pwd", "LOW", log_path=str(log_path))

    entries = read_history(limit=1, log_path=str(log_path))

    assert len(entries) == 1
    assert entries[0]["query"] == "second"


def test_log_command_accepts_fallback_intent_dict(tmp_path):
    log_path = tmp_path / "history.jsonl"

    result = log_command(
        query="git 상태 보여줘",
        intent={
            "action": "ai_fallback",
            "reason": "Invalid action: git_status"
        },
        command="git status",
        risk="LOW",
        log_path=str(log_path)
    )

    assert result is True

    log_entry = json.loads(log_path.read_text(encoding="utf-8").strip())

    assert log_entry["intent"]["action"] == "ai_fallback"
    assert log_entry["command"] == "git status"
