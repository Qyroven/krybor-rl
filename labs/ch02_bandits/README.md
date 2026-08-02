# Chapter 2 — Multi-armed bandits

The bandit removes state transitions so exploration and action-value estimation
can be studied in isolation.

## Reconstruct

Implement on paper and then trace in code:

```text
Q_{n+1}(A_n) = Q_n(A_n) + 1/N_n(A_n) * [R_n - Q_n(A_n)]
```

Map the action count, step size, reward error, and estimate to
`agents/epsilon_greedy.py`. Explain why random tie-breaking matters before any
action has been tried.

## Experiment

```bash
PYTHONPATH=src python -m krybor_rl run experiments/configs/ch02_bandit.toml
```

Before running, rank epsilon `0`, `0.01`, and `0.1` by early reward and by final
optimal-action rate. The run averages independent bandits; do not infer a general
result from one trajectory.

Then make one change at a time:

- increase the number of actions;
- compare more epsilon values;
- reduce the number of runs and observe metric noise;
- create a non-stationary variant only after the stationary case is understood.

## Done when

- [ ] You can derive the incremental sample average from the ordinary mean.
- [ ] You can explain how greedy selection gets trapped by early reward noise.
- [ ] A test catches an incorrect step size.
- [ ] A journal entry contains a prediction and aggregated result.
