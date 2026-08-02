"""Trajectory records shared by sampled reinforcement-learning methods."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, Hashable, TypeVar

State = TypeVar("State", bound=Hashable)
Action = TypeVar("Action", bound=Hashable)


@dataclass(frozen=True, slots=True)
class EpisodeStep(Generic[State, Action]):
    time: int
    state: State
    action: Action
    reward: float
    next_state: State
    terminated: bool


@dataclass(frozen=True, slots=True)
class EpisodeResult(Generic[State, Action]):
    steps: tuple[EpisodeStep[State, Action], ...]
    total_reward: float
    terminated: bool
