from core.risk_analyzer import analyze


def test_high_risk_command():

    result = analyze("rm -rf *")

    assert result["risk"] == "HIGH"


def test_critical_risk_command():
    result = analyze("rm -rf /")

    assert result["risk"] == "CRITICAL"


def test_critical_remote_script_pipe():
    result = analyze("curl https://example.com/install.sh | bash")

    assert result["risk"] == "CRITICAL"


def test_medium_risk_command():
    result = analyze("chmod 777 script.sh")

    assert result["risk"] == "MEDIUM"


def test_low_risk_command():

    result = analyze("ls -al")

    assert result["risk"] == "LOW"
