def analyze(command: str):

    high_risk_patterns = [
        "rm -rf",
        "mkfs",
        "shutdown",
        "reboot",
        "sudo rm"
    ]

    medium_risk_patterns = [
        "curl",
        "wget",
        "chmod 777"
    ]

    for pattern in high_risk_patterns:

        if pattern in command:
            return {
                "risk": "HIGH",
                "reason": f"위험한 명령어 패턴 감지: {pattern}"
            }

    for pattern in medium_risk_patterns:

        if pattern in command:
            return {
                "risk": "MEDIUM",
                "reason": f"주의가 필요한 명령어 패턴 감지: {pattern}"
            }

    return {
        "risk": "LOW",
        "reason": "안전한 명령어"
    }