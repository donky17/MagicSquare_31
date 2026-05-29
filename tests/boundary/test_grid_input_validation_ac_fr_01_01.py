"""AC-FR-01-01 boundary input validation — RED phase tests.

AC-FR-01-01, PRD §8.1 INVALID_SIZE — grid=None → code INVALID_SIZE, message Grid must be 4x4.
"""

from __future__ import annotations

import ast
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from boundary.models import FailureResult
from boundary.screen_boundary import ScreenBoundary

# PRD §8.1 / Error Contract golden strings (AC-FR-01-01)
EXPECTED_CODE = "INVALID_SIZE"
EXPECTED_MESSAGE = "Grid must be 4x4."

# AC-FR-01-01 scope: only None, [], [[]]*4, 3×4 — no 4×3, 5×5, valid 4×4
FORBIDDEN_TEST_NAME_FRAGMENTS = (
    "ac_fr_01_02",
    "ac_fr_01_03",
    "ac_fr_01_04",
    "ac_fr_01_05",
    "fr_02",
    "fr_03",
    "fr_04",
    "fr_05",
    "4x4_valid",
    "valid_grid",
    "empty_count",
    "duplicate",
    "no_solution",
)


class TestNormalFailureReturn:
    """AC-FR-01-01, PRD §8.1 INVALID_SIZE — grid=None 정상 실패 반환."""

    def test_grid_none_returns_invalid_size_code(
        self, boundary: ScreenBoundary, mock_resolve: MagicMock
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — failure code contract."""
        # Given
        grid = None

        # When
        result = boundary.submit(grid)

        # Then
        assert result.code == EXPECTED_CODE  # AC-FR-01-01
        mock_resolve.assert_not_called()

    def test_grid_none_returns_golden_message(
        self, boundary: ScreenBoundary, mock_resolve: MagicMock
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — failure message contract."""
        # Given
        grid = None

        # When
        result = boundary.submit(grid)

        # Then
        assert result.message == EXPECTED_MESSAGE  # AC-FR-01-01
        mock_resolve.assert_not_called()

    def test_grid_none_returns_failure_result_type(
        self, boundary: ScreenBoundary, mock_resolve: MagicMock
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — typed failure structure."""
        # Given
        grid = None

        # When
        result = boundary.submit(grid)

        # Then
        assert isinstance(result, FailureResult)  # AC-FR-01-01
        mock_resolve.assert_not_called()

    def test_grid_none_does_not_return_success_list(
        self, boundary: ScreenBoundary, mock_resolve: MagicMock
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — Happy Path of Failure (not int[6])."""
        # Given
        grid = None

        # When
        result = boundary.submit(grid)

        # Then
        assert not isinstance(result, list)  # AC-FR-01-01
        mock_resolve.assert_not_called()

    def test_grid_none_failure_has_both_code_and_message_fields(
        self, boundary: ScreenBoundary, mock_resolve: MagicMock
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — Error Contract field pair."""
        # Given
        grid = None

        # When
        result = boundary.submit(grid)

        # Then
        assert result.code == EXPECTED_CODE  # AC-FR-01-01
        assert result.message == EXPECTED_MESSAGE
        mock_resolve.assert_not_called()


class TestBoundaryValues:
    """AC-FR-01-01, PRD §8.1 INVALID_SIZE — 형식/차원 경계값 실패 반환."""

    def test_grid_empty_list_returns_invalid_size_code(
        self, boundary: ScreenBoundary, mock_resolve: MagicMock
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — empty list (0 rows)."""
        # Given
        grid: list[list[int]] = []

        # When
        result = boundary.submit(grid)

        # Then
        assert result.code == EXPECTED_CODE  # AC-FR-01-01
        mock_resolve.assert_not_called()

    def test_grid_jagged_four_empty_rows_returns_invalid_size(
        self, boundary: ScreenBoundary, mock_resolve: MagicMock
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — [[]]*4 jagged rows."""
        # Given
        grid = [[]] * 4

        # When
        result = boundary.submit(grid)

        # Then
        assert result.code == EXPECTED_CODE  # AC-FR-01-01
        mock_resolve.assert_not_called()

    def test_grid_3x4_returns_invalid_size_code(
        self, boundary: ScreenBoundary, mock_resolve: MagicMock
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — row count mismatch (3×4)."""
        # Given
        grid = [[0] * 4 for _ in range(3)]

        # When
        result = boundary.submit(grid)

        # Then
        assert result.code == EXPECTED_CODE  # AC-FR-01-01
        mock_resolve.assert_not_called()

    def test_grid_empty_list_returns_failure_result_type(
        self, boundary: ScreenBoundary, mock_resolve: MagicMock
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — [] typed failure."""
        # Given
        grid: list[list[int]] = []

        # When
        result = boundary.submit(grid)

        # Then
        assert isinstance(result, FailureResult)  # AC-FR-01-01
        mock_resolve.assert_not_called()

    def test_grid_jagged_four_empty_rows_message_golden(
        self, boundary: ScreenBoundary, mock_resolve: MagicMock
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — jagged message contract."""
        # Given
        grid = [[]] * 4

        # When
        result = boundary.submit(grid)

        # Then
        assert result.message == EXPECTED_MESSAGE  # AC-FR-01-01
        mock_resolve.assert_not_called()


class TestDomainIsolation:
    """AC-FR-01-01, PRD §8.1 INVALID_SIZE — resolve() 0회 호출 격리."""

    def test_grid_none_resolve_call_count_zero(
        self, boundary: ScreenBoundary, mock_resolve: MagicMock
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — mock call_count."""
        # Given
        grid = None

        # When
        boundary.submit(grid)

        # Then
        assert mock_resolve.call_count == 0  # AC-FR-01-01

    def test_grid_none_resolve_assert_not_called(
        self, boundary: ScreenBoundary, mock_resolve: MagicMock
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — assert_not_called."""
        # Given
        grid = None

        # When
        boundary.submit(grid)

        # Then
        mock_resolve.assert_not_called()  # AC-FR-01-01

    def test_grid_empty_list_resolve_not_called(
        self, boundary: ScreenBoundary, mock_resolve: MagicMock
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — [] isolation."""
        # Given
        grid: list[list[int]] = []

        # When
        boundary.submit(grid)

        # Then
        mock_resolve.assert_not_called()  # AC-FR-01-01

    def test_grid_jagged_resolve_not_called(
        self, boundary: ScreenBoundary, mock_resolve: MagicMock
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — [[]]*4 isolation."""
        # Given
        grid = [[]] * 4

        # When
        boundary.submit(grid)

        # Then
        mock_resolve.assert_not_called()  # AC-FR-01-01

    def test_grid_3x4_resolve_call_count_zero(
        self, boundary: ScreenBoundary, mock_resolve: MagicMock
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — 3×4 isolation."""
        # Given
        grid = [[0] * 4 for _ in range(3)]

        # When
        boundary.submit(grid)

        # Then
        assert mock_resolve.call_count == 0  # AC-FR-01-01


class TestMessageIdentity:
    """AC-FR-01-01, PRD §8.1 INVALID_SIZE — message 문자 단위 동일성."""

    def test_grid_none_message_exact_prd_8_1(
        self, boundary: ScreenBoundary
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — None golden string."""
        # Given
        grid = None
        expected = "Grid must be 4x4."

        # When
        result = boundary.submit(grid)

        # Then
        assert result.message == expected  # AC-FR-01-01
        assert len(result.message) == len(expected)

    def test_grid_empty_list_message_exact_prd_8_1(
        self, boundary: ScreenBoundary
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — [] golden string."""
        # Given
        grid: list[list[int]] = []

        # When
        result = boundary.submit(grid)

        # Then
        assert result.message == EXPECTED_MESSAGE  # AC-FR-01-01

    def test_grid_jagged_message_character_by_character(
        self, boundary: ScreenBoundary
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — jagged char-by-char."""
        # Given
        grid = [[]] * 4

        # When
        result = boundary.submit(grid)

        # Then
        assert list(result.message) == list(EXPECTED_MESSAGE)  # AC-FR-01-01

    def test_grid_3x4_message_no_extra_whitespace(
        self, boundary: ScreenBoundary
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — no leading/trailing space."""
        # Given
        grid = [[0] * 4 for _ in range(3)]

        # When
        result = boundary.submit(grid)

        # Then
        assert result.message == EXPECTED_MESSAGE  # AC-FR-01-01
        assert result.message == result.message.strip()

    def test_grid_none_message_identity_operators(
        self, boundary: ScreenBoundary
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — == and is not alternate string."""
        # Given
        grid = None

        # When
        result = boundary.submit(grid)

        # Then
        assert result.message == "Grid must be 4x4."  # AC-FR-01-01
        assert result.message is not "".join(["Grid must be 4x4", "."])


class TestScopeRestriction:
    """AC-FR-01-01 — AC-FR-01-02~05, FR-02~05 케이스 본 파일 미포함."""

    def test_module_has_no_4x4_valid_grid_test_function(self) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — no valid 4×4 happy path."""
        # Given
        module_path = Path(__file__)
        tree = ast.parse(module_path.read_text(encoding="utf-8"))

        # When
        test_names = [
            node.name
            for node in ast.walk(tree)
            if isinstance(node, ast.FunctionDef) and node.name.startswith("test_")
        ]

        # Then
        assert not any("valid" in name and "4x4" in name for name in test_names)  # AC-FR-01-01
        assert not any("happy_path_success" in name for name in test_names)

    def test_module_has_no_forbidden_ac_fr_01_02_to_05_test_names(self) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — no AC-FR-01-02~05 test IDs."""
        # Given
        module_path = Path(__file__)
        source = module_path.read_text(encoding="utf-8").lower()

        # When / Then
        for fragment in ("ac_fr_01_02", "ac_fr_01_03", "ac_fr_01_04", "ac_fr_01_05"):
            assert fragment not in source  # AC-FR-01-01

    def test_module_has_no_fr_02_to_05_references_in_test_names(self) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — no FR-02~05 scope."""
        # Given
        tree = ast.parse(Path(__file__).read_text(encoding="utf-8"))

        # When
        test_names = [
            node.name.lower()
            for node in ast.walk(tree)
            if isinstance(node, ast.FunctionDef) and node.name.startswith("test_")
        ]

        # Then
        for name in test_names:
            for forbidden in FORBIDDEN_TEST_NAME_FRAGMENTS:
                if forbidden in ("fr_02", "fr_03", "fr_04", "fr_05"):
                    assert forbidden not in name  # AC-FR-01-01

    def test_module_has_no_4x3_or_5x5_grid_literal_tests(self) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — 4×3, 5×5 excluded from AC."""
        # Given
        source = Path(__file__).read_text(encoding="utf-8")

        # When / Then
        assert "range(5)" not in source  # AC-FR-01-01 — no 5×5
        assert "* 3 for" not in source  # AC-FR-01-01 — no 4×3
        assert "for _ in range(4)]" in source or "range(3)" in source

    def test_module_docstring_declares_ac_fr_01_01_only(self) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — module scope declaration."""
        # Given
        module_path = Path(__file__)

        # When
        docstring = ast.get_docstring(ast.parse(module_path.read_text(encoding="utf-8")))

        # Then
        assert docstring is not None  # AC-FR-01-01
        assert "AC-FR-01-01" in docstring
        assert "INVALID_SIZE" in docstring
