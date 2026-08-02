import tempfile
import unittest
from contextlib import redirect_stderr
from io import StringIO
from pathlib import Path

from krybor_rl.interfaces.config import ExperimentConfigError, load_experiment_config
from krybor_rl.interfaces.cli import main


class ExperimentConfigTests(unittest.TestCase):
    def test_unknown_experiment_kind_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "invalid.toml"
            path.write_text('[experiment]\nkind = "telepathy"\n', encoding="utf-8")
            with self.assertRaises(ExperimentConfigError):
                load_experiment_config(path)

    def test_missing_config_is_reported_as_a_config_error(self) -> None:
        with self.assertRaises(ExperimentConfigError):
            load_experiment_config(Path("does-not-exist.toml"))

    def test_unknown_planning_algorithm_is_rejected_by_cli(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "invalid.toml"
            path.write_text(
                '[experiment]\nkind = "planning"\n\n'
                '[algorithm]\nname = "magic"\n',
                encoding="utf-8",
            )
            with redirect_stderr(StringIO()), self.assertRaises(SystemExit) as error:
                main(["run", str(path)])
            self.assertEqual(error.exception.code, 2)


if __name__ == "__main__":
    unittest.main()
