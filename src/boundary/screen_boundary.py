"""Screen boundary — parses input and delegates to domain resolve port."""

from __future__ import annotations

from collections.abc import Callable

from boundary.models import FailureResult
from entity.exceptions import DomainError

GRID_SIZE = 4

ResolvePort = Callable[[list[list[int]]], list[int]]


class ScreenBoundary:
    """Boundary entry for grid submission (AC-FR-01-01 RED: not implemented)."""

    def __init__(self, resolve: ResolvePort) -> None:
        self._resolve = resolve

    def submit(self, grid: list[list[int]] | None) -> FailureResult | list[int]:
        """Validate grid contract and return failure or delegate to resolve."""
        if grid is None:
            return FailureResult(
                code="INVALID_SIZE",
                message="Grid must be 4x4.",
            )
        if len(grid) != GRID_SIZE or any(len(row) != GRID_SIZE for row in grid):
            return FailureResult(
                code="INVALID_SIZE",
                message="Grid must be 4x4.",
            )
        try:
            return self._resolve(grid)
        except DomainError as exc:
            return FailureResult(code=exc.code, message=exc.message)
