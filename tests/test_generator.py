from core.generator import generate
from core.schema import Intent


def test_generate_list_files():

    intent = Intent(
        action="list_files",
        target="current_directory",
        recursive=False
    )

    command = generate(intent)

    assert command == "ls -al"


def test_generate_show_history():
    intent = Intent(
        action="show_history",
        target=None,
        recursive=False
    )

    command = generate(intent)

    assert command == "cat logs/history.log"
