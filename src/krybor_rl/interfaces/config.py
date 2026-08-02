"""Load small, reproducible experiment definitions from TOML."""

from __future__ import annotations

import tomllib
from pathlib import Path
from typing import Any


class ExperimentConfigError(ValueError):
    """Raised when an experiment config cannot be interpreted."""


def load_experiment_config(path: Path) -> dict[str, Any]:
    """Read a TOML config and validate its top-level experiment kind."""

    try:
        with path.open("rb") as stream:
            config = tomllib.load(stream)
    except FileNotFoundError as error:
        raise ExperimentConfigError(f"config does not exist: {path}") from error
    except tomllib.TOMLDecodeError as error:
        raise ExperimentConfigError(f"invalid TOML in {path}: {error}") from error

    experiment = config.get("experiment")
    if not isinstance(experiment, dict):
        raise ExperimentConfigError("config requires an [experiment] table")
    if experiment.get("kind") not in {"bandit", "planning"}:
        raise ExperimentConfigError(
            "experiment.kind must be either 'bandit' or 'planning'"
        )
    return config


def table(config: dict[str, Any], name: str) -> dict[str, Any]:
    """Return a TOML table or fail with a config-focused error."""

    value = config.get(name, {})
    if not isinstance(value, dict):
        raise ExperimentConfigError(f"[{name}] must be a TOML table")
    return value
