"""Resolve port implementation — boundary entry to domain solving."""

from __future__ import annotations

from entity.exceptions import DomainError
from entity.solver import solve as domain_solve


def resolve(grid: list[list[int]]) -> list[int]:
    """Run the two-blank solve use case for a validated 4×4 grid."""
    return domain_solve(grid)


__all__ = ["DomainError", "resolve"]
