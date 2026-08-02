# Chapter 3 — Finite Markov decision processes

This lab turns the agent-environment story into a probability model that dynamic
programming can enumerate.

## Reconstruct

For one nonterminal GridWorld state and one action, manually list every
`(probability, next_state, reward, terminated)` outcome. Confirm that the
probabilities sum to one and that terminal rewards are received on entry.

Questions to settle:

1. Why is position a sufficient state for the current GridWorld?
2. What hidden variable would break the Markov property?
3. Why is the goal state's own value zero when entering it yields `+20`?
4. Which objects describe dynamics, a policy, a return, `v_pi`, and `q_pi`?

Relevant code:

- `core/mdp.py` defines the model contract and invariants.
- `environments/gridworld.py` supplies one model.
- `tests/test_gridworld.py` checks its probability structure.

## Experiment

Run the equiprobable policy:

```bash
PYTHONPATH=src python -m krybor_rl plan --algorithm evaluation
```

Predict which states have the lowest value and justify the answer using possible
returns, not visual distance alone.

## Done when

- [ ] You can write `p(s', r | s, a)` for a real transition by hand.
- [ ] You can diagnose a non-Markov state representation.
- [ ] You can distinguish a terminal-entry reward from terminal-state value.
- [ ] The model validator rejects malformed transition probabilities.
