"""Compatibility imports for the original Chapter 2 module path."""

from .agents.epsilon_greedy import EpsilonGreedyAgent
from .evaluation.bandits import BanditCurve, BanditExperiment, run_bandit_experiment

__all__ = [
    "BanditCurve",
    "BanditExperiment",
    "EpsilonGreedyAgent",
    "run_bandit_experiment",
]
