"""Screen boundary — parses input and delegates to domain resolve port."""

from __future__ import annotations

from collections.abc import Callable

from boundary.models import FailureResult

ResolvePort = Callable[[list[list[int]]], list[int]]


class ScreenBoundary:
    """Boundary entry for grid submission (AC-FR-01-01 RED: not implemented)."""

    def __init__(self, resolve: ResolvePort) -> None:
        self._resolve = resolve

    def submit(self, grid: list[list[int]] | None) -> FailureResult | list[int]:
        """Validate grid contract and return failure or delegate to resolve."""
        raise NotImplementedError("AC-FR-01-01: input validation not implemented")
