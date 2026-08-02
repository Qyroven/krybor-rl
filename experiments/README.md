# Experiments

An experiment config is a versioned answer to “exactly what did you run?” Keep
inputs under `configs/`; keep only small, interpretable outputs under `results/`.

Run a config with:

```bash
krybor-rl run experiments/configs/ch02_bandit.toml
```

When adding one, include the question and prediction in a journal entry. Seeds
make a run reproducible; repeated independent runs make a stochastic comparison
credible.
