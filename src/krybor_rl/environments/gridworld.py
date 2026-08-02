"""A small stochastic gridworld with an explicit finite-MDP model."""

from __future__ import annotations

from collections import defaultdict
from enum import Enum
from random import Random

from ..core.mdp import Transition, validate_mdp

Position = tuple[int, int]


class Action(str, Enum):
    NORTH = "N"
    EAST = "E"
    SOUTH = "S"
    WEST = "W"


ACTIONS = (Action.NORTH, Action.EAST, Action.SOUTH, Action.WEST)

DELTAS = {
    Action.NORTH: (-1, 0),
    Action.EAST: (0, 1),
    Action.SOUTH: (1, 0),
    Action.WEST: (0, -1),
}

DEFAULT_LAYOUT = (
    "S......G",
    ".XXXXXX.",
    "....#...",
    "........",
)


class GridWorld:
    """Known stochastic dynamics for the Krybor rescue task.

    ``slip`` is split evenly between the directions perpendicular to the chosen
    action. Entering ``G`` or ``X`` terminates the episode. Terminal rewards are
    received on entry, so terminal state values themselves remain zero.
    """

    def __init__(
        self,
        layout: tuple[str, ...] = DEFAULT_LAYOUT,
        *,
        slip: float = 0.10,
        step_reward: float = -1.0,
        collision_reward: float = -2.0,
        goal_reward: float = 20.0,
        hazard_reward: float = -20.0,
    ) -> None:
        if not layout or not layout[0]:
            raise ValueError("layout cannot be empty")
        if len({len(row) for row in layout}) != 1:
            raise ValueError("all layout rows must have equal width")
        if not 0.0 <= slip <= 1.0:
            raise ValueError("slip must be between 0 and 1")

        valid_symbols = {"S", ".", "#", "G", "X"}
        unknown = set("".join(layout)) - valid_symbols
        if unknown:
            raise ValueError(f"unknown layout symbols: {sorted(unknown)}")
        if sum(row.count("S") for row in layout) != 1:
            raise ValueError("layout must contain exactly one start S")
        if sum(row.count("G") for row in layout) < 1:
            raise ValueError("layout must contain at least one goal G")

        self.layout = layout
        self.height = len(layout)
        self.width = len(layout[0])
        self.slip = slip
        self.step_reward = step_reward
        self.collision_reward = collision_reward
        self.goal_reward = goal_reward
        self.hazard_reward = hazard_reward

        self._states = tuple(
            (row, column)
            for row in range(self.height)
            for column in range(self.width)
            if layout[row][column] != "#"
        )
        self.start_state = next(
            state for state in self._states if self.symbol(state) == "S"
        )
        validate_mdp(self)

    @property
    def states(self) -> tuple[Position, ...]:
        return self._states

    def symbol(self, state: Position) -> str:
        row, column = state
        return self.layout[row][column]

    def is_terminal(self, state: Position) -> bool:
        return self.symbol(state) in {"G", "X"}

    def actions(self, state: Position) -> tuple[Action, ...]:
        return () if self.is_terminal(state) else ACTIONS

    def transitions(self, state: Position, action: Action) -> tuple[Transition, ...]:
        if action not in self.actions(state):
            raise ValueError(f"action {action!r} is unavailable in state {state!r}")

        index = ACTIONS.index(action)
        left = ACTIONS[(index - 1) % len(ACTIONS)]
        right = ACTIONS[(index + 1) % len(ACTIONS)]
        directions = (
            (action, 1.0 - self.slip),
            (left, self.slip / 2.0),
            (right, self.slip / 2.0),
        )

        combined: defaultdict[tuple[Position, float, bool], float] = defaultdict(float)
        for actual_action, probability in directions:
            if probability == 0.0:
                continue
            outcome = self._move(state, actual_action)
            combined[outcome] += probability

        return tuple(
            Transition(probability, next_state, reward, terminated)
            for (next_state, reward, terminated), probability in combined.items()
        )

    def sample_transition(
        self, state: Position, action: Action, rng: Random
    ) -> Transition:
        """Sample one outcome; planning itself always enumerates ``transitions``."""

        outcomes = self.transitions(state, action)
        return rng.choices(
            outcomes,
            weights=[item.probability for item in outcomes],
            k=1,
        )[0]

    def _move(self, state: Position, action: Action) -> tuple[Position, float, bool]:
        row_delta, column_delta = DELTAS[action]
        candidate = (state[0] + row_delta, state[1] + column_delta)
        row, column = candidate
        if (
            row < 0
            or row >= self.height
            or column < 0
            or column >= self.width
            or self.layout[row][column] == "#"
        ):
            return state, self.collision_reward, False

        symbol = self.symbol(candidate)
        if symbol == "G":
            return candidate, self.goal_reward, True
        if symbol == "X":
            return candidate, self.hazard_reward, True
        return candidate, self.step_reward, False
