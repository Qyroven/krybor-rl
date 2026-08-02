"""Stationary Gaussian multi-armed bandit testbed."""

from __future__ import annotations

from dataclasses import dataclass
from random import Random


@dataclass(frozen=True, slots=True)
class GaussianBandit:
    """A one-state environment with normally distributed rewards."""

    action_values: tuple[float, ...]
    reward_stddev: float = 1.0

    def __post_init__(self) -> None:
        if not self.action_values:
            raise ValueError("a bandit must expose at least one action")
        if self.reward_stddev < 0.0:
            raise ValueError("reward_stddev cannot be negative")

    @property
    def number_of_actions(self) -> int:
        return len(self.action_values)

    @property
    def optimal_action(self) -> int:
        return max(range(self.number_of_actions), key=self.action_values.__getitem__)

    def sample_reward(self, action: int, rng: Random) -> float:
        if not 0 <= action < self.number_of_actions:
            raise ValueError(f"unknown action index: {action}")
        return rng.gauss(self.action_values[action], self.reward_stddev)
