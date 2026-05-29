"""U-OUT-01~03 — Boundary output contract RED skeleton (Report/09)."""

from __future__ import annotations

import pytest

from boundary.screen_boundary import ScreenBoundary


class TestUOut01ResultLength:
    """U-OUT-01 — 성공 반환 배열 길이 6."""

    def test_u_out_01_valid_grid_returns_length_six(self) -> None:
        # Given: G1 (계약 만족 partial grid)
        # When: UIBoundary.solve(G1)  — ScreenBoundary.submit + mock execute → [2,2,7,3,3,10]
        # mock: execute = MagicMock(return_value=[2, 2, 7, 3, 3, 10])
        pytest.fail("RED: U-OUT-01 — 성공 시 int[6] 길이 6")


class TestUOut02OneIndexedCoords:
    """U-OUT-02 — 좌표 r,c ∈ [1,4] (1-index)."""

    def test_u_out_02_success_coords_are_one_indexed(self) -> None:
        # Given: G1; mock execute → [2, 2, 7, 3, 3, 10]
        # When: UIBoundary.solve(G1)
        pytest.fail("RED: U-OUT-02 — r1,c1,r2,c2 ∈ [1,4], 0·5 금지")


class TestUOut03SuccessNotFailureEnvelope:
    """U-OUT-03 — 성공 시 Failure envelope 아님."""

    def test_u_out_03_valid_grid_returns_list_not_failure(self) -> None:
        # Given: G1; mock execute 성공
        # When: UIBoundary.solve(G1)
        pytest.fail("RED: U-OUT-03 — 성공 시 list[int], FailureResult 아님")
