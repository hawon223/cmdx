from core.os_adapter import get_os
from core.schema import Intent
from shlex import quote


def _quote(value: str):
    return quote(value)


def _target_or_unsupported(intent: Intent):
    if not intent.target:
        return None

    return _quote(intent.target)


def generate(intent: Intent):

    current_os = get_os()

    action = intent.action

    if action == "list_files":

        if current_os == "windows":
            return "dir"

        return "ls -al"

    if action == "find_file":

        target = intent.target

        if current_os == "windows":
            return f'dir /s {target}'

        return f'find . -name "{target}"'
    if action == "delete_files":
        return "rm -rf *"

    if action == "show_history":
        if current_os == "windows":
            return "type logs\\history.jsonl"

        return "cat logs/history.jsonl"

    if action == "pwd":
        if current_os == "windows":
            return "cd"

        return "pwd"

    if action == "mkdir":
        target = _target_or_unsupported(intent)

        if not target:
            return "지원되지 않는 명령"

        return f"mkdir {target}"

    if action == "touch":
        target = _target_or_unsupported(intent)

        if not target:
            return "지원되지 않는 명령"

        if current_os == "windows":
            return f"type nul > {target}"

        return f"touch {target}"

    if action == "cat":
        target = _target_or_unsupported(intent)

        if not target:
            return "지원되지 않는 명령"

        if current_os == "windows":
            return f"type {target}"

        return f"cat {target}"

    if action == "grep":
        target = _target_or_unsupported(intent)

        if not target or not intent.pattern:
            return "지원되지 않는 명령"

        pattern = _quote(intent.pattern)

        if current_os == "windows":
            return f"findstr {pattern} {target}"

        if intent.recursive:
            return f"grep -R {pattern} {target}"

        return f"grep {pattern} {target}"

    return "지원되지 않는 명령"
