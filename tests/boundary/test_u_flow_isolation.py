"""U-FLOW-02 — invalid 입력 시 Domain execute 0회 (Report/09 확장)."""

from __future__ import annotations

import pytest

from boundary.screen_boundary import ScreenBoundary


class TestUFlow02DomainIsolation:
    """U-FLOW-02 — SolvePartialMagicSquare.execute mock/spy call_count == 0."""

    def test_u_flow_02_null_grid_execute_never_called(self) -> None:
        # Given: matrix = null
        # When: UIBoundary.solve(matrix)  — submit(grid=None)
        # mock/spy: execute.call_count == 0
        pytest.fail("RED: U-FLOW-02 — null → execute 0회")

    def test_u_flow_02_invalid_empty_count_execute_never_called(self) -> None:
        # Given: 빈칸 3개 (U-IN-05 동형 invalid)
        # When: UIBoundary.solve(matrix)
        # mock/spy: execute.call_count == 0
        pytest.fail("RED: U-FLOW-02 — E002 위반 → execute 0회")

    def test_u_flow_02_invalid_duplicate_execute_never_called(self) -> None:
        # Given: non-zero 중복 (U-IN-08 동형 invalid)
        # When: UIBoundary.solve(matrix)
        # mock/spy: execute.call_count == 0
        pytest.fail("RED: U-FLOW-02 — E005 위반 → execute 0회")
