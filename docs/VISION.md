# Vision and scope

This document summarizes the direction. The authoritative product definition and
current delivery boundary live in [product/PRODUCT.md](product/PRODUCT.md) and
[product/V1_SCOPE.md](product/V1_SCOPE.md).

## Mission

Krybor RL should become an executable visual map of reinforcement-learning
knowledge: concepts connected to equations, equations connected to code, code
connected to experiments and applications, and experiments connected to guided
practice and honest written conclusions.

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

## Current implementation scope

The implemented baseline remains pure reinforcement learning through small tabular
problems. ROS 2, Gazebo, MuJoCo, Isaac, PyTorch, distributed training, and
experiment-tracking services are intentionally absent from the RL core today.

The next product milestone is a public, account-free Chapter 1 vertical slice with
structured content, a visual knowledge graph, concept pages, two interactive
experiences, a learning path, local progress, and a stateless Python computation
API. Infrastructure grows alongside the product through a separate supporting
[roadmap](infrastructure/ROADMAP.md).

Robotics, AI assistance, cloud services, Kubernetes, and other advanced consumers
may be integrated behind clean interfaces after a product or learning milestone
requires them. A future specialization should consume the foundations, never
distort them.

## What success looks like

At maturity, a learner can navigate from a knowledge-graph question to its
prerequisites, visualize the behavior, trace the implementation to the exact
mathematical update, reproduce the result from a config, inspect the tests guarding
it, complete a mastery task, and connect the method to real applications.
