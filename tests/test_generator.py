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

    assert command == "cat logs/history.jsonl"


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


def test_generate_git_status():
    intent = Intent(
        action="git_status",
        target=None,
        recursive=False
    )

    command = generate(intent)

    assert command == "git status --short"


def test_generate_git_log_default_limit():
    intent = Intent(
        action="git_log",
        target=None,
        recursive=False
    )

    command = generate(intent)

    assert command == "git log --oneline -5"


def test_generate_git_log_custom_limit():
    intent = Intent(
        action="git_log",
        target="3",
        recursive=False
    )

    command = generate(intent)

    assert command == "git log --oneline -3"


def test_generate_git_log_ignores_non_numeric_limit():
    intent = Intent(
        action="git_log",
        target="main",
        recursive=False
    )

    command = generate(intent)

    assert command == "git log --oneline -5"


def test_generate_git_diff():
    intent = Intent(
        action="git_diff",
        target=None,
        recursive=False
    )

    command = generate(intent)

    assert command == "git diff --stat"


def test_generate_git_diff_target():
    intent = Intent(
        action="git_diff",
        target="README.md",
        recursive=False
    )

    command = generate(intent)

    assert command == "git diff --stat -- README.md"


def test_generate_git_branch():
    intent = Intent(
        action="git_branch",
        target=None,
        recursive=False
    )

    command = generate(intent)

    assert command == "git branch --show-current"


def test_generate_head_default_limit():
    intent = Intent(
        action="head",
        target="README.md",
        recursive=False
    )

    command = generate(intent)

    assert command == "head -n 10 README.md"


def test_generate_head_custom_limit():
    intent = Intent(
        action="head",
        target="README.md",
        pattern="20",
        recursive=False
    )

    command = generate(intent)

    assert command == "head -n 20 README.md"


def test_generate_tail_default_limit():
    intent = Intent(
        action="tail",
        target="logs/history.jsonl",
        recursive=False
    )

    command = generate(intent)

    assert command == "tail -n 10 logs/history.jsonl"


def test_generate_tail_ignores_non_numeric_limit():
    intent = Intent(
        action="tail",
        target="README.md",
        pattern="latest",
        recursive=False
    )

    command = generate(intent)

    assert command == "tail -n 10 README.md"


def test_generate_wc():
    intent = Intent(
        action="wc",
        target="README.md",
        recursive=False
    )

    command = generate(intent)

    assert command == "wc -l README.md"


def test_generate_head_requires_target():
    intent = Intent(
        action="head",
        target=None,
        recursive=False
    )

    command = generate(intent)

    assert command == "지원되지 않는 명령"
