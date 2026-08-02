import unittest
from random import Random

from krybor_rl.agents.epsilon_greedy import EpsilonGreedyAgent
from krybor_rl.environments.bandits import GaussianBandit
from krybor_rl.evaluation.bandits import run_bandit_experiment


class EpsilonGreedyTests(unittest.TestCase):
    def test_gaussian_bandit_exposes_its_optimal_action(self) -> None:
        bandit = GaussianBandit((-1.0, 2.0, 0.5), reward_stddev=0.0)
        self.assertEqual(bandit.optimal_action, 1)
        self.assertEqual(bandit.sample_reward(1, Random(1)), 2.0)

    def test_incremental_update_is_a_sample_average(self) -> None:
        agent = EpsilonGreedyAgent(2, epsilon=0.1, rng=Random(1))
        for reward in (2.0, 4.0, 9.0):
            agent.update(1, reward)
        self.assertAlmostEqual(agent.estimates[1], 5.0)
        self.assertEqual(agent.counts[1], 3)

    def test_experiment_is_reproducible_and_well_formed(self) -> None:
        first = run_bandit_experiment(epsilons=(0.0, 0.1), steps=20, runs=10, seed=3)
        second = run_bandit_experiment(epsilons=(0.0, 0.1), steps=20, runs=10, seed=3)
        self.assertEqual(first, second)
        self.assertEqual(len(first.curves), 2)
        for curve in first.curves:
            self.assertEqual(len(curve.average_rewards), 20)
            self.assertTrue(all(0.0 <= rate <= 1.0 for rate in curve.optimal_action_rates))


if __name__ == "__main__":
    unittest.main()
