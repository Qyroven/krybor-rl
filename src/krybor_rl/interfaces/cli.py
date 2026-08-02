"""Command-line interface for learning and reproducible experiments."""

from __future__ import annotations

import argparse
from collections.abc import Sequence
from pathlib import Path
from types import SimpleNamespace

from ..algorithms.dynamic_programming import (
    policy_evaluation,
    policy_iteration,
    uniform_random_policy,
    value_iteration,
)
from ..environments.gridworld import GridWorld
from ..evaluation.bandits import run_bandit_experiment
from ..evaluation.rollouts import run_episode
from ..visualization.text import format_layout, format_policy, format_values
from .config import ExperimentConfigError, load_experiment_config, table


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="krybor-rl",
        description="Reinforcement learning rebuilt from first principles.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    bandit = subparsers.add_parser("bandit", help="compare epsilon-greedy agents")
    bandit.add_argument("--epsilons", nargs="+", type=float, default=[0.0, 0.01, 0.1])
    bandit.add_argument("--actions", type=int, default=10)
    bandit.add_argument("--steps", type=int, default=1_000)
    bandit.add_argument("--runs", type=int, default=200)
    bandit.add_argument("--seed", type=int, default=7)
    bandit.set_defaults(handler=_run_bandit)

    plan = subparsers.add_parser("plan", help="solve or evaluate the rescue gridworld")
    _add_planning_arguments(plan)
    plan.add_argument(
        "--algorithm",
        choices=("evaluation", "policy-iteration", "value-iteration"),
        default="value-iteration",
    )
    plan.add_argument("--seed", type=int, default=7, help="rollout seed")
    plan.add_argument("--max-steps", type=int, default=100, help="rollout limit")
    plan.add_argument("--no-rollout", action="store_true")
    plan.set_defaults(handler=_run_plan)

    compare = subparsers.add_parser(
        "compare", help="verify that policy and value iteration agree"
    )
    _add_planning_arguments(compare)
    compare.set_defaults(handler=_run_compare)

    run = subparsers.add_parser("run", help="run a versioned TOML experiment config")
    run.add_argument("config", type=Path)
    run.set_defaults(handler=_run_config)
    return parser


def _add_planning_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--gamma", type=float, default=0.95)
    parser.add_argument("--theta", type=float, default=1e-9)
    parser.add_argument("--slip", type=float, default=0.10)


def _run_bandit(args: argparse.Namespace | SimpleNamespace) -> None:
    experiment = run_bandit_experiment(
        epsilons=tuple(args.epsilons),
        number_of_actions=args.actions,
        steps=args.steps,
        runs=args.runs,
        seed=args.seed,
    )
    window = min(100, experiment.steps)
    print(
        f"{experiment.number_of_actions}-armed stationary testbed | "
        f"{experiment.runs} runs x {experiment.steps} steps"
    )
    print(f"Metrics are averaged over the final {window} steps.\n")
    print(f"{'epsilon':>9}  {'average reward':>14}  {'optimal action':>14}")
    for curve in experiment.curves:
        print(
            f"{curve.epsilon:9.3f}  {curve.final_average_reward(window):14.3f}  "
            f"{curve.final_optimal_action_rate(window):13.1%}"
        )


