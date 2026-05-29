"""Domain exceptions with stable error codes (Error Contract)."""

from __future__ import annotations


class DomainError(Exception):
    """Raised when domain validation or solving fails."""

    def __init__(self, code: str, message: str) -> None:
        self.code = code
        self.message = message
        super().__init__(message)
