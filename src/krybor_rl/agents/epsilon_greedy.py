"""Sample-average epsilon-greedy action selection."""

from __future__ import annotations

from random import Random


class EpsilonGreedyAgent:
    """Estimate action values with sample averages and explore with probability epsilon."""

    def __init__(self, number_of_actions: int, epsilon: float, rng: Random) -> None:
        if number_of_actions < 1:
            raise ValueError("number_of_actions must be positive")
        if not 0.0 <= epsilon <= 1.0:
            raise ValueError("epsilon must be between 0 and 1")
        self.epsilon = epsilon
        self.rng = rng
        self.estimates = [0.0] * number_of_actions
        self.counts = [0] * number_of_actions

    def select_action(self) -> int:
        if self.rng.random() < self.epsilon:
            return self.rng.randrange(len(self.estimates))
        best_value = max(self.estimates)
        ties = [
            action
            for action, estimate in enumerate(self.estimates)
            if estimate == best_value
        ]
        return self.rng.choice(ties)

    def update(self, action: int, reward: float) -> None:
        self.counts[action] += 1
        step_size = 1.0 / self.counts[action]
        self.estimates[action] += step_size * (reward - self.estimates[action])
