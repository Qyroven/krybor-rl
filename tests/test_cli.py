import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

from krybor_rl.interfaces.cli import main


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


class CommandLineTests(unittest.TestCase):
    def test_small_bandit_run(self) -> None:
        output = StringIO()
        with redirect_stdout(output):
            main(["bandit", "--actions", "3", "--steps", "4", "--runs", "2"])
        self.assertIn("3-armed stationary testbed", output.getvalue())
        self.assertIn("optimal action", output.getvalue())

    def test_versioned_planning_config_runs(self) -> None:
        config = REPOSITORY_ROOT / "experiments/configs/ch04_value_iteration.toml"
        output = StringIO()
        with redirect_stdout(output):
            main(["run", str(config)])
        self.assertIn("Value iteration", output.getvalue())
        self.assertIn("One sampled rollout", output.getvalue())


if __name__ == "__main__":
    unittest.main()
