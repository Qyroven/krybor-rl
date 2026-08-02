import unittest

from krybor_rl.core.mdp import validate_mdp
from krybor_rl.environments.gridworld import Action, GridWorld


class GridWorldTests(unittest.TestCase):
    def test_every_state_action_is_a_probability_distribution(self) -> None:
        grid = GridWorld()
        validate_mdp(grid)
        for state in grid.states:
            for action in grid.actions(state):
                self.assertAlmostEqual(
                    sum(item.probability for item in grid.transitions(state, action)), 1.0
                )

    def test_slips_into_walls_are_aggregated(self) -> None:
        grid = GridWorld(("S.G", "...", "..X"), slip=0.2)
        outcomes = grid.transitions((0, 0), Action.NORTH)
        self.assertEqual(len(outcomes), 2)
        by_state = {item.next_state: item for item in outcomes}
        self.assertAlmostEqual(by_state[(0, 0)].probability, 0.9)
        self.assertEqual(by_state[(0, 0)].reward, grid.collision_reward)
        self.assertAlmostEqual(by_state[(0, 1)].probability, 0.1)

    def test_terminal_states_have_no_actions(self) -> None:
        grid = GridWorld(("SG",), slip=0.0)
        self.assertEqual(grid.actions((0, 1)), ())


if __name__ == "__main__":
    unittest.main()
