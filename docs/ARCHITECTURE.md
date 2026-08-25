# Architecture

This document describes the implemented Python RL architecture. The planned web,
API, content, and infrastructure boundaries are specified separately in
[architecture/SYSTEM.md](architecture/SYSTEM.md).

Krybor RL separates the learning journey from the reusable software system.
Folders under `labs/` follow the curriculum; packages under `src/` follow stable
technical responsibilities.

## Dependency direction

```text
interfaces ---> algorithms --------> core
          |--> evaluation ---------> agents
          |         |--------------> environments ---> core
          |--> visualization ------> environments
          |--> environments
```

Lower layers must not import higher layers. In particular:

- environments define dynamics and rewards, never learning updates;
- algorithms operate on protocols and data structures from `core/`;
- evaluation owns repeated runs, seeds, aggregation, and rollouts;
- visualization formats results but does not compute them;
- interfaces translate user input into calls to the system.

## Package responsibilities

| Package | Owns | Must not own |
| --- | --- | --- |
| `core` | MDP contracts, transitions, trajectories | Specific environments or algorithms |
| `environments` | States, actions, dynamics, reward mechanics | Value updates or policy improvement |
| `agents` | Action selection and agent-local estimates | Experiment loops |
| `algorithms` | Prediction, control, planning updates | CLI, plotting, domain stories |
| `evaluation` | Runs, seeds, metrics, rollout collection | Environment mechanics |
| `visualization` | Text, plots, tables | Algorithm decisions |
| `interfaces` | CLI, config parsing | Mathematical logic |

The flat modules such as `krybor_rl.bandits` are small compatibility imports for
the initial repository API. New implementation belongs in the packages above.

## Learning artifacts versus product code

- `labs/` may contain partial derivations, deliberately incomplete exercises,
  scratch comparisons, and chapter-specific explanations.
- `src/` only receives code that is reusable, typed, tested, and independent of a
  single notebook or experiment.
- `experiments/configs/` stores inputs required to reproduce a claim.
- `results/` stores small outputs worth reviewing in Git; large generated artifacts
  stay outside version control.
- `journal/` stores the learner's predictions, mistakes, and corrected model.

## Adding the next algorithm

For first-visit Monte Carlo prediction:

1. Define the question and derivation in `labs/ch05_monte_carlo/`.
2. Reuse `core/trajectory.py` rather than inventing a chapter-specific episode type.
3. Add the update to `algorithms/monte_carlo.py`.
4. Use an environment through sampled interaction; do not call its full transition
   model from the learning algorithm.
5. Add unit tests for first-visit behavior and return calculation.
6. Add a seeded config and a result comparing estimates with the DP ground truth.

That comparison reuses Chapter 4 as an oracle while preserving the conceptual
boundary between expected and sampled updates.
