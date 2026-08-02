# Chapter 1 — Foundations

Chapter 1 is not skipped. Its artifact is a precise mental and software model,
not a large standalone algorithm.

## Reconstruct

For the rescue GridWorld, identify:

- the agent and environment boundary;
- observation/state, action, reward, and next state;
- the return being optimized;
- the difference between a policy and a value function;
- what is known by the agent versus hidden in the environment;
- why reward is the objective signal rather than a sequence of instructions.

Draw one loop and map every arrow to current code under
`src/krybor_rl/environments/gridworld.py` and
`src/krybor_rl/evaluation/rollouts.py`.

## Experiment

Change exactly one reward in a temporary branch or working change. Predict the
behavior before solving the MDP, then run:

```bash
PYTHONPATH=src python -m krybor_rl plan --algorithm value-iteration
```

Explain whether the change modified the environment's objective, its dynamics,
or both.

## Done when

- [ ] You can narrate a complete agent-environment transition without notes.
- [ ] You can explain why an agent may maximize reward while violating the
      designer's actual intention.
- [ ] Your journal contains one reward-design prediction and observation.
- [ ] You can say which later concepts require the Markov property.
