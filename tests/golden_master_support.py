"""Golden Master (Approval) helpers for MagicSquare_xx solver output regression."""

from __future__ import annotations

import difflib
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

from boundary.models import FailureResult
from entity.constants import GRID_SIZE, SOLUTION_VECTOR_LENGTH
from entity.solver import find_missing_numbers, is_magic_square, locate_empty_cells

if TYPE_CHECKING:
    from boundary.screen_boundary import ScreenBoundary

SECTION_SEPARATOR = "________________________________________"
GOLDEN_MASTER_PATH = Path(__file__).resolve().parent / "golden_master_expected.txt"

# Requirement aliases → runtime Error Contract codes (DTO serialization uses runtime).
ERROR_CONTRACT_ALIASES: dict[str, str] = {
    "INVALID_BLANK_COUNT": "EMPTY_COUNT_INVALID",
    "DUPLICATE_NUMBER": "DUPLICATE_NONZERO",
    "NO_VALID_MAGIC_SQUARE": "NO_VALID_COMPLETION",
}


@dataclass(frozen=True)
class GoldenMasterCase:
    """One Golden Master test case (GM-TC-XX)."""

    test_id: str
    title: str
    grid: list[list[int]]
    contract_alias: str | None = None


GOLDEN_MASTER_CASES: tuple[GoldenMasterCase, ...] = (
    GoldenMasterCase(
        test_id="GM-TC-01",
        title="정상 조합 성공 (small-first)",
        grid=[
            [16, 2, 3, 13],
            [5, 11, 10, 8],
            [9, 7, 0, 12],
            [4, 14, 0, 1],
        ],
    ),
    GoldenMasterCase(
        test_id="GM-TC-02",
        title="reverse 조합 성공 (small-first 실패 → reverse)",
        grid=[
            [16, 2, 3, 13],
            [5, 11, 10, 8],
            [9, 7, 0, 12],
            [4, 14, 15, 0],
        ],
    ),
    GoldenMasterCase(
        test_id="GM-TC-03",
        title="INVALID_BLANK_COUNT",
        grid=[
            [16, 2, 3, 13],
            [5, 11, 10, 8],
            [9, 7, 0, 12],
            [4, 14, 0, 0],
        ],
        contract_alias="INVALID_BLANK_COUNT",
    ),
    GoldenMasterCase(
        test_id="GM-TC-04",
        title="DUPLICATE_NUMBER",
        grid=[
            [16, 2, 3, 13],
            [5, 11, 10, 8],
            [9, 7, 0, 12],
            [4, 14, 7, 0],
        ],
        contract_alias="DUPLICATE_NUMBER",
    ),
    GoldenMasterCase(
        test_id="GM-TC-05",
        title="NO_VALID_MAGIC_SQUARE",
        grid=[
            [16, 2, 3, 13],
            [5, 0, 11, 8],
            [9, 6, 0, 12],
            [4, 15, 14, 1],
        ],
        contract_alias="NO_VALID_MAGIC_SQUARE",
    ),
)


@dataclass(frozen=True)
class GoldenSection:
    """One scenario block parsed from the golden master file."""

    name: str
    input_text: str
    output_text: str | None
    error_code: str | None


def format_grid(grid: list[list[int]]) -> str:
    """Render a 4×4 grid as space-separated rows."""
    return "\n".join(" ".join(str(cell) for cell in row) for row in grid)


def serialize_result(result: FailureResult | list[int]) -> str:
    """Serialize ScreenBoundary.submit() API result for golden master comparison."""
    if isinstance(result, FailureResult):
        return f"Error:\n{result.code}"
    compact = ",".join(str(value) for value in result)
    return f"Output:\n[{compact}]"


def format_section(
    section_id: str,
    grid: list[list[int]],
    result: FailureResult | list[int],
) -> str:
    """Format one golden master scenario section."""
    return (
        f"[{section_id}]\n"
        f"Input:\n{format_grid(grid)}\n"
        f"{serialize_result(result)}"
    )


def capture_scenario(
    case: GoldenMasterCase,
    boundary: ScreenBoundary,
) -> str:
    """Run one GM-TC through the boundary and return its section text."""
    result = boundary.submit(case.grid)
    return format_section(case.test_id, case.grid, result)


def build_golden_document(boundary: ScreenBoundary) -> str:
    """Build the full golden master document from all registered scenarios."""
    sections = [capture_scenario(case, boundary) for case in GOLDEN_MASTER_CASES]
    return f"\n{SECTION_SEPARATOR}\n\n".join(sections) + "\n"


def parse_golden_document(text: str) -> dict[str, GoldenSection]:
    """Parse golden master text into sections keyed by GM-TC id."""
    raw_sections = [
        chunk.strip() for chunk in text.split(SECTION_SEPARATOR) if chunk.strip()
    ]
    parsed: dict[str, GoldenSection] = {}

    for chunk in raw_sections:
        lines = chunk.splitlines()
        if not lines or not lines[0].startswith("[") or not lines[0].endswith("]"):
            msg = f"Invalid section header: {lines[0] if lines else '<empty>'}"
            raise ValueError(msg)

        name = lines[0][1:-1]
        try:
            input_index = lines.index("Input:")
        except ValueError as exc:
            msg = f"Section [{name}] is missing 'Input:'"
            raise ValueError(msg) from exc

        output_index = None
        error_index = None
        for index, line in enumerate(lines):
            if line == "Output:":
                output_index = index
            elif line == "Error:":
                error_index = index

        if output_index is not None:
            output_text = lines[output_index + 1].strip()
            error_code = None
            input_end = output_index
        elif error_index is not None:
            output_text = None
            error_code = lines[error_index + 1].strip()
            input_end = error_index
        else:
            msg = f"Section [{name}] must contain Output: or Error:"
            raise ValueError(msg)

        input_text = "\n".join(lines[input_index + 1 : input_end]).strip()
        parsed[name] = GoldenSection(
            name=name,
            input_text=input_text,
            output_text=output_text,
            error_code=error_code,
        )

    return parsed


