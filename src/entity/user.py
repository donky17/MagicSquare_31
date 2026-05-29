from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from re import compile as re_compile
from typing import Any
from uuid import UUID, uuid4

_USERNAME_RE = re_compile(r"^[a-zA-Z0-9_]{3,32}$")


@dataclass(frozen=True, slots=True)
class User:
    """Domain entity representing a user in the system.

    This entity is intentionally pure (no I/O) and enforces local invariants:
    - `id` is a UUID.
    - `username` is 3..32 chars and matches `[a-zA-Z0-9_]+`.
    - `created_at` is timezone-aware (UTC recommended).

    Attributes:
        id: Unique identifier of the user.
        username: User's handle (ASCII letters/digits/underscore).
        created_at: Creation timestamp (timezone-aware).
    """

    username: str
    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def __post_init__(self) -> None:
        if not isinstance(self.id, UUID):
            raise TypeError("id must be a UUID")

        if not isinstance(self.username, str):
            raise TypeError("username must be a str")

        username = self.username.strip()
        if username != self.username:
            raise ValueError("username must not contain leading/trailing whitespace")

        if not _USERNAME_RE.fullmatch(self.username):
            raise ValueError("username must be 3..32 chars of [a-zA-Z0-9_]")

        if not isinstance(self.created_at, datetime):
            raise TypeError("created_at must be a datetime")

        if self.created_at.tzinfo is None or self.created_at.utcoffset() is None:
            raise ValueError("created_at must be timezone-aware")

    def rename(self, new_username: str) -> User:
        """Return a new User instance with updated username.

        Args:
            new_username: New username to set.

        Returns:
            A new `User` with the same `id` and `created_at`, but a new `username`.
        """

        return User(id=self.id, username=new_username, created_at=self.created_at)

    def to_dict(self) -> dict[str, Any]:
        """Serialize this entity to a plain dict.

        Returns:
            A JSON-serializable dict representation.
        """

        return {
            "id": str(self.id),
            "username": self.username,
            "created_at": self.created_at.isoformat(),
        }
