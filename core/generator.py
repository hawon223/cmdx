def generate(intent: dict):

    action = intent["action"]

    if action == "list_files":
        return "ls -al"

    if action == "find_file":
        target = intent["target"]
        return f'find . -name "{target}"'

    return "지원되지 않는 명령"