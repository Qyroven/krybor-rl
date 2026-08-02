"""Minimal types for a finite Markov decision process.

The interface represents the complete environment model required by dynamic
programming. It deliberately exposes every outcome rather than a sampling-only
``step`` method.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isclose
from typing import Hashable, Mapping, Protocol, TypeAlias, TypeVar

State = TypeVar("State", bound=Hashable)
Action = TypeVar("Action", bound=Hashable)


@dataclass(frozen=True, slots=True)
class Transition:
    """One possible outcome of taking an action in a state."""

    probability: float
    next_state: State
    reward: float
    terminated: bool = False


class FiniteMDP(Protocol[State, Action]):
    """The model operations needed by the tabular DP algorithms."""

    @property
    def states(self) -> tuple[State, ...]: ...

    def actions(self, state: State) -> tuple[Action, ...]: ...

    def transitions(self, state: State, action: Action) -> tuple[Transition, ...]: ...

    def is_terminal(self, state: State) -> bool: ...


Policy: TypeAlias = dict[State, dict[Action, float]]


def validate_mdp(mdp: FiniteMDP[State, Action]) -> None:
    """Raise ``ValueError`` if the finite model is not a probability model."""

    known_states = set(mdp.states)
    if not known_states:
        raise ValueError("an MDP must contain at least one state")

    for state in mdp.states:
        actions = mdp.actions(state)
        if mdp.is_terminal(state):
            if actions:
                raise ValueError(f"terminal state {state!r} must not expose actions")
            continue
        if not actions:
            raise ValueError(f"nonterminal state {state!r} has no actions")

        for action in actions:
            outcomes = mdp.transitions(state, action)
            if not outcomes:
                raise ValueError(f"{state!r}, {action!r} has no outcomes")
            total = 0.0
            for outcome in outcomes:
                if outcome.probability < 0.0:
                    raise ValueError("transition probabilities cannot be negative")
                if outcome.next_state not in known_states:
                    raise ValueError(f"unknown next state {outcome.next_state!r}")
                if outcome.terminated != mdp.is_terminal(outcome.next_state):
                    raise ValueError("terminated must agree with the next state's type")
                total += outcome.probability
            if not isclose(total, 1.0, rel_tol=0.0, abs_tol=1e-12):
                raise ValueError(
                    f"probabilities for {state!r}, {action!r} sum to {total}, not 1"
                )


def validate_policy(
    mdp: FiniteMDP[State, Action], policy: Mapping[State, Mapping[Action, float]]
) -> None:
    """Check that a policy is a distribution over available actions in every state."""

    for state in mdp.states:
        if mdp.is_terminal(state):
            continue
        if state not in policy:
            raise ValueError(f"policy is missing state {state!r}")

        available = set(mdp.actions(state))
        probabilities = policy[state]
        if set(probabilities) - available:
            raise ValueError(f"policy contains an unavailable action in {state!r}")
        if any(probability < 0.0 for probability in probabilities.values()):
            raise ValueError("policy probabilities cannot be negative")
        total = sum(probabilities.values())
        if not isclose(total, 1.0, rel_tol=0.0, abs_tol=1e-12):
            raise ValueError(f"policy probabilities in {state!r} sum to {total}, not 1")
