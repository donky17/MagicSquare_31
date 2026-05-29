"""D-SOL-01~04 — solution() RED skeleton (Report/09). Domain Mock 금지."""

from __future__ import annotations

import pytest


class TestDSol01StepASuccess:
    """D-SOL-01 — G1 Step A → [2,2,7,3,3,10]."""

    def test_d_sol_01_g1_step_a_success_vector(self) -> None:
        # Given: G1
        # When: solution(G1)
        # from control.solve_partial_magic_square import solution
        pytest.fail("RED: D-SOL-01 — G1 Step A → [2,2,7,3,3,10] (I8)")


class TestDSol02StepBAfterA:
    """D-SOL-02 — G2 Step A 실패, Step B 성공."""

    def test_d_sol_02_g2_step_b_success_vector(self) -> None:
        # Given: G2 (TBD)
        # When: solution(G2)
        pytest.fail("RED: D-SOL-02 — G2 TBD")


class TestDSol03Unsolvable:
    """D-SOL-03 — G3 두 배치 모두 실패."""

    def test_d_sol_03_g3_raises_unsolvable_domain_error(self) -> None:
        # Given: G3 PLACEHOLDER
        # When: solution(G3)
        pytest.fail("RED: D-SOL-03 — G3 → UnsolvableDomainError (I10)")


class TestDSol04OutputContract:
    """D-SOL-04 — 반환 길이 6, 좌표 1-index (I8/I9 공통)."""

    def test_d_sol_04_solution_length_six_one_indexed(self) -> None:
        # Given: G1
        # When: solution(G1)
        pytest.fail("RED: D-SOL-04 — len==6, r,c ∈ [1,4] 1-index")