def _run_plan(args: argparse.Namespace | SimpleNamespace) -> None:
    grid = GridWorld(slip=args.slip)
    if args.algorithm == "evaluation":
        policy = uniform_random_policy(grid)
        result = policy_evaluation(grid, policy, gamma=args.gamma, theta=args.theta)
        values = result.values
        heading = "Iterative policy evaluation of the equiprobable random policy"
        convergence = f"{result.sweeps} sweeps; final delta={result.deltas[-1]:.3g}"
    elif args.algorithm == "policy-iteration":
        plan = policy_iteration(grid, gamma=args.gamma, theta=args.theta)
        policy = plan.policy
        values = plan.values
        heading = "Policy iteration"
        convergence = (
            f"{plan.policy_iterations} policy improvements; "
            f"{plan.sweeps} evaluation sweeps; final delta={plan.deltas[-1]:.3g}"
        )
    else:
        plan = value_iteration(grid, gamma=args.gamma, theta=args.theta)
        policy = plan.policy
        values = plan.values
        heading = "Value iteration"
        convergence = f"{plan.sweeps} sweeps; final delta={plan.deltas[-1]:.3g}"

    print(heading)
    print(f"gamma={args.gamma:g}, theta={args.theta:g}, slip={args.slip:g}")
    print(convergence)
    print("\nMap\n---")
    print(format_layout(grid))
    print("\nState values\n------------")
    print(format_values(grid, values))
    print("\nPolicy\n------")
    print(format_policy(grid, policy))

    if not args.no_rollout:
        episode = run_episode(grid, policy, seed=args.seed, max_steps=args.max_steps)
        path = [str(grid.start_state)] + [str(step.next_state) for step in episode.steps]
        print("\nOne sampled rollout (for inspection, not learning)")
        print("--------------------------------------------------")
        print(" -> ".join(path))
        status = "terminal reached" if episode.terminated else "step limit reached"
        print(
            f"{status}; steps={len(episode.steps)}; "
            f"undiscounted reward={episode.total_reward:g}"
        )


def _run_compare(args: argparse.Namespace | SimpleNamespace) -> None:
    grid = GridWorld(slip=args.slip)
    policy_result = policy_iteration(grid, gamma=args.gamma, theta=args.theta)
    value_result = value_iteration(grid, gamma=args.gamma, theta=args.theta)
    difference = max(
        abs(policy_result.values[state] - value_result.values[state])
        for state in grid.states
    )
    print(f"gamma={args.gamma:g}, theta={args.theta:g}, slip={args.slip:g}")
    print(
        "policy iteration: "
        f"{policy_result.policy_iterations} improvements, {policy_result.sweeps} sweeps"
    )
    print(f"value iteration:  {value_result.sweeps} sweeps")
    print(f"maximum |V_policy_iteration - V_value_iteration| = {difference:.3g}")
    print("agreement:", "yes" if difference < max(args.theta * 10, 1e-7) else "not yet")


def _run_config(args: argparse.Namespace) -> None:
    config = load_experiment_config(args.config)
    experiment = table(config, "experiment")
    kind = experiment["kind"]

    if kind == "bandit":
        settings = table(config, "bandit")
        _print_config_header(args.config, experiment.get("name"))
        _run_bandit(
            SimpleNamespace(
                epsilons=settings.get("epsilons", [0.0, 0.01, 0.1]),
                actions=settings.get("actions", 10),
                steps=settings.get("steps", 1_000),
                runs=settings.get("runs", 200),
                seed=settings.get("seed", 7),
            )
        )
        return

    environment = table(config, "environment")
    algorithm = table(config, "algorithm")
    rollout = table(config, "rollout")
    algorithm_name = algorithm.get("name", "value-iteration")
    if algorithm_name not in {"evaluation", "policy-iteration", "value-iteration"}:
        raise ExperimentConfigError(
            "algorithm.name must be 'evaluation', 'policy-iteration', or "
            "'value-iteration'"
        )
    _print_config_header(args.config, experiment.get("name"))
    _run_plan(
        SimpleNamespace(
            algorithm=algorithm_name,
            gamma=algorithm.get("gamma", 0.95),
            theta=algorithm.get("theta", 1e-9),
            slip=environment.get("slip", 0.10),
            seed=rollout.get("seed", 7),
            max_steps=rollout.get("max_steps", 100),
            no_rollout=not rollout.get("enabled", True),
        )
    )


def _print_config_header(path: Path, name: object) -> None:
    if isinstance(name, str) and name:
        print(f"experiment: {name}")
    print(f"config: {path}")


def main(argv: Sequence[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        args.handler(args)
    except ExperimentConfigError as error:
        parser.error(str(error))
