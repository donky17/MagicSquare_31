"""Boundary response models (Input/Output/Error contract)."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class FailureResult(BaseModel):
    """Validation failure payload (Error Contract)."""

    model_config = ConfigDict(frozen=True)

    code: str
    message: str
