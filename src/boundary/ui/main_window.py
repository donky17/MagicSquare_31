"""Main window — 4×4 grid input and solve result display."""

from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from boundary.models import FailureResult
from boundary.screen_boundary import GRID_SIZE, ScreenBoundary
from entity.constants import BLANK_VALUE, MAX_CELL_VALUE

SAMPLE_GRID: list[list[int]] = [
    [16, 2, 3, 13],
    [5, 11, 10, 8],
    [9, 7, 0, 12],
    [4, 14, 15, 0],
]


class MainWindow(QMainWindow):
    """4×4 magic square puzzle GUI."""

    def __init__(self, boundary: ScreenBoundary) -> None:
        super().__init__()
        self._boundary = boundary
        self._cells: list[list[QLineEdit]] = []
        self._setup_ui()

    def _setup_ui(self) -> None:
        self.setWindowTitle("MagicSquare_xx — 4×4 마방진 퍼즐")
        self.setMinimumSize(520, 560)

        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setSpacing(12)

        title = QLabel("4×4 마방진 — 빈칸 2개를 채워 완성하세요")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(13)
        title_font.setBold(True)
        title.setFont(title_font)
        root.addWidget(title)

        hint = QLabel("0 = 빈칸 · 1~16 숫자 입력 · 중복 금지(0 제외)")
        hint.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hint.setStyleSheet("color: #555;")
        root.addWidget(hint)

        grid_box = QGroupBox("격자 입력")
        grid_layout = QGridLayout(grid_box)
        grid_layout.setSpacing(6)

        cell_font = QFont()
        cell_font.setPointSize(14)

        for row in range(GRID_SIZE):
            row_cells: list[QLineEdit] = []
            for col in range(GRID_SIZE):
                cell = QLineEdit()
                cell.setAlignment(Qt.AlignmentFlag.AlignCenter)
                cell.setFont(cell_font)
                cell.setMaxLength(2)
                cell.setFixedSize(72, 48)
                cell.setPlaceholderText("0")
                grid_layout.addWidget(cell, row, col)
                row_cells.append(cell)
            self._cells.append(row_cells)

        root.addWidget(grid_box)

        button_row = QHBoxLayout()
        solve_btn = QPushButton("해결")
        solve_btn.setMinimumHeight(36)
        solve_btn.clicked.connect(self._on_solve)
        clear_btn = QPushButton("초기화")
        clear_btn.setMinimumHeight(36)
        clear_btn.clicked.connect(self._on_clear)
        sample_btn = QPushButton("샘플 불러오기")
        sample_btn.setMinimumHeight(36)
        sample_btn.clicked.connect(self._on_load_sample)
        button_row.addWidget(solve_btn)
        button_row.addWidget(clear_btn)
        button_row.addWidget(sample_btn)
        root.addLayout(button_row)

        result_box = QGroupBox("결과")
        result_layout = QVBoxLayout(result_box)
        self._result_label = QLabel("격자를 입력한 뒤 「해결」을 누르세요.")
        self._result_label.setWordWrap(True)
        self._result_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        result_layout.addWidget(self._result_label)
        root.addWidget(result_box)

        self._on_load_sample()

    def _read_grid(self) -> list[list[int]] | FailureResult:
        grid: list[list[int]] = []
        for row_index, row_cells in enumerate(self._cells):
            row_values: list[int] = []
            for col_index, cell in enumerate(row_cells):
                text = cell.text().strip()
                if text == "":
                    row_values.append(BLANK_VALUE)
                    continue
                try:
                    value = int(text)
                except ValueError:
                    return FailureResult(
                        code="UI_PARSE_ERROR",
                        message=f"({row_index + 1},{col_index + 1}) 칸에 올바른 정수를 입력하세요.",
                    )
                if value < BLANK_VALUE or value > MAX_CELL_VALUE:
                    return FailureResult(
                        code="UI_CELL_RANGE",
                        message="셀 값은 0 또는 1~16이어야 합니다.",
                    )
                row_values.append(value)
            grid.append(row_values)
        return grid

    def _show_failure(self, failure: FailureResult) -> None:
        self._result_label.setStyleSheet("color: #c0392b;")
        self._result_label.setText(f"[{failure.code}] {failure.message}")

    def _show_success(self, solution: list[int]) -> None:
        self._result_label.setStyleSheet("color: #1e8449;")
        r1, c1, n1, r2, c2, n2 = solution
        self._result_label.setText(
            "해결 성공!\n\n"
            f"첫 번째 빈칸 ({r1},{c1}) → {n1}\n"
            f"두 번째 빈칸 ({r2},{c2}) → {n2}\n\n"
            f"출력 벡터: [{', '.join(str(v) for v in solution)}]"
        )
        self._apply_solution_to_grid(solution)

    def _apply_solution_to_grid(self, solution: list[int]) -> None:
        r1, c1, n1, r2, c2, n2 = solution
        self._cells[r1 - 1][c1 - 1].setText(str(n1))
        self._cells[r2 - 1][c2 - 1].setText(str(n2))

    def _on_solve(self) -> None:
        parsed = self._read_grid()
        if isinstance(parsed, FailureResult):
            self._show_failure(parsed)
            return

        result = self._boundary.submit(parsed)
        if isinstance(result, FailureResult):
            self._show_failure(result)
            return
        self._show_success(result)

    def _on_clear(self) -> None:
        for row_cells in self._cells:
            for cell in row_cells:
                cell.clear()
        self._result_label.setStyleSheet("")
        self._result_label.setText("격자를 입력한 뒤 「해결」을 누르세요.")

    def _on_load_sample(self) -> None:
        for row_index, row in enumerate(SAMPLE_GRID):
            for col_index, value in enumerate(row):
                self._cells[row_index][col_index].setText(
                    "" if value == BLANK_VALUE else str(value),
                )
        self._result_label.setStyleSheet("")
        self._result_label.setText("샘플 퍼즐이 로드되었습니다. 「해결」을 누르세요.")
