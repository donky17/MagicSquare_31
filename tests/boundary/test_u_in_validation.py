"""U-IN-04~08 — Boundary input validation RED skeleton (Report/09).

U-IN-01~03은 Report/08 Full RED — 본 파일에 포함하지 않음.
"""

from __future__ import annotations

import pytest


class TestUIn04EmptyCount:
    """U-IN-04 — 빈칸(0) 0개 → E002."""

    def test_u_in_04_zero_empty_cells_returns_e002(self) -> None:
        # Given: 4×4, 0개 빈칸 (예: G0 완전 격자)
        # When: InputValidator.validate(matrix)
        # from boundary.input_validator import InputValidator
        pytest.fail("RED: U-IN-04 — 빈칸 0개 → E002, Domain execute 0회")


class TestUIn05EmptyCount:
    """U-IN-05 — 빈칸(0) 3개 → E002."""

    def test_u_in_05_three_empty_cells_returns_e002(self) -> None:
        # Given: 4×4, 0이 3칸
        # When: InputValidator.validate(matrix)
        pytest.fail("RED: U-IN-05 — 빈칸 3개 → E002, Domain execute 0회")


class TestUIn06ValueRange:
    """U-IN-06 — 셀 값 -1 → E004."""

    def test_u_in_06_cell_minus_one_returns_e004(self) -> None:
        # Given: 4×4, 한 셀 -1, 빈칸 2개·나머지 계약 준수
        # When: InputValidator.validate(matrix)
        pytest.fail("RED: U-IN-06 — 값 -1 → E004, Domain execute 0회")


class TestUIn07ValueRange:
    """U-IN-07 — 셀 값 17 → E004."""

    def test_u_in_07_cell_seventeen_returns_e004(self) -> None:
        # Given: 4×4, 한 셀 17, 빈칸 2개
        # When: InputValidator.validate(matrix)
        pytest.fail("RED: U-IN-07 — 값 17 → E004, Domain execute 0회")


class TestUIn08Duplicate:
    """U-IN-08 — 0 제외 중복 → E005."""

    def test_u_in_08_nonzero_duplicate_returns_e005(self) -> None:
        # Given: 4×4, 0 제외 동일 값 2칸, 빈칸 2개
        # When: InputValidator.validate(matrix)
        pytest.fail("RED: U-IN-08 — non-zero 중복 → E005, Domain execute 0회")
