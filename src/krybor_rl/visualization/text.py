"""Readable text renderers for tabular values and policies."""

from __future__ import annotations

from typing import Mapping

from ..environments.gridworld import Action, GridWorld, Position

ARROWS = {
    Action.NORTH: "↑",
    Action.EAST: "→",
    Action.SOUTH: "↓",
    Action.WEST: "←",
}


def format_values(grid: GridWorld, values: Mapping[Position, float]) -> str:
    rows: list[str] = []
    for row in range(grid.height):
        cells: list[str] = []
        for column in range(grid.width):
            symbol = grid.layout[row][column]
            state = (row, column)
            if symbol == "#":
                cells.append("########")
            elif symbol == "G":
                cells.append(" GOAL   ")
            elif symbol == "X":
                cells.append(" HAZARD ")
            else:
                cells.append(f"{values[state]:8.2f}")
        rows.append(" ".join(cells))
    return "\n".join(rows)


def format_policy(
    grid: GridWorld, policy: Mapping[Position, Mapping[Action, float]]
) -> str:
    rows: list[str] = []
    for row in range(grid.height):
        cells: list[str] = []
        for column in range(grid.width):
            symbol = grid.layout[row][column]
            state = (row, column)
            if symbol == "#":
                cells.append("#####")
            elif symbol == "G":
                cells.append(" GOAL")
            elif symbol == "X":
                cells.append(" FAIL")
            else:
                actions = "".join(
                    ARROWS[action]
                    for action in grid.actions(state)
                    if policy[state].get(action, 0.0) > 0.0
                )
                marker = "S" if symbol == "S" else " "
                cells.append(f"{marker}{actions:^4}")
        rows.append(" ".join(cells))
    return "\n".join(rows)


def format_layout(grid: GridWorld) -> str:
    return "\n".join(grid.layout)
