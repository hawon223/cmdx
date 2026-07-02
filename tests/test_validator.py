import pytest

from core.schema import Intent
from core.validator import validate_intent


def test_validate_intent_accepts_allowed_action():
    intent = Intent(action="list_files")

    assert validate_intent(intent) is True


def test_validate_intent_accepts_git_action():
    intent = Intent(action="git_status")

    assert validate_intent(intent) is True


def test_validate_intent_accepts_git_diff_action():
    intent = Intent(action="git_diff")

    assert validate_intent(intent) is True


def test_validate_intent_accepts_file_inspection_action():
    intent = Intent(action="head", target="README.md")

    assert validate_intent(intent) is True


def test_validate_intent_rejects_unknown_action():
    intent = Intent.model_construct(action="unknown_action")

    with pytest.raises(ValueError, match="Invalid action: unknown_action"):
        validate_intent(intent)
