def analyze(command: str):
    normalized_command = command.lower()

    critical_risk_patterns = [
        "rm -rf /",
        "mkfs",
        "shutdown",
        "reboot",
        ":(){ :|:& };:",
        "dd if=",
        "dd of="
    ]

    high_risk_patterns = [
        "rm -rf",
        "sudo rm",
        "sudo",
        "> /etc/"
    ]

    medium_risk_patterns = [
        "curl",
        "wget",
        "chmod 777",
        "chmod -r 777",
        "mv ",
        "cp "
    ]

    for pattern in critical_risk_patterns:

        if pattern in normalized_command:
            return {
                "risk": "CRITICAL",
                "reason": f"치명적인 명령어 패턴 감지: {pattern}"
            }

    if _pipes_remote_script_to_shell(normalized_command):
        return {
            "risk": "CRITICAL",
            "reason": "원격 스크립트를 shell로 바로 실행하는 패턴 감지"
        }

    for pattern in high_risk_patterns:

        if pattern in normalized_command:
            return {
                "risk": "HIGH",
                "reason": f"위험한 명령어 패턴 감지: {pattern}"
            }

    for pattern in medium_risk_patterns:

        if pattern in normalized_command:
            return {
                "risk": "MEDIUM",
                "reason": f"주의가 필요한 명령어 패턴 감지: {pattern}"
            }

    return {
        "risk": "LOW",
        "reason": "안전한 명령어"
    }


def _pipes_remote_script_to_shell(command: str):
    downloads_script = "curl" in command or "wget" in command
    pipes_to_shell = "| bash" in command or "| sh" in command

    return downloads_script and pipes_to_shell
