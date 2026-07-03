from core.observation import Observation
from core.session_memory import SessionMemory


def make_observation(step_index: int, action: str, summary: str):
    return Observation(
        step_index=step_index,
        action=action,
        command=action,
        success=True,
        returncode=0,
        summary=summary
    )


def test_session_memory_adds_observation():
    memory = SessionMemory()
    observation = make_observation(1, "pwd", "Command succeeded with output: /tmp")

    memory.add_observation(observation)

    assert memory.observations == [observation]


def test_session_memory_returns_recent_summaries():
    memory = SessionMemory()

    for index in range(1, 7):
        memory.add_observation(
            make_observation(index, "pwd", f"summary {index}")
        )

    summaries = memory.recent_summaries(limit=2)

    assert summaries == [
        "5. pwd: summary 5",
        "6. pwd: summary 6",
    ]


def test_session_memory_prompt_context_without_observations():
    memory = SessionMemory()

    assert memory.to_prompt_context() == "No previous observations."


def test_session_memory_prompt_context_with_observations():
    memory = SessionMemory()
    memory.add_observation(
        make_observation(1, "pwd", "Command succeeded with output: /tmp")
    )

    assert memory.to_prompt_context() == (
        "1. pwd: Command succeeded with output: /tmp"
    )
