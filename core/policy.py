BLOCKED_PATTERNS = [

    "rm -rf /",

    "mkfs",

    ":(){ :|:& };:",

    "shutdown",

    "reboot"
]

def check_policy(command: str):

    for pattern in BLOCKED_PATTERNS:

        if pattern in command:

            return {
                "allowed": False,
                "reason": f"Blocked pattern detected: {pattern}"
            }

    return {
        "allowed": True,
        "reason": "Safe"
    }