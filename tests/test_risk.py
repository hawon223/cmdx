from core.risk_analyzer import analyze


def test_high_risk_command():

    result = analyze("rm -rf *")

    assert result["risk"] == "HIGH"


def test_low_risk_command():

    result = analyze("ls -al")

    assert result["risk"] == "LOW"