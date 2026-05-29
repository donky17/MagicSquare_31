from __future__ import annotations

from datetime import datetime, timezone
from uuid import UUID

import pytest

from entity.user import User


def test_user_defaults_create_valid_entity() -> None:
    # Arrange
    username = "alice_01"

    # Act
    user = User(username=username)

    # Assert
    assert isinstance(user.id, UUID)
    assert user.username == username
    assert user.created_at.tzinfo is not None
    assert user.created_at.utcoffset() is not None


@pytest.mark.parametrize(
    ("username", "expected_error"),
    [
        ("ab", "3..32"),
        ("a" * 33, "3..32"),
        ("a b", "[a-zA-Z0-9_]"),
        ("-bad-", "[a-zA-Z0-9_]"),
        (" ok", "whitespace"),
        ("ok ", "whitespace"),
        ("", "3..32"),
    ],
)
def test_user_rejects_invalid_username(username: str, expected_error: str) -> None:
    # Arrange
    # Act / Assert
    with pytest.raises(ValueError) as exc:
        User(username=username)
    assert expected_error in str(exc.value)


def test_user_requires_timezone_aware_created_at() -> None:
    # Arrange
    naive = datetime(2026, 1, 1, 0, 0, 0)

    # Act / Assert
    with pytest.raises(ValueError) as exc:
        User(username="alice_01", created_at=naive)
    assert "timezone-aware" in str(exc.value)


def test_user_rename_returns_new_instance_same_identity() -> None:
    # Arrange
    user = User(username="alice_01")

    # Act
    renamed = user.rename("alice_02")

    # Assert
    assert renamed is not user
    assert renamed.id == user.id
    assert renamed.created_at == user.created_at
    assert renamed.username == "alice_02"

