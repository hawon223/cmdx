from core.policy import check_policy


def test_blocked_command():

    result = check_policy("rm -rf /")

    assert result["allowed"] is False


def test_safe_command():

    result = check_policy("ls -al")

    assert result["allowed"] is True