# Chapter 4 — Dynamic programming

Dynamic programming assumes a complete model and turns Bellman equations into
iterative expected updates.

## Reconstruct in this order

1. One expected action-value backup.
2. Iterative policy evaluation for a fixed equiprobable policy.
3. Greedy policy improvement.
4. Policy iteration.
5. Value iteration.

For each method, identify the estimate, target, sweep stopping rule, and whether
the update performs prediction or control. The implementation lives in
`algorithms/dynamic_programming.py`.

## Experiments

```bash
PYTHONPATH=src python -m krybor_rl plan --algorithm evaluation
PYTHONPATH=src python -m krybor_rl plan --algorithm policy-iteration
PYTHONPATH=src python -m krybor_rl run experiments/configs/ch04_value_iteration.toml
PYTHONPATH=src python -m krybor_rl compare
```

Change `slip` from `0` to `0.35`. Predict when the policy will abandon the short
route beside the hazards. Then vary `gamma` and `theta` separately and explain
which changes the objective and which changes numerical convergence.

## Boundary before Chapter 5

The planner calls `transitions` and sums over all outcomes. A sampled rollout at
the end only inspects the policy; it does not update values. Monte Carlo begins
when complete sampled returns become the learning target.

## Done when

- [ ] You can write policy-evaluation and optimality backups without copying.
- [ ] A hand-computable grid produces the expected values.
- [ ] Policy iteration and value iteration agree within a justified tolerance.
- [ ] You can explain the policy-stability tie case.
- [ ] Your journal records the uncertainty experiment and its route change.