def unified_diff(expected: str, actual: str, label: str) -> str:
    """Return unified diff: --- expected / +++ actual / @@ line diff @@."""
    return "".join(
        difflib.unified_diff(
            expected.splitlines(keepends=True),
            actual.splitlines(keepends=True),
            fromfile="expected",
            tofile="actual",
            lineterm="",
        ),
    )


def write_golden_master(content: str, path: Path = GOLDEN_MASTER_PATH) -> Path:
    """Write golden master baseline to disk."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path


def read_expected(path: Path = GOLDEN_MASTER_PATH) -> str:
    """Read golden master baseline (open(expected).read() pattern)."""
    return path.read_text(encoding="utf-8")


def _expected_vector(grid: list[list[int]], *, small_first: bool) -> list[int]:
    """Build the output contract vector for a given combination strategy."""
    first_empty, second_empty = locate_empty_cells(grid)
    smaller, larger = find_missing_numbers(grid)
    if small_first:
        n1, n2 = smaller, larger
    else:
        n1, n2 = larger, smaller
    return [
        first_empty[0],
        first_empty[1],
        n1,
        second_empty[0],
        second_empty[1],
        n2,
    ]


def _filled_grid(grid: list[list[int]], vector: list[int]) -> list[list[int]]:
    filled = [row[:] for row in grid]
    filled[vector[0] - 1][vector[1] - 1] = vector[2]
    filled[vector[3] - 1][vector[4] - 1] = vector[5]
    return filled


def assert_success_output_contract(
    grid: list[list[int]],
    vector: list[int],
    *,
    strategy: str,
) -> None:
    """Assert int[6] format, row-major blanks, 1-index, and combination strategy."""
    assert len(vector) == SOLUTION_VECTOR_LENGTH
    assert all(isinstance(value, int) for value in vector)

    first_empty, second_empty = locate_empty_cells(grid)
    smaller, larger = find_missing_numbers(grid)

    assert vector[0] == first_empty[0]
    assert vector[1] == first_empty[1]
    assert vector[3] == second_empty[0]
    assert vector[4] == second_empty[1]

    for coord in (vector[0], vector[1], vector[3], vector[4]):
        assert 1 <= coord <= GRID_SIZE

    assert {vector[2], vector[5]} == {smaller, larger}
    assert vector[2] != vector[5]
    assert is_magic_square(_filled_grid(grid, vector))

    if strategy == "small_first":
        assert vector == _expected_vector(grid, small_first=True)
    elif strategy == "reverse":
        assert vector == _expected_vector(grid, small_first=False)
    else:
        msg = f"Unknown strategy: {strategy}"
        raise ValueError(msg)


def assert_failure_error_contract(
    result: FailureResult,
    *,
    contract_alias: str,
) -> None:
    """Assert FailureResult matches the Error Contract (runtime code)."""
    expected_code = ERROR_CONTRACT_ALIASES.get(contract_alias, contract_alias)
    assert result.code == expected_code
    assert isinstance(result.message, str) and result.message


def assert_section_matches_golden(
    actual_section: str,
    *,
    test_id: str,
    path: Path = GOLDEN_MASTER_PATH,
    approve: bool = False,
) -> None:
    """Compare one GM-TC section using open(expected).read() vs actual."""
    if approve or not path.exists():
        return

    expected_document = read_expected(path)
    sections = parse_golden_document(expected_document)
    if test_id not in sections:
        return

    expected_section = format_section_from_parsed(sections[test_id])
    if actual_section == expected_section:
        return

    diff = unified_diff(expected_section, actual_section, test_id)
    msg = (
        f"[{test_id}] Golden master mismatch.\n"
        "Approve baseline update:\n"
        "  pytest -m golden_master --approve-golden -v\n"
        "  python scripts/generate_golden_master.py --approve\n\n"
        f"{diff}"
    )
    raise AssertionError(msg)


def format_section_from_parsed(section: GoldenSection) -> str:
    """Reconstruct section text from a parsed golden section."""
    lines = [f"[{section.name}]", "Input:", section.input_text]
    if section.output_text is not None:
        lines.extend(["Output:", section.output_text])
    else:
        lines.extend(["Error:", section.error_code or ""])
    return "\n".join(lines)


def assert_golden_master(
    actual: str,
    *,
    path: Path = GOLDEN_MASTER_PATH,
    approve: bool = False,
) -> None:
    """Compare or approve the full golden master document.

    - Missing baseline: write ``actual`` and pass (bootstrap).
    - ``approve=True``: overwrite baseline with ``actual`` and pass.
    - Otherwise: open(expected).read() vs actual with unified diff on mismatch.
    """
    if approve or not path.exists():
        write_golden_master(actual, path)
        return

    expected = read_expected(path)
    if actual == expected:
        return

    diff = unified_diff(expected, actual, "golden_master_expected.txt")
    msg = (
        "Golden master mismatch. Re-run with approval to update baseline:\n"
        "  pytest -m golden_master --approve-golden -v\n"
        "  python scripts/generate_golden_master.py --approve\n\n"
        f"{diff}"
    )
    raise AssertionError(msg)
