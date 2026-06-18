import subprocess

from core.executor import execute


class FakeCompletedProcess:
    def __init__(self, returncode=0, stdout="", stderr=""):
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr


def test_execute_success(monkeypatch):
    def fake_run(command, shell, text, capture_output):
        assert command == "ls -al"
        assert shell is True
        assert text is True
        assert capture_output is True
        return FakeCompletedProcess(returncode=0, stdout="README.md\n")

    monkeypatch.setattr(subprocess, "run", fake_run)

    result = execute("ls -al")

    assert result["success"] is True
    assert result["returncode"] == 0
    assert result["stdout"] == "README.md\n"
    assert result["stderr"] == ""
    assert result["error"] is None
    assert isinstance(result["execution_time"], float)


def test_execute_failed_command(monkeypatch):
    def fake_run(command, shell, text, capture_output):
        return FakeCompletedProcess(
            returncode=1,
            stdout="",
            stderr="No such file or directory\n"
        )

    monkeypatch.setattr(subprocess, "run", fake_run)

    result = execute("cat missing.txt")

    assert result["success"] is False
    assert result["returncode"] == 1
    assert result["stdout"] == ""
    assert result["stderr"] == "No such file or directory\n"
    assert result["error"] is None


def test_execute_handles_subprocess_exception(monkeypatch):
    def fake_run(command, shell, text, capture_output):
        raise OSError("subprocess unavailable")

    monkeypatch.setattr(subprocess, "run", fake_run)

    result = execute("ls -al")

    assert result["success"] is False
    assert result["returncode"] is None
    assert result["stdout"] == ""
    assert result["stderr"] == ""
    assert result["error"] == "subprocess unavailable"
