"""Tabular dynamic-programming algorithms from Chapter 4."""

from __future__ import annotations

from dataclasses import dataclass
from math import isclose
from typing import Hashable, Mapping, TypeVar

from ..core.mdp import FiniteMDP, Policy, validate_mdp, validate_policy

State = TypeVar("State", bound=Hashable)
Action = TypeVar("Action", bound=Hashable)


class ConvergenceError(RuntimeError):
    """Raised when an iterative algorithm exceeds its safety limit."""


@dataclass(frozen=True, slots=True)
class EvaluationResult:
    values: dict[State, float]
    sweeps: int
    deltas: tuple[float, ...]


@dataclass(frozen=True, slots=True)
class PlanningResult:
    values: dict[State, float]
    policy: Policy
    sweeps: int
    deltas: tuple[float, ...]
    policy_iterations: int
    algorithm: str


def uniform_random_policy(mdp: FiniteMDP[State, Action]) -> Policy:
    policy: Policy = {}
    for state in mdp.states:
        actions = mdp.actions(state)
        if actions:
            probability = 1.0 / len(actions)
            policy[state] = {action: probability for action in actions}
    return policy


def expected_action_value(
    mdp: FiniteMDP[State, Action],
    state: State,
    action: Action,
    values: Mapping[State, float],
    gamma: float,
) -> float:
    """Perform one expected Bellman backup for a state-action pair."""

    return sum(
        outcome.probability
        * (
            outcome.reward
            + gamma * (0.0 if outcome.terminated else values[outcome.next_state])
        )
        for outcome in mdp.transitions(state, action)
    )


def policy_evaluation(
    mdp: FiniteMDP[State, Action],
    policy: Mapping[State, Mapping[Action, float]],
    *,
    gamma: float = 0.95,
    theta: float = 1e-9,
    initial_values: Mapping[State, float] | None = None,
    in_place: bool = True,
    max_sweeps: int = 100_000,
) -> EvaluationResult:
    """Estimate ``v_pi`` with iterative expected updates."""

    _validate_parameters(gamma, theta, max_sweeps)
    validate_mdp(mdp)
    validate_policy(mdp, policy)
    values = {state: float((initial_values or {}).get(state, 0.0)) for state in mdp.states}
    for state in mdp.states:
        if mdp.is_terminal(state):
            values[state] = 0.0

    deltas: list[float] = []
    for sweep in range(1, max_sweeps + 1):
        source = values if in_place else values.copy()
        delta = 0.0
        for state in mdp.states:
            if mdp.is_terminal(state):
                continue
            old_value = values[state]
            values[state] = sum(
                probability
                * expected_action_value(mdp, state, action, source, gamma)
                for action, probability in policy[state].items()
            )
            delta = max(delta, abs(old_value - values[state]))
        deltas.append(delta)
        if delta < theta:
            return EvaluationResult(values, sweep, tuple(deltas))

    raise ConvergenceError(f"policy evaluation did not converge in {max_sweeps} sweeps")


def greedy_actions(
    mdp: FiniteMDP[State, Action],
    state: State,
    values: Mapping[State, float],
    gamma: float,
    *,
    tolerance: float = 1e-12,
) -> tuple[Action, ...]:
    action_values = {
        action: expected_action_value(mdp, state, action, values, gamma)
        for action in mdp.actions(state)
    }
    best_value = max(action_values.values())
    return tuple(
        action
        for action, value in action_values.items()
        if isclose(value, best_value, rel_tol=0.0, abs_tol=tolerance)
    )


def greedy_policy(
    mdp: FiniteMDP[State, Action],
    values: Mapping[State, float],
    gamma: float,
) -> Policy:
    """Return a stochastic greedy policy, sharing probability across exact ties."""

    policy: Policy = {}
    for state in mdp.states:
        if mdp.is_terminal(state):
            continue
        best_actions = greedy_actions(mdp, state, values, gamma)
        probability = 1.0 / len(best_actions)
        policy[state] = {action: probability for action in best_actions}
    return policy


def policy_iteration(
    mdp: FiniteMDP[State, Action],
    *,
    gamma: float = 0.95,
    theta: float = 1e-9,
    max_policy_iterations: int = 1_000,
    max_evaluation_sweeps: int = 100_000,
) -> PlanningResult:
    """Alternate complete policy evaluation and greedy improvement."""

    _validate_parameters(gamma, theta, max_evaluation_sweeps)
    validate_mdp(mdp)
    policy = uniform_random_policy(mdp)
    values = {state: 0.0 for state in mdp.states}
    all_deltas: list[float] = []
    total_sweeps = 0

    for iteration in range(1, max_policy_iterations + 1):
        evaluation = policy_evaluation(
            mdp,
            policy,
            gamma=gamma,
            theta=theta,
            initial_values=values,
            max_sweeps=max_evaluation_sweeps,
        )
        values = evaluation.values
        total_sweeps += evaluation.sweeps
        all_deltas.extend(evaluation.deltas)

        stable = True
        improved: Policy = {}
        for state in mdp.states:
            if mdp.is_terminal(state):
                continue
            old_action = max(policy[state], key=policy[state].get)
            best_actions = greedy_actions(mdp, state, values, gamma)
            chosen_action = old_action if old_action in best_actions else best_actions[0]
            improved[state] = {chosen_action: 1.0}
            old_policy_is_chosen_action = (
                len(policy[state]) == 1
                and policy[state].get(chosen_action, 0.0) == 1.0
            )
            stable = stable and old_policy_is_chosen_action
        policy = improved

        if stable:
            return PlanningResult(
                values,
                policy,
                total_sweeps,
                tuple(all_deltas),
                iteration,
                "policy iteration",
            )

    raise ConvergenceError(
        f"policy iteration did not stabilize in {max_policy_iterations} improvements"
    )


def value_iteration(
    mdp: FiniteMDP[State, Action],
    *,
    gamma: float = 0.95,
    theta: float = 1e-9,
    max_sweeps: int = 100_000,
) -> PlanningResult:
    """Apply Bellman optimality backups until the values stabilize."""

    _validate_parameters(gamma, theta, max_sweeps)
    validate_mdp(mdp)
    values = {state: 0.0 for state in mdp.states}
    deltas: list[float] = []

    for sweep in range(1, max_sweeps + 1):
        delta = 0.0
        for state in mdp.states:
            if mdp.is_terminal(state):
                continue
            old_value = values[state]
            values[state] = max(
                expected_action_value(mdp, state, action, values, gamma)
                for action in mdp.actions(state)
            )
            delta = max(delta, abs(old_value - values[state]))
        deltas.append(delta)
        if delta < theta:
            return PlanningResult(
                values,
                greedy_policy(mdp, values, gamma),
                sweep,
                tuple(deltas),
                0,
                "value iteration",
            )

    raise ConvergenceError(f"value iteration did not converge in {max_sweeps} sweeps")


def _validate_parameters(gamma: float, theta: float, max_sweeps: int) -> None:
    if not 0.0 <= gamma <= 1.0:
        raise ValueError("gamma must be between 0 and 1")
    if theta <= 0.0:
        raise ValueError("theta must be positive")
    if max_sweeps < 1:
        raise ValueError("max_sweeps must be positive")
