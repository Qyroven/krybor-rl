import unittest

from krybor_rl.algorithms.dynamic_programming import value_iteration
from krybor_rl.environments.gridworld import GridWorld
from krybor_rl.evaluation.rollouts import run_episode


class SimulationTests(unittest.TestCase):
    def test_deterministic_optimal_policy_reaches_goal(self) -> None:
        grid = GridWorld(("S.G",), slip=0.0, goal_reward=10.0)
        plan = value_iteration(grid, gamma=0.9, theta=1e-12)
        episode = run_episode(grid, plan.policy, seed=1, max_steps=10)
        self.assertTrue(episode.terminated)
        self.assertEqual(len(episode.steps), 2)
        self.assertEqual(episode.total_reward, 9.0)


if __name__ == "__main__":
    unittest.main()
