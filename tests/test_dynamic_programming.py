import unittest

from krybor_rl.algorithms.dynamic_programming import (
    policy_evaluation,
    policy_iteration,
    uniform_random_policy,
    value_iteration,
)
from krybor_rl.environments.gridworld import Action, GridWorld


class DynamicProgrammingTests(unittest.TestCase):
    def test_value_iteration_solves_a_tiny_deterministic_grid(self) -> None:
        grid = GridWorld(("S.G",), slip=0.0, goal_reward=10.0)
        result = value_iteration(grid, gamma=0.9, theta=1e-12)
        self.assertAlmostEqual(result.values[(0, 1)], 10.0)
        self.assertAlmostEqual(result.values[(0, 0)], 8.0)
        self.assertIn(Action.EAST, result.policy[(0, 0)])
        self.assertIn(Action.EAST, result.policy[(0, 1)])
        self.assertEqual(result.values[(0, 2)], 0.0)

    def test_policy_evaluation_keeps_terminal_value_zero(self) -> None:
        grid = GridWorld(("S.G",), slip=0.0)
        result = policy_evaluation(
            grid, uniform_random_policy(grid), gamma=0.9, theta=1e-10
        )
        self.assertEqual(result.values[(0, 2)], 0.0)
        self.assertLess(result.deltas[-1], 1e-10)

    def test_policy_and_value_iteration_agree(self) -> None:
        grid = GridWorld(slip=0.1)
        policy_result = policy_iteration(grid, gamma=0.95, theta=1e-10)
        value_result = value_iteration(grid, gamma=0.95, theta=1e-10)
        max_difference = max(
            abs(policy_result.values[state] - value_result.values[state])
            for state in grid.states
        )
        self.assertLess(max_difference, 1e-7)

    def test_actuator_uncertainty_changes_the_route(self) -> None:
        certain_grid = GridWorld(slip=0.0)
        noisy_grid = GridWorld(slip=0.35)
        certain_plan = value_iteration(certain_grid, gamma=0.95, theta=1e-10)
        noisy_plan = value_iteration(noisy_grid, gamma=0.95, theta=1e-10)
        self.assertIn(Action.EAST, certain_plan.policy[certain_grid.start_state])
        self.assertIn(Action.SOUTH, noisy_plan.policy[noisy_grid.start_state])


if __name__ == "__main__":
    unittest.main()
