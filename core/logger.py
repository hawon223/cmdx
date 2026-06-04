from datetime import datetime
import json
import os

LOG_PATH = "logs/history.jsonl"


def log_command(
    query,
    intent,
    command,
    risk,
    result=None,
    log_path=LOG_PATH
):
    log_entry = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "query": query,
        "intent": intent.model_dump(),
        "command": command,
        "risk": risk,
    }

    if result:
        log_entry["result"] = {
            "success": result.get("success"),
            "returncode": result.get("returncode"),
            "stdout": result.get("stdout", ""),
            "stderr": result.get("stderr", ""),
            "error": result.get("error"),
            "execution_time": result.get("execution_time"),
        }

    log_dir = os.path.dirname(log_path)

    if log_dir:
        os.makedirs(log_dir, exist_ok=True)

    with open(
        log_path,
        "a",
        encoding="utf-8"
    ) as f:

        f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")

    return True


def read_history(limit=10, log_path=LOG_PATH):
    if not os.path.exists(log_path):
        return []

    with open(log_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    entries = []

    for line in lines[-limit:]:
        line = line.strip()

        if not line:
            continue

        entries.append(json.loads(line))

    return entries
