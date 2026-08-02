# Vision and scope

## Mission

Krybor RL should become a compact, inspectable body of reinforcement-learning
knowledge: equations connected to code, code connected to experiments, and
experiments connected to honest written conclusions.

The repository should answer three questions for every major method:

1. What problem and assumptions does it encode?
2. Why does its update rule make sense?
3. What evidence shows the implementation behaves as claimed?

## Principles

- **First principles before frameworks.** Use small implementations to expose the
  update rule and data flow.
- **One core, many domains.** Environments are replaceable. Robotics, games,
  recommendation, operations research, and control can consume the same RL core.
- **Evidence over screenshots.** Prefer seeded configs, aggregate metrics,
  invariants, and written conclusions.
- **Progress without pretending.** Distinguish code availability from personal
  mastery.
- **Complexity must be earned.** Add dependencies when they solve a demonstrated
  problem, not because a mature stack commonly contains them.

## Current scope

The current scope is pure reinforcement learning through small tabular problems.
ROS 2, Gazebo, MuJoCo, Isaac, PyTorch, distributed training, and experiment
tracking services are intentionally absent.

They may be integrated later behind clean interfaces after the corresponding RL
questions require them. A future robotics specialization should be a consumer or
adjacent project, never a reason to distort the foundations.

## What success looks like

At maturity, a reader can start from a lab question, trace the implementation to
the exact mathematical update, reproduce the result from a config, inspect the
tests guarding it, and read a concise account of what was learned.
