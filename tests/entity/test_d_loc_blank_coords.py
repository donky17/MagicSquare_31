"""D-LOC-01 — find_blank_coords RED skeleton (Report/09). Domain Mock 금지."""

from __future__ import annotations

import pytest


class TestDLoc01BlankCoords:
    """D-LOC-01 — G1 row-major 빈칸 (2,2), (3,3) 1-index."""

    def test_d_loc_01_g1_row_major_blank_coords(self) -> None:
        # Given: G1
        # When: find_blank_coords(G1)
        # from entity.services.empty_cell_locator import find_blank_coords
        pytest.fail("RED: D-LOC-01 — G1 → (2,2), (3,3) row-major 1-index")
