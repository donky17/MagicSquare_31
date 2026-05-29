"""[TAG][GoldenMaster] Magic Square Solver golden master regression tests."""

from __future__ import annotations

import pytest

from boundary.models import FailureResult
from boundary.screen_boundary import ScreenBoundary
from control.solve import resolve
from golden_master_support import (
    ERROR_CONTRACT_ALIASES,
    GOLDEN_MASTER_CASES,
    GoldenMasterCase,
    assert_failure_error_contract,
    assert_golden_master,
    assert_section_matches_golden,
    assert_success_output_contract,
    build_golden_document,
    capture_scenario,
)

pytestmark = pytest.mark.golden_master


@pytest.fixture
def solver_boundary() -> ScreenBoundary:
    """Boundary wired to the real resolve port (API result serialization target)."""
    return ScreenBoundary(resolve=resolve)


class TestGoldenMasterMagicSquare:
    """[TAG][GoldenMaster] Approval-pattern regression for solver output contract."""

    def test_golden_master_document_matches_baseline(
        self,
        solver_boundary: ScreenBoundary,
        approve_golden: bool,
    ) -> None:
        """Full baseline compare: open(expected).read() vs actual document."""
        actual = build_golden_document(solver_boundary)
        assert_golden_master(actual, approve=approve_golden)

    @pytest.mark.parametrize(
        "case",
        GOLDEN_MASTER_CASES,
        ids=[case.test_id for case in GOLDEN_MASTER_CASES],
    )
    def test_golden_master_case(
        self,
        case: GoldenMasterCase,
        solver_boundary: ScreenBoundary,
        approve_golden: bool,
    ) -> None:
        """GM-TC-XX: API result serialization + section golden compare."""
        result = solver_boundary.submit(case.grid)
        actual_section = capture_scenario(case, solver_boundary)

        if not approve_golden:
            assert_section_matches_golden(
                actual_section,
                test_id=case.test_id,
            )

        if isinstance(result, FailureResult):
            assert case.contract_alias is not None
            assert_failure_error_contract(
                result,
                contract_alias=case.contract_alias,
            )
            return

        assert case.contract_alias is None
        if case.test_id == "GM-TC-01":
            assert_success_output_contract(
                case.grid,
                result,
                strategy="small_first",
            )
        elif case.test_id == "GM-TC-02":
            assert_success_output_contract(
                case.grid,
                result,
                strategy="reverse",
            )
        else:
            pytest.fail(f"Unexpected success for {case.test_id}")


class TestGoldenMasterContractAliases:
    """Document requirement aliases mapped to runtime Error Contract codes."""

    @pytest.mark.parametrize(
        ("alias", "runtime_code"),
        list(ERROR_CONTRACT_ALIASES.items()),
    )
    def test_error_contract_alias_mapping(
        self,
        alias: str,
        runtime_code: str,
    ) -> None:
        """GM requirement names resolve to DTO error codes."""
        assert alias != runtime_code
        assert runtime_code.isupper()
