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


def test_generate_pwd():
    intent = Intent(
        action="pwd",
        target=None,
        recursive=False
    )

    command = generate(intent)

    assert command == "pwd"


def test_generate_mkdir():
    intent = Intent(
        action="mkdir",
        target="reports",
        recursive=False
    )

    command = generate(intent)

    assert command == "mkdir reports"


def test_generate_touch():
    intent = Intent(
        action="touch",
        target="notes.txt",
        recursive=False
    )

    command = generate(intent)

    assert command == "touch notes.txt"


def test_generate_cat():
    intent = Intent(
        action="cat",
        target="README.md",
        recursive=False
    )

    command = generate(intent)

    assert command == "cat README.md"


def test_generate_grep():
    intent = Intent(
        action="grep",
        target="README.md",
        pattern="Natural Language",
        recursive=False
    )

    command = generate(intent)

    assert command == "grep 'Natural Language' README.md"


def test_generate_recursive_grep():
    intent = Intent(
        action="grep",
        target=".",
        pattern="TODO",
        recursive=True
    )

    command = generate(intent)

    assert command == "grep -R TODO ."
