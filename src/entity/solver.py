"""Pure domain logic for partial-grid validation and two-blank solving."""

from __future__ import annotations

from entity.constants import (
    BLANK_VALUE,
    EXPECTED_BLANK_COUNT,
    GRID_SIZE,
    MAGIC_CONSTANT,
    MAX_CELL_VALUE,
    MIN_CELL_VALUE,
)
from entity.exceptions import DomainError

_ERROR_MESSAGES: dict[str, str] = {
    "EMPTY_COUNT_INVALID": "빈칸(0)은 정확히 2개여야 합니다.",
    "VALUE_RANGE_INVALID": "0이 아닌 값은 1~16이어야 합니다.",
    "DUPLICATE_NONZERO": "0을 제외한 값은 중복될 수 없습니다.",
    "NO_VALID_COMPLETION": "주어진 빈칸에 유효한 마방진 완성이 없습니다.",
}


def _raise(code: str) -> None:
    raise DomainError(code=code, message=_ERROR_MESSAGES[code])


def validate_partial_grid(grid: list[list[int]]) -> None:
    """Validate P-2~P-5 for a 4×4 grid (P-1 is enforced at boundary)."""
    blank_count = sum(cell == BLANK_VALUE for row in grid for cell in row)
    if blank_count != EXPECTED_BLANK_COUNT:
        _raise("EMPTY_COUNT_INVALID")

    nonzero_values: list[int] = []
    for row in grid:
        for value in row:
            if value == BLANK_VALUE:
                continue
            if not MIN_CELL_VALUE <= value <= MAX_CELL_VALUE:
                _raise("VALUE_RANGE_INVALID")
            nonzero_values.append(value)

    if len(nonzero_values) != len(set(nonzero_values)):
        _raise("DUPLICATE_NONZERO")


def locate_empty_cells(grid: list[list[int]]) -> tuple[tuple[int, int], tuple[int, int]]:
    """Return row-major 1-indexed coordinates of the two blank cells."""
    blanks: list[tuple[int, int]] = []
    for row_index in range(GRID_SIZE):
        for col_index in range(GRID_SIZE):
            if grid[row_index][col_index] == BLANK_VALUE:
                blanks.append((row_index + 1, col_index + 1))
    return blanks[0], blanks[1]


def find_missing_numbers(grid: list[list[int]]) -> tuple[int, int]:
    """Return missing values as (smaller, larger)."""
    present = {
        grid[row_index][col_index]
        for row_index in range(GRID_SIZE)
        for col_index in range(GRID_SIZE)
        if grid[row_index][col_index] != BLANK_VALUE
    }
    missing = sorted(
        set(range(MIN_CELL_VALUE, MAX_CELL_VALUE + 1)) - present,
    )
    return missing[0], missing[1]


def _line_sums(grid: list[list[int]]) -> list[int]:
    sums: list[int] = []
    for row_index in range(GRID_SIZE):
        sums.append(sum(grid[row_index][col_index] for col_index in range(GRID_SIZE)))
    for col_index in range(GRID_SIZE):
        sums.append(sum(grid[row_index][col_index] for row_index in range(GRID_SIZE)))
    sums.append(sum(grid[index][index] for index in range(GRID_SIZE)))
    sums.append(
        sum(grid[index][GRID_SIZE - 1 - index] for index in range(GRID_SIZE)),
    )
    return sums


def is_magic_square(grid: list[list[int]]) -> bool:
    """Return whether a completed grid satisfies I-1~I-7."""
    values = [
        grid[row_index][col_index]
        for row_index in range(GRID_SIZE)
        for col_index in range(GRID_SIZE)
    ]
    if set(values) != set(range(MIN_CELL_VALUE, MAX_CELL_VALUE + 1)):
        return False
    line_sums = _line_sums(grid)
    return len(set(line_sums)) == 1 and line_sums[0] == MAGIC_CONSTANT


def _fill_grid(
    grid: list[list[int]],
    first_cell: tuple[int, int],
    first_value: int,
    second_cell: tuple[int, int],
    second_value: int,
) -> list[list[int]]:
    filled = [row[:] for row in grid]
    filled[first_cell[0] - 1][first_cell[1] - 1] = first_value
    filled[second_cell[0] - 1][second_cell[1] - 1] = second_value
    return filled


def solve(grid: list[list[int]]) -> list[int]:
    """Solve a two-blank partial grid and return the output contract vector."""
    validate_partial_grid(grid)
    first_empty, second_empty = locate_empty_cells(grid)
    smaller, larger = find_missing_numbers(grid)

    small_first = _fill_grid(grid, first_empty, smaller, second_empty, larger)
    if is_magic_square(small_first):
        return [
            first_empty[0],
            first_empty[1],
            smaller,
            second_empty[0],
            second_empty[1],
            larger,
        ]

    large_first = _fill_grid(grid, first_empty, larger, second_empty, smaller)
    if is_magic_square(large_first):
        return [
            first_empty[0],
            first_empty[1],
            larger,
            second_empty[0],
            second_empty[1],
            smaller,
        ]

    _raise("NO_VALID_COMPLETION")
