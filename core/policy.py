BLOCKED_PATTERNS = [

    "rm -rf /",

    "mkfs",

    ":(){ :|:& };:",

    "shutdown",

    "reboot",

    "dd if=",

    "dd of=",

    "curl | bash",

    "curl | sh",

    "wget | bash",

    "wget | sh"
]

def check_policy(command: str):
    normalized_command = command.lower()

    for pattern in BLOCKED_PATTERNS:

        if pattern in normalized_command:

            return {
                "allowed": False,
                "reason": f"Blocked pattern detected: {pattern}"
            }

    if _pipes_remote_script_to_shell(normalized_command):
        return {
            "allowed": False,
            "reason": "Blocked pattern detected: remote script piped to shell"
        }

    return {
        "allowed": True,
        "reason": "Safe"
    }


def _pipes_remote_script_to_shell(command: str):
    downloads_script = "curl" in command or "wget" in command
    pipes_to_shell = "| bash" in command or "| sh" in command

    return downloads_script and pipes_to_shell
