from core.observation import build_summary, observe_result, truncate
from core.plan_schema import PlanStep


def test_observe_result_success_with_stdout():
    step = PlanStep(action="cat", target="README.md")
    result = {
        "success": True,
        "returncode": 0,
        "stdout": "Hello\n",
        "stderr": "",
        "error": None
    }

    observation = observe_result(
        step_index=1,
        step=step,
        command="cat README.md",
        result=result
    )

    assert observation.step_index == 1
    assert observation.action == "cat"
    assert observation.command == "cat README.md"
    assert observation.success is True
    assert observation.returncode == 0
    assert observation.stdout == "Hello\n"
    assert observation.summary == "Command succeeded with output: Hello"


def test_observe_result_failed_with_stderr():
    step = PlanStep(action="cat", target="missing.txt")
    result = {
        "success": False,
        "returncode": 1,
        "stdout": "",
        "stderr": "No such file or directory\n",
        "error": None
    }

    observation = observe_result(
        step_index=2,
        step=step,
        command="cat missing.txt",
        result=result
    )

    assert observation.success is False
    assert observation.returncode == 1
    assert observation.stderr == "No such file or directory\n"
    assert observation.summary == (
        "Command failed with stderr: No such file or directory"
    )


def test_build_summary_success_without_output():
    summary = build_summary(
        success=True,
        stdout="",
        stderr="",
        error=None
    )

    assert summary == "Command succeeded with no output"


def test_build_summary_failed_with_error():
    summary = build_summary(
        success=False,
        stdout="",
        stderr="",
        error="subprocess unavailable"
    )

    assert summary == "Command failed with error: subprocess unavailable"


def test_truncate_long_text():
    text = "a" * 205

    assert truncate(text, limit=10) == "aaaaaaaaaa..."
