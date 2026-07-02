from core.schema import Intent
from core.tools.base import (
    BaseTool,
    UNSUPPORTED_COMMAND,
    quote_value,
    quoted_target,
)


class ListFilesTool(BaseTool):
    action = "list_files"

    def build(self, intent: Intent, current_os: str):
        if current_os == "windows":
            return "dir"

        return "ls -al"


class FindFileTool(BaseTool):
    action = "find_file"

    def build(self, intent: Intent, current_os: str):
        target = intent.target

        if current_os == "windows":
            return f"dir /s {target}"

        return f'find . -name "{target}"'


class DeleteFilesTool(BaseTool):
    action = "delete_files"

    def build(self, intent: Intent, current_os: str):
        return "rm -rf *"


class ShowHistoryTool(BaseTool):
    action = "show_history"

    def build(self, intent: Intent, current_os: str):
        if current_os == "windows":
            return "type logs\\history.jsonl"

        return "cat logs/history.jsonl"


class PwdTool(BaseTool):
    action = "pwd"

    def build(self, intent: Intent, current_os: str):
        if current_os == "windows":
            return "cd"

        return "pwd"


class MkdirTool(BaseTool):
    action = "mkdir"

    def build(self, intent: Intent, current_os: str):
        target = quoted_target(intent)

        if not target:
            return UNSUPPORTED_COMMAND

        return f"mkdir {target}"


class TouchTool(BaseTool):
    action = "touch"

    def build(self, intent: Intent, current_os: str):
        target = quoted_target(intent)

        if not target:
            return UNSUPPORTED_COMMAND

        if current_os == "windows":
            return f"type nul > {target}"

        return f"touch {target}"


class CatTool(BaseTool):
    action = "cat"

    def build(self, intent: Intent, current_os: str):
        target = quoted_target(intent)

        if not target:
            return UNSUPPORTED_COMMAND

        if current_os == "windows":
            return f"type {target}"

        return f"cat {target}"


class GrepTool(BaseTool):
    action = "grep"

    def build(self, intent: Intent, current_os: str):
        target = quoted_target(intent)

        if not target or not intent.pattern:
            return UNSUPPORTED_COMMAND

        pattern = quote_value(intent.pattern)

        if current_os == "windows":
            return f"findstr {pattern} {target}"

        if intent.recursive:
            return f"grep -R {pattern} {target}"

        return f"grep {pattern} {target}"


class GitStatusTool(BaseTool):
    action = "git_status"

    def build(self, intent: Intent, current_os: str):
        return "git status --short"


class GitLogTool(BaseTool):
    action = "git_log"

    def build(self, intent: Intent, current_os: str):
        limit = "5"

        if intent.target and intent.target.isdigit():
            limit = intent.target

        return f"git log --oneline -{limit}"


class GitDiffTool(BaseTool):
    action = "git_diff"

    def build(self, intent: Intent, current_os: str):
        target = quoted_target(intent)

        if target:
            return f"git diff --stat -- {target}"

        return "git diff --stat"


class GitBranchTool(BaseTool):
    action = "git_branch"

    def build(self, intent: Intent, current_os: str):
        return "git branch --show-current"


def _line_limit(intent: Intent):
    if intent.pattern and intent.pattern.isdigit():
        return intent.pattern

    return "10"


class HeadTool(BaseTool):
    action = "head"

    def build(self, intent: Intent, current_os: str):
        target = quoted_target(intent)

        if not target:
            return UNSUPPORTED_COMMAND

        limit = _line_limit(intent)

        if current_os == "windows":
            return f"powershell -Command \"Get-Content {target} -TotalCount {limit}\""

        return f"head -n {limit} {target}"


class TailTool(BaseTool):
    action = "tail"

    def build(self, intent: Intent, current_os: str):
        target = quoted_target(intent)

        if not target:
            return UNSUPPORTED_COMMAND

        limit = _line_limit(intent)

        if current_os == "windows":
            return f"powershell -Command \"Get-Content {target} -Tail {limit}\""

        return f"tail -n {limit} {target}"


class WcTool(BaseTool):
    action = "wc"

    def build(self, intent: Intent, current_os: str):
        target = quoted_target(intent)

        if not target:
            return UNSUPPORTED_COMMAND

        if current_os == "windows":
            return f"powershell -Command \"(Get-Content {target}).Count\""

        return f"wc -l {target}"
