"""Sample policy rollouts for inspecting a plan, not for updating it."""

from __future__ import annotations

from random import Random
from typing import Mapping

from ..core.trajectory import EpisodeResult, EpisodeStep
from ..environments.gridworld import Action, GridWorld, Position


def run_episode(
    grid: GridWorld,
    policy: Mapping[Position, Mapping[Action, float]],
    *,
    seed: int = 7,
    max_steps: int = 100,
) -> EpisodeResult[Position, Action]:
    """Sample one trajectory from a fixed policy."""

    if max_steps < 1:
        raise ValueError("max_steps must be positive")
    rng = Random(seed)
    state = grid.start_state
    steps: list[EpisodeStep[Position, Action]] = []
    total_reward = 0.0

    for time in range(max_steps):
        action_probabilities = policy[state]
        actions = tuple(action_probabilities)
        action = rng.choices(
            actions,
            weights=[action_probabilities[item] for item in actions],
            k=1,
        )[0]
        outcome = grid.sample_transition(state, action, rng)
        steps.append(
            EpisodeStep(
                time,
                state,
                action,
                outcome.reward,
                outcome.next_state,
                outcome.terminated,
            )
        )
        total_reward += outcome.reward
        state = outcome.next_state
        if outcome.terminated:
            return EpisodeResult(tuple(steps), total_reward, True)

    return EpisodeResult(tuple(steps), total_reward, False)
