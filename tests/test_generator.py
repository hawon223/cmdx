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