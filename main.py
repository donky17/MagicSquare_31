"""MagicSquare_xx — PyQt GUI entry point."""

from __future__ import annotations

import sys
from pathlib import Path

_SRC = Path(__file__).resolve().parent / "src"
_src_str = str(_SRC)
if _src_str not in sys.path:
    sys.path.insert(0, _src_str)

from PyQt6.QtWidgets import QApplication

from boundary.screen_boundary import ScreenBoundary
from boundary.ui.main_window import MainWindow
from control.solve import resolve


def main() -> int:
    """Launch the MagicSquare_xx desktop application."""
    app = QApplication(sys.argv)
    app.setApplicationName("MagicSquare_xx")
    boundary = ScreenBoundary(resolve=resolve)
    window = MainWindow(boundary)
    window.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
