from core.os_adapter import get_os
from core.schema import Intent


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
    if action == "delete_all":
        return "rm -rf *"

    return "지원되지 않는 명령"
