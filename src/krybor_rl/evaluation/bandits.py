"""Evaluation harness for stationary bandit agents."""

from __future__ import annotations

from dataclasses import dataclass
from random import Random
from statistics import fmean

from ..agents.epsilon_greedy import EpsilonGreedyAgent
from ..environments.bandits import GaussianBandit


@dataclass(frozen=True, slots=True)
class BanditCurve:
    epsilon: float
    average_rewards: tuple[float, ...]
    optimal_action_rates: tuple[float, ...]

    def final_average_reward(self, window: int = 100) -> float:
        return fmean(self.average_rewards[-min(window, len(self.average_rewards)) :])

    def final_optimal_action_rate(self, window: int = 100) -> float:
        return fmean(self.optimal_action_rates[-min(window, len(self.optimal_action_rates)) :])


@dataclass(frozen=True, slots=True)
class BanditExperiment:
    number_of_actions: int
    steps: int
    runs: int
    curves: tuple[BanditCurve, ...]


def run_bandit_experiment(
    *,
    epsilons: tuple[float, ...] = (0.0, 0.01, 0.1),
    number_of_actions: int = 10,
    steps: int = 1_000,
    runs: int = 200,
    seed: int = 7,
) -> BanditExperiment:
    """Average epsilon-greedy behavior over independently sampled bandits."""

    if number_of_actions < 1 or steps < 1 or runs < 1:
        raise ValueError("actions, steps, and runs must all be positive")
    if not epsilons:
        raise ValueError("provide at least one epsilon")

    testbed_rng = Random(seed)
    testbed = tuple(
        GaussianBandit(
            tuple(testbed_rng.gauss(0.0, 1.0) for _ in range(number_of_actions))
        )
        for _ in range(runs)
    )
    curves: list[BanditCurve] = []

    for method_index, epsilon in enumerate(epsilons):
        reward_totals = [0.0] * steps
        optimal_totals = [0] * steps
        for run, bandit in enumerate(testbed):
            rng = Random(seed + 1_000_003 * (method_index + 1) + 10_007 * run)
            agent = EpsilonGreedyAgent(number_of_actions, epsilon, rng)
            for step in range(steps):
                action = agent.select_action()
                reward = bandit.sample_reward(action, rng)
                agent.update(action, reward)
                reward_totals[step] += reward
                optimal_totals[step] += action == bandit.optimal_action

        curves.append(
            BanditCurve(
                epsilon=epsilon,
                average_rewards=tuple(total / runs for total in reward_totals),
                optimal_action_rates=tuple(total / runs for total in optimal_totals),
            )
        )

    return BanditExperiment(number_of_actions, steps, runs, tuple(curves))
