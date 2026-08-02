"""Compatibility imports for the original gridworld module path."""

from __future__ import annotations

from .environments.gridworld import (
    ACTIONS,
    DEFAULT_LAYOUT,
    DELTAS,
    Action,
    GridWorld,
    Position,
)

__all__ = ["ACTIONS", "Action", "DEFAULT_LAYOUT", "DELTAS", "GridWorld", "Position"]
