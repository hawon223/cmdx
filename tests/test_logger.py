from core.logger import log_command
from core.schema import Intent


def test_log_creation():

    intent = Intent(
        action="list_files",
        target="current_directory",
        recursive=False
    )

    result = log_command(
        query="파일 목록 보여줘",
        intent=intent,
        command="ls -al",
        risk="LOW"
    )

    assert result is True