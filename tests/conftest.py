"""Shared pytest fixtures for MagicSquare_xx."""

from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import MagicMock

import pytest

# tests/boundary/ 와 동명 패키지 충돌 방지: src를 항상 최우선
_SRC = Path(__file__).resolve().parents[1] / "src"
_src_str = str(_SRC)
while _src_str in sys.path:
    sys.path.remove(_src_str)
sys.path.insert(0, _src_str)

from boundary.screen_boundary import ScreenBoundary


@pytest.fixture
def mock_resolve() -> MagicMock:
    """Domain resolve port mock (spy target for isolation tests)."""
    return MagicMock(return_value=[1, 1, 2, 2, 2, 3])


@pytest.fixture
def boundary(mock_resolve: MagicMock) -> ScreenBoundary:
    """ScreenBoundary with injected resolve mock."""
    return ScreenBoundary(resolve=mock_resolve)


# --- Report/09 grid fixtures (GREEN 전 placeholder — 주석만) ---
# G0: [[16, 2, 3, 13], [5, 11, 10, 8], [9, 7, 6, 12], [4, 14, 15, 1]]
# G1: [[16, 2, 3, 13], [5, 0, 11, 8], [9, 6, 0, 12], [4, 15, 14, 1]]
# G2: TBD (D-SOL-02 / SC-DOM-SOL-001)
# G3: PLACEHOLDER unsolvable partial grid
